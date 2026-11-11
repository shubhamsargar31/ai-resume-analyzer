"""
Skill Extraction Engine.
Detects technical and job-related skills using exact keyword and multi-word alias matching
against the skill dictionary with token boundary protection.
"""

import os
import re
import pandas as pd
from typing import List, Dict, Set, Any, Optional

DEFAULT_SKILL_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "skill_dictionary.csv")


class SkillExtractor:
    def __init__(self, dictionary_path: Optional[str] = None):
        self.dict_path = dictionary_path or DEFAULT_SKILL_CSV
        self.skills_df = pd.DataFrame()
        self.skill_map = {}       # canonical_name -> metadata dict
        self.alias_to_canonical = [] # list of (regex_pattern, canonical_name) sorted by length desc
        self._load_dictionary()

    def _load_dictionary(self):
        """Loads and parses the skill dictionary CSV."""
        if not os.path.exists(self.dict_path):
            raise FileNotFoundError(f"Skill dictionary not found at {self.dict_path}")

        df = pd.read_csv(self.dict_path)
        self.skills_df = df

        alias_pairs = []

        for _, row in df.iterrows():
            canonical = str(row["skill_name"]).strip()
            aliases_str = str(row.get("aliases", ""))
            
            # Combine canonical name and comma-separated aliases
            all_aliases = {canonical.lower()}
            if pd.notna(aliases_str) and aliases_str.strip():
                for a in aliases_str.split(","):
                    clean_a = a.strip().lower()
                    if clean_a:
                        all_aliases.add(clean_a)

            # Store metadata
            self.skill_map[canonical] = {
                "skill_id": row.get("skill_id", 0),
                "skill_name": canonical,
                "category": str(row.get("category", "General")),
                "importance_weight": float(row.get("importance_weight", 1.0)),
                "difficulty_level": str(row.get("difficulty_level", "Intermediate")),
                "estimated_learning_hours": int(row.get("estimated_learning_hours", 30)),
                "free_course": str(row.get("free_course", "")),
                "doc_url": str(row.get("doc_url", "")),
                "aliases": list(all_aliases)
            }

            for alias in all_aliases:
                alias_pairs.append((alias, canonical))

        # Sort aliases by character length descending so multi-word aliases match before single-word substrings
        alias_pairs.sort(key=lambda x: len(x[0]), reverse=True)

        # Pre-compile boundary-safe regex patterns
        self.alias_to_canonical = []
        for alias, canonical in alias_pairs:
            # Special handling for symbols like C++, C#, .NET, CI/CD, HTML/CSS
            escaped = re.escape(alias)
            # If alias starts/ends with alphanumeric, enforce word boundary \b
            prefix_bound = r"\b" if re.match(r"^[A-Za-z0-9]", alias) else r"(?:^|\s|[\(\[\{,;:])"
            suffix_bound = r"\b" if re.match(r".*[A-Za-z0-9]$", alias) else r"(?:$|\s|[\)\]\},;:])"
            
            pattern = re.compile(rf"{prefix_bound}{escaped}{suffix_bound}", re.IGNORECASE)
            self.alias_to_canonical.append((pattern, canonical, alias))

    def extract_skills(self, text: str) -> Dict[str, Any]:
        """
        Extracts all identified skills from input text.
        
        Returns:
            Dict containing:
                - 'detected_skills': sorted list of unique canonical skill names
                - 'skill_count': total unique skills found
                - 'skills_by_category': dict of category -> [skills]
                - 'skill_details': dict of skill_name -> metadata
                - 'matched_aliases': dict of canonical_name -> list of matched text tokens
        """
        if not text:
            return {
                "detected_skills": [],
                "skill_count": 0,
                "skills_by_category": {},
                "skill_details": {},
                "matched_aliases": {}
            }

        text_lower = text.lower()
        found_skills: Set[str] = set()
        matched_aliases: Dict[str, Set[str]] = {}

        for pattern, canonical, alias in self.alias_to_canonical:
            matches = pattern.findall(text_lower)
            if matches:
                found_skills.add(canonical)
                if canonical not in matched_aliases:
                    matched_aliases[canonical] = set()
                matched_aliases[canonical].add(alias)

        detected_list = sorted(list(found_skills))

        # Group by category
        by_category: Dict[str, List[str]] = {}
        for skill in detected_list:
            meta = self.skill_map.get(skill, {})
            cat = meta.get("category", "Other")
            by_category.setdefault(cat, []).append(skill)

        # Build details dictionary
        details = {skill: self.skill_map.get(skill, {}) for skill in detected_list}

        return {
            "detected_skills": detected_list,
            "skill_count": len(detected_list),
            "skills_by_category": by_category,
            "skill_details": details,
            "matched_aliases": {k: list(v) for k, v in matched_aliases.items()}
        }

    def get_skill_metadata(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """Returns metadata for a specific skill."""
        return self.skill_map.get(skill_name)

    def get_all_skills(self) -> List[str]:
        """Returns a list of all canonical skill names in the dictionary."""
        return sorted(list(self.skill_map.keys()))
