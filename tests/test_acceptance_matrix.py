"""
Acceptance Test Matrix: Evaluates all 5 sample resumes against all 10 job roles.
Verifies skill preservation (C++, C#, .NET), TF-IDF bounds, ranking accuracy, and error handling.
"""

import os
import unittest
import numpy as np

from src.text_extractor import extract_resume_text, ResumeExtractionError
from src.text_cleaner import clean_text, clean_for_vectorization, extract_sections, sanitize_protected_data
from src.skill_extractor import SkillExtractor
from src.profile_extractor import extract_full_profile
from src.job_matcher import JobMatcher
from src.recommender import JobRecommender
from src.roadmap_generator import RoadmapGenerator

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SAMPLES_DIR = os.path.join(ROOT_DIR, "sample_resumes")


class TestAcceptanceMatrix(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.skill_extractor = SkillExtractor()
        cls.job_matcher = JobMatcher()
        cls.recommender = JobRecommender(cls.job_matcher)
        cls.roadmap_gen = RoadmapGenerator(cls.skill_extractor)

    def test_sample_1_data_scientist_pdf(self):
        filepath = os.path.join(SAMPLES_DIR, "sample_data_scientist.pdf")
        text, ftype = extract_resume_text(filepath)
        self.assertEqual(ftype, "PDF")
        
        cleaned = clean_text(text)
        skill_res = self.skill_extractor.extract_skills(cleaned)
        detected = skill_res["detected_skills"]
        
        # Check expected skills
        for s in ["Python", "SQL", "Pandas", "NumPy", "Scikit-Learn"]:
            self.assertIn(s, detected, f"Expected {s} in detected skills")
            
        rec = self.recommender.recommend_top_roles(cleaned, detected, top_n=3)
        self.assertEqual(rec["total_roles_evaluated"], 10, "Must evaluate all 10 job roles")
        top_roles = rec["top_recommendations"]
        self.assertEqual(len(top_roles), 3)
        self.assertEqual(top_roles[0]["role_title"], "Data Scientist")
        self.assertGreaterEqual(top_roles[0]["match_score"], 75.0)

    def test_sample_2_full_stack_dev_pdf(self):
        filepath = os.path.join(SAMPLES_DIR, "sample_full_stack_dev.pdf")
        text, ftype = extract_resume_text(filepath)
        self.assertEqual(ftype, "PDF")
        
        cleaned = clean_text(text)
        skill_res = self.skill_extractor.extract_skills(cleaned)
        detected = skill_res["detected_skills"]
        
        for s in ["JavaScript", "TypeScript", "React", "Node.js", "Express.js", "SQL", "Git"]:
            self.assertIn(s, detected, f"Expected {s} in detected skills")
            
        rec = self.recommender.recommend_top_roles(cleaned, detected, top_n=3)
        self.assertEqual(rec["total_roles_evaluated"], 10)
        self.assertEqual(rec["top_recommendations"][0]["role_title"], "Full Stack Developer")

    def test_sample_3_devops_engineer_pdf(self):
        filepath = os.path.join(SAMPLES_DIR, "sample_devops_engineer.pdf")
        text, ftype = extract_resume_text(filepath)
        self.assertEqual(ftype, "PDF")
        
        cleaned = clean_text(text)
        skill_res = self.skill_extractor.extract_skills(cleaned)
        detected = skill_res["detected_skills"]
        
        for s in ["Docker", "Kubernetes", "AWS", "Terraform", "Linux", "CI/CD"]:
            self.assertIn(s, detected, f"Expected {s} in detected skills")
            
        rec = self.recommender.recommend_top_roles(cleaned, detected, top_n=3)
        self.assertEqual(rec["total_roles_evaluated"], 10)
        self.assertEqual(rec["top_recommendations"][0]["role_title"], "DevOps Engineer")

    def test_sample_4_frontend_developer_docx(self):
        filepath = os.path.join(SAMPLES_DIR, "sample_frontend_developer.docx")
        text, ftype = extract_resume_text(filepath)
        self.assertEqual(ftype, "DOCX")
        
        cleaned = clean_text(text)
        skill_res = self.skill_extractor.extract_skills(cleaned)
        detected = skill_res["detected_skills"]
        
        for s in ["JavaScript", "TypeScript", "React", "HTML/CSS", "Tailwind CSS", "Git"]:
            self.assertIn(s, detected, f"Expected {s} in detected skills")
            
        rec = self.recommender.recommend_top_roles(cleaned, detected, top_n=3)
        self.assertEqual(rec["total_roles_evaluated"], 10)
        self.assertEqual(rec["top_recommendations"][0]["role_title"], "Frontend Developer")

    def test_sample_5_data_analyst_docx(self):
        filepath = os.path.join(SAMPLES_DIR, "sample_data_analyst.docx")
        text, ftype = extract_resume_text(filepath)
        self.assertEqual(ftype, "DOCX")
        
        cleaned = clean_text(text)
        skill_res = self.skill_extractor.extract_skills(cleaned)
        detected = skill_res["detected_skills"]
        
        for s in ["SQL", "Python", "Pandas", "Data Visualization", "Statistics & Probability"]:
            self.assertIn(s, detected, f"Expected {s} in detected skills")
            
        rec = self.recommender.recommend_top_roles(cleaned, detected, top_n=3)
        self.assertEqual(rec["total_roles_evaluated"], 10)
        self.assertEqual(rec["top_recommendations"][0]["role_title"], "Data Analyst")

    def test_special_technical_symbols_preservation(self):
        """Verifies C++, C#, and .NET are not stripped or mangled during cleaning."""
        raw = "Proficient in C++, C#, .NET, Node.js, and CI/CD pipelines."
        vec = clean_for_vectorization(raw)
        self.assertIn("c++", vec)
        self.assertIn("c#", vec)
        self.assertIn(".net", vec)
        self.assertIn("node.js", vec)
        self.assertIn("ci/cd", vec)

        skill_res = self.skill_extractor.extract_skills(raw)
        detected = skill_res["detected_skills"]
        self.assertIn("C++", detected)
        self.assertIn("C#", detected)
        self.assertIn("Node.js", detected)
        self.assertIn("CI/CD", detected)

    def test_invalid_file_handling(self):
        with self.assertRaises(ResumeExtractionError):
            extract_resume_text("test_corrupt.xyz")

    def test_all_10_roles_loaded(self):
        roles_df = self.job_matcher.roles_df
        self.assertEqual(len(roles_df), 10, "System must maintain all 10 benchmark job roles")


if __name__ == "__main__":
    unittest.main()
