import streamlit as st
import PyPDF2

# Page config
st.set_page_config(page_title="Car Loan AI Assistant", layout="wide")

# ✅ FIXED WHITE UI
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #ffffff;
}
[data-testid="stSidebar"] {
    background-color: #f5f5f5;
}
h1 {
    color: #2E86C1;
    text-align: center;
}
h2, h3 {
    color: #1B4F72;
}
.stButton>button {
    background-color: #2E86C1;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
}
.card {
    padding: 15px;
    border-radius: 10px;
    background-color: #f8f9fa;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

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
        "⚠️ Penalty Charges": ["penalty", "fine"],
        "💰 High Interest": ["interest", "interest rate"],
        "⏰ Late Payment Fee": ["late fee", "delay"],
        "📑 Hidden Charges": ["charges", "processing fee"],
        "❌ Termination Clause": ["termination", "cancel"]
    }

    risks = []
    for category, words in risk_dict.items():
        for word in words:
            if word in text:
                risks.append(category)
                break

    return list(set(risks))

# Risk score
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
            suggestions.append("Check all extra charges.")
        elif "Termination" in r:
            suggestions.append("Review exit conditions.")
    return suggestions

# Summary
def generate_summary(text):
    sentences = text.split(".")
    return ". ".join(sentences[:3]) if len(sentences) > 3 else text

# Highlight keywords
def highlight_keywords(text):
    keywords = ["penalty", "interest", "charges", "fee"]
    for word in keywords:
        text = text.replace(word, f"**{word.upper()}**")
    return text

# MAIN
if uploaded_file:

    st.success("✅ File uploaded successfully!")

    text = extract_text(uploaded_file)

    if len(text) == 0:
        st.error("❌ Cannot read this PDF. Try another file.")
    else:
        risks = analyze_contract(text)
        score = calculate_score(risks)
        suggestions = generate_suggestions(risks)
        summary = generate_summary(text)

        st.divider()

        # 📄 Summary
        with st.expander("📄 Contract Summary"):
            st.write(summary)

        # 📊 Dashboard
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ⚠️ Risks Detected")
            if risks:
                for r in risks:
                    st.markdown(f"<div class='card'>{r}</div>", unsafe_allow_html=True)
            else:
                st.success("No major risks found")

        with col2:
            st.markdown("### 📊 Risk Score")
            st.progress(score / 100)
            st.write(f"Risk Level: {score}%")

        st.divider()

        # 💡 Suggestions
        st.markdown("### 💡 Suggestions")
        if suggestions:
            for s in suggestions:
                st.markdown(f"<div class='card'>👉 {s}</div>", unsafe_allow_html=True)
        else:
            st.write("No suggestions needed")

        st.divider()

        # 🔍 Highlighted text
        with st.expander("🔍 Highlighted Contract Text"):
            st.write(highlight_keywords(text[:1500]))

        st.divider()

        # 📌 Final Advice
        st.markdown("### 📌 Final Advice")
        if score > 60:
            st.error("⚠️ High risk contract! Review carefully.")
        elif score > 30:
            st.warning("Moderate risk. Try negotiation.")
        else:
            st.success("Low risk contract 👍")

        st.divider()

        # 📥 Download Report
        report = f"""
Contract Analysis Report

Risk Score: {score}%

Risks:
{', '.join(risks)}

Suggestions:
{', '.join(suggestions)}
"""
        st.download_button("📥 Download Report", report, file_name="report.txt")
