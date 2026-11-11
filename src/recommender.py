"""
Job Recommendation Engine.
Analyzes job matches, selects top recommendations, computes gap severity,
and prepares comparative visual analytics.
"""

from typing import List, Dict, Any, Optional
from src.job_matcher import JobMatcher


class JobRecommender:
    def __init__(self, matcher: Optional[JobMatcher] = None):
        self.matcher = matcher or JobMatcher()

    def recommend_top_roles(
        self,
        resume_text: str,
        detected_skills: List[str],
        top_n: int = 3
    ) -> Dict[str, Any]:
        """
        Ranks all available roles and returns top_n recommendations with detailed diagnostics.
        """
        all_matches = self.matcher.match_all_roles(resume_text, detected_skills)
        top_roles = all_matches[:top_n]
        other_roles = all_matches[top_n:]

        # Add readiness assessment and estimated learning hours for top roles
        for role in top_roles:
            missing_count = len(role["missing_skills"])
            # Readiness status
            if role["match_score"] >= 75:
                role["readiness"] = "Interview Ready"
                role["readiness_desc"] = "You have an exceptional match. Focus on polishing interview questions and system design."
            elif role["match_score"] >= 55:
                role["readiness"] = "High Potential (2-4 Weeks of Prep)"
                role["readiness_desc"] = "You meet core requirements. Closing a few targeted skill gaps will make you highly competitive."
            elif role["match_score"] >= 35:
                role["readiness"] = "Moderate Pivot (4-8 Weeks)"
                role["readiness_desc"] = "Solid foundational overlap, but requires dedicated upskilling in domain-specific tools."
            else:
                role["readiness"] = "Long-Term Career Goal"
                role["readiness_desc"] = "Significant skill additions required before applying to mid/senior positions."

        return {
            "top_recommendations": top_roles,
            "all_matches": all_matches,
            "total_roles_evaluated": len(all_matches),
            "primary_recommended_role": top_roles[0] if top_roles else None
        }
