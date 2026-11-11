# 🎬 Live Demonstration & Evaluator Presentation Guide

This guide provides a step-by-step demonstration walkthrough for professors, project evaluators, and viva panels.

---

## 🚀 1. Setup & Launching the Application (Under 1 Minute)

Open PowerShell or Terminal in the project root directory:

```powershell
# 1. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 2. Launch the Streamlit application
streamlit run app.py
```

The system will start and print `Local URL: http://localhost:8501`. Open this URL in your web browser.

---

## 🎯 2. Demonstration Flow (Recommended 5-Minute Walkthrough)

### Step 1: Instant Demo Sample Selection (Sidebar)
1. Point out the **Quick Demo Samples** in the left sidebar.
2. Select **"Data Scientist (PDF)"** and click **"Load & Analyze Sample"**.
3. **What to highlight to evaluators:**
   - Explain that the system processes real documents directly in memory without disk retention.
   - Point out the real-time progress indicators (Extraction &rarr; Cleaning &rarr; NLP Detection &rarr; TF-IDF Matching &rarr; Recommendations).

### Step 2: Inspected Profile & Detected Skills (Dashboard Tab)
1. Show the parsed **Metric Cards**:
   - Number of identified skills (e.g. 8 skills).
   - Degree detected (e.g. B.Tech in Computer Science).
   - Estimated experience level (e.g. 3 years, Junior / Mid-Level).
2. Show the **Detected Technical Skills** categorized neatly into domains (Programming Languages, Data Science & AI, Cloud & DevOps).
3. Expand **"View Parsed Resume Sections & Text Inspector"** to show that the system segmented the resume into Education, Experience, Skills, and Projects sections.

### Step 3: Job Recommendations & Mathematical Matching
1. Switch to the **"🎯 Job Recommendations"** tab in the sidebar.
2. Highlight the **Top 3 Recommended Roles** cards:
   - Rank #1: **Data Scientist** with high match score (~79-81%), labeled *"Excellent Match"*.
   - Rank #2 & #3: Related roles (e.g., Data Analyst, Machine Learning Engineer).
3. Show the interactive Plotly charts:
   - **Horizontal Compatibility Index Chart:** Compares the candidate against all 10 roles in the database.
   - **Component Attribution Chart:** Explain the exact mathematical formulation: 60% Skill Coverage, 30% TF-IDF Cosine Similarity, and 10% Preferred Bonus.

### Step 4: Skill Gap Analysis & Interactive Role Switching
1. Navigate to **"🔍 Skill Gap Analysis"**.
2. Explain the interactive role dropdown: the user can pick ANY job role in the database to see what skills they are missing.
3. Show the **Gauge Chart** reflecting compatibility.
4. Show the visual badges:
   - **Green Badges:** Matched required skills (e.g., Python, SQL, Pandas, NumPy, Scikit-Learn).
   - **Red Badges:** Missing skills required for the role.

### Step 5: Personalized Learning Roadmap & Capstone Projects
1. Navigate to **"🗺️ Learning Roadmap"**.
2. Walk the evaluator through the **3-Phase Structured Learning Plan**:
   - Phase 1: Foundational syntax.
   - Phase 2: Practical frameworks.
   - Phase 3: Production architecture.
3. Show that every skill gap has:
   - Estimated study hours.
   - Verified free course recommendation (Harvard CS50, freeCodeCamp, etc.).
   - Direct link to official documentation.
4. Scroll to the **Recommended Capstone Portfolio Projects**:
   - Point out how project suggestions combine the candidate's existing skills with newly learned skills to help them get hired.
   - Highlight the pre-written **STAR format resume bullet points**.

### Step 6: One-Click Report Generation & PDF Download
1. Navigate to **"📥 Download Report"**.
2. Click **"⬇️ Download PDF Report"** — open the downloaded file in front of the evaluator.
3. **Point out:**
   - Branded executive header and analysis ID.
   - Summary profile table.
   - Top 3 roles comparison table.
   - Detailed skill gap breakdown.
   - Complete upskilling roadmap.
   - Ethical AI compliance statement.
4. Also show the **Markdown/Text summary** preview.

### Step 7: Ethical AI, Privacy & SQLite Persistence
1. Navigate to **"⚖️ Ethical AI & Privacy"**.
2. Explain that the system strips gender, age, religion, marital status, and photos, ensuring non-discriminatory scoring.
3. Show the **Anonymized SQLite Database Log** at the bottom of the tab, proving local persistence without storing candidate PII.

---

## 🧪 3. Running Automated Tests Live for Evaluators

In the terminal, run:

```powershell
python -m unittest discover tests -v
```

Demonstrate that all 25 unit and acceptance test cases execute and pass in under 0.4 seconds.

---

## ❓ 4. Frequently Asked Viva / Oral Exam Questions

**Q1: Why did you combine TF-IDF with direct skill matching instead of relying solely on Cosine Similarity?**  
*Answer:* Pure cosine similarity evaluates term distributions across entire documents. If a resume is long or includes descriptive narratives, raw cosine similarity against a short job description can be artificially deflated (often 20–30%), even if the candidate possesses all mandatory technical qualifications. Our hybrid formula (60% Skill Matrix + 30% TF-IDF + 10% Preferred Bonus) ensures that candidates with exact skill alignment receive intuitive, realistic scores (75–85%+) while preserving semantic contextual scoring.

**Q2: How do you prevent word boundary false positives (e.g., matching the skill "Go" in words like "Good")?**  
*Answer:* We compile boundary-protected regex patterns with word boundaries (`\b`) and lookaheads. In addition, multi-word phrases (e.g., "Natural Language Processing") are sorted by length descending so that multi-word entities match before single-word substrings.

**Q3: How does the system protect user privacy?**  
*Answer:* Resumes are read as in-memory binary byte streams (`io.BytesIO`) using `pypdf` and `python-docx`. No uploaded files are written to permanent disk storage, and temporary memory is cleared immediately after processing. Furthermore, demographic attributes like age, gender, and religion are sanitized before scoring.
