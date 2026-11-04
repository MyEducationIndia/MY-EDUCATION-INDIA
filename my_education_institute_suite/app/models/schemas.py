from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any

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

# Assignments
class AssignmentCreate(BaseModel):
    title: str
    course_id: int
    batch_id: int
    trainer_id: int
    due_date: str
    instructions: str
    max_marks: Optional[int] = 20

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

class NewsletterSubscribe(BaseModel):
    email: str

class TestimonialCreate(BaseModel):
    name: str
    course: str
    quote: str
    rating: Optional[int] = 5

class FaqCreate(BaseModel):
    question: str
    answer: str
    category: Optional[str] = "General"

class BlogCreate(BaseModel):
    title: str
    slug: str
    author: str
    category: str
    summary: str
    content: str
    read_time: Optional[str] = "5 min read"

class CmsUpdate(BaseModel):
    settings: Dict[str, str]

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
