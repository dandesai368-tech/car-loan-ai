import streamlit as st

st.title("🚗 Car Loan AI Assistant")

st.write("Upload your contract and click analyze")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    st.success("File uploaded!")

    if st.button("Analyze Contract"):
        st.subheader("⚠️ Risks")
        st.write("Penalty, Interest found")

        st.subheader("📊 Risk Score")
        st.progress(0.6)

        st.subheader("💡 Suggestions")
        st.write("Negotiate interest rate")

        st.subheader("📄 Summary")
        st.write("This is sample summary")
