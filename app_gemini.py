# We can use the same app_openai code if we use from langchain_google_genai import ChatGoogleGenerativeAI
# and create the model using llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

import streamlit as st
from google import genai
from google.genai import types
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Setup streamlit UI
st.set_page_config(page_title="LangChain Demo with OPENAI API", page_icon=":shark:")
st.header("Let's start the chat")

load_dotenv()
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
except Exception as e:
    st.error(f"Failed to configure Gemini: {e}")
    st.stop()

# Initialize the model
model = genai.GenerativeModel('gemini-2.0-flash')      

# generation_config = types.GenerateContentConfig(
#     temperature=0.8,
#     top_p=0.95
# )
generation_config = {
    "temperature": 0.8,
    "top_p": 0.95
}

# chat = client.models.generate_content(
#     model_name="gemini-1.5-flash",
#     content=types.Content(text=""),
#     config=model_config
# )

if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant that can answer questions and help with tasks."}
    ]

def get_response(question):
    """
    Handles the chat interaction flow:
    1. Stores user messages in session state
    2. Generates AI response using Gemini
    3. Stores AI response in session state
    
    st.session_state is Streamlit's way of maintaining state between reruns.
    st.session_state.messages is a list that stores the entire chat history as dictionaries with:
    - 'role': either 'user', 'assistant', or 'system'
    - 'content': the actual message text
    
    The list grows with each interaction, maintaining conversation context.
    """
    
    # Store user message in session state
    st.session_state.messages.append({
        "role": "user", 
        "content": question
    })
    
    # Format entire chat history for Gemini
    chat_history = "\n".join([
        f"{msg['role']}: {msg['content']}" 
        for msg in st.session_state.messages
    ])
    
    # Get AI response from Gemini
    response = model.generate_content(
        chat_history,
        generation_config=generation_config
    )
    assistant_reply = response.text
    
    # Store AI response in session state
    st.session_state.messages.append({
        "role": "assistant", 
        "content": assistant_reply
    })
    
    return assistant_reply

input = st.text_input("Enter your question:")
submit = st.button("Submit")

if submit and input:
    response = get_response(input)
    st.subheader("The response is:")
    st.write(response)
