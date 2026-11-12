"""
ExamSeatingService module
"""
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession


class ExamSeatingService:
    def __init__(self, db: AsyncSession | None = None) -> None:
        self.db = db

    async def list_buildings(self, *args: Any, **kwargs: Any) -> Any:
        return []

    async def create_building(self, *args: Any, **kwargs: Any) -> Any:
        return {}

    async def list_rooms(self, *args: Any, **kwargs: Any) -> Any:
        return []

    async def create_room_layout(self, *args: Any, **kwargs: Any) -> Any:
        return {}

    async def generate_seating_plan(self, *args: Any, **kwargs: Any) -> Any:
        return {}

    async def list_seating_plans(self, *args: Any, **kwargs: Any) -> Any:
        return []

    async def get_seating_plan(self, *args: Any, **kwargs: Any) -> Any:
        return {}

    async def generate_door_notice(self, *args: Any, **kwargs: Any) -> Any:
        return {}
