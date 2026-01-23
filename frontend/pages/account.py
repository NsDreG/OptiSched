import streamlit as st
import csv
import os

USERS_FILE = "users.csv"

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

def show():
    st.title("Account")

    tab1, tab2 = st.tabs(["Login", "Register"])

    users = load_users()

    with tab1:
        st.subheader("Login")
        login_user = st.text_input("Username")
        login_pass = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_user in users and users[login_user] == login_pass:
                st.session_state.user = login_user
                st.session_state.page = "workspace"
                st.success("Login successful!")
            else:
                st.error("Invalid username or password")

    with tab2:
        st.subheader("Register")
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Register"):
            if new_user in users:
                st.warning("User already exists")
            else:
                save_user(new_user, new_pass)
                st.success("Account created! You can now log in.")
