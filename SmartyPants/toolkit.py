import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import firestore
import PyPDF2

cred = credentials.Certificate("/Users/leeyilin/LifeHack-2023/SmartyPants/firebaseKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Uploads pdf file directly
def upload_pdf_to_firestore(file):
    pdf_bytes = file.read()
    doc_ref = db.collection("pdfs").document()
    doc_ref.set({
        "pdf_bytes": pdf_bytes
    })

# Parse in pdf and returns txt 
def pdf_to_txt(pdf_file):
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    txt_content = ""
    for page_num in range(pdf_reader.numPages):
        currPage = pdf_reader.getPage(page_num)
        page_content = currPage.extractText()
        txt_content += page_content
    doc_ref = db.collection("pdfs").document()
    doc_ref.set({
        "pdf_text": txt_content
    })
    return txt_content