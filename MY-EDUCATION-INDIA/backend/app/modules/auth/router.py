import uuid
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Cookie, Depends, Query, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import get_settings
from app.core.exceptions import UnauthorizedException
from app.db.session import get_db_session
from app.modules.auth.dependencies import (
    enforce_csrf,
    get_current_user,
    require_permissions,
)
from app.modules.auth.models import User
from app.modules.auth.schemas import (
    ActiveSessionItem,
    AdminResetPasswordRequest,
    AuthSessionResponse,
    ChangePasswordRequest,
    ConfigurableLoginRequest,
    CreateCustomRoleRequest,
    CreateUserRequest,
    LoginHistoryItem,
    PasswordResetConfirmRequest,
    PasswordResetInitiateRequest,
    PermissionSummary,
    RoleSummary,
    SystemAuthSettingsResponse,
    UpdateAuthSettingsRequest,
    UpdateUserRequest,
    UserProfileResponse,
)
from app.modules.auth.service import AuthService

auth_router = APIRouter(prefix="/auth", tags=["Enterprise Authentication & Authorization"])
admin_auth_router = APIRouter(prefix="/auth/admin", tags=["Auth Administration & Governance"])

COOKIE_NAME = "mei_refresh_token"


def _set_refresh_cookie(response: Response, raw_refresh: str, remember_me: bool = False) -> None:
    settings = get_settings()
    max_age = (30 if remember_me else settings.REFRESH_TOKEN_EXPIRE_DAYS) * 86400
    response.set_cookie(
        key=COOKIE_NAME,
        value=raw_refresh,
        max_age=max_age,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="strict",
        domain=settings.COOKIE_DOMAIN,
        path="/api/v1/auth",
    )


def _extract_request_meta(request: Request) -> Dict[str, Any]:
    ua = request.headers.get("User-Agent", "Unknown")
    ip = getattr(request.state, "client_ip", "127.0.0.1")
    req_id = getattr(request.state, "request_id", str(uuid.uuid4()))

    device_type = "Mobile" if any(k in ua.lower() for k in ["mobi", "android", "iphone"]) else "Desktop"
    browser = "Chrome" if "chrome" in ua.lower() else ("Safari" if "safari" in ua.lower() else "Generic Browser")
    os_info = "Windows" if "windows" in ua.lower() else ("Mac" if "mac" in ua.lower() else ("Linux" if "linux" in ua.lower() else "Other OS"))

    return {
        "ip_address": ip,
        "user_agent": ua,
        "device_type": device_type,
        "browser": browser,
        "os_info": os_info,
        "request_id": req_id,
    }


# ==================== Core Public Auth Endpoints ====================

@auth_router.post("/login", response_model=AuthSessionResponse, status_code=status.HTTP_200_OK)
async def login(
    payload: ConfigurableLoginRequest,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db_session),
) -> AuthSessionResponse:
    meta = _extract_request_meta(request)
    service = AuthService(db)
    session_resp, raw_refresh = await service.login(
        payload=payload,
        ip_address=meta["ip_address"],
        user_agent=meta["user_agent"],
        device_type=meta["device_type"],
        browser=meta["browser"],
        os_info=meta["os_info"],
        request_id=meta["request_id"],
    )
    _set_refresh_cookie(response, raw_refresh, remember_me=payload.remember_me)
    return session_resp


@auth_router.post("/refresh", response_model=AuthSessionResponse, status_code=status.HTTP_200_OK)
async def refresh_token(
    request: Request,
    response: Response,
    mei_refresh_token: Optional[str] = Cookie(default=None),
    db: AsyncSession = Depends(get_db_session),
) -> AuthSessionResponse:
    if not mei_refresh_token:
        raise UnauthorizedException("No active refresh token cookie found in request.")

    meta = _extract_request_meta(request)
    service = AuthService(db)
    session_resp, new_refresh = await service.refresh_session(
        raw_refresh=mei_refresh_token,
        ip_address=meta["ip_address"],
        user_agent=meta["user_agent"],
        device_type=meta["device_type"],
        browser=meta["browser"],
        os_info=meta["os_info"],
        request_id=meta["request_id"],
    )
    _set_refresh_cookie(response, new_refresh)
    return session_resp


