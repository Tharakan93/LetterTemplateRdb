import streamlit as st
import pdfplumber
import google.generativeai as genai
from docx import Document
import io

# API Setup
genai.configure(api_key="AIzaSyDTiyzoeH2_mV6dMY9x_NXwCu9s9SVrdqM")
model = genai.GenerativeModel('gemini-pro')

st.title("📄 PDF to Sinhala Letter Generator")

uploaded_file = st.file_uploader("ඔබේ CRIB PDF එක මෙතැනට Upload කරන්න", type="pdf")

if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:
        raw_text = ""
        for page in pdf.pages:
            raw_text += page.extract_text()

    if st.button("ලිපිය සකස් කරන්න"):
        # AI එකට දත්ත ලබා ගැනීමට දෙන උපදෙස් (Prompt)
        prompt = f"""
        Extract the following from the text: Customer Name, Address, Total Granted Amount, Interest Rate (if any), and Guarantor Details.
        Then, write a formal Sinhala letter using this info. 
        Important: Convert the 'Amount' into Sinhala words (e.g., 120,000 as එක්ලක්ෂ විසිදහසක්).
        Text: {raw_text}
        """
        
        response = model.generate_content(prompt)
        letter_content = response.text
        
        st.subheader("සකස් කළ ලිපිය:")
        st.write(letter_content)

        # Word Document එකක් ලෙස සෑදීම
        doc = Document()
        doc.add_paragraph(letter_content)
        bio = io.BytesIO()
        doc.save(bio)
        
        st.download_button(
            label="Word Document එක බාගත කරගන්න (Download)",
            data=bio.getvalue(),
            file_name="Sinhala_Letter.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )