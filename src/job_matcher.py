"""
Job Matching Engine.
Calculates resume-to-job matching scores using TF-IDF vectorization, cosine similarity,
and direct skill coverage analysis.
"""

import os
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.text_cleaner import clean_for_vectorization

DEFAULT_JOB_ROLES_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "job_roles.csv")


class JobMatcher:
    def __init__(self, job_roles_path: Optional[str] = None):
        self.job_roles_path = job_roles_path or DEFAULT_JOB_ROLES_CSV
        self.roles_df = pd.DataFrame()
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            sublinear_tf=True,
            token_pattern=r"(?u)\S+",
            max_features=2500
        )
        self.role_corpus = []
        self.role_tfidf_matrix = None
        self._load_roles()

    def _load_roles(self):
        """Loads job roles and fits TF-IDF vectorizer on job descriptions and requirements."""
        if not os.path.exists(self.job_roles_path):
            raise FileNotFoundError(f"Job roles CSV not found at {self.job_roles_path}")

        self.roles_df = pd.read_csv(self.job_roles_path)

        # Build comprehensive textual corpus for each job role
        self.role_corpus = []
        for _, row in self.roles_df.iterrows():
            title = str(row.get("role_title", ""))
            category = str(row.get("category", ""))
            desc = str(row.get("description", ""))
            req_skills = str(row.get("required_skills", "")).replace(",", " ")
            pref_skills = str(row.get("preferred_skills", "")).replace(",", " ")
            resp = str(row.get("key_responsibilities", ""))

            # Repetition of required skills adds appropriate TF-IDF weight
            combined_text = f"{title} {category} {desc} {req_skills} {req_skills} {pref_skills} {resp}"
            cleaned_job_text = clean_for_vectorization(combined_text)
            self.role_corpus.append(cleaned_job_text)

        if self.role_corpus:
            self.role_tfidf_matrix = self.vectorizer.fit_transform(self.role_corpus)

    def calculate_match_for_role(
        self,
        resume_text: str,
        detected_skills: List[str],
        role_row: pd.Series,
        role_index: int
    ) -> Dict[str, Any]:
        """
        Calculates comprehensive matching analytics between a resume and a specific job role.
        """
        role_title = str(role_row.get("role_title", "Unknown Role"))
        role_category = str(role_row.get("category", "General"))
        
        # Parse required and preferred skills
        raw_req = str(role_row.get("required_skills", ""))
        required_skills = [s.strip() for s in raw_req.split(",") if s.strip()]
        
        raw_pref = str(role_row.get("preferred_skills", ""))
        preferred_skills = [s.strip() for s in raw_pref.split(",") if s.strip()]

        # Set calculations for skill coverage
        candidate_skills_set = set(detected_skills)
        req_set = set(required_skills)
        pref_set = set(preferred_skills)

        matched_skills = sorted(list(candidate_skills_set.intersection(req_set)))
        missing_skills = sorted(list(req_set.difference(candidate_skills_set)))
        matched_preferred = sorted(list(candidate_skills_set.intersection(pref_set)))

        # 1. Skill Overlap Percentage
        total_req_count = max(1, len(required_skills))
        skill_coverage_pct = round((len(matched_skills) / total_req_count) * 100, 1)

        # 2. Preferred Skill Bonus (up to 10 points)
        total_pref_count = max(1, len(preferred_skills))
        pref_bonus_pct = round((len(matched_preferred) / total_pref_count) * 10, 1)

        # 3. TF-IDF Cosine Similarity
        cleaned_resume = clean_for_vectorization(resume_text)
        cosine_sim = 0.0
        
        if cleaned_resume and self.role_tfidf_matrix is not None:
            try:
                resume_tfidf = self.vectorizer.transform([cleaned_resume])
                role_vector = self.role_tfidf_matrix[role_index]
                sim_matrix = cosine_similarity(resume_tfidf, role_vector)
                cosine_sim = float(sim_matrix[0][0])
            except Exception:
                cosine_sim = 0.0

        cosine_sim_pct = round(cosine_sim * 100, 1)

        # 4. Weighted Hybrid Match Score
        # 60% direct required skill coverage + 30% semantic TF-IDF context + 10% preferred bonus
        hybrid_score = (0.60 * skill_coverage_pct) + (0.30 * cosine_sim_pct) + pref_bonus_pct
        hybrid_score = min(100.0, max(0.0, round(hybrid_score, 1)))

        # Status badge / Match tier
        if hybrid_score >= 75:
            match_tier = "Excellent Match"
            tier_color = "green"
        elif hybrid_score >= 55:
            match_tier = "Good Match"
            tier_color = "blue"
        elif hybrid_score >= 35:
            match_tier = "Moderate Match"
            tier_color = "orange"
        else:
            match_tier = "Low Match / Pivot Needed"
            tier_color = "red"

        return {
            "role_id": int(role_row.get("role_id", role_index + 1)),
            "role_title": role_title,
            "category": role_category,
            "description": str(role_row.get("description", "")),
            "match_score": hybrid_score,
            "match_tier": match_tier,
            "tier_color": tier_color,
            "cosine_similarity": cosine_sim,
            "cosine_similarity_pct": cosine_sim_pct,
            "skill_coverage_pct": skill_coverage_pct,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "preferred_skills": preferred_skills,
            "matched_preferred": matched_preferred,
            "required_skills_count": len(required_skills),
            "matched_skills_count": len(matched_skills),
            "missing_skills_count": len(missing_skills),
            "experience_level": str(role_row.get("experience_level", "")),
            "min_education": str(role_row.get("min_education", "")),
            "avg_salary": str(role_row.get("avg_salary", "Market Rate")),
            "key_responsibilities": str(role_row.get("key_responsibilities", ""))
        }

    def match_all_roles(self, resume_text: str, detected_skills: List[str]) -> List[Dict[str, Any]]:
        """
        Evaluates resume against all roles in database and sorts by match_score descending.
        """
        results = []
        for idx, row in self.roles_df.iterrows():
            result = self.calculate_match_for_role(resume_text, detected_skills, row, idx)
            results.append(result)

        # Sort by match score descending, then by skill coverage
        results.sort(key=lambda x: (x["match_score"], x["skill_coverage_pct"]), reverse=True)
        return results

    def get_role_by_id(self, role_id: int) -> Optional[pd.Series]:
        """Fetches role row by ID."""
        matches = self.roles_df[self.roles_df["role_id"] == role_id]
        if not matches.empty:
            return matches.iloc[0]
        return None
