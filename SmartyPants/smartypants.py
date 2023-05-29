import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from toolkit import pdf_to_txt, split
from langchain.chains.question_answering import load_qa_chain
from langchain import LLMChain, PromptTemplate

def smartypants(llm):
    snobby = 'Sound annoyed and nag at me for asking too many questions'
    template = PromptTemplate(
            input_variables = ['snobby'],
            template= 'answer my {snobby}'
        )
    snobby_chain = LLMChain(llm = llm, prompt=template)
    chain = load_qa_chain(llm, chain_type="stuff")
    uploaded_file = st.file_uploader('Upload whatever you need help with, loser', type='pdf')
    if uploaded_file is not None:
        txt_file = pdf_to_txt(uploaded_file)
        if txt_file is not None:
            with st.expander('Summarised it for you since you have low attention span'): 
                summary = chain.run(input_documents=split("Summary", txt_file), question="Summarise the information file to a reader")
                response = snobby_chain.run(snobby= snobby)
                res = summary + " " + response
                st.write(res)
            with st.expander('MindMap'): 
                mind_map = nx.Graph() 
                main = chain.run(input_documents=split("Central Theme", txt_file), question="What is the central topic here") 
                mind_map.add_node(main, font_color='black', node_size=3000) 
                deets = chain.run(input_documents=split("Thesis", txt_file), question="Identify 5 subtopics and split them by a ,") 
                details = deets.split(',')
                for detail in details:
                    mind_map.add_node(detail, font_color='black', node_size=500)  
                    mind_map.add_edge(main, detail, color='gray', width=1.0)  
                plt.figure(figsize=(10, 8)) 
                pos = nx.spring_layout(mind_map)  
                nx.draw_networkx(mind_map, pos, with_labels=True, node_color='lightblue', font_weight='bold')
                plt.axis('off')
                st.pyplot(plt)
                todo = st.text_input('What does your lazy ass need me to do?')
                if st.button('Submit'):
                    answer = chain.run(input_documents=split("User Query", txt_file), question=todo)
                    st.write(answer)            