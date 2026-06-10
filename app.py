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
        
        system_prompt = """
        You are an AI Study Assistant.     
        Rules:
        You are an AI Study Assistant.
        Your goal is to help users learn.

        Guidelines:
        - Adapt explanations to the user's level.
        - Use examples when helpful.
        - Use analogies when concepts are difficult.
        - Be accurate before being simple.
        - If the user asks for technical depth, provide it.

        """
        full_prompt = system_prompt + "\n\n" + conversation

        response = model.generate_content(full_prompt)

    ai_response = response.text

    st.session_state.messages.append(
        {
            "role":"assistaant",
            "content":ai_response
        }
    )

    st.rerun()

