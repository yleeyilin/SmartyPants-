import os
import streamlit as st
from langchain import OpenAI
from apikey import apikey
from exampaper import exampapers
from insights import insights
from datascience import datascience
from smartypants import smartypants
from normal import normal

documents = None

# Instantiate environment 
os.environ['OPENAI_API_KEY'] = apikey

# Header 
st.title('😈 Smarty Pants 😈')
st.markdown("<h1 style='text-align: left; font-size:20px;'>Knowledge at your fingertips</h1>", unsafe_allow_html=True)

# Sidebar selection
file_type = st.sidebar.selectbox('Select tool', ['Generate Answers', 'Generate Exam Paper', 'Generate Insights'])

# Create instance of LLM
llm = OpenAI()

if file_type == 'Generate Answers':
    normal(llm)
elif file_type == 'Generate Exam Paper':
    exampapers(llm)
elif file_type == 'Generate Insights':
    style = st.sidebar.selectbox('Select mode', ['Normal Mode', 'Smarty Pants Mode', 'Data Scientist Mode'])
    if style == 'Normal Mode':
        st.write('Generate basic insights from your pdf')
        insights(llm)
    if style == 'Smarty Pants Mode':
        st.write('Your dumb ass needs help. LOL')
        smartypants(llm)
    if style == 'Data Scientist Mode':
        st.write('So you are a data scientist...')
        datascience(llm)
