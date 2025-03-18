# **ATS Resume Matcher & Job Description Parser**  
🚀 **An AI-powered tool to match resumes with job descriptions and extract key details using NLP & FastAPI.**  

![GitHub Repo Stars](https://img.shields.io/github/stars/your-repo?style=social) ![GitHub forks](https://img.shields.io/github/forks/ats-checker?style=social) ![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)  

---

## **📌 Overview**  
This project helps job seekers and recruiters analyze job descriptions and resumes using **FastAPI, Streamlit, and NLP models**. It extracts **job titles, required skills, and experience levels** to improve job-to-resume matching and **enhance ATS (Applicant Tracking System) compatibility**.

### **🔍 Features**  
✅ Extract **job titles, required skills, and experience levels** from job descriptions  
✅ AI-powered **resume matching** to assess job fit  
✅ **FastAPI** backend with RESTful API for job description parsing  
✅ **Streamlit UI** for an interactive, user-friendly experience  
✅ **Dockerized** for easy deployment  
✅ **Modular folder structure** for scalability and maintainability  

---

## **🛠️ Tech Stack**  
| **Category**       | **Technology** |
|--------------------|---------------|
| Backend API       | FastAPI |
| Frontend UI       | Streamlit |
| Model/AI          | NLP (Google Gemini / Custom NER) |
| Data Processing   | Python |
| Deployment        | Docker, Cloud (AWS/GCP) |
| Version Control   | Git & GitHub |

---

## **📂 Project Structure**  
```
📦 ats-checker
 ┣ 📂 backend
 ┃ ┣ 📜 models/utils.py  # Job description parser (AI logic)
 ┃ ┣ 📜 main.py          # FastAPI backend
 ┃ ┗ 📜 __init__.py      # Backend init
 ┣ 📂 frontend
 ┃ ┣ 📜 home.py          # Streamlit landing page
 ┃ ┣ 📜 atsfrontend.py   # Resume analysis UI
 ┃ ┣ 📜 __init__.py      # Frontend init
 ┣ 📜 app.py             # Streamlit app entry point
 ┣ 📜 main.py            # Main execution file
 ┣ 📜 requirements.txt   # Dependencies
 ┣ 📜 Dockerfile         # Docker setup
 ┗ 📜 README.md          # Documentation
```

---

## **🚀 Installation & Setup**  

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-username/ats-checker.git
cd ats-checker
```

### **2️⃣ Install Dependencies**  
Make sure you have **Python 3.8+** installed. Then, run:
```sh
pip install -r requirements.txt
```

### **3️⃣ Run the FastAPI Backend**
```sh
uvicorn backend.main:app --reload
```
Backend will start at: `http://127.0.0.1:8000`

### **4️⃣ Run the Streamlit Frontend**
```sh
streamlit run app.py
```
Frontend will be available at: `http://localhost:8501`

---

## **📌 API Endpoints**  

| Method | Endpoint            | Description  |
|--------|--------------------|--------------|
| `GET`  | `/`                | Home route |
| `POST` | `/parse-job/`      | Extracts job details from job description |

### **Example Request (POST `/parse-job/`)**
```json
{
  "text": "We are hiring a Senior DevOps Engineer with expertise in AWS, Kubernetes, and Terraform."
}
```

### **Example Response**
```json
{
  "job_titles": ["Senior DevOps Engineer"],
  "skills": ["AWS", "Kubernetes", "Terraform"],
  "experience_level": ["Senior"]
}
```

---

## **🎨 UI Screenshots**  
🔹 **Landing Page (Streamlit UI)**  
![Landing Page Screenshot](https://via.placeholder.com/800x400.png?text=Landing+Page)  

🔹 **Job Description Analysis**  
![Job Analysis Screenshot](https://via.placeholder.com/800x400.png?text=Job+Description+Analysis)  

🔹 **Resume Matcher Output**  
![Resume Matcher Screenshot](https://via.placeholder.com/800x400.png?text=Resume+Matcher)  

---

## **🛠️ Future Enhancements**  
🚀 **Planned Features**  
- 🔥 **ATS Resume Score Calculation**  
- 📊 **Job Recommendation Engine**  
- 🌍 **Multi-language Support**  
- 📂 **Database Storage for Job Descriptions & Resumes**  

---

## **🤝 Contributing**  
Want to improve this project? Contributions are welcome!  

### **Steps to Contribute**  
1. Fork the repo  
2. Create a new branch (`git checkout -b feature-branch`)  
3. Commit your changes (`git commit -m "Added new feature"`)  
4. Push to your branch (`git push origin feature-branch`)  
5. Submit a Pull Request  

---

## **📄 License**  
This project is licensed under the **MIT License**.  

---

💡 **If you found this project useful, give it a ⭐ on GitHub!**  
📩 **Have suggestions? Open an issue or connect with me!** 🚀  

