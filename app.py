import streamlit as st
import PyPDF2

# Page config
st.set_page_config(page_title="Car Loan AI Assistant", layout="wide")

# ✅ PROFESSIONAL WHITE UI + BIGGER TEXT
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #ffffff;
}

/* Global text */
html, body, [class*="css"] {
    color: #000000 !important;
    font-size: 18px !important;
}

/* Title */
h1 {
    color: #1F4E79 !important;
    text-align: center;
    font-size: 42px !important;
}

/* Sub headings */
h2, h3 {
    color: #2E86C1 !important;
    font-size: 26px !important;
}

/* Buttons */
.stButton>button {
    background-color: #2E86C1;
    color: white;
    border-radius: 10px;
    height: 3em;
    font-size: 18px;
    width: 100%;
}

/* Card design */
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #F8F9FA;
    margin-bottom: 12px;
    font-size: 18px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🚗 Car Loan Contract AI Assistant")
st.write("📊 Upload your contract and get smart AI insights, risk analysis & recommendations")

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
            suggestions.append("Request flexible payment terms.")
        elif "Hidden" in r:
            suggestions.append("Ask full breakdown of charges.")
        elif "Termination" in r:
            suggestions.append("Review exit conditions carefully.")
    return suggestions

# Summary
def generate_summary(text):
    sentences = text.split(".")
    return ". ".join(sentences[:4]) if len(sentences) > 4 else text

# Keyword count (NEW FEATURE)
def keyword_stats(text):
    keywords = ["penalty", "interest", "charges", "fee"]
    counts = {k: text.count(k) for k in keywords}
    return counts

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
        stats = keyword_stats(text)

        st.divider()

        # 📄 Summary
        with st.expander("📄 Contract Summary"):
            st.write(summary)

        # 📊 Dashboard
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### ⚠️ Risks")
            if risks:
                for r in risks:
                    st.markdown(f"<div class='card'>{r}</div>", unsafe_allow_html=True)
            else:
                st.success("No major risks")

        with col2:
            st.markdown("### 📊 Risk Score")
            st.progress(score / 100)
            st.write(f"**{score}% Risk Level**")

        with col3:
            st.markdown("### 📈 Keyword Stats")
            for k, v in stats.items():
                st.write(f"{k.capitalize()} : {v}")

        st.divider()

        # 💡 Suggestions
        st.markdown("### 💡 Recommendations")
        if suggestions:
            for s in suggestions:
                st.markdown(f"<div class='card'>👉 {s}</div>", unsafe_allow_html=True)
        else:
            st.write("No suggestions needed")

        st.divider()

        # 📌 Final Advice
        st.markdown("### 📌 Final Advice")
        if score > 60:
            st.error("⚠️ High risk contract! Please review carefully.")
        elif score > 30:
            st.warning("Moderate risk. Negotiation recommended.")
        else:
            st.success("Low risk contract 👍")

        st.divider()

        # 📥 Download report (PRO FEATURE)
        report = f"""
CAR LOAN CONTRACT ANALYSIS REPORT

Risk Score: {score}%

Risks:
{', '.join(risks)}

Suggestions:
{', '.join(suggestions)}
"""
        st.download_button("📥 Download Full Report", report, file_name="report.txt")
