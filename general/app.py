# general/app.py
import streamlit as st
import pandas as pd
import os
from datetime import time

from services.scheduler_service import optimize_timetable

st.set_page_config(page_title="OptiSched", layout="wide")

# -------------------- Session State --------------------
if "page" not in st.session_state:
    st.session_state.page = "main"

for key in ["timetable_df", "timetable_5min", "timetable_hourly"]:
    if key not in st.session_state:
        st.session_state[key] = None

# -------------------- CSS Loader --------------------
def load_css():
    css_file = os.path.join(os.path.dirname(__file__), "css", "style.css")
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# -------------------- Time Helpers --------------------
def row_to_time(r):
    m = r * 5
    return time(m // 60, m % 60)

def time_to_row(t):
    return (t.hour * 60 + t.minute) // 5

# -------------------- Timetable Display Helpers --------------------
def expand_to_5min(df):
    """Convert coarse timetable to 5-min internal resolution (288 rows/day)."""
    return pd.DataFrame({
        d: [v for val in df[d].fillna("") for v in [val]*12][:288]
        for d in df.columns
    })

def compress_to_hourly(df_5min):
    """Convert 288-row timetable to hourly view for display."""
    return pd.DataFrame({
        d: [
            df_5min[d][i*12:(i+1)*12].replace("", pd.NA).dropna().iloc[0]
            if not df_5min[d][i*12:(i+1)*12].replace("", pd.NA).dropna().empty else ""
            for i in range(24)
        ]
        for d in df_5min.columns
    })

# -------------------- Pages --------------------
def main_page():
    st.title("OptiSched")
    st.subheader("AI Powered Adaptive Study Planner")
    st.write("Organize your school life intelligently with AI.")
    st.write("Upload your timetable, instruct the AI, and optimize your schedule in real-time.")

    st.markdown("### Why OptiSched?")
    st.info("AI-based scheduling ensures minimal conflicts while prioritizing important tasks.")

    st.markdown("### Key Features")
    st.markdown("""
    - Natural language timetable editing  
    - AI-based schedule optimization  
    - Real-time visual updates  
    - Export and import schedules  
    """)

    if st.button("Start Planning"):
        st.session_state.page = "workspace"
        st.rerun()


def workspace_page():
    st.header("AI Workspace")

    if st.button("← Back to Main Page"):
        st.session_state.page = "main"
        st.rerun()

    st.write("---")

    # -------------------- Download Template --------------------
    st.subheader("Download Timetable Template")
    base_dir = os.path.dirname(os.path.dirname(__file__))
    template_file = os.path.join(base_dir, "data", "sample.xlsx")
    if os.path.exists(template_file):
        with open(template_file, "rb") as f:
            excel_bytes = f.read()
        st.download_button(
            "Download Template",
            excel_bytes,
            "optisched_template.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error(f"Template file not found! Expected at {template_file}")

    st.write("---")

    # -------------------- Upload Timetable --------------------
    uploaded = st.file_uploader("Upload timetable (Excel or CSV)", type=["xlsx", "csv"])
    if uploaded:
        df = pd.read_excel(uploaded) if uploaded.name.endswith(".xlsx") else pd.read_csv(uploaded)
        days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        if list(df.columns) != days:
            st.error("Invalid timetable format! Columns must be Monday → Sunday")
            return

        st.session_state.timetable_5min = expand_to_5min(df)
        st.session_state.timetable_hourly = compress_to_hourly(st.session_state.timetable_5min)
        st.session_state.timetable_df = df
        st.success("Timetable loaded successfully!")

    st.write("---")

    # -------------------- AI Assistant + Timetable --------------------
    left_col, right_col = st.columns([1, 2])

    with left_col:
        st.subheader("AI Assistant")
        user_input = st.text_area("Give instructions to the AI (e.g., 'Add Physics on Monday 1pm-3pm')")
        if st.button("Send") and st.session_state.timetable_5min is not None:
            # Call the scheduler service
            updated_5min = optimize_timetable(st.session_state.timetable_5min, user_input)
            st.session_state.timetable_5min = updated_5min
            st.session_state.timetable_hourly = compress_to_hourly(updated_5min)
            st.success("Schedule updated successfully!")

    with right_col:
        st.subheader("Timetable (Hourly View)")
        if st.session_state.timetable_hourly is not None:
            st.dataframe(st.session_state.timetable_hourly, height=400)
            csv_data = st.session_state.timetable_5min.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Full 5-Min Timetable",
                csv_data,
                "optisched_timetable_5min.csv",
                "text/csv"
            )
        else:
            st.info("Timetable will appear here after upload.")

# -------------------- Router --------------------
if st.session_state.page == "main":
    main_page()
else:
    workspace_page()
