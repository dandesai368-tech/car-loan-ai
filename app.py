import streamlit as st
import PyPDF2

# Page settings
st.set_page_config(page_title="Car Loan AI Assistant", layout="wide")

# Custom CSS for UI
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
h1 {
    color: #00FFAA;
    text-align: center;
}
.stButton>button {
    background-color: #00FFAA;
    color: black;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🚗 Car Loan Contract AI Assistant")

st.write("Upload your loan agreement and get smart analysis")

# File upload
uploaded_file = st.file_uploader("📄 Upload PDF", type=["pdf"])

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
        "Penalty Charges": ["penalty", "fine"],
        "High Interest": ["interest", "interest rate"],
        "Late Payment Fee": ["late fee", "delay charge"],
        "Hidden Charges": ["extra charges", "processing fee"],
        "Termination Clause": ["termination", "cancel"]
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
    return len(risks) * 20  # simple logic

# Suggestions
def generate_suggestions(risks):
    suggestions = []

    for r in risks:
        if r == "Penalty Charges":
            suggestions.append("Negotiate lower penalty charges.")
        elif r == "High Interest":
            suggestions.append("Ask for reduced interest rate.")
        elif r == "Late Payment Fee":
            suggestions.append("Request flexible payment terms.")
        elif r == "Hidden Charges":
            suggestions.append("Ask for full cost breakdown.")
        elif r == "Termination Clause":
            suggestions.append("Check early exit conditions.")

    return suggestions

# Main logic
if uploaded_file:
    st.success("✅ File uploaded successfully!")

    if st.button("🔍 Analyze Contract"):
        text = extract_text(uploaded_file)

        risks = analyze_contract(text)
        score = calculate_score(risks)
        suggestions = generate_suggestions(risks)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("⚠️ Risks Detected")
            if risks:
                for r in risks:
                    st.write("•", r)
            else:
                st.write("No major risks found")

        with col2:
            st.subheader("📊 Risk Score")
            st.progress(score / 100)
            st.write(f"Risk Level: {score}%")

        st.subheader("💡 Suggestions")
        if suggestions:
            for s in suggestions:
                st.write("•", s)
        else:
            st.write("No suggestions needed")
           
