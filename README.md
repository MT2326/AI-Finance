# AI Finance Controller - Streamlit Prototype (Final)

## What's included
- Robust login with session persistence (CFO / Analyst)
- MIS Reporting module (upload Excel/CSV, generate Gemini insight)
- GL Monitoring (anomaly detection with safe handling)
- Journal Suggestions & Accruals (simple heuristics)
- PDF export helper
- Gemini API stub (reads key from .streamlit/secrets.toml)

## Run locally
1. Install dependencies:
   ```
   python -m pip install -r requirements.txt
   ```
2. Set your Gemini API key in `.streamlit/secrets.toml`.
3. Run:
   ```
   streamlit run streamlit_app.py
   ```

## Notes
- The app uses `st.session_state` to persist uploaded files and user session so uploads or tab switches won't log you out.
- If you do not have Gemini credentials, the MIS module will show a helpful message and still allow file preview.
