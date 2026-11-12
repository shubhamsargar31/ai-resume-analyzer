# Demonstration Video Script & Guide

## Video Title
**AI Resume Analyzer and Job Recommendation System - Live Demo**

## Duration
Target: 5-7 minutes

## Equipment Needed
- Screen recording software (OBS Studio, Loom, or built-in screen recorder)
- Microphone for narration
- The running Streamlit app at `http://localhost:8501`

---

## Scene-by-Scene Script

### Scene 1: Introduction (0:00 - 0:30)

**Visual:** Title card with project name and your name/institution

**Narration:**
> "Hello! Today I'm demonstrating my AI Resume Analyzer and Job Recommendation System, a Python-based application that helps students understand how well their resume matches target job roles. The system uses NLP techniques including TF-IDF vectorization and cosine similarity to provide accurate match scores, identify skill gaps, and generate personalized learning roadmaps."

**Show:** Title slide or app homepage

---

### Scene 2: Application Overview (0:30 - 1:00)

**Visual:** Streamlit dashboard home page

**Narration:**
> "This is the main dashboard. On the left sidebar, I can select from pre-built sample resumes or upload my own PDF or DOCX file. The system supports both formats and processes them entirely in memory for privacy."

**Show:** Sidebar with sample dropdown and upload area

---

### Scene 3: Sample Resume Analysis (1:00 - 2:30)

**Visual:** Selecting and analyzing a sample resume

**Narration:**
> "Let me demonstrate with the Data Scientist sample resume. I'll select it from the dropdown and click 'Load & Analyze Sample'."

**Action:** Select "Data Scientist (PDF)" → Click "Load & Analyze Sample"

**Narration (while analyzing):**
> "The system is now extracting text from the PDF, cleaning and normalizing it, detecting skills, and computing match scores against 10 job roles using TF-IDF and cosine similarity. This takes less than a second."

**After analysis completes:**
> "The analysis is complete. I can see the candidate profile with their education, experience level, and detected skills. The top recommendation is Data Scientist with a 78.7% match score."

**Show:** Dashboard with metrics, charts, top 3 recommendations

---

### Scene 4: Job Recommendations (2:30 - 3:30)

**Visual:** Job Recommendations tab

**Narration:**
> "Let me navigate to the Job Recommendations tab to see the detailed breakdown."

**Action:** Click "🎯 Job Recommendations" in sidebar

**Narration:**
> "Here I can see the top 3 recommended roles with their match scores, skill coverage percentages, and readiness tiers. The bar chart shows compatibility across all 10 benchmark roles. I can also see which skills are matched and which are missing for each role."

**Show:** Role cards, bar chart, skill breakdown charts

---

### Scene 5: Skill Gap Analysis (3:30 - 4:30)

**Visual:** Skill Gap Analysis tab

**Narration:**
> "Now let me check the Skill Gap Analysis to understand what's missing for a specific role."

**Action:** Click "🔍 Skill Gap Analysis"

**Narration:**
> "I can select any target role from the dropdown to benchmark against. The system shows matched skills in green, missing skills in red, and preferred skills in purple. For the Data Scientist role, this candidate has 100% skill coverage, which is excellent."

**Show:** Matched/missing skill tags, gauge chart

---

### Scene 6: Learning Roadmap (4:30 - 5:30)

**Visual:** Learning Roadmap tab

**Narration:**
> "The Learning Roadmap provides a personalized 3-phase upskilling plan based on the missing skills."

**Action:** Click "🗺️ Learning Roadmap"

**Narration:**
> "For this candidate with perfect skill match, the roadmap shows advanced specialization phases. For candidates with gaps, it would show specific skills to learn, estimated hours, free course resources, and documentation links. It also suggests 3 capstone projects to demonstrate new skills."

**Show:** Roadmap phases, skill cards, capstone projects

---

### Scene 7: Custom Resume Upload (5:30 - 6:30)

**Visual:** Uploading a custom resume

**Narration:**
> "Let me demonstrate uploading a custom resume. I'll upload this challenging resume with non-standard formatting."

**Action:** Upload `Challenging_Resume_Neha_Kulkarni.pdf` → Click "⚡ Run Full AI Analysis"

**Narration:**
> "The system successfully handles non-standard section headers like 'CORE CAPABILITIES' and 'SELECTED PROJECTS'. It correctly identifies 15 skills, extracts 3 projects, and recommends Data Analyst as the top role with 78% match. The phone number and portfolio are also correctly extracted."

**Show:** Analysis results for custom resume

---

### Scene 8: Reports & Privacy (6:30 - 7:00)

**Visual:** Download Report and Privacy tabs

**Narration:**
> "Finally, let me show the report generation and privacy features."

**Action:** Click "📥 Download Report" → Show PDF/Markdown download buttons → Click "⚖️ Privacy & Compliance"

**Narration:**
> "The system generates publication-ready PDF and Markdown reports. The Privacy tab explains our ethical AI guarantees: no demographic scoring, in-memory processing, and transparent match score explanations. All uploaded resumes are processed in volatile memory and never stored permanently."

**Show:** Download buttons, privacy compliance information

---

### Scene 9: Conclusion (7:00 - 7:30)

**Visual:** Return to dashboard or show GitHub repository

**Narration:**
> "This AI Resume Analyzer demonstrates practical application of NLP, TF-IDF vectorization, and cosine similarity for career guidance. The system is open-source and available on GitHub with complete documentation, sample resumes, and automated tests. Thank you for watching!"

**Show:** GitHub repository URL or final dashboard

---

## Recording Tips

1. **Resolution:** 1920x1080 (Full HD) for clarity
2. **Frame rate:** 30fps is sufficient
3. **Audio:** Use a quiet room, test microphone beforehand
4. **Pacing:** Speak clearly, pause between actions
5. **Highlights:** Zoom in on key UI elements if needed
6. **Subtitles:** Add subtitles for accessibility

## Post-Production

- Trim dead air and mistakes
- Add intro/outro title cards
- Add background music (optional, low volume)
- Export as MP4 (H.264 codec)
- Upload to YouTube/Vimeo/Loom
- Link in README.md and project report

## Alternative: Loom Recording

If you prefer a quicker method:

1. Install [Loom](https://www.loom.com) browser extension
2. Click "New Video" → "Record Screen"
3. Select "Current Tab" or "Desktop"
4. Record your walkthrough
5. Share link directly in README

## Script File

Save this script as `DEMO_VIDEO_SCRIPT.md` for reference during recording.
