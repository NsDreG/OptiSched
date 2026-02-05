import streamlit as st
import pandas as pd
import os
from datetime import time

from ai.nlp import Activity, resolve_schedule

st.set_page_config(page_title="OptiSched", layout="wide")

# -------------------- Session State --------------------
if "page" not in st.session_state:
    st.session_state.page = "main"

for key in ["timetable_5min", "timetable_hourly"]:
    if key not in st.session_state:
        st.session_state[key] = None

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
        current = None
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
            df[d][i*12:(i+1)*12].replace("", pd.NA).dropna().iloc[0]
            if not df[d][i*12:(i+1)*12].replace("", pd.NA).dropna().empty else ""
            for i in range(24)
        ]
        for d in df.columns
    })

# -------------------- AI Instruction Interpreter --------------------
def interpret_instruction(msg: str):
    msg = msg.lower()

    if "study" in msg:
        return Activity(
            id="Study",
            priority=4,
            start_time=time(16, 0),
            end_time=time(17, 0),
            instructions=msg
        )

    if "gym" in msg:
        return Activity(
            id="Gym",
            priority=2,
            start_time=time(18, 0),
            end_time=time(19, 0),
            instructions=msg
        )

    return None

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

        expected = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        if list(df.columns) != expected:
            st.error("Invalid timetable format")
            return

        st.session_state.timetable_5min = expand_to_5min(df)
        st.session_state.timetable_hourly = compress_to_hourly(
            st.session_state.timetable_5min
        )
        st.success("Timetable loaded")

    st.write("---")

    left, right = st.columns([1, 2])

    with left:
        msg = st.text_area("Tell the AI what to change")

        if st.button("Send"):
            if st.session_state.timetable_5min is None:
                st.warning("Upload a timetable first")
                return

            activity = interpret_instruction(msg)
            if activity is None:
                st.warning("I didn't understand the instruction.")
                return

            schedule = df_to_schedule(st.session_state.timetable_5min)
            result = resolve_schedule(schedule, activity)

            st.session_state.timetable_5min = schedule_to_df(result.schedule)
            st.session_state.timetable_hourly = compress_to_hourly(
                st.session_state.timetable_5min
            )

            st.success("Schedule optimized!")
            st.rerun()

    with right:
        if st.session_state.timetable_hourly is not None:
            st.dataframe(st.session_state.timetable_hourly, height=400)

# -------------------- Router --------------------
if st.session_state.page == "main":
    main_page()
else:
    workspace_page()
