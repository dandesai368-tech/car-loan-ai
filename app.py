import streamlit as st
import PyPDF2

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Car Contract AI Assistant", layout="wide")

# ------------------ FORCE WHITE BACKGROUND ------------------
st.markdown("""
    <style>
    .stApp {
        background-color: white;
        color: black;
    }
    h1, h2, h3, h4 {
        color: #2C3E50;
    }
    .stButton>button {
        background-color: #2C3E50;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
    }
    .stTextInput>div>div>input {
        background-color: #F4F6F7;
        color: black;
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
    st.title("🔐 Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login Successful!")
            st.rerun()   # ✅ FIX
        else:
            st.error("Invalid Credentials")

# ------------------ SIDEBAR ------------------
def sidebar():
    st.sidebar.title("🚗 Navigation")

    page = st.sidebar.radio("Select Page", [
        "Dashboard",
        "Upload & Analyze",
        "AI Assistant",
        "Negotiation Helper",
        "History"
    ])

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    return page

# ------------------ DASHBOARD ------------------
def dashboard():
    st.title("📊 Dashboard")

    st.metric("Total Contracts Analyzed", len(st.session_state.history))

    st.info("Welcome to Car Contract AI Assistant 🚗")

# ------------------ PDF READER ------------------
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# ------------------ ANALYSIS ------------------
def analyze_contract(text):
    risks = []

    if "interest" in text.lower():
        risks.append("⚠ Interest rate clause detected")
    if "penalty" in text.lower():
        risks.append("⚠ Penalty clause detected")
    if "fine" in text.lower():
        risks.append("⚠ Hidden fine detected")

    summary = text[:500]

    return summary, risks

# ------------------ UPLOAD PAGE ------------------
def upload_page():
    st.title("📄 Upload & Analyze Contract")

    file = st.file_uploader("Upload PDF", type=["pdf"])

    if file:
        text = read_pdf(file)
        summary, risks = analyze_contract(text)

        st.subheader("📌 Contract Summary")
        st.write(summary)

        st.subheader("⚠ Risk Analysis")
        for r in risks:
            st.warning(r)

        st.session_state.history.append(summary)

# ------------------ AI ASSISTANT ------------------
def ai_assistant():
    st.title("🤖 AI Assistant")

    query = st.text_input("Ask something about your contract")

    if st.button("Get Answer"):
        st.success("Suggestion: Carefully review interest rates, penalties, and loan tenure before signing.")

# ------------------ NEGOTIATION ------------------
def negotiation():
    st.title("💬 Negotiation Helper")

    issue = st.selectbox("Select Issue", [
        "High Interest Rate",
        "Penalty Charges",
        "Loan Tenure"
    ])

    if st.button("Generate Message"):
        st.success(f"I would like to negotiate the {issue.lower()} for better terms and flexibility.")

# ------------------ HISTORY ------------------
def history():
    st.title("📁 History")

    if not st.session_state.history:
        st.info("No contracts analyzed yet.")

    for i, item in enumerate(st.session_state.history):
        st.write(f"Contract {i+1}: {item[:100]}...")

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
