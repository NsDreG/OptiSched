import streamlit as st
import pandas as pd
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="OptiSched", layout="wide")

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
SLOTS_PER_DAY = 288  # 24h * 12 (5-minute slots)

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "main"

if "timetable_df" not in st.session_state:
    st.session_state.timetable_df = None


# ---------------- HELPERS ----------------
def slot_to_time(slot):
    minutes = slot * 5
    h = minutes // 60
    m = minutes % 60
    return f"{h:02d}:{m:02d}"


def build_display_table(df):
    """Convert 5-min slots into human-readable blocks"""
    rows = []

    for day in DAYS:
        col = df[day].fillna("")
        start = None
        current = ""

        for i, value in enumerate(col.tolist() + [""]):
            if value != current:
                if current != "":
                    rows.append({
                        "Day": day,
                        "Start": slot_to_time(start),
                        "End": slot_to_time(i),
                        "Activity": current
                    })
                current = value
                start = i if value != "" else None

    return pd.DataFrame(rows)


# ---------------- MAIN PAGE ----------------
def main_page():
    st.title("OptiSched")
    st.subheader("AI-Powered Adaptive Study Planner")

    st.write("Upload your timetable and manage it using natural language.")

    if st.button("Start Planning"):
        st.session_state.page = "workspace"
        st.rerun()


# ---------------- WORKSPACE ----------------
def workspace_page():
    st.header("AI Workspace")

    if st.button("← Back"):
        st.session_state.page = "main"
        st.rerun()

    st.divider()

    # -------- TEMPLATE DOWNLOAD --------
    st.subheader("Download Template")

    template = pd.DataFrame(
        {day: [""] * SLOTS_PER_DAY for day in DAYS}
    )

    excel_bytes = template.to_excel(index=False, engine="xlsxwriter")
    st.download_button(
        "Download Excel Template",
        data=template.to_csv(index=False).encode("utf-8"),
        file_name="optisched_template.csv",
        mime="text/csv"
    )

    st.divider()

    # -------- UPLOAD --------
    st.subheader("Upload Timetable")
    file = st.file_uploader("Upload CSV file", type=["csv"])

    if file:
        try:
            df = pd.read_csv(file)

            if list(df.columns) != DAYS:
                st.error("Invalid format: columns must be Monday → Sunday")
            elif len(df) != SLOTS_PER_DAY:
                st.error("Invalid format: timetable must contain 288 rows")
            else:
                st.session_state.timetable_df = df
                st.success("Timetable loaded successfully!")

        except Exception as e:
            st.error(str(e))

    st.divider()

    # -------- UI LAYOUT --------
    left, right = st.columns([1, 2])

    # Chatbot
    with left:
        st.subheader("Assistant")

        if st.session_state.timetable_df is None:
            st.info("Upload a timetable first.")
        else:
            user_input = st.text_area(
                "Tell me what to add (e.g. School Mon–Fri 08:00–17:00)",
                height=150
            )
            if st.button("Send"):
                st.info("NLP + AI logic will be added here.")

    # Timetable
    with right:
        st.subheader("Timetable")

        if st.session_state.timetable_df is not None:
            display_df = build_display_table(st.session_state.timetable_df)

            if display_df.empty:
                st.info("No activities yet.")
            else:
                st.dataframe(display_df, use_container_width=True)

            csv = st.session_state.timetable_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Updated Timetable",
                csv,
                "optisched_timetable.csv",
                "text/csv"
            )


# ---------------- ROUTER ----------------
if st.session_state.page == "main":
    main_page()
elif st.session_state.page == "workspace":
    workspace_page()
