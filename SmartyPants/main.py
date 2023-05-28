import os
import streamlit as st
from langchain import OpenAI
from apikey import apikey
from answers import answers
from exampaper import exampapers
from insights import insights

documents = None

# Instantiate environment 
os.environ['OPENAI_API_KEY'] = apikey

# Header 
st.title('Smarty Pants')
st.markdown("<h1 style='text-align: left; font-size:20px;'>Knowledge at your fingertips</h1>", unsafe_allow_html=True)

# Sidebar selection
file_type = st.sidebar.selectbox('Select tool', ['Generate Exam Paper', 'Generate Answers', 'Generate Insights'])

# Create instance of LLM
llm = OpenAI()

if file_type == 'Generate Exam Paper':
    exampapers(llm)
elif file_type == 'Generate Answers':
    answers(llm)
elif file_type == 'Generate Insights':
    insights(llm)