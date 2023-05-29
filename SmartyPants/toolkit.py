import PyPDF2
import pdfkit
import os
import fpdf
from typing import List
from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from dataclasses import dataclass
import requests
import string
import io
from googlesearch import search
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import csv

db_path = 'your/path/to/db'

@dataclass
class Question:
    num: int
    question: str
    options: List[str]
    answer: int

def pdf_to_txt(pdf):
    pdf_filename = pdf.name  
    txt_filename = pdf_filename + '.txt'
    txt_path = db_path + txt_filename
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

# Convert prompt result to pdf
def convert_to_pdf(question_list):
    pdf = fpdf.FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for index, question in enumerate(question_list, start=1):
        pdf.multi_cell(0, 10, f"{index}. {question}", align="L")
        pdf.ln(5)
    pdf_bytes = pdf.output(dest='S')
    return pdf_bytes

def thisQuery(query):
    fallback = ""
    result = ''
    try:
        search_result_list = list(search(query))
        page = requests.get(search_result_list[0])
        soup = BeautifulSoup(page.content, features="lxml")
        article_text = ''
        article = soup.findAll('p')
        for element in article:
            article_text += '\n' + ''.join(element.findAll(text = True))
        article_text = article_text.replace('\n', '')
        first_sentence = article_text.split('.')
        first_sentence = first_sentence[0].split('?')[0]
        chars_without_whitespace = first_sentence.translate(
            { ord(c): None for c in string.whitespace }
        )
        if len(chars_without_whitespace) > 0:
            result = first_sentence
        else:
            result = fallback
        return result
    except Exception as e:
        print(f"An error occurred: {e}")

def searchWeb(file):
    df = pd.read_csv(file)
    category_cols = [col for col in df.columns if df[col].dtype == 'object']
    category_info = {}
    for col in category_cols:
        results = thisQuery(f'{col} finance')
        if results:
            category_info[col] = results
    return category_info

def makeLineGraph(file):
    df = pd.read_csv(file)
    category_cols = [col for col in df.columns if df[col].dtype == 'object']
    df_categories = df[category_cols].astype(str)
    plt.figure(figsize=(10,6))
    for col in df_categories.columns:
        plt.plot(df_categories[col], label=col)
    plt.legend()
    plt.title('Category Line Graph')
    plt.xlabel('X-axis label')
    plt.ylabel('Y-axis label')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    return buffer.getvalue()

def excel_to_txt(excel_file, db_path):
    excel_filename = os.path.splitext(excel_file)[0]
    txt_filename = excel_filename + '.txt'
    excel_path = os.path.join(db_path, excel_file)
    txt_path = os.path.join(db_path, txt_filename)
    df = pd.read_excel(excel_path)
    values = df.values.tolist()
    text = '\n'.join([str(row) for row in values])
    with open(txt_path, 'w') as f:
        f.write(text)
    loader = TextLoader(txt_path)
    documents = loader.load()
    return documents

def csv_to_txt(csv_file, db_path):
    csv_filename = os.path.splitext(csv_file.name)[0]
    txt_filename = csv_filename + '.txt'
    csv_path = os.path.join(db_path, csv_file.name)
    txt_path = os.path.join(db_path, txt_filename) 
    with open(csv_path, 'wb') as f:
        f.write(csv_file.read())
    with open(csv_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        with open(txt_path, 'w') as txtfile:
            for row in csvreader:
                txtfile.write('\t'.join(row) + '\n')
    loader = TextLoader(txt_path)
    documents = loader.load()
    return documents
