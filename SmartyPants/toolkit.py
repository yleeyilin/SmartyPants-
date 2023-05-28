import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import firestore

cred = credentials.Certificate("/Users/leeyilin/LifeHack-2023/SmartyPants/firebaseKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def upload_pdf_to_firestore(file):
    pdf_bytes = file.read()
    doc_ref = db.collection("pdfs").document()
    doc_ref.set({
        "pdf_bytes": pdf_bytes
    })