from datetime import datetime
from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


# 1. Institutes / Campus Settings
class Institute(Base):
    __tablename__ = "institutes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    slogan = Column(String(255), nullable=True)
    registration_no = Column(String(100), unique=True, nullable=True)
    iso_certification = Column(String(100), nullable=True)
    email = Column(String(150), nullable=False)
    phone = Column(String(50), nullable=False)
    address = Column(Text, nullable=False)
    whatsapp = Column(String(50), nullable=True)
    currency = Column(String(20), nullable=False, default="INR (₹)")
    timezone = Column(String(50), nullable=False, default="Asia/Kolkata")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


# 2. System Roles
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)

    users = relationship("User", back_populates="role", cascade="all, delete-orphan")


# 3. Master User Registry (Authentication & Credentials)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True, index=True)
    email = Column(String(150), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(150), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False, index=True)
    linked_id = Column(String(100), nullable=True, index=True)
    is_active = Column(Integer, nullable=False, default=1)
    failed_attempts = Column(Integer, nullable=False, default=0)
    locked_until = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    role = relationship("Role", back_populates="users")


# 4. Course Catalog
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False, index=True)
    duration = Column(String(50), nullable=False)
    fee = Column(Float, nullable=False, default=0.0)
    eligibility = Column(String(255), nullable=False)
    highlights = Column(Text, nullable=True)
    syllabus_modules = Column(Text, nullable=True)
    badge = Column(String(50), nullable=False, default="Standard")
    is_popular = Column(Integer, nullable=False, default=0)
    is_active = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    batches = relationship("Batch", back_populates="course", cascade="all, delete-orphan")
    students = relationship("Student", back_populates="course")


# 5. Faculty & Staff Members
class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_code = Column(String(50), nullable=False, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), unique=True, nullable=True)
    name = Column(String(150), nullable=False)
    designation = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False, index=True)
    qualification = Column(String(150), nullable=False)
    salary_amount = Column(Float, nullable=True, default=0.0)
    phone = Column(String(50), nullable=True)
    email = Column(String(150), nullable=False, index=True)
    joining_date = Column(Date, nullable=True)
    status = Column(String(50), nullable=False, default="Active")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    user = relationship("User")
    batches = relationship("Batch", back_populates="trainer")
    leaves = relationship("StaffLeave", back_populates="staff", cascade="all, delete-orphan")


# 6. Batches & Classroom Scheduling
class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(150), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    trainer_id = Column(Integer, ForeignKey("staff.id", ondelete="SET NULL"), nullable=True, index=True)
    timing = Column(String(100), nullable=False)
    room = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False, default=30)
    status = Column(String(50), nullable=False, default="Active")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    course = relationship("Course", back_populates="batches")
    trainer = relationship("Staff", back_populates="batches")
    students = relationship("Student", back_populates="batch")


# 7. Student Information & Roster
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    roll_number = Column(String(50), nullable=False, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), unique=True, nullable=True)
    name = Column(String(150), nullable=False, index=True)
    dob = Column(String(50), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="RESTRICT"), nullable=False, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id", ondelete="SET NULL"), nullable=True, index=True)
    mobile = Column(String(50), nullable=False)
    email = Column(String(150), nullable=False, index=True)
    guardian_name = Column(String(150), nullable=False)
    guardian_mobile = Column(String(50), nullable=True)
    gender = Column(String(20), nullable=False, default="Male")
    blood_group = Column(String(10), nullable=True, default="B+")
    address = Column(Text, nullable=True)
    total_fee = Column(Float, nullable=False, default=0.0)
    paid_fee = Column(Float, nullable=False, default=0.0)
    due_fee = Column(Float, nullable=False, default=0.0)
    attendance_rate = Column(Float, nullable=False, default=100.0)
    status = Column(String(50), nullable=False, default="Enrolled")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    user = relationship("User")
    course = relationship("Course", back_populates="students")
    batch = relationship("Batch", back_populates="students")
    fee_payments = relationship("FeePayment", back_populates="student", cascade="all, delete-orphan")
    attendances = relationship("Attendance", back_populates="student", cascade="all, delete-orphan")


# 8. Online Admissions Queue
class Admission(Base):
    __tablename__ = "admissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    application_number = Column(String(50), nullable=False, unique=True, index=True)
    applicant_name = Column(String(150), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="RESTRICT"), nullable=False, index=True)
    preferred_timing = Column(String(50), nullable=True)
    prior_qualification = Column(String(150), nullable=False)
    mobile = Column(String(50), nullable=False)
    email = Column(String(150), nullable=False)
    guardian_name = Column(String(150), nullable=True)
    status = Column(String(50), nullable=False, default="Pending Review", index=True)
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    course = relationship("Course")


# 9. Fee Payments & Official Tax Invoices
class FeePayment(Base):
    __tablename__ = "fee_payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_number = Column(String(50), nullable=False, unique=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    payment_mode = Column(String(50), nullable=False)
    payment_date = Column(Date, nullable=False, index=True)
    remarks = Column(Text, nullable=True)
    receipt_data = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    student = relationship("Student", back_populates="fee_payments")


