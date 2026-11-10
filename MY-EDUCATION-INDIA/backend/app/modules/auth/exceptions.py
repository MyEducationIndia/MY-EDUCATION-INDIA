from typing import Any, Dict, Optional
from fastapi import status
from app.core.exceptions import EnterpriseAppException


class InvalidCredentialsException(EnterpriseAppException):
    def __init__(self, message: str = "Invalid login credentials provided.") -> None:
        super().__init__(
            message=message,
            code="AUTH_INVALID_CREDENTIALS",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class AccountLockedException(EnterpriseAppException):
    def __init__(self, message: str, unlock_time: Optional[str] = None) -> None:
        super().__init__(
            message=message,
            code="AUTH_ACCOUNT_LOCKED",
            status_code=status.HTTP_423_LOCKED,
            details={"unlock_time": unlock_time} if unlock_time else {},
        )


class AccountInactiveException(EnterpriseAppException):
    def __init__(self, message: str = "Your user account is inactive or disabled.") -> None:
        super().__init__(
            message=message,
            code="AUTH_ACCOUNT_INACTIVE",
            status_code=status.HTTP_403_FORBIDDEN,
        )


class TokenRevokedException(EnterpriseAppException):
    def __init__(self, message: str = "Token has been revoked or session terminated.") -> None:
        super().__init__(
            message=message,
            code="AUTH_TOKEN_REVOKED",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class PasswordPolicyException(EnterpriseAppException):
    def __init__(self, message: str, violations: Optional[list] = None) -> None:
        super().__init__(
            message=message,
            code="AUTH_PASSWORD_POLICY_VIOLATION",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details={"violations": violations or []},
        )


class PasswordHistoryException(EnterpriseAppException):
    def __init__(self, message: str = "You cannot reuse your recent passwords.") -> None:
        super().__init__(
            message=message,
            code="AUTH_PASSWORD_REUSE_FORBIDDEN",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class ResetTokenInvalidException(EnterpriseAppException):
    def __init__(self, message: str = "Password reset token is invalid, used, or expired.") -> None:
        super().__init__(
            message=message,
            code="AUTH_RESET_TOKEN_INVALID",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
