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
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("OptiSched")
        st.subheader("AI-Powered Adaptive Study Planner")
        st.write("")
        if st.button("Let's Get Started"):
            st.session_state.page = "login"

    st.write("\n\n\n")
    st.header("Why OptiSched?")
    st.info("""
    This is a placeholder for your project motivation.

    Here you will later describe:
    - The problem students face
    - Why planning is difficult and exhausting
    - How OptiSched helps and why it is useful for students and society
    """)

    st.header("Features")
    st.markdown("""
    - Feature 1: (write description later)  
    - Feature 2: (write description later)  
    - Feature 3: (write description later)  
    - Feature 4: (write description later)  
    """)

# Login / Registration Page
elif st.session_state.page == "login":
    import frontend.pages.account as account  # Capital F
    account.show()

# Timetable Page
elif st.session_state.page == "timetable":
    import frontend.pages.timetable_creation as timetable
    timetable.show()

# AI Study Plan Page
elif st.session_state.page == "ai_plan":
    import frontend.pages.generate_plan as ai_plan
    ai_plan.show()

# Visualization Page
elif st.session_state.page == "visualization":
    import frontend.pages.visualization as visualization
    visualization.show()
