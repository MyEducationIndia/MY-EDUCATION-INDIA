"""
Module 15: Learning Progress & Gamification Engine
"""
from typing import List

class LearningProgressEngine:
    @staticmethod
    def calculate_course_progress(total_mandatory_lessons: int, completed_lessons: int) -> float:
        if total_mandatory_lessons <= 0:
            return 100.0 if completed_lessons > 0 else 0.0
        pct = (completed_lessons / total_mandatory_lessons) * 100.0
        return round(min(pct, 100.0), 2)

    @staticmethod
    def calculate_xp_earned(action: str, current_xp: int = 0) -> int:
        xp_map = {
            "LESSON_COMPLETED": 10,
            "ASSIGNMENT_SUBMITTED": 25,
            "QUIZ_PERFECT": 50,
            "COURSE_COMPLETED": 200,
            "FORUM_ACCEPTED_ANSWER": 30
        }
        return current_xp + xp_map.get(action, 5)

    @staticmethod
    def check_certificate_eligibility(progress_pct: float, threshold: float = 100.0) -> bool:
        return progress_pct >= threshold
