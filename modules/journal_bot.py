import streamlit as st
import pandas as pd
import io

def run(user):
    st.subheader("📥 Journal Entries & Accrual Suggestions")
    uploaded = st.file_uploader("Upload Trial Balance or Transactions (CSV/XLSX)", type=["xlsx","csv"], key="journal_uploader")
    if uploaded is not None:
        if "journal_file_bytes" not in st.session_state:
            try:
                st.session_state["journal_file_bytes"] = uploaded.read()
                st.success("File uploaded and cached in session.")
            except Exception as e:
                st.error("Failed to read uploaded file.")
                st.exception(e)
                return

        try:
            file_bytes = st.session_state.get("journal_file_bytes")
            if uploaded.name.endswith('.csv'):
                df = pd.read_csv(io.BytesIO(file_bytes))
            else:
                df = pd.read_excel(io.BytesIO(file_bytes), engine='openpyxl')
        except Exception as e:
            st.error("Failed to parse the uploaded journal file.")
            st.exception(e)
            return

        if df.empty:
            st.warning("Uploaded file has no data.")
            return

        st.write("Preview:")
        st.dataframe(df.head(10))

        # Simple heuristics: find unpaid expenses or accrual-like descriptions
        keywords = ['accrual','accrued','payable','accrued expense','expense']
        mask = df.apply(lambda row: row.astype(str).str.lower().str.contains('|'.join(keywords)).any(), axis=1)
        accruals = df[mask]
        st.success(f"Found {len(accruals)} possible accrual-related rows.")
        if not accruals.empty:
            st.dataframe(accruals.head(50))

        if st.button("Generate Sample Journal Entries from accruals"):
            entries = []
            for _, r in accruals.head(20).iterrows():
                desc = r.astype(str).to_dict()
                # simplistic entry template
                entries.append({
                    'Dr': 'Accrual Expense A/c',
                    'Cr': 'Accrual Liability A/c',
                    'Amount': desc.get('Amount') or desc.get('amount') or 'TBD',
                    'Narration': str(desc)
                })
            st.write("### Suggested Journal Entries")
            st.table(entries)
    else:
        st.info("Upload a small trial balance or transaction extract to find accruals.")

