import streamlit as st
from modules.login import login_user
from modules.mis_report_bot import run as run_mis
from modules.gl_monitor import run_gl
from modules.journal_bot import run as run_journal
from modules.pdf_export import export_pdf_report

st.set_page_config(page_title="AI Finance Controller", layout="wide")

# --- LOGIN / SESSION HANDLING ---
# login_user() manages st.session_state['user'] and ['role'] and returns a dict when logged in
user_info = login_user()
if not user_info:
    # login form shown by login_user(), halt further rendering until logged in
    st.stop()

# Ensure session has a consistent dict object
if "user_dict" not in st.session_state or st.session_state.get("user_dict") is None:
    st.session_state["user_dict"] = {"username": st.session_state.get("user"), "role": st.session_state.get("role")}

# Sidebar navigation
st.sidebar.title("📌 Navigation")
role = st.session_state["user_dict"].get("role", "Analyst")
if role == "CFO":
    menu_options = ["MIS Reporting", "GL Monitoring", "Journal Suggestions"]
else:
    menu_options = ["MIS Reporting", "GL Monitoring"]

menu = st.sidebar.radio("Go to", menu_options)

st.sidebar.markdown("---")
st.sidebar.caption(f"🔐 Logged in as: `{st.session_state['user_dict']['username']}` — Role: `{st.session_state['user_dict']['role']}`")

# Main module loader with safe try/except to avoid blank pages on errors
try:
    if menu == "MIS Reporting":
        run_mis(st.session_state["user_dict"])
    elif menu == "GL Monitoring":
        run_gl(st.session_state["user_dict"])
    elif menu == "Journal Suggestions":
        run_journal(st.session_state["user_dict"])

    # Footer: quick PDF export sample using current snapshot (demo)
    st.markdown("---")
    if st.button("Download Sample Summary PDF"):
        sample_text = "Auto-generated summary: Run MIS Reporting to generate specific summaries."
        path = export_pdf_report(sample_text)
        with open(path, "rb") as f:
            st.download_button("Download PDF", f, file_name="Finance_Summary.pdf")

except Exception as e:
    st.error("❌ Something went wrong in the selected module. See details below.")
    st.exception(e)
