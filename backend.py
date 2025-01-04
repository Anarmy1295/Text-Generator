# Import necessary libraries
import os
import sqlite3
import streamlit as st

# Check and handle missing dependencies
try:
    import pdfplumber
except ImportError:
    os.system('pip install pdfplumber')
    import pdfplumber

try:
    from docx import Document
except ImportError:
    os.system('pip install python-docx')
    from docx import Document

try:
    import pandas as pd
except ImportError:
    os.system('pip install pandas')
    import pandas as pd

# Function to check SQLite3 installation
def check_sqlite():
    try:
        st.write(f"SQLite version: {sqlite3.sqlite_version}")
    except Exception as e:
        st.error(f"SQLite3 error: {str(e)}. Ensure your Python installation includes the standard library.")

# Streamlit app code
def main():
    st.title("Document Analysis with PDF and Word")
    st.write("This application demonstrates the use of SQLite3, pdfplumber, and Streamlit.")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload a PDF or Word Document", type=["pdf", "docx"])
    
    if uploaded_file:
        file_name, file_extension = os.path.splitext(uploaded_file.name)
        
        if file_extension == ".pdf":
            st.write("Processing PDF file...")
            try:
                with pdfplumber.open(uploaded_file) as pdf:
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_text()
                    st.text_area("Extracted Text", value=text, height=300)
            except Exception as e:
                st.error(f"Error processing PDF: {str(e)}")
        
        elif file_extension == ".docx":
            st.write("Processing Word file...")
            try:
                doc = Document(uploaded_file)
                text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                st.text_area("Extracted Text", value=text, height=300)
            except Exception as e:
                st.error(f"Error processing Word document: {str(e)}")
        else:
            st.warning("Unsupported file type.")
    
    # SQLite3 check
    st.header("SQLite3 Version Check")
    check_sqlite()

if __name__ == "__main__":
    main()
