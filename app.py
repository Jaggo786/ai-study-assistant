import streamlit as st
import google.generativeai as genai
import time
from dotenv import load_dotenv
import os
import json
from pypdf import PdfReader

st.title("AI Study Assistant")

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

with st.expander("<---- PDF Question Answering ---->"):
    
    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file:
        reader = PdfReader(uploaded_file)
        st.write("Pages :" ,len(reader.pages))
        pdf_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pdf_text += text + "\n\n"

        chunk_size = 500

        chunks = []

        for i in range(0, len(pdf_text), chunk_size):
            chunk = pdf_text[i:i + chunk_size]
            chunks.append(chunk)
        
        pdf_question = st.text_input(
            "Ask a question about the pdf"
        )
        selected_chunk = ""
        
        if pdf_question:
            question = pdf_question.lower()

            for chunk in chunks:
                if any(word in chunk.lower() for word in question.split()):
                    selected_chunk = chunk
                    break
            
        st.write("number of chunks:" , len(chunks))
        
        


        st.write("Characters:" ,len(pdf_text))
        

        with open("uploaded_pdf.txt", "w", encoding = "utf-8") as file:
            file.write(pdf_text)

        st.success("pdf saved successfully")
        
        if pdf_question:
            prompt = f"""
            Use the following context to answer the question.
            Context:
            {selected_chunk}
            Question:
            {pdf_question}
            """
            response = model.generate_content(prompt)
            st.write(response.text)
            
            



CHAT_FILE = "chat_history.json"


if "messages" not in st.session_state:

    try:
        with open(CHAT_FILE, "r") as file:
            st.session_state.messages = json.load(file)

    except:
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

    with open(CHAT_FILE, "w") as file:
        json.dump(st.session_state.messages, file)

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
            "role":"assistant",
            "content":ai_response
        }
    )

    st.rerun()

