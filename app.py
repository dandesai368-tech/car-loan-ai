import streamlit as st
import PyPDF2

st.title("Car Loan Contract AI Assistant")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

def extract_text(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

def analyze(text):
    risks = []
    words = ["penalty", "interest", "late fee", "charges"]
    for w in words:
        if w in text:
            risks.append(w)
    return risks

if uploaded_file:
    st.write("File uploaded")

    if st.button("Analyze"):
        text = extract_text(uploaded_file)
        risks = analyze(text)

        st.subheader("Risks Found")
        if risks:
            for r in risks:
                st.write(r)
        else:
            st.write("No risks found")
