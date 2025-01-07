import streamlit as st
import sqlite3
import hashlib
import base64
import time
from gtts import gTTS
import os
import tempfile
import pdfplumber
from docx import Document
from backend import generate_response

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

                # salveaza datele utilizatorului in st.session_state
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
        # daca utilizatorul exista, returnează datele acestuia
        return {
            "username": user[0],
            "password": user[1],
            # verificare ca imaginea exista
            "profile_image": user[2] if user[2] else None
        }
    else:
        return None
    
def change_profile_image(username, new_image):
    conn = sqlite3.connect('users1.db')
    c = conn.cursor()
    
    c.execute("UPDATE users SET profile_image = ? WHERE username = ?", (new_image , username))
    conn.commit()
    conn.close()


def create_account(username, password):

    # conditii pentru o parola mai puternica
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


# functie pentru pagina principala
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

    # verifica daca utilizatorul a trimis un mesaj
    if "started_chat" not in st.session_state:
        st.session_state["started_chat"] = False

    # afisam titlul doar daca utilizatorul nu a trimis mesaje
    if not st.session_state["started_chat"]:
         st.title("Welcome to Text Generator")
    
    
   
    # stiluri CSS pentru a alinia mesajele utilizatorului și ale asistentului cu poza
    # se pune important petru a nu a se suprascrie setari deja predefinite
    st.markdown("""
        <style>
        .chat-user-container {
            display: flex;
            flex-direction: row-reverse;
            align-items: center;
            margin-bottom: 10px;
        }
        .chat-assistant-container {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        .chat-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin-left: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <style>
        .chat-assistant {{
            background-color: #F0F0F0;
            border-radius: 10px;
            padding: 10px;
            max-width: 70%;
            text-align: left;
            color: {st.session_state["settings"]["text_color"]} !important;
            font-family: {st.session_state["settings"]["font"]};
            margin-left: 10px;
        }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <style>
        .chat-user {{
            background-color: #F0F0F0;
            border-radius: 10px;
            padding: 10px;
            max-width: 70%;
            text-align: left;
            color: {st.session_state["settings"]["text_color"]} !important;
            font-family: {st.session_state["settings"]["font"]};
            margin-left: 10px;
        }}
    </style>
    """, unsafe_allow_html=True)

    # initializeaza istoricul conversatiei în session_state
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    if "pdf/doc" not in st.session_state:
        st.session_state["pdf/doc"] = False

    if "copie" not in st.session_state:
        st.session_state["copie"] = None

    
    uploaded_file = st.file_uploader("Upload a PDF or Word Document", type=["pdf", "docx"])
    
    if uploaded_file:
        if uploaded_file != st.session_state["copie"]:
            st.session_state["copie"] = uploaded_file 
            st.session_state["pdf/doc"] = True
            file_name, file_extension = os.path.splitext(uploaded_file.name)
            
            if file_extension == ".pdf":
                st.write("Processing PDF file...")
                try:
                    with pdfplumber.open(uploaded_file) as pdf:
                        text = ""
                        for page in pdf.pages:
                            text += page.extract_text()
                except Exception as e:
                    st.error(f"Error processing PDF: {str(e)}")
            
            elif file_extension == ".docx":
                st.write("Processing Word file...")
                try:
                    doc = Document(uploaded_file)
                    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                except Exception as e:
                    st.error(f"Error processing Word document: {str(e)}")
            else:
                st.warning("Unsupported file type.")

            st.session_state["messages"].append({"role": "user", "content":"file", "last": False})

            # genereaza raspuns in functie de mod
            if st.session_state["chat_mode"] == "faster":
                # assistant_response = f"{text}"
                assistant_response = generate_response(text, "faster")
            else:
                assistant_response = generate_response(text, "slower")
            
            st.session_state["messages"].append({"role": "assistant", "content": assistant_response, "processed": False})

    
    if prompt := st.chat_input("Say something"):
        st.session_state["started_chat"] = True

        # adauga mesajul user-ului la istoric
        st.session_state["messages"].append({"role": "user", "content": prompt, "last": False})

        # genereaza raspuns in functie de mod
        if st.session_state["chat_mode"] == "faster":
            # assistant_response = f"{prompt}"
            assistant_response = generate_response(prompt, "faster")
        else:
            assistant_response = generate_response(prompt, "slower")
        
        st.session_state["messages"].append({"role": "assistant", "content": assistant_response, "processed": False})


    bot_text = []
    # afiseaza toate mesajele din istoric fara ultimul 
    for i, message in enumerate(st.session_state["messages"]):
        if message["role"] == "user":

            st.markdown(f"""
                <div class="chat-user-container">
                    <div class="chat-user">{"You: " + message["content"]}</div>
                    <img src="data:image/jpeg;base64,{st.session_state['user_data']['profile_image']}" class="chat-avatar" alt="User Avatar"/>
                </div>
            """, unsafe_allow_html=True)

            if not message.get("last", False):  # default: False dacă cheia nu exista
                if "secret" in message["content"]:
                    st.balloons()
                # marcheaza mesajul ca procesat
                message["last"] = True

        else:

            # daca e ultimul mesaj adica neprocesat, se pune text progresiv, iar in
            # caz contrar se scrie normal
            if  message["processed"] == False:

                # container separat pentru text
                container = st.empty()

                bot_image_base64 = base64.b64encode(st.session_state["settings"]["bot_image"]).decode("utf-8")

                text = message["content"]
            
                # text progresiv
                output_text = ""
                for word in animated_text_display(text):
                  
                    if st.session_state.stop_flag:
                        st.session_state["messages"][i]["content"] = st.session_state.text_saver
                        break

                    output_text += word
                    st.session_state.text_saver = output_text
                
                    container.markdown(
                        f"""
                        <div class="chat-assistant-container">
                            <img src="data:image/jpeg;base64,{bot_image_base64}" class="chat-avatar" alt="Assistant Avatar"/>
                            <div class="chat-assistant">{st.session_state["settings"]["bot_name"] + ": " + output_text}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                        )

                if st.session_state.stop_flag:
                    st.session_state.stop_flag = False
                    container.markdown(
                        f"""
                        <div class="chat-assistant-container">
                            <img src="data:image/jpeg;base64,{bot_image_base64}" class="chat-avatar" alt="Assistant Avatar"/>
                            <div class="chat-assistant">{st.session_state["settings"]["bot_name"] + ": " + st.session_state["messages"][i]["content"]}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                        )
                    
                message["processed"] = True

            else:
                bot_image_base64 = base64.b64encode(st.session_state["settings"]["bot_image"]).decode("utf-8")

                st.markdown(f"""
                    <div class="chat-assistant-container">
                        <img src="data:image/jpeg;base64,{bot_image_base64}" class="chat-avatar" alt="Assistant Avatar"/>
                        <div class="chat-assistant">{st.session_state["settings"]["bot_name"] + ": " +  message["content"]}</div>
                    </div>
                """, unsafe_allow_html=True)


            # adaugarea feedback dupa fiecare mesaj
            sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]
            selected = st.feedback("thumbs", key=f"feedback_{i}")  # Unique key using message index
            if selected is not None:
                st.markdown(f"You selected: {sentiment_mapping[selected]}")

            if st.button("🗑️", key=f"trash_button{i}"):
                st.session_state["messages"] = []
                st.session_state["started_chat"] = False
                st.rerun()

            if st.button("🔊", key=f"text-to-speech_button{i}"):
                bot_text = st.session_state["messages"][i]["content"]
                if bot_text:
                    speech = gTTS(text=bot_text, lang='en', slow=False)

                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmpfile:
                        speech.save(tmpfile.name)
                        st.audio(tmpfile.name, format='audio/mp3')


