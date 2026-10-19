
import re

# ==========================
# TECHNICAL SKILLS DATABASE
# ==========================

SKILLS = {
    "Python": [
        "python", "python3"
    ],

    "SQL": [
        "sql", "mysql", "sql server",
        "mssql", "postgresql", "postgres",
        "t-sql", "tsql"
    ],

    "JavaScript": [
        "javascript", "java script", "js"
    ],

    "HTML": [
        "html", "html5"
    ],

    "CSS": [
        "css", "css3"
    ],

    "React": [
        "react", "react.js", "reactjs"
    ],

    "Node.js": [
        "node.js", "nodejs", "node js"
    ],

    "FastAPI": [
        "fastapi", "fast api"
    ],

    "Flask": [
        "flask"
    ],

    "Django": [
        "django"
    ],

    "Power BI": [
        "power bi", "powerbi", "power-bi"
    ],

    "Excel": [
        "excel", "microsoft excel", "ms excel"
    ],

    "Pandas": [
        "pandas"
    ],

    "NumPy": [
        "numpy", "num py"
    ],

    "Machine Learning": [
        "machine learning", "ml"
    ],

    "NLP": [
        "nlp", "natural language processing"
    ],

    "Git": [
        "git", "git version control"
    ],

    "GitHub": [
        "github"
    ],

    "Docker": [
        "docker", "docker containers"
    ],

    "AWS": [
        "aws", "amazon web services"
    ],

    "Azure": [
        "azure", "microsoft azure"
    ],

    "Java": [
        "java"
    ],

    "C++": [
        "c++", "cpp"
    ],

    "C#": [
        "c#", "c sharp"
    ],

    "REST API": [
        "rest api", "restful api",
        "rest apis", "restful services"
    ],

    "LangGraph": [
        "langgraph", "lang graph"
    ],

    "Data Analysis": [
        "data analysis", "data analytics",
        "data analyst"
    ]
}


# ==========================
# SKILL EXTRACTION FUNCTION
# ==========================

def extract_skills(text: str) -> list[str]:
    """
    Extract technical skills from resume or job description.

    Features:
    - Case-insensitive matching
    - Skill abbreviation recognition
    - Whole-term matching
    - Duplicate prevention
    - Alphabetically sorted output
    """

    if not isinstance(text, str) or not text.strip():
        return []

    found_skills = set()

    for skill, keywords in SKILLS.items():

        for keyword in keywords:

            # Match complete skill terms rather than parts of words
            pattern = (
                r"(?<![A-Za-z0-9_+#])"
                + re.escape(keyword)
                + r"(?![A-Za-z0-9_+#])"
            )

            if re.search(pattern, text, re.IGNORECASE):
                found_skills.add(skill)
                break

    return sorted(found_skills)
