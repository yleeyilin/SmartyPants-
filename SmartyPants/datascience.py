import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.utilities import WikipediaAPIWrapper 
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
import os
from openai.error import OpenAIError
from toolkit import db_path, excel_to_txt, csv_to_txt, makeLineGraph, searchWeb

def datascience(llm):
    documents = None
    uploaded_file = None
    docs = None
    file_type = st.sidebar.selectbox('Select file type', ['CSV', 'Excel'])
    if file_type == 'CSV':
        uploaded_file = st.file_uploader('Upload CSV file', type='csv')
        if uploaded_file is not None:
            documents = csv_to_txt(uploaded_file, db_path)
            csv_path = os.path.join(db_path, uploaded_file.name)
    elif file_type == 'Excel':
        uploaded_file = st.file_uploader('Upload Excel file', type='xlsx')
        if uploaded_file is not None:
            excel_data = uploaded_file.read()
            documents = excel_to_txt(excel_data, db_path)
    data = st.text_input('What is this dataset about?')
    todo = st.text_input('What do you need me to do?')
    topic_template = PromptTemplate(
        input_variables = ['topic'], 
        template='Write a short exerpt on {topic}'
    ) 
    try:
        if documents: 
            chain = load_qa_chain(llm, chain_type="stuff")
            embeddings = OpenAIEmbeddings()
            text_splitter = CharacterTextSplitter(        
                separator = "\n",
                chunk_size = 1000,
                chunk_overlap  = 0,
            )
            splitDocs = text_splitter.split_documents(documents)
            db = FAISS.from_documents(splitDocs, embeddings)
            docs = db.similarity_search(todo)
        topic_chain = LLMChain(llm=llm, prompt=topic_template, verbose=True, output_key='topic')
        wiki = WikipediaAPIWrapper()
        if data: 
            topic = topic_chain.run(data)
            wiki_research = wiki.run(data)  
            st.write(topic)
            with st.expander('Research'): 
                st.info(wiki_research)
        if docs and todo:
            fileCheck = chain.run(input_documents=docs, question=todo)
            st.write(fileCheck)
            if csv_path:
                st.image(makeLineGraph(csv_path), use_column_width=True)
                with st.expander('Web Query'): 
                    st.write(searchWeb(csv_path))
    except OpenAIError as error:
        st.write('No output...Write down what you want me to do!')