import streamlit as st
import os
import requests
import json
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

st.set_page_config(page_title="Chatbot UI", page_icon="💬")
st.title("💬 Cricket Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask something about cricket...")

if user_input:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare API request
    req_data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are an experienced cricket commentator."},
            {"role": "user", "content": user_input}
        ]
    }

    # Call Groq API
    response = requests.post(
        URL,
        headers=HEADERS,
        data=json.dumps(req_data)
    )

    assistant_reply = response.json()["choices"][0]["message"]["content"]

    # Function to stream text with delay
    def stream_text(text):
        for word in text.split(" "):
            yield word + " "
            time.sleep(0.05)

    # Display assistant reply with streaming effect
    with st.chat_message("assistant"):
        streamed_text = st.write_stream(stream_text(assistant_reply))

    # Save assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )
