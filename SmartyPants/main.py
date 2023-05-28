import os
import streamlit as st
from apikey import apikey

# Instantiate environment 
os.environ['OPENAI_API_KEY'] = apikey

# Header 
st.title('Smarty Pants')
st.markdown("<h1 style='text-align: left; font-size:20px;'>Exam insights at your fingertips</h1>", unsafe_allow_html=True)

# Sidebar selection
file_type = st.sidebar.selectbox('Select file type', ['CSV', 'Excel', 'PDF'])