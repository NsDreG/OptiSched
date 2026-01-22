import streamlit as st

st.set_page_config(page_title="OptiSched", layout="wide")

# Page state
if "page" not in st.session_state:
    st.session_state.page = "main"

# Optional: Logged-in user
if "user" not in st.session_state:
    st.session_state.user = None

# -------- Menu Bar --------
def menu_bar():
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("Home"):
            st.session_state.page = "main"
    with col2:
        if st.button("Login / Register"):
            st.session_state.page = "login"
    with col3:
        if st.button("Timetable"):
            st.session_state.page = "timetable"
    with col4:
        if st.button("AI Study Plan"):
            st.session_state.page = "ai_plan"
    with col5:
        if st.button("Visualization"):
            st.session_state.page = "visualization"

menu_bar()  # Display menu on every page

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

# -------- Timetable Page --------
elif st.session_state.page == "timetable":
    st.title("Timetable Creation")
    if st.session_state.user:
        st.write(f"Welcome, {st.session_state.user}! Here you can create your timetable.")
        # Placeholder for timetable form / chatbot
        st.info("Timetable creation form and chatbot will be implemented here.")
    else:
        st.warning("Please log in first to access the timetable.")

# -------- AI Study Plan Page --------
elif st.session_state.page == "ai_plan":
    st.title("AI Study Plan")
    if st.session_state.user:
        st.info("AI-generated study plan will be displayed here.")
    else:
        st.warning("Please log in first to view your AI study plan.")

# -------- Visualization Page --------
elif st.session_state.page == "visualization":
    st.title("Visualization")
    if st.session_state.user:
        st.info("Timetable visualizations and charts will be displayed here.")
    else:
        st.warning("Please log in first to view visualizations.")
