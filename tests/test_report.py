"""
Unit Tests for PDF Report Generation
"""
import io
import pytest
from engine.report_generator import ReportGenerator


def test_generate_pdf_report():
    analysis_data = {
        "overall_score": 88,
        "dimensions": {
            "skill_breadth": {"name": "Skills Breadth", "weight": "30%", "score": 85, "detail": "15 skills found"},
            "impact_metrics": {"name": "Impact Metrics", "weight": "25%", "score": 90, "detail": "6 metrics detected"}
        },
        "skills": {
            "total_count": 10,
            "by_category": {
                "Programming Languages": ["Python", "TypeScript"],
                "Databases & Storage": ["PostgreSQL", "Redis"]
            }
        },
        "metrics": {"count": 6},
        "verbs": {"strong_count": 8},
        "role_matches": [
            {
                "role": "Full Stack Engineer",
                "fit_percentage": 85,
                "matched_core": ["Python", "React", "SQL"],
                "missing_core": ["Docker"]
            }
        ],
        "action_plan": [
            "Incorporate more cloud tools like Docker and AWS.",
            "Quantify results in the second work experience."
        ]
    }
    metadata = {
        "candidate_name": "Jordan Smith",
        "email": "jordan@example.com",
        "phone": "(555) 321-7654"
    }

    pdf_stream = ReportGenerator.generate_pdf(analysis_data, metadata)
    assert isinstance(pdf_stream, io.BytesIO)
    content = pdf_stream.getvalue()
    assert len(content) > 1000
    assert content.startswith(b"%PDF-")
