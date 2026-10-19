
import os
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import pymupdf

from .skill_extractor import extract_skills
from .job_matcher import match_resume
from .database import save_analysis, get_analysis_history


# ==========================
# LOGGING CONFIGURATION
# ==========================

logger = logging.getLogger(__name__)


# ==========================
# FASTAPI APPLICATION
# ==========================

app = FastAPI(
    title="AI Resume Analyzer",
    description="Resume Analysis and Job Matching Web Application",
    version="1.1.0"
)


# ==========================
# CORS CONFIGURATION
# ==========================

# Allow existing local frontend
ALLOWED_ORIGINS = [
    "http://localhost:5500",
    "http://127.0.0.1:5500"
]

# Allow additional frontend origins configured in Azure App Service.
# Example:
# FRONTEND_ORIGINS=https://your-frontend.azurestaticapps.net

extra_origins = os.getenv("FRONTEND_ORIGINS", "")

if extra_origins:
    ALLOWED_ORIGINS.extend(
        origin.strip().rstrip("/")
        for origin in extra_origins.split(",")
        if origin.strip()
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# ==========================
# SKILL RECOMMENDATIONS
# ==========================

SKILL_RECOMMENDATIONS = {
    "Python": "Practice Python fundamentals, functions, OOP, and data structures.",
    "SQL": "Practice SQL joins, aggregations, subqueries, and window functions.",
    "JavaScript": "Learn JavaScript fundamentals, DOM manipulation, and asynchronous programming.",
    "HTML": "Learn semantic HTML and accessible web page structure.",
    "CSS": "Practice responsive layouts using Flexbox, Grid, and media queries.",
    "React": "Learn React components, props, state, and hooks.",
    "Node.js": "Learn Node.js fundamentals and build a basic REST API.",
    "FastAPI": "Build REST APIs using FastAPI, request validation, and routing.",
    "Flask": "Build a small web application using Flask.",
    "Django": "Learn Django models, views, templates, and authentication.",
    "Power BI": "Practice Power Query, DAX, data modeling, and dashboard creation.",
    "Excel": "Practice PivotTables, XLOOKUP, conditional formulas, and dashboards.",
    "Pandas": "Practice data cleaning, filtering, grouping, and merging DataFrames.",
    "NumPy": "Learn NumPy arrays, indexing, broadcasting, and numerical operations.",
    "Machine Learning": "Study supervised learning, model evaluation, and basic ML algorithms.",
    "NLP": "Learn text preprocessing, tokenization, and basic NLP techniques.",
    "Git": "Practice Git branching, merging, commits, and version control.",
    "GitHub": "Learn GitHub repositories, pull requests, and collaborative workflows.",
    "Docker": "Practice creating Dockerfiles and containerizing applications.",
    "AWS": "Learn AWS fundamentals, including EC2, S3, and IAM.",
    "Azure": "Explore Azure fundamentals, cloud storage, and virtual machines.",
    "Java": "Practice Java OOP, collections, and exception handling.",
    "C++": "Practice C++ fundamentals, STL, and object-oriented programming.",
    "C#": "Learn C# fundamentals, OOP, and basic .NET development.",
    "REST API": "Learn HTTP methods, status codes, JSON, and REST API design.",
    "LangGraph": "Explore LangGraph state management, nodes, and agent workflows.",
    "Data Analysis": "Practice data cleaning, exploratory analysis, visualization, and reporting."
}


def generate_recommendations(missing_skills: list[str]) -> list[dict]:
    """
    Generate learning recommendations for skills
    missing from the candidate's resume.
    """

    recommendations = []

    for skill in missing_skills:
        suggestion = SKILL_RECOMMENDATIONS.get(
            skill,
            f"Explore the fundamentals of {skill} and build a practical project."
        )

        recommendations.append({
            "skill": skill,
            "recommendation": suggestion
        })

    return recommendations


# ==========================
# HOME API
# ==========================

@app.get("/")
def home():
    return {
        "message": "Welcome to AI Resume Analyzer",
        "status": "Backend is running successfully"
    }


# ==========================
# HEALTH CHECK API
# ==========================

@app.get("/health")
def health_check():
    return {"status": "healthy"}


# ==========================
# RESUME UPLOAD API
# ==========================

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    pdf_bytes = await file.read()

    if len(pdf_bytes) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="PDF must be smaller than 5 MB"
        )

    if not pdf_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    try:
        with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:

            if doc.needs_pass:
                raise ValueError("Password-protected PDF")

            extracted_text = ""

            for page in doc:
                extracted_text += page.get_text() + "\n"

    except (pymupdf.FileDataError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="Invalid or password-protected PDF"
        )

    if not extracted_text.strip():
        raise HTTPException(
            status_code=422,
            detail="No readable text found in the PDF"
        )

    detected_skills = extract_skills(extracted_text)

    return {
        "filename": file.filename,
        "message": "Resume analyzed successfully",
        "extracted_text": extracted_text,
        "character_count": len(extracted_text),
        "detected_skills": detected_skills,
        "total_skills": len(detected_skills)
    }


# ==========================
# RESUME JOB MATCHING API
# ==========================

@app.post("/analyze-resume")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    pdf_bytes = await file.read()

    if len(pdf_bytes) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="PDF must be smaller than 5 MB"
        )

    if not pdf_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded PDF is empty"
        )

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty"
        )

    try:
        with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:

            if doc.needs_pass:
                raise ValueError("Password-protected PDF")

            resume_text = ""

            for page in doc:
                resume_text += page.get_text() + "\n"

    except (pymupdf.FileDataError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="Invalid or password-protected PDF"
        )

    if not resume_text.strip():
        raise HTTPException(
            status_code=422,
            detail="No readable text found in the PDF"
        )

    # Compare resume with job requirements
    result = match_resume(
        resume_text,
        job_description
    )

    if result["total_required_skills"] == 0:
        raise HTTPException(
            status_code=422,
            detail="No recognizable skills found in job description"
        )

    # Generate recommendations from missing skills
    recommendations = generate_recommendations(
        result["missing_skills"]
    )

    # Save analysis results to SQL Server
    try:
        analysis_id = save_analysis(
            filename=file.filename,
            job_description=job_description,
            result=result
        )

    except Exception:
        logger.exception("Database save failed")

        raise HTTPException(
            status_code=500,
            detail="Resume analyzed, but saving to the database failed"
        )

    # Return results and recommendations
    return {
        "analysis_id": analysis_id,
        "filename": file.filename,
        "message": "Resume analysis completed and saved successfully",
        **result,
        "recommendations": recommendations
    }


# ==========================
# ANALYSIS HISTORY API
# ==========================

@app.get("/analysis-history")
def analysis_history():

    try:
        history = get_analysis_history()

        return {
            "message": "Analysis history retrieved successfully",
            "total_analyses": len(history),
            "history": history
        }

    except Exception:
        logger.exception("Database history retrieval failed")

        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve analysis history"
        )
