"""
CareerIQ - Resume Text Extractor & Document Parser
Extracts raw text, detects sections, and parses contact metadata from PDF and plain text documents.
"""

import re
import io
from typing import Dict, Any, List, Optional
from pypdf import PdfReader


class ResumeExtractor:
    """Handles text extraction and structural decomposition from resume documents."""

    # Standard Section Headers Regex Patterns (supports leading whitespace/indentation)
    SECTION_PATTERNS = {
        "experience": re.compile(
            r"^\s*(?:work\s+experience|professional\s+experience|employment\s+history|experience|career\s+history)",
            re.IGNORECASE | re.MULTILINE
        ),
        "education": re.compile(
            r"^\s*(?:education|academic\s+background|qualifications|degrees|educational\s+history)",
            re.IGNORECASE | re.MULTILINE
        ),
        "skills": re.compile(
            r"^\s*(?:technical\s+skills|skills\s+&\s+competencies|core\s+competencies|skills|technologies|tools\s+&\s+technologies)",
            re.IGNORECASE | re.MULTILINE
        ),
        "projects": re.compile(
            r"^\s*(?:projects|personal\s+projects|key\s+projects|portfolio|technical\s+projects)",
            re.IGNORECASE | re.MULTILINE
        ),
        "certifications": re.compile(
            r"^\s*(?:certifications|licenses|courses\s+&\s+certifications|professional\s+certifications|awards)",
            re.IGNORECASE | re.MULTILINE
        ),
        "summary": re.compile(
            r"^\s*(?:professional\s+summary|executive\s+summary|summary|profile|about\s+me|objective)",
            re.IGNORECASE | re.MULTILINE
        )
    }

    # Contact info patterns
    EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    PHONE_PATTERN = re.compile(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")
    LINKEDIN_PATTERN = re.compile(r"linkedin\.com/in/[a-zA-Z0-9_-]+", re.IGNORECASE)
    GITHUB_PATTERN = re.compile(r"github\.com/[a-zA-Z0-9_-]+", re.IGNORECASE)

    @classmethod
    def extract_from_pdf(cls, file_stream_or_path) -> Dict[str, Any]:
        """
        Extracts text and page metadata from a PDF file.
        Accepts a file path string or a binary file-like stream.
        """
        try:
            reader = PdfReader(file_stream_or_path)
            num_pages = len(reader.pages)
            
            if num_pages == 0:
                return {
                    "success": False,
                    "error": "The uploaded PDF document contains 0 pages.",
                    "text": "",
                    "page_count": 0
                }

            page_texts = []
            for i, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                page_texts.append(text)

            full_text = "\n\n".join(page_texts)
            cleaned_text = cls.clean_text(full_text)

            # Check if extracted text is too short (likely scanned image without OCR)
            if len(cleaned_text.strip()) < 50:
                return {
                    "success": False,
                    "error": "Very little or no readable text found. This may be a scanned image-based PDF. Please upload a text-searchable PDF.",
                    "text": cleaned_text,
                    "page_count": num_pages
                }

            return {
                "success": True,
                "text": cleaned_text,
                "raw_text": full_text,
                "page_count": num_pages,
                "char_count": len(cleaned_text),
                "word_count": len(cleaned_text.split())
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to parse PDF document: {str(e)}",
                "text": "",
                "page_count": 0
            }

    @classmethod
    def extract_from_text(cls, raw_text: str) -> Dict[str, Any]:
        """Processes plain text resume content."""
        cleaned_text = cls.clean_text(raw_text or "")
        if len(cleaned_text.strip()) < 30:
            return {
                "success": False,
                "error": "The provided text is too short for a meaningful resume analysis.",
                "text": cleaned_text,
                "page_count": 1
            }

        return {
            "success": True,
            "text": cleaned_text,
            "raw_text": raw_text,
            "page_count": max(1, len(cleaned_text.split()) // 350),
            "char_count": len(cleaned_text),
            "word_count": len(cleaned_text.split())
        }

    @staticmethod
    def clean_text(text: str) -> str:
        """Cleans and standardizes extracted text formatting."""
        # Replace non-breaking spaces and exotic whitespace
        text = text.replace("\u00a0", " ").replace("\u200b", "")
        # Standardize quotes and dashes
        text = text.replace("“", '"').replace("”", '"').replace("’", "'").replace("–", "-").replace("—", "-")
        # Remove null bytes
        text = text.replace("\x00", "")
        # Normalize multiple spaces per line
        text = re.sub(r"[ \t]+", " ", text)
        # Collapse multiple empty lines to max 2
        text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
        return text.strip()

    @classmethod
    def parse_metadata(cls, text: str) -> Dict[str, Any]:
        """Extracts candidate contact details and identified sections."""
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        
        # Estimate candidate name (usually first non-empty line under 50 chars without email/numbers)
        candidate_name = "Candidate"
        for line in lines[:5]:
            if (len(line) < 40 and 
                not cls.EMAIL_PATTERN.search(line) and 
                not cls.PHONE_PATTERN.search(line) and 
                not re.search(r"\d", line) and
                not any(word in line.lower() for word in ["resume", "curriculum", "cv", "page"])):
                candidate_name = line.title()
                break

        # Contact items
        emails = cls.EMAIL_PATTERN.findall(text)
        phones = cls.PHONE_PATTERN.findall(text)
        linkedin = cls.LINKEDIN_PATTERN.findall(text)
        github = cls.GITHUB_PATTERN.findall(text)

        # Detect sections
        detected_sections = {}
        for section_name, pattern in cls.SECTION_PATTERNS.items():
            match = pattern.search(text)
            detected_sections[section_name] = bool(match)

        return {
            "candidate_name": candidate_name,
            "email": emails[0] if emails else None,
            "phone": phones[0] if phones else None,
            "linkedin": f"https://{linkedin[0]}" if linkedin else None,
            "github": f"https://{github[0]}" if github else None,
            "detected_sections": detected_sections
        }
