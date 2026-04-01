import streamlit as st
import PyPDF2

# Page config
st.set_page_config(page_title="Car Loan AI Assistant", layout="wide")

# Title
st.title("🚗 Car Loan Contract AI Assistant")
st.write("Analyze your contract and get smart insights 📊")

# Upload
uploaded_file = st.file_uploader("📄 Upload Contract (PDF)", type=["pdf"])

# Extract text
def extract_text(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            if page.extract_text():
                text += page.extract_text()
        return text.lower()
    except:
        return ""

# Risk detection
def analyze_contract(text):
    risk_dict = {
        "Penalty Charges": ["penalty", "fine"],
        "High Interest": ["interest", "interest rate"],
        "Late Payment Fee": ["late fee", "delay"],
        "Hidden Charges": ["charges", "processing fee"],
        "Termination Clause": ["termination", "cancel"]
    }

    risks = []
    for category, words in risk_dict.items():
        for word in words:
            if word in text:
                risks.append(category)
                break

    return list(set(risks))

# Score
def calculate_score(risks):
    return len(risks) * 20

# Suggestions
def generate_suggestions(risks):
    suggestions = []
    for r in risks:
        if "Penalty" in r:
            suggestions.append("Reduce penalty charges.")
        elif "Interest" in r:
            suggestions.append("Negotiate lower interest rate.")
        elif "Late" in r:
            suggestions.append("Ask flexible payment terms.")
        elif "Hidden" in r:
            suggestions.append("Check extra charges carefully.")
        elif "Termination" in r:
            suggestions.append("Review exit conditions.")
    return suggestions

# Summary
def generate_summary(text):
    sentences = text.split(".")
    return ". ".join(sentences[:3]) if len(sentences) > 3 else text

# MAIN
if uploaded_file:

    st.success("File uploaded successfully!")

    text = extract_text(uploaded_file)

    if len(text) == 0:
        st.error("Cannot read this PDF. Try another file.")
    else:
        risks = analyze_contract(text)
        score = calculate_score(risks)
        suggestions = generate_suggestions(risks)
        summary = generate_summary(text)

        st.divider()

        # Summary
        with st.expander("Contract Summary"):
            st.write(summary)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Risks Detected")
            if risks:
                for r in risks:
                    st.write("•", r)
            else:
                st.success("No major risks found")

        with col2:
            st.subheader("Risk Score")
            st.progress(score / 100)
            st.write(f"{score}% Risk")

        st.divider()

        st.subheader("Suggestions")
        if suggestions:
            for s in suggestions:
                st.write("👉", s)
        else:
            st.write("No suggestions needed")

        st.divider()

        st.subheader("Final Advice")
        if score > 60:
            st.error("High risk contract")
        elif score > 30:
            st.warning("Moderate risk")
        else:
            st.success("Low risk contract")

        st.divider()

        # Download report
        report = f"""
Contract Analysis Report

Risk Score: {score}%

Risks:
{', '.join(risks)}

Suggestions:
{', '.join(suggestions)}
"""
        st.download_button("Download Report", report, file_name="report.txt")
# Highlight keywords
