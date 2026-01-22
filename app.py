import streamlit as st

st.set_page_config(page_title="AI Study Planner", layout="wide")
st.title("AI-Powered Adaptive Study Planner")
st.subheader("InfoMatrix Asia 2026 – AI Programming Section")
st.write("""
Welcome! Use the buttons below to navigate between features of your study planner.
""")
st.header("Navigation")

col1, col2 = st.columns(2)

with col1:
    if st.button("Create / Upload Timetable"):
        st.session_state['page'] = 'timetable'

with col2:
    if st.button("Account / Login"):
        st.session_state['page'] = 'account'

if st.button("AI Study Plan Generator"):
    st.session_state['page'] = 'generator'

if st.button("Visualization & Export"):
    st.session_state['page'] = 'visualization'

st.markdown("---")

if 'page' not in st.session_state:
    st.session_state['page'] = 'main'

if st.session_state['page'] == 'main':
    st.info("Select a feature above to start using the planner.")

elif st.session_state['page'] == 'timetable':
    # import timetable page
    import frontend.pages.timetable_creation as timetable
    timetable.show()

elif st.session_state['page'] == 'account':
    # import account/login page
    import frontend.pages.account as account
    account.show()

elif st.session_state['page'] == 'generator':
    # import AI generator page
    import frontend.pages.generate_plan as generator
    generator.show()

elif st.session_state['page'] == 'visualization':
    # import visualization page
    import frontend.pages.visualization as viz
    viz.show()
