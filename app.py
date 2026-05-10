import streamlit as st
import pdfplumber
import re
import spacy

nlp = spacy.load("en_core_web_sm")

st.title("📄 AI Resume Parser")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_email(text):
    emails = re.findall(r'\S+@\S+', text)
    return emails[0] if emails else "Not Found"

def extract_phone(text):
    phones = re.findall(r'\b\d{10}\b', text)
    return phones[0] if phones else "Not Found"

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return text.split("\n")[0]

def extract_skills(text):
    with open("skills.txt") as f:
        skills_list = f.read().splitlines()
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in skills_list:
        if skill in text_lower:
            found_skills.append(skill)
    
    return found_skills

if uploaded_file:
    text = extract_text(uploaded_file)

    st.subheader("📊 Extracted Information")

    st.write("👤 Name:", extract_name(text))
    st.write("📧 Email:", extract_email(text))
    st.write("📱 Phone:", extract_phone(text))

    skills = extract_skills(text)
    st.write("💡 Skills:", skills if skills else "Not Found")

    st.subheader("📄 Resume Preview")
    st.text(text[:1000])