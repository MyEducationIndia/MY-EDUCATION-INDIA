"""
CBTCertificateService module
"""
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession


class CBTCertificateService:
    def __init__(self, db: AsyncSession | None = None) -> None:
        self.db = db

    async def issue_candidate_certificate(self, *args: Any, **kwargs: Any) -> Any:
        return {}

    async def batch_issue_session_certificates(self, *args: Any, **kwargs: Any) -> Any:
        return []

    async def list_session_certificates(self, *args: Any, **kwargs: Any) -> Any:
        return []

    async def dispatch_certificate_email(self, *args: Any, **kwargs: Any) -> Any:
        return {}

    async def public_verify_certificate(self, *args: Any, **kwargs: Any) -> Any:
        return {}
