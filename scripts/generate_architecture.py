"""
Generates high-resolution standalone architecture diagram files:
- architecture.png (High-DPI PNG)
- architecture.pdf (Publication-quality Vector PDF)
"""

import os
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PNG_PATH = os.path.join(ROOT_DIR, "architecture.png")
PDF_PATH = os.path.join(ROOT_DIR, "architecture.pdf")


def generate_png():
    width, height = 1800, 1100
    img = Image.new("RGBA", (width, height), (248, 250, 252, 255))
    draw = ImageDraw.Draw(img)

    # Palette
    c_primary = (30, 58, 138, 255)     # Deep Navy
    c_secondary = (13, 148, 136, 255)  # Teal
    c_blue = (59, 130, 246, 255)       # Blue
    c_dark = (31, 41, 55, 255)         # Charcoal text
    c_muted = (107, 114, 128, 255)     # Gray text
    c_card_bg = (255, 255, 255, 255)   # White card
    c_card_border = (229, 231, 235, 255)
    c_accent_green = (16, 185, 129, 255)
    c_accent_amber = (245, 158, 11, 255)

    # Load default or fallback font
    try:
        font_title = ImageFont.truetype("arial.ttf", 36)
        font_subtitle = ImageFont.truetype("arial.ttf", 20)
        font_stage = ImageFont.truetype("arialbd.ttf", 20)
        font_box_title = ImageFont.truetype("arialbd.ttf", 16)
        font_box_desc = ImageFont.truetype("arial.ttf", 13)
        font_badge = ImageFont.truetype("arialbd.ttf", 12)
    except Exception:
        font_title = ImageFont.load_default()
        font_subtitle = font_title
        font_stage = font_title
        font_box_title = font_title
        font_box_desc = font_title
        font_badge = font_title

    # Top Header Banner
    draw.rectangle([(0, 0), (width, 110)], fill=c_primary)
    draw.text((60, 25), "AI Resume Analyzer & Job Recommendation System", fill=(255, 255, 255, 255), font=font_title)
    draw.text((60, 70), "End-to-End System Workflow Architecture: Parsing, TF-IDF Cosine Similarity & Upskilling", fill=(203, 213, 225, 255), font=font_subtitle)

    # 4 Columns / Pipeline Stages
    stages = [
        ("STAGE 1: Ingestion & Privacy", 60, 380),
        ("STAGE 2: Feature Extraction", 480, 800),
        ("STAGE 3: Hybrid Matching", 900, 1220),
        ("STAGE 4: Outputs & Roadmap", 1320, 1740)
    ]

    for title, x1, x2 in stages:
        draw.rectangle([(x1, 140), (x2, 175)], fill=c_secondary)
        draw.text((x1 + 15, 146), title, fill=(255, 255, 255, 255), font=font_stage)

    def draw_card(x1, y1, x2, y2, title, bullets, border_accent=c_blue):
        # Card shadow & body
        draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=10, fill=c_card_bg, outline=c_card_border, width=2)
        # Left accent stripe
        draw.rounded_rectangle([(x1, y1), (x1 + 6, y2)], radius=3, fill=border_accent)
        # Title
        draw.text((x1 + 18, y1 + 14), title, fill=c_primary, font=font_box_title)
        # Bullets
        curr_y = y1 + 42
        for b in bullets:
            draw.text((x1 + 18, curr_y), f"• {b}", fill=c_dark, font=font_box_desc)
            curr_y += 22

    # STAGE 1 CARDS
    draw_card(60, 200, 380, 360, "Resume Upload (In-Memory)", [
        "Native PDF Stream Ingestion (pypdf)",
        "Microsoft Word Ingestion (python-docx)",
        "Byte-Stream Memory Buffering",
        "Zero Persistent Disk Storage (GDPR Compliant)"
    ], c_blue)

    draw_card(60, 390, 380, 560, "Normalization & Anti-Bias", [
        "Unicode & Bullet Point Normalizer",
        "Demographic Stripper (Gender, Age, Religion)",
        "PII Scrubbing for Scoring Operations",
        "Token-Boundary Preserving Sanitizer"
    ], c_secondary)

    draw_card(60, 590, 380, 770, "Section Segmentation", [
        "Regex Boundary Heuristic Parser",
        "Structured Education Section Slicing",
        "Work Experience Timeline Extraction",
        "Academic & Personal Projects Slicing"
    ], c_blue)

    draw_card(60, 800, 380, 990, "Candidate Profile Parser", [
        "Degree Detection (B.Tech, M.S., BCA)",
        "Field of Study & Graduation Year",
        "Seniority / Experience Level Estimator",
        "Role History & Institution Extractor"
    ], c_secondary)

    # STAGE 2 CARDS
    draw_card(480, 200, 800, 430, "Knowledge Base Datasets", [
        "skill_dictionary.csv (60 Verified Skills)",
        "7 Categorized Technical Domains",
        "N-Gram Aliases & Difficulty Tiers",
        "job_roles.csv (10 Enterprise Roles)",
        "Required vs Preferred Qualifications"
    ], c_accent_amber)

    draw_card(480, 460, 800, 700, "Skill Extraction Engine", [
        "Boundary-Safe Regex Engine (\\b...\\b)",
        "Multi-Word Entity Lookahead Priority",
        "Single-Letter Collision Protection ('Go')",
        "Exact Alias & Canonical Normalization",
        "Domain Frequency & Coverage Matrix"
    ], c_secondary)

    draw_card(480, 730, 800, 990, "Profile & Contact Inspector", [
        "Display-Only Handle Extraction",
        "GitHub & LinkedIn Presentation Handles",
        "Anonymized Identity Assignment",
        "Strict Exclusion from Score Weights"
    ], c_blue)

    # STAGE 3 CARDS
    draw_card(900, 200, 1220, 450, "TF-IDF Vector Space Model", [
        "Scikit-Learn TfidfVectorizer",
        "Sublinear TF Scaling (sublinear_tf=True)",
        "N-Gram Range (1, 2) Token Representation",
        "Custom Token Regex (r'(?u)\\S+') for C++, C#",
        "10-Role Corpus Semantic Fitting"
    ], c_accent_green)

    draw_card(900, 480, 1220, 740, "Hybrid Mathematical Matcher", [
        "Formula: S = 0.60*C_skills + 0.30*S_tfidf + 0.10*B_pref",
        "60% Skill Matrix Jaccard Overlap",
        "30% Contextual Cosine Similarity",
        "10% Bonus for Preferred Competencies",
        "Normalized 0.0% - 100.0% Index"
    ], c_primary)

    draw_card(900, 770, 1220, 990, "Ranking & Diagnostics", [
        "Multi-Role Sorting by Match Score",
        "Top 3 Role Recommendations",
        "Readiness Assessment (Interview Ready)",
        "Salary & Responsibility Benchmarks"
    ], c_accent_green)

    # STAGE 4 CARDS
    draw_card(1320, 200, 1740, 420, "Granular Skill Gap Analysis", [
        "Matched Required Skills (Emerald Badges)",
        "Missing Skills to Bridge (Rose Badges)",
        "Preferred Skills Credit (Amber Badges)",
        "Interactive Any-Role Benchmark Selector",
        "Plotly Gauge & Comparative Bar Charts"
    ], c_secondary)

    draw_card(1320, 450, 1740, 710, "Personalized Learning Roadmap", [
        "3-Phase Progression (Foundations to Scale)",
        "Estimated Study Hours & Weekly Budget",
        "Curated Free Courses (CS50, freeCodeCamp)",
        "Direct Official Documentation Links",
        "3 Tailored Capstone Projects (STAR Format)"
    ], c_blue)

    draw_card(1320, 740, 1740, 990, "Outputs, Reports & Audit Log", [
        "Programmatic ReportLab Executive PDF",
        "Formatted Markdown Summary Export",
        "SQLite Anonymous Audit Log (resume_analyzer.db)",
        "Ethical AI & Compliance Transparency Notice"
    ], c_primary)

    # Draw Inter-Stage Arrows
    arrow_color = (148, 163, 184, 255)
    def draw_arrow(start_x, start_y, end_x, end_y):
        draw.line([(start_x, start_y), (end_x, end_y)], fill=arrow_color, width=3)
        draw.polygon([(end_x, end_y), (end_x - 10, end_y - 6), (end_x - 10, end_y + 6)], fill=arrow_color)

    draw_arrow(380, 280, 480, 280)
    draw_arrow(380, 580, 480, 580)
    draw_arrow(800, 320, 900, 320)
    draw_arrow(800, 580, 900, 580)
    draw_arrow(1220, 320, 1320, 320)
    draw_arrow(1220, 580, 1320, 580)
    draw_arrow(1220, 850, 1320, 850)

    # Footer
    draw.rectangle([(0, height - 40), (width, height)], fill=c_primary)
    draw.text((60, height - 28), "AI Resume Analyzer & Job Recommendation System v1.0.0 | Built with Python, Streamlit, Scikit-Learn & ReportLab", fill=(226, 232, 240, 255), font=font_badge)

    img.save(PNG_PATH, "PNG", dpi=(300, 300))
    print(f"Generated standalone PNG: {PNG_PATH}")


