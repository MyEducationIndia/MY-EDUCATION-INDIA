"""
Module 14: Library Schemas (Pydantic v2 / v1 compatible)
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field

class LibraryCategoryBase(BaseModel):
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=150)
    description: Optional[str] = None
    parent_category_id: Optional[str] = None
    is_active: bool = True

class LibraryCategoryCreate(LibraryCategoryBase):
    pass

class LibraryCategoryResponse(LibraryCategoryBase):
    id: str
    institute_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class LibraryBookBase(BaseModel):
    isbn: str = Field(..., max_length=30)
    title: str = Field(..., max_length=255)
    subtitle: Optional[str] = None
    category_id: str
    author_name: str = Field(..., max_length=200)
    publisher_name: Optional[str] = None
    edition: Optional[str] = None
    publication_year: Optional[int] = None
    language: str = "English"
    total_pages: Optional[int] = None
    classification_ddc: Optional[str] = None
    location_id: Optional[str] = None
    cover_image_url: Optional[str] = None
    description: Optional[str] = None
    is_reference_only: bool = False

class LibraryBookCreate(LibraryBookBase):
    initial_copies_count: int = Field(1, ge=1)
    purchase_price_per_copy: float = Field(0.0, ge=0.0)

class LibraryBookResponse(LibraryBookBase):
    id: str
    institute_id: str
    total_copies_count: int
    available_copies_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class LibraryBookCopyResponse(BaseModel):
    id: str
    book_id: str
    institute_id: str
    accession_number: str
    barcode: str
    rfid_tag: Optional[str] = None
    status: str
    condition: str
    purchase_price: float
    created_at: datetime

    class Config:
        orm_mode = True

class LibraryMemberBase(BaseModel):
    user_id: str
    membership_card_number: str
    member_type: str
    max_borrow_limit: int = 3
    issue_period_days: int = 14
    expiry_date: Optional[date] = None

class LibraryMemberCreate(LibraryMemberBase):
    pass

class LibraryMemberResponse(LibraryMemberBase):
    id: str
    institute_id: str
    is_active: bool
    current_issued_count: int
    total_fines_due: float
    created_at: datetime

    class Config:
        orm_mode = True

class BookIssueRequest(BaseModel):
    book_copy_id: str
    member_id: str
    issue_period_days: Optional[int] = None
    remarks: Optional[str] = None

class BookReturnRequest(BaseModel):
    issue_transaction_id: str
    book_condition: str = "GOOD"
    fine_collected_amount: float = 0.0
    remarks: Optional[str] = None

class BookRenewalRequest(BaseModel):
    issue_transaction_id: str
    additional_days: int = 14

class LibraryFineWaiverRequest(BaseModel):
    fine_id: str
    waiver_amount: float
    waiver_reason: str

class DigitalResourceCreate(BaseModel):
    title: str = Field(..., max_length=255)
    category_id: str
    resource_type: str
    author_or_creator: str
    publication_year: Optional[int] = None
    file_format: str
    file_size_bytes: int = 0
    file_url: str
    thumbnail_url: Optional[str] = None
    download_allowed: bool = True
    description: Optional[str] = None

class LibraryDashboardMetrics(BaseModel):
    total_titles: int
    total_physical_copies: int
    available_copies: int
    active_issued_copies: int
    total_members: int
    overdue_issues_count: int
    total_fines_collected: float
    digital_resources_count: int
