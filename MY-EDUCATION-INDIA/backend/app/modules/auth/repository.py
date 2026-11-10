import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.modules.auth.models import (
    AuditLog,
    EmailVerificationToken,
    LoginHistory,
    PasswordResetToken,
    Permission,
    RefreshToken,
    Role,
    SystemSetting,
    User,
)


class AuthRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # ==================== User Access ====================
    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        stmt = (
            select(User)
            .options(selectinload(User.roles).selectinload(Role.permissions))
            .where(User.id == user_id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_user_by_any_identifier(
        self,
        identifier: str,
        criterion: Optional[str] = None,
        institute_id: Optional[uuid.UUID] = None,
    ) -> Optional[User]:
        """Dynamically resolves user based on configured identifier criteria."""
        clean_id = identifier.strip()
        lower_id = clean_id.lower()

        stmt = select(User).options(selectinload(User.roles).selectinload(Role.permissions))

        if criterion and criterion != "identifier":
            # Explicit column check
            col = getattr(User, criterion, None)
            if col is not None:
                if criterion in ("email", "username"):
                    stmt = stmt.where(func.lower(col) == lower_id)
                else:
                    stmt = stmt.where(col == clean_id)
        else:
            # Multi-criterion adaptive check
            predicates = [
                func.lower(User.email) == lower_id,
                func.lower(User.username) == lower_id,
                User.phone_number == clean_id,
                User.registration_number == clean_id,
                User.enrollment_number == clean_id,
                User.roll_number == clean_id,
                User.erp_id == clean_id,
                User.student_id == clean_id,
                User.custom_field_identifier == clean_id,
            ]
            stmt = stmt.where(or_(*predicates))

        if institute_id:
            stmt = stmt.where(or_(User.institute_id == institute_id, User.is_super_admin.is_(True)))

        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def create_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        return user

    async def list_users_paginated(
        self,
        institute_id: Optional[uuid.UUID],
        search: Optional[str],
        role_code: Optional[str],
        page: int,
        page_size: int,
    ) -> Tuple[List[User], int]:
        stmt = select(User).options(selectinload(User.roles))
        count_stmt = select(func.count(User.id))

        if institute_id:
            stmt = stmt.where(User.institute_id == institute_id)
            count_stmt = count_stmt.where(User.institute_id == institute_id)

        if search:
            pat = f"%{search.strip()}%"
            filter_expr = or_(
                User.email.ilike(pat),
                User.username.ilike(pat),
                User.first_name.ilike(pat),
                User.last_name.ilike(pat),
                User.roll_number.ilike(pat),
                User.erp_id.ilike(pat),
            )
            stmt = stmt.where(filter_expr)
            count_stmt = count_stmt.where(filter_expr)

        if role_code:
            stmt = stmt.join(User.roles).where(Role.code == role_code.upper())
            count_stmt = count_stmt.join(User.roles).where(Role.code == role_code.upper())

        total_res = await self.session.execute(count_stmt)
        total = int(total_res.scalar_one() or 0)

        stmt = stmt.order_by(User.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
        res = await self.session.execute(stmt)
        return list(res.scalars().all()), total

    # ==================== Refresh Token Sessions ====================
    async def create_refresh_token(self, token: RefreshToken) -> RefreshToken:
        self.session.add(token)
        await self.session.flush()
        return token

    async def get_refresh_token_by_hash(self, token_hash: str) -> Optional[RefreshToken]:
        stmt = (
            select(RefreshToken)
            .options(selectinload(RefreshToken.user).selectinload(User.roles).selectinload(Role.permissions))
            .where(RefreshToken.token_hash == token_hash)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def revoke_refresh_family(self, token_family: str, reason: str) -> None:
        now = datetime.now(timezone.utc)
        stmt = select(RefreshToken).where(
            RefreshToken.token_family == token_family,
            RefreshToken.is_revoked.is_(False),
        )
        res = await self.session.execute(stmt)
        for s in res.scalars().all():
            s.is_revoked = True
            s.revoked_reason = reason
            s.revoked_at = now
        await self.session.flush()

    async def get_active_sessions_for_user(self, user_id: uuid.UUID) -> List[RefreshToken]:
        now = datetime.now(timezone.utc)
        stmt = (
            select(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked.is_(False),
                RefreshToken.expires_at > now,
            )
            .order_by(RefreshToken.created_at.desc())
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def revoke_session_by_id(self, session_id: uuid.UUID, reason: str = "Admin force logout") -> Optional[RefreshToken]:
        now = datetime.now(timezone.utc)
        stmt = select(RefreshToken).where(RefreshToken.id == session_id)
        res = await self.session.execute(stmt)
        token = res.scalar_one_or_none()
        if token:
            token.is_revoked = True
            token.revoked_reason = reason
            token.revoked_at = now
            await self.session.flush()
        return token

    # ==================== Password Reset Tokens ====================
    async def create_password_reset_token(self, token: PasswordResetToken) -> PasswordResetToken:
        self.session.add(token)
        await self.session.flush()
        return token

    async def get_valid_reset_token_by_hash(self, token_hash: str) -> Optional[PasswordResetToken]:
        now = datetime.now(timezone.utc)
        stmt = select(PasswordResetToken).where(
            PasswordResetToken.token_hash == token_hash,
            PasswordResetToken.is_used.is_(False),
            PasswordResetToken.expires_at > now,
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    # ==================== Login History & Audit Logs ====================
    async def record_login_history(self, history: LoginHistory) -> LoginHistory:
        self.session.add(history)
        await self.session.flush()
        return history

    async def update_login_history_logout(self, session_id: str) -> None:
        now = datetime.now(timezone.utc)
        stmt = select(LoginHistory).where(
            LoginHistory.session_id == session_id,
            LoginHistory.logged_out_at.is_(None),
        )
        res = await self.session.execute(stmt)
        for h in res.scalars().all():
            h.logged_out_at = now
        await self.session.flush()

    async def list_login_history_paginated(
        self,
        user_id: Optional[uuid.UUID],
        institute_id: Optional[uuid.UUID],
        page: int,
        page_size: int,
    ) -> Tuple[List[LoginHistory], int]:
        stmt = select(LoginHistory)
        count_stmt = select(func.count(LoginHistory.id))

        if user_id:
            stmt = stmt.where(LoginHistory.user_id == user_id)
            count_stmt = count_stmt.where(LoginHistory.user_id == user_id)
        if institute_id:
            stmt = stmt.where(LoginHistory.institute_id == institute_id)
            count_stmt = count_stmt.where(LoginHistory.institute_id == institute_id)

        total_res = await self.session.execute(count_stmt)
        total = int(total_res.scalar_one() or 0)

        stmt = stmt.order_by(LoginHistory.logged_in_at.desc()).offset((page - 1) * page_size).limit(page_size)
        res = await self.session.execute(stmt)
        return list(res.scalars().all()), total

    async def record_audit_log(self, log_entry: AuditLog) -> AuditLog:
        self.session.add(log_entry)
        await self.session.flush()
        return log_entry

    # ==================== Roles & Permissions ====================
    async def get_role_by_id(self, role_id: uuid.UUID) -> Optional[Role]:
        stmt = select(Role).options(selectinload(Role.permissions)).where(Role.id == role_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_role_by_code(self, code: str, institute_id: Optional[uuid.UUID]) -> Optional[Role]:
        stmt = (
            select(Role)
            .options(selectinload(Role.permissions))
            .where(Role.code == code.upper(), Role.institute_id == institute_id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_roles(self, institute_id: Optional[uuid.UUID]) -> List[Role]:
        stmt = select(Role).options(selectinload(Role.permissions))
        if institute_id:
            stmt = stmt.where(or_(Role.institute_id == institute_id, Role.is_system_role.is_(True)))
        stmt = stmt.order_by(Role.name.asc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_roles_by_ids(self, role_ids: List[uuid.UUID]) -> List[Role]:
        if not role_ids:
            return []
        stmt = select(Role).options(selectinload(Role.permissions)).where(Role.id.in_(role_ids))
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_role(self, role: Role) -> Role:
        self.session.add(role)
        await self.session.flush()
        return role

    async def list_permissions(self, module_key: Optional[str] = None) -> List[Permission]:
        stmt = select(Permission)
        if module_key:
            stmt = stmt.where(Permission.module_key == module_key)
        stmt = stmt.order_by(Permission.module_key.asc(), Permission.code.asc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_permissions_by_codes(self, codes: List[str]) -> List[Permission]:
        if not codes:
            return []
        stmt = select(Permission).where(Permission.code.in_(codes))
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # ==================== Configurable System Settings ====================
    async def get_setting(self, key: str, institute_id: Optional[uuid.UUID]) -> Optional[SystemSetting]:
        stmt = select(SystemSetting).where(
            SystemSetting.key == key,
            SystemSetting.institute_id == institute_id,
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def save_setting(self, setting: SystemSetting) -> SystemSetting:
        self.session.add(setting)
        await self.session.flush()
        return setting
