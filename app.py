import streamlit as st
import PyPDF2

# Page config
st.set_page_config(page_title="Car Loan AI Assistant", layout="wide")

# Custom CSS (WHITE UI)
st.markdown("""
<style>
body {
    background-color: #ffffff;
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
</style>
""", unsafe_allow_html=True)

# Title
st.title("🚗 Car Loan Contract AI Assistant")
st.write("Analyze your loan agreement and get smart insights 📊")

# Upload file
uploaded_file = st.file_uploader("📄 Upload your Contract (PDF)", type=["pdf"])

# Extract text
def extract_text(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# Analyze risks
def analyze_contract(text):
    risk_dict = {
        "⚠️ Penalty Charges": ["penalty", "fine"],
        "💰 High Interest": ["interest", "interest rate"],
        "⏰ Late Payment Fee": ["late fee", "delay charge"],
        "📑 Hidden Charges": ["extra charges", "processing fee"],
        "❌ Termination Clause": ["termination", "cancel"]
    }

    found_risks = []

    for category, words in risk_dict.items():
        for word in words:
            if word in text:
                found_risks.append(category)
                break

    return list(set(found_risks))

# Risk score
def calculate_score(risks):
    return len(risks) * 20

# Suggestions
def generate_suggestions(risks):
    suggestions = []

    for r in risks:
        if "Penalty" in r:
            suggestions.append("👉 Try to reduce penalty charges.")
        elif "Interest" in r:
            suggestions.append("👉 Negotiate for lower interest rate.")
        elif "Late" in r:
            suggestions.append("👉 Request flexible payment options.")
        elif "Hidden" in r:
            suggestions.append("👉 Ask for full cost breakdown.")
        elif "Termination" in r:
            suggestions.append("👉 Check early exit conditions.")

    return suggestions

# Summary
def generate_summary(text):
    sentences = text.split(".")
    return ". ".join(sentences[:3])

# Main logic
if uploaded_file:
    st.success("✅ File uploaded successfully!")

    if st.button("🔍 Analyze Contract"):
        text = extract_text(uploaded_file)

        risks = analyze_contract(text)
        score = calculate_score(risks)
        suggestions = generate_suggestions(risks)
        summary = generate_summary(text)

        st.divider()

        # Summary Section
        with st.expander("📄 Contract Summary"):
            st.write(summary)

        # Layout columns
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("⚠️ Risks Detected")
            if risks:
                for r in risks:
                    st.write(r)
            else:
                st.write("✅ No major risks found")

        with col2:
            st.subheader("📊 Risk Score")
            st.progress(score / 100)
            st.write(f"Risk Level: {score}%")

        st.divider()

        # Suggestions
        st.subheader("💡 Suggestions")
        if suggestions:
            for s in suggestions:
                st.write(s)
        else:
            st.write("👍 No suggestions needed")

        st.divider()

        # Extra Feature
        st.subheader("📌 Final Advice")
        if score > 60:
            st.error("High risk contract! Review carefully ⚠️")
        elif score > 30:
            st.warning("Moderate risk. Consider negotiation.")
        else:
            st.success("Low risk contract 👍")
