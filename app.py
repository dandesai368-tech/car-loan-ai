import streamlit as st
import PyPDF2
import openai

# Set API Key
openai.api_key = "YOUR_API_KEY"

# Function to extract text from PDF
def extract_text(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to analyze contract
def analyze_contract(text):
    prompt = f"""
    Analyze this car lease/loan contract and provide:
    1. Summary
    2. Key terms (interest rate, EMI, tenure)
    3. Risky clauses
    4. Negotiation tips
    
    Contract:
    {text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['choices'][0]['message']['content']

# Streamlit UI
st.set_page_config(page_title="Car Contract AI", layout="wide")

st.title("🚗 Car Lease / Loan Contract AI Assistant")

st.write("Upload your contract and get AI insights")

uploaded_file = st.file_uploader("Upload Contract (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Reading document..."):
        text = extract_text(uploaded_file)

    st.subheader("📄 Extracted Text")
    st.text_area("", text, height=200)

    if st.button("Analyze Contract"):
        with st.spinner("Analyzing..."):
            result = analyze_contract(text)

        st.subheader("📊 AI Analysis")
        st.write(result)
