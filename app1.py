import os
import streamlit as st
import google.generativeai as geai
from dotenv import load_dotenv

load_dotenv()
geai.configure(api_key=os.getenv("GOOGLE_GEMINI_KEY"))

# Initial welcome message with custom formatting
st.markdown("<h1 style='text-align: center; font-size: 26px; font-weight: bold;'>Welcome to the Chat App! How can I help you today?</h1>", 
            unsafe_allow_html=True)

# Initialize an empty dictionary to store multiple chat sessions
if "chats" not in st.session_state:
    st.session_state.chats = {}

# Create a list of chat options
chat_options = list(st.session_state.chats.keys())

# Add "New Chat" option dynamically
new_chat_name = st.sidebar.text_input("Create New Chat", key="new_chat_name")
if st.sidebar.button("Add New Chat") and new_chat_name and new_chat_name not in chat_options:
    chat_options.append(new_chat_name)
    st.session_state.chats[new_chat_name] = geai.GenerativeModel("gemini-pro").start_chat(history=[])
    st.sidebar.success(f"Chat '{new_chat_name}' added successfully!")

# Sidebar to select different chat sessions
selected_chat =    st.sidebar.selectbox("Select Chat", chat_options, index=len(chat_options)-1)


# Get or create the selected chat
current_chat = st.session_state.chats.get(selected_chat, geai.GenerativeModel("gemini-pro").start_chat(history=[]))

# Use a default value if selected_chat is None
selected_chat = selected_chat or "new chat"

# Display the chat title without "Chat with" prefix with increased font size using Markdown
st.markdown(f"<h1 style='text-align: center; font-size: 24px;'>{selected_chat.capitalize()}</h1>",
                unsafe_allow_html=True)


def role_to_streamlit(role):
    return "assistant" if role == "model" else role

# Display chat history
for message in current_chat.history:
    with st.chat_message(role_to_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# User input and model response
if prompt := st.chat_input("What can I do for you?"):
    st.chat_message("user").markdown(prompt)
    try:
        response = current_chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except geai.generation_types.StopCandidateException as stop_exception:
        st.error("Error: The generative model encountered an issue. Please try again.")
st.empty()                