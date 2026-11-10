"""
Module 15: Assignment Evaluation & Rubric Engine
"""
from datetime import datetime

class AssignmentEngine:
    @staticmethod
    def evaluate_late_submission(submission_time: datetime, due_date: datetime, late_penalty_percent: float = 10.0) -> dict:
        is_late = submission_time > due_date
        penalty_factor = (100.0 - late_penalty_percent) / 100.0 if is_late else 1.0
        return {
            "is_late": is_late,
            "penalty_factor": penalty_factor
        }

    @staticmethod
    def compute_rubric_grade(rubric_scores: dict, max_marks: float = 100.0) -> float:
        total = sum(rubric_scores.values())
        return min(round(total, 2), max_marks)
