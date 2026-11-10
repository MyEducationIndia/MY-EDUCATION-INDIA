"""
Module 14: Library Service Layer
"""
from app.modules.library.repository import LibraryRepository
from app.modules.library.validators import LibraryBusinessValidators
from app.modules.library.fine_engine import LibraryFineEngine
from app.modules.library.issue_engine import CirculationEngine
from datetime import datetime

class LibraryManagementService:
    def __init__(self, repo: LibraryRepository):
        self.repo = repo

    async def add_book(self, institute_id: str, data: dict, copies: int, price: float):
        if not LibraryBusinessValidators.validate_isbn(data.get("isbn", "")):
            # Warning or soft validation
            pass
        return await self.repo.create_book_with_copies(institute_id, data, copies, price)

    async def list_catalog(self, institute_id: str, query: str = None):
        return await self.repo.list_books(institute_id, query)

    def calculate_fine(self, due_date: datetime, return_date: datetime) -> dict:
        return LibraryFineEngine.calculate_overdue_fine(due_date, return_date)
