import streamlit as st
import pandas as pd
import os

class OptiSchedApp:
    def __init__(self):
        # ---------- Session State ----------
        if "page" not in st.session_state:
            st.session_state.page = "main"
        if "timetable_df" not in st.session_state:
            st.session_state.timetable_df = None

        # ---------- Load CSS ----------
        self.load_css()

        # ---------- Set page config ----------
        st.set_page_config(page_title="OptiSched", layout="wide")

        # ---------- Run page ----------
        self.run_page()

    # ------------------ Load CSS ------------------
    def load_css(self):
        CSS_FILE = os.path.join(os.path.dirname(__file__), "css", "style.css")
        if os.path.exists(CSS_FILE):
            with open(CSS_FILE) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # ------------------ Main Page ------------------
    def main_page(self):
        with st.container():
            st.markdown('<div class="section-block">', unsafe_allow_html=True)
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
            st.markdown('</div>', unsafe_allow_html=True)

    # ------------------ Workspace Page ------------------
    def workspace_page(self):
        st.header("AI Workspace")

        # Back button
        if st.button("← Back to Main Page"):
            st.session_state.page = "main"
            st.rerun()

        st.write("---")

        # ---------- Template Download Block ----------
        with st.container():
            st.markdown('<div class="section-block">', unsafe_allow_html=True)
            st.markdown('<h3>Download Template</h3>', unsafe_allow_html=True)

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
            st.markdown('</div>', unsafe_allow_html=True)

        st.write("---")

        # ---------- Upload Timetable Block ----------
        with st.container():
            st.markdown('<div class="section-block alt">', unsafe_allow_html=True)
            st.markdown('<h3>Upload Your Timetable</h3>', unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])

            if uploaded_file:
                try:
                    if uploaded_file.name.endswith(".xlsx"):
                        df = pd.read_excel(uploaded_file)
                    else:
                        df = pd.read_csv(uploaded_file)

                    expected_days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
                    if list(df.columns) != expected_days:
                        st.error(f"Invalid format! Columns must be: {expected_days}")
                    else:
                        st.session_state.timetable_df = df
                        st.success("Timetable loaded successfully!")

                except Exception as e:
                    st.error(f"Error loading file: {e}")

            st.markdown('</div>', unsafe_allow_html=True)

        st.write("---")

        # ---------- AI Assistant + Timetable Block ----------
        with st.container():
            st.markdown('<div class="section-block">', unsafe_allow_html=True)
            left_col, right_col = st.columns([1, 2])

            with left_col:
                st.markdown('<h3>AI Assistant</h3>', unsafe_allow_html=True)
                if st.session_state.timetable_df is not None:
                    user_message = st.text_area(
                        "Type your instruction (e.g. Add Math test on Friday at 10:00)",
                        height=200
                    )
                    if st.button("Send"):
                        st.info("Instruction will be processed by the AI planner (coming soon).")
                else:
                    st.info("Upload a timetable first to interact with AI.")

            with right_col:
                st.markdown('<h3>Timetable</h3>', unsafe_allow_html=True)
                if st.session_state.timetable_df is not None:
                    st.dataframe(
                        st.session_state.timetable_df.style.set_table_styles([
                            {'selector': 'th', 'props': [('background-color', '#7b2ff7'), ('color', 'white')]},
                            {'selector': 'td', 'props': [('background-color', '#1e1e2f'), ('color', 'white')]}
                        ]),
                        height=400
                    )

                    csv_data = st.session_state.timetable_df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "Download Updated Timetable",
                        csv_data,
                        "optisched_timetable.csv",
                        "text/csv"
                    )
                else:
                    st.info("Timetable will appear here after upload.")
            st.markdown('</div>', unsafe_allow_html=True)

    # ------------------ Run page ------------------
    def run_page(self):
        if st.session_state.page == "main":
            self.main_page()
        elif st.session_state.page == "workspace":
            self.workspace_page()


# ------------------ Launch App ------------------
if __name__ == "__main__":
    OptiSchedApp()
