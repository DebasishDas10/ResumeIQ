
from .skill_extractor import extract_skills


# ==========================
# CALCULATE SKILL MATCH SCORE
# ==========================

def calculate_match_score(matched_count: int, required_count: int) -> float:
    """
    Calculate the percentage of required skills
    found in the candidate's resume.
    """

    if required_count <= 0:
        return 0.0

    score = (matched_count / required_count) * 100

    return round(max(0.0, min(100.0, score)), 2)


# ==========================
# RESUME JOB MATCHING ENGINE
# ==========================

def match_resume(resume_text: str, job_description: str) -> dict:
    """
    Compare technical skills extracted from a resume
    with the skills required in a job description.

    Returns:
        - Skill match score
        - Resume skills
        - Required job skills
        - Matched skills
        - Missing skills
        - Total required skills
        - Total matched skills
    """

    # Handle invalid or empty inputs
    if not isinstance(resume_text, str):
        resume_text = ""

    if not isinstance(job_description, str):
        job_description = ""

    # Extract and normalize recognized skills
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))

    # Identify matched and missing skills
    matched_skills = resume_skills & job_skills
    missing_skills = job_skills - resume_skills

    # Calculate skill compatibility
    total_required_skills = len(job_skills)
    total_matched_skills = len(matched_skills)

    match_score = calculate_match_score(
        total_matched_skills,
        total_required_skills
    )

    # Return results in the existing API format
    return {
        "match_score": match_score,
        "resume_skills": sorted(resume_skills),
        "required_skills": sorted(job_skills),
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "total_required_skills": total_required_skills,
        "total_matched_skills": total_matched_skills
    }
