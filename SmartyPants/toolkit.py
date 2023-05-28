import PyPDF2
import os
from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings

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
