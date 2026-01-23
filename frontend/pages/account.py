import streamlit as st
import csv
import os

USERS_FILE = "../users.csv"
#Helper functions
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    users = {}
    with open(USERS_FILE, mode="r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                users[row[0]] = row[1]
    return users
def save_user(username, password):
    with open(USERS_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, password])
#Streamlit UI
elif st.session_state.page == "login":
    import pages.account  # UI only shows if page state is 'login'
st.title("Account")
if "user" not in st.session_state:
    st.session_state.user = None
tab1, tab2 = st.tabs(["Login", "Register"])
users = load_users()
#Login
with tab1:
    st.subheader("Login")
    login_user = st.text_input("Username", key="login_user")
    login_pass = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        if login_user in users and users[login_user] == login_pass:
            st.session_state.user = login_user
            st.session_state.page = "workspace"
            st.success(f"Login successful! Welcome {login_user}")
        else:
            st.error("Invalid username or password")
#Register
with tab2:
    st.subheader("Register")
    new_user = st.text_input("New Username", key="reg_user")
    new_pass = st.text_input("New Password", type="password", key="reg_pass")
    if st.button("Register"):
        if new_user in users:
            st.warning("Username already exists. Choose another.")
        elif new_user.strip() == "" or new_pass.strip() == "":
            st.warning("Username and password cannot be empty")
        else:
            save_user(new_user, new_pass)
            st.success("Account created! You can now log in.")
