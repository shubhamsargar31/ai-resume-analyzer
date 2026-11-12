# GitHub Repository Setup Guide

## Quick Start (5 minutes)

### Step 1: Create GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click the **+** icon (top right) → **New repository**
3. Configure:
   - **Repository name:** `ai-resume-analyzer` (or your preferred name)
   - **Description:** `AI Resume Analyzer and Job Recommendation System - NLP-based career guidance tool`
   - **Visibility:** Public (recommended for portfolio) or Private
   - **Initialize:** Do NOT check "Add a README" (we already have one)
   - **Do NOT** add .gitignore or license (we have them)

4. Click **Create repository**

### Step 2: Connect Local Repository to GitHub

Copy the commands below and run them in your terminal:

```bash
# Navigate to your project directory
cd "C:\Users\varad\Desktop\shubham major projecyts\major 2"

# Add GitHub remote (replace with your actual repo URL)
git remote add origin https://github.com/YOUR_USERNAME/ai-resume-analyzer.git

# Rename branch to main (GitHub default)
git branch -M main

# Push all commits to GitHub
git push -u origin main
```

### Step 3: Verify

1. Go to your GitHub repository URL
2. You should see all your files
3. The README.md will be automatically displayed

---

## Alternative: Using GitHub Desktop

If you prefer a GUI:

1. Download [GitHub Desktop](https://desktop.github.com)
2. Sign in to your GitHub account
3. Click **File** → **Add Local Repository**
4. Select your project folder
5. Click **Publish repository**
6. Choose visibility and click **Publish**

---

## Updating Your Repository

After making changes:

```bash
# Stage all changes
git add -A

# Commit with a message
git commit -m "feat: add new feature"

# Push to GitHub
git push
```

---

## Repository Structure

Your GitHub repository will contain:

```
ai-resume-analyzer/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── DEPLOYMENT.md             # Deployment guide
├── DEMO_GUIDE.md             # Demo instructions
├── DEMO_VIDEO_SCRIPT.md      # Video recording script
├── TESTING.md                # Test verification report
├── PROJECT_REPORT.md         # Academic project report
├── TECHNICAL_DOCUMENTATION.md # Technical details
├── FINAL_ACCEPTANCE_REPORT.md # Acceptance criteria
├── Dockerfile                # Docker deployment
├── docker-compose.yml        # Docker Compose config
├── .gitignore                # Git ignore rules
├── architecture.png          # Architecture diagram
├── architecture.pdf          # Architecture PDF
├── data/
│   ├── job_roles.csv         # 10 job roles dataset
│   ├── skill_dictionary.csv  # 60 skills dataset
│   └── test_cases.csv        # Test case specifications
├── src/
│   ├── text_extractor.py     # PDF/DOCX extraction
│   ├── text_cleaner.py       # Text cleaning & privacy
│   ├── skill_extractor.py    # Skill detection
│   ├── profile_extractor.py  # Profile parsing
│   ├── job_matcher.py        # TF-IDF matching
│   ├── recommender.py        # Role recommendations
│   ├── roadmap_generator.py  # Learning roadmap
│   ├── report_generator.py   # PDF/Markdown reports
│   └── database.py           # SQLite manager
├── sample_resumes/           # 5 anonymized sample resumes
├── tests/                    # 25 automated tests
├── reports/                  # Generated reports (gitignored)
└── scripts/                  # Utility scripts
```

---

## Deployment to Streamlit Cloud

After pushing to GitHub:

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file to `app.py`
6. Click "Deploy"

Your app will be live at: `https://<app-name>.streamlit.app`

See `DEPLOYMENT.md` for detailed instructions.

---

## Troubleshooting

### "Permission denied" error
- Ensure you have write access to the repository
- Try: `git remote set-url origin https://YOUR_TOKEN@github.com/USERNAME/REPO.git`

### "Repository not found"
- Check the URL is correct
- Ensure repository exists on GitHub
- Check if repository is private (you need access)

### "Everything up-to-date" but files not showing
- Run: `git push -u origin main --force`
- Or delete and recreate remote: `git remote remove origin` then `git remote add origin <url>`

### Merge conflicts
- Pull latest changes: `git pull origin main`
- Resolve conflicts in your editor
- Commit and push again

---

## Best Practices

1. **Commit often** with descriptive messages
2. **Use .gitignore** to exclude sensitive files
3. **Never commit** API keys or passwords
4. **Write meaningful** commit messages
5. **Tag releases** for version milestones: `git tag v1.0.0 && git push --tags`

---

## Repository Badges

Add these to your README.md for a professional look:

```markdown
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![Tests](https://img.shields.io/badge/Tests-25%20Passing-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)
```

---

## Support

For issues, check:
- [GitHub Docs](https://docs.github.com)
- [Git Documentation](https://git-scm.com/doc)
- Project README.md
