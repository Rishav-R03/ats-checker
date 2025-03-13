import streamlit as st

def home():
    st.set_page_config(page_title="ATS Resume Expert", page_icon="📄")

    st.title("Welcome to ATS Resume Expert")
    st.subheader("Optimize your resume for job applications")

    st.markdown(
        """
        **Features:**
        - 📄 Upload your resume and get an AI-powered analysis.
        - 🎯 Match your resume with job descriptions.
        - 🔍 Identify missing keywords to improve your chances.
        - 📊 Get a percentage match score for ATS optimization.

        **How It Works:**
        1. Navigate to **Analyze Resume** page.
        2. Upload your resume in **PDF format**.
        3. Enter the job description.
        4. Get AI-powered feedback!
        """
    )

    # st.image("https://via.placeholder.com/800x400?text=ATS+Resume+Expert", use_container_width=True)

    # Correct Navigation for Multi-Page App
    if st.button("Go to Resume Analyzer"):
        st.page_link("pages/analyseresume.py", label="Go to Resume Analyzer", icon="📄")
    if st.button("Go to Job Description Parser"):
        st.page_link("pages/resumematcher.py", label="Go to Job Description Parser", icon="📄")
