import streamlit as st
import toolkit

def answers(llm):
    txt_docs = None
    file = st.file_uploader('Upload Question Paper', type='pdf')
    if file is not None:
        toolkit.upload_pdf_to_firestore(file)
        txt_docs = toolkit.pdf_to_txt(file)
    