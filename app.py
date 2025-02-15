from dotenv import load_dotenv
import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image

import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set in environment variables")
genai.configure(api_key=api_key)

# Function to generate response using Gemini
# Function to generate response using Gemini (Ensuring Free Version)
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')  # Ensure correct model name
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Function to process PDF and extract first page as an image
def input_pdf_setup(uploaded_file):
    if uploaded_file is None:
        raise FileNotFoundError("No file uploaded")

    # Convert the PDF to images
    images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path=r"E:\ats-checker\Release-24.08.0-0\poppler-24.08.0\Library\bin")

    if not images:
        raise ValueError("Failed to extract images from the PDF")

    first_page = images[0]

    # Convert image to bytes
    img_byte_arr = io.BytesIO()
    first_page.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()

    pdf_parts = [
        {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode('utf-8')
        }
    ]
    
    return pdf_parts

# streamlit application 

st.set_page_config(page_title="ATS Resume Expert", page_icon=":books:")
st.header("Application Tracking System")
input_text = st.text_area("Job Description :",key= "input")

uploaded_file = st.file_uploader("Upload your resume[pdf]", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Sucessfully")

submit1 = st.button("Tell me about the resume")
# submit2 = st.button("How can I improve my resume")
submit3 = st.button("Percentage match")

input_prompt1 = """
You are an experienced HR With Tech Experience in the filed of Data Science, Full stack Web development, 
Big Data Engineering, DEVOPS, Data Analyst, your task is to
review the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with |
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements
"""

input_prompt2 ="""
    You are an skilled ATS(Application Tracking System) scanner with a deep understanding of the ATS industry.
    Your task is to review the provided resume against the job description provided.
    Please provide a detailed analysis highlighting any potential strengths and weaknesses of the candidate in relation to the job requirements.
    First the output should come as percentage and then keywords missing in the resume.

"""
# input_prompt3 = """

# """

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The response is :")
        st.write(response)
    else:
        st.write("Please upload file")

if submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The response is :")
        st.write(response)
    else:
        st.write("Please upload file")