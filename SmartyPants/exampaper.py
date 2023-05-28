import streamlit as st

def exampapers(llm):
    uploaded_file = st.file_uploader('Upload Exam PDF file', type='pdf')
