import streamlit as st

# Simple credentials - replace with real auth for production
CREDENTIALS = {
    "admin": {"password": "1234", "role": "CFO"},
    "analyst": {"password": "analyst123", "role": "Analyst"}
}

def login_user():
    """
    Manages login UI and session state.
    Returns a dict {'username','role'} when logged in, otherwise None.
    Sets st.session_state['user'] and ['role'].
    """
    if "user" not in st.session_state:
        st.session_state["user"] = None
        st.session_state["role"] = None

    # If already logged in, show logout on sidebar and return info
    if st.session_state["user"]:
        with st.sidebar:
            if st.button("Logout"):
                st.session_state["user"] = None
                st.session_state["role"] = None
                st.session_state["user_dict"] = None
                st.experimental_rerun()
        return {"username": st.session_state["user"], "role": st.session_state["role"]}

    # Show login form
    st.header("🔐 Login to AI Finance Controller")
    col1, col2 = st.columns([2,3])
    with col1:
        username = st.text_input("Username", key="login_username")
    with col2:
        password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if username in CREDENTIALS and CREDENTIALS[username]["password"] == password:
            st.session_state["user"] = username
            st.session_state["role"] = CREDENTIALS[username]["role"]
            st.session_state["user_dict"] = {"username": username, "role": st.session_state["role"]}
            # Rerun so the main app can proceed
            st.rerun()
        else:
            st.error("Invalid credentials. Try 'admin' / '1234' or 'analyst' / 'analyst123'.")

    return None
