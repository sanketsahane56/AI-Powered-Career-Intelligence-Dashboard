"""
CareerIQ - Application Configuration
"""
import os
from pathlib import Path

# Base directory of the application
BASE_DIR = Path(__file__).resolve().parent

class Config:
    BASE_DIR = BASE_DIR
    # Flask settings
    SECRET_KEY = os.environ.get("SECRET_KEY", "careeriq-dev-secret-key-2026-safe")
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    
    # Upload and report storage
    UPLOAD_FOLDER = BASE_DIR / os.environ.get("UPLOAD_FOLDER", "uploads")
    REPORTS_FOLDER = BASE_DIR / os.environ.get("REPORTS_FOLDER", "reports")
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH", 10 * 1024 * 1024))  # 10 MB limit
    ALLOWED_EXTENSIONS = {"pdf", "txt"}
    
    # Database
    DATABASE_PATH = BASE_DIR / os.environ.get("DATABASE_PATH", "data/careeriq.db")
    
    # Server configuration
    PORT = int(os.environ.get("PORT", 5000))
    HOST = os.environ.get("HOST", "0.0.0.0")

    @classmethod
    def init_app(cls):
        """Ensure all required runtime directories exist."""
        cls.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
        cls.REPORTS_FOLDER.mkdir(parents=True, exist_ok=True)
        cls.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
