# ResumeIQ — Resume Analyzer & Job Matcher

[![Automated Tests](https://github.com/DebasishDas10/ResumeIQ/actions/workflows/tests.yml/badge.svg)](https://github.com/DebasishDas10/ResumeIQ/actions/workflows/tests.yml)

**ResumeIQ** is a full-stack, cloud-deployed web application that analyzes PDF resumes and compares technical skills against job descriptions.

It helps users understand their technical skill compatibility by identifying matched skills, missing skills, and recommended areas for improvement.

The application uses a **Python FastAPI backend**, a responsive **HTML/CSS/JavaScript frontend**, and **Azure SQL Database** for persistent storage. It is deployed on Microsoft Azure with automated testing and deployment through GitHub Actions.

## Live Demo

**[Launch ResumeIQ](https://ambitious-grass-062b32300.6.azurestaticapps.net)**

**[GitHub Repository](https://github.com/DebasishDas10/ResumeIQ)**

## Features

- Upload PDF resumes and extract text using PyMuPDF
- Detect technical skills using predefined keywords and aliases
- Extract technical skill requirements from job descriptions
- Calculate percentage-based skill compatibility scores
- Identify matched and missing skills
- Generate rule-based skill improvement recommendations
- Display results through a responsive web dashboard
- Store analysis results in Azure SQL Database
- Validate uploaded files and user inputs
- Expose REST APIs using FastAPI
- Run automated unit tests using pytest
- Automate testing and deployment with GitHub Actions

## Technology Stack

| Component | Technologies |
|---|---|
| Backend | Python, FastAPI, PyMuPDF |
| Frontend | HTML5, CSS3, JavaScript |
| Database | Microsoft SQL Server, Azure SQL Database |
| Database Connectivity | pyodbc, ODBC Driver 18 |
| Testing | pytest |
| CI/CD | GitHub Actions |
| Cloud Platform | Microsoft Azure |
| Backend Hosting | Azure App Service |
| Frontend Hosting | Azure Static Web Apps |
| Development Tools | VS Code, Git, GitHub |

## System Architecture

```text
                  USER
                    |
                    v
        Azure Static Web Apps
          HTML / CSS / JS
                    |
               HTTPS API
                    |
                    v
           Azure App Service
             Python FastAPI
                    |
          +---------+---------+
          |                   |
          v                   v
      PyMuPDF           Skill Extraction
   PDF Text Parsing      & Job Matching
          |                   |
          +---------+---------+
                    |
                    v
             Azure SQL Database
           Persistent Analysis Data
```

## How It Works

1. The user uploads a PDF resume.
2. PyMuPDF extracts text from the document.
3. ResumeIQ identifies recognized technical skills.
4. The user provides a job description.
5. The backend extracts recognized skills required by the job.
6. The matching algorithm compares resume skills with required skills.
7. The application calculates a skill match score.
8. Matched skills, missing skills, and recommendations are displayed.
9. Analysis results are saved to Azure SQL Database.

## Skill Matching Algorithm

ResumeIQ uses a rule-based skill extraction and comparison approach.

The application identifies technical skills through predefined keywords and aliases, normalizes recognized skills, and compares the skills detected in the resume against those detected in the job description.

### Match Score Formula

**Match Score (%) = (Matched Required Skills / Total Recognized Required Skills) × 100**

For example, if a job description contains five recognized required skills and the resume contains four of them:

**Match Score = (4 / 5) × 100 = 80%**

The score measures recognized technical skill overlap. It is not an official ATS score or a prediction of hiring probability.

## REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Application information |
| GET | `/health` | Backend health check |
| POST | `/upload-resume` | Upload and parse a PDF resume |
| POST | `/analyze-resume` | Analyze a resume against a job description |

### Interactive API Documentation

[Open Live FastAPI Swagger Documentation](https://resumeiq-api-debasish-hpg7acezd0haebbm.koreacentral-01.azurewebsites.net/docs)

## Database Integration

ResumeIQ uses Microsoft SQL Server for local development and Azure SQL Database for cloud deployment.

Analysis records include:

- Resume filename
- Submitted job description
- Match score
- Matched skills
- Missing skills
- Total recognized required skills
- Total matched skills
- Analysis timestamp

Database operations are performed through Python using `pyodbc`.

Database credentials are configured through environment variables in the deployed application.

## Automated Testing

ResumeIQ includes **12 automated unit tests** using pytest.

### Skill Extraction Tests

- Python skill detection
- Multiple skill detection
- Case-insensitive matching
- Skill alias recognition
- Duplicate skill removal
- Empty text handling

### Job Matching Tests

- Perfect matching
- Partial matching
- No matching skills
- Additional resume skills
- Match percentage calculation
- Analysis response structure validation

### Run Tests Locally

```bash
python -m pytest tests/ -v
```

## CI/CD Pipeline

GitHub Actions automates testing and deployment.

The workflow includes:

1. Source code changes pushed to GitHub
2. Automated unit test execution
3. Backend deployment to Azure App Service
4. Frontend deployment to Azure Static Web Apps through its deployment workflow

The deployed application can be updated through the repository's configured GitHub Actions workflows.

## Project Structure

```text
AI-Resume-Analyzer/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── skill_extractor.py
│   └── job_matcher.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── tests/
│   ├── test_skill_extractor.py
│   └── test_job_matcher.py
├── .github/
│   └── workflows/
├── requirements.txt
├── .gitignore
└── README.md
```

## Local Development

### 1. Clone the Repository

```bash
git clone https://github.com/DebasishDas10/ResumeIQ.git
cd ResumeIQ
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure the Database

Install Microsoft SQL Server and ODBC Driver 18 for SQL Server.

Create a database and configure the connection settings expected by `backend/database.py`.

The deployed backend uses a `DATABASE_CONNECTION_STRING` environment variable for Azure SQL connectivity.

Do not commit database passwords, connection strings containing credentials, or other secrets to GitHub.

### 6. Start the Backend

```bash
python -m uvicorn backend.main:app --reload
```

Local API documentation:

http://127.0.0.1:8000/docs

### 7. Start the Frontend

Open `frontend/index.html` using VS Code Live Server.

For local development, configure the frontend API URL to point to the locally running backend. The deployed frontend is configured to use the Azure-hosted FastAPI service.

## Limitations

- Technical skill extraction relies on predefined keywords and aliases.
- Semantic understanding of experience and proficiency is limited.
- The match score is not an official ATS score.
- Image-only scanned PDFs may require OCR.
- Automated tests primarily cover the core matching logic.
- The application requires additional security and operational hardening before production use.

## Future Improvements

- Improved skill normalization and synonym recognition
- Weighted skill matching
- NLP-based contextual skill extraction
- Semantic similarity using embeddings
- User authentication and authorization
- Expanded API and database integration tests
- Improved analysis history and reporting

## Author

**Debasish Das**

B.Tech — Electronics and Communication Engineering

National Institute of Technology Silchar

**GitHub:** [DebasishDas10](https://github.com/DebasishDas10)
