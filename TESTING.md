# 🧪 Acceptance Testing & Verification Report

**Project Title:** AI Resume Analyzer and Job Recommendation System  
**Test Suite Status:** ✅ 25 / 25 Test Cases Passing (100% Pass Rate)  
**Execution Runtime:** ~0.37 seconds  
**Test Harness:** Python `unittest` framework  

---

## 📋 1. Test Suite Summary

| Module | Test Suite File | Test Cases | Status | Focus Area |
| :--- | :--- | :---: | :---: | :--- |
| **Acceptance Matrix** | `tests/test_acceptance_matrix.py` | 8 | `PASSED` | 5 sample resumes across 10 roles, symbol safety (`C++`, `C#`, `.NET`), error handling |
| **Text Extraction** | `tests/test_extractor.py` | 4 | `PASSED` | PDF/DOCX parsing, empty files, unsupported types |
| **Text Cleaning & Privacy** | `tests/test_cleaner.py` | 5 | `PASSED` | Unicode bullets, regex segmentation, anti-bias filter |
| **Skill Extraction** | `tests/test_skills.py` | 4 | `PASSED` | 60 skills, alias resolution, word boundaries |
| **Job Matching & Ranking** | `tests/test_matcher.py` | 3 | `PASSED` | TF-IDF, Cosine Similarity, Top 3 ranking, roadmap |
| **Report Generation** | `tests/test_report.py` | 1 | `PASSED` | ReportLab PDF compilation, Markdown structure |
| **Total** | | **25** | **100%** | |

---

## 🔬 2. Acceptance Matrix Specifications & Results (`tests/test_acceptance_matrix.py`)

| Test ID | Test Method | Input Specification | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `TC-ACC-01` | `test_sample_1_data_scientist_pdf` | `sample_data_scientist.pdf` | Ranked #1 for Data Scientist; score >= 75%; evaluates all 10 roles | #1 Data Scientist (78.7%), 10 roles evaluated | **PASS** |
| `TC-ACC-02` | `test_sample_2_full_stack_dev_pdf` | `sample_full_stack_dev.pdf` | Ranked #1 for Full Stack Developer; evaluates all 10 roles | #1 Full Stack Dev (84.5%), 10 roles evaluated | **PASS** |
| `TC-ACC-03` | `test_sample_3_devops_engineer_pdf` | `sample_devops_engineer.pdf` | Ranked #1 for DevOps Engineer; evaluates all 10 roles | #1 DevOps Engineer (83.0%), 10 roles evaluated | **PASS** |
| `TC-ACC-04` | `test_sample_4_frontend_developer_docx` | `sample_frontend_developer.docx` | DOCX parsed; Ranked #1 for Frontend Developer | #1 Frontend Dev (79.0%), 10 roles evaluated | **PASS** |
| `TC-ACC-05` | `test_sample_5_data_analyst_docx` | `sample_data_analyst.docx` | DOCX parsed; Ranked #1 for Data Analyst | #1 Data Analyst (82.1%), 10 roles evaluated | **PASS** |
| `TC-ACC-06` | `test_special_technical_symbols_preservation` | String containing `C++`, `C#`, `.NET`, `Node.js`, `CI/CD` | Tokens preserved without mangling; detected as distinct skills | All 5 symbols preserved & detected | **PASS** |
| `TC-ACC-07` | `test_invalid_file_handling` | Invalid format `test_corrupt.xyz` | Raises `ResumeExtractionError` cleanly | Caught exception gracefully | **PASS** |
| `TC-ACC-08` | `test_all_10_roles_loaded` | Load `data/job_roles.csv` | Exactly 10 enterprise roles loaded | Exactly 10 loaded | **PASS** |

---

## 🔬 3. Core Unit Test Specifications

### Suite B: File Extraction (`tests/test_extractor.py`)

