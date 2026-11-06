import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    generate_csrf_token,
    hash_password,
    hash_token_identifier,
    verify_password,
)
from app.core.exceptions import ForbiddenException, UnauthorizedException
from app.models.refresh_token import RefreshTokenSession
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    AuthenticatedUserResponse,
    LoginRequest,
    PasswordChangeRequest,
    TokenSessionResponse,
)
from app.services.audit_service import AuditService

MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repo = UserRepository(session)
        self.audit_service = AuditService(session)

    def _serialize_user(self, user: User) -> AuthenticatedUserResponse:
        roles = [role.code for role in user.roles]
        perms = sorted(
            {perm.code for role in user.roles for perm in role.permissions}
        )
        if user.is_super_admin and "*" not in perms:
            perms.append("*")
        return AuthenticatedUserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            phone_number=user.phone_number,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_super_admin=user.is_super_admin,
            is_verified=user.is_verified,
            institute_id=user.institute_id,
            roles=roles,
            permissions=perms,
            last_login_at=user.last_login_at,
        )

    async def authenticate_user(
        self,
        payload: LoginRequest,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> tuple[TokenSessionResponse, str]:
        user = await self.user_repo.get_by_identifier(payload.identifier)
        now = datetime.now(timezone.utc)

        if not user:
            raise UnauthorizedException("Invalid username/email or password.")

        if user.locked_until and user.locked_until > now:
            raise ForbiddenException(
                f"Account is temporarily locked due to repeated failed attempts until {user.locked_until.isoformat()}."
            )

        if not verify_password(payload.password, user.password_hash):
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
                user.locked_until = now + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
            await self.audit_service.record_event(
                actor_user_id=user.id,
                institute_id=user.institute_id,
                module_key="authentication",
                action="AUTH_LOGIN_FAILED",
                resource_type="user",
                resource_id=str(user.id),
                http_method="POST",
                endpoint_path="/api/v1/auth/login",
                status_code=401,
                ip_address=ip_address,
                user_agent=user_agent,
                request_id=request_id,
                changes_payload={"failed_attempts": user.failed_login_attempts},
            )
            await self.session.commit()
            raise UnauthorizedException("Invalid username/email or password.")

        if not user.is_active:
            raise ForbiddenException("Your user account has been deactivated by an administrator.")

        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login_at = now

        serialized_user = self._serialize_user(user)
        access_token, access_expires_at = create_access_token(
            subject=str(user.id),
            institute_id=str(user.institute_id) if user.institute_id else None,
            roles=serialized_user.roles,
            permissions=serialized_user.permissions,
        )
        raw_refresh_token, token_family, refresh_expires_at = create_refresh_token(
            subject=str(user.id)
        )

        refresh_session = RefreshTokenSession(
            user_id=user.id,
            token_hash=hash_token_identifier(raw_refresh_token),
            token_family=token_family,
            ip_address=ip_address,
            user_agent=user_agent[:512],
            expires_at=refresh_expires_at,
            is_revoked=False,
        )
        await self.user_repo.save_refresh_session(refresh_session)

        csrf_token = generate_csrf_token(str(user.id))

        await self.audit_service.record_event(
            actor_user_id=user.id,
            institute_id=user.institute_id,
            module_key="authentication",
            action="AUTH_LOGIN_SUCCESS",
            resource_type="user",
            resource_id=str(user.id),
            http_method="POST",
            endpoint_path="/api/v1/auth/login",
            status_code=200,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            changes_payload={"token_family": token_family},
        )
        await self.session.commit()

        return (
            TokenSessionResponse(
                access_token=access_token,
                expires_at=access_expires_at,
                csrf_token=csrf_token,
                user=serialized_user,
            ),
            raw_refresh_token,
        )

    async def rotate_refresh_token(
        self,
        raw_refresh_token: str,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> tuple[TokenSessionResponse, str]:
        decoded = decode_refresh_token(raw_refresh_token)
        token_hash = hash_token_identifier(raw_refresh_token)
        stored_session = await self.user_repo.get_refresh_session_by_hash(token_hash)

        if not stored_session:
            raise UnauthorizedException("Refresh session not recognized.")

        if stored_session.is_revoked:
            # Reuse detection: revoke entire token family immediately
            await self.user_repo.revoke_token_family(
                stored_session.token_family, reason="Compromised refresh token reuse detected"
            )
            await self.session.commit()
            raise UnauthorizedException("Refresh token has already been rotated or revoked.")

        now = datetime.now(timezone.utc)
        if stored_session.expires_at <= now:
            stored_session.is_revoked = True
            stored_session.revoked_reason = "Expired"
            await self.session.commit()
            raise UnauthorizedException("Refresh token session has expired.")

        user = await self.user_repo.get_by_id(stored_session.user_id)
        if not user or not user.is_active:
            raise UnauthorizedException("User is no longer active.")

        # Mark old refresh token as rotated
        stored_session.is_revoked = True
        stored_session.revoked_reason = "Rotated"

        serialized_user = self._serialize_user(user)
        access_token, access_expires_at = create_access_token(
            subject=str(user.id),
            institute_id=str(user.institute_id) if user.institute_id else None,
            roles=serialized_user.roles,
            permissions=serialized_user.permissions,
        )
        new_raw_refresh, token_family, refresh_expires_at = create_refresh_token(
            subject=str(user.id),
            family_id=stored_session.token_family,
        )
        new_session = RefreshTokenSession(
            user_id=user.id,
            token_hash=hash_token_identifier(new_raw_refresh),
            token_family=token_family,
            ip_address=ip_address,
            user_agent=user_agent[:512],
            expires_at=refresh_expires_at,
            is_revoked=False,
        )
        await self.user_repo.save_refresh_session(new_session)
        await self.session.commit()

        csrf_token = generate_csrf_token(str(user.id))
        return (
            TokenSessionResponse(
                access_token=access_token,
                expires_at=access_expires_at,
                csrf_token=csrf_token,
                user=serialized_user,
            ),
            new_raw_refresh,
        )

    async def revoke_session(
        self,
        raw_refresh_token: str | None,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> None:
        if raw_refresh_token:
            token_hash = hash_token_identifier(raw_refresh_token)
            stored = await self.user_repo.get_refresh_session_by_hash(token_hash)
            if stored:
                await self.user_repo.revoke_token_family(
                    stored.token_family, reason="User initiated logout"
                )
        await self.audit_service.record_event(
            actor_user_id=actor.id,
            institute_id=actor.institute_id,
            module_key="authentication",
            action="AUTH_LOGOUT",
            resource_type="user",
            resource_id=str(actor.id),
            http_method="POST",
            endpoint_path="/api/v1/auth/logout",
            status_code=200,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
        )
        await self.session.commit()

    async def change_password(
        self,
        user: User,
        payload: PasswordChangeRequest,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> None:
        if not verify_password(payload.current_password, user.password_hash):
            raise UnauthorizedException("Current password verification failed.")
        user.password_hash = hash_password(payload.new_password)
        await self.audit_service.record_event(
            actor_user_id=user.id,
            institute_id=user.institute_id,
            module_key="authentication",
            action="AUTH_PASSWORD_CHANGED",
            resource_type="user",
            resource_id=str(user.id),
            http_method="POST",
            endpoint_path="/api/v1/auth/change-password",
            status_code=200,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
        )
        await self.session.commit()
