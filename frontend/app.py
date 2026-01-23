import streamlit as st

st.set_page_config(page_title="OptiSched", layout="wide")

# Session state initialization
if "page" not in st.session_state:
    st.session_state.page = "main"

if "user" not in st.session_state:
    st.session_state.user = None

# -------- Navigation Bar --------
def navbar():
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Home"):
            st.session_state.page = "main"
    with col2:
        if st.button("Account"):
            st.session_state.page = "login"
    with col3:
        if st.button("Workspace"):
            st.session_state.page = "workspace"

st.markdown("---")
navbar()
st.markdown("---")

# -------- Main Page --------
if st.session_state.page == "main":
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("OptiSched")
        st.subheader("AI-Powered Adaptive Study Planner")
        st.write("")
        if st.button("Let's Get Started"):
            st.session_state.page = "login"

    st.write("\n\n\n")

    st.header("Why OptiSched?")
    st.info("Placeholder for your problem statement and social importance.")

    st.header("Key Features")
    st.markdown("""
    - Natural language timetable editing  
    - AI-assisted schedule optimization  
    - Real-time visual timetable updates  
    """)

# -------- Account Page --------
elif st.session_state.page == "login":
    import pages.account as account
    account.show()

# -------- Workspace Page --------
elif st.session_state.page == "workspace":
    if st.session_state.user:
        import pages.workspace as workspace
        workspace.show()
    else:
        st.warning("Please log in first to access the workspace.")
        if st.button("Go to Login"):
            st.session_state.page = "login"
