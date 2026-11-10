"""
Module 19: Platform SQLAlchemy 2.x Async Repository
"""
from typing import List, Optional
from datetime import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from app.modules.platform.models import (
    PlatformSetting, SecurityPolicy, BackupJob, BackupHistory,
    RestoreHistory, AuditEvent, SystemLog, ApiKey, FeatureFlag,
    StorageConfig, LicenseSetting, MaintenanceWindow
)

class PlatformRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_security_policy(self, institute_id: str) -> Optional[SecurityPolicy]:
        res = await self.session.execute(
            select(SecurityPolicy).where(SecurityPolicy.institute_id == institute_id)
        )
        return res.scalar_one_or_none()

    async def list_backup_jobs(self, institute_id: str) -> List[BackupJob]:
        res = await self.session.execute(
            select(BackupJob).where(BackupJob.institute_id == institute_id)
        )
        return list(res.scalars().all())

    async def create_backup_record(self, institute_id: str, data: dict) -> BackupHistory:
        bid = str(uuid.uuid4())
        rec = BackupHistory(id=bid, institute_id=institute_id, **data)
        self.session.add(rec)
        await self.session.commit()
        await self.session.refresh(rec)
        return rec

    async def list_feature_flags(self, institute_id: str) -> List[FeatureFlag]:
        res = await self.session.execute(
            select(FeatureFlag).where(FeatureFlag.institute_id == institute_id)
        )
        return list(res.scalars().all())
