import streamlit as st
import toolkit
from langchain.prompts import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import LLMChain
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA

# Prompt Templates 
get_question_list = "List all explicitly written questions in the file with a :: between each question"

def get_answers(llm):
    question_template = PromptTemplate(
        input_variables=['question'],
        template='Give me the answer for this question: {question}'
    )
    return LLMChain(llm=llm, prompt=question_template, verbose=True, output_key='question')


def answers(llm):
    txt_docs = None
    file = st.file_uploader('Upload Question Paper', type='pdf')
    if file is not None:
        toolkit.upload_pdf_to_firestore(file)
        txt_docs = toolkit.pdf_to_txt(file)
    if txt_docs: 
        embeddings = OpenAIEmbeddings()
        text_splitter = CharacterTextSplitter(        
            separator = "\n",
            chunk_size = 1000,
            chunk_overlap  = 0,
        )
        splitDocs = text_splitter.split_documents(txt_docs)
        db = FAISS.from_documents(splitDocs, embeddings)
        qa = RetrievalQA.from_chain_type(llm=llm, chain_type= "stuff", retriever= db.as_retriever())
        questions = qa.run(get_question_list).output['answers']
        question_chain = get_answers(llm)
        # result = ""
        for question in questions.split('::'):
            st.write(question)
            answer = question_chain.run(question)
            st.write(answer)
            # result += "question: " + question + "\n" + "answer: " + answer + "\n"
        # st.write(result)