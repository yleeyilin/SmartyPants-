import streamlit as st
from toolkit import pdf_to_txt, split
from langchain.chains.question_answering import load_qa_chain

# Prompt Template

first_prompt = """ You are an esteemed teacher and a question setter. Given the file, for each question, identify the topic and type of question. 
The type of questions are as follows:
1. Multiple Choice Questions (MCQs):
   a. Include MCQs with options.
   b. Ensure a balanced distribution of difficulty levels.

2. Short Answer Questions:
   a. Provide short answer questions covering different topics.
   b. Each question should require a concise answer within {word limit} words.

3. Essay Questions:
   a. Include essay questions that require in-depth explanations.
   b. Each question should cover a specific aspect of the course material.

4. Problem-solving Questions:
   a. Design problem-solving questions that test application skills.
   b. Ensure a mix of theoretical and practical scenarios.

The topics are the central theme of the question. 

Present the breakdown in the following manner: [(Question 1 topic, Question 1 type), (Question 2 topic, Question 2 type),...]
"""

def exampapers(llm):
    chain = load_qa_chain(llm, chain_type="stuff")
    uploaded_file = st.file_uploader("Upload Exam PDF file", type="pdf")
    if uploaded_file is not None:
        