# Streamlit Cloud / Render Deployment Guide

## Option 1: Streamlit Cloud (Recommended - Free)

Streamlit Cloud is the easiest way to deploy this app for free.

### Steps:

1. **Push your code to GitHub** (see GitHub setup below)

2. **Go to [share.streamlit.io](https://share.streamlit.io)**

3. **Sign in with your GitHub account**

4. **Click "New app"**

5. **Configure:**
   - **Repository:** Select your GitHub repository
   - **Branch:** `main` or `master`
   - **Main file path:** `app.py`
   - **Python version:** `3.11`

6. **Click "Deploy"**

7. **Your app will be live at:** `https://<your-app-name>.streamlit.app`

### Environment Variables (if needed):
None required for basic functionality.

---

## Option 2: Render.com (Free Tier)

### Steps:

1. **Push your code to GitHub**

2. **Go to [render.com](https://render.com)** and sign up

3. **Click "New +" → "Web Service"**

4. **Connect your GitHub repository**

5. **Configure:**
   - **Name:** `ai-resume-analyzer`
   - **Runtime:** `Docker` (uses your Dockerfile)
   - **Region:** Choose closest to your users
   - **Plan:** `Free`

6. **Click "Create Web Service"**

7. **Your app will be live at:** `https://<your-app-name>.onrender.com`

### Notes:
- Free tier may sleep after 15 minutes of inactivity
- First deploy may take 5-10 minutes
- Subsequent deploys are faster

---

## Option 3: Docker (Self-Hosted)

### Prerequisites:
- Docker installed on your system

### Build and Run:

```bash
# Build the Docker image
docker build -t resume-analyzer .

# Run the container
docker run -p 8501:8501 -v $(pwd)/data:/app/data -v $(pwd)/reports:/app/reports resume-analyzer

# Or using docker-compose
docker-compose up -d
```

### Access:
Open `http://localhost:8501` in your browser.

### Stop:
```bash
docker-compose down
# or
docker stop <container_id>
```

---

## Option 4: Local Development

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\Activate.ps1

# Activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Environment Variables Reference

| Variable | Default | Description |
|---|---|---|
| `STREAMLIT_SERVER_PORT` | `8501` | Port for Streamlit server |
| `STREAMLIT_SERVER_ADDRESS` | `0.0.0.0` | Bind address |
| `STREAMLIT_SERVER_HEADLESS` | `true` | Disable browser auto-open |
| `STREAMLIT_BROWSER_GATHER_USAGE_STATS` | `false` | Disable usage stats |

---

## Troubleshooting

### App won't start
- Check Python version (3.10-3.13)
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check for port conflicts: `netstat -ano | findstr :8501`

### Deployment fails
- Ensure `app.py` is in root directory
- Check `requirements.txt` is present
- Verify GitHub repository is public or Streamlit Cloud has access

### Reports not saving
- Ensure `reports/` directory exists or is writable
- Check file permissions
