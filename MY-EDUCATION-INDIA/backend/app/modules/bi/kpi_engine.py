"""
Module 18: KPI Evaluation Engine
"""
class KpiEvaluationEngine:
    @staticmethod
    def evaluate_status(current: float, warning: float, critical: float, higher_is_better: bool = True) -> str:
        if higher_is_better:
            if current >= warning:
                return "NORMAL"
            elif current >= critical:
                return "WARNING"
            return "CRITICAL"
        else:
            if current <= warning:
                return "NORMAL"
            elif current <= critical:
                return "WARNING"
            return "CRITICAL"
