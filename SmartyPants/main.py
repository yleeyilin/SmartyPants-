import os
import streamlit as st
from apikey import apikey
from answers import answers
from exampaper import exampapers
from insights import insights

# Instantiate environment 
os.environ['OPENAI_API_KEY'] = apikey

# Header 
st.title('Smarty Pants')
st.markdown("<h1 style='text-align: left; font-size:20px;'>Knowledge at your fingertips</h1>", unsafe_allow_html=True)

# Sidebar selection
file_type = st.sidebar.selectbox('Select tool', ['Generate Exam Paper', 'Generate Answers', 'Generate Insights'])

if file_type == 'Generate Exam Paper':
    exampapers()
elif file_type == 'Generate Answers':
    answers()
elif file_type == 'Generate Insights':
    insights()