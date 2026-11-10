"""
Module 14: Library SQLAlchemy 2.x Async Repository
"""
from typing import List, Optional
from datetime import datetime, date
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from app.modules.library.models import (
    LibraryCategory, LibraryBook, LibraryBookCopy, LibraryMember,
    LibraryIssueTransaction, LibraryReturnTransaction, LibraryFine,
    LibraryReservation, LibraryDigitalResource
)

class LibraryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_category(self, institute_id: str, data: dict) -> LibraryCategory:
        cat = LibraryCategory(id=str(uuid.uuid4()), institute_id=institute_id, **data)
        self.session.add(cat)
        await self.session.commit()
        await self.session.refresh(cat)
        return cat

    async def list_categories(self, institute_id: str) -> List[LibraryCategory]:
        res = await self.session.execute(
            select(LibraryCategory).where(LibraryCategory.institute_id == institute_id)
        )
        return list(res.scalars().all())

    async def create_book_with_copies(self, institute_id: str, book_data: dict, copies_count: int, price: float) -> LibraryBook:
        book_id = str(uuid.uuid4())
        book = LibraryBook(
            id=book_id,
            institute_id=institute_id,
            total_copies_count=copies_count,
            available_copies_count=copies_count,
            **book_data
        )
        self.session.add(book)
        for i in range(1, copies_count + 1):
            copy_id = str(uuid.uuid4())
            acc_num = f"ACC-{book_id[:6].upper()}-{i:03d}"
            copy = LibraryBookCopy(
                id=copy_id,
                book_id=book_id,
                institute_id=institute_id,
                accession_number=acc_num,
                barcode=acc_num,
                purchase_price=price,
                status="AVAILABLE"
            )
            self.session.add(copy)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def list_books(self, institute_id: str, search: Optional[str] = None) -> List[LibraryBook]:
        stmt = select(LibraryBook).where(LibraryBook.institute_id == institute_id)
        if search:
            stmt = stmt.where(LibraryBook.title.ilike(f"%{search}%") | LibraryBook.author_name.ilike(f"%{search}%"))
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_dashboard_metrics(self, institute_id: str) -> dict:
        total_books_res = await self.session.execute(
            select(func.count(LibraryBook.id)).where(LibraryBook.institute_id == institute_id)
        )
        copies_res = await self.session.execute(
            select(
                func.count(LibraryBookCopy.id),
                func.sum(case((LibraryBookCopy.status == "AVAILABLE", 1), else_=0)),
                func.sum(case((LibraryBookCopy.status == "ISSUED", 1), else_=0))
            ).where(LibraryBookCopy.institute_id == institute_id)
        )
        return {
            "total_titles": total_books_res.scalar() or 0,
            "total_physical_copies": 0,
            "available_copies": 0,
            "active_issued_copies": 0,
            "total_members": 0,
            "overdue_issues_count": 0,
            "total_fines_collected": 0.0,
            "digital_resources_count": 0
        }
