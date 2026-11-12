"""
Resume Analysis Report Generation Engine.
Generates publication-quality PDF reports using ReportLab,
as well as structured Markdown/Text summaries for instant export.
"""

import io
from datetime import datetime
from typing import Dict, Any, List

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def generate_markdown_report(analysis_data: Dict[str, Any]) -> str:
    """
    Generates a markdown resume analysis report.
    """
    candidate_name = analysis_data.get("candidate_name", "Candidate")
    timestamp = analysis_data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    profile = analysis_data.get("profile", {})
    edu = profile.get("education", {})
    exp = profile.get("experience", {})
    detected_skills = analysis_data.get("detected_skills", [])
    top_roles = analysis_data.get("top_roles", [])
    primary_role = top_roles[0] if top_roles else {}
    roadmap = analysis_data.get("roadmap", {})

    lines = [
        f"# AI Resume Analysis & Job Recommendation Report",
        f"**Generated:** {timestamp}  ",
        f"**Candidate:** {candidate_name}  ",
        f"**Evaluation Mode:** Unbiased Technical Competency & Semantic Assessment  ",
        "",
        "---",
        "",
        "## 1. Executive Summary & Candidate Profile",
        f"- **Primary Education:** {edu.get('education_summary', 'Not Specified')}",
        f"- **Estimated Experience:** {exp.get('estimated_years', 0)} years ({exp.get('seniority_level', 'Entry-Level')})",
        f"- **Total Technical Skills Detected:** {len(detected_skills)} skills",
        f"- **Top Recommended Role:** **{primary_role.get('role_title', 'N/A')}** ({primary_role.get('match_score', 0)}% Match)",
        "",
        "### Detected Skills by Domain:",
    ]

    by_cat = analysis_data.get("skills_by_category", {})
    if by_cat:
        for cat, skills in by_cat.items():
            lines.append(f"- **{cat}:** {', '.join(skills)}")
    else:
        lines.append(f"- {', '.join(detected_skills)}")

    lines.extend([
        "",
        "---",
        "",
        "## 2. Top Job Role Recommendations",
        "| Rank | Role Title | Category | Match Score | Match Tier | Matched Skills | Missing Skills |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ])

    for i, role in enumerate(top_roles, start=1):
        lines.append(
            f"| #{i} | **{role.get('role_title')}** | {role.get('category')} | "
            f"**{role.get('match_score')}%** | {role.get('match_tier')} | "
            f"{len(role.get('matched_skills', []))} | {len(role.get('missing_skills', []))} |"
        )

    lines.extend([
        "",
        "---",
        "",
        f"## 3. Detailed Skill Gap Analysis: {primary_role.get('role_title', 'Primary Role')}",
        f"**Target Role Description:** {primary_role.get('description', '')}",
        "",
        f"### Matched Skills ({len(primary_role.get('matched_skills', []))}):",
        f"> {', '.join(primary_role.get('matched_skills', [])) if primary_role.get('matched_skills') else 'None'}",
        "",
        f"### Missing Skills to Bridge ({len(primary_role.get('missing_skills', []))}):",
        f"> {', '.join(primary_role.get('missing_skills', [])) if primary_role.get('missing_skills') else 'No gaps detected! Excellent alignment.'}",
        "",
        "---",
        "",
        f"## 4. Personalized Learning Roadmap & Curated Resources",
        f"**Estimated Time to Bridge Gaps:** ~{roadmap.get('estimated_weeks', 4)} weeks ({roadmap.get('total_estimated_hours', 40)} total study hours)",
        ""
    ])

    for phase in roadmap.get("phases", []):
        if phase.get("skills"):
            lines.append(f"### {phase.get('phase_name')} ({phase.get('duration')})")
            lines.append(f"*{phase.get('objective')}*")
            lines.append("")
            for s in phase.get("skills", []):
                lines.append(f"- **{s.get('skill_name')}** ({s.get('difficulty_level')} | ~{s.get('estimated_learning_hours')} hrs)")
                lines.append(f"  - Resource: {s.get('free_course')}")
                lines.append(f"  - Docs: {s.get('doc_url')}")
            lines.append("")

    lines.extend([
        "---",
        "",
        "## 5. Recommended Capstone Portfolio Projects",
    ])

    for p in roadmap.get("capstone_projects", []):
        lines.append(f"### {p.get('title')}")
        lines.append(f"- **Concept:** {p.get('concept')}")
        lines.append(f"- **Tech Stack:** `{p.get('tech_stack')}`")
        lines.append(f"- **Sample Resume Bullet:** *\"{p.get('resume_bullet_sample')}\"*")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## 6. Disclaimer & Ethical AI Statement",
        "> **Note:** This resume analysis is an educational and career-advisory estimate generated via NLP, ",
        "> TF-IDF cosine similarity, and skill matrix comparison. It is NOT an automated hiring decision. ",
        "> In accordance with ethical AI guidelines, protected personal attributes (age, gender, ethnicity, ",
        "> religion) are strictly excluded from evaluation. Missing keywords do not always indicate missing ability — ",
        "> candidates may possess equivalent competencies expressed through different terminology or experience."
    ])

    return "\n".join(lines)


