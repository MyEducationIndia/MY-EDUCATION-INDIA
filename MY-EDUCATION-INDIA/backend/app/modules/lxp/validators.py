"""
Module 15: LXP Business Validators
"""
import re

class LXPBusinessValidators:
    @staticmethod
    def validate_course_code(code: str) -> bool:
        if not code or len(code) < 3 or len(code) > 20:
            return False
        return bool(re.match(r'^[A-Z0-9_-]+$', code.upper()))

    @staticmethod
    def validate_lesson_type(lesson_type: str) -> bool:
        valid_types = {
            "VIDEO", "PDF", "PRESENTATION", "ARTICLE", "HTML_LESSON",
            "EXTERNAL_LINK", "YOUTUBE_EMBED", "AUDIO", "DOWNLOAD",
            "ASSIGNMENT", "QUIZ", "PRACTICE_TEST", "CBT_SESSION"
        }
        return lesson_type.upper() in valid_types

    @staticmethod
    def validate_enrollment_eligibility(is_free: bool, fee_cleared: bool) -> bool:
        if is_free:
            return True
        return fee_cleared

    @staticmethod
    def validate_marks(obtained: float, max_marks: float) -> bool:
        return 0.0 <= obtained <= max_marks
