import streamlit as st
import pandas as pd
import numpy as np
import pytesseract
from PIL import Image
import io
import re

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Car Loan AI Assistant",
    layout="wide"
)

# -------------------------------
# CUSTOM CSS (WHITE UI + BIG TEXT)
# -------------------------------
st.markdown("""
    <style>
    body {
        background-color: white;
    }
    .main {
        background-color: white;
    }
    h1, h2, h3 {
        color: #1a1a1a;
        font-size: 28px;
    }
    p, div {
        color: #333333;
        font-size: 18px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# TITLE
# -------------------------------
st.title("🚗 Car Lease / Loan Contract AI Assistant")
st.write("Analyze contracts, detect risks, and get negotiation suggestions instantly.")

# -------------------------------
# SIDEBAR DASHBOARD
# -------------------------------
st.sidebar.header("📊 Dashboard")

risk_score = st.sidebar.metric("Risk Score", "Medium")
total_cost = st.sidebar.metric("Total Cost", "₹5,20,000")
savings = st.sidebar.metric("Savings Potential", "₹30,000")

# -------------------------------
# FILE UPLOAD
# -------------------------------
uploaded_file = st.file_uploader("📄 Upload Contract (PDF/Image)", type=["png", "jpg", "jpeg"])

extracted_text = ""

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Contract", use_column_width=True)

    # OCR
    extracted_text = pytesseract.image_to_string(image)

    st.subheader("📃 Extracted Text")
    st.write(extracted_text)

# -------------------------------
# TEXT ANALYSIS FUNCTION
# -------------------------------
def analyze_contract(text):
    risks = []
    suggestions = []

    # Interest detection
    interest = re.findall(r"\d+%", text)
    if interest:
        rate = int(interest[0].replace("%", ""))
        if rate > 10:
            risks.append("High Interest Rate Detected")
            suggestions.append("Negotiate for lower interest rate")

    # Hidden fees
    if "processing fee" in text.lower():
        risks.append("Processing Fee Found")
        suggestions.append("Request waiver of processing fee")

    if "penalty" in text.lower():
        risks.append("Penalty Clause Present")
        suggestions.append("Negotiate lower penalty charges")

    if not risks:
        risks.append("No major risks detected")
        suggestions.append("Contract looks fair")

    return risks, suggestions

# -------------------------------
# ANALYZE BUTTON
# -------------------------------
if st.button("🔍 Analyze Contract"):
    if extracted_text:
        risks, suggestions = analyze_contract(extracted_text)

        st.subheader("⚠ Risk Analysis")
        for r in risks:
            st.error(r)

        st.subheader("💡 Negotiation Suggestions")
        for s in suggestions:
            st.success(s)

# -------------------------------
# SIMPLE EMI CALCULATION
# -------------------------------
st.subheader("📈 Loan Calculator")

amount = st.number_input("Loan Amount", value=500000)
rate = st.number_input("Interest Rate (%)", value=10)
time = st.number_input("Years", value=5)

if st.button("Calculate EMI"):
    emi = (amount * rate * (1 + rate) ** time) / ((1 + rate) ** time - 1)
    st.success(f"Estimated EMI: ₹{int(emi)}")

# -------------------------------
# CHATBOT
# -------------------------------
st.subheader("💬 AI Assistant")

user_query = st.text_input("Ask about your contract")

if user_query:
    if "interest" in user_query.lower():
        st.write("Interest rate affects total repayment. Lower is better.")
    elif "penalty" in user_query.lower():
        st.write("Penalty clauses may increase cost. Try negotiating.")
    else:
        st.write("This clause looks standard. Please verify with bank.")

# -------------------------------
# REPORT DOWNLOAD
# -------------------------------
st.subheader("📥 Download Report")

report = "Contract Analysis Report\n\nRisks and Suggestions Generated."

st.download_button(
    label="Download Report",
    data=report,
    file_name="report.txt"
)
 
