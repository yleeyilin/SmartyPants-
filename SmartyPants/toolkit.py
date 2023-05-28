import PyPDF2
import pdfkit
import os
import subprocess
from typing import List
from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from typing import List
from dataclasses import dataclass

@dataclass
class Question:
    num: int
    question: str
    options: List[str]
    answer: int

db_path = '/Users/leeyilin/LifeHack-2023/SmartyPants/db'

# Convert pdf file to txt file for easier processing
def pdf_to_txt(pdf):
    pdf_filename = pdf.name  
    txt_filename = pdf_filename + '.txt'
    txt_path = '/Users/leeyilin/LifeHack-2023/SmartyPants/db/' + txt_filename
    with open(os.path.join(db_path, pdf_filename), 'wb') as pdf_file:
        pdf_file.write(pdf.read())
    with open(os.path.join(db_path, pdf_filename), 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)
    loader = TextLoader(txt_path)
    documents = loader.load()
    return documents

# Prevent exceeding the token limit of OpenAI API 
def split(query, documents):
    embeddings = OpenAIEmbeddings()
    text_splitter = CharacterTextSplitter(        
        separator="\n",
        chunk_size=1000,
        chunk_overlap=0,
    )
    splitDocs = text_splitter.split_documents(documents)
    db = FAISS.from_documents(splitDocs, embeddings)
    return db.similarity_search(query)

# Convert list of question to pdf 
def generate_pdf(html_content, output_file):
    try:
        pdfkit.from_string(html_content, output_file)
        return True
    except Exception as e:
        print(f"Error occurred during PDF generation: {str(e)}")
        return False

def prompt(topics, num):
    return (
        f"Create an exam of multiple choice questions with {num} "
        f"questions and 1 possible and correct answer in each question. "
        f"Put the correct answer in bold (surrounded by **) in its original spot. "
        f"The exam should be about {topics}. Only generate the questions and "
        f"answers, not the exam itself."
    )
