# 📖 Technical Documentation & Technologies Achieved

**Project Name:** AI Resume Analyzer and Job Recommendation System  
**Version:** 1.0.0  
**Target Architecture:** Cross-Platform (Windows, Linux, macOS)  

---

## 🛠️ Technical Competencies & Technologies Achieved

This project represents comprehensive mastery over end-to-end software engineering, applied artificial intelligence, natural language processing, and interactive data visualization.

### 1. Natural Language Processing (NLP) & Information Retrieval
- **TF-IDF Vector Space Modeling:** Implementation of `TfidfVectorizer` from `scikit-learn` configured with sublinear term-frequency scaling (`sublinear_tf=True`) to prevent keyword stuffing while prioritizing discriminative industry terms.
- **Cosine Distance & Similarity Metrics:** Computation of normalized dot products between multi-dimensional document vectors (`cosine_similarity`) to assess semantic context.
- **N-Gram Tokenization & Custom Token Patterns:** Configured custom token regex patterns (`r"(?u)\S+"`) to preserve specialized programming syntax such as `C++`, `C#`, `.NET`, `CI/CD`, and `Node.js` that standard word boundary tokenizers truncate.
- **Boundary-Protected Multi-Word Matching:** Regex engine leveraging lookaheads and boundary assertions to match multi-word phrases (e.g., "Natural Language Processing", "Computer Vision") before individual token matches, eliminating substring false positives (e.g., preventing "Go" from matching "Good").

### 2. File Stream Processing & Data Security
- **Multi-Format Ingestion:** Programmatic reading of binary streams (`io.BytesIO`) using `pypdf` for Portable Document Format files and `python-docx` for OpenXML Word documents.
- **Zero-Disk Retention Architecture:** Files are processed entirely in volatile memory and never persisted to permanent disk storage, ensuring candidate confidentiality under GDPR and privacy best practices.
- **Demographic Bias Scrubbing:** Active regex sanitization stripping gender pronouns, age, marital status, nationality, and religious identifiers prior to feature vectorization.

### 3. Modular Object-Oriented Software Design
- **Separation of Concerns:** Clean architecture cleanly decoupling input extraction (`text_extractor.py`), normalization (`text_cleaner.py`), feature detection (`skill_extractor.py`), matching algorithms (`job_matcher.py`), business recommendations (`recommender.py`), upskilling synthesis (`roadmap_generator.py`), and document reporting (`report_generator.py`).
- **Comprehensive Unit & Acceptance Testing:** 25 test cases with automated discovery via Python's standard `unittest` framework, validating parsing accuracy, boundary conditions, acceptance matrix, and error recovery.

### 4. Interactive Web Application & Data Visualization
- **Streamlit Framework:** Dynamic multi-page reactive dashboard with cached resource singletons (`@st.cache_resource`) for sub-second page transitions.
- **Plotly Visualizations:** Interactive gauge indicators, stacked component attribution charts, and horizontal ranking bars with responsive tooltips.
- **Modern Responsive CSS:** Glassmorphism cards, color-coded pill badges, and mobile-friendly layouts.

### 5. Document Automation & Database Integration
- **Programmatic PDF Compilation:** Assembling styled vector PDFs using ReportLab (`SimpleDocTemplate`, `Table`, `TableStyle`, `ParagraphStyle`), implementing dynamic headers, tables, and compliance statements.
- **Relational Persistence:** SQLite3 database management (`src/database.py`) providing anonymous audit logging and extensible custom job role storage.

---

## 📐 API & Module Reference

### `src.text_extractor`
```python
def extract_resume_text(uploaded_file, file_name: Optional[str] = None) -> Tuple[str, str]:
    """
    Extracts text from PDF or DOCX file streams safely in-memory.
    Returns: (extracted_text, file_type)
    """
```

### `src.text_cleaner`
```python
def clean_text(raw_text: str) -> str:
    """Normalizes unicode characters, bullet points, and whitespace."""

def extract_sections(text: str) -> Dict[str, str]:
    """Segments resume into 'education', 'skills', 'experience', 'projects'."""

def sanitize_protected_data(text: str) -> str:
    """Strips age, gender, marital status, and religion to eliminate bias."""
```

### `src.skill_extractor`
```python
class SkillExtractor:
    def extract_skills(self, text: str) -> Dict[str, Any]:
        """
        Scans text against 60 skills across 7 domains in skill_dictionary.csv using alias resolution.
        Returns detected skills, categorized lists, and metadata.
        """
```

### `src.job_matcher`
```python
class JobMatcher:
    def match_all_roles(self, resume_text: str, detected_skills: List[str]) -> List[Dict[str, Any]]:
        """
        Calculates hybrid match score combining:
        - 60% Skill Matrix Coverage
        - 30% TF-IDF Cosine Similarity
        - 10% Preferred Competency Bonus
        Evaluated across 10 benchmark roles in 5 career tracks.
        """
```

### `src.roadmap_generator`
```python
class RoadmapGenerator:
    def generate_roadmap(self, target_role: Dict[str, Any], candidate_skills: List[str]) -> Dict[str, Any]:
        """
        Organizes missing skills into 3 progressive phases and generates 3 tailored capstone projects.
        """
```

### `src.report_generator`
```python
def generate_pdf_report(analysis_data: Dict[str, Any]) -> bytes:
    """Assembles a publication-ready PDF report using ReportLab and returns raw bytes."""

def generate_markdown_report(analysis_data: Dict[str, Any]) -> str:
    """Generates formatted markdown summary."""
```
