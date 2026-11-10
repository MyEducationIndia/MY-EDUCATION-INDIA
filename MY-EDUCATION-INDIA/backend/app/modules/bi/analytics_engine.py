"""
Module 18: Predictive Analytics & Health Score Engine
"""
from typing import List

class PredictiveAnalyticsEngine:
    @staticmethod
    def compute_moving_average(series: List[float], window: int = 3) -> List[float]:
        if len(series) < window or window <= 0:
            return series[:]
        result = []
        for i in range(len(series)):
            if i < window - 1:
                result.append(round(sum(series[:i+1]) / (i+1), 2))
            else:
                result.append(round(sum(series[i-window+1:i+1]) / window, 2))
        return result

    @staticmethod
    def compute_institute_health_score(
        attendance_pct: float,
        fee_collection_pct: float,
        exam_pass_pct: float,
        lead_conversion_pct: float
    ) -> float:
        # Weighted institutional composite score
        score = (
            (attendance_pct * 0.25) +
            (fee_collection_pct * 0.35) +
            (exam_pass_pct * 0.25) +
            (lead_conversion_pct * 0.15)
        )
        return round(min(max(score, 0.0), 100.0), 2)
