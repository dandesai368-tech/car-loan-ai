import streamlit as st
import PyPDF2

# Page config
st.set_page_config(page_title="Car Loan AI Assistant", layout="wide")

# ✅ STRONG UI FIX (BIG TEXT + VISIBLE HEADINGS)
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #ffffff;
}

/* Force all text visible */
html, body, [class*="css"] {
    color: #111111 !important;
}

/* Title */
h1 {
    font-size: 48px !important;
    color: #0B3C5D !important;
    text-align: center;
    font-weight: bold;
}

/* Section headings */
h2 {
    font-size: 30px !important;
    color: #1F4E79 !important;
    font-weight: bold;
}
h3 {
    font-size: 24px !important;
    color: #2E86C1 !important;
    font-weight: bold;
}

/* Cards */
.card {
    background-color: #F4F6F7;
    padding: 20px;
    border-radius: 12px;
    margin: 10px 0;
    font-size: 18px;
    color: black;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}

/* Buttons */
.stButton>button {
    background-color: #2E86C1;
    color: white;
    font-size: 18px;
    border-radius: 10px;
    height: 3em;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🚗 Car Loan Contract AI Dashboard")
st.write("Analyze contracts with AI insights, risk scores, and smart recommendations")

# Upload
uploaded_file = st.file_uploader("📄 Upload Contract PDF", type=["pdf"])

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

# Analyze risks
def analyze_contract(text):
    risk_dict = {
        "Penalty Charges": ["penalty", "fine"],
        "High Interest": ["interest"],
        "Late Fee": ["late fee", "delay"],
        "Hidden Charges": ["charges", "processing fee"],
        "Termination Clause": ["termination"]
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
        suggestions.append(f"Improve terms related to {r}")
    return suggestions

# Summary
def generate_summary(text):
    sentences = text.split(".")
    return ". ".join(sentences[:4])

# Keyword stats
def keyword_stats(text):
    keywords = ["penalty", "interest", "charges", "fee"]
    return {k: text.count(k) for k in keywords}

# MAIN
if uploaded_file:

    text = extract_text(uploaded_file)

    if len(text) == 0:
        st.error("❌ Cannot read PDF. Try another file.")
    else:
        risks = analyze_contract(text)
        score = calculate_score(risks)
        suggestions = generate_suggestions(risks)
        summary = generate_summary(text)
        stats = keyword_stats(text)

        # 🔥 DASHBOARD METRICS
        st.subheader("📊 Dashboard Overview")
        col1, col2, col3 = st.columns(3)

        col1.metric("Risk Score", f"{score}%")
        col2.metric("Risks Found", len(risks))
        col3.metric("Keywords Found", sum(stats.values()))

        st.divider()

        # 📄 Summary
        st.subheader("📄 Contract Summary")
        st.markdown(f"<div class='card'>{summary}</div>", unsafe_allow_html=True)

        # ⚠️ Risks
        st.subheader("⚠️ Risks Detected")
        if risks:
            for r in risks:
                st.markdown(f"<div class='card'>{r}</div>", unsafe_allow_html=True)
        else:
            st.success("No major risks found")

        # 📈 Keyword stats
        st.subheader("📈 Keyword Analysis")
        st.bar_chart(stats)

        st.divider()

        # 💡 Suggestions
        st.subheader("💡 Recommendations")
        for s in suggestions:
            st.markdown(f"<div class='card'>👉 {s}</div>", unsafe_allow_html=True)

        # 📌 Final Advice
        st.subheader("📌 Final Advice")
        if score > 60:
            st.error("High Risk Contract!")
        elif score > 30:
            st.warning("Moderate Risk - Negotiate Terms")
        else:
            st.success("Low Risk - Safe Contract")

        # 📥 Download
        report = f"""
Risk Score: {score}%
Risks: {risks}
Suggestions: {suggestions}
"""
        st.download_button("📥 Download Report", report)
