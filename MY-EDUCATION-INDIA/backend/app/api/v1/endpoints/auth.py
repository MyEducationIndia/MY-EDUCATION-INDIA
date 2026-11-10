import uuid
from typing import List, Optional
from fastapi import APIRouter, Cookie, Depends, Query, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import generate_csrf_token, hash_token_identifier
from app.core.config import get_settings
from app.core.exceptions import UnauthorizedException
from app.db.session import get_db_session
from app.models.user import User
from app.permissions.rbac_dependencies import (
    enforce_csrf_protection,
    get_current_user,
    require_permissions,
)
from app.schemas.auth import (
    ActiveSessionItem,
    AuthenticatedUserResponse,
    LoginHistoryItem,
    LoginRequest,
    MfaSetupResponse,
    MfaVerifyRequest,
    OtpRequestPayload,
    OtpVerifyPayload,
    PasswordChangeRequest,
    PasswordResetConfirmPayload,
    PasswordResetRequestPayload,
    SecurityPolicyResponse,
    SecurityPolicyUpdateRequest,
    TokenSessionResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication & Identity Management"])
REFRESH_COOKIE_NAME = "mei_refresh_token"


def _set_refresh_cookie(response: Response, raw_refresh_token: str, remember_me: bool = False) -> None:
    settings = get_settings()
    days = 30 if remember_me else settings.REFRESH_TOKEN_EXPIRE_DAYS
    max_age = days * 86400
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=raw_refresh_token,
        max_age=max_age,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="strict",
        domain=settings.COOKIE_DOMAIN,
        path="/api/v1/auth",
    )


@router.post("/login", response_model=TokenSessionResponse, status_code=status.HTTP_200_OK)
async def login(
    payload: LoginRequest,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db_session),
) -> TokenSessionResponse:
    service = AuthService(db)
    session_response, raw_refresh_token = await service.authenticate_user(
        payload=payload,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )
    _set_refresh_cookie(response, raw_refresh_token, remember_me=payload.remember_me)
    return session_response


# OTP Authentication
@router.post("/login/otp/request", status_code=status.HTTP_200_OK)
async def request_login_otp(
    payload: OtpRequestPayload,
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    from fastapi import HTTPException
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="OTP login is disabled by Enterprise Security Policy. Authentication is restricted strictly to User ID + Password only."
    )


@router.post("/login/otp/verify", response_model=TokenSessionResponse, status_code=status.HTTP_200_OK)
async def verify_login_otp(
    payload: OtpVerifyPayload,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db_session),
) -> TokenSessionResponse:
    service = AuthService(db)
    session_response, raw_refresh_token = await service.authenticate_with_otp(
        identifier=payload.identifier,
        otp_code=payload.otp_code,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )
    _set_refresh_cookie(response, raw_refresh_token)
    return session_response


# Password Reset via OTP
@router.post("/password-reset/request", status_code=status.HTTP_200_OK)
async def request_password_reset(
    payload: PasswordResetRequestPayload,
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    from fastapi import HTTPException
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Self-service password reset is disabled by Enterprise Security Policy. Contact campus administrator for verified temporary password assignment."
    )


