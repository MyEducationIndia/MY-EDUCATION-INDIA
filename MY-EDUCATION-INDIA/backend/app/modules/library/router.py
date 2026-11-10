"""
Module 14: Library FastAPI Router
Endpoints mounted under /api/v1/library/
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from app.modules.library.schemas import (
    LibraryCategoryCreate, LibraryCategoryResponse,
    LibraryBookCreate, LibraryBookResponse,
    LibraryDashboardMetrics, BookIssueRequest, BookReturnRequest
)

library_router = APIRouter(prefix="/library", tags=["Enterprise Library & Digital Knowledge"])

@library_router.get("/health")
async def library_health():
    return {"status": "healthy", "module": "Module 14 - Enterprise Library & Digital Knowledge"}

@library_router.get("/dashboard/metrics")
async def get_library_metrics(institute_id: str = "inst_default"):
    return {
        "total_titles": 4250,
        "total_physical_copies": 18500,
        "available_copies": 16200,
        "active_issued_copies": 2300,
        "total_members": 3400,
        "overdue_issues_count": 85,
        "total_fines_collected": 14250.0,
        "digital_resources_count": 1280
    }

@library_router.get("/categories")
async def list_categories():
    return [
        {"id": "cat_1", "code": "CS", "name": "Computer Science & Engineering", "is_active": True},
        {"id": "cat_2", "code": "EE", "name": "Electrical & Electronics", "is_active": True},
        {"id": "cat_3", "code": "MGMT", "name": "Business & Management", "is_active": True}
    ]

@library_router.get("/books")
async def list_books(search: Optional[str] = None):
    return [
        {
            "id": "bk_1",
            "isbn": "978-0131103627",
            "title": "The C Programming Language",
            "author_name": "Brian W. Kernighan, Dennis M. Ritchie",
            "publisher_name": "Prentice Hall",
            "edition": "2nd",
            "publication_year": 1988,
            "language": "English",
            "category_id": "cat_1",
            "total_copies_count": 25,
            "available_copies_count": 18,
            "is_reference_only": False
        },
        {
            "id": "bk_2",
            "isbn": "978-0262033848",
            "title": "Introduction to Algorithms",
            "author_name": "Thomas H. Cormen, Charles E. Leiserson",
            "publisher_name": "MIT Press",
            "edition": "3rd",
            "publication_year": 2009,
            "language": "English",
            "category_id": "cat_1",
            "total_copies_count": 30,
            "available_copies_count": 22,
            "is_reference_only": False
        }
    ]

@library_router.get("/opac/search")
async def public_opac_search(query: str = Query(...)):
    return {
        "query": query,
        "total_results": 2,
        "items": [
            {
                "id": "bk_1",
                "title": "The C Programming Language",
                "author": "Brian W. Kernighan",
                "isbn": "9780131103627",
                "available_copies": 18,
                "status": "AVAILABLE",
                "shelf_location": "Rack 4, Shelf B"
            }
        ]
    }
