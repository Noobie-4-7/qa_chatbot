import streamlit as st
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

# Setup streamlit UI
st.set_page_config(page_title="LangChain Demo with OPENAI API", page_icon=":shark:")
st.header("Let's start the chat")

load_dotenv()
chat = ChatOpenAI(temperature=0.8, openai_api_key=os.getenv("OPENAI_API_KEY"))

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        SystemMessage(content="You are a helpful assistant that can answer questions and help with tasks.")
    ]

def get_response(question):
    st.session_state['messages'].append(HumanMessage(content=question))
    answer = chat(st.session_state['messages'])
    st.session_state['messages'].append(AIMessage(content=answer.content))
    return answer.content

input = st.text_input("Enter your question:")
submit = st.button("Submit")
response = get_response(input)

if submit:
    st.subheader("The response is:")
    st.write(response)
    
