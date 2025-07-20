import streamlit as st
import json
import os

def load_users():
    USERS_FILE = "users.json"
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    USERS_FILE = "users.json"
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def set_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def login_page():
    set_background("https://static.vecteezy.com/system/resources/previews/035/898/034/large_2x/ai-generated-little-boy-playing-with-a-toy-robot-in-the-field-at-sunset-a-child-playing-with-a-toy-robot-ai-generated-free-photo.jpg")
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    users = load_users()
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.experimental_set_query_params(page="main")
            st.rerun()
        else:
            st.error("Invalid username or password")
    if st.button("Go to Register"):
        st.experimental_set_query_params(page="register")
        st.rerun()

def register_page():
    set_background("https://wallpaperaccess.com/full/6717480.jpg")
    st.title("Register Page")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    users = load_users()
    if st.button("Register"):
        if new_username in users:
            st.error("Username already exists!")
        else:
            users[new_username] = new_password
            save_users(users)
            st.success("Registration successful! Please login.")
    if st.button("Back to Login"):
        st.experimental_set_query_params(page="login")
        st.rerun()

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.experimental_set_query_params(page="login")
    st.rerun()
