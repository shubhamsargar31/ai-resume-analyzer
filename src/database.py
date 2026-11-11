"""
SQLite Database Module.
Manages session logs, anonymous analytics, and custom job roles storage.
Guarantees privacy by never storing resume text or PII.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "resume_analyzer.db")


class DatabaseManager:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or DEFAULT_DB_PATH
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Anonymous Analysis Log (No resume text or PII stored)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analysis_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    file_name TEXT,
                    file_type TEXT,
                    detected_skills_count INTEGER,
                    top_recommended_role TEXT,
                    top_match_score REAL,
                    top_skill_coverage REAL
                )
            """)

            # Custom / Community Job Roles
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS custom_job_roles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role_title TEXT NOT NULL UNIQUE,
                    category TEXT NOT NULL,
                    description TEXT,
                    required_skills TEXT NOT NULL,
                    preferred_skills TEXT,
                    experience_level TEXT,
                    avg_salary TEXT,
                    created_at TEXT
                )
            """)

            # User Feedback
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    rating INTEGER,
                    comment TEXT,
                    helpful INTEGER
                )
            """)
            conn.commit()

    def log_analysis(
        self,
        file_name: str,
        file_type: str,
        detected_skills_count: int,
        top_role: str,
        match_score: float,
        skill_coverage: float
    ) -> int:
        """Logs an anonymized analysis session."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO analysis_history 
                (timestamp, file_name, file_type, detected_skills_count, top_recommended_role, top_match_score, top_skill_coverage)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                os.path.basename(file_name) if file_name else "uploaded_resume",
                file_type,
                detected_skills_count,
                top_role,
                match_score,
                skill_coverage
            ))
            conn.commit()
            return cursor.lastrowid

    def get_recent_analyses(self, limit: int = 15) -> List[Dict[str, Any]]:
        """Fetches recent analysis records."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM analysis_history ORDER BY id DESC LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def save_feedback(self, rating: int, comment: str, helpful: bool = True) -> int:
        """Saves user feedback."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO feedback (timestamp, rating, comment, helpful)
                VALUES (?, ?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                rating,
                comment,
                1 if helpful else 0
            ))
            conn.commit()
            return cursor.lastrowid
