"""
Text Cleaning and Resume Segmentation Module.
Prepares extracted resume text for NLP processing, skill extraction, and TF-IDF matching.
Includes privacy sanitization to strip protected personal attributes.
"""

import re
import unicodedata
from typing import Dict, Optional, List, Tuple


# Regex patterns for common resume sections
SECTION_PATTERNS = {
    "skills": r"(?i)(?:technical\s+skills|skills\s*(?:&|and)\s*technologies|core\s+competencies|technical\s+expertise|skills|technologies|tools\s*(?:&|and)\s*skills)",
    "experience": r"(?i)(?:work\s+experience|professional\s+experience|experience|employment\s+history|internships|work\s+history)",
    "education": r"(?i)(?:education|academic\s+background|academic\s+qualifications|educational\s+history|academics)",
    "projects": r"(?i)(?:projects|academic\s+projects|personal\s+projects|key\s+projects|portfolio|technical\s+projects)",
    "certifications": r"(?i)(?:certifications|licenses\s*(?:&|and)\s*certifications|certificates|professional\s+certifications|courses)",
    "achievements": r"(?i)(?:achievements|awards|honors|publications|extracurricular)",
}


def normalize_whitespace(text: str) -> str:
    """Replaces multiple whitespace characters with a single space and cleans linebreaks."""
    text = re.sub(r"[\r\f\v]", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def clean_text(raw_text: str) -> str:
    """
    Cleans raw resume text by normalizing unicode characters, bullet points,
    dashes, and special symbols while preserving structure.
    """
    if not raw_text:
        return ""

    # Normalize unicode (decompose combined characters)
    text = unicodedata.normalize("NFKC", raw_text)

    # Standardize bullet points and list markers
    bullet_patterns = r"[\u2022\u2023\u25E6\u2043\u2219\u25AA\u25AB\u25CF\u25CB\u25C6\u27A2\u2713\u2714\uF0B7\uF0A7\u25BA\*]"
    text = re.sub(bullet_patterns, "\n- ", text)

    # Standardize dashes and hyphens
    text = re.sub(r"[\u2010\u2011\u2012\u2013\u2014\u2015\u2212]", "-", text)

    # Standardize quotes
    text = re.sub(r"[\u2018\u2019\u201A\u201B]", "'", text)
    text = re.sub(r"[\u201C\u201D\u201E\u201F]", '"', text)

    # Remove non-printable / binary junk characters
    text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]", " ", text)

    return normalize_whitespace(text)


