"""
Module 14: Library Fine Calculation Engine
"""
from datetime import datetime
import math

class LibraryFineEngine:
    DEFAULT_DAILY_RATE = 5.0 # INR 5.00 per overdue day
    DEFAULT_GRACE_DAYS = 1
    DEFAULT_MAX_FINE = 500.0

    @classmethod
    def calculate_overdue_fine(
        cls,
        due_date: datetime,
        return_date: datetime,
        daily_rate: float = DEFAULT_DAILY_RATE,
        grace_days: int = DEFAULT_GRACE_DAYS,
        max_fine: float = DEFAULT_MAX_FINE
    ) -> dict:
        if return_date <= due_date:
            return {"overdue_days": 0, "billable_days": 0, "fine_amount": 0.0}

        diff = (return_date.date() - due_date.date()).days
        if diff <= grace_days:
            return {"overdue_days": diff, "billable_days": 0, "fine_amount": 0.0}

        billable_days = diff - grace_days
        fine = round(billable_days * daily_rate, 2)
        fine = min(fine, max_fine)
        return {"overdue_days": diff, "billable_days": billable_days, "fine_amount": fine}
