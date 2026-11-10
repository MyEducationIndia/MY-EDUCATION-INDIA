"""
Module 14: Library Circulation & Issue Engine
"""
from datetime import datetime, timedelta

class CirculationEngine:
    @staticmethod
    def calculate_due_date(issue_date: datetime, period_days: int) -> datetime:
        return issue_date + timedelta(days=period_days)

    @staticmethod
    def can_renew(current_renewals: int, max_renewals: int = 2) -> bool:
        return current_renewals < max_renewals

    @staticmethod
    def calculate_renewal_due_date(current_due_date: datetime, extension_days: int = 14) -> datetime:
        return current_due_date + timedelta(days=extension_days)
