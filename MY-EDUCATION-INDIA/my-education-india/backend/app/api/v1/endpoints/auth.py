from fastapi import APIRouter, Cookie, Depends, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.security import generate_csrf_token
from app.core.config import get_settings
from app.core.exceptions import UnauthorizedException
from app.db.session import get_db_session
from app.models.user import User
from app.permissions.rbac_dependencies import (
    enforce_csrf_protection,
    get_current_user,
)
from app.schemas.auth import (
    AuthenticatedUserResponse,
    LoginRequest,
    PasswordChangeRequest,
    TokenSessionResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])
REFRESH_COOKIE_NAME = "mei_refresh_token"


def _set_refresh_cookie(response: Response, raw_refresh_token: str) -> None:
    settings = get_settings()
    max_age = settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400
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
    _set_refresh_cookie(response, raw_refresh_token)
    return session_response


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
