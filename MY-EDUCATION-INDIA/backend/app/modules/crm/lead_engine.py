"""
Module 17: Lead Scoring & Deduplication Engine
"""
from typing import Dict, Any, Optional

class LeadScoringAndDeduplicationEngine:
    @staticmethod
    def compute_lead_score(source: str, priority: str, has_guardian: bool, has_email: bool) -> int:
        score = 40
        if priority == "URGENT":
            score += 30
        elif priority == "HIGH":
            score += 20
        elif priority == "MEDIUM":
            score += 10

        source_weights = {
            "WALK_IN": 25,
            "REFERRAL": 20,
            "PHONE": 15,
            "WEBSITE": 10,
            "FACEBOOK": 5,
            "INSTAGRAM": 5
        }
        score += source_weights.get(source.upper(), 5)

        if has_guardian:
            score += 5
        if has_email:
            score += 5

        return min(score, 100)

    @staticmethod
    def is_duplicate_lead(existing_mobile: str, existing_email: Optional[str], incoming_mobile: str, incoming_email: Optional[str]) -> bool:
        import re
        m1 = re.sub(r'\D', '', existing_mobile)[-10:]
        m2 = re.sub(r'\D', '', incoming_mobile)[-10:]
        if m1 and m2 and m1 == m2:
            return True
        if existing_email and incoming_email and existing_email.lower().strip() == incoming_email.lower().strip():
            return True
        return False
