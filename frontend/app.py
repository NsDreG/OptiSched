import streamlit as st
import pandas as pd
import os
from datetime import time

from ai.nlp import Activity, resolve_schedule

st.set_page_config(page_title="OptiSched", layout="wide")

# -------------------- Session State --------------------
if "page" not in st.session_state:
    st.session_state.page = "main"

for key in ["timetable_df", "timetable_5min", "timetable_hourly"]:
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
    m = r * 5
    return time(m // 60, m % 60)

def time_to_row(t):
    return (t.hour * 60 + t.minute) // 5

# -------------------- Timetable ↔ AI --------------------
def df_to_schedule(df):
    schedule = {}
    for day in df.columns:
        acts = []
        current, start = "", None

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
                current, start = v, i if v else None

        if current:
            acts.append(Activity(
                id=current,
                priority=3,
                start_time=row_to_time(start),
                end_time=time(23, 55),
                instructions="flexible"
            ))

        schedule[day] = acts
    return schedule

def schedule_to_df(schedule):
    df = pd.DataFrame("", index=range(288), columns=schedule.keys())
    for day, acts in schedule.items():
        for a in acts:
            s, e = time_to_row(a.start_time), time_to_row(a.end_time)
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
            df[d][i*12:(i+1)*12].replace("", pd.NA).dropna().iloc[0]
            if not df[d][i*12:(i+1)*12].replace("", pd.NA).dropna().empty else ""
            for i in range(24)
        ]
        for d in df.columns
    })

# -------------------- Pages --------------------
def main_page():
    st.title("OptiSched")
    st.subheader("AI Powered Adaptive Study Planner")

    if st.button("Start Planning"):
        st.session_state.page = "workspace"
        st.rerun()

def workspace_page():
    st.header("AI Workspace")

    if st.button("← Back"):
        st.session_state.page = "main"
        st.rerun()

    st.write("---")

    uploaded = st.file_uploader("Upload timetable", type=["xlsx", "csv"])
    if uploaded:
        df = pd.read_excel(uploaded) if uploaded.name.endswith(".xlsx") else pd.read_csv(uploaded)
        days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

        if list(df.columns) != days:
            st.error("Invalid timetable format")
            return

        st.session_state.timetable_5min = expand_to_5min(df)
        st.session_state.timetable_hourly = compress_to_hourly(st.session_state.timetable_5min)
        st.success("Timetable loaded")

    st.write("---")

    left, right = st.columns([1, 2])

    with left:
        msg = st.text_area("Tell the AI what to change")

        if st.button("Send") and st.session_state.timetable_5min is not None:
            schedule = df_to_schedule(st.session_state.timetable_5min)

            new_activity = Activity(
                id="AI_TASK",
                priority=4,
                start_time=time(9, 0),
                end_time=time(10, 0),
                instructions=msg
            )

            result = resolve_schedule(schedule, new_activity)

            st.session_state.timetable_5min = schedule_to_df(result.schedule)
            st.session_state.timetable_hourly = compress_to_hourly(
                st.session_state.timetable_5min
            )

            st.success("Schedule optimized")

    with right:
        if st.session_state.timetable_hourly is not None:
            st.dataframe(st.session_state.timetable_hourly, height=400)

# -------------------- Router --------------------
if st.session_state.page == "main":
    main_page()
else:
    workspace_page()
