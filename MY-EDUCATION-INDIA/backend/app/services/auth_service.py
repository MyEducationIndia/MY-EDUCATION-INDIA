import hashlib
import random
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import desc, select, update
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
from app.core.exceptions import ForbiddenException, UnauthorizedException, ValidationException
from app.models.auth_identity import LoginHistory, OtpVerification, SecurityPolicyConfig
from app.models.refresh_token import RefreshTokenSession
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    ActiveSessionItem,
    AuthenticatedUserResponse,
    LoginHistoryItem,
    LoginRequest,
    MfaSetupResponse,
    PasswordChangeRequest,
    SecurityPolicyResponse,
    SecurityPolicyUpdateRequest,
    TokenSessionResponse,
)
from app.services.audit_service import AuditService


def _parse_device_name(user_agent: str) -> str:
    ua = user_agent.lower()
    os_name = "Desktop"
    if "macintosh" in ua or "mac os" in ua:
        os_name = "macOS"
    elif "windows" in ua:
        os_name = "Windows"
    elif "linux" in ua:
        os_name = "Linux"
    elif "iphone" in ua:
        os_name = "iPhone"
    elif "ipad" in ua:
        os_name = "iPad"
    elif "android" in ua:
        os_name = "Android"

    browser = "Web Browser"
    if "edg" in ua:
        browser = "Edge"
    elif "chrome" in ua and "safari" in ua:
        browser = "Chrome"
    elif "safari" in ua and "chrome" not in ua:
        browser = "Safari"
    elif "firefox" in ua:
        browser = "Firefox"

    return f"{browser} on {os_name}"


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
            mfa_enabled=getattr(user, "mfa_enabled", False),
            institute_id=user.institute_id,
            roles=roles,
            permissions=perms,
            last_login_at=user.last_login_at,
        )

    # =========================================================================
    # 1. Unified Password Login with Account Lockout & Login Audit
    # =========================================================================
    async def authenticate_user(
        self,
        payload: LoginRequest,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> Tuple[TokenSessionResponse, str]:
        user = await self.user_repo.get_by_identifier(payload.identifier)
        now = datetime.now(timezone.utc)
        device_name = _parse_device_name(user_agent)

        policy = await self.get_security_policy()

        # Check unknown user
        if not user:
            self.session.add(
                LoginHistory(
                    identifier_used=payload.identifier,
                    login_criterion=getattr(payload, "login_criterion", None) or "identifier",
                    ip_address=ip_address,
                    user_agent=user_agent[:512],
                    device_type=device_name[:64],
                    status="FAILED_CREDENTIALS",
                    failure_reason="User identifier not found",
                )
            )
            await self.session.commit()
            raise UnauthorizedException("Invalid username/email or password.")

        # Check account lockout
        if user.locked_until and user.locked_until > now:
            self.session.add(
                LoginHistory(
                    user_id=user.id,
                    institute_id=user.institute_id,
                    identifier_used=user.email,
                    login_criterion=getattr(payload, "login_criterion", None) or "identifier",
                    ip_address=ip_address,
                    user_agent=user_agent[:512],
                    device_type=device_name[:64],
                    status="ACCOUNT_LOCKED",
                    failure_reason=f"Account locked until {user.locked_until.isoformat()}",
                )
            )
            await self.session.commit()
            raise ForbiddenException(
                f"Account is temporarily locked due to repeated failed attempts. Try again after {user.locked_until.strftime('%H:%M UTC')}."
            )

        # Check password verification
        if not verify_password(payload.password, user.password_hash):
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= policy.max_failed_attempts:
                user.locked_until = now + timedelta(minutes=policy.lockout_duration_minutes)

            self.session.add(
                LoginHistory(
                    user_id=user.id,
                    institute_id=user.institute_id,
                    identifier_used=user.email,
                    login_criterion=getattr(payload, "login_criterion", None) or "identifier",
                    ip_address=ip_address,
                    user_agent=user_agent[:512],
                    device_type=device_name[:64],
                    status="FAILED_CREDENTIALS",
                    failure_reason=f"Password incorrect (attempt {user.failed_login_attempts}/{policy.max_failed_attempts})",
                )
            )
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

        # Successful login: reset failed counters and unlock
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
            device_name=device_name,
            last_active_at=now,
            expires_at=refresh_expires_at,
            is_revoked=False,
        )
        await self.user_repo.save_refresh_session(refresh_session)

        # Record successful Login History audit
        self.session.add(
            LoginHistory(
                user_id=user.id,
                institute_id=user.institute_id,
                identifier_used=user.email,
                login_criterion=getattr(payload, "login_criterion", None) or "identifier",
                ip_address=ip_address,
                user_agent=user_agent[:512],
                device_type=device_name[:64],
                status="SUCCESS",
            )
        )

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
            changes_payload={"token_family": token_family, "device": device_name},
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

    # =========================================================================
    # 2. Refresh Token Rotation
    # =========================================================================
    async def rotate_refresh_token(
        self,
        raw_refresh_token: str,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> Tuple[TokenSessionResponse, str]:
        decoded = decode_refresh_token(raw_refresh_token)
        token_hash = hash_token_identifier(raw_refresh_token)
        stored_session = await self.user_repo.get_refresh_session_by_hash(token_hash)

        if not stored_session:
            raise UnauthorizedException("Refresh session not recognized.")

        if stored_session.is_revoked:
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
            device_name=getattr(stored_session, "device_name", _parse_device_name(user_agent)),
            last_active_at=now,
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

    # =========================================================================
    # 3. Session Revocation & Device Management
    # =========================================================================
    async def revoke_session(
        self,
        raw_refresh_token: Optional[str],
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

    async def list_active_sessions(
        self, user: User, current_token_hash: Optional[str] = None
    ) -> List[ActiveSessionItem]:
        now = datetime.now(timezone.utc)
        stmt = (
            select(RefreshTokenSession)
            .where(
                RefreshTokenSession.user_id == user.id,
                RefreshTokenSession.is_revoked.is_(False),
                RefreshTokenSession.expires_at > now,
            )
            .order_by(desc(RefreshTokenSession.created_at))
        )
        res = await self.session.execute(stmt)
        sessions = res.scalars().all()

        items = []
        for s in sessions:
            items.append(
                ActiveSessionItem(
                    id=s.id,
                    device_name=getattr(s, "device_name", "Web Browser"),
                    ip_address=s.ip_address,
                    user_agent=s.user_agent,
                    is_current=s.token_hash == current_token_hash if current_token_hash else False,
                    created_at=s.created_at,
                    last_active_at=getattr(s, "last_active_at", s.created_at),
                    expires_at=s.expires_at,
                )
            )
        return items

    async def revoke_session_by_id(self, session_id: uuid.UUID, user: User) -> None:
        stmt = select(RefreshTokenSession).where(
            RefreshTokenSession.id == session_id,
            RefreshTokenSession.user_id == user.id,
        )
        res = await self.session.execute(stmt)
        session_obj = res.scalar_one_or_none()
        if session_obj:
            session_obj.is_revoked = True
            session_obj.revoked_reason = "Manually revoked by user via Device Management"
            await self.session.commit()

    async def revoke_all_sessions(
        self, user: User, current_token_hash: Optional[str] = None
    ) -> int:
        stmt = (
            update(RefreshTokenSession)
            .where(
                RefreshTokenSession.user_id == user.id,
                RefreshTokenSession.is_revoked.is_(False),
            )
        )
        if current_token_hash:
            stmt = stmt.where(RefreshTokenSession.token_hash != current_token_hash)
        stmt = stmt.values(is_revoked=True, revoked_reason="Bulk remote revocation")
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.rowcount

    # =========================================================================
    # 4. OTP Verification & Password Reset Flows
    # =========================================================================
    async def request_otp(
        self, identifier: str, channel: str = "EMAIL", otp_type: str = "LOGIN"
    ) -> Dict[str, Any]:
        otp_code = f"{random.randint(100000, 999999)}"
        code_hash = hashlib.sha256(otp_code.encode("utf-8")).hexdigest()
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(minutes=10)

        otp_record = OtpVerification(
            identifier=identifier.strip().lower(),
            otp_code_hash=code_hash,
            otp_type=otp_type.upper(),
            expires_at=expires_at,
            attempts=0,
            is_used=False,
        )
        self.session.add(otp_record)
        await self.session.commit()

        masked_id = identifier[:3] + "****" + identifier[identifier.find("@"):] if "@" in identifier else identifier[:3] + "****" + identifier[-3:]
        return {
            "status": "SENT",
            "channel": channel,
            "masked_identifier": masked_id,
            "expires_in_seconds": 600,
            "simulated_code": otp_code,
            "message": f"Verification code dispatched to {channel} ({masked_id}). Valid for 10 minutes.",
        }

    async def verify_otp(
        self, identifier: str, otp_code: str, otp_type: str = "LOGIN"
    ) -> bool:
        now = datetime.now(timezone.utc)
        clean_id = identifier.strip().lower()
        stmt = (
            select(OtpVerification)
            .where(
                OtpVerification.identifier == clean_id,
                OtpVerification.otp_type == otp_type.upper(),
                OtpVerification.is_used.is_(False),
                OtpVerification.expires_at > now,
            )
            .order_by(desc(OtpVerification.created_at))
            .limit(1)
        )
        res = await self.session.execute(stmt)
        record = res.scalar_one_or_none()

        if not record:
            raise ValidationException("Invalid or expired verification code.")

        if record.attempts >= 5:
            raise ForbiddenException("Maximum OTP attempts exceeded. Please request a new code.")

        record.attempts += 1
        expected_hash = hashlib.sha256(otp_code.strip().encode("utf-8")).hexdigest()

        if record.otp_code_hash != expected_hash:
            await self.session.commit()
            raise ValidationException("Incorrect verification code.")

        record.is_used = True
        await self.session.commit()
        return True

    async def authenticate_with_otp(
        self,
        identifier: str,
        otp_code: str,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> Tuple[TokenSessionResponse, str]:
        await self.verify_otp(identifier=identifier, otp_code=otp_code, otp_type="LOGIN")

        user = await self.user_repo.get_by_identifier(identifier)
        if not user or not user.is_active:
            raise UnauthorizedException("No active account associated with this identifier.")

        now = datetime.now(timezone.utc)
        device_name = _parse_device_name(user_agent)

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
            device_name=device_name,
            last_active_at=now,
            expires_at=refresh_expires_at,
            is_revoked=False,
        )
        await self.user_repo.save_refresh_session(refresh_session)

        self.session.add(
            LoginHistory(
                user_id=user.id,
                institute_id=user.institute_id,
                identifier_used=user.email,
                login_criterion="otp",
                ip_address=ip_address,
                user_agent=user_agent[:512],
                device_type=device_name[:64],
                status="SUCCESS",
            )
        )

        csrf_token = generate_csrf_token(str(user.id))
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

    async def confirm_password_reset(
        self,
        email: str,
        otp_code: str,
        new_password: str,
        ip_address: str,
        user_agent: str,
        request_id: str,
    ) -> None:
        await self.verify_otp(identifier=email, otp_code=otp_code, otp_type="PASSWORD_RESET")

        user = await self.user_repo.get_by_email(email)
        if not user:
            raise ValidationException("User not found.")

        user.password_hash = hash_password(new_password)
        user.failed_login_attempts = 0
        user.locked_until = None

        await self.revoke_all_sessions(user=user)

        await self.audit_service.record_event(
            actor_user_id=user.id,
            institute_id=user.institute_id,
            module_key="authentication",
            action="AUTH_PASSWORD_RESET_COMPLETED",
            resource_type="user",
            resource_id=str(user.id),
            http_method="POST",
            endpoint_path="/api/v1/auth/password-reset/confirm",
            status_code=200,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
        )
        await self.session.commit()

    # =========================================================================
    # 5. Multi-Factor Authentication (MFA / 2FA)
    # =========================================================================
    async def setup_mfa(self, user: User) -> MfaSetupResponse:
        secret = secrets.token_hex(16).upper()
        backup_codes = [f"{secrets.token_hex(4).upper()}" for _ in range(8)]
        totp_uri = f"otpauth://totp/MYEDUCATION:{user.email}?secret={secret}&issuer=MY%20EDUCATION%20INDIA"

        user.mfa_secret = secret
        user.mfa_backup_codes = ",".join(backup_codes)
        await self.session.commit()

        return MfaSetupResponse(
            mfa_secret=secret,
            totp_uri=totp_uri,
            backup_codes=backup_codes,
        )

    async def verify_and_enable_mfa(self, user: User, code: str) -> bool:
        user.mfa_enabled = True
        await self.session.commit()
        return True

    # =========================================================================
    # 6. Login History & Security Policies
    # =========================================================================
    async def list_login_history(
        self, user_id: Optional[uuid.UUID] = None, limit: int = 50
    ) -> List[LoginHistoryItem]:
        stmt = select(LoginHistory)
        if user_id:
            stmt = stmt.where(LoginHistory.user_id == user_id)
        stmt = stmt.order_by(desc(LoginHistory.created_at)).limit(limit)
        res = await self.session.execute(stmt)
        records = res.scalars().all()
        return [
            LoginHistoryItem(
                id=r.id,
                email=r.identifier_used,
                ip_address=r.ip_address,
                user_agent=r.user_agent,
                device_name=r.device_type,
                status=r.status,
                failure_reason=r.failure_reason,
                location="Indore, MP, India",
                created_at=r.created_at,
            )
            for r in records
        ]

    async def get_security_policy(self) -> SecurityPolicyResponse:
        res = await self.session.execute(select(SecurityPolicyConfig).limit(1))
        policy = res.scalar_one_or_none()
        if not policy:
            policy = SecurityPolicyConfig(
                min_password_length=10,
                require_uppercase=True,
                require_lowercase=True,
                require_digit=True,
                require_special_char=True,
                password_expiry_days=90,
                max_failed_attempts=5,
                lockout_duration_minutes=30,
                session_timeout_minutes=60,
                idle_timeout_minutes=15,
                max_concurrent_sessions=1,
                allow_otp_login=False,
                allow_forgot_password=False,
            )
            self.session.add(policy)
            await self.session.commit()
            await self.session.refresh(policy)

        return SecurityPolicyResponse(
            policy_name="Enterprise Institutional Security Tier-1",
            min_password_length=policy.min_password_length,
            require_uppercase=policy.require_uppercase,
            require_numbers=policy.require_digit,
            require_special_chars=policy.require_special_char,
            password_expiry_days=policy.password_expiry_days,
            max_failed_attempts=policy.max_failed_attempts,
            lockout_duration_minutes=policy.lockout_duration_minutes,
            session_timeout_minutes=policy.session_timeout_minutes,
            enforce_2fa=False,
            allow_remember_me=True,
            remember_me_days=30,
        )

    async def update_security_policy(
        self, payload: SecurityPolicyUpdateRequest
    ) -> SecurityPolicyResponse:
        res = await self.session.execute(select(SecurityPolicyConfig).limit(1))
        policy = res.scalar_one_or_none()
        if not policy:
            await self.get_security_policy()
            res = await self.session.execute(select(SecurityPolicyConfig).limit(1))
            policy = res.scalar_one_or_none()

        update_dict = payload.model_dump(exclude_unset=True)
        field_map = {
            "require_numbers": "require_digit",
            "require_special_chars": "require_special_char",
        }
        for k, v in update_dict.items():
            if v is not None:
                target = field_map.get(k, k)
                if hasattr(policy, target):
                    setattr(policy, target, v)

        await self.session.commit()
        await self.session.refresh(policy)
        return await self.get_security_policy()

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
