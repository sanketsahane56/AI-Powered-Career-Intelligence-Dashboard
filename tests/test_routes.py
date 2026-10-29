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
    # Default (tech)
    res = client.get("/api/sample-resume")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "ALEX MORGAN" in data["text"]

    # Product domain
    res_pm = client.get("/api/sample-resume?domain=product")
    assert res_pm.status_code == 200
    data_pm = res_pm.get_json()
    assert data_pm["success"] is True
    assert "PRIYA SHARMA" in data_pm["text"]

    # Data domain
    res_data = client.get("/api/sample-resume?domain=data")
    assert res_data.status_code == 200
    data_res = res_data.get_json()
    assert data_res["success"] is True
    assert "DAVID CHEN" in data_res["text"]

    # Design domain
    res_design = client.get("/api/sample-resume?domain=design")
    assert res_design.status_code == 200
    data_design = res_design.get_json()
    assert data_design["success"] is True
    assert "MAYA LIN" in data_design["text"]

    # Marketing domain
    res_mktg = client.get("/api/sample-resume?domain=marketing")
    assert res_mktg.status_code == 200
    data_mktg = res_mktg.get_json()
    assert data_mktg["success"] is True
    assert "SARAH JENKINS" in data_mktg["text"]

    # Finance domain
    res_fin = client.get("/api/sample-resume?domain=finance")
    assert res_fin.status_code == 200
    data_fin = res_fin.get_json()
    assert data_fin["success"] is True
    assert "LIAM KAUFMAN" in data_fin["text"]

    # HR domain
    res_hr = client.get("/api/sample-resume?domain=hr")
    assert res_hr.status_code == 200
    data_hr = res_hr.get_json()
    assert data_hr["success"] is True
    assert "RACHEL GREENBERG" in data_hr["text"]

    # Cybersecurity domain
    res_sec = client.get("/api/sample-resume?domain=cybersecurity")
    assert res_sec.status_code == 200
    data_sec = res_sec.get_json()
    assert data_sec["success"] is True
    assert "ETHAN VANCE" in data_sec["text"]


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


def test_delete_analysis_api(client):
    # Test deleting a session via API
    res = client.delete("/api/analysis/non-existent-session-id")
    assert res.status_code == 200
    data = res.get_json()
    assert "success" in data

