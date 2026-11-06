import uuid
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.permission import Permission
from app.models.role import Role


class RoleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, role_id: uuid.UUID) -> Role | None:
        stmt = select(Role).options(selectinload(Role.permissions)).where(Role.id == role_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_code(self, code: str, institute_id: uuid.UUID | None) -> Role | None:
        stmt = (
            select(Role)
            .options(selectinload(Role.permissions))
            .where(Role.code == code.upper(), Role.institute_id == institute_id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_roles(self, institute_id: uuid.UUID | None = None) -> List[Role]:
        stmt = select(Role).options(selectinload(Role.permissions))
        if institute_id:
            stmt = stmt.where((Role.institute_id == institute_id) | (Role.is_system_role.is_(True)))
        stmt = stmt.order_by(Role.name.asc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_Roles_by_ids(self, role_ids: List[uuid.UUID]) -> List[Role]:
        if not role_ids:
            return []
        stmt = select(Role).options(selectinload(Role.permissions)).where(Role.id.in_(role_ids))
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def list_permissions(self, module_key: str | None = None) -> List[Permission]:
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

    async def create(self, role: Role) -> Role:
        self.session.add(role)
        await self.session.flush()
        return role
