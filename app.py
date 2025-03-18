from dotenv import load_dotenv
import streamlit as st
import re
import json
from frontend import analyze_resume
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import os
import io
import base64
from pydantic import BaseModel
from PIL import Image
import pdf2image
import google.generativeai as genai

# Load environment variables
load_dotenv()
class JobDescriptionRequest(BaseModel):
    text: str

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

# Define the request model

# Pydantic model to accept job description
class JobDescriptionRequest(BaseModel):
    description: str

class JobDescription(BaseModel):
    text: str

class JobDetails(BaseModel):
    role_name: Optional[str]
    salary: Optional[str]
    location: Optional[str]
    skills: List[str]

# Function to extract key details from job description

# API endpoint to parse job description
@app.post("/resume_matcher", response_model=JobDetails)
async def parse_job_description(job_desc: JobDescription):
    """
    Parse a job description to extract role name, salary range, location, and required skills.
    """
    text = job_desc.text

    # Extract role name
    role_patterns = [
        r"(?:Job Title|Title|Position|Role):\s*([^\n]+)",
        r"^([A-Z][a-zA-Z\s]+(?:Developer|Engineer|Manager|Analyst|Designer|Consultant|Specialist|Architect|Director|Officer|Administrator|Coordinator|Executive|Assistant|Lead))"
    ]
    role_name_list = [match.group(1).strip() for pattern in role_patterns if (match := re.search(pattern, text))]
    role_name = role_name_list[0] if role_name_list else None

    # Extract salary
    salary_patterns = [
        r"(?:Salary|Compensation|Pay):\s*([^\n]+)",
        r"((?:\$|₹|USD|EUR|£|€)[0-9,.]+\s*(?:to|–|-)\s*(?:\$|₹|USD|EUR|£|€)?[0-9,.]+\s*(?:per\s*year|/year|annum|annually|/yr|a year)?)",
        r"((?:\$|₹|USD|EUR|£|€)[0-9,.]+\s*(?:per\s*year|/year|annum|annually|/yr|a year)?)"
    ]
    salary_list = [match.group(1).strip() for pattern in salary_patterns if (match := re.search(pattern, text))]
    salary = salary_list[0] if salary_list else None

    # Extract location
    location_patterns = [
        r"(?:Location|Place|City|Address|Based in|Position located in|Work location):\s*([^\n]+)",
        r"(?:in|at)\s+([A-Z][a-zA-Z\s]+,\s*[A-Z]{2})",
        r"([A-Z][a-zA-Z\s]+,\s*[A-Z]{2})",
        r"(Remote|Work from home|Hybrid|On-site)"
    ]
    location_list = [match.group(1).strip() for pattern in location_patterns if (match := re.search(pattern, text, re.IGNORECASE))]
    location = location_list[0] if location_list else None

    # Extract skills
    skill_keywords = [
        "Python", "Java", "JavaScript", "SQL", "C\\+\\+", "C#", "Ruby", "PHP", "Swift", 
        "Kotlin", "Go", "Rust", "HTML", "CSS", "React", "Angular", "Vue", "Node.js",
        "Django", "Flask", "Ruby on Rails", "Spring", "ASP.NET", "Express.js", 
        "PostgreSQL", "MySQL", "MongoDB", "Oracle", "SQL Server", "NoSQL",
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Git", "CI/CD", "Jenkins",
        "Agile", "Scrum", "Kanban", "Jira", "Confluence", "DevOps", "Linux", "Unix",
        "Machine Learning", "AI", "Data Science", "TensorFlow", "PyTorch", "Pandas",
        "Excel", "PowerPoint", "Word", "Communication", "Teamwork", "Leadership"
    ]
    
    skill_pattern = r'\b(?:' + '|'.join(skill_keywords) + r')\b'
    skills_found = list(set(re.findall(skill_pattern, text, re.IGNORECASE)))

    # Extract additional skills from sections like "Skills:", "Requirements:", etc.
    skill_section_patterns = [
        r"(?:Skills|Requirements|Qualifications|Prerequisites):\s*([^\n]+)",
        r"(?:Skills Required|Technical Skills):\s*([^\n]+)"
    ]
    for pattern in skill_section_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            section_text = match.group(1)
            section_skills = [s.strip() for s in re.split(r',|\•|\*|\-', section_text) if s.strip()]
            skills_found.extend(section_skills)

    # Clean up skills list (remove duplicates and empty strings)
    skills_found = list(set([skill.strip() for skill in skills_found if skill.strip()]))

    # Return parsed details
    return JobDetails(
        role_name=role_name,
        salary=salary,
        location=location,
        skills=skills_found
    )