"""
Unit tests for skill extraction engine and alias resolution.
"""

import unittest
from src.skill_extractor import SkillExtractor


class TestSkillExtractor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.extractor = SkillExtractor()

    def test_dictionary_loading(self):
        skills = self.extractor.get_all_skills()
        self.assertGreaterEqual(len(skills), 20, "Should have at least 20 skills in database")
        self.assertIn("Python", skills)
        self.assertIn("Docker", skills)
        self.assertIn("SQL", skills)

    def test_skill_extraction_and_aliases(self):
        text = "Experienced in python3, sklearn, postgresql, and containerization using docker."
        res = self.extractor.extract_skills(text)
        detected = res["detected_skills"]
        self.assertIn("Python", detected)
        self.assertIn("Scikit-Learn", detected)
        self.assertIn("PostgreSQL", detected)
        self.assertIn("Docker", detected)

    def test_multi_word_skill_extraction(self):
        text = "Deep understanding of natural language processing and computer vision."
        res = self.extractor.extract_skills(text)
        detected = res["detected_skills"]
        self.assertIn("Natural Language Processing", detected)
        self.assertIn("Computer Vision", detected)

    def test_word_boundary_isolation(self):
        # "Go" should not trigger on "Good morning" or "Going"
        text = "Good morning, I am going to write software."
        res = self.extractor.extract_skills(text)
        self.assertNotIn("Go", res["detected_skills"])

        # Actual "Go" language usage
        text_go = "Engineered services in Go and Python."
        res_go = self.extractor.extract_skills(text_go)
        self.assertIn("Go", res_go["detected_skills"])


if __name__ == "__main__":
    unittest.main()
