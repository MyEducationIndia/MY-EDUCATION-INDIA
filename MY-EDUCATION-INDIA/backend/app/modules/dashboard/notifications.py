from datetime import datetime, timezone
from typing import List, Optional, Tuple
import uuid
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.dashboard.models import Notification
from app.modules.dashboard.schemas import NotificationCreateRequest


class NotificationService:
    """Enterprise notification dispatch and state management service."""

    @staticmethod
    async def create_notification(
        session: AsyncSession,
        payload: NotificationCreateRequest,
    ) -> Notification:
        notif = Notification(
            user_id=payload.user_id,
            institute_id=payload.institute_id,
            title=payload.title,
            message=payload.message,
            category=payload.category,
            priority=payload.priority,
            action_url=payload.action_url,
            is_read=False,
            meta_data=payload.meta_data,
        )
        session.add(notif)
        await session.commit()
        await session.refresh(notif)
        return notif

    @staticmethod
    async def get_user_notifications(
        session: AsyncSession,
        user_id: Optional[uuid.UUID],
        institute_id: Optional[uuid.UUID],
        unread_only: bool = False,
        limit: int = 20,
    ) -> List[Notification]:
        stmt = select(Notification).where(Notification.is_archived.is_(False))
        if user_id:
            stmt = stmt.where((Notification.user_id == user_id) | (Notification.user_id.is_(None)))
        if institute_id:
            stmt = stmt.where((Notification.institute_id == institute_id) | (Notification.institute_id.is_(None)))
        if unread_only:
            stmt = stmt.where(Notification.is_read.is_(False))

        stmt = stmt.order_by(Notification.created_at.desc()).limit(limit)
        res = await session.execute(stmt)
        return list(res.scalars().all())

    @staticmethod
    async def mark_as_read(
        session: AsyncSession,
        notification_id: uuid.UUID,
    ) -> Optional[Notification]:
        stmt = select(Notification).where(Notification.id == notification_id)
        res = await session.execute(stmt)
        notif = res.scalar_one_or_none()
        if notif:
            notif.is_read = True
            notif.read_at = datetime.now(timezone.utc)
            await session.commit()
            await session.refresh(notif)
        return notif

    @staticmethod
    async def mark_all_as_read(
        session: AsyncSession,
        user_id: Optional[uuid.UUID],
        institute_id: Optional[uuid.UUID],
    ) -> int:
        now = datetime.now(timezone.utc)
        stmt = select(Notification).where(Notification.is_read.is_(False))
        if user_id:
            stmt = stmt.where(Notification.user_id == user_id)
        res = await session.execute(stmt)
        items = list(res.scalars().all())
        for n in items:
            n.is_read = True
            n.read_at = now
        await session.commit()
        return len(items)
