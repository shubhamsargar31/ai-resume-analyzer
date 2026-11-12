"""
AI Resume Analyzer & Job Recommendation System
Design Concept: AI Career Intelligence Platform (Premium SaaS Dark Theme)
Inspired by Linear, Stripe, and modern cloud analytics platforms.
"""

import os
import io
import time
from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import core system modules (backend logic remains 100% unchanged)
from src.text_extractor import extract_resume_text, ResumeExtractionError
from src.text_cleaner import clean_text, extract_sections, extract_contact_info, sanitize_protected_data
from src.skill_extractor import SkillExtractor
from src.profile_extractor import extract_full_profile
from src.job_matcher import JobMatcher
from src.recommender import JobRecommender
from src.roadmap_generator import RoadmapGenerator
from src.report_generator import generate_pdf_report, generate_markdown_report
from src.database import DatabaseManager

# Page Configuration
st.set_page_config(
    page_title="Career Intelligence Platform | AI Resume Analyzer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium SaaS Dark Theme Stylesheet
SAAS_THEME_CSS = """
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Global Reset & Base */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        background-color: #0B1020 !important;
        color: #F3F6FC !important;
    }

    /* Hide Default Streamlit Chrome */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header[data-testid="stHeader"] {
        background-color: rgba(11, 16, 32, 0.85) !important;
        backdrop-filter: blur(12px) !important;
    }

    /* Main Container Padding */
    .main .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1400px;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.07) !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        background-color: #111827 !important;
        padding-top: 1.2rem;
    }

    /* Sidebar Brand Header */
    .brand-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 4px 6px 18px 6px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 16px;
    }
    .brand-logo-icon {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: linear-gradient(135deg, #27D3C2 0%, #648CFF 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 1.25rem;
        color: #0B1020;
        box-shadow: 0 4px 14px rgba(39, 211, 194, 0.35);
    }
    .brand-text-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #F3F6FC;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    .brand-text-subtitle {
        font-size: 0.72rem;
        color: #27D3C2;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    /* Navigation Radio Items */
    [data-testid="stSidebar"] [data-testid="stRadio"] > div {
        gap: 4px !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        background: transparent !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        margin-bottom: 2px !important;
        color: #94A3B8 !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        transition: all 0.15s ease-in-out !important;
        border: 1px solid transparent !important;
        cursor: pointer !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: rgba(255, 255, 255, 0.04) !important;
        color: #F3F6FC !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
        background: rgba(39, 211, 194, 0.1) !important;
        color: #27D3C2 !important;
        font-weight: 600 !important;
        border-color: rgba(39, 211, 194, 0.3) !important;
    }

    /* User Profile Footer in Sidebar */
    .user-profile-badge {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 14px;
        background: #171F32;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        margin-top: 24px;
    }
    .user-avatar {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: linear-gradient(135deg, #648CFF, #27D3C2);
        color: #0B1020;
        font-weight: 700;
        font-size: 0.85rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .user-meta-name {
        font-size: 0.82rem;
        font-weight: 600;
        color: #F3F6FC;
        line-height: 1.2;
    }
    .user-meta-role {
        font-size: 0.72rem;
        color: #94A3B8;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    .status-dot-live {
        width: 6px;
        height: 6px;
        background-color: #27D3C2;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px #27D3C2;
    }

    /* SaaS Hero Banner */
    .saas-hero {
        background: radial-gradient(ellipse at 80% -20%, rgba(100, 140, 255, 0.15) 0%, rgba(39, 211, 194, 0.08) 40%, rgba(11, 16, 32, 0) 70%), #171F32;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .saas-hero::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #27D3C2, #648CFF, transparent);
    }
    .hero-badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 20px;
        background: rgba(39, 211, 194, 0.12);
        border: 1px solid rgba(39, 211, 194, 0.3);
        color: #27D3C2;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    .hero-title-text {
        font-size: 2.1rem;
        font-weight: 800;
        color: #F3F6FC !important;
        letter-spacing: -0.03em;
        margin: 0 0 8px 0;
        line-height: 1.2;
    }
    .hero-title-gradient {
        background: linear-gradient(135deg, #27D3C2 0%, #648CFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-desc-text {
        font-size: 0.98rem;
        color: #94A3B8 !important;
        margin: 0;
        max-width: 820px;
        line-height: 1.5;
    }

    /* Metric Cards */
    .saas-metric-card {
        background: #171F32;
        border: 1px solid #232F4A;
        border-radius: 12px;
        padding: 20px;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    .saas-metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(39, 211, 194, 0.4);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    .metric-card-label {
        font-size: 0.78rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 6px;
    }
    .metric-card-val {
        font-size: 1.9rem;
        font-weight: 800;
        color: #F3F6FC;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }
    .metric-card-sub {
        font-size: 0.8rem;
        color: #27D3C2;
        margin-top: 6px;
        font-weight: 500;
    }

    /* SaaS Panels */
    .saas-panel {
        background-color: #171F32;
        border: 1px solid #232F4A;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .saas-panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }
    .saas-panel-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #F3F6FC;
        margin: 0;
        letter-spacing: -0.02em;
    }

    /* Role Cards */
    .role-recommend-card {
        background: #171F32;
        border: 1px solid #232F4A;
        border-radius: 14px;
        padding: 22px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        position: relative;
    }
    .role-recommend-card:hover {
        transform: translateY(-3px);
        border-color: #648CFF;
        box-shadow: 0 12px 28px -6px rgba(0, 0, 0, 0.4);
    }
    .role-card-rank {
        font-size: 0.72rem;
        font-weight: 800;
        color: #94A3B8;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    .role-card-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #F3F6FC;
        margin: 6px 0 2px 0;
        letter-spacing: -0.02em;
    }
    .role-card-meta {
        font-size: 0.8rem;
        color: #94A3B8;
        margin-bottom: 14px;
    }
    .role-score-display {
        display: flex;
        align-items: baseline;
        gap: 6px;
        margin: 12px 0 16px 0;
    }
    .role-score-number {
        font-size: 2.4rem;
        font-weight: 800;
        color: #27D3C2;
        line-height: 1;
        letter-spacing: -0.03em;
    }
    .role-score-label {
        font-size: 0.78rem;
        color: #94A3B8;
        font-weight: 500;
    }

    /* Skill Tags */
    .skill-tag-matched {
        display: inline-flex;
        align-items: center;
        background: rgba(39, 211, 194, 0.1);
        color: #27D3C2;
        border: 1px solid rgba(39, 211, 194, 0.28);
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 3px 4px;
    }
    .skill-tag-missing {
        display: inline-flex;
        align-items: center;
        background: rgba(245, 158, 11, 0.1);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.28);
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 3px 4px;
    }
    .skill-tag-neutral {
        display: inline-flex;
        align-items: center;
        background: rgba(100, 140, 255, 0.08);
        color: #ADC3FF;
        border: 1px solid rgba(100, 140, 255, 0.2);
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 0.82rem;
        font-weight: 500;
        margin: 3px 4px;
    }
    .skill-tag-preferred {
        display: inline-flex;
        align-items: center;
        background: rgba(167, 139, 250, 0.1);
        color: #C4B5FD;
        border: 1px solid rgba(167, 139, 250, 0.28);
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 3px 4px;
    }

    /* Tier Status Pills */
    .tier-badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .tier-excellent { background: rgba(39, 211, 194, 0.15); color: #27D3C2; border: 1px solid rgba(39, 211, 194, 0.3); }
    .tier-good { background: rgba(100, 140, 255, 0.15); color: #648CFF; border: 1px solid rgba(100, 140, 255, 0.3); }
    .tier-moderate { background: rgba(245, 158, 11, 0.15); color: #F59E0B; border: 1px solid rgba(245, 158, 11, 0.3); }
    .tier-low { background: rgba(244, 63, 94, 0.15); color: #F43F5E; border: 1px solid rgba(244, 63, 94, 0.3); }

    /* Timeline Component */
    .timeline-node {
        position: relative;
        padding-left: 28px;
        margin-bottom: 22px;
    }
    .timeline-node::before {
        content: "";
        position: absolute;
        left: 6px;
        top: 6px;
        bottom: -22px;
        width: 2px;
        background: #232F4A;
    }
    .timeline-node:last-child::before {
        display: none;
    }
    .timeline-dot {
        position: absolute;
        left: 0;
        top: 4px;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: #27D3C2;
        border: 3px solid #171F32;
        box-shadow: 0 0 10px rgba(39, 211, 194, 0.6);
    }

    /* Streamlit Control Overrides */
    .stButton > button {
        background: linear-gradient(135deg, #27D3C2 0%, #15B8A6 100%) !important;
        color: #0B1020 !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.55rem 1.2rem !important;
        box-shadow: 0 4px 14px rgba(39, 211, 194, 0.25) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(39, 211, 194, 0.4) !important;
    }
    .stButton > button[kind="secondary"] {
        background: #171F32 !important;
        color: #F3F6FC !important;
        border: 1px solid #232F4A !important;
        box-shadow: none !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: #202B46 !important;
        border-color: #648CFF !important;
    }

    /* File Uploader Container */
    [data-testid="stFileUploader"] {
        background-color: #171F32 !important;
        border: 2px dashed #2A3859 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        transition: all 0.25s ease !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #27D3C2 !important;
        box-shadow: 0 0 18px rgba(39, 211, 194, 0.15) !important;
    }
    [data-testid="stFileUploaderDropzone"] {
        background-color: transparent !important;
    }

    /* Input & Select Boxes */
    div[data-baseweb="select"] {
        background-color: #171F32 !important;
        border: 1px solid #232F4A !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #171F32 !important;
        color: #F3F6FC !important;
    }
    div[data-baseweb="popover"], div[data-baseweb="menu"] {
        background-color: #171F32 !important;
        border: 1px solid #232F4A !important;
    }

    /* Expanders */
    [data-testid="stExpander"] {
        background-color: #171F32 !important;
        border: 1px solid #232F4A !important;
        border-radius: 10px !important;
        margin-bottom: 12px !important;
    }
    [data-testid="stExpander"] details summary {
        color: #F3F6FC !important;
        font-weight: 600 !important;
    }

    /* Dataframe Table Container */
    [data-testid="stDataFrame"] {
        background-color: #171F32 !important;
        border: 1px solid #232F4A !important;
        border-radius: 10px !important;
    }
</style>
"""
st.markdown(SAAS_THEME_CSS, unsafe_allow_html=True)


# Initialize Session State
@st.cache_resource
def load_system_engines():
    """Initializes and caches the NLP matching and extraction engines."""
    skill_extractor = SkillExtractor()
    job_matcher = JobMatcher()
    recommender = JobRecommender(job_matcher)
    roadmap_gen = RoadmapGenerator(skill_extractor)
    db_mgr = DatabaseManager()
    return skill_extractor, job_matcher, recommender, roadmap_gen, db_mgr

skill_extractor, job_matcher, recommender, roadmap_gen, db_mgr = load_system_engines()

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "📊 Dashboard"


# Helper function to run analysis
def run_analysis(file_object, file_name: str):
    """Executes the complete end-to-end analysis workflow."""
    try:
        progress_bar = st.progress(0, text="Ingesting document byte stream...")

        # 1. Text Extraction
        try:
            raw_text, file_type = extract_resume_text(file_object, file_name=file_name)
        except ResumeExtractionError as e:
            st.error(f"Extraction Error: {str(e)}")
            progress_bar.empty()
            return
        except Exception as e:
            st.error(f"Unexpected file error: {str(e)}")
            progress_bar.empty()
            return

        progress_bar.progress(25, text="Normalizing & segmenting sections...")

        # 2. Text Cleaning & Privacy Sanitization
        sanitized_text = sanitize_protected_data(raw_text)
        cleaned_text = clean_text(sanitized_text)
        sections = extract_sections(cleaned_text)
        contact_info = extract_contact_info(raw_text)

        progress_bar.progress(50, text="Matching skills against 60 industry competencies...")

        # 3. Skill & Profile Extraction
        skill_data = skill_extractor.extract_skills(cleaned_text)
        detected_skills = skill_data["detected_skills"]
        profile_data = extract_full_profile(cleaned_text, sections)

        progress_bar.progress(75, text="Computing TF-IDF cosine similarity across 10 roles...")

        # 4. Job Matching & Recommendations
        recommendations = recommender.recommend_top_roles(cleaned_text, detected_skills, top_n=3)
        top_roles = recommendations["top_recommendations"]
        primary_role = top_roles[0] if top_roles else {}

        # 5. Roadmap Generation
        roadmap = roadmap_gen.generate_roadmap(primary_role, detected_skills)

        progress_bar.progress(95, text="Compiling intelligence diagnostics...")

        # Package Results
        candidate_name = contact_info.get("email") or "Evaluated Candidate"
        if candidate_name and "@" in candidate_name:
            candidate_name = candidate_name.split("@")[0].replace(".", " ").title()

        results = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "file_name": file_name,
            "file_type": file_type,
            "candidate_name": candidate_name,
            "raw_text": raw_text,
            "cleaned_text": cleaned_text,
            "sections": sections,
            "contact_info": contact_info,
            "detected_skills": detected_skills,
            "skills_by_category": skill_data["skills_by_category"],
            "skill_details": skill_data["skill_details"],
            "skill_count": len(detected_skills),
            "profile": profile_data,
            "top_roles": top_roles,
            "all_matches": recommendations["all_matches"],
            "primary_role": primary_role,
            "roadmap": roadmap
        }

        # Log anonymized analysis to SQLite
        try:
            db_mgr.log_analysis(
                file_name=file_name,
                file_type=file_type,
                detected_skills_count=len(detected_skills),
                top_role=primary_role.get("role_title", "N/A"),
                match_score=primary_role.get("match_score", 0.0),
                skill_coverage=primary_role.get("skill_coverage_pct", 0.0)
            )
        except Exception:
            pass

        progress_bar.progress(100, text="Analysis Complete!")
        time.sleep(0.3)
        progress_bar.empty()

        st.session_state.analysis_results = results
        st.success("Analysis complete. Explore the intelligence panels below.")

    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
        import traceback
        st.code(traceback.format_exc(), language="python")


