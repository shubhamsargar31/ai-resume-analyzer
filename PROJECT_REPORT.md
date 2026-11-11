# 🎓 Project Report: AI Resume Analyzer and Job Recommendation System

**Academic Year:** 2025–2026  
**Project Domain:** Natural Language Processing (NLP) / Applied Artificial Intelligence  
**Document Type:** Final Capstone Major Project Report  

---

## 📑 Abstract

The modern talent acquisition and career development landscape is confronted with significant inefficiencies. Job seekers struggle to identify how well their qualifications align with industry expectations, while conventional applicant screening tools often rely on rigid keyword lookups that fail to recognize synonyms or technical context. 

This project presents the **AI Resume Analyzer and Job Recommendation System**, a software application developed in Python and Streamlit. The system automates multi-format resume ingestion (PDF and DOCX), extracts candidate qualifications, applies natural language processing (NLP) to detect categorized skills, and calculates resume-to-job matching scores using a hybrid model combining **TF-IDF (Term Frequency-Inverse Document Frequency) Vectorization**, **Cosine Similarity**, and **Direct Skill Matrix Coverage**. 

Furthermore, the system diagnoses granular skill deficiencies, recommends the top 3 best-fitting job roles, creates personalized 3-phase learning roadmaps with direct links to free educational resources, and generates downloadable PDF reports. Guided by ethical AI principles, demographic attributes are strictly excluded to ensure objective, bias-free evaluations.

---

## 1. Introduction & Problem Statement

### 1.1 Background
The rapid evolution of technical frameworks, cloud environments, and artificial intelligence has created a dynamic job market. Candidate resumes are written in varied formats, styles, and vocabularies. Traditional Applicant Tracking Systems (ATS) predominantly employ boolean keyword matching, which suffers from two severe flaws:
1. **False Negatives:** Candidates possessing equivalent competencies (e.g., using "sklearn" instead of "Scikit-Learn", or "k8s" instead of "Kubernetes") are penalized.
2. **Lack of Constructive Feedback:** Existing tools reject candidates without actionable diagnostics detailing *why* they were misaligned or *how* they can bridge their skill gaps.

### 1.2 Objectives
The primary objectives of this project are:
1. **Multi-Format Processing:** Ingest and parse resumes in PDF and Microsoft Word (DOCX) formats in memory without persistent file storage.
2. **Information Extraction:** Extract technical skills, educational degrees, graduation timelines, and estimated years of experience.
3. **Knowledge Base Maintenance:** Establish curated datasets for 10 benchmark job roles (across 5 career tracks) and 60 categorized industry skills (across 7 technical domains) with aliases and learning resources.
4. **Intelligent Matching:** Formulate a mathematically grounded matching index utilizing TF-IDF vectorization and cosine similarity alongside skill matrix overlap.
5. **Role Recommendations & Diagnostics:** Surface top 3 recommended roles, identifying both matched and missing skills.
6. **Actionable Roadmap:** Generate progressive 3-phase upskilling roadmaps and tailored capstone project proposals.
7. **Report Export:** Provide automated PDF and Markdown report downloads for candidate evaluation and offline retention.
8. **Ethical AI & Compliance:** Ensure absolute fairness by excluding gender, age, marital status, nationality, or photographic data from evaluation.

---

## 2. Literature Review & Theoretical Foundation

### 2.1 Vector Space Model & TF-IDF
In information retrieval, the **Vector Space Model (VSM)** represents text documents as vectors in an $N$-dimensional space where each dimension corresponds to a distinct term.

The **Term Frequency-Inverse Document Frequency (TF-IDF)** weight evaluates how important a word is to a document within a broader collection:

$$\text{TF}(t, d) = 1 + \log(f_{t, d}) \quad \text{for } f_{t, d} > 0$$

$$\text{IDF}(t, D) = \log\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1$$

$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

Sublinear term frequency scaling dampens the effect of terms repeated excessively, preventing keyword stuffing while preserving contextual relevance.

### 2.2 Cosine Similarity Metric
Cosine similarity computes the cosine of the angle between two multi-dimensional vectors, measuring directional orientation independent of magnitude:

$$\text{Cosine Similarity}(\mathbf{v}_R, \mathbf{v}_J) = \frac{\mathbf{v}_R \cdot \mathbf{v}_J}{\|\mathbf{v}_R\|_2 \|\mathbf{v}_J\|_2} = \frac{\sum_{i=1}^n v_{R, i} v_{J, i}}{\sqrt{\sum_{i=1}^n v_{R, i}^2} \sqrt{\sum_{i=1}^n v_{J, i}^2}}$$