@auth_router.post("/logout", status_code=status.HTTP_200_OK, dependencies=[Depends(enforce_csrf)])
async def logout(
    request: Request,
    response: Response,
    mei_refresh_token: Optional[str] = Cookie(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    meta = _extract_request_meta(request)
    service = AuthService(db)
    await service.logout(
        raw_refresh=mei_refresh_token,
        actor=current_user,
        ip_address=meta["ip_address"],
        user_agent=meta["user_agent"],
        request_id=meta["request_id"],
    )
    response.delete_cookie(key=COOKIE_NAME, path="/api/v1/auth")
    return {"success": True, "message": "Successfully logged out and revoked session."}


@auth_router.get("/me", response_model=UserProfileResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> UserProfileResponse:
    service = AuthService(db)
    return service.serialize_user_profile(current_user)


@auth_router.get("/permissions", response_model=List[str])
async def get_my_permissions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> List[str]:
    service = AuthService(db)
    profile = service.serialize_user_profile(current_user)
    return profile.permissions


@auth_router.get("/session", response_model=UserProfileResponse)
async def verify_active_session(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> UserProfileResponse:
    return AuthService(db).serialize_user_profile(current_user)


@auth_router.post("/change-password", status_code=status.HTTP_200_OK, dependencies=[Depends(enforce_csrf)])
async def change_password(
    payload: ChangePasswordRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    meta = _extract_request_meta(request)
    service = AuthService(db)
    await service.change_password(
        user=current_user,
        current_password=payload.current_password,
        new_password=payload.new_password,
        ip_address=meta["ip_address"],
        user_agent=meta["user_agent"],
        request_id=meta["request_id"],
    )
    return {"success": True, "message": "Password changed successfully."}


@auth_router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(
    payload: PasswordResetInitiateRequest,
    request: Request,
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    meta = _extract_request_meta(request)
    service = AuthService(db)
    reset_token = await service.initiate_forgot_password(
        identifier=payload.identifier,
        ip_address=meta["ip_address"],
        user_agent=meta["user_agent"],
        request_id=meta["request_id"],
    )
    return {
        "success": True,
        "message": "Password reset instructions generated.",
        "reset_token": reset_token, # Delivered in response for API verification
    }


@auth_router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    payload: PasswordResetConfirmRequest,
    request: Request,
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    meta = _extract_request_meta(request)
    service = AuthService(db)
    await service.reset_password_with_token(
        payload=payload,
        ip_address=meta["ip_address"],
        user_agent=meta["user_agent"],
        request_id=meta["request_id"],
    )
    return {"success": True, "message": "Password reset successfully. You may now sign in with your new password."}


@auth_router.get("/config", response_model=SystemAuthSettingsResponse)
async def get_public_auth_configuration(
    db: AsyncSession = Depends(get_db_session),
) -> SystemAuthSettingsResponse:
    service = AuthService(db)
    effective = await service.get_effective_auth_settings(None)
    return SystemAuthSettingsResponse(
        login_criteria=effective["login_criteria"],
        allow_remember_me=effective["allow_remember_me"],
        password_min_length=effective["password_min_length"],
        password_require_uppercase=effective["password_require_uppercase"],
        password_require_lowercase=effective["password_require_lowercase"],
        password_require_number=effective["password_require_number"],
        password_require_special=effective["password_require_special"],
        session_timeout_minutes=effective["session_timeout_minutes"],
    )


# ==================== Admin Governance Endpoints ====================

@admin_auth_router.get("/users")
async def list_users(
    institute_id: Optional[uuid.UUID] = Query(default=None),
    search: Optional[str] = Query(default=None),
    role: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(require_permissions("users.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    service = AuthService(db)
    eff_inst = institute_id if current_user.is_super_admin else current_user.institute_id
    users, total = await service.repo.list_users_paginated(eff_inst, search, role, page, page_size)
    return {
        "items": [service.serialize_user_profile(u) for u in users],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@admin_auth_router.post("/users", status_code=status.HTTP_201_CREATED, dependencies=[Depends(enforce_csrf)])
async def create_user(
    payload: CreateUserRequest,
    request: Request,
    current_user: User = Depends(require_permissions("users.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> UserProfileResponse:
    meta = _extract_request_meta(request)
    service = AuthService(db)
    return await service.create_user(payload, current_user, meta["ip_address"], meta["user_agent"], meta["request_id"])


@admin_auth_router.patch("/users/{user_id}", dependencies=[Depends(enforce_csrf)])
async def update_user(
    user_id: uuid.UUID,
    payload: UpdateUserRequest,
    request: Request,
    current_user: User = Depends(require_permissions("users.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> UserProfileResponse:
    meta = _extract_request_meta(request)
    service = AuthService(db)
    return await service.update_user(user_id, payload, current_user, meta["ip_address"], meta["user_agent"], meta["request_id"])


@admin_auth_router.post("/users/{user_id}/reset-password", dependencies=[Depends(enforce_csrf)])
async def admin_reset_user_password(
    user_id: uuid.UUID,
    payload: AdminResetPasswordRequest,
    request: Request,
    current_user: User = Depends(require_permissions("users.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    meta = _extract_request_meta(request)
    service = AuthService(db)
    await service.admin_reset_password(user_id, payload.new_password, current_user, meta["ip_address"], meta["user_agent"], meta["request_id"])
    return {"success": True, "message": "User password has been reset by administrator."}


@admin_auth_router.get("/users/{user_id}/sessions", response_model=List[ActiveSessionItem])
async def list_user_active_sessions(
    user_id: uuid.UUID,
    current_user: User = Depends(require_permissions("users.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> List[ActiveSessionItem]:
    service = AuthService(db)
    return await service.get_active_sessions(user_id)


@admin_auth_router.post("/sessions/{session_id}/revoke", dependencies=[Depends(enforce_csrf)])
async def force_logout_session(
    session_id: uuid.UUID,
    request: Request,
    current_user: User = Depends(require_permissions("users.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    meta = _extract_request_meta(request)
    service = AuthService(db)
    await service.force_logout_session(session_id, current_user, meta["ip_address"], meta["user_agent"], meta["request_id"])
    return {"success": True, "message": "Session has been forcefully terminated."}


@admin_auth_router.get("/login-history")
async def list_login_history(
    user_id: Optional[uuid.UUID] = Query(default=None),
    institute_id: Optional[uuid.UUID] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
    current_user: User = Depends(require_permissions("audit.view")),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    service = AuthService(db)
    eff_inst = institute_id if current_user.is_super_admin else current_user.institute_id
    items, total = await service.repo.list_login_history_paginated(user_id, eff_inst, page, page_size)
    return {
        "items": [LoginHistoryItem.model_validate(h) for h in items],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@admin_auth_router.get("/roles", response_model=List[RoleSummary])
async def list_all_roles(
    current_user: User = Depends(require_permissions("users.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> List[RoleSummary]:
    service = AuthService(db)
    roles = await service.repo.list_roles(current_user.institute_id)
    return [RoleSummary.model_validate(r) for r in roles]


@admin_auth_router.post("/roles", response_model=RoleSummary, status_code=status.HTTP_201_CREATED, dependencies=[Depends(enforce_csrf)])
async def create_custom_role(
    payload: CreateCustomRoleRequest,
    request: Request,
    current_user: User = Depends(require_permissions("users.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> RoleSummary:
    meta = _extract_request_meta(request)
    service = AuthService(db)
    role = await service.create_custom_role(payload, current_user, meta["ip_address"], meta["user_agent"], meta["request_id"])
    return RoleSummary.model_validate(role)


@admin_auth_router.get("/permissions", response_model=List[PermissionSummary])
async def list_all_permissions(
    current_user: User = Depends(require_permissions("users.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> List[PermissionSummary]:
    service = AuthService(db)
    perms = await service.repo.list_permissions()
    return [PermissionSummary.model_validate(p) for p in perms]


@admin_auth_router.get("/settings", response_model=Dict[str, Any])
async def get_institutional_auth_settings(
    current_user: User = Depends(require_permissions("settings.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> Dict[str, Any]:
    service = AuthService(db)
    return await service.get_effective_auth_settings(current_user.institute_id)


@admin_auth_router.put("/settings", response_model=Dict[str, Any], dependencies=[Depends(enforce_csrf)])
async def update_institutional_auth_settings(
    payload: UpdateAuthSettingsRequest,
    request: Request,
    current_user: User = Depends(require_permissions("settings.manage")),
    db: AsyncSession = Depends(get_db_session),
) -> Dict[str, Any]:
    meta = _extract_request_meta(request)
    service = AuthService(db)
    return await service.update_auth_settings(payload, current_user, meta["ip_address"], meta["user_agent"], meta["request_id"])
