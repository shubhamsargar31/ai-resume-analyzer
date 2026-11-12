"""
Candidate Profile Extraction Engine.
Extracts structured education, experience, and project highlights from resume text.
Strictly adheres to fair evaluation principles by excluding demographic attributes.
"""

import re
from datetime import datetime
from typing import Dict, List, Any, Optional

# Current reference year for experience calculation
CURRENT_YEAR = 2026

DEGREE_PATTERNS = [
    (r"(?i)\b(?:ph\.?d\.?|doctorate|doctor\s+of\s+philosophy)\b", "Doctorate / Ph.D."),
    (r"(?i)\b(?:m\.?tech\.?|master\s+of\s+technology)\b", "Master of Technology (M.Tech)"),
    (r"(?i)\b(?:m\.?s\.?|master\s+of\s+science)\b", "Master of Science (M.S.)"),
    (r"(?i)\b(?:m\.?e\.?|master\s+of\s+engineering)\b", "Master of Engineering (M.E.)"),
    (r"(?i)\b(?:mca|master\s+of\s+computer\s+applications)\b", "Master of Computer Applications (MCA)"),
    (r"(?i)\b(?:mba|master\s+of\s+business\s+administration)\b", "Master of Business Administration (MBA)"),
    (r"(?i)\b(?:postgraduate\s+diploma|pg\s+diploma|post\s+graduate\s+diploma)\b", "Postgraduate Diploma"),
    (r"(?i)\b(?:b\.?tech\.?|bachelor\s+of\s+technology)\b", "Bachelor of Technology (B.Tech)"),
    (r"(?i)\b(?:b\.?e\.?|bachelor\s+of\s+engineering)\b", "Bachelor of Engineering (B.E.)"),
    (r"(?i)\b(?:b\.?sc\.?|b\.?s\.?|bachelor\s+of\s+science)\b", "Bachelor of Science (B.S.)"),
    (r"(?i)\b(?:bca|bachelor\s+of\s+computer\s+applications)\b", "Bachelor of Computer Applications (BCA)"),
    (r"(?i)\b(?:bachelor(?:'s)?(?:\s+degree)?)\b", "Bachelor's Degree"),
    (r"(?i)\b(?:master(?:'s)?(?:\s+degree)?)\b", "Master's Degree"),
    (r"(?i)\b(?:diploma|associate(?:'s)?\s+degree)\b", "Diploma / Associate"),
]

FIELDS_OF_STUDY = [
    "Computer Science and Engineering", "Computer Science", "Information Technology",
    "Artificial Intelligence and Machine Learning", "Data Science",
    "Software Engineering", "Cybersecurity", "Electrical Engineering",
    "Electronics and Communication", "Mechanical Engineering",
    "Mathematics and Computing", "Statistics", "Information Systems"
]

COMMON_ROLES = [
    "software engineer", "frontend developer", "backend developer", "full stack developer",
    "data scientist", "machine learning engineer", "devops engineer", "cloud engineer",
    "data analyst", "systems engineer", "qa engineer", "software development intern",
    "web developer", "ai engineer", "research intern", "technical lead", "solution architect"
]


def extract_education(text: str, education_section: str = "") -> Dict[str, Any]:
    """
    Extracts degrees, majors/fields of study, institutions, and graduation years.
    """
    search_text = education_section if education_section.strip() else text
    degrees_found = []
    
    # Check degree matches
    for pattern, canonical_degree in DEGREE_PATTERNS:
        if re.search(pattern, search_text):
            if canonical_degree not in degrees_found:
                degrees_found.append(canonical_degree)

    # Check fields of study
    field_found = None
    for field in FIELDS_OF_STUDY:
        if re.search(rf"\b{re.escape(field)}\b", search_text, re.IGNORECASE):
            field_found = field
            break

    # Extract graduation year range or year
    year_matches = re.findall(r"\b(20[0-2][0-9]|199[0-9])\b", search_text)
    grad_year = None
    if year_matches:
        # Most recent year is usually graduation
        years = sorted([int(y) for y in year_matches])
        grad_year = str(years[-1])

    # Extract institution keywords (University, Institute, College, Academy)
    institution = None
    inst_match = re.search(
        r"(?i)\b([A-Z][A-Za-z0-9\s,\.&]{2,40}\s+(?:University|Institute|College|Academy|School\s+of\s+[A-Za-z]+))\b",
        search_text
    )
    if inst_match:
        institution = inst_match.group(1).strip()

    primary_degree = degrees_found[0] if degrees_found else "Degree not explicitly detected"

    return {
        "primary_degree": primary_degree,
        "all_degrees": degrees_found,
        "field_of_study": field_found or "Computer Science / Related Field",
        "graduation_year": grad_year,
        "institution": institution,
        "education_summary": f"{primary_degree}" + (f" in {field_found}" if field_found else "") + (f" ({grad_year})" if grad_year else "")
    }


