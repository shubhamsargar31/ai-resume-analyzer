"""
AI Resume Analyzer & Job Recommendation System
Main Streamlit Application
"""

import os
import io
import time
from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import core system modules
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
    page_title="AI Resume Analyzer & Job Matcher",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Professional CSS Styling
CUSTOM_CSS = """
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Container Padding */
    .main .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }

    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 50%, #0D9488 100%);
        color: white;
        padding: 24px 32px;
        border-radius: 14px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.25);
    }
    .hero-banner h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0 0 8px 0;
        color: #FFFFFF !important;
    }
    .hero-banner p {
        font-size: 1.05rem;
        opacity: 0.95;
        margin: 0;
        color: #E2E8F0 !important;
    }

    /* Metric Cards */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
    }
    .metric-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        font-weight: 600;
        color: #6B7280;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #111827;
    }
    .metric-subtitle {
        font-size: 0.82rem;
        color: #059669;
        margin-top: 4px;
    }

    /* Skill Badges */
    .badge-matched {
        display: inline-block;
        background-color: #DEF7EC;
        color: #03543F;
        border: 1px solid #BCF0DA;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 3px 4px;
    }
    .badge-missing {
        display: inline-block;
        background-color: #FDE8E8;
        color: #9B1C1C;
        border: 1px solid #F8B4B4;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 3px 4px;
    }
    .badge-skill {
        display: inline-block;
        background-color: #EBF5FF;
        color: #1E429F;
        border: 1px solid #C3DDFD;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 500;
        margin: 3px 4px;
    }
    .badge-preferred {
        display: inline-block;
        background-color: #FEF3C7;
        color: #92400E;
        border: 1px solid #FDE68A;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 3px 4px;
    }

    /* Card Panels */
    .custom-card {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* Status Pill */
    .status-pill {
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }

    /* Ethical banner */
    .ethical-banner {
        background-color: #F8FAFC;
        border-left: 4px solid #0D9488;
        padding: 12px 16px;
        border-radius: 6px;
        font-size: 0.88rem;
        color: #334155;
        margin-bottom: 16px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


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
    st.session_state.active_tab = "Dashboard & Upload"


# Helper function to run analysis
def run_analysis(file_object, file_name: str):
    """Executes the complete end-to-end analysis workflow."""
    with st.spinner("Processing resume..."):
        progress_bar = st.progress(0, text="Reading and extracting text...")
        
        # 1. Text Extraction
        try:
            raw_text, file_type = extract_resume_text(file_object, file_name=file_name)
        except ResumeExtractionError as e:
            st.error(f"Extraction Error: {str(e)}")
            return
        except Exception as e:
            st.error(f"Unexpected file error: {str(e)}")
            return

        progress_bar.progress(25, text="Normalizing & segmenting resume sections...")
        
        # 2. Text Cleaning & Privacy Sanitization
        sanitized_text = sanitize_protected_data(raw_text)
        cleaned_text = clean_text(sanitized_text)
        sections = extract_sections(cleaned_text)
        contact_info = extract_contact_info(raw_text)

        progress_bar.progress(50, text="Detecting technical skills & profile attributes...")
        
        # 3. Skill & Profile Extraction
        skill_data = skill_extractor.extract_skills(cleaned_text)
        detected_skills = skill_data["detected_skills"]
        profile_data = extract_full_profile(cleaned_text, sections)

        progress_bar.progress(75, text="Calculating TF-IDF similarities & role matches...")
        
        # 4. Job Matching & Recommendations
        recommendations = recommender.recommend_top_roles(cleaned_text, detected_skills, top_n=3)
        top_roles = recommendations["top_recommendations"]
        primary_role = top_roles[0] if top_roles else {}

        # 5. Roadmap Generation
        roadmap = roadmap_gen.generate_roadmap(primary_role, detected_skills)

        progress_bar.progress(95, text="Finalizing analysis report...")
        
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
            pass # Silent log fail to never interrupt user experience

        progress_bar.progress(100, text="Analysis Complete!")
        time.sleep(0.3)
        progress_bar.empty()
        
        st.session_state.analysis_results = results
        st.success("Resume successfully analyzed! Explore the tabs above to view recommendations.")


# SIDEBAR
with st.sidebar:
    st.markdown("### 💼 AI Resume Analyzer")
    st.caption("Intelligent Career Recommendation Engine")
    st.markdown("---")

    # Sample Resumes for Quick Testing & Evaluation
    st.markdown("#### ⚡ Quick Demo Samples")
    st.caption("Select a pre-built anonymized resume to test immediately:")

    samples_dir = os.path.join(os.path.dirname(__file__), "sample_resumes")
    sample_files = {
        "Data Scientist (PDF)": "sample_data_scientist.pdf",
        "Full Stack Developer (PDF)": "sample_full_stack_dev.pdf",
        "DevOps Engineer (PDF)": "sample_devops_engineer.pdf",
        "Frontend Developer (DOCX)": "sample_frontend_developer.docx",
        "Data Analyst (DOCX)": "sample_data_analyst.docx"
    }

    selected_sample = st.selectbox(
        "Choose a sample resume:",
        ["-- Select Sample --"] + list(sample_files.keys()),
        index=0
    )

    if st.button("Load & Analyze Sample", type="secondary", use_container_width=True):
        if selected_sample != "-- Select Sample --":
            sample_rel_path = os.path.join(samples_dir, sample_files[selected_sample])
            if os.path.exists(sample_rel_path):
                with open(sample_rel_path, "rb") as f:
                    file_bytes = io.BytesIO(f.read())
                run_analysis(file_bytes, sample_files[selected_sample])
            else:
                st.error("Sample file not found on disk.")
        else:
            st.warning("Please choose a sample resume from the dropdown.")

    st.markdown("---")
    
    # Navigation Radio
    st.markdown("#### 🧭 Navigation")
    nav_option = st.radio(
        "Go to Section:",
        [
            "🚀 Dashboard & Upload",
            "🎯 Job Recommendations",
            "🔍 Skill Gap Analysis",
            "🗺️ Learning Roadmap",
            "📊 Job & Skill Database",
            "📥 Download Report",
            "⚖️ Ethical AI & Privacy"
        ],
        index=0
    )

    st.markdown("---")
    st.markdown(
        """
        <div style='font-size:0.78rem; color:#6B7280; text-align:center;'>
            <b>AI Resume Analyzer v1.0.0</b><br/>
            Engineered with Streamlit, Scikit-learn & TF-IDF.<br/>
            <i>College Major Project Submission</i>
        </div>
        """,
        unsafe_allow_html=True
    )


# MAIN APP HEADER
st.markdown(
    """
    <div class="hero-banner">
        <h1>AI Resume Analyzer & Job Recommendation System</h1>
        <p>Automated multi-format resume parsing, TF-IDF cosine similarity job matching, skill gap diagnostics, and personalized upskilling roadmaps.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Render View Based on Navigation Option
