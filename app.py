import streamlit as st
import google.generativeai as genai
import time
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

st.title("AI Study Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


user_input = st.chat_input("Ask me anything")

if user_input:
    st.session_state.messages.append(
        {
            "role":"user",
            "content": user_input
        }
    )

    conversation = ""

    for message in st.session_state.messages:

        role =message["role"].capitalize()
        content = message["content"]

        conversation += f"{role}: {content}\n"
    
    with st.spinner("soch rha hu....."):
        response = model.generate_content(conversation)

    ai_response = response.text

    st.session_state.messages.append(
        {
            "role":"assistaant",
            "content":ai_response
        }
    )

    st.rerun()