# 10. Daily Attendance Register
class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    status = Column(String(20), nullable=False)
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    student = relationship("Student", back_populates="attendances")
    batch = relationship("Batch")

    __table_args__ = (
        UniqueConstraint("student_id", "batch_id", "date", name="uq_attendance_student_batch_date"),
    )


# 11. Study Materials & Lecture Notes
class StudyMaterial(Base):
    __tablename__ = "study_materials"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id", ondelete="SET NULL"), nullable=True, index=True)
    file_path = Column(Text, nullable=False)
    file_type = Column(String(20), nullable=False, default="PDF")
    file_size = Column(String(50), nullable=True)
    author = Column(String(100), nullable=False, default="Faculty Desk")
    uploaded_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    course = relationship("Course")
    batch = relationship("Batch")


# 12. Institutional Notices & Animated Circulars
class Notice(Base):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    target_audience = Column(String(50), nullable=False, default="All", index=True)
    category = Column(String(50), nullable=False, default="Urgent")
    is_pinned = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


# 13. Academic Homework & Assignments
class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id", ondelete="CASCADE"), nullable=False, index=True)
    trainer_id = Column(Integer, ForeignKey("staff.id", ondelete="CASCADE"), nullable=False, index=True)
    due_date = Column(Date, nullable=False)
    instructions = Column(Text, nullable=False)
    max_marks = Column(Integer, nullable=False, default=20)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    course = relationship("Course")
    batch = relationship("Batch")
    trainer = relationship("Staff")
    submissions = relationship("AssignmentSubmission", back_populates="assignment", cascade="all, delete-orphan")


# 14. Assignment Submissions
class AssignmentSubmission(Base):
    __tablename__ = "assignment_submissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    submission_text = Column(Text, nullable=True)
    file_path = Column(Text, nullable=True)
    submitted_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    grade = Column(String(20), nullable=True)
    marks_obtained = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="Submitted")

    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("Student")

    __table_args__ = (
        UniqueConstraint("assignment_id", "student_id", name="uq_assignment_student"),
    )


# 15. Staff Leave Management
class StaffLeave(Base):
    __tablename__ = "staff_leaves"

    id = Column(Integer, primary_key=True, autoincrement=True)
    staff_id = Column(Integer, ForeignKey("staff.id", ondelete="CASCADE"), nullable=False, index=True)
    leave_type = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="Pending", index=True)
    approved_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    staff = relationship("Staff", back_populates="leaves")


# 16. Public Inquiries & Callback Requests
class Enquiry(Base):
    __tablename__ = "enquiries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(150), nullable=True)
    course_interest = Column(String(100), nullable=True)
    message = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="New", index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


# 17. Newsletter Subscribers
class NewsletterSubscriber(Base):
    __tablename__ = "newsletter_subscribers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(150), nullable=False, unique=True, index=True)
    subscribed_at = Column(DateTime, nullable=False, default=datetime.utcnow)


# 18. Website Testimonials
class Testimonial(Base):
    __tablename__ = "testimonials"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    course = Column(String(150), nullable=False)
    quote = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False, default=5)
    is_featured = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


# 19. Website FAQs
class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String(50), nullable=False, default="General")
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


# 20. Photo Gallery & Campus Facilities
class GalleryItem(Base):
    __tablename__ = "gallery"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    category = Column(String(50), nullable=False)
    image_url = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


# 21. Blog Posts & Career Guidance (News)
class BlogPost(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    author = Column(String(150), nullable=False)
    category = Column(String(50), nullable=False)
    summary = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    read_time = Column(String(50), nullable=False, default="5 min read")
    published_at = Column(DateTime, nullable=False, default=datetime.utcnow)


# 22. Security Audit Trail & System Logs
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    actor = Column(String(100), nullable=False, index=True)
    action = Column(String(255), nullable=False)
    module = Column(String(100), nullable=False, index=True)
    ip_address = Column(String(50), nullable=True)
    status = Column(String(50), nullable=False, default="Success")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)


# 23. Master Website CMS Parameters (Key-Value)
class CMSContent(Base):
    __tablename__ = "cms_content"

    key = Column(String(150), primary_key=True)
    value = Column(Text, nullable=False)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


# 24. Shared Institutional State (Real-Time Cloud State Sync)
class SharedInstitutionalState(Base):
    __tablename__ = "shared_institutional_state"

    id = Column(Integer, primary_key=True, default=1)
    state_json = Column(Text, nullable=False)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


# 25. Database Restore Points
class RestorePoint(Base):
    __tablename__ = "restore_points"

    id = Column(String(50), primary_key=True)
    label = Column(String(255), nullable=False)
    state_json = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


# 26. Public Downloads & Institutional Documents
class PublicDocument(Base):
    __tablename__ = "public_documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    file_type = Column(String(50), nullable=False, default="PDF")
    file_size = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    download_url = Column(Text, nullable=True)
    is_active = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


