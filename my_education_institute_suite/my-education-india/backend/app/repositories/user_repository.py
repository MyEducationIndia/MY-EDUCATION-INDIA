import uuid
from typing import List, Tuple
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.refresh_token import RefreshTokenSession
from app.models.role import Role
from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        stmt = (
            select(User)
            .options(selectinload(User.roles).selectinload(Role.permissions))
            .where(User.id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_identifier(self, identifier: str) -> User | None:
        normalized = identifier.strip().lower()
        stmt = (
            select(User)
            .options(selectinload(User.roles).selectinload(Role.permissions))
            .where(
                or_(
                    func.lower(User.email) == normalized,
                    func.lower(User.username) == normalized,
                )
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_paginated(
        self,
        institute_id: uuid.UUID | None,
        search: str | None,
        page: int,
        page_size: int,
    ) -> Tuple[List[User], int]:
        stmt = select(User).options(selectinload(User.roles))
        count_stmt = select(func.count(User.id))

        if institute_id:
            stmt = stmt.where(User.institute_id == institute_id)
            count_stmt = count_stmt.where(User.institute_id == institute_id)

        if search:
            pattern = f"%{search.strip()}%"
            filter_expr = or_(
                User.email.ilike(pattern),
                User.username.ilike(pattern),
                User.first_name.ilike(pattern),
                User.last_name.ilike(pattern),
            )
            stmt = stmt.where(filter_expr)
            count_stmt = count_stmt.where(filter_expr)

        total_res = await self.session.execute(count_stmt)
        total = int(total_res.scalar_one() or 0)

        stmt = stmt.order_by(User.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
        rows = await self.session.execute(stmt)
        return list(rows.scalars().all()), total

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        return user

    async def save_refresh_session(self, token_session: RefreshTokenSession) -> RefreshTokenSession:
        self.session.add(token_session)
        await self.session.flush()
        return token_session

    async def get_refresh_session_by_hash(self, token_hash: str) -> RefreshTokenSession | None:
        stmt = select(RefreshTokenSession).where(RefreshTokenSession.token_hash == token_hash)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def revoke_token_family(self, token_family: str, reason: str) -> None:
        stmt = select(RefreshTokenSession).where(
            RefreshTokenSession.token_family == token_family,
            RefreshTokenSession.is_revoked.is_(False),
        )
        res = await self.session.execute(stmt)
        for session_row in res.scalars().all():
            session_row.is_revoked = True
            session_row.revoked_reason = reason
        await self.session.flush()
