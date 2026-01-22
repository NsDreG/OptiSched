import streamlit as st

st.set_page_config(page_title="OptiSched", layout="wide")

# Page state
if "page" not in st.session_state:
    st.session_state.page = "main"

# -------- Main Page --------
if st.session_state.page == "main":

    # Centered title and button
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("OptiSched")
        st.subheader("AI-Powered Adaptive Study Planner")
        st.write("")
        if st.button("Let's Get Started"):
            st.session_state.page = "login"

    st.write("\n\n\n")

    # Scroll section: Why OptiSched
    st.header("Why OptiSched?")
    st.info("""
    This is a placeholder for your project motivation.

    Here you will later describe:
    - The problem students face
    - Why planning is difficult and exhausting
    - How OptiSched helps and why it is useful for students and society
    """)

    # Scroll section: Features
    st.header("Features")
    st.markdown("""
    - Feature 1: (write description later)  
    - Feature 2: (write description later)  
    - Feature 3: (write description later)  
    - Feature 4: (write description later)  
    """)

# -------- Login / Registration Page --------
elif st.session_state.page == "login":
    import frontend.pages.account as account
    account.show()