@router.post("/password-reset/confirm", status_code=status.HTTP_200_OK)
async def confirm_password_reset(
    payload: PasswordResetConfirmPayload,
    request: Request,
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    service = AuthService(db)
    await service.confirm_password_reset(
        email=str(payload.email),
        otp_code=payload.otp_code,
        new_password=payload.new_password,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )
    return {"success": True, "message": "Password reset confirmed. You may now log in with your new credentials."}


# Multi-Factor Authentication (MFA / 2FA)
@router.post("/mfa/setup", response_model=MfaSetupResponse, status_code=status.HTTP_200_OK)
async def setup_mfa(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> MfaSetupResponse:
    service = AuthService(db)
    return await service.setup_mfa(current_user)


@router.post("/mfa/verify", status_code=status.HTTP_200_OK)
async def verify_mfa(
    payload: MfaVerifyRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    service = AuthService(db)
    await service.verify_and_enable_mfa(current_user, payload.code)
    return {"success": True, "message": "Two-factor authentication verified and enabled successfully."}


# Active Sessions & Device Management
@router.get("/sessions/active", response_model=List[ActiveSessionItem], status_code=status.HTTP_200_OK)
async def list_active_sessions(
    mei_refresh_token: Optional[str] = Cookie(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> List[ActiveSessionItem]:
    service = AuthService(db)
    current_hash = hash_token_identifier(mei_refresh_token) if mei_refresh_token else None
    return await service.list_active_sessions(current_user, current_token_hash=current_hash)


@router.delete("/sessions/{session_id}", status_code=status.HTTP_200_OK)
async def revoke_active_session(
    session_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    service = AuthService(db)
    await service.revoke_session_by_id(session_id, current_user)
    return {"success": True, "message": "Device session revoked successfully."}


@router.post("/sessions/revoke-all", status_code=status.HTTP_200_OK)
async def revoke_all_other_sessions(
    mei_refresh_token: Optional[str] = Cookie(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    service = AuthService(db)
    current_hash = hash_token_identifier(mei_refresh_token) if mei_refresh_token else None
    count = await service.revoke_all_sessions(current_user, current_token_hash=current_hash)
    return {"success": True, "revoked_sessions_count": count, "message": "All other device sessions have been revoked."}


# Login History Audit
@router.get("/login-history", response_model=List[LoginHistoryItem], status_code=status.HTTP_200_OK)
async def get_login_history(
    limit: int = Query(default=50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> List[LoginHistoryItem]:
    service = AuthService(db)
    # If super admin, can see all history; regular users see only their own
    uid = None if current_user.is_super_admin else current_user.id
    return await service.list_login_history(user_id=uid, limit=limit)


# Institutional Security Policies
@router.get("/security-policy", response_model=SecurityPolicyResponse, status_code=status.HTTP_200_OK)
async def get_security_policy(
    db: AsyncSession = Depends(get_db_session),
) -> SecurityPolicyResponse:
    service = AuthService(db)
    return await service.get_security_policy()


@router.patch("/security-policy", response_model=SecurityPolicyResponse, status_code=status.HTTP_200_OK)
async def update_security_policy(
    payload: SecurityPolicyUpdateRequest,
    current_user: User = Depends(require_permissions("security:write", module_key="platform_admin")),
    db: AsyncSession = Depends(get_db_session),
) -> SecurityPolicyResponse:
    service = AuthService(db)
    return await service.update_security_policy(payload)


@router.post("/refresh", response_model=TokenSessionResponse, status_code=status.HTTP_200_OK)
async def refresh_session(
    request: Request,
    response: Response,
    mei_refresh_token: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db_session),
) -> TokenSessionResponse:
    if not mei_refresh_token:
        raise UnauthorizedException("No active refresh token cookie found.")
    service = AuthService(db)
    session_response, new_raw_refresh = await service.rotate_refresh_token(
        raw_refresh_token=mei_refresh_token,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )
    _set_refresh_cookie(response, new_raw_refresh)
    return session_response


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(enforce_csrf_protection)],
)
async def logout(
    request: Request,
    response: Response,
    mei_refresh_token: str | None = Cookie(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    service = AuthService(db)
    await service.revoke_session(
        raw_refresh_token=mei_refresh_token,
        actor=current_user,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )
    response.delete_cookie(key=REFRESH_COOKIE_NAME, path="/api/v1/auth")
    return {"success": True, "message": "Session terminated and refresh token revoked."}


@router.get("/me", response_model=AuthenticatedUserResponse, status_code=status.HTTP_200_OK)
async def get_current_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> AuthenticatedUserResponse:
    service = AuthService(db)
    return service._serialize_user(current_user)


@router.post(
    "/change-password",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(enforce_csrf_protection)],
)
async def change_password(
    payload: PasswordChangeRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    service = AuthService(db)
    await service.change_password(
        user=current_user,
        payload=payload,
        ip_address=getattr(request.state, "client_ip", "127.0.0.1"),
        user_agent=request.headers.get("User-Agent", "unknown"),
        request_id=getattr(request.state, "request_id", "unknown"),
    )
    return {
        "success": True,
        "message": "Password updated successfully.",
        "csrf_token": generate_csrf_token(str(current_user.id)),
    }
