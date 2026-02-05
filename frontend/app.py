import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="OptiSched", layout="wide")

# -------------------- Session State --------------------
if "page" not in st.session_state:
    st.session_state.page = "main"

if "timetable_df" not in st.session_state:
    st.session_state.timetable_df = None  # Original coarse timetable

if "timetable_5min" not in st.session_state:
    st.session_state.timetable_5min = None  # Internal 5-minute resolution

if "timetable_hourly" not in st.session_state:
    st.session_state.timetable_hourly = None  # Displayed hourly table

# -------------------- CSS Loader --------------------
def load_css():
    CSS_FILE = os.path.join(os.path.dirname(__file__), "css", "style.css")
    if os.path.exists(CSS_FILE):
        with open(CSS_FILE) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# -------------------- Helper Functions --------------------
def expand_to_5min(df):
    """
    Expand each row to 12 rows (5-min intervals) for 24 rows → 288 rows/day.
    If the original df is empty, we fill with empty strings.
    """
    expanded = {}
    for day in df.columns:
        col_data = df[day].fillna("").tolist()  # fill empty cells
        repeated = []
        for val in col_data:
            repeated.extend([val]*12)  # 1 hour → 12 × 5-min
        # Ensure 288 rows
        while len(repeated) < 288:
            repeated.append("")
        expanded[day] = repeated[:288]
    return pd.DataFrame(expanded)

def compress_to_hourly(df_5min):
    """
    Compress 288-row 5-min table to 24 rows for display.
    Pick the first non-empty value in each 12-row block.
    """
    hourly = {}
    for day in df_5min.columns:
        blocks = [df_5min[day][i*12:(i+1)*12].replace("", pd.NA).dropna() for i in range(24)]
        # If all empty, show empty string
        hourly[day] = [b.iloc[0] if not b.empty else "" for b in blocks]
    return pd.DataFrame(hourly)

# -------------------- Pages --------------------
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

    st.write("---")

    # -------- Download Template --------
    st.subheader("Download Template")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_FILE = os.path.join(BASE_DIR, "data", "sample.xlsx")
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
            if uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)

            expected_days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
            if list(df.columns) != expected_days:
                st.error(f"Invalid format! Columns must be exactly: {expected_days}")
            else:
                # Save original
                st.session_state.timetable_df = df

                # Expand to 5-min internal representation
                st.session_state.timetable_5min = expand_to_5min(df)

                # Compress for display
                st.session_state.timetable_hourly = compress_to_hourly(st.session_state.timetable_5min)

                st.success("Timetable loaded successfully!")

        except Exception as e:
            st.error(f"Error loading file: {e}")

    st.write("---")

    # -------- Chatbot + Timetable UI --------
    left_col, right_col = st.columns([1, 2])

    with left_col:
        st.subheader("AI Assistant")
        if st.session_state.timetable_5min is not None:
            user_message = st.text_area("Type your instruction", height=350)
            if st.button("Send"):
                st.info("Instruction will be processed by the AI planner")
        else:
            st.info("Upload a timetable first to interact with AI.")

    with right_col:
        st.subheader("Timetable")
        if st.session_state.timetable_hourly is not None:
            st.dataframe(st.session_state.timetable_hourly, height=350)

            # Download full 5-min timetable internally
            csv_data = st.session_state.timetable_5min.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Full 5-Min Timetable",
                csv_data,
                "optisched_timetable_5min.csv",
                "text/csv"
            )
        else:
            st.info("Timetable will appear here after upload.")

# -------------------- Page Router --------------------
if st.session_state.page == "main":
    main_page()
elif st.session_state.page == "workspace":
    workspace_page()
