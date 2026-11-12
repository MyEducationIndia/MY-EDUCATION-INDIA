"""
ExamStudentPortalService module
"""
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession


class ExamStudentPortalService:
    def __init__(self, db: AsyncSession | None = None) -> None:
        self.db = db

    @staticmethod
    async def get_student_portal_dashboard(*args: Any, **kwargs: Any) -> Any:
        return {}

    @staticmethod
    async def get_student_seating_lookup(*args: Any, **kwargs: Any) -> Any:
        return {}

    @staticmethod
    async def register_student_exam(*args: Any, **kwargs: Any) -> Any:
        return {}
