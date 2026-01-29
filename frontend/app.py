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







# ------------------ WORKSPACE PAGE ------------------
def workspace_page():
    st.header("AI Workspace")

    # Back button
    if st.button("← Back to Main Page"):
        st.session_state.page = "main"
        st.rerun()

    # -------- Download Template --------
    st.subheader("Download Template")
    template = pd.DataFrame({
        "Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "Start": ["08:00"]*5,
        "End": ["08:45"]*5,
        "Subject": [""]*5,
        "Type": ["Lesson"]*5,
        "Priority": ["Medium"]*5
    })
    csv_template = template.to_csv(index=False).encode("utf-8")
    st.download_button("Download Timetable Template", csv_template, "optisched_template.csv", "text/csv")

    st.write("---")

    # -------- Upload Timetable --------
    st.subheader("Upload Your Timetable")
    uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)

            # Validate columns
            expected_cols = ["Day", "Start", "End", "Subject", "Type", "Priority"]
            if list(df.columns) != expected_cols:
                st.error(f"Invalid format! Columns must be: {expected_cols}")
            else:
                st.session_state.timetable_df = df
                st.success("Timetable loaded successfully!")
        except Exception as e:
            st.error(f"Error loading file: {e}")

    st.write("---")

    # -------- Chatbot + Timetable UI --------
    left, right = st.columns([1, 2])

    with left:
        st.subheader("AI Assistant")
        if st.session_state.timetable_df is not None:
            user_message = st.text_area("Type your instruction (e.g. Add Math test on Friday at 10:00)")
            if st.button("Send"):
                # Placeholder for NLP → Planner
                st.info("Later this will be processed by the AI planner.")

        else:
            st.info("Upload a timetable first to interact with AI.")

    with right:
        st.subheader("Timetable")
        if st.session_state.timetable_df is not None:
            st.dataframe(st.session_state.timetable_df)

            # Download updated timetable
            csv_data = st.session_state.timetable_df.to_csv(index=False).encode("utf-8")
            st.download_button("Download Updated Timetable", csv_data, "optisched_timetable.csv", "text/csv")
        else:
            st.info("Timetable will appear here after upload.")





if st.session_state.page == "main":
    main_page()

elif st.session_state.page == "workspace":
    workspace_page()
