import uuid
from typing import List, Optional, Tuple
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.refresh_token import RefreshTokenSession
from app.models.role import Role
from app.models.user import User
from app.models.user_document import UserDocument


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        stmt = (
            select(User)
            .options(
                selectinload(User.roles).selectinload(Role.permissions),
                selectinload(User.documents),
            )
            .where(User.id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_identifier(self, identifier: str) -> User | None:
        normalized = identifier.strip().lower()
        stmt = (
            select(User)
            .options(
                selectinload(User.roles).selectinload(Role.permissions),
                selectinload(User.documents),
            )
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
        user_category: str | None,
        is_archived: bool | None,
        department: str | None,
        verification_status: str | None,
        page: int,
        page_size: int,
    ) -> Tuple[List[User], int]:
        stmt = select(User).options(
            selectinload(User.roles),
            selectinload(User.documents),
        )
        count_stmt = select(func.count(User.id))

        if institute_id:
            stmt = stmt.where(User.institute_id == institute_id)
            count_stmt = count_stmt.where(User.institute_id == institute_id)

        if is_archived is not None:
            stmt = stmt.where(User.is_archived == is_archived)
            count_stmt = count_stmt.where(User.is_archived == is_archived)
        else:
            # Default to active unarchived users unless explicitly requested
            stmt = stmt.where(User.is_archived.is_(False))
            count_stmt = count_stmt.where(User.is_archived.is_(False))

        if user_category and user_category.upper() != "ALL":
            stmt = stmt.where(User.user_category == user_category.upper())
            count_stmt = count_stmt.where(User.user_category == user_category.upper())

        if department:
            stmt = stmt.where(User.department.ilike(f"%{department.strip()}%"))
            count_stmt = count_stmt.where(User.department.ilike(f"%{department.strip()}%"))

        if verification_status:
            stmt = stmt.where(User.identity_verification_status == verification_status.upper())
            count_stmt = count_stmt.where(User.identity_verification_status == verification_status.upper())

        if search:
            pattern = f"%{search.strip()}%"
            filter_expr = or_(
                User.email.ilike(pattern),
                User.username.ilike(pattern),
                User.first_name.ilike(pattern),
                User.last_name.ilike(pattern),
                User.admission_or_emp_id.ilike(pattern),
                User.phone_number.ilike(pattern),
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

    async def get_document_by_id(self, document_id: uuid.UUID) -> UserDocument | None:
        stmt = select(UserDocument).where(UserDocument.id == document_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_documents_for_user(self, user_id: uuid.UUID) -> List[UserDocument]:
        stmt = (
            select(UserDocument)
            .where(UserDocument.user_id == user_id)
            .order_by(UserDocument.created_at.desc())
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def add_document(self, document: UserDocument) -> UserDocument:
        self.session.add(document)
        await self.session.flush()
        return document

    async def delete_document(self, document: UserDocument) -> None:
        await self.session.delete(document)
        await self.session.flush()

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
