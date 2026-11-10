from typing import Dict, Tuple


class UGCGradingEngine:
    """Official UGC/AICTE CBCS & NEP 10-Point Letter Grading Scale."""

    # Scale: (min_pct, letter_grade, grade_point, description, is_passing)
    UGC_10_POINT_SCALE = [
        (90.0, "O", 10.0, "Outstanding", True),
        (80.0, "A+", 9.0, "Excellent", True),
        (70.0, "A", 8.0, "Very Good", True),
        (60.0, "B+", 7.0, "Good", True),
        (55.0, "B", 6.0, "Above Average", True),
        (50.0, "C", 5.0, "Average", True),
        (40.0, "P", 4.0, "Pass", True),
        (0.0, "F", 0.0, "Fail", False),
    ]

    @staticmethod
    def percentage_to_grade(percentage: float) -> Tuple[str, float, str, bool]:
        pct = round(percentage, 2)
        for min_pct, letter, point, desc, passing in UGCGradingEngine.UGC_10_POINT_SCALE:
            if pct >= min_pct:
                return letter, point, desc, passing
        return "F", 0.0, "Fail", False

    @staticmethod
    def get_division(cgpa: float) -> str:
        if cgpa >= 8.5:
            return "FIRST_CLASS_WITH_DISTINCTION"
        elif cgpa >= 6.5:
            return "FIRST_CLASS"
        elif cgpa >= 5.5:
            return "SECOND_CLASS"
        elif cgpa >= 4.0:
            return "PASS_CLASS"
        return "FAILED"
