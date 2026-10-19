
from backend.skill_extractor import extract_skills


def test_python_skill_detection():
    text = "I have experience in Python programming."
    skills = extract_skills(text)

    assert "Python" in skills


def test_multiple_skill_detection():
    text = "Python, SQL, Docker and AWS"
    skills = extract_skills(text)

    assert "Python" in skills
    assert "SQL" in skills
    assert "Docker" in skills
    assert "AWS" in skills


def test_case_insensitive_detection():
    text = "python and docker"
    skills = extract_skills(text)

    assert "Python" in skills
    assert "Docker" in skills


def test_skill_alias_detection():
    text = "JS, ML, Postgres"
    skills = extract_skills(text)

    assert "JavaScript" in skills
    assert "Machine Learning" in skills
    assert "SQL" in skills


def test_duplicate_skill_removal():
    text = "Python, python, PYTHON"
    skills = extract_skills(text)

    assert skills.count("Python") == 1


def test_empty_text():
    skills = extract_skills("")

    assert skills == []
