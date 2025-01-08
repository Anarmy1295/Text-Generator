# Text Generator # 

1) Short description

This application, developed using Streamlit, provides a user-friendly interface for interacting with a text generator. To access the application, users must log in or create an account. When creating a new account, a default profile picture is assigned, which can be customized later. The database securely stores user information along with the profile picture. Once logged in, users can interact with the app by entering text or uploading documents. The generator processes the input and provides a response. Various settings and options are available through a sidebar menu, offering a personalized experience. In the Home section, users can choose between two modes of text generation: a fast mode that prioritizes speed but offers lower quality, or a slow mode that focuses on delivering higher-quality responses. Additionally, users have the ability to stop the text generation process at any time. The Settings section allows users to update their profile picture, delete their account, or change their password. In the Preferences section, users can customize the text font, change the bot’s name and avatar, or log out of the application.

2) Github link

https://github.com/Anarmy1295/Text-Generator

4) Technologies used

Frontend: streamlit, sqlite3, hashlib, base64, time, pdfplumber

Backend: AutoModelForCausalLM, AutoTokenizer, GPT2LMHeadModel, GPT2Tokenizer, torch

5) Running instructions

streamlit run main.py

7) Team Contributions and Challenges Faced

Delia-Maria Rizescu: I contributed to the development of the application's frontend using Streamlit. I implemented features such as login/create account, the sidebar navigation menu, sections for profile and preference configuration, as well as options for text generation. Additionally, I integrated mechanisms that allow users to personalize their experience, such as changing the text font or setting a custom avatar for the bot.

The main difficulty I faced was getting used to Streamlit since it was something entirely new to me. Adapting to its structure and learning how to use its components effectively required additional time and effort. By exploring the documentation, experimenting with features, and resolving issues as they came up, I managed to implement the functionalities. Another challenge was the addition of new functionalities that required changes to existing ones. For example, initially, I only planned for a database with usernames and passwords, but later I had to modify it to associate a picture with each account. This required ensuring the images were correctly saved in the database.

Ana-Maria Ripeanu: I contributed to the development of the application's backend. My work primarily involved: backend logic and algorithms, frontend integration, and parsing text for analysis. I implemented the backend logic, including functions for text processing and generation. Specifically, I developed algorithms for tokenization, k-sequence generation, distinct word handling, and the construction of stochastic matrices for predictive modelling. These components formed the foundation for the text generator's ability to provide contextually accurate responses when the user wants answers based on an uploaded file. I integrated the backend with the frontend and linked the two parts so that when the user uploads a file, the response will be provided based entirely on the text parsed using Markov chains, otherwise are used the two models gpt2 or gpt-neo, based on the user preference in terms of how fast he wants the response. 

The main difficulty I faced was the limitation of the hardware. I tried to use more powerful models to generate better responses, but the hardware resources of my laptop were not powerful enough. Also, when linking the backend with frontend I faced multiple errors I had to solve such as parsing the correct text and debugging. The algorithm that uses stochastic matrices wasn't that challenging, because I have done something similar in octave. Still, I had to search thoroughly to understand how the models I used from HuggingFace work and how to adjust them to the needs of our project.
