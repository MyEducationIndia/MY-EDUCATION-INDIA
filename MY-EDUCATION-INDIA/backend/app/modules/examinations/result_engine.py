from typing import Any, Dict, List
from app.modules.examinations.grading_engine import UGCGradingEngine


class ResultCalculationEngine:
    """Calculates Semester Grade Point Average (SGPA), CGPA, Credits, and Pass/Fail Classifications."""

    @staticmethod
    def compute_sgpa(subject_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_credits_registered = 0.0
        total_credits_earned = 0.0
        total_credit_points = 0.0
        total_marks = 0.0
        total_max_marks = 0.0
        backlogs = 0

        for sub in subject_records:
            credits = float(sub.get("credits", 4.0))
            max_marks = float(sub.get("max_marks", 100.0))
            marks_obtained = float(sub.get("total_marks_obtained", 0.0))
            is_absent = bool(sub.get("is_absent", False))

            pct = (marks_obtained / max_marks * 100.0) if max_marks > 0 else 0.0
            letter, point, desc, passing = UGCGradingEngine.percentage_to_grade(pct)

            total_credits_registered += credits
            total_marks += marks_obtained
            total_max_marks += max_marks

            if passing and not is_absent:
                total_credits_earned += credits
                total_credit_points += (credits * point)
            else:
                backlogs += 1

        sgpa = round(total_credit_points / total_credits_registered, 2) if total_credits_registered > 0 else 0.0
        overall_pct = round(total_marks / total_max_marks * 100.0, 2) if total_max_marks > 0 else 0.0
        classification = UGCGradingEngine.get_division(sgpa)

        status = "PASSED"
        if backlogs > 0:
            status = "PROMOTED_WITH_BACKLOG" if backlogs <= 3 else "FAILED"

        return {
            "total_credits_registered": total_credits_registered,
            "total_credits_earned": total_credits_earned,
            "total_marks_obtained": total_marks,
            "total_max_marks": total_max_marks,
            "percentage": overall_pct,
            "sgpa": sgpa,
            "cgpa": sgpa, # Single semester equivalence
            "classification": classification,
            "status": status,
            "backlog_count": backlogs,
        }
