"""
CBTMockTestService module
"""
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession


class CBTMockTestService:
    def __init__(self, db: AsyncSession | None = None) -> None:
        self.db = db

    async def list_mock_series(self, *args: Any, **kwargs: Any) -> Any:
        return []

    async def register_public_aspirant(self, *args: Any, **kwargs: Any) -> Any:
        return {}

    async def get_public_leaderboard(self, *args: Any, **kwargs: Any) -> Any:
        return {}

    async def list_subject_chapter_practice(self, *args: Any, **kwargs: Any) -> Any:
        return []

    async def get_candidate_mock_history(self, *args: Any, **kwargs: Any) -> Any:
        return []
