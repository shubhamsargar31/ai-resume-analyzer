"""
Unit tests for JobMatcher, Recommender, and RoadmapGenerator.
"""

import unittest
from src.job_matcher import JobMatcher
from src.recommender import JobRecommender
from src.roadmap_generator import RoadmapGenerator


class TestJobMatcherAndRecommender(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.matcher = JobMatcher()
        cls.recommender = JobRecommender(cls.matcher)
        cls.roadmap_gen = RoadmapGenerator()

    def test_job_matcher_data_scientist(self):
        resume_text = (
            "Data Scientist with hands-on experience in Python, SQL, Pandas, NumPy, Scikit-Learn, "
            "Statistics & Probability, and Data Visualization. Built predictive ML models and pipelines."
        )
        detected_skills = ["Python", "SQL", "Pandas", "NumPy", "Scikit-Learn", "Statistics & Probability", "Data Visualization"]
        
        matches = self.matcher.match_all_roles(resume_text, detected_skills)
        self.assertGreaterEqual(len(matches), 5, "Should evaluate at least 5 job roles")
        
        top_match = matches[0]
        self.assertEqual(top_match["role_title"], "Data Scientist")
        self.assertGreaterEqual(top_match["match_score"], 75.0)
        self.assertEqual(len(top_match["missing_skills"]), 0)

    def test_recommender_top_3(self):
        resume_text = (
            "Full Stack Developer proficient in JavaScript, TypeScript, React, Node.js, Express.js, HTML/CSS, SQL, Git."
        )
        detected_skills = ["JavaScript", "TypeScript", "React", "Node.js", "Express.js", "HTML/CSS", "SQL", "Git"]
        
        rec = self.recommender.recommend_top_roles(resume_text, detected_skills, top_n=3)
        top_3 = rec["top_recommendations"]
        self.assertEqual(len(top_3), 3)
        self.assertEqual(top_3[0]["role_title"], "Full Stack Developer")
        self.assertIn(top_3[1]["role_title"], ["Frontend Developer", "Backend Developer"])

    def test_roadmap_generation(self):
        # Suppose candidate wants DevOps Engineer but lacks Terraform and Kubernetes
        target_role = {
            "role_title": "DevOps Engineer",
            "matched_skills": ["Linux", "Docker", "AWS", "Git"],
            "missing_skills": ["Kubernetes", "Terraform", "CI/CD"]
        }
        roadmap = self.roadmap_gen.generate_roadmap(target_role, ["Linux", "Docker", "AWS", "Git"])
        self.assertEqual(roadmap["target_role"], "DevOps Engineer")
        self.assertEqual(len(roadmap["phases"]), 3)
        self.assertGreater(roadmap["total_estimated_hours"], 0)
        self.assertGreater(len(roadmap["capstone_projects"]), 0)


if __name__ == "__main__":
    unittest.main()
