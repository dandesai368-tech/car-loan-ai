import streamlit as st
import PyPDF2

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Car Contract AI Assistant",
    layout="wide"
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
    <style>
    body {
        background-color: white;
        color: black;
    }
    .title {
        font-size: 40px;
        font-weight: bold;
        color: #2C3E50;
    }
    .subheader {
        font-size: 24px;
        color: #34495E;
    }
    .box {
        padding: 15px;
        border-radius: 10px;
        background-color: #F8F9F9;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ SESSION STATE ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "history" not in st.session_state:
    st.session_state.history = []

# ------------------ LOGIN PAGE ------------------
def login():
    st.markdown('<div class="title">🔐 Login Page</div>', unsafe_allow_html=True)
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login Successful!")
        else:
            st.error("Invalid Credentials")

# ------------------ SIDEBAR ------------------
def sidebar():
    st.sidebar.title("🚗 Navigation")
    page = st.sidebar.radio("Go to", [
        "Dashboard",
        "Upload & Analyze",
        "AI Assistant",
        "Negotiation Helper",
        "History"
    ])

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False

    return page

# ------------------ DASHBOARD ------------------
def dashboard():
    st.markdown('<div class="title">📊 Dashboard</div>', unsafe_allow_html=True)

    st.markdown('<div class="box">Total Contracts Analyzed: {}</div>'.format(len(st.session_state.history)), unsafe_allow_html=True)

    st.markdown('<div class="subheader">Welcome to AI Contract Assistant</div>', unsafe_allow_html=True)

# ------------------ PDF READER ------------------
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# ------------------ ANALYSIS ------------------
def analyze_contract(text):
    risks = []
    if "interest" in text.lower():
        risks.append("⚠ Interest rate clause detected")
    if "penalty" in text.lower():
        risks.append("⚠ Penalty clause detected")

    summary = text[:500]

    return summary, risks

# ------------------ UPLOAD PAGE ------------------
def upload_page():
    st.markdown('<div class="title">📄 Upload Contract</div>', unsafe_allow_html=True)

    file = st.file_uploader("Upload PDF", type=["pdf"])

    if file:
        text = read_pdf(file)
        summary, risks = analyze_contract(text)

        st.markdown('<div class="subheader">Summary</div>', unsafe_allow_html=True)
        st.write(summary)

        st.markdown('<div class="subheader">Risks</div>', unsafe_allow_html=True)
        for r in risks:
            st.warning(r)

        st.session_state.history.append(summary)

# ------------------ AI ASSISTANT ------------------
def ai_assistant():
    st.markdown('<div class="title">🤖 AI Assistant</div>', unsafe_allow_html=True)

    query = st.text_input("Ask about your contract")

    if st.button("Get Answer"):
        st.info("AI Suggestion: Review interest rates and penalty clauses carefully.")

# ------------------ NEGOTIATION ------------------
def negotiation():
    st.markdown('<div class="title">💬 Negotiation Helper</div>', unsafe_allow_html=True)

    issue = st.selectbox("Select Issue", [
        "High Interest Rate",
        "Penalty Charges",
        "Loan Tenure"
    ])

    if st.button("Generate Negotiation Message"):
        st.success(f"Suggested Message: I would like to negotiate the {issue.lower()} for better terms.")

# ------------------ HISTORY ------------------
def history():
    st.markdown('<div class="title">📁 History</div>', unsafe_allow_html=True)

    for i, item in enumerate(st.session_state.history):
        st.markdown(f"<div class='box'>Contract {i+1}: {item[:100]}...</div>", unsafe_allow_html=True)

# ------------------ MAIN ------------------
if not st.session_state.logged_in:
    login()
else:
    page = sidebar()

    if page == "Dashboard":
        dashboard()
    elif page == "Upload & Analyze":
        upload_page()
    elif page == "AI Assistant":
        ai_assistant()
    elif page == "Negotiation Helper":
        negotiation()
    elif page == "History":
        history()
