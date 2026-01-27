import streamlit as st

st.set_page_config(page_title="OptiSched", layout="wide")

# ---------- STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "main"

# ---------- COSMIC THEME ----------
st.markdown("""
<style>
body {
    background-color: #0b0b14;
}
.stApp {
    background: radial-gradient(circle at top, #1a0f2e, #05010a);
    color: white;
}
h1, h2, h3 {
    color: #c77dff;
}
button {
    background: linear-gradient(135deg, #7b2cff, #c77dff);
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 18px;
}
.chatbox {
    background: rgba(30, 0, 60, 0.6);
    border-radius: 15px;
    padding: 20px;
}
.tablebox {
    background: rgba(10, 10, 30, 0.7);
    border-radius: 15px;
    padding: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------- MAIN PAGE ----------
if st.session_state.page == "main":
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("OptiSched")
        st.subheader("AI-Powered Adaptive Study Planner")
        st.write("")
        if st.button("Start Planning"):
            st.session_state.page = "workspace"
            st.rerun()

    st.write("\n\n")
    st.markdown("### Why OptiSched?")
    st.info("Replace this with your competition explanation about students, overload, and AI planning.")

    st.markdown("### Key Features")
    st.markdown("""
    • Natural language timetable editing  
    • AI schedule optimization  
    • Real-time visual updates  
    • Smart workload balance  
    """)

# ---------- WORKSPACE ----------
elif st.session_state.page == "workspace":
    st.markdown("## Your AI Study Workspace")

    left, right = st.columns([1,2])

    with left:
        st.markdown('<div class="chatbox">', unsafe_allow_html=True)
        st.subheader("AI Assistant")
        st.text_area("Chat here (e.g. 'Add math test on Monday at 3pm')", height=200)
        st.button("Send")
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="tablebox">', unsafe_allow_html=True)
        st.subheader("Timetable")
        st.info("Your dynamically updated schedule will appear here.")
        st.markdown('</div>', unsafe_allow_html=True)