def clean_for_vectorization(text: str) -> str:
    """
    Prepares text for TF-IDF vectorization:
    - Lowercase
    - Removes URLs, emails, phone numbers, and arbitrary punctuation
    - Preserves meaningful technical terms like c++, c#, .net, ci/cd
    """
    if not text:
        return ""

    text = text.lower()
    
    # Strip URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    
    # Strip emails
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", " ", text)
    
    # Strip phone numbers
    text = re.sub(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", " ", text)

    # Preserve special technical tags by token replacement
    text = re.sub(r"\bc\+\+(?=[^a-z0-9]|$)", "cpp_lang", text)
    text = re.sub(r"\bc#(?=[^a-z0-9]|$)", "csharp_lang", text)
    text = re.sub(r"(?:\b|\s)\.net(?=[^a-z0-9]|$)", " dotnet_tech ", text)
    text = re.sub(r"\bci/cd\b", "cicd_pipe", text)
    text = re.sub(r"\bnode\.js\b", "nodejs_runtime", text)
    text = re.sub(r"\bnext\.js\b", "nextjs_framework", text)

    # Remove non-alphanumeric except spaces and underscores
    text = re.sub(r"[^a-z0-9_\s]", " ", text)

    # Restore technical tags
    text = text.replace("cpp_lang", "c++")
    text = text.replace("csharp_lang", "c#")
    text = text.replace("dotnet_tech", ".net")
    text = text.replace("cicd_pipe", "ci/cd")
    text = text.replace("nodejs_runtime", "node.js")
    text = text.replace("nextjs_framework", "next.js")

    return normalize_whitespace(text)


def extract_sections(text: str) -> Dict[str, str]:
    """
    Segments resume text into distinct structured sections.
    Returns a dictionary mapping section keys to their extracted contents.
    """
    cleaned = clean_text(text)
    lines = cleaned.split("\n")
    
    # Identify positions of section headers
    section_positions = []
    
    for idx, line in enumerate(lines):
        line_clean = line.strip().strip(":-_#")
        if not line_clean or len(line_clean) > 50:
            continue
            
        for sec_name, pattern in SECTION_PATTERNS.items():
            if re.fullmatch(pattern, line_clean):
                section_positions.append((idx, sec_name, line_clean))
                break

    # If no sections could be identified by full match, try prefix match
    if not section_positions:
        for idx, line in enumerate(lines):
            line_clean = line.strip().strip(":-_#")
            if not line_clean or len(line_clean) > 40:
                continue
            for sec_name, pattern in SECTION_PATTERNS.items():
                if re.match(r"^" + pattern + r"(?:\s*[:\-\|]|$)", line_clean):
                    section_positions.append((idx, sec_name, line_clean))
                    break

    sections: Dict[str, str] = {
        "summary": "",
        "skills": "",
        "experience": "",
        "education": "",
        "projects": "",
        "certifications": "",
        "other": ""
    }

    if not section_positions:
        # Fallback: cannot segment, treat everything as general content
        sections["other"] = cleaned
        return sections

    # Sort positions by line index
    section_positions.sort(key=lambda x: x[0])

    # Text before the first header is usually Summary / Header
    first_idx = section_positions[0][0]
    if first_idx > 0:
        sections["summary"] = "\n".join(lines[:first_idx]).strip()

    # Slice between headers
    for i in range(len(section_positions)):
        start_idx, sec_name, _ = section_positions[i]
        end_idx = section_positions[i + 1][0] if i + 1 < len(section_positions) else len(lines)
        section_content = "\n".join(lines[start_idx + 1:end_idx]).strip()
        
        if sec_name in sections:
            # Append if duplicate header occurs
            if sections[sec_name]:
                sections[sec_name] += "\n" + section_content
            else:
                sections[sec_name] = section_content
        else:
            sections["other"] += "\n" + section_content

    return sections


def extract_contact_info(text: str) -> Dict[str, Optional[str]]:
    """
    Extracts basic contact handles (email, phone, linkedin, github) for presentation only.
    These are NEVER used in matching, scoring, or recommendations.
    """
    info = {
        "email": None,
        "phone": None,
        "linkedin": None,
        "github": None,
        "portfolio": None
    }

    # Email
    email_match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text)
    if email_match:
        info["email"] = email_match.group(0)

    # Phone
    phone_match = re.search(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
    if phone_match:
        info["phone"] = phone_match.group(0).strip()

    # LinkedIn
    linkedin_match = re.search(r"(?:https?://)?(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+", text, re.IGNORECASE)
    if linkedin_match:
        info["linkedin"] = linkedin_match.group(0)

    # GitHub
    github_match = re.search(r"(?:https?://)?(?:www\.)?github\.com/[A-Za-z0-9_-]+", text, re.IGNORECASE)
    if github_match:
        info["github"] = github_match.group(0)

    return info


def sanitize_protected_data(text: str) -> str:
    """
    Strips explicit demographic indicators such as gender mentions, marital status,
    religion, caste, nationality, date of birth, or age to enforce fair, bias-free AI evaluation.
    """
    if not text:
        return ""

    # Remove marital status
    text = re.sub(r"(?i)\b(marital\s*(?:status)?\s*:\s*(?:single|married|unmarried|divorced|widowed))\b", "[REDACTED]", text)
    # Remove religion / caste / community
    text = re.sub(r"(?i)\b((?:religion|caste|community)\s*:\s*[A-Za-z]+)\b", "[REDACTED]", text)
    # Remove nationality / citizenship if explicitly listed
    text = re.sub(r"(?i)\b((?:nationality|citizenship)\s*:\s*[A-Za-z\s]+)\b", "[REDACTED]", text)
    # Remove gender mentions (e.g., "Gender: Male", "Sex: Female")
    text = re.sub(r"(?i)\b((?:gender|sex)\s*:\s*(?:male|female|other|non-binary|prefer\s+not\s+to\s+say))\b", "[REDACTED]", text)
    # Remove date of birth
    text = re.sub(r"(?i)\b(d\.?o\.?b\.?|date\s+of\s+birth)\s*:\s*[0-9\/\-\.]+", "[REDACTED]", text)
    # Remove explicit age lines (e.g. "Age: 25", "Age - 28 years")
    text = re.sub(r"(?i)\b(age\s*[:\-]?\s*\d{1,2}(?:\s*years?(?:\s*old)?)?)\b", "[REDACTED]", text)
    # Remove photo / headshot placeholder markers
    text = re.sub(r"(?i)\[(?:photo|picture|photograph|headshot|avatar)\]", "[REDACTED]", text)

    return text
