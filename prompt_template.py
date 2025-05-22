import streamlit as st
import os
from langchain_core.prompts import ChatPromptTemplate
# from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
# import getpass
# if "GOOGLE_API_KEY" not in os.environ:
#     os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

from langchain_core.prompts import ChatPromptTemplate

st.title("Celibrity search engine")
input_text = st.text_input("Enter the name of the celebrity")

# prompt_template = PromptTemplate(
#     input_variables=["text"],
#     template="Tell me about the celebrity: {text}"
# )

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "Tell me about the celebrity: {text}"),
        ("human", "{text}")
    ]
)

# Second prompt to get birth date
prompt_template2 = ChatPromptTemplate.from_messages(
    [
        ("system", "What is the date of birth of the celebrity: {general_info}"),
        ("human", "{general_info}")
    ]
)

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature= 0.8, top_p= 0.95, google_api_key=os.environ["GEMINI_API_KEY"])
# GENERATION CONFIG IS NOT SUPPORTED IN LANGCHAIN GEMINI
# generation_config = {
#     "temperature": 0.8,
#     "top_p": 0.95
# }

# Create chains for both prompts
chain1 = prompt_template | llm
chain2 = prompt_template2 | llm

# llm_chain = LLMChain(llm=llm, prompt=prompt_template, generation_config=generation_config, verbose=True)
# llm_chain = prompt_template | llm

# This method is typically used when the model expects input in a structured format (like a dictionary).
if input_text:
    # st.write(llm_chain.invoke({"text": input_text}).content)
    # Execute both chains in sequence
    general_info = chain1.invoke({"text": input_text}).content
    birth_date = chain2.invoke({"general_info": general_info}).content
    
    # Display both responses
    st.subheader("General Information:")
    st.write(general_info)
    
    st.subheader("Birth Date:")
    st.write(birth_date)

# This method is typically used when the model expects input in a free-form text format.
# if input_text:
#     st.write(llm_chain.run(input_text))




# EXAMPLE OF A PROMPT TEMPLATE WHERE INPUT IS GIVEN IN JSON FORMAT AS MULTIPLE INPUTS ARE REQUIRED
# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You are a helpful assistant that translates {input_language} to {output_language}.",
#         ),
#         ("human", "{input}"),
#     ]
# )

# chain = prompt | llm
# chain.invoke(
#     {
#         "input_language": "English",
#         "output_language": "German",
#         "input": "I love programming.",
#     }
# )

