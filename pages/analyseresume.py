import streamlit as st
import requests

BACKEND_URL = "http://localhost:3000"

def analyse_resume():
    st.set_page_config(page_title="Resume Analyzer", page_icon="📄")
    st.header("Resume Analyzer")

    job_description = st.text_area("Job Description:", key="input")

    uploaded_file = st.file_uploader("Upload your resume [PDF]", type=["pdf"])

    if uploaded_file is not None:
        st.write("✅ PDF Uploaded Successfully")

        submit1 = st.button("Tell me about the resume")
        submit2 = st.button("Percentage match")

        if submit1 or submit2:
            files = {"resume": uploaded_file.getvalue()}
            data = {"job_description": job_description}

            response = requests.post(f"{BACKEND_URL}/analyse_resume", files={"resume": uploaded_file}, data=data)

            if response.status_code == 200:
                result = response.json()
                st.subheader("Analysis:")
                st.write(result.get("analysis"))

                if submit2:
                    st.subheader("Percentage Match:")
                    st.write(result.get("percentage_match"))
            else:
                st.error("⚠️ Error processing the resume. Please try again.")

if __name__ == "__main__":
    analyse_resume()
