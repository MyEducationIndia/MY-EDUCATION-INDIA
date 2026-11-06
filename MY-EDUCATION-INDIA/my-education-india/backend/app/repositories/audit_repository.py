import uuid
from typing import List, Tuple
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog


class AuditLogRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, entry: AuditLog) -> AuditLog:
        self.session.add(entry)
        await self.session.flush()
        return entry

    async def list_paginated(
        self,
        institute_id: uuid.UUID | None,
        module_key: str | None,
        action: str | None,
        page: int,
        page_size: int,
    ) -> Tuple[List[AuditLog], int]:
        stmt = select(AuditLog)
        count_stmt = select(func.count(AuditLog.id))

        if institute_id:
            stmt = stmt.where(AuditLog.institute_id == institute_id)
            count_stmt = count_stmt.where(AuditLog.institute_id == institute_id)
        if module_key:
            stmt = stmt.where(AuditLog.module_key == module_key)
            count_stmt = count_stmt.where(AuditLog.module_key == module_key)
        if action:
            stmt = stmt.where(AuditLog.action.ilike(f"%{action.strip()}%"))
            count_stmt = count_stmt.where(AuditLog.action.ilike(f"%{action.strip()}%"))

        total_res = await self.session.execute(count_stmt)
        total = int(total_res.scalar_one() or 0)

        stmt = (
            stmt.order_by(AuditLog.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all()), total
