"""
API Integration Async Repository
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.modules.integrations.models import (
    ApiProvider, ApiCredential, ApiEndpoint, ApiExecutionLog,
    WebhookRegistration, WebhookDeliveryLog
)

class ApiIntegrationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_provider(self, institute_id: str, data: dict) -> ApiProvider:
        pid = str(uuid.uuid4())
        prov = ApiProvider(id=pid, institute_id=institute_id, **data)
        self.session.add(prov)
        await self.session.commit()
        await self.session.refresh(prov)
        return prov

    async def list_providers(self, institute_id: str, category: Optional[str] = None) -> List[ApiProvider]:
        stmt = select(ApiProvider).where(ApiProvider.institute_id == institute_id)
        if category:
            stmt = stmt.where(ApiProvider.category == category)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_provider_by_id(self, provider_id: str) -> Optional[ApiProvider]:
        res = await self.session.execute(
            select(ApiProvider).where(ApiProvider.id == provider_id)
        )
        return res.scalar_one_or_none()

    async def save_credentials(self, provider_id: str, institute_id: str, encrypted_payload: str) -> ApiCredential:
        res = await self.session.execute(
            select(ApiCredential).where(ApiCredential.provider_id == provider_id)
        )
        cred = res.scalar_one_or_none()
        if cred:
            cred.encrypted_payload = encrypted_payload
            cred.last_rotated_at = datetime.utcnow()
            cred.key_version += 1
        else:
            cred = ApiCredential(
                id=str(uuid.uuid4()),
                provider_id=provider_id,
                institute_id=institute_id,
                encrypted_payload=encrypted_payload,
                key_version=1
            )
            self.session.add(cred)
        await self.session.commit()
        await self.session.refresh(cred)
        return cred

    async def log_execution(self, institute_id: str, provider_id: str, endpoint_key: str, category: str, status_code: int, latency_ms: float, is_success: bool, error: str = None) -> ApiExecutionLog:
        log = ApiExecutionLog(
            id=str(uuid.uuid4()),
            institute_id=institute_id,
            provider_id=provider_id,
            endpoint_key=endpoint_key,
            category=category,
            status_code=status_code,
            latency_ms=latency_ms,
            is_success=is_success,
            error_message=error
        )
        self.session.add(log)
        await self.session.commit()
        return log
