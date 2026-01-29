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




BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
TEMPLATE_FILE = os.path.join(DATA_DIR, "sample.xlsx")


# ------------------ WORKSPACE PAGE ------------------
def workspace_page():
    st.header("AI Workspace")

    # Back button
    if st.button("← Back to Main Page"):
        st.session_state.page = "main"
        st.rerun()

    # -------- Download Template from file --------
    st.subheader("Download Template")
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
        st.error("Template file not found in data folder.")

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

            # -------- Validation by days --------
            expected_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            df_days = list(df.columns)

            if df_days != expected_days:
                st.error(f"Invalid format! Columns must be exactly days: {expected_days}")
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
                st.info("Later this will be processed by the AI planner.")

        else:
            st.info("Upload a timetable first to interact with AI.")

    with right:
        st.subheader("Timetable")
        if st.session_state.timetable_df is not None:
            st.dataframe(st.session_state.timetable_df)

            # Download updated timetable
            excel_bytes = st.session_state.timetable_df.to_excel(index=False)
            st.download_button(
                "Download Updated Timetable",
                st.session_state.timetable_df.to_csv(index=False).encode("utf-8"),
                "optisched_timetable.csv",
                "text/csv"
            )
        else:
            st.info("Timetable will appear here after upload.")



if st.session_state.page == "main":
    main_page()

elif st.session_state.page == "workspace":
    workspace_page()
