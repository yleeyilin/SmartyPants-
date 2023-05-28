import streamlit as st

def insights(llm):
    uploaded_file = st.file_uploader('Upload PDF file', type='pdf')