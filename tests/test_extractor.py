"""
Unit Tests for Resume Extractor & Parser
"""
import io
import pytest
from reportlab.pdfgen import canvas
from engine.extractor import ResumeExtractor


def create_mock_pdf_stream(text: str) -> io.BytesIO:
    """Helper to generate an in-memory PDF stream for testing."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, text)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


def test_clean_text():
    raw = "Hello   World!\u00a0\u00a0How\nare\n\n\n\nyou?"
    cleaned = ResumeExtractor.clean_text(raw)
    assert "Hello World!" in cleaned
    assert "\u00a0" not in cleaned
    assert "\n\n\n\n" not in cleaned


def test_extract_from_text():
    sample = """
    JANE DOE
    jane.doe@email.com | (555) 123-4567 | San Francisco, CA
    linkedin.com/in/janedoe | github.com/janedoe
    
    EXPERIENCE
    Senior Software Engineer with extensive experience building web apps.
    """
    res = ResumeExtractor.extract_from_text(sample)
    assert res["success"] is True
    assert res["word_count"] > 10
    assert "JANE DOE" in res["text"]


def test_extract_from_pdf():
    mock_pdf = create_mock_pdf_stream("John Doe Developer john.doe@test.com Python React AWS experience")
    res = ResumeExtractor.extract_from_pdf(mock_pdf)
    assert res["success"] is True
    assert "John Doe" in res["text"]
    assert res["page_count"] == 1


def test_parse_metadata():
    text = """
    Sarah Connor
    sarah.connor@cyberdyne.org
    (310) 555-0199
    linkedin.com/in/sarah-connor
    github.com/sarah-c

    EXPERIENCE
    Led resistance software architecture.

    EDUCATION
    BS in Computer Science.

    SKILLS
    Python, C++, Linux, Cryptography.
    """
    metadata = ResumeExtractor.parse_metadata(text)
    assert metadata["candidate_name"] == "Sarah Connor"
    assert metadata["email"] == "sarah.connor@cyberdyne.org"
    assert metadata["phone"] == "(310) 555-0199"
    assert "linkedin.com/in/sarah-connor" in metadata["linkedin"]
    assert "github.com/sarah-c" in metadata["github"]
    assert metadata["detected_sections"]["experience"] is True
    assert metadata["detected_sections"]["education"] is True
    assert metadata["detected_sections"]["skills"] is True
