"""
ExamMarksEntryService module
"""
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession


class ExamMarksEntryService:
    def __init__(self, db: AsyncSession | None = None) -> None:
        self.db = db

    async def list_submissions(self, *args: Any, **kwargs: Any) -> Any:
        return []

    async def create_submission(self, *args: Any, **kwargs: Any) -> Any:
        return {}

    async def get_submission(self, *args: Any, **kwargs: Any) -> Any:
        return {}

    async def list_entries(self, *args: Any, **kwargs: Any) -> Any:
        return []

    async def save_batch_marks(self, *args: Any, **kwargs: Any) -> Any:
        return {}

    async def import_excel_marks(self, *args: Any, **kwargs: Any) -> Any:
        return {}

    async def approve_workflow(self, *args: Any, **kwargs: Any) -> Any:
        return {}