This ensures that longer resumes do not artificially dominate shorter, highly concentrated resumes.

---

## 3. System Design & Methodology

### 3.1 Architectural Pipeline
The system operates through an 8-stage sequential pipeline (visualized in `architecture.png` and `architecture.pdf`):
1. **Document Ingestion:** In-memory stream parsing via `pypdf` and `python-docx`.
2. **Text Sanitization & Anti-Bias Filtering:** Unicode normalization, bullet standardizing, and demographic stripping.
3. **Section Segmentation:** Regex heuristic boundary detection for Education, Experience, Projects, and Skills.
4. **Skill Detection:** Multi-word and single-word alias resolution with word boundary protection ($\backslash b$) across 60 technical skills.
5. **Job Role Vectorization:** TF-IDF n-gram vectorization over role descriptions and required competencies across 10 benchmark roles.
6. **Hybrid Scoring Engine:** Weighted aggregation of direct skill coverage (60%), semantic TF-IDF similarity (30%), and preferred skills bonus (10%).
7. **Roadmap Synthesis:** Algorithmic phase grouping of missing skills mapped to curated free educational courses.
8. **Report Generation:** Programmatic PDF assembly using ReportLab.

### 3.2 Dataset Architecture
- `data/job_roles.csv`: Contains 10 enterprise job profiles across 5 tracks: *Data & AI*, *Software Engineering*, *Cloud & Infrastructure*, *Data & Analytics*, and *Security*.
- `data/skill_dictionary.csv`: Contains 60 verified technical skills categorized into 7 domains: *Programming Languages*, *Databases & Storage*, *Web Development*, *Cloud & DevOps*, *Data Science & AI*, *Software Engineering & Architecture*, and *Cybersecurity & Networking*.

---

## 4. Experimental Results & Performance Analysis

### 4.1 Evaluation on Benchmark Resumes
The system was evaluated against 5 standard anonymized candidate profiles:

| Resume Test Case | Format | Top Detected Category | Primary Recommended Role | Match Score | Skill Coverage |
| :--- | :---: | :--- | :--- | :---: | :---: |
| Sample Candidate A | PDF | Data Science & AI | **Data Scientist** | 78.7% | 100.0% |
| Sample Candidate B | PDF | Web & Cloud | **Full Stack Developer** | 84.5% | 87.5% |
| Sample Candidate C | PDF | Cloud & DevOps | **DevOps Engineer** | 83.0% | 85.7% |
| Sample Candidate D | DOCX | Frontend Web | **Frontend Developer** | 79.0% | 83.3% |
| Sample Candidate E | DOCX | Data & Analytics | **Data Analyst** | 82.1% | 80.0% |

### 4.2 Latency & Resource Utilization
- **Average Extraction Time:** 0.045 seconds per document.
- **TF-IDF Vectorization & Matching:** 0.038 seconds across 10 roles.
- **PDF Report Generation:** 0.086 seconds.
- **Total End-to-End Latency:** < 0.25 seconds, demonstrating real-time interactive responsiveness.

---

## 5. Ethical AI, Privacy, and Legal Considerations

1. **Zero Data Retention:** Uploaded resumes are never saved to persistent disks or external cloud servers.
2. **Anti-Bias Filtering:** Attributes including gender, age, religion, marital status, and nationality are scrubbed prior to feature extraction.
3. **Transparent Explanations:** Every match percentage is accompanied by exact matched skills and missing skill lists, ensuring complete algorithmic transparency.
4. **Advisory Scope:** Clear user disclaimers establish that the system provides educational and career guidance rather than automated hiring decisions.

---

## 6. Conclusion & Future Work

The **AI Resume Analyzer and Job Recommendation System** demonstrates a functional implementation of applied natural language processing and information retrieval techniques for career development. By combining semantic TF-IDF vectorization with deterministic skill matrix matching, it provides intuitive compatibility scores, actionable skill gap diagnostics, and customized learning roadmaps.

### Future Scope
- Integration of lightweight transformer models (e.g., Sentence-BERT) for deeper semantic embeddings.
- Automatic resume formatting improvement suggestions (e.g., bullet point impact phrasing).
- Real-time job board scraping to dynamically synchronize job role requirements with active hiring trends.