def generate_pdf():
    c = canvas.Canvas(PDF_PATH, pagesize=landscape(letter))
    w, h = landscape(letter)

    # Background
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # Header
    c.setFillColor(colors.HexColor("#1E3A8A"))
    c.rect(0, h - 55, w, 55, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(36, h - 32, "AI Resume Analyzer & Job Recommendation System")
    c.setFont("Helvetica", 10)
    c.drawString(36, h - 46, "End-to-End Workflow & Architectural Specification")

    # Pipeline Boxes
    stages = [
        ("1. Ingestion & Privacy", 36, 170, "#3B82F6", [
            "In-Memory PDF (pypdf)",
            "DOCX Parser (python-docx)",
            "Zero Persistent Storage",
            "Anti-Bias Data Scrubber",
            "Section Segmenter"
        ]),
        ("2. Feature Extraction", 216, 170, "#0D9488", [
            "60 Skills (7 Domains)",
            "Boundary Regex Matcher",
            "Multi-Word Lookahead",
            "Degree & Graduation Year",
            "Experience Years Estimator"
        ]),
        ("3. Hybrid Matching", 396, 170, "#10B981", [
            "TfidfVectorizer (ngram 1,2)",
            "Sublinear TF Scaling",
            "Contextual Cosine Sim",
            "60% Skill + 30% TFIDF",
            "Top 3 Role Recommendations"
        ]),
        ("4. Outputs & Roadmap", 576, 180, "#1E3A8A", [
            "Skill Gap Matrix (Matched/Missing)",
            "3-Phase Upskilling Roadmap",
            "Curated Free Courses & Docs",
            "3 Capstone Projects (STAR)",
            "ReportLab PDF & Markdown Export"
        ])
    ]

    for title, x, box_w, color_hex, items in stages:
        c.setFillColor(colors.HexColor(color_hex))
        c.roundRect(x, h - 90, box_w, 24, 4, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(x + 8, h - 75, title)

        # Body card
        c.setFillColor(colors.white)
        c.setStrokeColor(colors.HexColor("#E5E7EB"))
        c.roundRect(x, 70, box_w, h - 170, 8, fill=1, stroke=1)

        # Card items
        c.setFillColor(colors.HexColor("#1F2937"))
        c.setFont("Helvetica", 8.5)
        curr_y = h - 195
        for it in items:
            c.drawString(x + 12, curr_y, f"• {it}")
            curr_y -= 26

    # Mathematical Formula Box
    c.setFillColor(colors.HexColor("#EFF6FF"))
    c.setStrokeColor(colors.HexColor("#BFDBFE"))
    c.roundRect(36, 68, w - 72, 70, 6, fill=1, stroke=1)
    c.setFillColor(colors.HexColor("#1E3A8A"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(48, 122, "System Matching Function Formulation:")
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(48, 104, "Match Score = 0.60 * Skill_Coverage_Pct + 0.30 * TFIDF_Cosine_Pct + 0.10 * Preferred_Bonus_Pct")
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#4B5563"))
    c.drawString(48, 86, "Evaluated across 10 benchmark enterprise job roles and 60 technical skills. Demographic variables strictly excluded.")

    # Footer
    c.setFillColor(colors.HexColor("#1E3A8A"))
    c.rect(0, 0, w, 28, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#E2E8F0"))
    c.setFont("Helvetica", 8)
    c.drawString(36, 10, "AI Resume Analyzer & Job Recommendation System | Architecture Diagram Specification | Version 1.0.0")

    c.save()
    print(f"Generated standalone PDF: {PDF_PATH}")


if __name__ == "__main__":
    generate_png()
    generate_pdf()
