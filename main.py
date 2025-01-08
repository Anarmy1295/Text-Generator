# # import backend
# from backend import main_screen

# main_screen()
import streamlit as st
from frontend import main_page, options_menu, init_db, option_func

if "user_data" not in st.session_state:
    st.session_state["user_data"] = {}

if "profile_image" not in st.session_state["user_data"]:
    st.session_state["user_data"]["profile_image"] = None

if "copie" not in st.session_state:
    st.session_state["copie"] = None

if "stop_flag" not in st.session_state:
    st.session_state.stop_flag = False

if "text_saver" not in st.session_state:
    st.session_state.text_saver = ""

if "page" not in st.session_state:
    st.session_state["page"] = "autentification"

if st.session_state["page"] == "autentification":
    init_db()
    option_func()
elif st.session_state["page"] == "main_screen":
    with open("bot1.jpeg", "rb") as image_file:
        default_image_data = image_file.read()
    if "settings" not in st.session_state:
        st.session_state["settings"] = {
            "bot_name": "ChatBot",
            "bot_image": default_image_data,
            "text_color": "#000000",
            "font": "Arial"
        }

    main_page()
    options_menu()