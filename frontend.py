import streamlit as st
import sqlite3
import hashlib

def mfunc():
    # titlul de inceput
    st.title("Welcome to miniChat")

    option = st.radio("Choose an option", ["Create account", "Log in"])

    if option == "Create account":
        username = st.text_input(":blue[Username]", placeholder = 'Enter your username')
        password = st.text_input(":blue[Password]", type="password", placeholder = 'Enter your password')
        password_confirm = st.text_input(":blue[Confirm password]", type="password", placeholder = 'Confirm your password')

        if st.button("Create account"):
            if password == password_confirm:
                create_account(username, password)
                st.session_state["page"] = "main_screen"
                st.rerun()
            else:
                st.error("Passwords are different.")

    elif option == "Log in":
        username = st.text_input(":blue[Username]", placeholder = 'Enter your username')
        password = st.text_input(":blue[Password]", type="password", placeholder = 'Enter your password')

        if st.button("Connect"):
            if log_in(username, password):
                st.success(f"Welcome, {username}!")
                st.session_state["page"] = "main_screen"
                st.rerun()
                
            else:
                st.error("Username or password are invalid!")

def log_in(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # cauta username-ul si parola specificata in baza de date
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password_hash))
    
    user = c.fetchone()
    conn.close()
    
    if user:
        return True
    else:
        return False

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
    conn = sqlite3.connect('users.db')
    # creeaza un cursor
    c = conn.cursor()
    
    # cripteaza parola pentru securitatea datelor
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_hash))

        # confirma si salveaza schimbarile efectuate in baza de date
        conn.commit()
        st.success("Account created successfully!")
        #st.rerun()
        #st.session_state["page"] = "main_screen"
    except sqlite3.IntegrityError:
        st.error("Username is already in use.")
    
    conn.close()

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Funcție pentru pagina principală
def main_page():
    # Centrarea casetei de text pe pagină
    st.title("Welcome to Text Generator")
    
    # Casetă de text centrală
    input_text = st.text_area("Enter some text here...", height=200)
    
    # Afișează textul introdus
    if input_text:
        st.write("You entered:", input_text)

if "page" not in st.session_state:
    st.session_state["page"] = "autentification"

if st.session_state["page"] == "autentification":
    init_db()
    mfunc()
elif st.session_state["page"] == "main_screen":
    st.session_state.selected_option = "Home"
    main_page()