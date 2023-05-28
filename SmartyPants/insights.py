import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

from toolkit import pdf_to_txt
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings

def split(llm, query, documents):
    embeddings = OpenAIEmbeddings()
    text_splitter = CharacterTextSplitter(        
        separator="\n",
        chunk_size=1000,
        chunk_overlap=0,
    )
    splitDocs = text_splitter.split_documents(documents)
    db = FAISS.from_documents(splitDocs, embeddings)
    return db.similarity_search(query)
    
def insights(llm):
    chain = load_qa_chain(llm, chain_type="stuff")
    uploaded_file = st.file_uploader('Upload PDF file', type='pdf')
    if uploaded_file is not None:
        txt_file = pdf_to_txt(uploaded_file)
        if txt_file is not None:
            with st.expander('General summary'): 
                summary = chain.run(input_documents=split(llm, "Summary", txt_file), question="What is the summary here")
                st.write(summary)
            with st.expander('MindMap'): 
                mind_map = nx.Graph() 
                main = chain.run(input_documents=split(llm, "Central Theme", txt_file), question="What is the central topic here") 
                mind_map.add_node(main, font_color='black', node_size=3000)  # Customize main node appearance
                deets = chain.run(input_documents=split(llm, "Thesis", txt_file), question="Identify 5 subtopics and split them by a ,") 
                details = deets.split(',')
                for detail in details:
                    mind_map.add_node(detail, font_color='black', node_size=500)  # Customize subtopic node appearance
                    mind_map.add_edge(main, detail, color='gray', width=1.0)  # Customize edge appearance
                plt.figure(figsize=(10, 8))  # Adjust the figure size for better visibility
                pos = nx.spring_layout(mind_map)  # Use a spring layout for improved node placement
                nx.draw_networkx(mind_map, pos, with_labels=True, node_color='lightblue', font_weight='bold')
                plt.axis('off')
                st.pyplot(plt)
