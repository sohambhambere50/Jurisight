import os
import fitz  # PyMuPDF
import docx

def extract_text_from_pdf(file_path):
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def extract_text_from_docx(file_path):
    text = ""
    doc = docx.Document(file_path)
    for para in doc.paragraphs:
        if para.text.strip():
            text += para.text + "\n"
    return text

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".docx", ".doc"]:
        return extract_text_from_docx(file_path)
    else:
        return ""
