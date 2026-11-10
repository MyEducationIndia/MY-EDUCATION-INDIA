"""
Module 14: Enterprise Library & Digital Knowledge Management System - SQLAlchemy Models
Provides 18 enterprise tables for physical & digital library operations.
"""
from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Date, ForeignKey, Text, JSON, Enum, Index
)
from sqlalchemy.orm import relationship
from app.db.base import Base

class LibraryCategory(Base):
    __tablename__ = "library_categories"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    code = Column(String(50), nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    parent_category_id = Column(String(36), ForeignKey("library_categories.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    books = relationship("LibraryBook", back_populates="category", cascade="all, delete-orphan")

class LibraryAuthor(Base):
    __tablename__ = "library_authors"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    biography = Column(Text, nullable=True)
    email = Column(String(150), nullable=True)
    nationality = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class LibraryPublisher(Base):
    __tablename__ = "library_publishers"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    address = Column(Text, nullable=True)
    contact_person = Column(String(150), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(150), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class LibraryLocation(Base):
    __tablename__ = "library_locations"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    building = Column(String(100), nullable=False)
    floor = Column(String(50), nullable=False)
    room_number = Column(String(50), nullable=False)
    aisle = Column(String(50), nullable=True)
    rack_number = Column(String(50), nullable=False)
    shelf_number = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class LibraryBook(Base):
    __tablename__ = "library_books"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    isbn = Column(String(30), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    subtitle = Column(String(255), nullable=True)
    category_id = Column(String(36), ForeignKey("library_categories.id"), nullable=False)
    author_name = Column(String(200), nullable=False, index=True)
    publisher_name = Column(String(200), nullable=True)
    edition = Column(String(50), nullable=True)
    publication_year = Column(Integer, nullable=True)
    language = Column(String(50), default="English", nullable=False)
    total_pages = Column(Integer, nullable=True)
    classification_ddc = Column(String(50), nullable=True)
    location_id = Column(String(36), ForeignKey("library_locations.id"), nullable=True)
    cover_image_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    is_reference_only = Column(Boolean, default=False, nullable=False)
    total_copies_count = Column(Integer, default=1, nullable=False)
    available_copies_count = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    category = relationship("LibraryCategory", back_populates="books")
    copies = relationship("LibraryBookCopy", back_populates="book", cascade="all, delete-orphan")

class LibraryBookCopy(Base):
    __tablename__ = "library_book_copies"
    id = Column(String(36), primary_key=True)
    book_id = Column(String(36), ForeignKey("library_books.id"), nullable=False)
    institute_id = Column(String(36), nullable=False, index=True)
    accession_number = Column(String(60), unique=True, nullable=False, index=True)
    barcode = Column(String(100), unique=True, nullable=False, index=True)
    rfid_tag = Column(String(100), unique=True, nullable=True, index=True)
    status = Column(String(30), default="AVAILABLE", nullable=False) # AVAILABLE, ISSUED, RESERVED, LOST, DAMAGED, WEEDED
    condition = Column(String(50), default="GOOD", nullable=False) # NEW, GOOD, FAIR, WORN, DAMAGED
    purchase_price = Column(Float, default=0.0, nullable=False)
    purchase_date = Column(Date, nullable=True)
    source_vendor = Column(String(150), nullable=True)
    call_number = Column(String(80), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    book = relationship("LibraryBook", back_populates="copies")

class LibraryMember(Base):
    __tablename__ = "library_members"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    user_id = Column(String(36), nullable=False, index=True)
    membership_card_number = Column(String(60), unique=True, nullable=False, index=True)
    member_type = Column(String(30), nullable=False) # STUDENT, FACULTY, STAFF, RESEARCHER, ALUMNI
    max_borrow_limit = Column(Integer, default=3, nullable=False)
    issue_period_days = Column(Integer, default=14, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    current_issued_count = Column(Integer, default=0, nullable=False)
    total_fines_due = Column(Float, default=0.0, nullable=False)
    expiry_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class LibraryIssueTransaction(Base):
    __tablename__ = "library_issue_transactions"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    transaction_number = Column(String(60), unique=True, nullable=False, index=True)
    book_copy_id = Column(String(36), ForeignKey("library_book_copies.id"), nullable=False)
    member_id = Column(String(36), ForeignKey("library_members.id"), nullable=False)
    issued_by_user_id = Column(String(36), nullable=False)
    issue_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    due_date = Column(DateTime, nullable=False, index=True)
    renewal_count = Column(Integer, default=0, nullable=False)
    max_allowed_renewals = Column(Integer, default=2, nullable=False)
    status = Column(String(30), default="ACTIVE", nullable=False) # ACTIVE, RETURNED, OVERDUE, LOST
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class LibraryReturnTransaction(Base):
    __tablename__ = "library_return_transactions"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    issue_transaction_id = Column(String(36), ForeignKey("library_issue_transactions.id"), nullable=False)
    return_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    received_by_user_id = Column(String(36), nullable=False)
    book_condition_on_return = Column(String(50), default="GOOD", nullable=False)
    overdue_days = Column(Integer, default=0, nullable=False)
    calculated_fine_amount = Column(Float, default=0.0, nullable=False)
    fine_collected_amount = Column(Float, default=0.0, nullable=False)
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class LibraryReservation(Base):
    __tablename__ = "library_reservations"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    book_id = Column(String(36), ForeignKey("library_books.id"), nullable=False)
    member_id = Column(String(36), ForeignKey("library_members.id"), nullable=False)
    reservation_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    priority_order = Column(Integer, default=1, nullable=False)
    status = Column(String(30), default="PENDING", nullable=False) # PENDING, FULFILLED, EXPIRED, CANCELLED
    expiry_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class LibraryFine(Base):
    __tablename__ = "library_fines"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    member_id = Column(String(36), ForeignKey("library_members.id"), nullable=False)
    issue_transaction_id = Column(String(36), ForeignKey("library_issue_transactions.id"), nullable=True)
    amount = Column(Float, nullable=False)
    amount_paid = Column(Float, default=0.0, nullable=False)
    balance_amount = Column(Float, nullable=False)
    fine_reason = Column(String(100), default="OVERDUE_FINE", nullable=False) # OVERDUE_FINE, BOOK_DAMAGE, BOOK_LOSS
    status = Column(String(30), default="UNPAID", nullable=False) # UNPAID, PARTIAL, PAID, WAIVED
    waived_by_user_id = Column(String(36), nullable=True)
    waiver_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class LibraryDigitalResource(Base):
    __tablename__ = "library_digital_resources"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    category_id = Column(String(36), ForeignKey("library_categories.id"), nullable=False)
    resource_type = Column(String(50), nullable=False) # EBOOK, JOURNAL, RESEARCH_PAPER, THESIS, VIDEO, AUDIO
    author_or_creator = Column(String(200), nullable=False)
    publication_year = Column(Integer, nullable=True)
    file_format = Column(String(20), nullable=False) # PDF, EPUB, MP4, MP3
    file_size_bytes = Column(Integer, default=0, nullable=False)
    file_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500), nullable=True)
    download_allowed = Column(Boolean, default=True, nullable=False)
    view_count = Column(Integer, default=0, nullable=False)
    download_count = Column(Integer, default=0, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class LibraryQuestionPaper(Base):
    __tablename__ = "library_question_papers"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    program_id = Column(String(36), nullable=True)
    course_id = Column(String(36), nullable=True)
    semester = Column(String(30), nullable=False)
    academic_year = Column(String(30), nullable=False)
    exam_type = Column(String(50), nullable=False) # MID_TERM, END_TERM, ARREAR
    file_url = Column(String(500), nullable=False)
    download_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class LibraryNote(Base):
    __tablename__ = "library_notes"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    subject_title = Column(String(200), nullable=False)
    topic_name = Column(String(200), nullable=False)
    faculty_user_id = Column(String(36), nullable=True)
    file_url = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class LibraryReadingHistory(Base):
    __tablename__ = "library_reading_histories"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    member_id = Column(String(36), ForeignKey("library_members.id"), nullable=False)
    book_id = Column(String(36), ForeignKey("library_books.id"), nullable=False)
    access_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    resource_type = Column(String(30), default="PHYSICAL", nullable=False) # PHYSICAL, DIGITAL

class LibraryNotification(Base):
    __tablename__ = "library_notifications"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    member_id = Column(String(36), ForeignKey("library_members.id"), nullable=False)
    notification_type = Column(String(50), nullable=False) # DUE_REMINDER, OVERDUE_ALERT, RESERVATION_AVAILABLE
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class LibraryReport(Base):
    __tablename__ = "library_reports"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    report_name = Column(String(150), nullable=False)
    report_type = Column(String(50), nullable=False)
    parameters = Column(JSON, nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class LibraryAnalytics(Base):
    __tablename__ = "library_analytics"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    date_key = Column(Date, nullable=False, index=True)
    total_circulations = Column(Integer, default=0, nullable=False)
    total_returns = Column(Integer, default=0, nullable=False)
    total_fines_accrued = Column(Float, default=0.0, nullable=False)
    digital_downloads = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
