"""
Module 14: Library Business Validators
"""
import re
from typing import Optional

class LibraryBusinessValidators:
    @staticmethod
    def validate_isbn(isbn: str) -> bool:
        clean = isbn.replace("-", "").replace(" ", "").strip()
        if len(clean) == 10:
            if not (clean[:9].isdigit() and (clean[9].isdigit() or clean[9].upper() == 'X')):
                return False
            val = sum((10 - i) * (int(c) if c.isdigit() else 10) for i, c in enumerate(clean))
            return val % 11 == 0
        elif len(clean) == 13:
            if not clean.isdigit():
                return False
            val = sum(int(c) * (1 if i % 2 == 0 else 3) for i, c in enumerate(clean))
            return val % 10 == 0
        return False

    @staticmethod
    def validate_member_borrow_limit(current_issued: int, max_limit: int) -> bool:
        return current_issued < max_limit

    @staticmethod
    def validate_overdue_fine_eligibility(fines_due: float, max_allowed_fines: float = 200.0) -> bool:
        return fines_due < max_allowed_fines
