import streamlit as st
import pandas as pd
import io
from modules.gemini_utils import ask_gemini, analyze_with_gemini
from modules.pdf_export import export_pdf_report

def run(user):
    st.subheader("📊 MIS Reporting Bot")

    # File uploader (persistent key for reruns)
    uploaded = st.file_uploader(
        "Upload Excel (.xlsx) or CSV file", 
        type=["xlsx", "csv"], 
        key="mis_uploader"
    )

    if uploaded is not None:
        try:
            # Always update the file bytes for a new upload
            file_bytes = uploaded.read()
            st.session_state["mis_file_bytes"] = file_bytes
            st.session_state["mis_file_name"] = uploaded.name
            st.success(f"File '{uploaded.name}' uploaded successfully.")
        except Exception as e:
            st.error("Failed to read uploaded file.")
            st.exception(e)
            return

        # Read from cached bytes
        try:
            if uploaded.name.endswith('.csv'):
                df = pd.read_csv(io.BytesIO(st.session_state["mis_file_bytes"]))
            else:
                df = pd.read_excel(io.BytesIO(st.session_state["mis_file_bytes"]), engine='openpyxl')
            st.session_state["mis_data"] = df
        except Exception as e:
            st.error("Failed to parse the uploaded file. Ensure it's a valid XLSX/CSV without macros or protection.")
            st.exception(e)
            return

        if df.empty:
            st.warning("The uploaded file appears to be empty.")
            return

        # Show preview
        st.write("Preview (first 10 rows):")
        st.dataframe(df.head(10))

        # Question box
        question = st.text_area(
            "Ask a question about this data (e.g., 'Summarize key trends')", 
            height=120
        )
        if st.button("Generate Insight (Gemini)"):
            sample_csv = df.head(20).to_csv(index=False)
            prompt = (
                "You are an AI finance analyst. Answer the user's question concisely.\n"
                f"Question: {question}\nData (first 20 rows):\n{sample_csv}"
            )
            with st.spinner("Contacting Gemini..."):
                resp = ask_gemini(prompt)
                st.markdown("### 💡 Insight from Gemini")
                st.write(resp)
                
        user_cmd = st.text_area("Ask Gemini for analysis & graphs")
         
        if st.button("Analyze"):
            with st.spinner("Analyzing with Gemini..."):
                analysis = analyze_with_gemini(st.session_state["mis_data"], user_cmd)
                st.markdown("### 📄 Gemini's Analysis")
                st.write(analysis)

                # Example: Generate one sample chart (Revenue trend if exists)
                df = st.session_state["mis_data"]
                numeric_cols = df.select_dtypes(include="number").columns
                if len(numeric_cols) >= 2:
                    plt.figure(figsize=(8, 4))
                    df.plot(x=numeric_cols[0], y=numeric_cols[1], kind="line")
                    plt.title(f"{numeric_cols[1]} over {numeric_cols[0]}")
                    st.pyplot(plt)

        # Export to PDF
        if st.button("Export Simple PDF Summary from Preview"):
            summary_text = f"MIS Summary for {st.session_state['mis_file_name']}\n\nTop rows:\n" + df.head(10).to_string(index=False)
            pdf_path = export_pdf_report(summary_text)
            with open(pdf_path, 'rb') as f:
                st.download_button("Download MIS PDF", f, file_name="MIS_Report.pdf")

    else:
        st.info("Upload a small XLSX or CSV (suggested < 5MB) to preview and analyze.")
