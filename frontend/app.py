import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="OptiSched", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "main"

if "timetable_df" not in st.session_state:
    st.session_state.timetable_df = None

def load_css():
    CSS_FILE = os.path.join(os.path.dirname(__file__), "css", "style.css")
    if os.path.exists(CSS_FILE):
        with open(CSS_FILE) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


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
    st.header("AI Workspace")

    # Back button
    if st.button("← Back to Main Page"):
        st.session_state.page = "main"
        st.rerun()

    # -------- Download Template from file --------
    st.subheader("Download Template")
    # Path relative to this file
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # frontend/
    TEMPLATE_FILE = os.path.join(BASE_DIR, "data", "sample.xlsx")  # frontend/data/sample.xlsx

    if os.path.exists(TEMPLATE_FILE):
        with open(TEMPLATE_FILE, "rb") as f:
            excel_bytes = f.read()
        st.download_button(
            "Download Timetable Template",
            excel_bytes,
            "optisched_template.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error(f"Template file not found! Expected at {TEMPLATE_FILE}")

    st.write("---")

    # -------- Upload Timetable --------
    st.subheader("Upload Your Timetable")
    uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])
    
    if uploaded_file:
        try:
            # Read uploaded file
            if uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)

            # -------- Validation: columns must be Monday → Sunday --------
            expected_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            if list(df.columns) != expected_days:
                st.error(f"Invalid format! Columns must be exactly: {expected_days}")
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
                # Placeholder: AI processing will go here
                st.info("Later this will be processed by the AI planner.")
        else:
            st.info("Upload a timetable first to interact with AI.")

    with right:
        st.subheader("Timetable")
        if st.session_state.timetable_df is not None:
            st.dataframe(st.session_state.timetable_df)

            # Download updated timetable as CSV
            csv_data = st.session_state.timetable_df.to_csv(index=False).encode("utf-8")
            st.download_button("Download Updated Timetable", csv_data, "optisched_timetable.csv", "text/csv")
        else:
            st.info("Timetable will appear here after upload.")




if st.session_state.page == "main":
    main_page()
elif st.session_state.page == "workspace":
    workspace_page()
