import streamlit as st
import PyPDF2

# Page config
st.set_page_config(page_title="Car Loan AI Assistant", layout="wide")

# ✅ STRONG CSS FIX (Headings + Text visible)
st.markdown("""
<style>
/* White background */
[data-testid="stAppViewContainer"] {
    background-color: #ffffff !important;
}

/* Force all text visible */
* {
    color: #000000 !important;
    font-size: 18px !important;
}

/* Title */
h1 {
    color: #1F4E79 !important;
    font-size: 42px !important;
    text-align: center;
}

/* Headings */
h2, h3 {
    color: #2E86C1 !important;
    font-size: 26px !important;
}

/* Buttons */
.stButton>button {
    background-color: #2E86C1 !important;
    color: white !important;
    border-radius: 10px;
    font-size: 18px;
}

/* Cards */
.card {
    background-color: #F8F9FA;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🚗 Car Loan Contract AI Assistant")
st.write("📊 Upload contract → Get risk analysis + smart suggestions")

# Upload
uploaded_file = st.file_uploader("📄 Upload PDF", type=["pdf"])

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

# Analyze
def analyze(text):
    risks = {
        "Penalty Charges": ["penalty"],
        "High Interest": ["interest"],
        "Late Fee": ["late fee"],
        "Hidden Charges": ["charges"],
        "Termination Clause": ["termination"]
    }
    found = []
    for k, v in risks.items():
        for word in v:
            if word in text:
                found.append(k)
                break
    return list(set(found))

# Score
def score_calc(risks):
    return len(risks) * 20

# Suggestions
def suggestions_func(risks):
    return [f"Improve {r}" for r in risks]

# MAIN
if uploaded_file:

    st.success("File uploaded successfully")

    text = extract_text(uploaded_file)

    if len(text) == 0:
        st.error("Cannot read this PDF")
    else:
        risks = analyze(text)
        score = score_calc(risks)
        suggestions = suggestions_func(risks)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("⚠️ Risks Detected")
            if risks:
                for r in risks:
                    st.markdown(f"<div class='card'>{r}</div>", unsafe_allow_html=True)
            else:
                st.success("No risks found")

        with col2:
            st.subheader("📊 Risk Score")
            st.progress(score / 100)
            st.write(f"{score}%")

        st.divider()

        st.subheader("💡 Suggestions")
        if suggestions:
            for s in suggestions:
                st.markdown(f"<div class='card'>{s}</div>", unsafe_allow_html=True)
        else:
            st.write("No suggestions")

        st.divider()

        st.subheader("📌 Final Advice")
        if score > 60:
            st.error("High risk contract")
        elif score > 30:
            st.warning("Moderate risk")
        else:
            st.success("Low risk")

        st.divider()

        st.download_button("📥 Download Report", str(risks), file_name="report.txt")