# =============================================================
# LEFT SIDEBAR: APPLICATION SHELL & CONTROLS
# =============================================================
with st.sidebar:
    # Custom Application Brand
    st.markdown(
        """
        <div class="brand-container">
            <div class="brand-logo-icon">⚡</div>
            <div>
                <div class="brand-text-title">VECTRA INTELLIGENCE</div>
                <div class="brand-text-subtitle">AI Career Platform</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Demo Quick Selector
    st.markdown(
        """
        <div style="font-size:0.75rem; font-weight:700; color:#94A3B8; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:6px;">
            ⚡ Demo Benchmarks
        </div>
        """,
        unsafe_allow_html=True
    )
    samples_dir = os.path.join(os.path.dirname(__file__), "sample_resumes")
    sample_files = {
        "Data Scientist (PDF)": "sample_data_scientist.pdf",
        "Full Stack Developer (PDF)": "sample_full_stack_dev.pdf",
        "DevOps Engineer (PDF)": "sample_devops_engineer.pdf",
        "Frontend Developer (DOCX)": "sample_frontend_developer.docx",
        "Data Analyst (DOCX)": "sample_data_analyst.docx"
    }

    selected_sample = st.selectbox(
        "Load Anonymized Benchmark:",
        ["-- Select Benchmark --"] + list(sample_files.keys()),
        index=0,
        label_visibility="collapsed"
    )

    if st.button("Load & Analyze Sample", type="secondary", use_container_width=True):
        if selected_sample != "-- Select Benchmark --":
            sample_rel_path = os.path.join(samples_dir, sample_files[selected_sample])
            if os.path.exists(sample_rel_path):
                with open(sample_rel_path, "rb") as f:
                    file_bytes = io.BytesIO(f.read())
                run_analysis(file_bytes, sample_files[selected_sample])
            else:
                st.error("Benchmark file not found on disk.")
        else:
            st.warning("Select a sample resume from the dropdown.")

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    
    # Navigation
    st.markdown(
        """
        <div style="font-size:0.75rem; font-weight:700; color:#94A3B8; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:6px;">
            🧭 Navigation
        </div>
        """,
        unsafe_allow_html=True
    )
    nav_option = st.radio(
        "Navigation Menu",
        [
            "📊 Dashboard",
            "📄 Resume Analyzer",
            "🎯 Job Recommendations",
            "🔍 Skill Gap Analysis",
            "🗺️ Learning Roadmap",
            "📜 Analysis History",
            "⚙️ Job & Skill Catalog",
            "📥 Download Report",
            "⚖️ Privacy & Compliance"
        ],
        index=0,
        label_visibility="collapsed"
    )

    # User Profile / System Status Badge at Bottom
    st.markdown(
        """
        <div class="user-profile-badge">
            <div class="user-avatar">AI</div>
            <div>
                <div class="user-meta-name">Enterprise Analyst</div>
                <div class="user-meta-role">
                    <span class="status-dot-live"></span> NLP Engine Online
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =============================================================
# TOP HEADER / BANNER
# =============================================================
st.markdown(
    """
    <div class="saas-hero">
        <div class="hero-badge-pill">
            <span class="status-dot-live"></span> AI CAREER INTELLIGENCE PLATFORM v1.0
        </div>
        <h1 class="hero-title-text">
            Understand your potential. <span class="hero-title-gradient">Discover your next opportunity.</span>
        </h1>
        <p class="hero-desc-text">
            Enterprise qualification benchmarking powered by sublinear TF-IDF vectorization, semantic cosine similarity, 
            and real-time skill gap synthesis across 10 benchmark industry roles.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

results = st.session_state.analysis_results


# =============================================================
# VIEW 1: DASHBOARD
# =============================================================
if nav_option == "📊 Dashboard":
    # Upload Panel (Drag & Drop Styled)
    col_upload, col_guarantee = st.columns([1.8, 1.2])

    with col_upload:
        st.markdown(
            """
            <div style="margin-bottom:8px; font-size:0.95rem; font-weight:700; color:#F3F6FC;">
                📥 Ingest Candidate Credentials
            </div>
            """,
            unsafe_allow_html=True
        )
        uploaded_file = st.file_uploader(
            "Upload Resume (PDF, DOCX)",
            type=["pdf", "docx"],
            help="Support for standard PDF (.pdf) and Microsoft Word (.docx) resumes (max 10MB)."
        )

        if uploaded_file is not None:
            MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
            if uploaded_file.size > MAX_FILE_SIZE:
                st.error(f"File too large: {uploaded_file.size / (1024*1024):.1f} MB. Maximum allowed size is 10 MB.")
            else:
                st.info(f"📁 Selected: **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")
                if st.button("⚡ Run Full AI Analysis", type="primary", use_container_width=True):
                    run_analysis(uploaded_file, uploaded_file.name)

    with col_guarantee:
        st.markdown(
            """
            <div class="saas-panel" style="padding:18px 20px; height:100%;">
                <div style="font-size:0.85rem; font-weight:700; color:#27D3C2; text-transform:uppercase; letter-spacing:0.04em; margin-bottom:8px;">
                    🛡️ Security & Privacy Guarantees
                </div>
                <ul style="font-size:0.82rem; color:#94A3B8; padding-left:16px; margin:0; line-height:1.6;">
                    <li><b>Volatile In-Memory Processing:</b> Zero disk retention of uploaded files.</li>
                    <li><b>Strict Anti-Bias Sanitization:</b> Gender, age, marital status, and religion are stripped prior to scoring.</li>
                    <li><b>Hybrid Verification:</b> 60% direct skill matrix coverage + 30% semantic TF-IDF.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    if results:
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="saas-panel-header">
                <h3 class="saas-panel-title">📈 Candidate Executive Overview</h3>
                <span class="tier-badge tier-excellent">VERIFIED SESSION</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # 4 Core KPI Metric Cards
        prof = results["profile"]
        edu = prof.get("education", {})
        exp = prof.get("experience", {})
        primary_role = results["primary_role"]

        m_col1, m_col2, m_col3, m_col4 = st.columns(4)

        with m_col1:
            st.markdown(
                f"""
                <div class="saas-metric-card">
                    <div class="metric-card-label">Verified Skills</div>
                    <div class="metric-card-val" style="color:#27D3C2;">{results['skill_count']}</div>
                    <div class="metric-card-sub">Across {len(results['skills_by_category'])} domains</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with m_col2:
            st.markdown(
                f"""
                <div class="saas-metric-card">
                    <div class="metric-card-label">Primary Degree</div>
                    <div class="metric-card-val" style="font-size:1.15rem; min-height:42px;">
                        {edu.get('primary_degree', 'B.Tech / B.S.')}
                    </div>
                    <div class="metric-card-sub">{edu.get('field_of_study', 'Computer Science')}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with m_col3:
            st.markdown(
                f"""
                <div class="saas-metric-card">
                    <div class="metric-card-label">Seniority Tier</div>
                    <div class="metric-card-val">{exp.get('estimated_years', 0)} yrs</div>
                    <div class="metric-card-sub">{exp.get('seniority_level', 'Entry-Level')}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with m_col4:
            st.markdown(
                f"""
                <div class="saas-metric-card">
                    <div class="metric-card-label">Primary Role Match</div>
                    <div class="metric-card-val" style="color:#648CFF;">{primary_role.get('match_score', 0)}%</div>
                    <div class="metric-card-sub">{primary_role.get('role_title', 'Analyzing')}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        # Overview: Primary Role Circular Score & Top 3 Recommendations
        col_score_chart, col_top_roles = st.columns([1.2, 1.8])

        with col_score_chart:
            st.markdown(
                f"""
                <div class="saas-panel" style="text-align:center; height:100%;">
                    <div style="font-size:0.8rem; font-weight:700; color:#94A3B8; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:4px;">
                        Primary Role Compatibility
                    </div>
                    <h3 style="color:#F3F6FC; margin:0 0 10px 0;">{primary_role.get('role_title')}</h3>
                """,
                unsafe_allow_html=True
            )

            # Circular Gauge Chart in Plotly
            score_val = primary_role.get("match_score", 0.0)
            fig_score_radial = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score_val,
                number={"suffix": "%", "font": {"size": 42, "color": "#27D3C2", "family": "Plus Jakarta Sans"}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#232F4A", "tickfont": {"color": "#94A3B8"}},
                    "bar": {"color": "#27D3C2", "thickness": 0.28},
                    "bgcolor": "#111827",
                    "borderwidth": 1,
                    "bordercolor": "#232F4A",
                    "steps": [
                        {"range": [0, 40], "color": "rgba(244, 63, 94, 0.12)"},
                        {"range": [40, 65], "color": "rgba(245, 158, 11, 0.12)"},
                        {"range": [65, 80], "color": "rgba(100, 140, 255, 0.15)"},
                        {"range": [80, 100], "color": "rgba(39, 211, 194, 0.2)"}
                    ],
                    "threshold": {
                        "line": {"color": "#27D3C2", "width": 3},
                        "thickness": 0.8,
                        "value": 75
                    }
                }
            ))
            fig_score_radial.update_layout(
                paper_bgcolor="#171F32",
                plot_bgcolor="#171F32",
                height=230,
                margin=dict(l=20, r=20, t=10, b=10)
            )
            st.plotly_chart(fig_score_radial, use_container_width=True)

            st.markdown(
                f"""
                    <div style="font-size:0.82rem; color:#94A3B8; margin-top:6px;">
                        <b>Assessment:</b> <span style="color:#27D3C2;">{primary_role.get('readiness', 'Ready')}</span><br/>
                        <span style="font-size:0.78rem;">{primary_role.get('readiness_desc', '')}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_top_roles:
            st.markdown(
                """
                <div class="saas-panel" style="height:100%;">
                    <div class="saas-panel-header">
                        <h4 class="saas-panel-title">🎯 Top 3 Target Roles</h4>
                        <span style="font-size:0.75rem; color:#94A3B8;">Multi-factor weighted match</span>
                    </div>
                """,
                unsafe_allow_html=True
            )

            for i, r in enumerate(results["top_roles"]):
                score = r["match_score"]
                tier_class = "tier-excellent" if score >= 75 else ("tier-good" if score >= 55 else "tier-moderate")
                matched_cnt = len(r.get("matched_skills", []))
                req_cnt = r.get("required_skills_count", 0)
                
                st.markdown(
                    f"""
                    <div style="background:#111827; border:1px solid #232F4A; border-radius:10px; padding:14px 16px; margin-bottom:10px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                            <div style="display:flex; align-items:center; gap:8px;">
                                <span style="font-weight:800; font-size:0.85rem; color:#648CFF;">#{i+1}</span>
                                <span style="font-weight:700; font-size:0.95rem; color:#F3F6FC;">{r['role_title']}</span>
                                <span style="font-size:0.75rem; color:#94A3B8;">&bull; {r['category']}</span>
                            </div>
                            <span class="tier-badge {tier_class}">{score}% MATCH</span>
                        </div>
                        <div style="font-size:0.78rem; color:#94A3B8; margin-bottom:8px;">
                            Required Skills: <span style="color:#27D3C2; font-weight:600;">{matched_cnt}/{req_cnt} verified ({r['skill_coverage_pct']}%)</span> &bull; {r['avg_salary']}
                        </div>
                        <div style="background:#232F4A; border-radius:4px; height:6px; overflow:hidden;">
                            <div style="background:linear-gradient(90deg, #27D3C2, #648CFF); height:100%; width:{min(100.0, score)}%;"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("</div>", unsafe_allow_html=True)

        # Overview: Skills Breakdown Preview
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="saas-panel">
                <div class="saas-panel-header">
                    <h4 class="saas-panel-title">🛠️ Competency Breakdown</h4>
                    <span style="font-size:0.78rem; color:#94A3B8;">Categorized skill clusters</span>
                </div>
            """,
            unsafe_allow_html=True
        )

        by_cat = results["skills_by_category"]
        if by_cat:
            cat_cols = st.columns(min(4, len(by_cat)))
            for idx, (cat_name, skills_list) in enumerate(by_cat.items()):
                with cat_cols[idx % len(cat_cols)]:
                    st.markdown(f"<div style='font-size:0.8rem; font-weight:700; color:#648CFF; margin-bottom:6px;'>{cat_name.upper()} ({len(skills_list)})</div>", unsafe_allow_html=True)
                    tags_html = " ".join([f"<span class='skill-tag-matched'>✓ {s}</span>" for s in skills_list])
                    st.markdown(tags_html, unsafe_allow_html=True)
                    st.write("")
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown(
            """
            <div class="saas-panel" style="text-align:center; padding:50px 20px;">
                <div style="font-size:2.8rem; margin-bottom:12px;">📊</div>
                <h3 style="color:#F3F6FC; margin:0 0 8px 0;">No Candidate Profile Loaded</h3>
                <p style="color:#94A3B8; font-size:0.9rem; max-width:540px; margin:0 auto 20px auto;">
                    Upload a resume using the box above or select a pre-built benchmark from the sidebar to inspect instant intelligence.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


# =============================================================
# VIEW 2: RESUME ANALYZER (DEEP DIVE)
# =============================================================
elif nav_option == "📄 Resume Analyzer":
    st.markdown("### 📄 Resume Parsing & Entity Diagnostics")
    
    if not results:
        st.warning("Upload a resume or select a benchmark sample to inspect parsing details.")
    else:
        tab_sec, tab_clean, tab_raw = st.tabs(["Structured Section Inspector", "Cleaned Text Stream", "Raw Extracted Text"])
        
        with tab_sec:
            st.markdown(
                """
                <div class="saas-panel">
                    <div class="saas-panel-header">
                        <h4 class="saas-panel-title">Segmented Document Boundaries</h4>
                        <span style="font-size:0.75rem; color:#27D3C2;">Regex Heuristic Segmentation</span>
                    </div>
                """,
                unsafe_allow_html=True
            )
            for sec, content in results["sections"].items():
                if content.strip():
                    with st.expander(f"📌 {sec.upper()} SECTION", expanded=True):
                        st.markdown(f"<div style='font-family:JetBrains Mono, monospace; font-size:0.82rem; color:#ADC3FF;'>{content}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with tab_clean:
            st.text_area("Normalized Vectorization Text Stream", results["cleaned_text"], height=320)

        with tab_raw:
            st.text_area("Raw Extracted Stream", results["raw_text"], height=320)


# =============================================================
# VIEW 3: JOB RECOMMENDATIONS
# =============================================================
elif nav_option == "🎯 Job Recommendations":
    st.markdown("### 🎯 Benchmark Job Role Recommendations")

    if not results:
        st.warning("Please upload a resume or choose a benchmark sample first.")
    else:
        top_roles = results["top_roles"]
        
        # 3 Role Cards Grid
        r_cols = st.columns(3)
        for idx, role in enumerate(top_roles):
            with r_cols[idx]:
                score = role["match_score"]
                tier_class = "tier-excellent" if score >= 75 else ("tier-good" if score >= 55 else "tier-moderate")
                
                st.markdown(
                    f"""
                    <div class="role-recommend-card">
                        <div>
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span class="role-card-rank">RANK #{idx+1}</span>
                                <span class="tier-badge {tier_class}">{role['match_tier']}</span>
                            </div>
                            <div class="role-card-title">{role['role_title']}</div>
                            <div class="role-card-meta">{role['category']} &bull; {role['avg_salary']}</div>
                            <div class="role-score-display">
                                <div class="role-score-number">{score}%</div>
                                <div class="role-score-label">MATCH INDEX</div>
                            </div>
                            <div style="background:#232F4A; border-radius:4px; height:6px; overflow:hidden; margin-bottom:14px;">
                                <div style="background:linear-gradient(90deg, #27D3C2, #648CFF); height:100%; width:{min(100.0, score)}%;"></div>
                            </div>
                            <div style="font-size:0.82rem; color:#94A3B8; margin-bottom:8px;">
                                <b>Required Skills Coverage:</b> <span style="color:#27D3C2; font-weight:600;">{len(role['matched_skills'])} of {role['required_skills_count']} ({role['skill_coverage_pct']}%)</span>
                            </div>
                        </div>
                        <div style="font-size:0.78rem; color:#ADC3FF; font-style:italic; border-top:1px solid rgba(255,255,255,0.06); padding-top:10px; margin-top:10px;">
                            "{role.get('readiness_desc', '')}"
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Plotly Visualizations in Dark Mode
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        chart_col1, chart_col2 = st.columns([1.5, 1.2])

        with chart_col1:
            all_matches_df = pd.DataFrame(results["all_matches"])
            fig_bar = px.bar(
                all_matches_df.sort_values(by="match_score", ascending=True),
                x="match_score",
                y="role_title",
                orientation="h",
                text="match_score",
                title="Compatibility Across All 10 Benchmark Roles (%)",
                labels={"match_score": "Match Score (%)", "role_title": "Target Role"},
                color="match_score",
                color_continuous_scale=["#1E2942", "#648CFF", "#27D3C2"]
            )
            fig_bar.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_bar.update_layout(
                paper_bgcolor="#171F32",
                plot_bgcolor="#171F32",
                font=dict(color="#F3F6FC", family="Plus Jakarta Sans"),
                height=430,
                margin=dict(l=10, r=20, t=40, b=10),
                xaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#94A3B8")),
                yaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#94A3B8")),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with chart_col2:
            breakdown_data = []
            for r in top_roles:
                breakdown_data.append({
                    "Role": r["role_title"],
                    "Skill Coverage (60%)": r["skill_coverage_pct"] * 0.60,
                    "TF-IDF Semantic Match (30%)": r["cosine_similarity_pct"] * 0.30,
                    "Preferred Bonus (10%)": min(10.0, len(r.get("matched_preferred", [])) * 2.5)
                })
            b_df = pd.DataFrame(breakdown_data).set_index("Role")
            fig_stack = px.bar(
                b_df,
                barmode="stack",
                title="Mathematical Component Attribution",
                labels={"value": "Weighted Points", "Role": "Job Role"},
                color_discrete_sequence=["#27D3C2", "#648CFF", "#A78BFA"]
            )
            fig_stack.update_layout(
                paper_bgcolor="#171F32",
                plot_bgcolor="#171F32",
                font=dict(color="#F3F6FC", family="Plus Jakarta Sans"),
                height=430,
                margin=dict(l=10, r=20, t=40, b=10),
                xaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#94A3B8")),
                yaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#94A3B8")),
                legend=dict(font=dict(color="#94A3B8"))
            )
            st.plotly_chart(fig_stack, use_container_width=True)


# =============================================================
# VIEW 4: SKILL GAP ANALYSIS
# =============================================================
elif nav_option == "🔍 Skill Gap Analysis":
    st.markdown("### 🔍 Granular Skill Gap & Competency Analysis")

    if not results:
        st.warning("Please upload a resume or select a benchmark sample first.")
    else:
        all_role_titles = [r["role_title"] for r in results["all_matches"]]
        selected_role_title = st.selectbox(
            "Select Target Role to Benchmark Against:",
            all_role_titles,
            index=0
        )

        selected_role = next((r for r in results["all_matches"] if r["role_title"] == selected_role_title), results["primary_role"])

        col_role_details, col_gauge = st.columns([1.3, 1.7])

        with col_role_details:
            st.markdown(
                f"""
                <div class="saas-panel" style="height:100%;">
                    <h3 style="color:#F3F6FC; margin:0 0 4px 0;">{selected_role['role_title']}</h3>
                    <div style="font-size:0.8rem; color:#27D3C2; margin-bottom:12px;">{selected_role['category']} &bull; {selected_role['experience_level']}</div>
                    <p style="font-size:0.84rem; color:#94A3B8; line-height:1.5;">{selected_role['description']}</p>
                    <hr style="border:0; border-top:1px solid rgba(255,255,255,0.06); margin:12px 0;"/>
                    <div style="font-size:0.8rem; color:#ADC3FF;"><b>Min Education:</b> {selected_role['min_education']}</div>
                    <div style="font-size:0.8rem; color:#ADC3FF;"><b>Typical Compensation:</b> {selected_role['avg_salary']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_gauge:
            score_val = selected_role["match_score"]
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score_val,
                title={"text": f"<b>{selected_role['role_title']} Readiness</b>", "font": {"size": 16, "color": "#F3F6FC"}},
                number={"suffix": "%", "font": {"size": 38, "color": "#27D3C2", "family": "Plus Jakarta Sans"}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#232F4A", "tickfont": {"color": "#94A3B8"}},
                    "bar": {"color": "#27D3C2"},
                    "bgcolor": "#111827",
                    "borderwidth": 1,
                    "bordercolor": "#232F4A",
                    "steps": [
                        {"range": [0, 40], "color": "rgba(244, 63, 94, 0.15)"},
                        {"range": [40, 65], "color": "rgba(245, 158, 11, 0.15)"},
                        {"range": [65, 80], "color": "rgba(100, 140, 255, 0.15)"},
                        {"range": [80, 100], "color": "rgba(39, 211, 194, 0.18)"}
                    ],
                    "threshold": {"line": {"color": "#27D3C2", "width": 3}, "thickness": 0.8, "value": 75}
                }
            ))
            fig_g.update_layout(
                paper_bgcolor="#171F32",
                plot_bgcolor="#171F32",
                height=260,
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig_g, use_container_width=True)

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        
        # Matched vs Missing Skills Badges Grid
        col_m, col_g = st.columns(2)

        with col_m:
            st.markdown(
                f"""
                <div class="saas-panel" style="border-top: 3px solid #27D3C2; height:100%;">
                    <div class="saas-panel-header">
                        <h4 class="saas-panel-title">✅ Matched Required Skills ({len(selected_role['matched_skills'])})</h4>
                        <span class="tier-badge tier-excellent">VERIFIED</span>
                    </div>
                """,
                unsafe_allow_html=True
            )
            if selected_role['matched_skills']:
                tags = " ".join([f"<span class='skill-tag-matched'>✓ {s}</span>" for s in selected_role['matched_skills']])
                st.markdown(tags, unsafe_allow_html=True)
            else:
                st.info("No direct skill matches found for this role.")

            if selected_role.get("matched_preferred"):
                st.markdown("<br/><span style='font-size:0.8rem; font-weight:700; color:#C4B5FD;'>★ BONUS PREFERRED SKILLS DETECTED:</span>", unsafe_allow_html=True)
                pref_tags = " ".join([f"<span class='skill-tag-preferred'>★ {s}</span>" for s in selected_role['matched_preferred']])
                st.markdown(pref_tags, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with col_g:
            st.markdown(
                f"""
                <div class="saas-panel" style="border-top: 3px solid #F59E0B; height:100%;">
                    <div class="saas-panel-header">
                        <h4 class="saas-panel-title">❌ Missing Skills to Bridge ({len(selected_role['missing_skills'])})</h4>
                        <span class="tier-badge tier-moderate">ACTION REQUIRED</span>
                    </div>
                """,
                unsafe_allow_html=True
            )
            if selected_role['missing_skills']:
                missing_tags = " ".join([f"<span class='skill-tag-missing'>✗ {s}</span>" for s in selected_role['missing_skills']])
                st.markdown(missing_tags, unsafe_allow_html=True)
                st.caption("Strategic gaps to bridge in your learning roadmap below.")
            else:
                st.success("🎉 Exceptional alignment! You possess 100% of the core competencies for this role.")

            st.markdown("</div>", unsafe_allow_html=True)

        # Resume Improvement Suggestions
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        with st.expander("💡 Resume Improvement Suggestions", expanded=False):
            st.markdown(
                """
                <div class="saas-panel" style="border-left: 3px solid #648CFF;">
                    <div class="saas-panel-header">
                        <h4 class="saas-panel-title">🎯 Actionable Resume Enhancement Tips</h4>
                        <span class="tier-badge tier-good">AI-GENERATED</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            suggestions = []

            # Suggestion 1: Missing skills
            if selected_role['missing_skills']:
                missing_str = ", ".join(selected_role['missing_skills'][:3])
                suggestions.append({
                    "icon": "🔧",
                    "title": "Bridge Critical Skill Gaps",
                    "desc": f"Your resume lacks {len(selected_role['missing_skills'])} required skills for {selected_role['role_title']}: {missing_str}. Add these to your 'Skills' section or create projects demonstrating them.",
                    "priority": "High"
                })
            else:
                suggestions.append({
                    "icon": "✅",
                    "title": "Perfect Skill Alignment",
                    "desc": f"You already possess all required skills for {selected_role['role_title']}. Focus on quantifying your impact with metrics (e.g., 'reduced latency by 40%', 'improved accuracy by 15%').",
                    "priority": "Medium"
                })

            # Suggestion 2: Quantify achievements
            suggestions.append({
                "icon": "📊",
                "title": "Quantify Your Impact",
                "desc": "Replace vague descriptions with measurable outcomes. Example: 'Built a dashboard' → 'Built a Power BI dashboard reducing reporting time by 60% for 50+ stakeholders.'",
                "priority": "High"
            })

            # Suggestion 3: Keyword optimization
            if selected_role['missing_skills']:
                missing_keywords = ", ".join(selected_role['missing_skills'][:2])
                suggestions.append({
                    "icon": "🔍",
                    "title": "Optimize for ATS Keywords",
                    "desc": f"Applicant Tracking Systems scan for exact keywords. Naturally incorporate '{missing_keywords}' into your experience bullets, not just the skills section.",
                    "priority": "Medium"
                })

            # Suggestion 4: Project showcase
            projects = results['profile'].get('projects', [])
            if len(projects) < 2:
                suggestions.append({
                    "icon": "🚀",
                    "title": "Add More Projects",
                    "desc": "Include 2-3 substantial projects with tech stacks, problem statements, and measurable outcomes. Projects demonstrate practical application beyond coursework.",
                    "priority": "Medium"
                })
            else:
                suggestions.append({
                    "icon": "🚀",
                    "title": "Strengthen Project Descriptions",
                    "desc": "For each project, add: (1) Problem you solved, (2) Your specific contribution, (3) Technologies used, (4) Measurable result or impact.",
                    "priority": "Low"
                })

            # Suggestion 5: Tailor to role
            suggestions.append({
                "icon": "🎯",
                "title": "Tailor Resume Per Application",
                "desc": f"Create a customized version of your resume for each {selected_role['role_title']} application. Emphasize relevant projects and reorder skills to match the job description.",
                "priority": "High"
            })

            # Display suggestions
            for sug in suggestions:
                priority_color = {"High": "#F59E0B", "Medium": "#648CFF", "Low": "#94A3B8"}[sug["priority"]]
                st.markdown(
                    f"""
                    <div class="saas-panel" style="margin-bottom:10px; border-left: 3px solid {priority_color};">
                        <div style="display:flex; align-items:flex-start; gap:12px;">
                            <div style="font-size:1.5rem;">{sug['icon']}</div>
                            <div style="flex:1;">
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                                    <span style="font-weight:700; color:#F3F6FC; font-size:0.9rem;">{sug['title']}</span>
                                    <span style="font-size:0.7rem; font-weight:700; color:{priority_color}; text-transform:uppercase;">{sug['priority']} Priority</span>
                                </div>
                                <div style="font-size:0.82rem; color:#94A3B8; line-height:1.5;">{sug['desc']}</div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.caption("💡 These suggestions are generated based on skill gap analysis and industry best practices. Always tailor your resume to the specific job description.")


# =============================================================
# VIEW 5: LEARNING ROADMAP
# =============================================================
elif nav_option == "🗺️ Learning Roadmap":
    st.markdown("### 🗺️ Tailored Strategic Upskilling Roadmap")

    if not results:
        st.warning("Please upload a resume or select a benchmark sample first.")
    else:
        all_role_titles = [r["role_title"] for r in results["all_matches"]]
        active_target_title = st.selectbox(
            "Select Target Role for Upskilling Strategy:",
            all_role_titles,
            index=0
        )

        active_target_role = next((r for r in results["all_matches"] if r["role_title"] == active_target_title), results["primary_role"])
        roadmap = roadmap_gen.generate_roadmap(active_target_role, results["detected_skills"])

        st.markdown(
            f"""
            <div class="saas-panel" style="background:rgba(39, 211, 194, 0.05); border-color:rgba(39, 211, 194, 0.25);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-size:0.75rem; font-weight:700; color:#27D3C2; text-transform:uppercase; letter-spacing:0.04em;">Target Strategic Milestone</div>
                        <h3 style="color:#F3F6FC; margin:2px 0 0 0;">{roadmap['target_role']}</h3>
                    </div>
                    <div style="text-align:right;">
                        <span style="font-size:1.3rem; font-weight:800; color:#27D3C2;">~{roadmap['total_estimated_hours']} hrs</span>
                        <div style="font-size:0.75rem; color:#94A3B8;">Across ~{roadmap['estimated_weeks']} weeks (15 hrs/wk)</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Vertical Timeline Node Layout
        st.markdown("#### ⏳ Structured Curriculum Timeline")
        for phase in roadmap["phases"]:
            if phase.get("skills"):
                st.markdown(
                    f"""
                    <div class="timeline-node">
                        <div class="timeline-dot"></div>
                        <div style="font-size:0.8rem; font-weight:700; color:#648CFF; text-transform:uppercase;">
                            {phase['duration']}
                        </div>
                        <h4 style="color:#F3F6FC; margin:2px 0 4px 0;">{phase['phase_name']}</h4>
                        <div style="font-size:0.82rem; color:#94A3B8; margin-bottom:12px;">{phase['objective']}</div>
                    """,
                    unsafe_allow_html=True
                )

                sk_cols = st.columns(min(3, len(phase["skills"])))
                for s_idx, s in enumerate(phase["skills"]):
                    with sk_cols[s_idx % len(sk_cols)]:
                        st.markdown(
                            f"""
                            <div style="background:#111827; border:1px solid #232F4A; border-radius:10px; padding:12px 14px; margin-bottom:8px;">
                                <div style="font-weight:700; color:#27D3C2; font-size:0.92rem;">{s['skill_name']}</div>
                                <div style="font-size:0.75rem; color:#94A3B8; margin:2px 0 6px 0;">{s['category']} &bull; ~{s['estimated_learning_hours']} hrs</div>
                                <div style="font-size:0.78rem; color:#ADC3FF; margin-bottom:6px;"><b>Course:</b> {s['free_course']}</div>
                                <a href="{s['doc_url']}" target="_blank" style="font-size:0.75rem; color:#648CFF; text-decoration:none; font-weight:600;">
                                    📖 Official Docs &rarr;
                                </a>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                st.markdown("</div>", unsafe_allow_html=True)

        # Capstone Portfolio Projects
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="saas-panel-header">
                <h4 class="saas-panel-title">🏆 Portfolio Capstone Projects (STAR Format)</h4>
                <span style="font-size:0.78rem; color:#94A3B8;">Demonstrate verified mastery to recruiters</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        p_cols = st.columns(3)
        for p_idx, p in enumerate(roadmap["capstone_projects"]):
            with p_cols[p_idx]:
                st.markdown(
                    f"""
                    <div class="saas-panel" style="height:100%; display:flex; flex-direction:column; justify-content:space-between;">
                        <div>
                            <h4 style="color:#F3F6FC; margin:0 0 6px 0;">{p['title']}</h4>
                            <p style="font-size:0.82rem; color:#94A3B8; margin-bottom:10px;">{p['concept']}</p>
                            <div style="background:#111827; border-radius:6px; padding:6px 10px; font-size:0.78rem; color:#27D3C2; margin-bottom:10px;">
                                <b>Tech Stack:</b> {p['tech_stack']}
                            </div>
                            <div style="font-size:0.78rem; color:#ADC3FF;">{p['key_features']}</div>
                        </div>
                        <div style="background:#111827; border-left:3px solid #648CFF; padding:8px 10px; border-radius:4px; font-size:0.75rem; color:#F3F6FC; margin-top:12px;">
                            <b>Resume Bullet:</b><br/><i>"{p['resume_bullet_sample']}"</i>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =============================================================
# VIEW 6: ANALYSIS HISTORY
# =============================================================
elif nav_option == "📜 Analysis History":
    st.markdown("### 📜 Session History & Audit Trail (SQLite)")
    st.caption("Demonstrating local database integration (strictly anonymized; zero candidate resume text or PII stored):")

    try:
        recent_logs = db_mgr.get_recent_analyses(limit=25)
        if recent_logs:
            df_logs = pd.DataFrame(recent_logs)
            st.dataframe(df_logs, use_container_width=True, hide_index=True)
        else:
            st.info("No session records found in local database.")
    except Exception as e:
        st.warning(f"Database error: {e}")


# =============================================================
# VIEW 7: JOB & SKILL CATALOG
# =============================================================
elif nav_option == "⚙️ Job & Skill Catalog":
    st.markdown("### ⚙️ Benchmark Knowledge Base")
    st.caption("Explore the 10 enterprise target roles and 60 verified technical skills powering the platform.")

    cat_tab1, cat_tab2 = st.tabs(["💼 Enterprise Job Roles (10)", "🛠️ Verified Skills Taxonomy (60)"])

    with cat_tab1:
        st.dataframe(
            job_matcher.roles_df[[
                "role_id", "role_title", "category", "experience_level",
                "avg_salary", "required_skills", "preferred_skills"
            ]],
            use_container_width=True,
            hide_index=True
        )

    with cat_tab2:
        skills_df = skill_extractor.skills_df
        categories = ["All Domains"] + sorted(list(skills_df["category"].dropna().unique()))
        selected_cat = st.selectbox("Domain Filter:", categories)
        
        filtered = skills_df if selected_cat == "All Domains" else skills_df[skills_df["category"] == selected_cat]
        st.dataframe(
            filtered[[
                "skill_id", "skill_name", "category", "difficulty_level",
                "estimated_learning_hours", "free_course", "doc_url"
            ]],
            use_container_width=True,
            hide_index=True
        )


# =============================================================
# VIEW 8: DOWNLOAD REPORT
# =============================================================
elif nav_option == "📥 Download Report":
    st.markdown("### 📥 Publication-Ready Diagnostic Reports")

    if not results:
        st.warning("Please upload a resume or select a benchmark sample first.")
    else:
        d_col1, d_col2 = st.columns(2)

        with d_col1:
            st.markdown(
                """
                <div class="saas-panel" style="text-align:center; padding:28px 20px;">
                    <div style="font-size:2.5rem; margin-bottom:8px;">📄</div>
                    <h3 style="color:#F3F6FC; margin:0 0 6px 0;">Executive PDF Report</h3>
                    <p style="font-size:0.84rem; color:#94A3B8; margin-bottom:16px;">
                        Branded report with candidate profile, match scores, skill gap tables, roadmap, and compliance statements.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            with st.spinner("Compiling PDF bytes..."):
                payload = {
                    "candidate_name": results["candidate_name"],
                    "file_name": results["file_name"],
                    "file_type": results["file_type"],
                    "timestamp": results["timestamp"],
                    "detected_skills": results["detected_skills"],
                    "skills_by_category": results["skills_by_category"],
                    "profile": results["profile"],
                    "top_roles": results["top_roles"],
                    "roadmap": results["roadmap"]
                }
                pdf_bytes = generate_pdf_report(payload)

            clean_filename = f"Career_Intelligence_Report_{results['candidate_name'].replace(' ', '_')}.pdf"
            st.download_button(
                label="⬇️ Download Executive PDF",
                data=pdf_bytes,
                file_name=clean_filename,
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )

        with d_col2:
            st.markdown(
                """
                <div class="saas-panel" style="text-align:center; padding:28px 20px;">
                    <div style="font-size:2.5rem; margin-bottom:8px;">📝</div>
                    <h3 style="color:#F3F6FC; margin:0 0 6px 0;">Structured Markdown</h3>
                    <p style="font-size:0.84rem; color:#94A3B8; margin-bottom:16px;">
                        Lightweight plain-text and GitHub-flavored markdown export for offline analysis and developer documentation.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            md_content = generate_markdown_report(payload)
            clean_md_filename = f"Career_Intelligence_Report_{results['candidate_name'].replace(' ', '_')}.md"
            st.download_button(
                label="⬇️ Download Markdown Report",
                data=md_content,
                file_name=clean_md_filename,
                mime="text/markdown",
                type="secondary",
                use_container_width=True
            )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        with st.expander("👁️ Live Markdown Report Preview", expanded=True):
            st.markdown(md_content)

        # Save reports to persistent reports/ directory
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
        os.makedirs(reports_dir, exist_ok=True)

        if st.button("💾 Save Reports to Project Folder", type="secondary", use_container_width=True):
            pdf_path = os.path.join(reports_dir, clean_filename)
            md_path = os.path.join(reports_dir, clean_md_filename)
            try:
                with open(pdf_path, "wb") as f:
                    f.write(pdf_bytes)
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(md_content)
                st.success(f"Reports saved to `reports/` folder:\n- `{clean_filename}`\n- `{clean_md_filename}`")
            except Exception as e:
                st.error(f"Failed to save reports: {e}")


# =============================================================
# VIEW 9: PRIVACY & COMPLIANCE
# =============================================================
elif nav_option == "⚖️ Privacy & Compliance":
    st.markdown("### ⚖️ Ethical AI, Privacy Guarantees & Mathematical Formulation")

    st.markdown(
        """
        <div class="saas-panel" style="border-left: 3px solid #27D3C2;">
            <div style="font-size:0.85rem; font-weight:700; color:#27D3C2; text-transform:uppercase; letter-spacing:0.04em; margin-bottom:4px;">
                Advisory Scope & Compliance Notice
            </div>
            <div style="font-size:0.88rem; color:#F3F6FC; line-height:1.5;">
                This platform is an educational qualification-diagnostic tool. Matching scores reflect heuristic cosine similarities 
                and skill coverage indices rather than automated hiring decisions. Demographic attributes (gender, age, marital status, 
                nationality, religion) are strictly excluded from evaluation. Missing keywords do not always indicate missing ability — 
                candidates may possess equivalent competencies expressed through different terminology or experience.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    c_col1, c_col2 = st.columns(2)

    with c_col1:
        st.markdown(
            """
            <div class="saas-panel" style="height:100%;">
                <h4 style="color:#F3F6FC; margin:0 0 8px 0;">🛡️ Privacy & Anti-Bias Pipeline</h4>
                <ul style="font-size:0.84rem; color:#94A3B8; line-height:1.6; padding-left:16px;">
                    <li><b>Zero Persistent Storage:</b> Processed entirely in volatile RAM streams.</li>
                    <li><b>Demographic Stripper:</b> Active regex scrubbing removes age, gender, marital status, and religion before feature extraction.</li>
                    <li><b>Algorithmic Transparency:</b> Match scores provide explicit breakdowns of matched vs missing competencies.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c_col2:
        st.markdown(
            """
            <div class="saas-panel" style="height:100%;">
                <h4 style="color:#F3F6FC; margin:0 0 8px 0;">📐 Mathematical Formulation</h4>
                <div style="font-size:0.82rem; color:#94A3B8; line-height:1.6;">
                    $$\\mathcal{S}_{\\text{match}} = 0.60 \\cdot \\mathcal{C}_{\\text{skills}} + 0.30 \\cdot \\mathcal{S}_{\\text{tfidf}} + 0.10 \\cdot \\mathcal{B}_{\\text{pref}}$$
                    <br/>
                    • <b>60% Skill Matrix Coverage:</b> Jaccard overlap of mandatory technical skills.<br/>
                    • <b>30% TF-IDF Cosine Similarity:</b> Contextual document alignment.<br/>
                    • <b>10% Preferred Bonus:</b> Nice-to-have secondary competencies.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
