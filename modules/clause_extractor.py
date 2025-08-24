import os
from docx import Document
import PyPDF2

def extract_clauses(input_data, is_file=True):
    text = ""
    if is_file:
        ext = os.path.splitext(input_data)[1].lower()
        if ext == ".pdf":
            with open(input_data, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        elif ext == ".docx":
            doc = Document(input_data)
            for para in doc.paragraphs:
                if para.text.strip():
                    text += para.text + "\n"
    else:
        text = input_data

    clauses = [line.strip() for line in text.split("\n") if line.strip()]
    return clauses
    # return text.strip()