"""
CareerIQ - SQLite Database Manager
Persists resume analyses, user histories, job description match logs,
and platform analytics.
"""

import sqlite3
import json
import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from config import Config


class Database:
    """Manages SQLite database connections, tables, and CRUD operations."""

    @staticmethod
    def get_connection() -> sqlite3.Connection:
        """Returns a configured SQLite connection with row factories."""
        Config.init_app()
        conn = sqlite3.connect(str(Config.DATABASE_PATH))
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def init_db(cls):
        """Initializes tables with proper indexes if they do not exist."""
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            
            # Analyses table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    candidate_name TEXT DEFAULT 'Candidate',
                    email TEXT,
                    phone TEXT,
                    overall_score INTEGER NOT NULL,
                    word_count INTEGER DEFAULT 0,
                    page_count INTEGER DEFAULT 1,
                    skills_count INTEGER DEFAULT 0,
                    top_role TEXT DEFAULT 'Full Stack Engineer',
                    top_role_fit INTEGER DEFAULT 0,
                    skills_json TEXT,
                    dimensions_json TEXT,
                    role_matches_json TEXT,
                    action_plan_json TEXT,
                    raw_text_snippet TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Job comparisons table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS job_matches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    analysis_id INTEGER,
                    job_title TEXT,
                    match_score INTEGER NOT NULL,
                    matched_skills_json TEXT,
                    missing_skills_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (analysis_id) REFERENCES analyses (id) ON DELETE CASCADE
                )
            """)

            cursor.execute("CREATE INDEX IF NOT EXISTS idx_analyses_created ON analyses(created_at DESC)")
            conn.commit()

    @classmethod
    def save_analysis(cls, analysis_data: Dict[str, Any], metadata: Dict[str, Any], raw_text: str = "") -> str:
        """
        Saves an analysis record into SQLite and returns the unique session ID.
        """
        session_id = str(uuid.uuid4())[:8]
        top_role = "Full Stack Engineer"
        top_role_fit = 0

        roles = analysis_data.get("role_matches", [])
        if roles:
            top_role = roles[0].get("role", "Full Stack Engineer")
            top_role_fit = roles[0].get("fit_percentage", 0)

        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO analyses (
                    session_id, candidate_name, email, phone, overall_score,
                    word_count, page_count, skills_count, top_role, top_role_fit,
                    skills_json, dimensions_json, role_matches_json, action_plan_json,
                    raw_text_snippet
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_id,
                metadata.get("candidate_name", "Candidate"),
                metadata.get("email"),
                metadata.get("phone"),
                analysis_data.get("overall_score", 0),
                analysis_data.get("word_count", 0),
                analysis_data.get("page_count", 1),
                analysis_data.get("skills", {}).get("total_count", 0),
                top_role,
                top_role_fit,
                json.dumps(analysis_data.get("skills", {})),
                json.dumps(analysis_data.get("dimensions", {})),
                json.dumps(roles),
                json.dumps(analysis_data.get("action_plan", [])),
                raw_text[:500] if raw_text else ""
            ))
            conn.commit()

        return session_id

    @classmethod
    def get_analysis_by_session_id(cls, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a single full analysis record by session ID."""
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM analyses WHERE session_id = ?", (session_id,))
            row = cursor.fetchone()
            if not row:
                return None

            return cls._row_to_dict(row)

    @classmethod
    def get_analysis_by_id(cls, analysis_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves an analysis record by primary key."""
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM analyses WHERE id = ?", (analysis_id,))
            row = cursor.fetchone()
            if not row:
                return None

            return cls._row_to_dict(row)

    @classmethod
    def get_recent_analyses(cls, limit: int = 15) -> List[Dict[str, Any]]:
        """Returns recent analysis summaries ordered by creation date."""
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, session_id, candidate_name, email, overall_score,
                       skills_count, top_role, top_role_fit, created_at
                FROM analyses
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    @classmethod
    def get_analytics_summary(cls) -> Dict[str, Any]:
        """Calculates global platform metrics across all saved analyses."""
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*), AVG(overall_score), AVG(skills_count) FROM analyses")
            total_count, avg_score, avg_skills = cursor.fetchone()
            
            total_count = total_count or 0
            avg_score = round(avg_score, 1) if avg_score else 0
            avg_skills = round(avg_skills, 1) if avg_skills else 0

            # Count top roles
            cursor.execute("""
                SELECT top_role, COUNT(*) as count
                FROM analyses
                GROUP BY top_role
                ORDER BY count DESC
                LIMIT 5
            """)
            top_roles = [dict(r) for r in cursor.fetchall()]

            return {
                "total_analyses": total_count,
                "average_score": avg_score,
                "average_skills": avg_skills,
                "popular_roles": top_roles
            }

    @classmethod
    def delete_analysis(cls, session_id: str) -> bool:
        """Deletes an analysis and associated records."""
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM analyses WHERE session_id = ?", (session_id,))
            conn.commit()
            return cursor.rowcount > 0

    @classmethod
    def _row_to_dict(cls, row: sqlite3.Row) -> Dict[str, Any]:
        """Converts an SQLite row to a Python dict, unpacking JSON fields."""
        data = dict(row)
        for json_field in ["skills_json", "dimensions_json", "role_matches_json", "action_plan_json"]:
            if data.get(json_field):
                try:
                    data[json_field.replace("_json", "")] = json.loads(data[json_field])
                except Exception:
                    data[json_field.replace("_json", "")] = None
        return data
