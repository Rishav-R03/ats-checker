import streamlit as st
import requests

# Backend API URL
BACKEND_URL = "http://localhost:8000"

def resume_matcher():
    st.title("Job Description Parser")
    st.write("Paste a job description to extract key details")
    
    # Text area for input
    job_description = st.text_area("Job Description", height=300)
    
    if st.button("Parse Description"):
        if job_description:
            try:
                # ✅ Corrected API request
                response = requests.post(
                    f"{BACKEND_URL}/resume_matcher",
                    json={"text": job_description}  # ✅ Use "text" instead of "description"
                )

                if response.status_code == 200:
                    result = response.json()

                    # Display results
                    st.subheader("Parsed Results")
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"**Role:** {result['role_name'] or 'Not found'}")
                        st.markdown(f"**Salary:** {result['salary'] or 'Not found'}")

                    with col2:
                        st.markdown(f"**Location:** {result['location'] or 'Not found'}")

                    st.subheader("Skills")
                    if result['skills']:
                        skills_html = "".join(
                            f'<span style="background-color: #e0e0e0; padding: 5px 10px; margin: 5px; border-radius: 15px;">{skill}</span>'
                            for skill in result['skills']
                        )
                        st.markdown(skills_html, unsafe_allow_html=True)
                    else:
                        st.write("No skills found")
                else:
                    st.error(f"Error: {response.status_code}")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Error connecting to API: {str(e)}")
        else:
            st.warning("Please enter a job description")

if __name__ == "__main__":
    resume_matcher()
