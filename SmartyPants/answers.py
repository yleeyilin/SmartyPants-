import streamlit as st
from toolkit import upload_pdf_to_firestore

def answers(llm):
    file = st.file_uploader('Upload Question Paper', type='pdf')
    if file is not None:
        upload_pdf_to_firestore(file)
    