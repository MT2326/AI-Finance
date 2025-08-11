import streamlit as st
try:
    import google.generativeai as genai
except Exception:
    genai = None

def ask_gemini(prompt, max_output_chars=3000):
    """
    Sends prompt to Gemini (if available) and returns text.
    Falls back to a placeholder if gemini sdk isn't installed or key missing.
    """
    if genai is None:
        return "Gemini SDK not installed in this environment. Install 'google-generativeai' to enable real responses."

    try:
        api_key = st.secrets.get("gemini", {}).get("api_key", "")
        if not api_key:
            return "Gemini API key not set in .streamlit/secrets.toml."

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(prompt)
        # response.text may be large; truncate if necessary
        text = response.text
        if len(text) > max_output_chars:
            return text[:max_output_chars] + "...(truncated)"
        return text
    except Exception as e:
        return f"Gemini API error: {e}"

def analyze_with_gemini(df, prompt):
    """
    Sends prompt to Gemini (if available) and returns text.
    Falls back to a placeholder if gemini sdk isn't installed or key missing.
    """
    if genai is None:
        return "Gemini SDK not installed in this environment. Install 'google-generativeai' to enable real responses."
    try:
        api_key = st.secrets.get("gemini", {}).get("api_key", "")
        if not api_key:
            return "Gemini API key not set in .streamlit/secrets.toml."
        genai.configure(api_key=api_key)
        csv_data = df.to_csv(index=False)
        model = genai.GenerativeModel("gemini-1.5-pro")
        full_prompt = f"""
        You are a financial analyst. Here is the financial data in CSV format:

        {csv_data}

        User request: {prompt}
        Please:
        1. Provide a detailed financial analysis.
        2. Suggest what graphs should be plotted (bar, line, pie, etc.), and for which columns.
        3. Do not output Python code, only instructions and the analysis.
        """
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Gemini API error: {e}"
