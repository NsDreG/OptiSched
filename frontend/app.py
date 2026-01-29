import streamlit as st
import pandas as pd


st.set_page_config(page_title="OptiSched", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "main"

if "timetable_df" not in st.session_state:
    st.session_state.timetable_df = None






def main_page():
    st.title("OptiSched")
    st.subheader("AI Powered Adaptive Study Planner")

    st.write("Organize your school life intelligently with AI.")
    st.write("Upload your timetable, talk to the assistant, and let the system optimize your schedule.")

    if st.button("Start Planning"):
        st.session_state.page = "workspace"
        st.rerun()

    st.markdown("### Why OptiSched?")
    st.info("This is where you will later write about the problem, relevance, and social usefulness.")

    st.markdown("### Key Features")
    st.markdown("""
    - Natural language timetable editing  
    - AI-based schedule optimization  
    - Real-time visual updates  
    - Export and import of schedules  
    """)










def workspace_page():
    if st.button("← Back to Main Page"):
        st.session_state.page = "main"
        st.rerun()

    st.header("AI Workspace")

    # Upload timetable
    uploaded_file = st.file_uploader("Upload your timetable (Excel format)", type=["xlsx", "csv"])

    if uploaded_file:
        if uploaded_file.name.endswith(".xlsx"):
            st.session_state.timetable_df = pd.read_excel(uploaded_file)
        else:
            st.session_state.timetable_df = pd.read_csv(uploaded_file)

    left, right = st.columns([1, 2])

    with left:
        st.subheader("AI Assistant")
        user_message = st.text_area("Type your instruction (e.g. Add Math test on Friday at 10:00)")
        if st.button("Send"):
            st.info("Later this will be sent to the NLP module and planner engine.")

    with right:
        st.subheader("Timetable")

        if st.session_state.timetable_df is not None:
            st.dataframe(st.session_state.timetable_df)

            csv = st.session_state.timetable_df.to_csv(index=False).encode("utf-8")
            st.download_button("Download Updated Timetable", csv, "optisched_timetable.csv", "text/csv")
        else:
            st.info("Upload a timetable to begin.")






if st.session_state.page == "main":
    main_page()

elif st.session_state.page == "workspace":
    workspace_page()