# text progresiv(cu delay)
def animated_text_display(text, delay=0.2):
    for word in text.split(" "):
        yield word + " "
        time.sleep(delay)

        
def reset_password(username, new_password):
    password_hash = hashlib.sha256(new_password.encode()).hexdigest()

    conn = sqlite3.connect('users1.db')
    c = conn.cursor()
    
    # verifica daca utilizatorul exista
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    
    if not user:
        conn.close()
        return False  # utilizatorul nu exista
    
    # actualizare parola
    c.execute("UPDATE users SET password = ? WHERE username = ?", (password_hash, username))
    conn.commit()
    conn.close()
    
    return True

# funcție pentru optiuni
def options_menu():

    if "selected_option" not in st.session_state:
        st.session_state.selected_option = "Home"

    st.sidebar.title("Options Menu")

    tab1, tab2, tab3, tab4 = st.sidebar.tabs(["🏠Home", "🖋️Preferences", "⚙️Settins", "🔒Log out"])

    # implicit se seteaza slower daca utilizatorul nu alege
    if "chat_mode" not in st.session_state:
        st.session_state["chat_mode"] = "slower"

    # in home avem optiuni pentru modul generatorului
    with tab1:
        st.markdown("<h1 style='text-align: center; font-size:32px; font-weight:bold; color:lightblue;'>Welcome to Text Generator🤖</h1>", unsafe_allow_html=True)

        st.write("Write a question and the generator will try to answer.")
        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown(
            """
            <p style="color:gray; font-size:17px;">
        You have two text generation options (the first one is the default if no choice is made):
            </p>
            """,
        unsafe_allow_html=True,
        )

        if st.button("🐢🌟Slower, but higher quality"):
            st.session_state["chat_mode"] = "slower"

        if st.button("⚡🔧Faster, but lower quality"):
            st.session_state["chat_mode"] = "faster"
        
        if st.session_state["chat_mode"] == "slower":
            st.write(" ")
            st.write("You are in higher quality mode")
        else:
            st.write(" ")
            st.write("You are in lower quality mode")

        st.button("Stop generate", on_click=stop_generation)

    with tab2:
        st.title("Preferences")

        # schimbare nume bot
        bot_name = st.text_input("Bot Name", value=st.session_state["settings"]["bot_name"])
        if bot_name != st.session_state["settings"]["bot_name"]:
            st.session_state["settings"]["bot_name"] = bot_name
            st.rerun()

        # schimbare imagine bot
        bot_image = st.file_uploader("Upload an image for the bot", type=["jpg", "jpeg", "png"])
        if bot_image:  # Verifică dacă s-a încărcat un fișier
            bot_image_data = bot_image.read()  # Citește conținutul fișierului
            st.session_state["settings"]["bot_image"] = bot_image_data
            st.rerun()

        # alege culoare textului user-ului si al bot-ului
        text_color = st.color_picker("Pick text color", value=st.session_state["settings"]["text_color"])
        if text_color != st.session_state["settings"]["text_color"]:
            st.session_state["settings"]["text_color"] = text_color
            st.rerun()

        #  alege stilul textului
        font = st.selectbox("Choose font", ["Arial", "Courier", "Times New Roman", "Georgia"], index=["Arial", "Courier", "Times New Roman", "Georgia"].index(st.session_state["settings"]["font"]))
        if font != st.session_state["settings"]["font"]:
            st.session_state["settings"]["font"] = font
            st.rerun()

    with tab3:
        st.title("User Settings")

        uploaded_file = st.file_uploader("Upload Profile Picture", type=["jpg", "png", "jpeg"])
        
        if uploaded_file:
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

        # pun o line intre sectiuni pentru a delimita mai bine
        st.markdown("<hr>", unsafe_allow_html=True)

        st.write("Reset password")
        username = st.text_input(":blue[Username]", placeholder = 'Enter your username,',  key="change_username")
        new_password = st.text_input(":blue[Password]", type="password", placeholder = 'Enter your new password')
        confirm_password = st.text_input(":blue[Confirm password]", type="password", placeholder = 'Confirm your new password')


        if st.button("Reset Password"):
            if new_password != confirm_password:
                st.error("Passwords do not match!")
            elif len(new_password) < 4:
                st.error("Password must be at least 4 characters long!")
            else:
                success = reset_password(username, new_password)
                if success:
                    # st.success(f"Password successfully reset for user: {username}")

                    if "info_reset" in st.session_state:
                        del st.session_state['info_reset']

                    if "info_reset" not in st.session_state:
                        info_reset()

                else:
                    st.error("User does not exist!")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.write("Delete Account")

        if st.button("Delete Account"):
            if "vote1" in st.session_state:
                del st.session_state['vote1']

            if "vote1" not in st.session_state:
                vote1()
     
    with tab4:
        st.header("Log Out")

        if st.button("Log Out"):
            st.session_state["messages"] = []
            st.session_state["started_chat"] = False

            if "vote" in st.session_state:
                del st.session_state['vote']

            if "vote" not in st.session_state:
                vote()

