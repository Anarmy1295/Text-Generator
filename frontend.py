import streamlit as st
import sqlite3
import hashlib
import base64
import time
from gtts import gTTS
import os
import tempfile

def option_func():
    # titlul de inceput
    st.title("Welcome to Text Generator")

    option = st.radio("Choose an option", ["Create account", "Log in"])

    if option == "Create account":
        username = st.text_input(":blue[Username]", placeholder = 'Enter your username',  key = "create_username")
        password = st.text_input(":blue[Password]", type="password", placeholder = 'Enter your password', key = "create_password")
        password_confirm = st.text_input(":blue[Confirm password]", type="password", placeholder = 'Confirm your password')

        if st.button("Create account"):
            if password == password_confirm:
                create_account(username, password)
                st.session_state["page"] = "main_screen"
                st.rerun()
            else:
                st.error("Passwords are different.")

    elif option == "Log in":
        username = st.text_input(":blue[Username]", placeholder = 'Enter your username',  key = "login_username")
        password = st.text_input(":blue[Password]", type="password", placeholder = 'Enter your password',  key = "login_password")

        if st.button("Connect"):
            user_data = log_in(username, password)
            if user_data:
                st.success(f"Welcome, {username}!")
                st.session_state["page"] = "main_screen"

                # Salvează datele utilizatorului în st.session_state
                st.session_state["user_data"] = user_data
                st.rerun()
                
            else:
                st.error("Username or password are invalid!")

def log_in(username, password):
    conn = sqlite3.connect('users1.db')
    c = conn.cursor()
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # cauta username-ul si parola specificata in baza de date
    c.execute("SELECT username, password, profile_image FROM users WHERE username = ? AND password = ?", (username, password_hash))
    
    user = c.fetchone()
    conn.close()
    
    if user:
        # global username1
        # username1 = username
        # Dacă utilizatorul există, returnează datele acestuia
        return {
            "username": user[0],
            "password": user[1],
            "profile_image": user[2] if user[2] else None  # Asigură-te că profile_image este None dacă nu există
        }
    else:
        return None
    
def change_profile_image(username, new_image):
    conn = sqlite3.connect('users1.db')
    c = conn.cursor()
    
    # Salvăm noua imagine
    #image_data = new_image.getvalue()
    #new_image_base64 = base64.b64encode(image_data).decode()
    
    c.execute("UPDATE users SET profile_image = ? WHERE username = ?", (new_image , username))
    conn.commit()
    conn.close()


def create_account(username, password):

    if len(password) < 4:
        st.error("Password must be at least 4 characters long.")
        return
    
    if not any(char.isupper() for char in password):
        st.error("Password must contain at least one uppercase letter.")
        return
    
    if not any(char.isdigit() for char in password):
        st.error("Password must contain at least one digit.")
        return
    
    # conenctare la baza de date si creeaza user.db daca nu exista
    conn = sqlite3.connect('users1.db')
    # creeaza un cursor
    c = conn.cursor()
    
    # cripteaza parola pentru securitatea datelor
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    #global user_data

    with open("user.jpg", "rb") as img_file:
        image_data = img_file.read()
        profile_image_base64 = base64.b64encode(image_data).decode()
        st.session_state["user_data"]["profile_image"] = profile_image_base64
        #user_data["profile_image"] = profile_image_base64
    
    try:
        c.execute("INSERT INTO users (username, password, profile_image) VALUES (?, ?, ?)", 
                  (username, password_hash, profile_image_base64))

        # confirma si salveaza schimbarile efectuate in baza de date
        conn.commit()
        st.success("Account created successfully!")
        #st.rerun()
        #st.session_state["page"] = "main_screen"
    except sqlite3.IntegrityError:
        st.error("Username is already in use.")
    
    conn.close()

def init_db():
    conn = sqlite3.connect('users1.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            profile_image BLOB
        )
    ''')
    conn.commit()
    conn.close()

def main_page():

    if st.session_state["user_data"]["profile_image"]:
        st.markdown(
            f"""
            <style>
            .profile-pic {{
                width: 70px;
                height: 70px;
                border-radius: 50%;
                object-fit: cover;
                position: fixed;
                top: 60px;  /* Ajustează distanța faaă de partea de sus */
                right: 20px;  /* ajusteaza distanta fata de partea dreapta */
                z-index: 10;  /* imaginea va fi vizibila deasupra altor elemente */
            }}
            </style>
            <img class="profile-pic" src="data:image/jpeg;base64,{st.session_state['user_data']['profile_image']}">
            """,
            unsafe_allow_html=True
        )

   

# Funcție pentru opțiuni
def options_menu():

    if "selected_option" not in st.session_state:
        st.session_state.selected_option = "Home"

    st.sidebar.title("Options Menu")


    tab1, tab2, tab3, tab4 = st.sidebar.tabs(["🏠Home", "🖋️Preferences", "⚙️Settins", "🔒Log out"])

    with tab1:
        st.title("Home")
        st.header("Welcome to Text Generator🤖")
        st.write("Write a question and the generator will try to answer.")
    with tab2:
   

        st.title("Preferences")
 
    with tab3:
        st.header("Setting")

        #st.session_state.selected_option = "Settings"
        # st.write("This is the settings page.")

        st.title("User Settings")

        # Upload Profile Picture
        uploaded_file = st.file_uploader("Upload Profile Picture", type=["jpg", "png", "jpeg"])
        

        if uploaded_file:
            # Encode the image in Base64
            #image_data = uploaded_file.getvalue()

            # image_data = uploaded_file.getvalue()
            # decoded_image = base64.b64decode(image_data)
            # Actualizăm imaginea în session_state
            #st.session_state["profile_image"] =  uploaded_file.getvalue()
            # Salvează imaginea în baza de date
            #user_data = st.session_state["user_data"]

            uploaded_file_base64 = base64.b64encode(uploaded_file.getvalue()).decode()
            st.session_state["user_data"]["profile_image"] = uploaded_file_base64
            change_profile_image(st.session_state["user_data"]["username"], st.session_state["user_data"]["profile_image"])
   

        if st.session_state["user_data"]["profile_image"]:
            st.markdown(
                f"""
                <style>
                .profile-pic {{
                    width: 50px;
                    height: 50px;
                    border-radius: 50%;
                    object-fit: cover;
                    margin: 0 auto;
                    display: block;
                }}
                </style>
                <img class="profile-pic" src="data:image/jpeg;base64,{st.session_state["user_data"]["profile_image"]}">
                """,
                unsafe_allow_html=True
            )

    with tab4:
        st.header("Log Out")

        if st.button("Log Out"):

            if "vote" in st.session_state:
                del st.session_state['vote']

            if "vote" not in st.session_state:
                vote()

@st.dialog("Are you sure you want to log out?")
def vote():
    if st.button("Yes"):
        st.session_state.selected_option = "Home"
        st.session_state.vote = True
        st.session_state["page"] = "autentification"
        st.rerun()
    if st.button("Cancel"):
        st.session_state.vote = True
        st.session_state.selected_option = "Home"
        st.rerun()

if "page" not in st.session_state:
    st.session_state["page"] = "autentification"

if st.session_state["page"] == "autentification":
    init_db()
    option_func()
elif st.session_state["page"] == "main_screen":
    #st.session_state.selected_option = "Home"

    main_page()
    options_menu()