results = st.session_state.analysis_results

# -------------------------------------------------------------
# TAB 1: DASHBOARD & UPLOAD
# -------------------------------------------------------------
if nav_option == "🚀 Dashboard & Upload":
    st.markdown("### 📤 Upload Resume")
    
    col_up, col_info = st.columns([1.8, 1.2])

    with col_up:
        uploaded_file = st.file_uploader(
            "Upload your resume in PDF or DOCX format",
            type=["pdf", "docx"],
            help="Upload a standard PDF or Microsoft Word document (max 10MB)."
        )

        if uploaded_file is not None:
            st.info(f"📁 Selected File: **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")
            if st.button("🚀 Analyze Resume", type="primary", use_container_width=True):
                run_analysis(uploaded_file, uploaded_file.name)

    with col_info:
        st.markdown(
            """
            <div class="custom-card">
                <h4 style="margin-top:0; color:#1E3A8A;">🔒 Privacy & System Guarantees</h4>
                <ul style="font-size:0.88rem; color:#374151; padding-left:18px; margin-bottom:0;">
                    <li><b>In-Memory Parsing:</b> Your resume is processed directly in RAM and never saved to public storage.</li>
                    <li><b>Bias-Free NLP:</b> Gender, age, marital status, race, and photos are strictly excluded from scoring.</li>
                    <li><b>Multi-Format:</b> Native support for both <code>.pdf</code> and <code>.docx</code> formats.</li>
                    <li><b>Scientific Matching:</b> Hybrid TF-IDF vectorization paired with exact skill matrix coverage.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    # If results are ready, show Extracted Profile & Skills
    if results:
        st.markdown("---")
        st.markdown("### 👤 Parsed Candidate Profile")
        
        p_col1, p_col2, p_col3, p_col4 = st.columns(4)
        
        prof = results["profile"]
        edu = prof.get("education", {})
        exp = prof.get("experience", {})
        
        with p_col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Identified Skills</div>
                    <div class="metric-value">{results['skill_count']}</div>
                    <div class="metric-subtitle">Across {len(results['skills_by_category'])} domains</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with p_col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Primary Degree</div>
                    <div class="metric-value" style="font-size:1.15rem; font-weight:600; min-height:48px;">
                        {edu.get('primary_degree', 'B.Tech / B.S.')}
                    </div>
                    <div class="metric-subtitle">{edu.get('field_of_study', 'CS / Related')}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with p_col3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Experience Level</div>
                    <div class="metric-value">{exp.get('estimated_years', 0)} yrs</div>
                    <div class="metric-subtitle">{exp.get('seniority_level', 'Entry-Level')}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with p_col4:
            top_r = results["primary_role"]
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Top Role Alignment</div>
                    <div class="metric-value" style="color:#0D9488;">{top_r.get('match_score', 0)}%</div>
                    <div class="metric-subtitle">{top_r.get('role_title', 'Analyzing')}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Categorized Skills Section
        st.markdown("#### 🛠️ Detected Technical Skills")
        by_cat = results["skills_by_category"]
        if by_cat:
            cat_cols = st.columns(len(by_cat))
            for idx, (category, skills) in enumerate(by_cat.items()):
                with cat_cols[idx % len(cat_cols)]:
                    st.markdown(f"**{category}** ({len(skills)})")
                    badges_html = " ".join([f"<span class='badge-skill'>{s}</span>" for s in skills])
                    st.markdown(badges_html, unsafe_allow_html=True)
                    st.write("")
        else:
            st.info("No predefined technical skills found. Check the extracted text below.")

        # Interactive Expander for Extracted Sections & Raw Text
        with st.expander("📄 View Parsed Resume Sections & Text Inspector"):
            t1, t2, t3 = st.tabs(["Structured Sections", "Cleaned Text", "Raw Extracted Text"])
            with t1:
                for sec, content in results["sections"].items():
                    if content.strip():
                        st.markdown(f"**{sec.upper()}**")
                        st.text(content[:800] + ("..." if len(content) > 800 else ""))
            with t2:
                st.text_area("Cleaned Text", results["cleaned_text"], height=200)
            with t3:
                st.text_area("Raw Text", results["raw_text"], height=200)

    else:
        st.markdown(
            """
            <div style="text-align:center; padding: 40px 20px; color:#6B7280;">
                <h4>No resume analyzed yet</h4>
                <p>Upload your resume using the box above or click <b>'Load & Analyze Sample'</b> in the sidebar to test immediately.</p>
            </div>
            """,
            unsafe_allow_html=True
        )


# -------------------------------------------------------------
# TAB 2: JOB RECOMMENDATIONS
# -------------------------------------------------------------
elif nav_option == "🎯 Job Recommendations":
    st.markdown("### 🎯 Top 3 Recommended Job Roles")
    
    if not results:
        st.warning("Please upload and analyze a resume first in the 'Dashboard & Upload' section or pick a demo sample.")
    else:
        top_roles = results["top_roles"]
        
        # 3 Top Recommendation Cards
        card_cols = st.columns(3)
        for i, role in enumerate(top_roles):
            with card_cols[i]:
                score = role["match_score"]
                tier_color = "#059669" if score >= 75 else ("#2563EB" if score >= 55 else ("#D97706" if score >= 35 else "#DC2626"))
                
                st.markdown(
                    f"""
                    <div class="custom-card" style="border-top: 4px solid {tier_color}; min-height: 380px;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:0.85rem; font-weight:700; color:#6B7280;">RANK #{i+1}</span>
                            <span style="background:{tier_color}20; color:{tier_color}; font-size:0.75rem; font-weight:700; padding:2px 8px; border-radius:10px;">
                                {role['match_tier']}
                            </span>
                        </div>
                        <h3 style="margin: 8px 0 4px 0; color:#1E3A8A;">{role['role_title']}</h3>
                        <p style="font-size:0.82rem; color:#6B7280; margin-bottom:12px;">{role['category']} &bull; {role['avg_salary']}</p>
                        <div style="text-align:center; margin: 14px 0;">
                            <div style="font-size:2.8rem; font-weight:800; color:{tier_color}; line-height:1;">
                                {score}%
                            </div>
                            <div style="font-size:0.8rem; color:#6B7280;">Overall Match Index</div>
                        </div>
                        <div style="font-size:0.84rem; color:#374151; margin-bottom:12px;">
                            <b>Required Skills Matched:</b> {len(role['matched_skills'])} of {role['required_skills_count']} ({role['skill_coverage_pct']}%)
                        </div>
                        <div style="font-size:0.82rem; color:#4B5563; font-style:italic;">
                            "{role.get('readiness_desc', '')}"
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Plotly Score Comparison & Component Breakdown
        st.markdown("---")
        st.markdown("#### 📊 Matching Score Breakdown Across All Evaluated Roles")

        all_matches_df = pd.DataFrame(results["all_matches"])
        
        chart_col1, chart_col2 = st.columns([1.5, 1.2])

        with chart_col1:
            fig_bar = px.bar(
                all_matches_df.sort_values(by="match_score", ascending=True),
                x="match_score",
                y="role_title",
                orientation="h",
                text="match_score",
                title="Job Role Compatibility Index (%)",
                labels={"match_score": "Match Score (%)", "role_title": "Job Role"},
                color="match_score",
                color_continuous_scale="Viridis"
            )
            fig_bar.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_bar.update_layout(height=420, margin=dict(l=10, r=20, t=40, b=10))
            st.plotly_chart(fig_bar, use_container_width=True)

        with chart_col2:
            # Component breakdown for top 3 roles
            breakdown_data = []
            for r in top_roles:
                breakdown_data.append({
                    "Role": r["role_title"],
                    "Skill Coverage (60%)": r["skill_coverage_pct"] * 0.60,
                    "TF-IDF Semantic Match (30%)": r["cosine_similarity_pct"] * 0.30,
                    "Preferred Skills Bonus (10%)": min(10.0, len(r.get("matched_preferred", [])) * 2.5)
                })
            
            b_df = pd.DataFrame(breakdown_data).set_index("Role")
            fig_stack = px.bar(
                b_df,
                barmode="stack",
                title="Scoring Component Attribution",
                labels={"value": "Weighted Points", "Role": "Job Role"},
                color_discrete_sequence=["#3B82F6", "#10B981", "#F59E0B"]
            )
            fig_stack.update_layout(height=420, margin=dict(l=10, r=20, t=40, b=10))
            st.plotly_chart(fig_stack, use_container_width=True)


# -------------------------------------------------------------
# TAB 3: SKILL GAP ANALYSIS
# -------------------------------------------------------------
elif nav_option == "🔍 Skill Gap Analysis":
    st.markdown("### 🔍 In-Depth Skill Gap & Competency Analysis")

    if not results:
        st.warning("Please upload and analyze a resume first in the 'Dashboard & Upload' section or pick a demo sample.")
    else:
        # Allow user to choose ANY job role in database for gap analysis
        all_role_titles = [r["role_title"] for r in results["all_matches"]]
        selected_role_title = st.selectbox(
            "Select target job role to analyze skill requirements:",
            all_role_titles,
            index=0
        )

        selected_role = next((r for r in results["all_matches"] if r["role_title"] == selected_role_title), results["primary_role"])

        col_g1, col_g2 = st.columns([1.2, 1.8])

        with col_g1:
            st.markdown(
                f"""
                <div class="custom-card">
                    <h3 style="margin-top:0; color:#1E3A8A;">{selected_role['role_title']}</h3>
                    <p style="font-size:0.86rem; color:#4B5563;">{selected_role['description']}</p>
                    <hr style="margin:12px 0; border:0; border-top:1px solid #E5E7EB;"/>
                    <div style="margin-bottom:8px;"><b>Experience Level:</b> {selected_role['experience_level']}</div>
                    <div style="margin-bottom:8px;"><b>Minimum Education:</b> {selected_role['min_education']}</div>
                    <div style="margin-bottom:8px;"><b>Typical Compensation:</b> {selected_role['avg_salary']}</div>
                    <div style="margin-bottom:8px;"><b>Key Responsibilities:</b><br/>
                        <span style="font-size:0.82rem; color:#6B7280;">{selected_role['key_responsibilities']}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_g2:
            # Gauge chart for selected role match
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=selected_role["match_score"],
                title={"text": f"<b>{selected_role['role_title']} Match</b>", "font": {"size": 18}},
                number={"suffix": "%", "font": {"size": 36, "color": "#1E3A8A"}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "darkblue"},
                    "bar": {"color": "#3B82F6"},
                    "bgcolor": "white",
                    "borderwidth": 2,
                    "bordercolor": "#E5E7EB",
                    "steps": [
                        {"range": [0, 35], "color": "#FEE2E2"},
                        {"range": [35, 55], "color": "#FEF3C7"},
                        {"range": [55, 75], "color": "#DBEAFE"},
                        {"range": [75, 100], "color": "#D1FAE5"}
                    ],
                    "threshold": {
                        "line": {"color": "#059669", "width": 4},
                        "thickness": 0.75,
                        "value": 75
                    }
                }
            ))
            fig_gauge.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_gauge, use_container_width=True)

        st.markdown("---")
        
        # Matched vs Missing Skills Badges
        col_matched, col_missing = st.columns(2)

        with col_matched:
            st.markdown(
                f"""
                <div class="custom-card" style="border-top: 4px solid #10B981;">
                    <h4 style="color:#065F46; margin-top:0;">✅ Matched Required Skills ({len(selected_role['matched_skills'])})</h4>
                    <p style="font-size:0.82rem; color:#4B5563;">Skills successfully detected in your resume:</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            if selected_role['matched_skills']:
                matched_html = " ".join([f"<span class='badge-matched'>✓ {s}</span>" for s in selected_role['matched_skills']])
                st.markdown(matched_html, unsafe_allow_html=True)
            else:
                st.info("No direct skill matches found for this specific role.")

            if selected_role.get("matched_preferred"):
                st.markdown("<br/><b>⭐ Bonus Preferred Skills Matched:</b>", unsafe_allow_html=True)
                pref_html = " ".join([f"<span class='badge-preferred'>★ {s}</span>" for s in selected_role['matched_preferred']])
                st.markdown(pref_html, unsafe_allow_html=True)

        with col_missing:
            st.markdown(
                f"""
                <div class="custom-card" style="border-top: 4px solid #EF4444;">
                    <h4 style="color:#991B1B; margin-top:0;">❌ Missing Skills to Bridge ({len(selected_role['missing_skills'])})</h4>
                    <p style="font-size:0.82rem; color:#4B5563;">Skills required for this role not found on your resume:</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            if selected_role['missing_skills']:
                missing_html = " ".join([f"<span class='badge-missing'>✗ {s}</span>" for s in selected_role['missing_skills']])
                st.markdown(missing_html, unsafe_allow_html=True)
                st.caption("Tip: Add these to your study roadmap below to become a top candidate.")
            else:
                st.success("🎉 Outstanding! You meet 100% of the core required technical skills for this role.")


# -------------------------------------------------------------
# TAB 4: PERSONALIZED LEARNING ROADMAP
# -------------------------------------------------------------
elif nav_option == "🗺️ Learning Roadmap":
    st.markdown("### 🗺️ Personalized Upskilling Roadmap")

    if not results:
        st.warning("Please upload and analyze a resume first in the 'Dashboard & Upload' section or pick a demo sample.")
    else:
        # Target role selector for roadmap
        all_role_titles = [r["role_title"] for r in results["all_matches"]]
        active_target_title = st.selectbox(
            "Select target role for tailored roadmap:",
            all_role_titles,
            index=0
        )

        active_target_role = next((r for r in results["all_matches"] if r["role_title"] == active_target_title), results["primary_role"])
        roadmap = roadmap_gen.generate_roadmap(active_target_role, results["detected_skills"])

        # Overview Stats
        st.markdown(
            f"""
            <div class="custom-card" style="background:#F0FDF4; border: 1px solid #BBF7D0;">
                <h4 style="color:#166534; margin:0 0 6px 0;">🎯 Target Role: {roadmap['target_role']}</h4>
                <div style="font-size:0.9rem; color:#15803D;">
                    Estimated study investment: <b>~{roadmap['total_estimated_hours']} hours</b> across <b>~{roadmap['estimated_weeks']} weeks</b> (15 hrs/wk) to close {roadmap['missing_skills_count']} skill gaps.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if roadmap["perfect_match"]:
            st.balloons()
            st.success("🌟 You have 100% of the required skills for this role! Focus on system design, mock interviews, and advanced architecture.")

        # Display Phases
        for phase in roadmap["phases"]:
            skills_in_phase = phase["skills"]
            if skills_in_phase:
                with st.expander(f"📌 {phase['phase_name']} &bull; {phase['duration']}", expanded=True):
                    st.markdown(f"*{phase['objective']}*")
                    st.write("")
                    
                    skill_cols = st.columns(min(3, len(skills_in_phase)))
                    for idx, s in enumerate(skills_in_phase):
                        with skill_cols[idx % len(skill_cols)]:
                            st.markdown(
                                f"""
                                <div class="custom-card" style="border-left: 3px solid #3B82F6; margin-bottom:10px; padding:12px 14px;">
                                    <div style="font-weight:700; color:#1E3A8A; font-size:0.95rem;">{s['skill_name']}</div>
                                    <div style="font-size:0.75rem; color:#6B7280; margin: 2px 0 6px 0;">
                                        {s['category']} &bull; {s['difficulty_level']} &bull; ~{s['estimated_learning_hours']} hrs
                                    </div>
                                    <div style="font-size:0.8rem; margin-top:6px;">
                                        <b>Course:</b> <span style="color:#059669;">{s['free_course']}</span>
                                    </div>
                                    <div style="margin-top:8px;">
                                        <a href="{s['doc_url']}" target="_blank" style="font-size:0.78rem; text-decoration:none; color:#2563EB;">
                                            📖 Official Documentation &rarr;
                                        </a>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

        # Capstone Projects
        st.markdown("---")
        st.markdown("### 🏆 Recommended Capstone Portfolio Projects")
        st.caption("Build these projects to showcase your bridged skills directly on your resume and GitHub:")

        proj_cols = st.columns(3)
        for idx, p in enumerate(roadmap["capstone_projects"]):
            with proj_cols[idx]:
                st.markdown(
                    f"""
                    <div class="custom-card" style="min-height:360px;">
                        <h4 style="color:#1E3A8A; margin-top:0;">{p['title']}</h4>
                        <p style="font-size:0.82rem; color:#4B5563;">{p['concept']}</p>
                        <div style="font-size:0.8rem; color:#1E429F; background:#EFF6FF; padding:6px 10px; border-radius:6px; margin:10px 0;">
                            <b>Tech Stack:</b> {p['tech_stack']}
                        </div>
                        <div style="font-size:0.8rem; color:#374151;">
                            <b>Key Highlights:</b><br/>
                            <span style="font-size:0.78rem; color:#6B7280;">{p['key_features']}</span>
                        </div>
                        <div style="font-size:0.78rem; margin-top:12px; background:#F8FAFC; padding:8px; border-left:2px solid #0D9488;">
                            <b>Sample Resume Bullet:</b><br/>
                            <i>"{p['resume_bullet_sample']}"</i>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# -------------------------------------------------------------
# TAB 5: JOB & SKILL DATABASE
# -------------------------------------------------------------
elif nav_option == "📊 Job & Skill Database":
    st.markdown("### 📊 Explore Job Roles & Skill Dictionary")
    st.caption("Inspect the active benchmarking database powering the AI analyzer.")

    d_tab1, d_tab2 = st.tabs(["💼 Job Roles Catalog", "🛠️ Skill Dictionary"])

    with d_tab1:
        st.markdown("#### Built-in Target Job Roles")
        roles_df = job_matcher.roles_df
        st.dataframe(
            roles_df[[
                "role_id", "role_title", "category", "experience_level",
                "avg_salary", "required_skills", "preferred_skills"
            ]],
            use_container_width=True,
            hide_index=True
        )

    with d_tab2:
        st.markdown("#### Verified Skill Catalog & Learning Resources")
        skills_df = skill_extractor.skills_df
        
        # Category Filter
        categories = ["All"] + sorted(list(skills_df["category"].dropna().unique()))
        selected_cat = st.selectbox("Filter by Category:", categories)
        
        filtered_skills = skills_df if selected_cat == "All" else skills_df[skills_df["category"] == selected_cat]
        
        st.dataframe(
            filtered_skills[[
                "skill_id", "skill_name", "category", "difficulty_level",
                "estimated_learning_hours", "free_course", "doc_url"
            ]],
            use_container_width=True,
            hide_index=True
        )


# -------------------------------------------------------------
# TAB 6: DOWNLOAD REPORT
# -------------------------------------------------------------
elif nav_option == "📥 Download Report":
    st.markdown("### 📥 Download Resume Analysis Report")
    st.caption("Generate publication-ready PDF or formatted Markdown reports.")

    if not results:
        st.warning("Please upload and analyze a resume first in the 'Dashboard & Upload' section or pick a demo sample.")
    else:
        col_down1, col_down2 = st.columns(2)

        with col_down1:
            st.markdown(
                """
                <div class="custom-card" style="text-align:center; padding:30px 20px;">
                    <div style="font-size:2.5rem; margin-bottom:10px;">📄</div>
                    <h3 style="margin:0 0 8px 0; color:#1E3A8A;">Formal PDF Report</h3>
                    <p style="font-size:0.85rem; color:#6B7280; margin-bottom:20px;">
                        Complete analysis report generated via ReportLab including candidate profile, match scores, skill gap table, roadmap, and ethical AI notice.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Generate PDF in-memory
            with st.spinner("Generating PDF report..."):
                analysis_payload = {
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
                pdf_bytes = generate_pdf_report(analysis_payload)

            clean_filename = f"Resume_Analysis_{results['candidate_name'].replace(' ', '_')}.pdf"
            st.download_button(
                label="⬇️ Download PDF Report",
                data=pdf_bytes,
                file_name=clean_filename,
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )

        with col_down2:
            st.markdown(
                """
                <div class="custom-card" style="text-align:center; padding:30px 20px;">
                    <div style="font-size:2.5rem; margin-bottom:10px;">📝</div>
                    <h3 style="margin:0 0 8px 0; color:#0D9488;">Markdown / Text Summary</h3>
                    <p style="font-size:0.85rem; color:#6B7280; margin-bottom:20px;">
                        Lightweight plain-text and GitHub-flavored markdown export ideal for documentation, portfolio READMEs, or quick copy-pasting.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            md_content = generate_markdown_report(analysis_payload)
            clean_md_filename = f"Resume_Analysis_{results['candidate_name'].replace(' ', '_')}.md"
            st.download_button(
                label="⬇️ Download Markdown Report",
                data=md_content,
                file_name=clean_md_filename,
                mime="text/markdown",
                type="secondary",
                use_container_width=True
            )

        st.markdown("---")
        st.markdown("#### 👁️ Live Report Preview")
        with st.expander("Expand to preview Markdown Report text", expanded=True):
            st.markdown(md_content)


# -------------------------------------------------------------
# TAB 7: ETHICAL AI & PRIVACY
# -------------------------------------------------------------
elif nav_option == "⚖️ Ethical AI & Privacy":
    st.markdown("### ⚖️ Ethical AI, Privacy Guarantees & System Methodology")

    st.markdown(
        """
        <div class="ethical-banner">
            <b>Fundamental Principle:</b> This system is strictly an educational career-guidance and upskilling diagnostic tool.
            Matching percentages represent heuristic similarity indices rather than definitive employment decisions.
        </div>
        """,
        unsafe_allow_html=True
    )

    col_e1, col_e2 = st.columns(2)

    with col_e1:
        st.markdown(
            """
            <div class="custom-card">
                <h4 style="color:#1E3A8A; margin-top:0;">🛡️ Privacy & Anti-Bias Architecture</h4>
                <ul style="font-size:0.88rem; color:#374151; padding-left:18px;">
                    <li><b>Zero Persistent Storage:</b> Uploaded files are converted into in-memory Byte streams and discarded after the session ends.</li>
                    <li><b>Strict Exclusion of Protected Attributes:</b> Gender, age, date of birth, marital status, nationality, caste, and religion are sanitized before scoring.</li>
                    <li><b>No Facial or Photographic Analysis:</b> Resumes with headshots or images are handled strictly through raw text streams.</li>
                    <li><b>Transparent Algorithmic Rationale:</b> All match scores are accompanied by explicit lists of matched skills and missing skills.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_e2:
        st.markdown(
            """
            <div class="custom-card">
                <h4 style="color:#0D9488; margin-top:0;">📐 Mathematical Matching Methodology</h4>
                <p style="font-size:0.84rem; color:#374151;">
                    The system combines two complementary NLP techniques to guarantee both precision and semantic coverage:
                </p>
                <ol style="font-size:0.82rem; color:#374151; padding-left:18px;">
                    <li><b>Skill Matrix Coverage (60% weight):</b> Jaccard overlap between the candidate's verified skills and the mandatory requirements for the target role.</li>
                    <li><b>TF-IDF Cosine Similarity (30% weight):</b> Sublinear Term Frequency-Inverse Document Frequency vectorization measuring semantic alignment between the resume context and role responsibilities.</li>
                    <li><b>Preferred Skill Bonus (10% weight):</b> Incremental credit for possessing nice-to-have secondary competencies.</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Anonymized Analytics Table from SQLite
    st.markdown("---")
    st.markdown("#### 📈 Anonymized Session History (SQLite DB)")
    st.caption("Demonstrating local database integration (no personal resume text or contact details are logged):")
    
    try:
        recent_logs = db_mgr.get_recent_analyses(limit=10)
        if recent_logs:
            st.dataframe(pd.DataFrame(recent_logs), use_container_width=True, hide_index=True)
        else:
            st.info("No sessions logged yet in the database.")
    except Exception as e:
        st.warning(f"Could not load database records: {e}")
