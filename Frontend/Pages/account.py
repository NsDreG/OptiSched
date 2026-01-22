import streamlit as st
import pandas as pd
import hashlib
import os

# -------- Constants --------
USERS_FILE = "data/users.csv"

# -------- Helper Functions --------

def hash_password(password):
    """Hash a password using MD5."""
    return hashlib.md5(password.encode()).hexdigest()

def load_users():
    """Load the CSV users file. Create it if it doesn't exist."""
    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame(columns=["username", "password", "email"])
        df.to_csv(USERS_FILE, index=False)
        return df
    return pd.read_csv(USERS_FILE)

def check_login(username, password):
    """Check if the username and password match a user in CSV."""
    users_df = load_users()
    hashed_pw = hash_password(password)
    user = users_df[(users_df['username'] == username) & (users_df['password'] == hashed_pw)]
    return not user.empty

def add_user(username, password, email):
    """Add a new user to CSV if username is not taken."""
    users_df = load_users()
    
    if username in users_df['username'].values:
        return False  # Username already exists
    
    hashed_pw = hash_password(password)
    new_user = pd.DataFrame([[username, hashed_pw, email]], columns=['username','password','email'])
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    users_df.to_csv(USERS_FILE, index=False)
    return True

# -------- Page UI --------

def show():
    """Display login and registration page."""
    
    st.title("Login / Registration")

    # Initialize session state for logged-in user
    if "user" not in st.session_state:
        st.session_state.user = None

    # Choose between Login or Register
    choice = st.radio("Go to", ["Login", "Register"])

    # ----- LOGIN -----
    if choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if check_login(username, password):
                st.success(f"Logged in as {username}")
                st.session_state.user = username
            else:
                st.error("Incorrect username or password")

    # ----- REGISTER -----
    if choice == "Register":
        username = st.text_input("New Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Register"):
            if add_user(username, password, email):
                st.success("Account created! You can now log in.")
            else:
                st.error("Username already taken. Choose another.")