# 27. Exam Portal Configuration
class ExamConfiguration(Base):
    __tablename__ = "exam_configurations"

    id = Column(Integer, primary_key=True, default=1)
    window_open = Column(Integer, nullable=False, default=1)
    require_no_dues = Column(Integer, nullable=False, default=1)
    session_title = Column(String(255), nullable=True)
    start_date = Column(String(50), nullable=True)
    last_form_date = Column(String(50), nullable=True)
    center_name = Column(String(255), nullable=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


# 28. Exam Registration Forms & Admit Cards
class ExamForm(Base):
    __tablename__ = "exam_forms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    form_no = Column(String(50), nullable=False, unique=True, index=True)
    admit_card_no = Column(String(50), unique=True, index=True, nullable=True)
    student_id = Column(String(50), nullable=False, index=True)
    student_name = Column(String(150), nullable=False)
    course = Column(String(100), nullable=False)
    batch = Column(String(100), nullable=True)
    exam_session = Column(String(255), nullable=True)
    category = Column(String(50), nullable=True)
    medium = Column(String(20), nullable=True)
    papers = Column(Text, nullable=True)
    no_dues_cert_no = Column(String(50), nullable=True)
    submitted_date = Column(String(50), nullable=True)
    status = Column(String(50), nullable=False, default="Pending", index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


# 29. Public Website Sections Arrangement & Visibility
class WebsiteSection(Base):
    __tablename__ = "website_sections"

    id = Column(String(100), primary_key=True)
    label = Column(String(255), nullable=False)
    icon = Column(String(50), nullable=True)
    visible = Column(Integer, nullable=False, default=1)
    display_order = Column(Integer, nullable=False, default=0, index=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


# 30. Custom Admin Website Sections
class CustomSection(Base):
    __tablename__ = "custom_sections"

    id = Column(String(100), primary_key=True)
    badge = Column(String(255), nullable=True)
    title = Column(String(255), nullable=False)
    subtitle = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    cta_text = Column(String(100), nullable=True)
    cta_action = Column(String(255), nullable=True)
    theme = Column(String(50), nullable=True)
    image_url = Column(Text, nullable=True)
    visible = Column(Integer, nullable=False, default=1)
    display_order = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


# 31. Question Bank for CBT & Semester Exams
class QuestionBank(Base):
    __tablename__ = "question_bank"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_code = Column(String(50), index=True, nullable=True)
    paper_code = Column(String(50), index=True, nullable=True)
    question_text = Column(Text, nullable=False)
    options = Column(Text, nullable=False)
    correct_option = Column(Integer, nullable=False)
    explanation = Column(Text, nullable=True)
    marks = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


# 32. CBT Examination Results
class CBTExamResult(Base):
    __tablename__ = "cbt_exam_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(50), index=True, nullable=False)
    roll_number = Column(String(50), index=True, nullable=False)
    exam_session = Column(String(255), nullable=True)
    score = Column(Float, nullable=False, default=0.0)
    max_score = Column(Float, nullable=False, default=100.0)
    percentage = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), nullable=False, default="Completed")
    answers_json = Column(Text, nullable=True)
    submitted_at = Column(DateTime, nullable=False, default=datetime.utcnow)


# 33. Marketing Advertisements & Banners
class Advertisement(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    placement = Column(String(50), nullable=False, default="sidebar")
    image_url = Column(Text, nullable=False)
    target_url = Column(Text, nullable=True)
    is_active = Column(Integer, nullable=False, default=1)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    impressions = Column(Integer, nullable=False, default=0)
    clicks = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


# 34. Role Permissions Matrix
class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50), nullable=False, index=True)
    module_key = Column(String(100), nullable=False)
    label = Column(String(255), nullable=False)
    enabled = Column(Integer, nullable=False, default=1)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("role_name", "module_key", name="uq_role_module"),
    )


# 35. Persistent File Storage (PostgreSQL Binary / S3 Object Storage)
class StoredFile(Base):
    __tablename__ = "stored_files"

    id = Column(String(64), primary_key=True)
    filename = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False, default="application/octet-stream")
    file_size = Column(Integer, nullable=False, default=0)
    storage_backend = Column(String(50), nullable=False, default="postgres_bytea")
    file_data = Column(LargeBinary, nullable=True)
    external_url = Column(Text, nullable=True)
    category = Column(String(50), nullable=True, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


# 36. Master Fee Heads Structure
class FeeHead(Base):
    __tablename__ = "fee_heads"

    id = Column(String(50), primary_key=True)
    code = Column(String(50), nullable=False, unique=True, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False, default="One-Time")
    course = Column(String(100), nullable=False, default="All Courses")
    default_amount = Column(Float, nullable=False, default=0.0)
    gst = Column(String(50), nullable=False, default="Exempt (0%)")
    mandatory = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


# 37. Institute Expense Vouchers & Petty Cash Ledger
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(String(50), primary_key=True)
    category = Column(String(150), nullable=False, index=True)
    amount = Column(Float, nullable=False, default=0.0)
    payee = Column(String(150), nullable=False)
    mode = Column(String(100), nullable=False, default="Cash Voucher")
    notes = Column(Text, nullable=True)
    expense_date = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
