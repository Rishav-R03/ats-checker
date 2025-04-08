import streamlit as st
import requests

# Backend API URL
BACKEND_URL = "https://ats-checker-u4tz.onrender.com"

def resume_matcher():
    """Resume Matcher UI Page"""
    st.set_page_config(page_title="Resume Matcher", page_icon="📄")
    
    st.title("🔍 Job Description Parser")
    st.write("Enter a job description and extract key details!")

    # Text input for job description
    job_desc = st.text_area("📄 Paste Job Description Here:", height=200)

    if st.button("🔍 Extract Details"):
        if job_desc.strip():
            with st.spinner("Processing... ⏳"):
                try:
                    # Send request to FastAPI backend
                    response = requests.post(f"{BACKEND_URL}/resume_matcher", json={"text": job_desc}, timeout=10)
                    response.raise_for_status()  # Raise error for 4xx/5xx responses

                    # Ensure response is valid JSON
                    result = response.json()

                    # Display extracted information
                    st.markdown("### **🔎 Extracted Details**")

                    st.markdown("**📝 Job Titles:**")
                    st.write(", ".join(result.get("job_titles", [])) or "❌ No titles found.")

                    st.markdown("**🛠️ Required Skills:**")
                    st.write(", ".join(result.get("skills", [])) or "❌ No skills found.")

                    st.markdown("**📈 Experience Level:**")
                    st.write(", ".join(result.get("experience_level", [])) or "❌ Not specified.")

                except requests.exceptions.RequestException as e:
                    st.error(f"❌ API request failed: {e}")
                except ValueError:
                    st.error("❌ Invalid response from API. Expected JSON but got a string.")
                    st.write(response.text)  # Print actual response for debugging

        else:
            st.warning("⚠️ Please enter a job description!")

if __name__ == "__main__":
    resume_matcher()