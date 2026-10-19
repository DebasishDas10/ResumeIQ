
# ResumeIQ — Resume Analyzer & Job Matcher

[![ResumeIQ Automated Tests](https://github.com/DebasishDas10/ResumeIQ/actions/workflows/tests.yml/badge.svg)](https://github.com/DebasishDas10/ResumeIQ/actions/workflows/tests.yml)

ResumeIQ is a full-stack web application that analyzes PDF resumes, extracts technical skills, and compares them with job descriptions to identify matching and missing skills.

It provides a skill match score, personalized improvement recommendations, and a history of previous analyses stored in Microsoft SQL Server.

## Features

- Upload and extract text from PDF resumes
- Extract technical skills using rule-based keyword matching
- Compare resume skills with job description requirements
- Calculate a percentage-based skill match score
- Display matched and missing skills
- Generate personalized skill improvement recommendations
- Store analysis results in Microsoft SQL Server
- View previous resume analyses
- Validate file format, file size, and user inputs
- Responsive web dashboard
- Automated unit testing with pytest
- Continuous Integration using GitHub Actions

## Tech Stack

**Backend:** Python, FastAPI, PyMuPDF

**Frontend:** HTML, CSS, JavaScript

**Database:** Microsoft SQL Server, pyodbc

**Testing:** pytest

**CI:** GitHub Actions

**Development Tools:** VS Code, Git, GitHub

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
│       └── tests.yml
├── requirements.txt
├── .gitignore
└── README.md
```

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

The match score is calculated using:

**Match Score (%) = (Number of Matched Skills / Total Required Skills) × 100**

For example, if a job description requires 5 recognized technical skills and the resume contains 4 of them, the match score is 80%.

This score measures technical skill keyword overlap. It is not an official Applicant Tracking System (ATS) score or a prediction of hiring probability.

## Automated Testing & Continuous Integration

ResumeIQ includes an automated testing suite built using **pytest** and a Continuous Integration (CI) workflow configured with **GitHub Actions**.

### Unit Testing

The project includes 12 automated unit tests covering two core components.

**Skill Extraction Tests (6)**

- Python skill detection
- Multiple skill detection
- Case-insensitive skill recognition
- Technical skill alias detection
- Duplicate skill removal
- Empty text handling

**Job Matching Tests (6)**

- Perfect skill matching
- Partial skill matching
- No matching skills
- Additional resume skills
- Percentage-based match score calculation
- API response data structure validation

### Running Tests Locally

Install project dependencies:

```bash
python -m pip install -r requirements.txt
```

Execute all tests:

```bash
python -m pytest tests/ -v
```

### GitHub Actions CI Workflow

The project uses a GitHub Actions workflow located at:

`.github/workflows/tests.yml`

The workflow automatically:

1. Triggers on pushes to the `main` branch and pull requests targeting `main`.
2. Checks out the repository.
3. Sets up Python 3.12.
4. Installs pytest.
5. Executes the automated unit tests.
6. Reports test results on GitHub.

The CI workflow tests the core Python skill extraction and matching logic without requiring a running SQL Server instance.

**Workflow:** [View GitHub Actions](https://github.com/DebasishDas10/ResumeIQ/actions/workflows/tests.yml)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/DebasishDas10/ResumeIQ.git
cd ResumeIQ
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure SQL Server

Install Microsoft SQL Server and ODBC Driver 18 for SQL Server.

Create a database named `ResumeIQ` and execute the following SQL script to create the analysis table:

```sql
USE ResumeIQ;

CREATE TABLE dbo.Resume_Analysis (
    Analysis_ID INT IDENTITY(1,1) PRIMARY KEY,
    File_Name NVARCHAR(255) NOT NULL,
    Job_Description NVARCHAR(MAX) NOT NULL,
    Match_Score DECIMAL(5,2) NOT NULL,
    Matched_Skills NVARCHAR(MAX),
    Missing_Skills NVARCHAR(MAX),
    Total_Required_Skills INT NOT NULL,
    Total_Matched_Skills INT NOT NULL,
    Created_At DATETIME2 DEFAULT SYSDATETIME()
);
```

If the database does not already exist, create it first using SQL Server Management Studio.

Update the connection settings in `backend/database.py` to match your local SQL Server instance.

For the original local development environment, the application uses SQL Server Express with Windows Authentication.

### 6. Start the Backend

From the project root directory:

```bash
python -m uvicorn backend.main:app --reload
```

The API will run at:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

### 7. Start the Frontend

Open `frontend/index.html` using VS Code Live Server.

The frontend is configured to communicate with the locally running FastAPI backend.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Application information |
| GET | `/health` | Health check |
| POST | `/upload-resume` | Upload and extract resume information |
| POST | `/analyze-resume` | Analyze resume against job description |
| GET | `/analysis-history` | Retrieve previous analyses |

## Limitations

- Skill detection uses predefined rules rather than a trained machine learning model.
- The match score does not represent hiring probability.
- Scanned PDFs without selectable text may not be supported.
- SQL Server must be configured locally before running the complete application.
- Current automated tests cover core matching functions, not the full database or frontend integration.
- The application is intended for local demonstration and is not production-ready.

## Future Improvements

- NLP-based skill extraction
- Semantic similarity using embeddings
- User authentication
- Integration testing for API and database operations
- Resume analysis visualization
- Secure cloud deployment

## Author

**Debasish Das**

B.Tech, Electronics and Communication Engineering

National Institute of Technology Silchar

**GitHub:** [DebasishDas10](https://github.com/DebasishDas10)
