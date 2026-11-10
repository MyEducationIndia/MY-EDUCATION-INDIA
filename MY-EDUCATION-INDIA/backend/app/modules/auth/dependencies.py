import uuid
from typing import Callable, List
from fastapi import Depends, Header, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.security import verify_csrf_token
from app.core.exceptions import ForbiddenException, UnauthorizedException
from app.db.session import get_db_session
from app.modules.auth.jwt import decode_access_token
from app.modules.auth.models import User
from app.modules.auth.permissions import PermissionEngine
from app.modules.auth.repository import AuthRepository

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db_session),
) -> User:
    if not credentials or not credentials.credentials:
        raise UnauthorizedException("Authentication token required in Authorization header.")

    payload = decode_access_token(credentials.credentials)
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise UnauthorizedException("Invalid token payload: missing subject claim.")

    repo = AuthRepository(db)
    user = await repo.get_user_by_id(uuid.UUID(user_id_str))
    if not user or not user.is_active:
        raise UnauthorizedException("User account does not exist or has been disabled.")

    request.state.user_id = str(user.id)
    return user


async def enforce_csrf(
    request: Request,
    x_csrf_token: str | None = Header(default=None, alias="X-CSRF-Token"),
    current_user: User = Depends(get_current_user),
) -> None:
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        if not x_csrf_token or not verify_csrf_token(str(current_user.id), x_csrf_token):
            raise ForbiddenException("CSRF protection check failed. Request blocked.")


def require_permissions(*required_permissions: str) -> Callable:
    async def permission_dependency(
        current_user: User = Depends(get_current_user),
    ) -> User:
        for perm in required_permissions:
            if not PermissionEngine.has_permission(current_user, perm):
                raise ForbiddenException(
                    f"Access Denied: Missing required institutional permission '{perm}'."
                )
        return current_user

    return permission_dependency


def require_roles(*required_roles: str) -> Callable:
    async def role_dependency(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.is_super_admin:
            return current_user

        user_role_codes = {r.code for r in current_user.roles}
        allowed = any(r.upper() in user_role_codes for r in required_roles)
        if not allowed:
            raise ForbiddenException(
                f"Access Denied: This operation requires one of these roles: {', '.join(required_roles)}."
            )
        return current_user

    return role_dependency
