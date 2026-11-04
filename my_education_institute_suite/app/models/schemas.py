from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import date, datetime

# Authentication & User Management
class LoginRequest(BaseModel):
    username: str
    password: str
    role: Optional[str] = "admin"

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str
    name: Optional[str] = ""
    linked_id: Optional[str] = ""

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class ForgotPasswordRequest(BaseModel):
    identifier: str # Email or Roll Number

class ResetPasswordRequest(BaseModel):
    identifier: str
    otp_code: str
    new_password: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: Optional[str] = None
    full_name: str
    role_id: int
    linked_id: Optional[str] = None

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[int] = 1

# Student Models
class StudentCreate(BaseModel):
    name: str
    dob: str
    course_id: int
    batch_id: Optional[int] = 1
    mobile: str
    email: str
    guardian_name: str
    guardian_mobile: Optional[str] = ""
    gender: str = "Male"
    blood_group: Optional[str] = "B+"
    address: Optional[str] = ""
    total_fee: float = 9500.0
    paid_fee: float = 0.0

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    dob: Optional[str] = None
    course_id: Optional[int] = None
    batch_id: Optional[int] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    guardian_name: Optional[str] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    address: Optional[str] = None
    total_fee: Optional[float] = None
    paid_fee: Optional[float] = None
    status: Optional[str] = None

# Staff Models
class StaffCreate(BaseModel):
    name: str
    designation: str
    department: str
    qualification: str
    salary_amount: Optional[float] = 40000.0
    phone: Optional[str] = ""
    email: str

class StaffUpdate(BaseModel):
    name: Optional[str] = None
    designation: Optional[str] = None
    department: Optional[str] = None
    qualification: Optional[str] = None
    salary_amount: Optional[float] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class LeaveApplyRequest(BaseModel):
    staff_id: int
    leave_type: str
    start_date: str
    end_date: str
    reason: str

# Course & Batch Models
class CourseCreate(BaseModel):
    code: str
    title: str
    category: str = "diploma"
    duration: str = "6 Months"
    fee: float = 9500.0
    eligibility: str = "10+2 Any Stream"
    highlights: Optional[str] = "Practical Lab Workflows"
    badge: Optional[str] = "Standard"

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    duration: Optional[str] = None
    fee: Optional[float] = None
    eligibility: Optional[str] = None
    highlights: Optional[str] = None
    is_active: Optional[int] = 1

class BatchCreate(BaseModel):
    code: str
    name: str
    course_id: int
    trainer_id: Optional[int] = None
    timing: str
    room: str
    capacity: Optional[int] = 30

class BatchUpdate(BaseModel):
    name: Optional[str] = None
    timing: Optional[str] = None
    room: Optional[str] = None
    trainer_id: Optional[int] = None
    capacity: Optional[int] = None

# Admissions & Fees
class AdmissionApply(BaseModel):
    applicant_name: str
    course_id: int
    preferred_timing: Optional[str] = "Morning"
    prior_qualification: str
    mobile: str
    email: str
    guardian_name: Optional[str] = ""

class FeePaymentCreate(BaseModel):
    student_id: int
    amount: float
    payment_mode: str = "UPI"
    remarks: Optional[str] = "Tuition Installment"

class FeePaymentUpdate(BaseModel):
    amount: Optional[float] = None
    payment_mode: Optional[str] = None
    remarks: Optional[str] = None

# Attendance
class AttendanceRecord(BaseModel):
    student_id: int
    batch_id: int
    date: str
    status: str
    remarks: Optional[str] = ""

# Notices & Materials
class NoticeCreate(BaseModel):
    title: str
    content: str
    target_audience: str = "All"
    category: str = "Urgent"
    is_pinned: Optional[int] = 0

class NoticeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    target_audience: Optional[str] = None
    category: Optional[str] = None
    is_pinned: Optional[int] = None

class MaterialCreate(BaseModel):
    title: str
    course_id: int
    batch_id: Optional[int] = None
    file_path: str
    file_type: str = "PDF"
    file_size: Optional[str] = "3.5 MB"
    author: Optional[str] = "Faculty Desk"

class MaterialUpdate(BaseModel):
    title: Optional[str] = None
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[str] = None
    author: Optional[str] = None

# Assignments
class AssignmentCreate(BaseModel):
    title: str
    course_id: int
    batch_id: int
    trainer_id: int
    due_date: str
    instructions: str
    max_marks: Optional[int] = 20

class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    due_date: Optional[str] = None
    instructions: Optional[str] = None
    max_marks: Optional[int] = None

class AssignmentSubmit(BaseModel):
    assignment_id: int
    student_id: int
    submission_text: str
    file_path: Optional[str] = ""

class AssignmentGrade(BaseModel):
    grade: str
    marks_obtained: float
    feedback: str

