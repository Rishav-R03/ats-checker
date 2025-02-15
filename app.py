from dotenv import load_dotenv
import streamlit as st
from fastapi import FastAPI, UploadFile, File
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

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to ATS Resume Expert"}

# Function to extract first page from PDF as image
def extract_pdf_content(pdf_bytes):
    images = pdf2image.convert_from_bytes(pdf_bytes)  # Ensure Poppler is installed
    if not images:
        return None
    
    first_page = images[0]
    img_byte_arr = io.BytesIO()
    first_page.save(img_byte_arr, format='JPEG')
    return base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')  # Corrected encoding

# Function to generate response using Gemini AI
def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content([input_text, pdf_content, prompt])  
    return response.text

# FastAPI endpoint for resume analysis
@app.post("/analyse_resume")
async def input_pdf_setup(job_description: str, resume: UploadFile = File(...)):
    try:
        pdf_content = extract_pdf_content(await resume.read())
        if not pdf_content:
            return {"error": "Failed to process PDF"}

        # Different prompts for analysis
        input_prompt1 = """
        You are an experienced HR with expertise in Data Science, Full Stack Development, Big Data, DevOps, and Data Analytics. 
        Your task is to evaluate the resume based on the given job description and provide insights on strengths and weaknesses.
        """
        input_prompt2 = """
        You are an ATS (Applicant Tracking System) expert. Your task is to analyze the resume against the given job description. 
        Provide a percentage match and list missing keywords.
        """

        # Generate responses
        response1 = get_gemini_response(input_prompt1, pdf_content, job_description)
        response2 = get_gemini_response(input_prompt2, pdf_content, job_description)

        return {"job_description": job_description, "analysis": response1, "percentage_match": response2}
    except Exception as e:
        return {"error": str(e)}

# Streamlit UI
st.set_page_config(page_title="ATS Resume Expert", page_icon=":books:")
st.header("Application Tracking System")

# Job description input
input_text = st.text_area("Job Description:", key="input")

# Resume upload
uploaded_file = st.file_uploader("Upload your resume [PDF]", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

    # Buttons for different analyses
    submit1 = st.button("Tell me about the resume")
    submit3 = st.button("Percentage match")

    if submit1 or submit3:
        pdf_bytes = uploaded_file.read()
        pdf_content = extract_pdf_content(pdf_bytes)

        if pdf_content:
            prompt = (
                "Analyze this resume" if submit1 
                else "Provide a percentage match and missing keywords"
            )
            response = get_gemini_response(input_text, pdf_content, prompt)

            st.subheader("The response is:")
            st.write(response)
        else:
            st.write("Error processing PDF. Please try again.")
