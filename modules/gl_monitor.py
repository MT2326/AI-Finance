import streamlit as st
import pandas as pd
import io
import numpy as np

def detect_outliers_iqr(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return series[(series < lower) | (series > upper)]

def run_gl(user):
    st.subheader("🧾 GL Monitoring")
    uploaded = st.file_uploader("Upload GL Extract (XLSX/CSV)", type=["xlsx","csv"], key="gl_uploader")
    if uploaded is not None:
        if "gl_file_bytes" not in st.session_state:
            try:
                st.session_state["gl_file_bytes"] = uploaded.read()
                st.success("GL file uploaded and cached.")
            except Exception as e:
                st.error("Failed to read the GL file.")
                st.exception(e)
                return

        try:
            file_bytes = st.session_state.get("gl_file_bytes")
            if uploaded.name.endswith('.csv'):
                df = pd.read_csv(io.BytesIO(file_bytes))
            else:
                df = pd.read_excel(io.BytesIO(file_bytes), engine='openpyxl')
        except Exception as e:
            st.error("Could not parse GL file. Ensure columns include 'Amount' or similar numeric columns.")
            st.exception(e)
            return

        if df.empty:
            st.warning("Uploaded GL extract is empty.")
            return

        st.write("Preview (first 10 rows)")
        st.dataframe(df.head(10))

        # Try to find an amount-like column
        amount_cols = [c for c in df.columns if 'amount' in c.lower() or 'amt' in c.lower() or 'dr' in c.lower() or 'cr' in c.lower()]
        if not amount_cols:
            st.info("No obvious amount column found. Please ensure your GL has a numeric amount column (e.g., Amount, Cr, Dr).")
            return

        # pick first candidate and coerce to numeric
        col = amount_cols[0]
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        st.write(f"Using column: {col} for anomaly detection")

        # Outlier detection
        outlier_series = detect_outliers_iqr(df[col])
        anomalies = df[df[col].isin(outlier_series)]
        st.warning(f"Detected {len(anomalies)} anomalous entries based on IQR method.")
        if not anomalies.empty:
            st.dataframe(anomalies.head(50))
            # Cache anomalies in session for later actions
            st.session_state['gl_anomalies'] = anomalies.to_dict(orient='records')
        else:
            st.success("No statistical outliers detected in the sample.")

        # Simple KPI
        st.metric("Total Transactions (sample)", int(len(df)))
        st.metric("Anomalies Detected", int(len(anomalies)))
    else:
        st.info("Upload a GL extract (CSV/XLSX). Keep files small for demo (<10MB).")

