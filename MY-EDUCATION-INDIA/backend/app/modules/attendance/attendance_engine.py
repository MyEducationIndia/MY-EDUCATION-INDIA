from datetime import date
from typing import Any, Dict
import uuid


class AttendanceCalculationEngine:
    """Calculates attendance percentages, verifies UGC/AICTE 75% rule, and evaluates exam eligibility."""

    @staticmethod
    def compute_percentage(total_classes: int, attended_classes: int) -> float:
        if total_classes <= 0:
            return 100.0
        pct = (attended_classes / total_classes) * 100.0
        return round(pct, 2)

    @staticmethod
    def check_exam_eligibility(
        total_classes: int,
        attended_classes: int,
        threshold_pct: float = 75.0,
    ) -> Dict[str, Any]:
        pct = AttendanceCalculationEngine.compute_percentage(total_classes, attended_classes)
        is_eligible = pct >= threshold_pct
        shortfall_classes = 0
        if not is_eligible:
            numerator = (threshold_pct / 100.0 * total_classes) - attended_classes
            denominator = 1.0 - (threshold_pct / 100.0)
            shortfall_classes = max(1, int(round(numerator / denominator))) if denominator > 0 else 0

        return {
            "attendance_percentage": pct,
            "threshold_percentage": threshold_pct,
            "is_exam_eligible": is_eligible,
            "classes_shortfall": shortfall_classes,
        }
