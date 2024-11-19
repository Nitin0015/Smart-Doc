import fitz  # PyMuPDF
import os
from docx import Document
import pandas as pd 


def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as pdf:
        for page in pdf:
            text += page.get_text()
    return text

def extract_text_from_txt(file):
    """Extract text from a TXT file."""
    return file.read().decode('utf-8')  

def extract_text_from_docx(file):
    """Extract text from a DOCX file."""
    doc = Document(file)
    # Collect paragraphs, stripping excess whitespace
    paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    return "\n".join(paragraphs)

def extract_text_from_excel(file):
    """Extract and format data from an Excel file."""
    try:
        
        df = pd.read_excel(file)
        
        df = df.dropna(how='all').drop_duplicates()

        df = df.apply(pd.to_numeric, errors='ignore')  

        # Format the data into the desired row-column structure
        formatted_text = ""
        for i, row in df.iterrows():
            formatted_text += f"Row {i + 1}:\n"
            for col in df.columns:
                formatted_text += f"{col}: {row[col]}\n"
            formatted_text += "\n"  

        return formatted_text.strip()
    except Exception as e:
        raise ValueError(f"Error processing Excel file: {e}")

def extract_text(file, file_type):
    """Extract text based on file type."""
    if file_type == "pdf":
        text = extract_text_from_pdf(file)
    elif file_type == "txt":
        text = extract_text_from_txt(file)
    elif file_type == "docx":
        text = extract_text_from_docx(file)
    elif file_type in ["xls", "xlsx"]: 
        text = extract_text_from_excel(file)
    else:
        raise ValueError("Unsupported file type")
    
    # Ensure extracted text is valid
    if not text or not isinstance(text, str):
        raise ValueError("Failed to extract text from the uploaded document.")
    
    return text