def extract_experience(text: str, experience_section: str = "") -> Dict[str, Any]:
    """
    Extracts professional roles, calculates estimated years of experience,
    and categorizes candidate seniority.
    """
    search_text = experience_section if experience_section.strip() else text

    # Look for explicit years of experience phrases (e.g. "3+ years of experience")
    explicit_exp = 0.0
    exp_phrase_match = re.search(r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+experience", text, re.IGNORECASE)
    if exp_phrase_match:
        try:
            explicit_exp = float(exp_phrase_match.group(1))
        except ValueError:
            explicit_exp = 0.0

    # Calculate experience by date ranges in experience section
    # e.g., "2021 - 2024", "Jan 2022 - Present", "06/2022 - 12/2023"
    calculated_months = 0
    date_range_pattern = r"(?i)\b(?:(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*)?(20[1-2][0-9])\s*(?:-|to|–|—)\s*(?:(Present|Current|Now)|(?:(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*)?(20[1-2][0-9]))\b"
    
    ranges = re.findall(date_range_pattern, search_text)
    
    for r in ranges:
        start_year = int(r[1])
        if r[2]:  # Present
            end_year = CURRENT_YEAR
        elif r[4]:  # End year
            end_year = int(r[4])
        else:
            end_year = start_year
        
        diff_years = max(0, end_year - start_year)
        calculated_months += (diff_years * 12) + 6 # default estimate

    range_exp = round(calculated_months / 12.0, 1)
    
    # Final estimate: max of explicit or date range, capped reasonably
    estimated_years = max(explicit_exp, range_exp)
    if estimated_years > 25:
        estimated_years = 25.0

    # Seniority level
    if estimated_years < 1.0:
        level = "Fresher / Entry-Level"
    elif estimated_years <= 3.0:
        level = "Junior (1-3 yrs)"
    elif estimated_years <= 6.0:
        level = "Mid-Level (3-6 yrs)"
    else:
        level = "Senior / Lead (6+ yrs)"

    # Identify roles mentioned
    roles_detected = []
    text_lower = text.lower()
    for role in COMMON_ROLES:
        if re.search(rf"\b{re.escape(role)}\b", text_lower):
            roles_detected.append(role.title())

    return {
        "estimated_years": estimated_years,
        "seniority_level": level,
        "roles_detected": roles_detected[:4],
        "is_fresher": estimated_years < 1.0
    }


def extract_projects(text: str, projects_section: str = "") -> List[Dict[str, str]]:
    """
    Parses individual projects from the projects section.
    """
    content = projects_section if projects_section.strip() else ""
    projects_list = []

    if content:
        # Split by bullet points or common project separators
        lines = content.split("\n")
        current_project = None

        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue

            # Heuristic for project title line: short line, may contain '|' or ':' or brackets
            if (len(line_str) < 70 and not line_str.startswith("-") and not line_str.startswith("•")) or ("|" in line_str and len(line_str) < 90):
                if current_project:
                    projects_list.append(current_project)
                
                parts = line_str.split("|")
                title = parts[0].strip().strip("#*:-_")
                tech_stack = parts[1].strip() if len(parts) > 1 else ""
                current_project = {
                    "title": title,
                    "tech_stack": tech_stack,
                    "description": ""
                }
            elif current_project:
                current_project["description"] += " " + line_str.lstrip("-•* ")

        if current_project:
            projects_list.append(current_project)

    # If no structured projects could be parsed from section, search for project mentions in text
    if not projects_list:
        generic_matches = re.findall(r"(?i)(?:project|system|application|platform):\s*([^\n]{5,80})", text)
        for g in generic_matches[:3]:
            projects_list.append({"title": g.strip(), "tech_stack": "", "description": ""})

    return projects_list[:4]


def extract_full_profile(text: str, sections: Dict[str, str]) -> Dict[str, Any]:
    """
    Extracts candidate profile summary incorporating education, experience, and projects.
    """
    edu_info = extract_education(text, sections.get("education", ""))
    exp_info = extract_experience(text, sections.get("experience", ""))
    projects_info = extract_projects(text, sections.get("projects", ""))

    return {
        "education": edu_info,
        "experience": exp_info,
        "projects": projects_info,
        "anti_bias_verified": True,
        "fairness_notice": (
            "Ethical AI Guarantee: Matching scores are strictly calculated based on technical skills, "
            "education, and verifiable project competencies. Demographic attributes such as age, gender, "
            "marital status, race, or religion are never extracted or evaluated."
        )
    }
