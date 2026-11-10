"""
Module 19: Platform Security Engine
"""
import re

class PlatformSecurityEngine:
    @staticmethod
    def verify_password_strength(password: str, min_len: int = 10, req_upper: bool = True, req_num: bool = True, req_spec: bool = True) -> dict:
        reasons = []
        if len(password) < min_len:
            reasons.append(f"Minimum length is {min_len}")
        if req_upper and not re.search(r'[A-Z]', password):
            reasons.append("Must contain uppercase letter")
        if req_num and not re.search(r'[0-9]', password):
            reasons.append("Must contain a digit")
        if req_spec and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            reasons.append("Must contain a special character")
        return {
            "is_valid": len(reasons) == 0,
            "violations": reasons
        }

    @staticmethod
    def is_locked_out(failed_attempts: int, max_attempts: int = 5) -> bool:
        return failed_attempts >= max_attempts
