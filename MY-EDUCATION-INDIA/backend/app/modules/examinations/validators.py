from datetime import date
from typing import List
from app.core.exceptions import ValidationException
from app.modules.examinations.schemas import ExamSubjectItemCreate, StudentMarkItem


class ExamBusinessValidators:
    @staticmethod
    def validate_session_dates(start_date: date, end_date: date) -> None:
        if start_date >= end_date:
            raise ValidationException("Examination session start date must precede end date.")

    @staticmethod
    def validate_marks_within_limits(item: StudentMarkItem, max_marks: float) -> float:
        if item.is_absent:
            return 0.0
        total = item.internal_marks + item.external_marks + item.practical_marks + item.grace_marks + item.moderation_adjustment
        if total < 0.0:
            raise ValidationException("Total marks obtained cannot be negative.")
        if total > max_marks:
            raise ValidationException(f"Total calculated marks ({total}) exceed the maximum allowable marks ({max_marks}).")
        return round(total, 2)

    @staticmethod
    def validate_subject_weightages(item: ExamSubjectItemCreate) -> None:
        if abs((item.weightage_internal_pct + item.weightage_external_pct) - 100.0) > 0.01:
            raise ValidationException("Internal and external weightage percentages must sum strictly to 100.0%.")
