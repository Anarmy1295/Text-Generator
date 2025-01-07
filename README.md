# Text Generator # 

1) Short description

This application, developed using Streamlit, provides a user-friendly interface for interacting with an text generator. To access the application, users must log in or create an account. When creating a new account, a default profile picture is assigned, which can be customized later. The database securely stores user information along with the profile picture. Once logged in, users can interact with the app by entering text or uploading documents. The generator processes the input and provides a response. Various settings and options are available through a sidebar menu, offering a personalized experience. In the Home section, users can choose between two modes of text generation: a fast mode that prioritizes speed but offers lower quality, or a slow mode that focuses on delivering higher-quality responses. Additionally, users have the ability to stop the text generation process at any time. The Settings section allows users to update their profile picture, delete their account, or change their password. In the Preferences section, users can customize the text font, change the bot’s name and avatar, or log out of the application.

2) Github link

3) Technologies used

Frontend: streamlit, sqlite3, hashlib, base64, time, pdfplumber

5) Running instructions

streamlit run app_name

7) Team Contributions and Challenges Faced

Delia-Maria Rizescu: I contributed to the development of the application's frontend using Streamlit. I implemented features such as log in/create account, the sidebar navigation menu, sections for profile and preference configuration, as well as options for text generation. Additionally, I integrated mechanisms that allow users to personalize their experience, such as changing the text font or setting a custom avatar for the bot.
The main difficulty I faced was getting used to Streamlit since it was something entirely new to me. Adapting to its structure and learning how to use its components effectively required additional time and effort. By exploring the documentation, experimenting with features, and resolving issues as they came up, I managed to implement the functionalities. Another challenge was the addition of new functionalities that required changes to existing ones. For example, initially, I only planned for a database with usernames and passwords, but later I had to modify it to associate a picture with each account. This required ensuring the images were correctly saved in the database.
