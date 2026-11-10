import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.security import generate_csrf_token
from app.core.exceptions import ConflictException, ResourceNotFoundException
from app.modules.auth.constants import DEFAULT_AUTH_SETTINGS
from app.modules.auth.exceptions import (
    AccountInactiveException,
    AccountLockedException,
    InvalidCredentialsException,
    ResetTokenInvalidException,
    TokenRevokedException,
)
from app.modules.auth.jwt import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from app.modules.auth.models import (
    AuditLog,
    LoginHistory,
    PasswordResetToken,
    RefreshToken,
    Role,
    SystemSetting,
    User,
)
from app.modules.auth.permissions import PermissionEngine
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import (
    ActiveSessionItem,
    AdminResetPasswordRequest,
    AuthSessionResponse,
    ConfigurableLoginRequest,
    CreateCustomRoleRequest,
    CreateUserRequest,
    LoginHistoryItem,
    PasswordResetConfirmRequest,
    SystemAuthSettingsResponse,
    UpdateAuthSettingsRequest,
    UpdateUserRequest,
    UserProfileResponse,
)
from app.modules.auth.security import (
    generate_secure_token,
    hash_password,
    hash_token,
    validate_password_policy,
    verify_password,
    verify_password_history,
)


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = AuthRepository(session)

    # ==================== Settings Helper ====================
    async def get_effective_auth_settings(self, institute_id: Optional[uuid.UUID] = None) -> Dict[str, Any]:
        setting_row = await self.repo.get_setting("auth_config", institute_id)
        if setting_row and isinstance(setting_row.value, dict):
            merged = {**DEFAULT_AUTH_SETTINGS, **setting_row.value}
            return merged
        return DEFAULT_AUTH_SETTINGS.copy()

    # ==================== Serialization ====================
    def serialize_user_profile(self, user: User) -> UserProfileResponse:
        perms = list(PermissionEngine.get_effective_permissions(user))
        return UserProfileResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            phone_number=user.phone_number,
            first_name=user.first_name,
            last_name=user.last_name,
            registration_number=user.registration_number,
            enrollment_number=user.enrollment_number,
            roll_number=user.roll_number,
            erp_id=user.erp_id,
            student_id=user.student_id,
            is_active=user.is_active,
            is_super_admin=user.is_super_admin,
            is_verified=user.is_verified,
            institute_id=user.institute_id,
            roles=[r for r in user.roles],
            permissions=sorted(perms),
            last_login_at=user.last_login_at,
        )

    # ==================== Authentication Lifecycle ====================
    async def login(
        self,
        payload: ConfigurableLoginRequest,
        ip_address: str,
        user_agent: str,
        device_type: str,
        browser: str,
        os_info: str,
        request_id: str,
        institute_id: Optional[uuid.UUID] = None,
    ) -> Tuple[AuthSessionResponse, str]:
        settings = await self.get_effective_auth_settings(institute_id)
        user = await self.repo.get_user_by_any_identifier(
            payload.identifier,
            criterion=payload.login_criterion,
            institute_id=institute_id,
        )
        now = datetime.now(timezone.utc)

        # Device & criterion label
        used_criterion = payload.login_criterion or "identifier"

        if not user:
            # Record failed login attempt in login_history and audit_logs
            await self.repo.record_login_history(
                LoginHistory(
                    user_id=None,
                    institute_id=institute_id,
                    identifier_used=payload.identifier,
                    login_criterion=used_criterion,
                    status="FAILED",
                    failure_reason="User not found",
                    ip_address=ip_address,
                    user_agent=user_agent[:512],
                    device_type=device_type,
                    browser=browser,
                    os=os_info,
                )
            )
            await self.session.commit()
            raise InvalidCredentialsException("Invalid credentials provided.")

        # Check account lockout
        if user.locked_until and user.locked_until > now:
            unlock_str = user.locked_until.isoformat()
            await self.repo.record_login_history(
                LoginHistory(
                    user_id=user.id,
                    institute_id=user.institute_id,
                    identifier_used=payload.identifier,
                    login_criterion=used_criterion,
                    status="LOCKED",
                    failure_reason="Account temporarily locked",
                    ip_address=ip_address,
                    user_agent=user_agent[:512],
                    device_type=device_type,
                    browser=browser,
                    os=os_info,
                )
            )
            await self.session.commit()
            raise AccountLockedException(
                f"Account is temporarily locked due to excessive failed attempts. Try again after {unlock_str}",
                unlock_time=unlock_str,
            )

        # Check password verification
        if not verify_password(payload.password, user.password_hash):
            user.failed_login_attempts += 1
            max_attempts = settings.get("max_failed_attempts", 5)
            if user.failed_login_attempts >= max_attempts:
                lock_duration = settings.get("lockout_duration_minutes", 15)
                user.locked_until = now + timedelta(minutes=lock_duration)

            await self.repo.record_login_history(
                LoginHistory(
                    user_id=user.id,
                    institute_id=user.institute_id,
                    identifier_used=payload.identifier,
                    login_criterion=used_criterion,
                    status="FAILED",
                    failure_reason="Incorrect password",
                    ip_address=ip_address,
                    user_agent=user_agent[:512],
                    device_type=device_type,
                    browser=browser,
                    os=os_info,
                )
            )
            await self.repo.record_audit_log(
                AuditLog(
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
                    user_agent=user_agent[:512],
                    device_info=device_type,
                    browser=browser,
                    request_id=request_id,
                    changes_payload={"attempts": user.failed_login_attempts},
                )
            )
            await self.session.commit()
            raise InvalidCredentialsException("Invalid credentials provided.")

        # Check active status
        if not user.is_active:
            raise AccountInactiveException("Account is disabled. Please contact the administrator.")

        # Reset failed attempts and update last login
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login_at = now

        # Create JWT Access Token and Refresh Token session in PostgreSQL
        profile = self.serialize_user_profile(user)
        access_token, access_exp = create_access_token(
            user_id=str(user.id),
            institute_id=str(user.institute_id) if user.institute_id else None,
            roles=[r.code for r in user.roles],
            permissions=profile.permissions,
            expire_minutes=settings.get("access_token_expire_minutes", 15),
        )

        raw_refresh, token_family, refresh_exp = create_refresh_token(
            user_id=str(user.id),
            remember_me=payload.remember_me,
            expire_days=settings.get("remember_me_refresh_days", 30) if payload.remember_me else settings.get("refresh_token_expire_days", 7),
        )

        session_record = RefreshToken(
            user_id=user.id,
            token_hash=hash_token(raw_refresh),
            token_family=token_family,
            ip_address=ip_address,
            user_agent=user_agent[:512],
            device_info=f"{browser} on {os_info} ({device_type})",
            expires_at=refresh_exp,
            is_revoked=False,
        )
        await self.repo.create_refresh_token(session_record)

        # Record Successful Login History
        await self.repo.record_login_history(
            LoginHistory(
                user_id=user.id,
                institute_id=user.institute_id,
                identifier_used=payload.identifier,
                login_criterion=used_criterion,
                status="SUCCESS",
                ip_address=ip_address,
                user_agent=user_agent[:512],
                device_type=device_type,
                browser=browser,
                os=os_info,
                session_id=str(session_record.id),
            )
        )

        # Record Audit Log
        await self.repo.record_audit_log(
            AuditLog(
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
                user_agent=user_agent[:512],
                device_info=device_type,
                browser=browser,
                request_id=request_id,
                changes_payload={"session_id": str(session_record.id), "remember_me": payload.remember_me},
            )
        )
        await self.session.commit()

        csrf_token = generate_csrf_token(str(user.id))
        return (
            AuthSessionResponse(
                access_token=access_token,
                expires_at=access_exp,
                csrf_token=csrf_token,
                user=profile,
            ),
            raw_refresh,
        )

    async def refresh_session(
        self,
        raw_refresh: str,
        ip_address: str,
        user_agent: str,
        device_type: str,
        browser: str,
        os_info: str,
        request_id: str,
    ) -> Tuple[AuthSessionResponse, str]:
        decoded = decode_refresh_token(raw_refresh)
        token_h = hash_token(raw_refresh)
        stored_token = await self.repo.get_refresh_token_by_hash(token_h)

        if not stored_token:
            raise TokenRevokedException("Refresh token session was not found.")

        # Reuse Detection: revoke entire session family if revoked token is re-presented
        if stored_token.is_revoked:
            await self.repo.revoke_refresh_family(
                stored_token.token_family,
                reason="Automatic revocation: Replay of already rotated refresh token detected",
            )
            await self.session.commit()
            raise TokenRevokedException("Compromised session detected. Token family revoked.")

        now = datetime.now(timezone.utc)
        if stored_token.expires_at <= now:
            stored_token.is_revoked = True
            stored_token.revoked_reason = "Expired"
            await self.session.commit()
            raise TokenRevokedException("Refresh session has expired. Please login again.")

        user = stored_token.user
        if not user or not user.is_active:
            raise AccountInactiveException("User account is inactive.")

        # Mark current token as rotated
        stored_token.is_revoked = True
        stored_token.revoked_reason = "Rotated"
        stored_token.revoked_at = now

        settings = await self.get_effective_auth_settings(user.institute_id)
        profile = self.serialize_user_profile(user)

        new_access, access_exp = create_access_token(
            user_id=str(user.id),
            institute_id=str(user.institute_id) if user.institute_id else None,
            roles=[r.code for r in user.roles],
            permissions=profile.permissions,
            expire_minutes=settings.get("access_token_expire_minutes", 15),
        )

        remember_me = decoded.get("rem", False)
        new_refresh, token_family, refresh_exp = create_refresh_token(
            user_id=str(user.id),
            family_id=stored_token.token_family,
            remember_me=remember_me,
            expire_days=settings.get("remember_me_refresh_days", 30) if remember_me else settings.get("refresh_token_expire_days", 7),
        )

        new_session_record = RefreshToken(
            user_id=user.id,
            token_hash=hash_token(new_refresh),
            token_family=token_family,
            ip_address=ip_address,
            user_agent=user_agent[:512],
            device_info=f"{browser} on {os_info} ({device_type})",
            expires_at=refresh_exp,
            is_revoked=False,
        )
        await self.repo.create_refresh_token(new_session_record)
        await self.session.commit()

        csrf_token = generate_csrf_token(str(user.id))
        return (
            AuthSessionResponse(
                access_token=new_access,
                expires_at=access_exp,
                csrf_token=csrf_token,
                user=profile,
            ),
            new_refresh,
        )

    async def logout(
        self,
        raw_refresh: Optional[str],
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> None:
        if raw_refresh:
            th = hash_token(raw_refresh)
            stored = await self.repo.get_refresh_token_by_hash(th)
            if stored:
                await self.repo.revoke_refresh_family(stored.token_family, reason="User initiated logout")
                await self.repo.update_login_history_logout(str(stored.id))

        await self.repo.record_audit_log(
            AuditLog(
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
                user_agent=user_agent[:512],
                request_id=request_id,
            )
        )
        await self.session.commit()

    async def change_password(
        self,
        user: User,
        current_password: str,
        new_password: str,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> None:
        if not verify_password(current_password, user.password_hash):
            raise InvalidCredentialsException("Current password is not correct.")

        settings = await self.get_effective_auth_settings(user.institute_id)
        validate_password_policy(new_password, settings)

        # Check password history
        verify_password_history(new_password, user.password_history or [])

        # Maintain history ring buffer
        new_hash = hash_password(new_password)
        history_limit = settings.get("password_history_limit", 5)
        updated_history = [user.password_hash] + (user.password_history or [])
        user.password_history = updated_history[:history_limit]
        user.password_hash = new_hash
        user.password_changed_at = datetime.now(timezone.utc)

        await self.repo.record_audit_log(
            AuditLog(
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
                user_agent=user_agent[:512],
                request_id=request_id,
            )
        )
        await self.session.commit()

    async def initiate_forgot_password(
        self,
        identifier: str,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> str:
        user = await self.repo.get_user_by_any_identifier(identifier)
        if not user or not user.is_active:
            # Constant response to prevent user enumeration attacks
            return "If an active account exists, password reset instructions have been generated."

        raw_token, token_h = generate_secure_token()
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(hours=1)

        token_record = PasswordResetToken(
            user_id=user.id,
            token_hash=token_h,
            expires_at=expires_at,
            ip_address=ip_address,
        )
        await self.repo.create_password_reset_token(token_record)

        await self.repo.record_audit_log(
            AuditLog(
                actor_user_id=user.id,
                institute_id=user.institute_id,
                module_key="authentication",
                action="AUTH_PASSWORD_RESET_REQUESTED",
                resource_type="password_reset_token",
                resource_id=str(token_record.id),
                http_method="POST",
                endpoint_path="/api/v1/auth/forgot-password",
                status_code=200,
                ip_address=ip_address,
                user_agent=user_agent[:512],
                request_id=request_id,
            )
        )
        await self.session.commit()
        # In production this is emailed via SMTP abstraction; returned here for API delivery
        return raw_token

    async def reset_password_with_token(
        self,
        payload: PasswordResetConfirmRequest,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> None:
        token_h = hash_token(payload.token)
        reset_token = await self.repo.get_valid_reset_token_by_hash(token_h)
        if not reset_token:
            raise ResetTokenInvalidException("Reset token is invalid, expired, or already used.")

        user = await self.repo.get_user_by_id(reset_token.user_id)
        if not user or not user.is_active:
            raise AccountInactiveException("User account is inactive.")

        settings = await self.get_effective_auth_settings(user.institute_id)
        validate_password_policy(payload.new_password, settings)
        verify_password_history(payload.new_password, user.password_history or [])

        now = datetime.now(timezone.utc)
        reset_token.is_used = True
        reset_token.used_at = now

        history_limit = settings.get("password_history_limit", 5)
        updated_history = [user.password_hash] + (user.password_history or [])
        user.password_history = updated_history[:history_limit]
        user.password_hash = hash_password(payload.new_password)
        user.password_changed_at = now
        user.failed_login_attempts = 0
        user.locked_until = None

        await self.repo.record_audit_log(
            AuditLog(
                actor_user_id=user.id,
                institute_id=user.institute_id,
                module_key="authentication",
                action="AUTH_PASSWORD_RESET_COMPLETED",
                resource_type="user",
                resource_id=str(user.id),
                http_method="POST",
                endpoint_path="/api/v1/auth/reset-password",
                status_code=200,
                ip_address=ip_address,
                user_agent=user_agent[:512],
                request_id=request_id,
            )
        )
        await self.session.commit()

    # ==================== Admin Features ====================
    async def get_active_sessions(self, user_id: uuid.UUID, current_session_hash: Optional[str] = None) -> List[ActiveSessionItem]:
        sessions = await self.repo.get_active_sessions_for_user(user_id)
        items = []
        for s in sessions:
            items.append(
                ActiveSessionItem(
                    id=s.id,
                    device_info=s.device_info,
                    ip_address=s.ip_address,
                    user_agent=s.user_agent,
                    created_at=s.created_at,
                    expires_at=s.expires_at,
                    is_current=(s.token_hash == current_session_hash) if current_session_hash else False,
                )
            )
        return items

    async def force_logout_session(
        self,
        session_id: uuid.UUID,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> None:
        revoked = await self.repo.revoke_session_by_id(session_id, reason=f"Force logout by {actor.username}")
        if not revoked:
            raise ResourceNotFoundException("Session", session_id)

        await self.repo.update_login_history_logout(str(session_id))
        await self.repo.record_audit_log(
            AuditLog(
                actor_user_id=actor.id,
                institute_id=actor.institute_id,
                module_key="authentication",
                action="AUTH_ADMIN_FORCE_LOGOUT",
                resource_type="refresh_token",
                resource_id=str(session_id),
                http_method="POST",
                endpoint_path=f"/api/v1/auth/admin/sessions/{session_id}/revoke",
                status_code=200,
                ip_address=ip_address,
                user_agent=user_agent[:512],
                request_id=request_id,
            )
        )
        await self.session.commit()

    async def create_user(
        self,
        payload: CreateUserRequest,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> UserProfileResponse:
        existing = await self.repo.get_user_by_any_identifier(payload.email)
        if existing:
            raise ConflictException(f"User with email '{payload.email}' already exists.")

        settings = await self.get_effective_auth_settings(payload.institute_id or actor.institute_id)
        validate_password_policy(payload.password, settings)

        roles = await self.repo.get_roles_by_ids(payload.role_ids)
        new_user = User(
            email=payload.email.lower(),
            username=payload.username,
            phone_number=payload.phone_number,
            first_name=payload.first_name,
            last_name=payload.last_name,
            password_hash=hash_password(payload.password),
            registration_number=payload.registration_number,
            enrollment_number=payload.enrollment_number,
            roll_number=payload.roll_number,
            erp_id=payload.erp_id,
            student_id=payload.student_id,
            is_active=True,
            is_super_admin=payload.is_super_admin if actor.is_super_admin else False,
            is_verified=True,
            institute_id=payload.institute_id or actor.institute_id,
            roles=roles,
            password_history=[],
        )
        await self.repo.create_user(new_user)

        await self.repo.record_audit_log(
            AuditLog(
                actor_user_id=actor.id,
                institute_id=new_user.institute_id,
                module_key="role_management",
                action="USER_PROVISIONED",
                resource_type="user",
                resource_id=str(new_user.id),
                http_method="POST",
                endpoint_path="/api/v1/auth/admin/users",
                status_code=201,
                ip_address=ip_address,
                user_agent=user_agent[:512],
                request_id=request_id,
                changes_payload={"email": new_user.email, "username": new_user.username},
            )
        )
        await self.session.commit()
        await self.session.refresh(new_user)
        return self.serialize_user_profile(new_user)

    async def update_user(
        self,
        user_id: uuid.UUID,
        payload: UpdateUserRequest,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> UserProfileResponse:
        user = await self.repo.get_user_by_id(user_id)
        if not user:
            raise ResourceNotFoundException("User", user_id)

        update_dict = payload.model_dump(exclude_unset=True)
        if "role_ids" in update_dict:
            user.roles = await self.repo.get_roles_by_ids(payload.role_ids or [])
            del update_dict["role_ids"]

        for k, v in update_dict.items():
            setattr(user, k, v)

        await self.repo.record_audit_log(
            AuditLog(
                actor_user_id=actor.id,
                institute_id=user.institute_id,
                module_key="role_management",
                action="USER_UPDATED",
                resource_type="user",
                resource_id=str(user.id),
                http_method="PATCH",
                endpoint_path=f"/api/v1/auth/admin/users/{user.id}",
                status_code=200,
                ip_address=ip_address,
                user_agent=user_agent[:512],
                request_id=request_id,
                changes_payload=update_dict,
            )
        )
        await self.session.commit()
        await self.session.refresh(user)
        return self.serialize_user_profile(user)

    async def admin_reset_password(
        self,
        user_id: uuid.UUID,
        new_password: str,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> None:
        user = await self.repo.get_user_by_id(user_id)
        if not user:
            raise ResourceNotFoundException("User", user_id)

        settings = await self.get_effective_auth_settings(user.institute_id)
        validate_password_policy(new_password, settings)

        user.password_hash = hash_password(new_password)
        user.failed_login_attempts = 0
        user.locked_until = None

        await self.repo.record_audit_log(
            AuditLog(
                actor_user_id=actor.id,
                institute_id=user.institute_id,
                module_key="role_management",
                action="ADMIN_PASSWORD_RESET",
                resource_type="user",
                resource_id=str(user.id),
                http_method="POST",
                endpoint_path=f"/api/v1/auth/admin/users/{user.id}/reset-password",
                status_code=200,
                ip_address=ip_address,
                user_agent=user_agent[:512],
                request_id=request_id,
            )
        )
        await self.session.commit()

    async def create_custom_role(
        self,
        payload: CreateCustomRoleRequest,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> Role:
        existing = await self.repo.get_role_by_code(payload.code, actor.institute_id)
        if existing:
            raise ConflictException(f"Role with code '{payload.code}' already exists.")

        permissions = await self.repo.get_permissions_by_codes(payload.permission_codes)
        new_role = Role(
            code=payload.code.upper(),
            name=payload.name,
            description=payload.description,
            portal_subdomain=payload.portal_subdomain,
            is_system_role=False,
            institute_id=actor.institute_id,
            permissions=permissions,
        )
        await self.repo.create_role(new_role)

        await self.repo.record_audit_log(
            AuditLog(
                actor_user_id=actor.id,
                institute_id=actor.institute_id,
                module_key="role_management",
                action="CUSTOM_ROLE_CREATED",
                resource_type="role",
                resource_id=str(new_role.id),
                http_method="POST",
                endpoint_path="/api/v1/auth/admin/roles",
                status_code=201,
                ip_address=ip_address,
                user_agent=user_agent[:512],
                request_id=request_id,
                changes_payload={"code": new_role.code, "name": new_role.name},
            )
        )
        await self.session.commit()
        await self.session.refresh(new_role)
        return new_role

    async def update_auth_settings(
        self,
        payload: UpdateAuthSettingsRequest,
        actor: User,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> Dict[str, Any]:
        inst_id = actor.institute_id
        setting = await self.repo.get_setting("auth_config", inst_id)
        current_val = setting.value if setting and isinstance(setting.value, dict) else DEFAULT_AUTH_SETTINGS.copy()

        updates = payload.model_dump(exclude_unset=True)
        merged = {**current_val, **updates}

        if setting:
            setting.value = merged
        else:
            setting = SystemSetting(
                key="auth_config",
                category="auth",
                value=merged,
                description="Institutional Authentication & Password Security Configuration",
                is_public=True,
                institute_id=inst_id,
            )
            await self.repo.save_setting(setting)

        await self.repo.record_audit_log(
            AuditLog(
                actor_user_id=actor.id,
                institute_id=inst_id,
                module_key="settings",
                action="AUTH_SETTINGS_UPDATED",
                resource_type="system_setting",
                resource_id=str(setting.id),
                http_method="PUT",
                endpoint_path="/api/v1/auth/admin/settings",
                status_code=200,
                ip_address=ip_address,
                user_agent=user_agent[:512],
                request_id=request_id,
                changes_payload=updates,
            )
        )
        await self.session.commit()
        return merged
