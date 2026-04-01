import streamlit as st
import PyPDF2

# Page config
st.set_page_config(page_title="Car Loan AI Assistant", layout="wide")

# Custom CSS (WHITE UI)
st.markdown("""
<style>
body {
    background-color: white;
}
h1 {
    color: #2E86C1;
    text-align: center;
}
.stButton>button {
    background-color: #2E86C1;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🚗 Car Loan Contract AI Assistant")
st.markdown("### 📄 Upload your contract and get AI-based analysis")

# Upload file
uploaded_file = st.file_uploader("📂 Upload PDF File", type=["pdf"])

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
    return min(len(risks) * 20, 100)

# Suggestions
def generate_suggestions(risks):
    suggestions = []

    for r in risks:
        if "Penalty" in r:
            suggestions.append("👉 Try to negotiate lower penalty charges.")
        elif "Interest" in r:
            suggestions.append("👉 Ask for a reduced interest rate.")
        elif "Late" in r:
            suggestions.append("👉 Request flexible payment options.")
        elif "Hidden" in r:
            suggestions.append("👉 Ask for a detailed cost breakdown.")
        elif "Termination" in r:
            suggestions.append("👉 Carefully review exit conditions.")

    return suggestions

# Simple summary
def generate_summary(text):
    return text[:500] + "..."

# Main
if uploaded_file:
    st.success("✅ File uploaded successfully!")

    if st.button("🔍 Analyze Contract"):
        text = extract_text(uploaded_file)

        risks = analyze_contract(text)
        score = calculate_score(risks)
        suggestions = generate_suggestions(risks)
        summary = generate_summary(text)

        col1, col2 = st.columns(2)

        # Risks
        with col1:
            st.subheader("⚠️ Detected Risks")
            if risks:
                for r in risks:
                    st.write(r)
            else:
                st.write("✅ No major risks found")

        # Score
        with col2:
            st.subheader("📊 Risk Score")
            st.progress(score / 100)
            st.write(f"### {score}% Risk Level")

        # Suggestions
        st.subheader("💡 Suggestions")
        if suggestions:
            for s in suggestions:
                st.write(s)
        else:
            st.write("👍 No suggestions needed")

        # Summary (Expandable)
        with st.expander("📄 View Contract Summary"):
            st.write(summary)

        # Raw text (Optional)
        with st.expander("📝 View Extracted Text"):
            st.write(text[:1000])
