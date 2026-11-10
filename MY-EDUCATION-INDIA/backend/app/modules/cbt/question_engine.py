from typing import Any, List, Tuple


class QuestionEvaluationEngine:
    """Evaluates student responses against question criteria across all supported test question formats."""

    @staticmethod
    def evaluate_response(
        question_type: str,
        user_selected: List[Any],
        user_text: str | None,
        correct_answers: List[Any],
        positive_marks: float,
        negative_marks: float,
    ) -> Tuple[bool, float]:
        if not user_selected and not user_text:
            return False, 0.0 # Unanswered: 0 marks

        if question_type in ["MCQ", "TRUE_FALSE"]:
            # Single option match
            if user_selected and str(user_selected[0]) == str(correct_answers[0]):
                return True, positive_marks
            return False, -abs(negative_marks)

        elif question_type == "MSQ":
            # Multiple select question: strict match of sets
            user_set = {str(x) for x in user_selected}
            correct_set = {str(x) for x in correct_answers}
            if user_set == correct_set:
                return True, positive_marks
            return False, -abs(negative_marks)

        elif question_type == "NUMERICAL":
            try:
                user_val = float(user_text.strip()) if user_text else None
                correct_val = float(correct_answers[0])
                if user_val is not None and abs(user_val - correct_val) < 0.01:
                    return True, positive_marks
                return False, -abs(negative_marks)
            except (ValueError, TypeError):
                return False, -abs(negative_marks)

        # Subjective or Default
        return True, positive_marks
