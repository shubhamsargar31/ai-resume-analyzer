"""
Unit tests for text cleaning, section extraction, and anti-bias filtering.
"""

import unittest
from src.text_cleaner import (
    clean_text,
    clean_for_vectorization,
    extract_sections,
    extract_contact_info,
    sanitize_protected_data
)


class TestTextCleaner(unittest.TestCase):

    def test_clean_text_bullets_and_unicode(self):
        raw = "• Python programming\n\u2022 Machine Learning \u2013 Models\n\n\n\n- Data Science"
        cleaned = clean_text(raw)
        self.assertIn("- Python programming", cleaned)
        self.assertIn("- Machine Learning - Models", cleaned)

    def test_clean_for_vectorization(self):
        raw = "Contact me at user@test.com or +1 (555) 123-4567. Experience with C++, Node.js, and CI/CD."
        vec_text = clean_for_vectorization(raw)
        self.assertNotIn("user@test.com", vec_text)
        self.assertNotIn("555", vec_text)
        self.assertIn("c++", vec_text)
        self.assertIn("node.js", vec_text)
        self.assertIn("ci/cd", vec_text)

    def test_extract_sections(self):
        sample_doc = (
            "John Doe\n\n"
            "EDUCATION\n"
            "B.Tech in Computer Science, 2023\n\n"
            "TECHNICAL SKILLS\n"
            "Python, Django, PostgreSQL, Docker\n\n"
            "EXPERIENCE\n"
            "Software Developer at Tech Inc (2023 - Present)\n\n"
            "PROJECTS\n"
            "E-Commerce App | Built full-stack store\n"
        )
        sections = extract_sections(sample_doc)
        self.assertIn("Computer Science", sections["education"])
        self.assertIn("Django", sections["skills"])
        self.assertIn("Tech Inc", sections["experience"])
        self.assertIn("E-Commerce", sections["projects"])

    def test_extract_contact_info(self):
        text = "Reach out at dev@example.com or linkedin.com/in/alex-sample and github.com/alex-sample."
        contact = extract_contact_info(text)
        self.assertEqual(contact["email"], "dev@example.com")
        self.assertIn("linkedin.com/in/alex-sample", contact["linkedin"])
        self.assertIn("github.com/alex-sample", contact["github"])

    def test_sanitize_protected_data(self):
        text = "Personal details: Gender: Male, Marital Status: Single, Religion: Secular."
        sanitized = sanitize_protected_data(text)
        self.assertNotIn("Male", sanitized)
        self.assertNotIn("Single", sanitized)
        self.assertIn("[REDACTED]", sanitized)


if __name__ == "__main__":
    unittest.main()
