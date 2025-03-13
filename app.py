from dotenv import load_dotenv
import streamlit as st
from frontend import analyze_resume
from fastapi import FastAPI, UploadFile, File, Form
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
    try:
        images = pdf2image.convert_from_bytes(pdf_bytes)
        if not images:
            print("Error: No images extracted from PDF")
            return None

        first_page = images[0]
        print("First page extracted successfully.")

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')

        base64_encoded = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

        print("Extracted PDF Content (Base64, first 100 chars):", base64_encoded[:100])  # Debugging
        return base64_encoded
    except Exception as e:
        print("Poppler/PDF Extraction Error:", e)
        return None


# Function to generate response using Gemini AI
def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content([input_text, pdf_content, prompt])  
    
    print("Gemini Response:", response)  # Debugging line

    if not response or not response.text:
        return "Error: Empty response from Gemini"
    
    return response.text

# FastAPI endpoint for resume analysis
@app.post("/analyse_resume")
async def input_pdf_setup(job_description: str = Form(...), resume: UploadFile = File(...)):
    try:
        pdf_bytes = await resume.read()

        if not pdf_bytes:
            return {"error": "Uploaded file is empty"}

        pdf_content = extract_pdf_content(pdf_bytes)

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

        return {
            "job_description": job_description,
            "analysis": response1 if response1 else "Error: No analysis generated.",
            "percentage_match": response2 if response2 else "Error: No percentage match found."
        }
    except Exception as e:
        return {"error": f"Server error: {str(e)}"}
