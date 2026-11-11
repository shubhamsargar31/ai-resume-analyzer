"""
Unit tests for text extraction from PDF and DOCX resumes.
"""

import os
import unittest
from src.text_extractor import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_resume_text,
    ResumeExtractionError
)

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "sample_resumes")


class TestTextExtractor(unittest.TestCase):

    def test_extract_pdf_valid(self):
        pdf_path = os.path.join(SAMPLES_DIR, "sample_data_scientist.pdf")
        self.assertTrue(os.path.exists(pdf_path), f"Sample PDF not found at {pdf_path}")
        text, file_type = extract_resume_text(pdf_path)
        self.assertEqual(file_type, "PDF")
        self.assertIn("Python", text)
        self.assertIn("Scikit-Learn", text)
        self.assertGreater(len(text), 200)

    def test_extract_docx_valid(self):
        docx_path = os.path.join(SAMPLES_DIR, "sample_frontend_developer.docx")
        self.assertTrue(os.path.exists(docx_path), f"Sample DOCX not found at {docx_path}")
        text, file_type = extract_resume_text(docx_path)
        self.assertEqual(file_type, "DOCX")
        self.assertIn("React", text)
        self.assertIn("JavaScript", text)
        self.assertGreater(len(text), 150)

    def test_unsupported_format(self):
        with self.assertRaises(ResumeExtractionError):
            extract_resume_text("dummy_image.png")

    def test_nonexistent_file(self):
        with self.assertRaises(ResumeExtractionError):
            extract_text_from_pdf("non_existent_file.pdf")


if __name__ == "__main__":
    unittest.main()
