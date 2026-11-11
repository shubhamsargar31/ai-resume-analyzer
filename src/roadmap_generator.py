"""
Personalized Learning Roadmap Engine.
Generates structured multi-phase study plans, curated high-quality free learning resources,
and resume-worthy capstone project suggestions based on detected skill gaps.
"""

from typing import List, Dict, Any, Optional
from src.skill_extractor import SkillExtractor


class RoadmapGenerator:
    def __init__(self, skill_extractor: Optional[SkillExtractor] = None):
        self.skill_extractor = skill_extractor or SkillExtractor()

    def generate_roadmap(
        self,
        target_role: Dict[str, Any],
        candidate_skills: List[str]
    ) -> Dict[str, Any]:
        """
        Creates a personalized roadmap for a selected target job role.
        """
        role_title = target_role.get("role_title", "Target Role")
        missing_skills = target_role.get("missing_skills", [])
        matched_skills = target_role.get("matched_skills", [])

        # Gather rich metadata for each missing skill
        skill_cards = []
        total_hours = 0

        for skill in missing_skills:
            meta = self.skill_extractor.get_skill_metadata(skill)
            if not meta:
                meta = {
                    "skill_name": skill,
                    "category": "Technical Skill",
                    "difficulty_level": "Intermediate",
                    "estimated_learning_hours": 25,
                    "free_course": f"freeCodeCamp / YouTube tutorials for {skill}",
                    "doc_url": f"https://www.google.com/search?q={skill}+official+documentation"
                }

            skill_cards.append({
                "skill_name": skill,
                "category": meta.get("category", "General"),
                "difficulty_level": meta.get("difficulty_level", "Intermediate"),
                "estimated_learning_hours": meta.get("estimated_learning_hours", 25),
                "free_course": meta.get("free_course", ""),
                "doc_url": meta.get("doc_url", "")
            })
            total_hours += meta.get("estimated_learning_hours", 25)

        # Distribute into 3 sequential phases based on difficulty
        phase_1 = [] # Beginner / Foundational
        phase_2 = [] # Intermediate / Core
        phase_3 = [] # Advanced / Production

        for card in skill_cards:
            diff = card["difficulty_level"].lower()
            if "beginner" in diff:
                phase_1.append(card)
            elif "advanced" in diff:
                phase_3.append(card)
            else:
                phase_2.append(card)

        # If phases are imbalanced (e.g., all intermediate), balance them out smoothly
        if not phase_1 and phase_2:
            phase_1.append(phase_2.pop(0))
        if not phase_3 and len(phase_2) > 2:
            phase_3.append(phase_2.pop())

        phases = [
            {
                "phase_number": 1,
                "phase_name": "Phase 1: Foundational Syntax & Core Concepts",
                "duration": "Weeks 1 - 2 (approx. 10-15 hrs/wk)",
                "objective": "Establish fundamental competency and grasp essential syntax and libraries.",
                "skills": phase_1
            },
            {
                "phase_number": 2,
                "phase_name": "Phase 2: Hands-on Frameworks & Core Engineering",
                "duration": "Weeks 3 - 4 (approx. 15 hrs/wk)",
                "objective": "Build practical APIs, modules, and apply frameworks to real-world datasets/apps.",
                "skills": phase_2
            },
            {
                "phase_number": 3,
                "phase_name": "Phase 3: Production Architecture, Testing & Deployment",
                "duration": "Weeks 5 - 6+ (approx. 15 hrs/wk)",
                "objective": "Containerize, test, scale, and integrate systems ready for enterprise deployment.",
                "skills": phase_3
            }
        ]

        # Generate Capstone Project Ideas combining existing skills + new missing skills
        project_ideas = self._generate_capstone_projects(role_title, matched_skills, missing_skills)

        return {
            "target_role": role_title,
            "missing_skills_count": len(missing_skills),
            "matched_skills_count": len(matched_skills),
            "total_estimated_hours": total_hours,
            "estimated_weeks": max(2, round(total_hours / 15)),
            "phases": phases,
            "skill_cards": skill_cards,
            "capstone_projects": project_ideas,
            "perfect_match": len(missing_skills) == 0
        }

    def _generate_capstone_projects(
        self,
        role_title: str,
        matched_skills: List[str],
        missing_skills: List[str]
    ) -> List[Dict[str, str]]:
        """
        Creates 3 realistic, impressive portfolio project recommendations.
        """
        known_preview = ", ".join(matched_skills[:3]) if matched_skills else "Python / JavaScript"
        gap_preview = ", ".join(missing_skills[:3]) if missing_skills else "System Design & CI/CD"

        projects = [
            {
                "title": f"Production-Ready {role_title} Showcase Application",
                "concept": f"A scalable full-cycle application designed to demonstrate mastery over {gap_preview}.",
                "tech_stack": f"{known_preview} + {gap_preview}",
                "key_features": (
                    "• Implemented end-to-end pipeline with rigorous input validation and error handling.\n"
                    "• Created automated unit tests achieving >80% test coverage.\n"
                    "• Configured CI/CD automation and containerized deployment with Docker."
                ),
                "resume_bullet_sample": (
                    f"Architected and deployed a {role_title} system using {known_preview} and {gap_preview}, "
                    "reducing latency by 35% and automating test execution through GitHub Actions."
                )
            },
            {
                "title": f"Real-Time Analytics & Dashboard Engine",
                "concept": "Interactive operational dashboard processing streaming or tabular datasets with automated reporting.",
                "tech_stack": f"Data processing & visualization using {known_preview} and {gap_preview}",
                "key_features": (
                    "• Built low-latency REST/WebSocket endpoints for querying aggregated metrics.\n"
                    "• Integrated caching layers and optimized database indexing to handle concurrent requests.\n"
                    "• Deployed live dashboard with interactive filtering and downloadable executive summaries."
                ),
                "resume_bullet_sample": (
                    f"Designed an analytical metrics service leveraging {gap_preview}; engineered modular pipelines "
                    "enabling real-time KPI visualization for 1,000+ simulated users."
                )
            },
            {
                "title": f"Microservices-Based Enterprise Utility Platform",
                "concept": "Distributed system solving a concrete business workflow with secured auth and database persistence.",
                "tech_stack": f"{known_preview}, {gap_preview}, Docker, Git",
                "key_features": (
                    "• Modular architecture separating client, server API, and database layers.\n"
                    "• Implemented authentication, rate limiting, and structured JSON logging.\n"
                    "• Packaged service into multi-stage Docker containers with clear documentation."
                ),
                "resume_bullet_sample": (
                    f"Built a resilient microservice suite utilizing {gap_preview}; authored comprehensive API "
                    "documentation and containerized the service for rapid multi-environment deployment."
                )
            }
        ]

        return projects
