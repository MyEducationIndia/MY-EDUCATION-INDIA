import uuid
from typing import Callable
from fastapi import Depends, Header, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.security import decode_access_token, verify_csrf_token
from app.core.exceptions import (
    ForbiddenException,
    ModuleDisabledException,
    UnauthorizedException,
)
from app.db.session import get_db_session
from app.models.user import User
from app.repositories.institute_repository import InstituteRepository
from app.repositories.user_repository import UserRepository

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db_session),
) -> User:
    if not credentials or not credentials.credentials:
        raise UnauthorizedException("Missing Bearer authorization token.")

    payload = decode_access_token(credentials.credentials)
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise UnauthorizedException("Invalid token subject.")

    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(uuid.UUID(user_id_str))
    if not user or not user.is_active:
        raise UnauthorizedException("User account is inactive or no longer exists.")

    request.state.user_id = str(user.id)
    return user


async def enforce_csrf_protection(
    request: Request,
    x_csrf_token: str | None = Header(default=None, alias="X-CSRF-Token"),
    current_user: User = Depends(get_current_user),
) -> None:
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        if not x_csrf_token or not verify_csrf_token(str(current_user.id), x_csrf_token):
            raise ForbiddenException("CSRF token validation failed.")


def require_permissions(*required_codes: str, module_key: str | None = None) -> Callable:
    async def dependency(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db_session),
    ) -> User:
        if module_key and current_user.institute_id:
            inst_repo = InstituteRepository(db)
            mod_cfg = await inst_repo.get_module_config(current_user.institute_id, module_key)
            if mod_cfg and not mod_cfg.is_enabled:
                raise ModuleDisabledException(module_key)

        if current_user.is_super_admin:
            return current_user

        granted_codes = {
            perm.code
            for role in current_user.roles
            for perm in role.permissions
        }
        missing = [code for code in required_codes if code not in granted_codes]
        if missing:
            raise ForbiddenException(
                f"Missing required permission(s): {', '.join(missing)}"
            )
        return current_user

    return dependency
