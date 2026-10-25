"""
Integration Tests for Flask Web Routes & API Endpoints
"""
import io
import json
import pytest
from app import app
from database.db import Database


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "healthy"
    assert data["service"] == "CareerIQ - AI Career Intelligence Dashboard"


def test_page_routes(client):
    pages = ["/", "/scanner", "/job-match", "/roles", "/history", "/guide"]
    for path in pages:
        res = client.get(path)
        assert res.status_code == 200, f"Failed on path {path}"


def test_sample_resume_api(client):
    res = client.get("/api/sample-resume")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "ALEX MORGAN" in data["text"]


def test_analyze_resume_api_text(client):
    sample_text = """
    SAMANTHA VANCE
    sam.vance@techdev.io | (415) 555-8765
    linkedin.com/in/samvance | github.com/samvance

    EXPERIENCE
    Senior Full Stack Engineer
    • Architected microservices in Python, FastAPI, and React, increasing throughput by 40%.
    • Spearheaded database migration to PostgreSQL and Redis.
    • Managed a team of 4 engineers and improved sprint velocity by 25%.

    SKILLS
    Python, JavaScript, TypeScript, React, Next.js, Node.js, PostgreSQL, Docker, AWS, Git, CI/CD

    EDUCATION
    BS Computer Science
    """
    res = client.post("/api/analyze-resume", data={"resume_text": sample_text})
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "session_id" in data
    assert data["metadata"]["candidate_name"] == "Samantha Vance"
    assert data["analysis"]["overall_score"] >= 60

    # Test PDF download endpoint for this newly created session
    session_id = data["session_id"]
    pdf_res = client.get(f"/api/download-report/{session_id}")
    assert pdf_res.status_code == 200
    assert pdf_res.mimetype == "application/pdf"


def test_compare_job_api(client):
    payload = {
        "job_description": "We need a Senior Backend Engineer proficient in Python, FastAPI, PostgreSQL, Docker, and Kubernetes.",
        "skills": ["Python", "PostgreSQL", "Docker", "Git"]
    }
    res = client.post(
        "/api/compare-job",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["comparison"]["match_score"] > 0
    assert "Python" in data["comparison"]["matched_skills"]
    assert "Kubernetes" in data["comparison"]["missing_skills"]


def test_404_page(client):
    res = client.get("/non-existent-route-xyz")
    assert res.status_code == 404
    assert b"404" in res.data
