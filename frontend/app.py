import streamlit as st
import pandas as pd
import os
from datetime import time
import re

from ai.nlp import Activity, resolve_schedule

st.set_page_config(page_title="OptiSched", layout="wide")

# -------------------- Session State --------------------
if "page" not in st.session_state:
    st.session_state.page = "main"

for key in ["timetable_5min", "timetable_hourly"]:
    if key not in st.session_state:
        st.session_state[key] = None

# -------------------- CSS Loader --------------------
def load_css():
    css = os.path.join(os.path.dirname(__file__), "css", "style.css")
    if os.path.exists(css):
        with open(css) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# -------------------- Time Helpers --------------------
def row_to_time(r):
    minutes = r * 5
    return time(minutes // 60, minutes % 60)

def time_to_row(t):
    return (t.hour * 60 + t.minute) // 5

# -------------------- Timetable ↔ AI --------------------
def df_to_schedule(df):
    schedule = {}
    for day in df.columns:
        acts = []
        current = ""
        start = None
        for i, v in enumerate(df[day].fillna("")):
            if v != current:
                if current:
                    acts.append(Activity(
                        id=current,
                        priority=3,
                        start_time=row_to_time(start),
                        end_time=row_to_time(i),
                        instructions="flexible"
                    ))
                current = v
                start = i if v else None
        if current:
            acts.append(Activity(
                id=current,
                priority=3,
                start_time=row_to_time(start),
                end_time=time(23, 59),
                instructions="flexible"
            ))
        schedule[day] = acts
    return schedule

def schedule_to_df(schedule):
    df = pd.DataFrame("", index=range(288), columns=schedule.keys())
    for day, acts in schedule.items():
        for a in acts:
            s = time_to_row(a.start_time)
            e = time_to_row(a.end_time)
            df.loc[s:e-1, day] = a.id
    return df

# -------------------- 5-min / Hour --------------------
def expand_to_5min(df):
    return pd.DataFrame({
        d: [v for val in df[d].fillna("") for v in [val]*12][:288]
        for d in df.columns
    })

def compress_to_hourly(df):
    return pd.DataFrame({
        d: [
            df[d][i*12:(i+1)*12]
            .replace("", pd.NA)
            .dropna()
            .iloc[0] if not df[d][i*12:(i+1)*12].replace("", pd.NA).dropna().empty else ""
            for i in range(24)
        ]
        for d in df.columns
    })

# -------------------- Instruction Parser --------------------
DAYS = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]

def parse_instruction(msg: str):
    """
    Converts natural-language instructions into Activity objects.
    Example: 'Add physics on Monday 1pm to 3pm'
    """
    msg_lower = msg.lower()

    # Extract day
    day_found = None
    for day in DAYS:
        if day in msg_lower:
            day_found = day.capitalize()
            break
    if not day_found:
        day_found = "Monday"

    # Extract times
    times = re.findall(r'(\d{1,2})(am|pm)?', msg_lower)
    start, end = time(9,0), time(10,0)
    if len(times) >= 2:
        def to_time(h, ampm):
            h = int(h)
            if ampm == "pm" and h != 12:
                h += 12
            if ampm == "am" and h == 12:
                h = 0
            return h
        start_hour = to_time(times[0][0], times[0][1])
        end_hour   = to_time(times[1][0], times[1][1])
        start = time(start_hour, 0)
        end = time(end_hour, 0)

    # Extract activity name
    act_match = re.search(r'add\s+([a-z\s]+?)\s+on', msg_lower)
    if act_match:
        act_name = act_match.group(1).strip().capitalize()
    else:
        act_name = "Task"

    return Activity(
        id=act_name,
        priority=3,
        start_time=start,
        end_time=end,
        instructions=msg
    ), day_found

# -------------------- Pages --------------------
def main_page():
    st.title("OptiSched")
    st.subheader("AI-Powered Adaptive Study Planner")

    st.write(
        """
        OptiSched helps students **organize their weekly schedules intelligently**.
        Upload your timetable, describe what you want to change in natural language,
        and let AI rearrange your schedule while avoiding conflicts.
        """
    )

    st.markdown("### Why OptiSched?")
    st.info(
        """
        Students often struggle with rigid timetables. OptiSched introduces
        AI-driven scheduling to create flexible, optimized study plans.
        """
    )

    st.markdown("### Key Features")
    st.markdown("""
    - Natural language timetable editing  
    - Conflict-aware AI scheduling  
    - 5-minute precision internal planning  
    - Easy import/export with Excel & CSV  
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

    # -------- Download Template --------
    st.subheader("Download Template")
    base = os.path.dirname(os.path.abspath(__file__))
    template = os.path.join(base, "data", "sample.xlsx")

    if os.path.exists(template):
        with open(template, "rb") as f:
            st.download_button(
                "Download Timetable Template",
                f.read(),
                "optisched_template.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.warning("Template file not found.")

    st.write("---")

    # -------- Upload Timetable --------
    st.subheader("Upload Timetable")
    uploaded = st.file_uploader("Upload Excel or CSV", type=["xlsx","csv"])

    if uploaded:
        df = pd.read_excel(uploaded) if uploaded.name.endswith(".xlsx") else pd.read_csv(uploaded)
        days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

        if list(df.columns) != days:
            st.error("Columns must be Monday → Sunday")
            return

        st.session_state.timetable_5min = expand_to_5min(df)
        st.session_state.timetable_hourly = compress_to_hourly(
            st.session_state.timetable_5min
        )
        st.success("Timetable loaded successfully")

    st.write("---")

    left, right = st.columns([1, 2])

    with left:
        st.subheader("AI Assistant")
        msg = st.text_area("Describe what you want to change")

        if st.button("Send"):
            if st.session_state.timetable_5min is None:
                st.warning("Upload a timetable first")
            else:
                activity, day_found = parse_instruction(msg)
                schedule = df_to_schedule(st.session_state.timetable_5min)

                # Insert activity into correct day first
                schedule.setdefault(day_found, []).append(activity)

                # Resolve conflicts
                result = resolve_schedule(schedule, activity)

                # Update in-memory timetable
                st.session_state.timetable_5min = schedule_to_df(result.schedule)
                st.session_state.timetable_hourly = compress_to_hourly(
                    st.session_state.timetable_5min
                )

                st.success("Schedule optimized!")
                st.rerun()

    with right:
        st.subheader("Timetable")
        if st.session_state.timetable_hourly is not None:
            st.dataframe(st.session_state.timetable_hourly, height=400)

            csv = st.session_state.timetable_5min.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Updated Timetable (5-min)",
                csv,
                "optisched_updated_timetable.csv",
                "text/csv"
            )

# -------------------- Router --------------------
if st.session_state.page == "main":
    main_page()
else:
    workspace_page()
