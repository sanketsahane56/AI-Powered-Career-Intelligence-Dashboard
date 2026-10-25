"""
Unit Tests for Database Operations
"""
import pytest
from database.db import Database


@pytest.fixture(autouse=True)
def setup_test_db():
    Database.init_db()


def test_save_and_retrieve_analysis():
    dummy_analysis = {
        "overall_score": 85,
        "word_count": 450,
        "page_count": 1,
        "skills": {"total_count": 12, "all_skills": ["Python", "Docker"]},
        "dimensions": {"skill_breadth": {"score": 80}},
        "role_matches": [{"role": "Full Stack Engineer", "fit_percentage": 82}],
        "action_plan": ["Add more metrics"]
    }
    dummy_meta = {
        "candidate_name": "Test Candidate",
        "email": "test@example.com",
        "phone": "(555) 000-1111"
    }

    session_id = Database.save_analysis(dummy_analysis, dummy_meta, "Sample raw text content")
    assert session_id is not None
    assert len(session_id) > 0

    record = Database.get_analysis_by_session_id(session_id)
    assert record is not None
    assert record["candidate_name"] == "Test Candidate"
    assert record["overall_score"] == 85
    assert record["top_role"] == "Full Stack Engineer"

    # Test analytics summary
    stats = Database.get_analytics_summary()
    assert stats["total_analyses"] >= 1
    assert stats["average_score"] > 0

    # Test delete
    deleted = Database.delete_analysis(session_id)
    assert deleted is True
    assert Database.get_analysis_by_session_id(session_id) is None