| Test ID | Test Method | Input Specification | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `TC-EXT-01` | `test_extract_pdf_valid` | Standard multi-page PDF (`sample_data_scientist.pdf`) | Text extracted with >200 chars, contains "Python" | Extracted successfully | **PASS** |
| `TC-EXT-02` | `test_extract_docx_valid` | Standard Microsoft Word DOCX (`sample_frontend_developer.docx`) | Paragraphs & tables parsed, contains "React" | Extracted successfully | **PASS** |
| `TC-EXT-03` | `test_unsupported_format` | Image file `dummy_image.png` | Raises `ResumeExtractionError` with helpful message | Error caught cleanly | **PASS** |
| `TC-EXT-04` | `test_nonexistent_file` | Missing path `non_existent_file.pdf` | Raises `ResumeExtractionError` gracefully | Error caught cleanly | **PASS** |

---

### Suite C: Text Cleaning & Privacy Sanitization (`tests/test_cleaner.py`)

| Test ID | Test Method | Input Specification | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `TC-CLN-01` | `test_clean_text_bullets_and_unicode` | Text with `\u2022`, bullet points, and uneven spacing | Normalized dashes, clean whitespace | Perfectly normalized | **PASS** |
| `TC-CLN-02` | `test_clean_for_vectorization` | String containing email, phone, `C++`, `Node.js`, `CI/CD` | Strip PII, preserve technical tags (`c++`, `node.js`, `ci/cd`) | PII stripped, tags intact | **PASS** |
| `TC-CLN-03` | `test_extract_sections` | Raw resume text with standard headers | Dict segmented into `education`, `skills`, `experience`, `projects` | Accurate segmentation | **PASS** |
| `TC-CLN-04` | `test_extract_contact_info` | Text with email, LinkedIn, and GitHub links | Presentation handles extracted safely | Accurately extracted | **PASS** |
| `TC-CLN-05` | `test_sanitize_protected_data` | Text with "Gender: Male, Marital Status: Single, Age: 25" | Replaces demographic attributes with `[REDACTED]` | Sanitized strictly | **PASS** |

---

### Suite D: Skill Extraction Engine (`tests/test_skills.py`)

| Test ID | Test Method | Input Specification | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `TC-SKL-01` | `test_dictionary_loading` | Load `data/skill_dictionary.csv` | Loaded >=20 skills; contains "Python", "Docker", "SQL" | 60 skills loaded | **PASS** |
| `TC-SKL-02` | `test_skill_extraction_and_aliases` | Text: "python3, sklearn, postgresql, containerization" | Maps to canonical "Python", "Scikit-Learn", "PostgreSQL", "Docker" | Correctly mapped | **PASS** |
| `TC-SKL-03` | `test_multi_word_skill_extraction` | Text: "natural language processing and computer vision" | Multi-word phrases identified as single skills | Both detected | **PASS** |
| `TC-SKL-04` | `test_word_boundary_isolation` | "Good morning, I am going to write software." | Does NOT match "Go"; only matches when standalone language | No false positive | **PASS** |

---

### Suite E: Matching & Recommendations (`tests/test_matcher.py`)

| Test ID | Test Method | Input Specification | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `TC-MCH-01` | `test_job_matcher_data_scientist` | Candidate with Python, SQL, Pandas, NumPy, Scikit-Learn | Ranks "Data Scientist" #1 with score >= 75% | Ranked #1 (78.7%) | **PASS** |
| `TC-MCH-02` | `test_recommender_top_3` | Full Stack candidate with React, Node, Express, SQL | Top 3 recommendations produced; #1 is Full Stack Developer | Top 3 returned | **PASS** |
| `TC-MCH-03` | `test_roadmap_generation` | DevOps candidate lacking Kubernetes, Terraform | 3-phase roadmap generated with estimated study hours > 0 | Phases & courses ready | **PASS** |

---

### Suite F: Report Generation (`tests/test_report.py`)

| Test ID | Test Method | Input Specification | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `TC-RPT-01` | `test_end_to_end_report_generation` | Full analysis payload from `sample_data_scientist.pdf` | Valid `%PDF` binary >1000 bytes and valid Markdown string | PDF: 18.2 KB, MD: 3.4 KB | **PASS** |

---

## 🎯 4. How to Execute the Full Test Suite

Run the following command from the root directory:

```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run all 25 automated tests with verbose reporting
python -m unittest discover tests -v
```
