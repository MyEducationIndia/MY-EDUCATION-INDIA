from datetime import datetime
from app.core.exceptions import ValidationException
from app.modules.cbt.schemas import QuestionVersionCreate


class CBTBusinessValidators:
    @staticmethod
    def validate_question_data(payload: QuestionVersionCreate) -> None:
        if payload.question_type in ["MCQ", "MSQ", "TRUE_FALSE"] and not payload.options:
            raise ValidationException("Objective question must define at least two answer options.")
        if payload.question_type in ["MCQ", "TRUE_FALSE"] and len(payload.correct_answers) != 1:
            raise ValidationException("Single-choice questions must define exactly one correct answer.")
        if payload.negative_marks > payload.default_marks:
            raise ValidationException("Negative marking penalty cannot exceed positive default marks.")

    @staticmethod
    def validate_session_window(start: datetime, end: datetime) -> None:
        if start >= end:
            raise ValidationException("Examination start window must precede the closing window.")
