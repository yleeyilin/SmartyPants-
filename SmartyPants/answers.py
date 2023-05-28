import streamlit as st

def answers(llm):
    uploaded_file = st.file_uploader('Upload Question', type='pdf')