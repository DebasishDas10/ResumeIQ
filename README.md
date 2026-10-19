
# ResumeIQ — Resume Analyzer & Job Matcher

ResumeIQ is a full-stack web application that analyzes PDF resumes, extracts technical skills, and compares them with job descriptions to identify matching and missing skills.

It provides a skill match score, personalized improvement recommendations, and a history of previous analyses stored in Microsoft SQL Server.

## Features

- Upload and extract text from PDF resumes
- Extract technical skills using rule-based keyword matching
- Compare resume skills with job description requirements
- Calculate a percentage-based skill match score
- Display matched and missing skills
- Generate skill improvement recommendations
- Store analysis results in Microsoft SQL Server
- View previous resume analyses
- Validate file format, file size, and user inputs
- Responsive web dashboard

## Tech Stack

**Backend:** Python, FastAPI, PyMuPDF

**Frontend:** HTML, CSS, JavaScript

**Database:** Microsoft SQL Server, pyodbc

**Development Tools:** VS Code, Git, GitHub

## Project Structure

AI-Resume-Analyzer/
- backend/
  - main.py
  - database.py
  - skill_extractor.py
  - job_matcher.py
- frontend/
  - index.html
  - style.css
  - script.js
- requirements.txt
- .gitignore
- README.md

## How It Works

1. The user uploads a PDF resume.
2. PyMuPDF extracts text from the PDF.
3. The application identifies technical skills using predefined keywords and aliases.
4. The user enters a job description.
5. ResumeIQ extracts the required technical skills.
6. The matching algorithm compares both skill sets.
7. The application displays the match score and missing skills.
8. Rule-based recommendations suggest areas for improvement.
9. The analysis is saved to SQL Server for future reference.

## Match Score Calculation

Match Score (%) =
(Number of Matched Skills / Total Required Skills) × 100

This score measures technical skill keyword overlap. It is not an official Applicant Tracking System (ATS) score.

## Installation

### 1. Clone the Repository

git clone YOUR_REPOSITORY_URL
cd AI-Resume-Analyzer

### 2. Create a Virtual Environment

python -m venv .venv

### 3. Activate the Virtual Environment

Windows PowerShell:

.\.venv\Scripts\Activate.ps1

### 4. Install Dependencies

pip install -r requirements.txt

### 5. Configure SQL Server

Install Microsoft SQL Server and ODBC Driver 18 for SQL Server.

Create a database named ResumeIQ and a table named dbo.Resume_Analysis.

Update the connection settings in backend/database.py to match your local SQL Server instance.

### 6. Start the Backend

python -m uvicorn backend.main:app --reload

The API will run at:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

### 7. Start the Frontend

Open frontend/index.html using VS Code Live Server.

The frontend is configured to communicate with the locally running FastAPI backend.

## API Endpoints

- GET / — Application information
- GET /health — Health check
- POST /upload-resume — Upload and extract resume information
- POST /analyze-resume — Analyze resume against job description
- GET /analysis-history — Retrieve previous analyses

## Limitations

- Skill detection uses predefined rules rather than a trained machine learning model.
- The match score does not represent hiring probability.
- Scanned PDFs without selectable text may not be supported.
- SQL Server must be configured locally before running the complete application.
- The application is intended for local demonstration and is not production-ready.

## Future Improvements

- NLP-based skill extraction
- Semantic similarity using embeddings
- User authentication
- Resume analysis visualization
- Cloud deployment

## Author

Debasish Das
B.Tech, Electronics and Communication Engineering
National Institute of Technology Silchar