# CMS & Inquiries
class EnquiryCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str] = ""
    course_interest: Optional[str] = "D.C.A"
    message: Optional[str] = ""

class EnquiryUpdate(BaseModel):
    status: Optional[str] = None
    message: Optional[str] = None

class NewsletterSubscribe(BaseModel):
    email: str

class TestimonialCreate(BaseModel):
    name: str
    course: str
    quote: str
    rating: Optional[int] = 5

class TestimonialUpdate(BaseModel):
    name: Optional[str] = None
    course: Optional[str] = None
    quote: Optional[str] = None
    rating: Optional[int] = None
    is_featured: Optional[int] = None

class FaqCreate(BaseModel):
    question: str
    answer: str
    category: Optional[str] = "General"

class FaqUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None
    display_order: Optional[int] = None

class GalleryCreate(BaseModel):
    title: str
    category: str
    image_url: str

class GalleryUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None

class BlogCreate(BaseModel):
    title: str
    slug: str
    author: str
    category: str
    summary: str
    content: str
    read_time: Optional[str] = "5 min read"

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    read_time: Optional[str] = None

class CmsUpdate(BaseModel):
    settings: Dict[str, Any]

class SettingsUpdate(BaseModel):
    name: Optional[str] = None
    slogan: Optional[str] = None
    registration_no: Optional[str] = None
    iso_certification: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    whatsapp: Optional[str] = None
    currency: Optional[str] = None
    timezone: Optional[str] = None

# Public Downloads
class PublicDocumentCreate(BaseModel):
    title: str
    category: str = "Academic"
    file_type: str = "PDF"
    file_size: Optional[str] = "1.5 MB"
    description: Optional[str] = ""
    content: Optional[str] = ""
    download_url: Optional[str] = ""

class PublicDocumentUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    download_url: Optional[str] = None
    is_active: Optional[int] = None

# Exam Management & CBT
class ExamConfigUpdate(BaseModel):
    window_open: Optional[int] = None
    require_no_dues: Optional[int] = None
    session_title: Optional[str] = None
    start_date: Optional[str] = None
    last_form_date: Optional[str] = None
    center_name: Optional[str] = None

class ExamFormCreate(BaseModel):
    student_id: str
    student_name: str
    course: str
    batch: Optional[str] = ""
    exam_session: Optional[str] = ""
    category: Optional[str] = "Regular"
    medium: Optional[str] = "English"
    papers: Optional[List[str]] = []
    no_dues_cert_no: Optional[str] = ""

class ExamFormUpdate(BaseModel):
    status: Optional[str] = None
    admit_card_no: Optional[str] = None
    papers: Optional[List[str]] = None

class QuestionCreate(BaseModel):
    course_code: Optional[str] = None
    paper_code: Optional[str] = None
    question_text: str
    options: List[str]
    correct_option: int
    explanation: Optional[str] = ""
    marks: Optional[int] = 1

class QuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    options: Optional[List[str]] = None
    correct_option: Optional[int] = None
    explanation: Optional[str] = None
    marks: Optional[int] = None

class CBTResultSubmit(BaseModel):
    student_id: str
    roll_number: str
    exam_session: Optional[str] = ""
    score: float
    max_score: float = 100.0
    percentage: float
    status: Optional[str] = "Completed"
    answers: Optional[Dict[str, Any]] = None

# Website Sections Arrangement
class SectionOrderItem(BaseModel):
    id: str
    label: Optional[str] = None
    icon: Optional[str] = None
    visible: bool = True
    display_order: int

class SectionOrderUpdate(BaseModel):
    sections: List[SectionOrderItem]

class CustomSectionCreate(BaseModel):
    id: Optional[str] = None
    badge: Optional[str] = ""
    title: str
    subtitle: Optional[str] = ""
    content: Optional[str] = ""
    cta_text: Optional[str] = ""
    cta_action: Optional[str] = ""
    theme: Optional[str] = "gradient-indigo"
    image_url: Optional[str] = ""
    visible: Optional[bool] = True
    display_order: Optional[int] = 0

class CustomSectionUpdate(BaseModel):
    badge: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    content: Optional[str] = None
    cta_text: Optional[str] = None
    cta_action: Optional[str] = None
    theme: Optional[str] = None
    image_url: Optional[str] = None
    visible: Optional[bool] = None
    display_order: Optional[int] = None

# Advertisements
class AdvertisementCreate(BaseModel):
    title: str
    placement: Optional[str] = "sidebar"
    image_url: str
    target_url: Optional[str] = ""
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class AdvertisementUpdate(BaseModel):
    title: Optional[str] = None
    placement: Optional[str] = None
    image_url: Optional[str] = None
    target_url: Optional[str] = None
    is_active: Optional[int] = None

# Permissions
class RolePermissionUpdate(BaseModel):
    role_name: str
    permissions: Dict[str, bool]
