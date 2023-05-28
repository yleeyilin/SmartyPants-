import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

from toolkit import pdf_to_txt, split
from langchain.chains.question_answering import load_qa_chain

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
                    mind_map.add_node(detail, font_color='black', node_size=500)  
                    mind_map.add_edge(main, detail, color='gray', width=1.0)  
                plt.figure(figsize=(10, 8)) 
                pos = nx.spring_layout(mind_map)  
                nx.draw_networkx(mind_map, pos, with_labels=True, node_color='lightblue', font_weight='bold')
                plt.axis('off')
                st.pyplot(plt)