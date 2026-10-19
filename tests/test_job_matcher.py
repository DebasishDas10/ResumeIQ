
import pytest

from backend.job_matcher import match_resume


def test_perfect_match():
    result = match_resume(
        "Python, SQL, Docker",
        "Python, SQL, Docker"
    )

    assert result["match_score"] == 100.0
    assert result["total_matched_skills"] == 3
    assert result["missing_skills"] == []


def test_partial_match():
    result = match_resume(
        "Python, SQL",
        "Python, SQL, Docker, AWS"
    )

    assert result["match_score"] == 50.0
    assert set(result["missing_skills"]) == {"Docker", "AWS"}


def test_no_match():
    result = match_resume(
        "Python",
        "Docker, AWS"
    )

    assert result["match_score"] == 0.0
    assert result["total_matched_skills"] == 0


def test_extra_resume_skills():
    result = match_resume(
        "Python, SQL, Docker",
        "Python"
    )

    assert result["match_score"] == 100.0


def test_match_score_calculation():
    result = match_resume(
        "Python",
        "Python, SQL, Docker"
    )

    assert result["match_score"] == pytest.approx(33.33)


def test_expected_response_fields():
    result = match_resume(
        "Python, SQL",
        "Python, SQL, AWS"
    )

    expected_fields = {
        "match_score",
        "resume_skills",
        "required_skills",
        "matched_skills",
        "missing_skills",
        "total_required_skills",
        "total_matched_skills",
    }

    assert expected_fields.issubset(result.keys())