def generate_pdf_report(analysis_data: Dict[str, Any]) -> bytes:
    """
    Builds a PDF report using ReportLab and returns the binary PDF bytes.
    """
    if not REPORTLAB_AVAILABLE:
        # Fallback to plain text bytes if reportlab is missing
        md = generate_markdown_report(analysis_data)
        return md.encode("utf-8")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom color palette
    primary_color = colors.HexColor("#1E3A8A")   # Deep navy
    secondary_color = colors.HexColor("#0D9488") # Teal
    dark_gray = colors.HexColor("#1F2937")       # Charcoal
    light_gray = colors.HexColor("#F3F4F6")      # Background tint
    border_color = colors.HexColor("#E5E7EB")

    # Typography styles
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#4B5563"),
        spaceAfter=12
    )

    h2_style = ParagraphStyle(
        "ReportH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=dark_gray,
        spaceAfter=4
    )

    badge_style = ParagraphStyle(
        "ReportBadge",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.whitesmoke,
        alignment=TA_CENTER
    )

    elements = []

    # Title & Header
    elements.append(Paragraph("AI Resume Analysis & Job Recommendation System", title_style))
    elements.append(Paragraph(
        f"<b>Candidate:</b> {analysis_data.get('candidate_name', 'Evaluated Resume')} &nbsp;|&nbsp; "
        f"<b>Generated:</b> {analysis_data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M'))} &nbsp;|&nbsp; "
        f"<b>Framework:</b> TF-IDF & Skill Vectorizer v1.0",
        subtitle_style
    ))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=10))

    # Executive Summary Box
    profile = analysis_data.get("profile", {})
    edu = profile.get("education", {})
    exp = profile.get("experience", {})
    detected_skills = analysis_data.get("detected_skills", [])
    top_roles = analysis_data.get("top_roles", [])
    primary_role = top_roles[0] if top_roles else {}

    summary_data = [
        [
            Paragraph("<b>Target Education:</b>", body_style),
            Paragraph(str(edu.get("education_summary", "Not Specified")), body_style),
            Paragraph("<b>Total Skills Found:</b>", body_style),
            Paragraph(f"<b>{len(detected_skills)}</b> verified skills", body_style),
        ],
        [
            Paragraph("<b>Experience Level:</b>", body_style),
            Paragraph(f"{exp.get('estimated_years', 0)} yrs ({exp.get('seniority_level', 'Entry-Level')})", body_style),
            Paragraph("<b>Top Role Match:</b>", body_style),
            Paragraph(f"<b>{primary_role.get('role_title', 'N/A')}</b> ({primary_role.get('match_score', 0)}%)", body_style),
        ]
    ]

    summary_table = Table(summary_data, colWidths=[100, 170, 100, 170])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), light_gray),
        ("BOX", (0, 0), (-1, -1), 1, border_color),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 10))

    # Top Recommended Roles Table
    elements.append(Paragraph("1. Top Job Role Recommendations", h2_style))
    role_rows = [["Rank", "Role Title", "Domain", "Match Score", "Skill Coverage", "Readiness"]]
    
    for idx, role in enumerate(top_roles, start=1):
        role_rows.append([
            f"#{idx}",
            role.get("role_title", ""),
            role.get("category", ""),
            f"{role.get('match_score')}%",
            f"{role.get('skill_coverage_pct')}% ({len(role.get('matched_skills', []))}/{role.get('required_skills_count', 0)})",
            role.get("match_tier", "")
        ])

    role_table = Table(role_rows, colWidths=[40, 140, 110, 75, 95, 80])
    role_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), primary_color),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ALIGN", (1, 1), (2, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, border_color),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, light_gray]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    elements.append(role_table)
    elements.append(Spacer(1, 10))

    # Skill Gap Breakdown
    elements.append(Paragraph(f"2. Skill Gap Analysis: {primary_role.get('role_title', 'Target Role')}", h2_style))
    matched_str = ", ".join(primary_role.get("matched_skills", [])) or "None identified"
    missing_str = ", ".join(primary_role.get("missing_skills", [])) or "Zero gaps! Perfect alignment."

    gap_data = [
        [
            Paragraph("<b>Matched Skills:</b>", body_style),
            Paragraph(f"<font color='#0D9488'>{matched_str}</font>", body_style)
        ],
        [
            Paragraph("<b>Missing Skills:</b>", body_style),
            Paragraph(f"<font color='#DC2626'>{missing_str}</font>", body_style)
        ]
    ]
    gap_table = Table(gap_data, colWidths=[100, 440])
    gap_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F9FAFB")),
        ("BOX", (0, 0), (-1, -1), 1, border_color),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    elements.append(gap_table)
    elements.append(Spacer(1, 10))

    # Roadmap Section
    roadmap = analysis_data.get("roadmap", {})
    elements.append(Paragraph("3. Step-by-Step Learning Roadmap & Recommended Projects", h2_style))
    
    phases = roadmap.get("phases", [])
    for p in phases:
        if p.get("skills"):
            elements.append(Paragraph(f"<b>{p.get('phase_name')}</b> - <i>{p.get('duration')}</i>", body_style))
            skill_bullets = []
            for s in p.get("skills", []):
                skill_bullets.append(
                    f"• <b>{s.get('skill_name')}</b> ({s.get('difficulty_level')}, ~{s.get('estimated_learning_hours')} hrs): "
                    f"<i>{s.get('free_course')}</i>"
                )
            elements.append(Paragraph("<br/>".join(skill_bullets), body_style))
            elements.append(Spacer(1, 4))

    # Capstone Project
    capstones = roadmap.get("capstone_projects", [])
    if capstones:
        elements.append(Spacer(1, 4))
        p0 = capstones[0]
        elements.append(Paragraph(f"<b>Key Portfolio Project:</b> {p0.get('title')}", body_style))
        elements.append(Paragraph(f"<b>Stack:</b> {p0.get('tech_stack')}", body_style))
        elements.append(Paragraph(f"<b>Resume Impact:</b> <i>\"{p0.get('resume_bullet_sample')}\"</i>", body_style))

    # Disclaimer
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceAfter=6))
    elements.append(Paragraph(
        "<b>Ethical AI & Compliance Notice:</b> This report is generated algorithmically for educational guidance. "
        "It assesses solely technical skills and qualifications. Demographic characteristics (age, gender, ethnicity, religion) "
        "are strictly omitted from extraction and evaluation. Match scores represent heuristic similarity estimates, not hiring decisions. "
        "Missing keywords do not always indicate missing ability — candidates may possess equivalent competencies expressed through different terminology.",
        ParagraphStyle("Notice", parent=styles["Normal"], fontName="Helvetica", fontSize=7.5, leading=10, textColor=colors.HexColor("#6B7280"))
    ))

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