def delete_account(username, password):
    conn = sqlite3.connect('users1.db')
    c = conn.cursor()
    
    # verificare daca utilzatorul exista
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    
    if user:
        c.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        st.success("Account deleted successfully!")
    else:
        st.error("Invalid username or password.")
    
    # inchide conexiunea
    conn.close()

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

@st.dialog("Are you sure you want to delete the account?")
def vote1():
    if st.button("Yes"):
        delete_account(st.session_state["user_data"]["username"], st.session_state["user_data"]["password"])
        st.session_state["page"] = "autentification"
        st.session_state.vote1 = True
        st.rerun()
    if st.button("Cancel"):
        st.session_state.vote1 = True
        st.rerun()

@st.dialog("The password has been reset")
def info_reset():
    if st.button("Ok"):
        st.session_state["page"] = "autentification"
        st.rerun()

# if "user_data" not in st.session_state:
#     st.session_state["user_data"] = {}

# if "profile_image" not in st.session_state["user_data"]:
#     st.session_state["user_data"]["profile_image"] = None

# if "copie" not in st.session_state:
#     st.session_state["copie"] = None

# if "stop_flag" not in st.session_state:
#     st.session_state.stop_flag = False

# if "text_saver" not in st.session_state:
#     st.session_state.text_saver = ""
 
# def stop_generation():
#     st.session_state.stop_flag = True

# if "page" not in st.session_state:
#     st.session_state["page"] = "autentification"

# if st.session_state["page"] == "autentification":
#     init_db()
#     option_func()
# elif st.session_state["page"] == "main_screen":
#     with open("bot1.jpeg", "rb") as image_file:
#         default_image_data = image_file.read()
#     if "settings" not in st.session_state:
#         st.session_state["settings"] = {
#             "bot_name": "ChatBot",
#             "bot_image": default_image_data,
#             "text_color": "#000000",
#             "font": "Arial"
#         }

#     main_page()
#     options_menu()