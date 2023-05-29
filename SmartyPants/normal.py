import streamlit as st
from langchain import LLMChain, PromptTemplate

def normal(llm):
    query = st.text_input('Ask me anything')
    if query:
        template = PromptTemplate(
            input_variables = ['query'],
            template= 'answer my {query}'
        )
        chain = LLMChain(llm = llm, prompt=template)
        response = chain.run(query= query)
        st.write(response)