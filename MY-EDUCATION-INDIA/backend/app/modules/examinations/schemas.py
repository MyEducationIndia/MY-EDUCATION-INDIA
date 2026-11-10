import uuid
from datetime import date, datetime, time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


# ------------------- Exam Types & Sessions -------------------
class ExamTypeCreate(BaseModel):
    institute_id: uuid.UUID
    code: str = Field(..., min_length=2, max_length=32)
    name: str = Field(..., min_length=2, max_length=120)
    category: str = "EXTERNAL" # INTERNAL, EXTERNAL
    default_weightage_pct: float = Field(100.0, ge=0.0, le=100.0)


class ExamTypeResponse(ExamTypeCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    is_active: bool
    created_at: datetime


class ExamSessionCreate(BaseModel):
    institute_id: uuid.UUID
    branch_id: Optional[uuid.UUID] = None
    academic_year_id: uuid.UUID
    code: str = Field(..., min_length=3, max_length=48)
    name: str = Field(..., min_length=3, max_length=180)
    start_date: date
    end_date: date
    min_attendance_threshold_pct: float = Field(75.0, ge=0.0, le=100.0)
    requires_fee_clearance: bool = True


class ExamSessionResponse(ExamSessionCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    status: str
    created_at: datetime


# ------------------- Exam Schedules & Subjects -------------------
class ExamSubjectItemCreate(BaseModel):
    subject_id: uuid.UUID
    exam_type_id: uuid.UUID
    max_marks: float = Field(100.0, gt=0.0)
    pass_marks: float = Field(40.0, gt=0.0)
    credits: float = Field(4.0, ge=0.0)
    weightage_internal_pct: float = Field(30.0, ge=0.0, le=100.0)
    weightage_external_pct: float = Field(70.0, ge=0.0, le=100.0)


class ExamScheduleCreate(BaseModel):
    exam_session_id: uuid.UUID
    course_id: uuid.UUID
    semester_id: Optional[uuid.UUID] = None
    batch_id: Optional[uuid.UUID] = None
    exam_date: date
    start_time: time
    end_time: time
    subjects: List[ExamSubjectItemCreate] = Field(default_factory=list)


class ExamScheduleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    exam_session_id: uuid.UUID
    course_id: uuid.UUID
    exam_date: date
    start_time: time
    end_time: time
    created_at: datetime


# ------------------- Mark Entry -------------------
class StudentMarkItem(BaseModel):
    student_id: uuid.UUID
    internal_marks: float = Field(0.0, ge=0.0)
    external_marks: float = Field(0.0, ge=0.0)
    practical_marks: float = Field(0.0, ge=0.0)
    grace_marks: float = Field(0.0, ge=0.0)
    moderation_adjustment: float = Field(0.0)
    is_absent: bool = False


class MarkBatchEntryRequest(BaseModel):
    exam_subject_id: uuid.UUID
    marks: List[StudentMarkItem] = Field(default_factory=list)


class MarkEntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    exam_subject_id: uuid.UUID
    student_id: uuid.UUID
    total_marks_obtained: float
    is_absent: bool
    is_locked: bool
    updated_at: datetime


# ------------------- Hall Tickets -------------------
class HallTicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    hall_ticket_number: str
    schedule_id: uuid.UUID
    student_id: uuid.UUID
    seat_number: str
    qr_verification_token: str
    barcode_data: str
    is_eligible: bool
    status: str
    created_at: datetime


# ------------------- Results & Transcripts -------------------
class ResultCalculationRequest(BaseModel):
    exam_session_id: uuid.UUID
    course_id: Optional[uuid.UUID] = None
    batch_id: Optional[uuid.UUID] = None


class StudentResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    exam_session_id: uuid.UUID
    student_id: uuid.UUID
    total_credits_registered: float
    total_credits_earned: float
    percentage: float
    sgpa: float
    cgpa: float
    classification: str
    status: str
    backlog_count: int
    rank_in_batch: Optional[int]
    is_published: bool


class TranscriptResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    transcript_number: str
    student_id: uuid.UUID
    transcript_type: str
    final_cgpa: float
    digital_signature_hash: str
    issued_date: date


# ------------------- Dashboard & Analytics -------------------
class ExamDashboardSummary(BaseModel):
    active_exam_sessions_count: int
    scheduled_papers_count: int
    total_students_enrolled: int
    hall_tickets_generated_count: int
    results_published_count: int
    overall_pass_percentage: float
    grade_distribution: Dict[str, int]
    top_performers: List[Dict[str, Any]]


# ------------------- Phase 4 Module 1: EMS Dashboard Schemas -------------------
class EMSRoleDashboardSummary(BaseModel):
    role_name: str
    upcoming_exams_count: int
    running_exams_count: int
    pending_results_count: int
    evaluation_progress_percentage: float
    hall_tickets_issued_count: int
    revaluation_requests_count: int
    supplementary_exams_count: int
    overall_pass_percentage: float
    total_active_students: int
    active_evaluation_cycles: int


class EMSUpcomingExamWidget(BaseModel):
    id: uuid.UUID
    title: str
    exam_type: str
    exam_date: str
    session_code: str
    total_students: int
    center_code: str


class EMSRunningExamWidget(BaseModel):
    id: uuid.UUID
    subject_name: str
    room_lab: str
    shift_timing: str
    attendance_marked_pct: float
    status: str


class EMSEvaluationProgressWidget(BaseModel):
    course_name: str
    evaluator_name: str
    total_scripts: int
    evaluated_scripts: int
    progress_pct: float
    deadline: str


class EMSDashboardResponse(BaseModel):
    role_name: str
    metrics: EMSRoleDashboardSummary
    upcoming_exams: List[EMSUpcomingExamWidget]
    running_exams: List[EMSRunningExamWidget]
    evaluation_progress: List[EMSEvaluationProgressWidget]
    revaluation_summary: Dict[str, Any]
    supplementary_summary: Dict[str, Any]


# ------------------- Phase 4 Module 2: Academic Structure Schemas -------------------
class AcademicSessionCreate(BaseModel):
    session_code: str = Field(..., max_length=48)
    name: str = Field(..., max_length=120)
    start_date: date
    end_date: date
    is_current: bool = True
    status: str = Field("ACTIVE")


class AcademicSessionResponse(AcademicSessionCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    institute_id: uuid.UUID
    created_at: datetime


class AcademicSemesterCreate(BaseModel):
    academic_session_id: uuid.UUID
    semester_code: str = Field(..., max_length=48)
    name: str = Field(..., max_length=120)
    semester_type: str = Field("ODD", description="ODD, EVEN, SUMMER, TRIMESTER")
    start_date: date
    end_date: date
    is_active: bool = True


class AcademicSemesterResponse(AcademicSemesterCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime


class AssessmentComponentTypeCreate(BaseModel):
    code: str = Field(..., max_length=48)
    name: str = Field(..., max_length=120)
    modality: str = Field("THEORY_OFFLINE")
    default_max_marks: float = Field(100.0, ge=1.0)
    default_pass_percentage: float = Field(40.0, ge=0.0, le=100.0)
    default_weightage_percentage: float = Field(30.0, ge=0.0, le=100.0)
    requires_rubric: bool = False
    requires_external_examiner: bool = False
    description: Optional[str] = None


class AssessmentComponentTypeResponse(AssessmentComponentTypeCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    institute_id: uuid.UUID
    is_active: bool
    created_at: datetime


class WeightageComponentItem(BaseModel):
    component_code: str
    weightage_percentage: float
    min_pass_percentage: float
    max_marks: float


class CourseWeightageSchemeCreate(BaseModel):
    academic_semester_id: uuid.UUID
    course_id: uuid.UUID
    scheme_name: str
    components: List[WeightageComponentItem]
    minimum_aggregate_pass_pct: float = Field(40.0, ge=0.0, le=100.0)


class CourseWeightageSchemeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    academic_semester_id: uuid.UUID
    course_id: uuid.UUID
    scheme_name: str
    components_weightage_json: List[Dict[str, Any]]
    total_weightage: float
    minimum_aggregate_pass_pct: float
    created_at: datetime


class AcademicExamStructureSummaryResponse(BaseModel):
    current_session: AcademicSessionResponse
    total_semesters_active: int
    configured_modalities_count: int
    weightage_schemes_count: int
    modalities: List[AssessmentComponentTypeResponse]


# ------------------- Phase 4 Module 3: Exam Planning Schemas -------------------
class ExamDepartmentPlanCreate(BaseModel):
    exam_session_id: uuid.UUID
    department_id: uuid.UUID
    plan_code: str = Field(..., max_length=48)
    department_name: str = Field(..., max_length=120)
    head_of_department_user_id: uuid.UUID
    total_courses_planned: int = Field(0, ge=0)
    total_candidates_eligible: int = Field(0, ge=0)
    status: str = Field("DRAFT")


class ExamDepartmentPlanResponse(ExamDepartmentPlanCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime


class ExamTimeSlotCreate(BaseModel):
    slot_code: str = Field(..., max_length=32)
    name: str = Field(..., max_length=120)
    start_time: time
    end_time: time
    duration_minutes: int = Field(180, ge=30)
    is_active: bool = True


class ExamTimeSlotResponse(ExamTimeSlotCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    institute_id: uuid.UUID
    created_at: datetime


class ExamCourseMappingCreate(BaseModel):
    plan_id: uuid.UUID
    course_id: uuid.UUID
    course_code: str
    course_title: str
    component_type_id: Optional[uuid.UUID] = None
    component_code: str = Field("SEMESTER_FINAL")
    paper_code: str
    max_marks: float = Field(100.0, ge=1.0)
    passing_marks: float = Field(40.0, ge=0.0)
    duration_minutes: int = Field(180, ge=30)


class ExamCourseMappingResponse(ExamCourseMappingCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime


class ExamRoomPlanningCreate(BaseModel):
    center_code: str = Field("TC-IND-01")
    building_name: str = Field(..., max_length=120)
    room_number: str = Field(..., max_length=48)
    room_type: str = Field("EXAM_HALL")
    bench_count: int = Field(30, ge=1)
    seats_per_bench: int = Field(2, ge=1, le=4)
    total_capacity: int = Field(60, ge=1)
    buffer_seats: int = Field(6, ge=0)
    is_active: bool = True


class ExamRoomPlanningResponse(ExamRoomPlanningCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    institute_id: uuid.UUID
    created_at: datetime


class ExamFacultyDutyPlanningCreate(BaseModel):
    faculty_user_id: uuid.UUID
    faculty_name: str
    department_name: str
    duty_type: str = Field("ROOM_INVIGILATOR")
    assigned_room_id: Optional[uuid.UUID] = None
    assigned_date: date
    slot_code: str = Field("SLOT-MORNING-A")
    status: str = Field("ALLOCATED")


class ExamFacultyDutyPlanningResponse(ExamFacultyDutyPlanningCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    institute_id: uuid.UUID
    created_at: datetime


class ExamPlanningCalendarResponse(BaseModel):
    session_id: uuid.UUID
    session_title: str
    total_slots_count: int
    total_plans_count: int
    total_rooms_planned: int
    total_faculty_allocated: int
    plans: List[ExamDepartmentPlanResponse]
    slots: List[ExamTimeSlotResponse]
    rooms: List[ExamRoomPlanningResponse]
    faculty: List[ExamFacultyDutyPlanningResponse]


# Phase 4 Module 4: Timetable Generator Schemas
class TimetableScheduleCreate(BaseModel):
    session_id: uuid.UUID
    department_id: uuid.UUID
    department_name: str = Field(..., max_length=120)
    semester_id: Optional[uuid.UUID] = None
    semester_code: str = Field("SEM-5", max_length=32)
    course_id: uuid.UUID
    course_code: str = Field(..., max_length=32)
    course_title: str = Field(..., max_length=180)
    paper_code: str = Field(..., max_length=48)
    component_type: str = Field("THEORY_OFFLINE", max_length=48)
    is_practical: bool = False
    batch_name: str = Field("ALL", max_length=48)
    exam_date: date
    time_slot_id: Optional[uuid.UUID] = None
    slot_code: str = Field("SLOT-MORNING-A", max_length=32)
    start_time: str = Field("09:30", max_length=16)
    end_time: str = Field("12:30", max_length=16)
    room_id: Optional[uuid.UUID] = None
    room_number: str = Field("HALL-A1", max_length=48)
    building_name: str = Field("Main Examination Complex", max_length=120)
    faculty_in_charge_id: Optional[uuid.UUID] = None
    faculty_name: Optional[str] = None
    max_candidates: int = Field(60, ge=1)
    allocated_candidates: int = Field(60, ge=1)
    status: str = Field("SCHEDULED", max_length=32)
    conflict_notes: Optional[str] = None
    is_locked: bool = False


class TimetableScheduleUpdate(BaseModel):
    exam_date: Optional[date] = None
    slot_code: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    room_id: Optional[uuid.UUID] = None
    room_number: Optional[str] = None
    building_name: Optional[str] = None
    faculty_in_charge_id: Optional[uuid.UUID] = None
    faculty_name: Optional[str] = None
    allocated_candidates: Optional[int] = None
    status: Optional[str] = None
    conflict_notes: Optional[str] = None
    is_locked: Optional[bool] = None


class TimetableScheduleResponse(TimetableScheduleCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class TimetableAutoGenerateRequest(BaseModel):
    session_id: uuid.UUID
    department_id: Optional[uuid.UUID] = None
    semester_id: Optional[uuid.UUID] = None
    start_date: date
    end_date: date
    min_study_gap_days: int = Field(1, ge=0, le=7)
    enable_batch_scheduling_for_labs: bool = True
    lab_batch_size: int = Field(30, ge=10, le=100)
    preferred_slots: List[str] = Field(default_factory=lambda: ["SLOT-MORNING-A", "SLOT-AFTERNOON-B"])


class TimetableConflictResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    session_id: uuid.UUID
    schedule_id: Optional[uuid.UUID] = None
    conflict_type: str
    severity: str
    description: str
    suggested_resolution: Optional[str] = None
    is_resolved: bool
    resolution_action: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime


class TimetableConflictResolveRequest(BaseModel):
    action: str = Field(..., max_length=120)
    new_room_number: Optional[str] = None
    new_slot_code: Optional[str] = None
    new_date: Optional[date] = None


class TimetableAutoGenerateResponse(BaseModel):
    session_id: uuid.UUID
    total_courses_scheduled: int
    total_shifts_utilized: int
    total_rooms_utilized: int
    conflicts_detected: int
    schedules: List[TimetableScheduleResponse]
    conflicts: List[TimetableConflictResponse]


# Phase 4 Module 5: Hall Ticket System Schemas
class HallTicketPaperEntry(BaseModel):
    course_code: str
    course_title: str
    paper_code: str
    exam_date: str
    slot_code: str
    start_time: str
    end_time: str
    room_number: str
    seat_number: str
    is_practical: bool = False


class HallTicketCreate(BaseModel):
    session_id: uuid.UUID
    student_id: uuid.UUID
    enrollment_no: str
    roll_number: str
    candidate_name: str
    father_name: str = "Shri R. K. Sharma"
    program_name: str = "B.Tech Computer Science & Engineering"
    department_name: str = "Computer Science & Engineering"
    semester_code: str = "SEM-5"
    academic_year: str = "2026-2027"
    exam_center_code: str = "TC-IND-01"
    exam_center_name: str = "Main Examination Complex, MEI Autonomous Campus"
    exam_center_address: str = "Campus Ring Road, Indore, Madhya Pradesh - 452010"
    ticket_number: str
    barcode_data: str
    qr_verification_code: str
    digital_signature_hash: str
    controller_name: str = "Dr. V. K. Maheshwari, Controller of Examinations"
    signed_at: Optional[datetime] = None
    issue_date: Optional[date] = None
    status: str = "ISSUED"
    eligibility_status: str = "ELIGIBLE"
    paper_entries: List[HallTicketPaperEntry] = Field(default_factory=list)
    student_instructions: List[str] = Field(default_factory=list)


class HallTicketResponse(HallTicketCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    download_count: int
    last_downloaded_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class HallTicketBulkGenerateRequest(BaseModel):
    session_id: uuid.UUID
    department_id: Optional[uuid.UUID] = None
    semester_code: Optional[str] = None
    require_fee_clearance: bool = True
    require_attendance_threshold: bool = True
    minimum_attendance_pct: float = Field(75.0, ge=0.0, le=100.0)


class HallTicketBulkGenerateResponse(BaseModel):
    session_id: uuid.UUID
    total_eligible_students: int
    tickets_generated: int
    tickets_blocked_fees: int
    tickets_blocked_attendance: int
    tickets: List[HallTicketResponse]


class HallTicketVerificationResponse(BaseModel):
    is_valid: bool
    ticket_number: str
    candidate_name: str
    roll_number: str
    enrollment_no: str
    program_name: str
    semester_code: str
    exam_center: str
    digital_signature_hash: str
    controller_name: str
    signed_at: datetime
    status: str
    papers_count: int
    verification_timestamp: datetime
    verification_message: str


class HallTicketStatusUpdateRequest(BaseModel):
    status: str
    reason: Optional[str] = None


# Phase 4 Module 6: Seating & Room Management Schemas
class ExamBuildingCreate(BaseModel):
    building_code: str = Field(..., max_length=32)
    building_name: str = Field(..., max_length=120)
    total_floors: int = Field(4, ge=1)
    has_elevator: bool = True
    is_accessible: bool = True
    is_active: bool = True


class ExamBuildingResponse(ExamBuildingCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    institute_id: uuid.UUID
    created_at: datetime


class ExamRoomLayoutCreate(BaseModel):
    building_id: uuid.UUID
    room_number: str = Field(..., max_length=48)
    floor_number: int = Field(1, ge=0)
    room_type: str = Field("CENTRAL_HALL", max_length=32)
    rows_count: int = Field(10, ge=1)
    columns_count: int = Field(6, ge=1)
    benches_count: int = Field(60, ge=1)
    seats_per_bench: int = Field(2, ge=1, le=4)
    total_capacity: int = Field(120, ge=1)
    buffer_capacity: int = Field(10, ge=0)
    has_cctv: bool = True
    is_air_conditioned: bool = True
    is_active: bool = True


class ExamRoomLayoutResponse(ExamRoomLayoutCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime


class SeatAllocationItem(BaseModel):
    seat_label: str
    row_num: int
    col_num: int
    bench_num: int
    seat_pos: int
    roll_number: Optional[str] = None
    candidate_name: Optional[str] = None
    department_code: Optional[str] = None
    course_code: Optional[str] = None
    paper_code: Optional[str] = None
    is_buffer: bool = False


class SeatingPlanGenerateRequest(BaseModel):
    session_id: uuid.UUID
    room_id: uuid.UUID
    exam_date: date
    slot_code: str = Field("SLOT-MORNING-A", max_length=32)
    allocation_strategy: str = Field("CHECKERBOARD_GRID", max_length=48)
    buffer_percentage: float = Field(10.0, ge=0.0, le=50.0)


class SeatingPlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    session_id: uuid.UUID
    schedule_id: Optional[uuid.UUID] = None
    room_id: uuid.UUID
    room_number: str
    exam_date: date
    slot_code: str
    allocation_strategy: str
    total_allocated_seats: int
    total_empty_buffer_seats: int
    status: str
    seating_matrix: List[SeatAllocationItem]
    created_at: datetime
    updated_at: datetime


class SeatingPlanDoorNoticeResponse(BaseModel):
    plan_id: uuid.UUID
    room_number: str
    building_name: str
    exam_date: date
    slot_code: str
    session_title: str
    total_candidates: int
    department_roll_ranges: List[Dict[str, Any]]
    invigilator_names: List[str]
    generated_at: datetime


# Phase 4 Module 7: Invigilator Management Schemas
class InvigilatorProfileCreate(BaseModel):
    invigilator_type: str = Field("INTERNAL_FACULTY", max_length=32)
    full_name: str = Field(..., max_length=120)
    email: str = Field(..., max_length=120)
    phone: str = Field(..., max_length=32)
    institution_name: str = Field("MY EDUCATION INDIA Autonomous Campus, Indore", max_length=140)
    department_name: str = Field(..., max_length=120)
    designation: str = Field(..., max_length=80)
    experience_years: int = Field(5, ge=0)
    is_external: bool = False
    bank_account_no: Optional[str] = None
    ifsc_code: Optional[str] = None
    pan_number: Optional[str] = None
    max_duties_per_session: int = Field(6, ge=1)
    is_active: bool = True


class InvigilatorProfileResponse(InvigilatorProfileCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    institute_id: uuid.UUID
    allocated_duties_count: int
    created_at: datetime


class InvigilatorRosterCreate(BaseModel):
    session_id: uuid.UUID
    invigilator_id: uuid.UUID
    schedule_id: Optional[uuid.UUID] = None
    room_number: str = Field(..., max_length=48)
    building_name: str = Field("Main Examination Complex", max_length=120)
    duty_date: date
    slot_code: str = Field("SLOT-MORNING-A", max_length=32)
    start_time: str = Field("09:30", max_length=16)
    end_time: str = Field("12:30", max_length=16)
    duty_role: str = Field("ROOM_INVIGILATOR", max_length=32)
    status: str = Field("ALLOCATED", max_length=32)
    honorarium_amount: float = Field(0.0, ge=0.0)


class InvigilatorRosterResponse(InvigilatorRosterCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    replacement_roster_id: Optional[uuid.UUID] = None
    replacement_reason: Optional[str] = None
    duty_report_notes: Optional[str] = None
    booklets_issued: int
    booklets_collected: int
    malpractice_cases_reported: int
    honorarium_status: str
    created_at: datetime
    updated_at: datetime
    invigilator_name: Optional[str] = None
    invigilator_department: Optional[str] = None
    is_external: Optional[bool] = None


class InvigilatorAttendanceRequest(BaseModel):
    status: str = Field("REPORTED_PRESENT", max_length=32)
    notes: Optional[str] = None


class InvigilatorReplacementRequest(BaseModel):
    replacement_invigilator_id: uuid.UUID
    reason: str = Field(..., max_length=240)


class InvigilatorDutyReportSubmitRequest(BaseModel):
    booklets_issued: int = Field(..., ge=0)
    booklets_collected: int = Field(..., ge=0)
    malpractice_cases_reported: int = Field(0, ge=0)
    notes: Optional[str] = None


class InvigilatorAutoRosterRequest(BaseModel):
    session_id: uuid.UUID
    duty_date: date
    slot_code: str = Field("SLOT-MORNING-A", max_length=32)
    prevent_same_department: bool = True
    rooms: List[str] = Field(default_factory=lambda: ["HALL-A1", "HALL-B2", "LAB-01"])


class InvigilatorAutoRosterResponse(BaseModel):
    session_id: uuid.UUID
    total_duties_allocated: int
    chief_superintendents_count: int
    room_invigilators_count: int
    relievers_count: int
    squad_members_count: int
    rosters: List[InvigilatorRosterResponse]


# Phase 4 Module 8: Practical & Viva Management Schemas
class RubricCriterionItem(BaseModel):
    criterion_name: str
    max_score: float
    weightage_pct: float
    description: Optional[str] = None


class PracticalAssessmentCreate(BaseModel):
    session_id: uuid.UUID
    course_id: uuid.UUID
    course_code: str = Field(..., max_length=32)
    course_title: str = Field(..., max_length=180)
    assessment_type: str = Field("PRACTICAL_EXAM", max_length=32)
    lab_room_number: str = Field(..., max_length=48)
    scheduled_date: date
    slot_code: str = Field("SLOT-MORNING-A", max_length=32)
    total_candidates: int = Field(30, ge=1)
    total_stations: int = Field(1, ge=1)
    max_marks: float = Field(50.0, ge=1.0)
    passing_marks: float = Field(20.0, ge=0.0)
    internal_examiner_id: Optional[uuid.UUID] = None
    external_examiner_id: Optional[uuid.UUID] = None
    external_examiner_name: Optional[str] = None
    external_examiner_institution: Optional[str] = None
    rubrics_definition: List[RubricCriterionItem] = Field(default_factory=list)
    status: str = Field("SCHEDULED", max_length=32)


class PracticalAssessmentResponse(PracticalAssessmentCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class PracticalScoreRecordCreate(BaseModel):
    student_id: uuid.UUID
    enrollment_no: str
    roll_number: str
    candidate_name: str
    batch_name: str = Field("Batch B1", max_length=48)
    station_scores: List[Dict[str, Any]] = Field(default_factory=list)
    internal_marks: float = Field(0.0, ge=0.0)
    external_marks: float = Field(0.0, ge=0.0)
    viva_marks: float = Field(0.0, ge=0.0)
    examiner_remarks: Optional[str] = None


class PracticalScoreRecordResponse(PracticalScoreRecordCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    assessment_id: uuid.UUID
    total_marks_obtained: float
    is_passed: bool
    is_locked: bool
    evaluated_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class PracticalBatchMarksEntryRequest(BaseModel):
    records: List[PracticalScoreRecordCreate]


class PracticalBatchMarksEntryResponse(BaseModel):
    assessment_id: uuid.UUID
    total_records_updated: int
    passed_count: int
    failed_count: int
    average_score: float
    score_records: List[PracticalScoreRecordResponse]


class PracticalLockApprovalRequest(BaseModel):
    internal_examiner_signature: str
    external_examiner_signature: str
    approval_notes: Optional[str] = None


# Phase 4 Module 9: Attendance During Exams Schemas
class CandidateAttendanceCreate(BaseModel):
    session_id: uuid.UUID
    schedule_id: uuid.UUID
    student_id: uuid.UUID
    hall_ticket_id: Optional[uuid.UUID] = None
    enrollment_no: str = Field(..., max_length=48)
    roll_number: str = Field(..., max_length=48)
    candidate_name: str = Field(..., max_length=120)
    room_number: str = Field(..., max_length=48)
    seat_number: str = Field(..., max_length=48)
    attendance_status: str = Field("PRESENT", max_length=32)
    entry_time: Optional[datetime] = None
    answer_booklet_barcode: Optional[str] = None
    supplementary_booklet_count: int = Field(0, ge=0)
    supplementary_booklet_barcodes: List[str] = Field(default_factory=list)
    malpractice_category: Optional[str] = None
    malpractice_evidence_notes: Optional[str] = None
    medical_contingency_notes: Optional[str] = None
    invigilator_signature_flag: bool = True
    candidate_signature_flag: bool = True


class CandidateAttendanceResponse(CandidateAttendanceCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class AttendanceUpdateItem(BaseModel):
    attendance_id: uuid.UUID
    attendance_status: str
    answer_booklet_barcode: Optional[str] = None
    supplementary_booklet_count: int = 0
    supplementary_booklet_barcodes: List[str] = Field(default_factory=list)


class AttendanceBatchUpdateRequest(BaseModel):
    schedule_id: uuid.UUID
    attendances: List[AttendanceUpdateItem]


class AttendanceBatchUpdateResponse(BaseModel):
    schedule_id: uuid.UUID
    total_updated: int
    present_count: int
    absent_count: int
    late_count: int
    malpractice_count: int
    medical_count: int
    records: List[CandidateAttendanceResponse]


class AttendanceQrScanRequest(BaseModel):
    schedule_id: uuid.UUID
    qr_or_ticket_number: str
    answer_booklet_barcode: Optional[str] = None


class AttendanceQrScanResponse(BaseModel):
    is_success: bool
    message: str
    candidate_name: str
    roll_number: str
    allocated_seat: str
    assigned_booklet_barcode: Optional[str] = None
    entry_timestamp: datetime
    record: Optional[CandidateAttendanceResponse] = None


class MalpracticeReportRequest(BaseModel):
    malpractice_category: str = Field(..., max_length=64)
    evidence_notes: str
    confiscated_items: Optional[str] = None


class MedicalCaseReportRequest(BaseModel):
    contingency_notes: str
    compensatory_minutes_approved: int = Field(20, ge=0, le=60)


class HallAttendanceSummaryResponse(BaseModel):
    schedule_id: uuid.UUID
    room_number: str
    total_allocated: int
    present_count: int
    absent_count: int
    late_count: int
    malpractice_count: int
    medical_count: int
    total_main_booklets_used: int
    total_supplementary_used: int
    all_present_verified: bool


# Phase 4 Module 10: Evaluation Management Schemas
class EvaluationBatchCreate(BaseModel):
    session_id: uuid.UUID
    schedule_id: Optional[uuid.UUID] = None
    course_code: str = Field(..., max_length=32)
    paper_code: str = Field(..., max_length=48)
    evaluation_mode: str = Field("DIGITAL_ON_SCREEN", max_length=32)
    evaluation_type: str = Field("DOUBLE_BLIND", max_length=32)
    total_scripts: int = Field(0, ge=0)
    max_marks: float = Field(70.0, ge=1.0)
    passing_marks: float = Field(28.0, ge=0.0)
    max_deviation_threshold: float = Field(15.0, ge=0.0)
    evaluator_1_id: Optional[uuid.UUID] = None
    evaluator_2_id: Optional[uuid.UUID] = None
    moderator_id: Optional[uuid.UUID] = None


class EvaluationBatchResponse(EvaluationBatchCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    evaluated_scripts: int
    moderated_scripts: int
    status: str
    created_at: datetime
    updated_at: datetime


class ScriptScoreSubmitRequest(BaseModel):
    evaluator_number: int = Field(1, ge=1, le=2)
    question_scores: Dict[str, float]
    remarks: Optional[str] = None


class ScriptEvaluationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    batch_id: uuid.UUID
    dummy_barcode: str
    actual_roll_number: Optional[str] = None
    actual_candidate_name: Optional[str] = None
    evaluator_1_marks: Optional[float] = None
    evaluator_1_breakdown: Dict[str, Any] = Field(default_factory=dict)
    evaluator_2_marks: Optional[float] = None
    evaluator_2_breakdown: Dict[str, Any] = Field(default_factory=dict)
    moderator_marks: Optional[float] = None
    moderator_breakdown: Dict[str, Any] = Field(default_factory=dict)
    deviation_pct: Optional[float] = None
    is_deviation_triggered: bool = False
    grace_marks_awarded: float = 0.0
    grace_rule_applied: Optional[str] = None
    final_score: Optional[float] = None
    rechecking_status: str = "NONE"
    is_locked: bool = False
    created_at: datetime
    updated_at: datetime


class ModerationApplyRequest(BaseModel):
    moderator_marks: float = Field(..., ge=0.0)
    moderator_breakdown: Dict[str, Any] = Field(default_factory=dict)
    notes: str = Field(..., max_length=240)


class GraceMarksApplyRequest(BaseModel):
    grace_marks: float = Field(..., ge=0.0, le=5.0)
    ordinance_rule: str = Field("ORDINANCE_5_PERCENT_PASSING_DEFICIT", max_length=120)


class RecheckingProcessRequest(BaseModel):
    action: str = Field("ARITHMETIC_VERIFIED", max_length=64)
    revised_score: Optional[float] = None
    scrutiny_notes: str = Field(..., max_length=240)


# Phase 4 Module 11: Marks Entry Schemas
class StudentMarkItemCreate(BaseModel):
    student_id: uuid.UUID
    roll_number: str = Field(..., max_length=48)
    enrollment_no: str = Field(..., max_length=48)
    candidate_name: str = Field(..., max_length=120)
    marks_obtained: float = Field(0.0, ge=0.0)
    is_absent: bool = False
    is_malpractice: bool = False
    faculty_remarks: Optional[str] = None


class StudentMarkItemResponse(StudentMarkItemCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    submission_id: uuid.UUID
    is_passed: bool
    grade_letter: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class MarksSubmissionCreate(BaseModel):
    session_id: uuid.UUID
    course_id: uuid.UUID
    course_code: str = Field(..., max_length=32)
    course_title: str = Field(..., max_length=180)
    component_type: str = Field("THEORY_INTERNAL", max_length=48)
    semester_code: str = Field("SEM-5", max_length=32)
    faculty_user_id: uuid.UUID
    faculty_name: str = Field(..., max_length=120)
    department_name: str = Field(..., max_length=120)
    max_marks: float = Field(30.0, ge=1.0)
    passing_marks: float = Field(12.0, ge=0.0)
    submission_mode: str = Field("ONLINE_PORTAL", max_length=32)


class MarksSubmissionResponse(MarksSubmissionCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    status: str
    is_locked: bool
    locked_at: Optional[datetime] = None
    hod_approved_at: Optional[datetime] = None
    coe_approved_at: Optional[datetime] = None
    approval_notes: Optional[str] = None
    total_students_enrolled: int
    total_marks_entered: int
    created_at: datetime
    updated_at: datetime


class MarksBatchSaveRequest(BaseModel):
    marks: List[StudentMarkItemCreate]


class MarksBatchSaveResponse(BaseModel):
    submission_id: uuid.UUID
    total_updated: int
    highest_marks: float
    lowest_marks: float
    average_marks: float
    passed_count: int
    failed_count: int
    entries: List[StudentMarkItemResponse]


class MarksExcelRowItem(BaseModel):
    roll_number: str
    marks_obtained: float
    is_absent: bool = False
    faculty_remarks: Optional[str] = None


class MarksExcelImportRequest(BaseModel):
    rows: List[MarksExcelRowItem]


class MarksExcelImportResponse(BaseModel):
    submission_id: uuid.UUID
    total_imported: int
    errors: List[str]
    entries: List[StudentMarkItemResponse]


class MarksWorkflowApprovalRequest(BaseModel):
    action: str = Field("SUBMIT", max_length=32)  # SUBMIT, HOD_APPROVE, COE_LOCK, REJECT_REVISION
    notes: Optional[str] = None


# Phase 4 Module 12: Result Processing Schemas
class CourseResultItem(BaseModel):
    course_code: str
    course_title: str
    credits: float = 4.0
    internal_marks: float = 0.0
    external_marks: float = 0.0
    total_marks: float
    max_marks: float = 100.0
    grade_letter: str
    grade_point: float
    is_passed: bool = True


class StudentSemesterResultCreate(BaseModel):
    session_id: uuid.UUID
    student_id: uuid.UUID
    roll_number: str = Field(..., max_length=48)
    enrollment_no: str = Field(..., max_length=48)
    candidate_name: str = Field(..., max_length=120)
    program_name: str = Field("B.Tech Computer Science & Engineering", max_length=120)
    department_name: str = Field("Computer Science & Engineering", max_length=120)
    semester_code: str = Field("SEM-5", max_length=32)
    academic_year: str = Field("2026-2027", max_length=32)
    grading_system: str = Field("ABSOLUTE", max_length=32)
    total_credits_registered: float = Field(24.0, ge=0.0)
    total_credits_earned: float = Field(24.0, ge=0.0)
    total_marks_obtained: float = Field(480.0, ge=0.0)
    total_max_marks: float = Field(600.0, ge=1.0)
    percentage: float = Field(80.0, ge=0.0, le=100.0)
    sgpa: float = Field(8.5, ge=0.0, le=10.0)
    cgpa: float = Field(8.65, ge=0.0, le=10.0)
    overall_grade: str = Field("A", max_length=8)
    division: str = Field("FIRST_CLASS_DISTINCTION", max_length=48)
    class_rank: int = Field(1, ge=1)
    result_status: str = Field("PASSED", max_length=32)
    course_results: List[CourseResultItem] = Field(default_factory=list)
    is_published: bool = False


class StudentSemesterResultResponse(StudentSemesterResultCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class ResultProcessingCalculateRequest(BaseModel):
    session_id: uuid.UUID
    department_name: Optional[str] = None
    semester_code: Optional[str] = "SEM-5"
    grading_system: str = Field("ABSOLUTE", max_length=32)  # ABSOLUTE, RELATIVE
    relative_curve_top_pct: float = Field(10.0, ge=5.0, le=25.0)


class ResultProcessingCalculateResponse(BaseModel):
    session_id: uuid.UUID
    grading_system: str
    total_students_processed: int
    total_passed: int
    total_failed: int
    class_average_sgpa: float
    class_average_cgpa: float
    results: List[StudentSemesterResultResponse]


class MeritListEntryItem(BaseModel):
    rank: int
    roll_number: str
    candidate_name: str
    cgpa: float
    sgpa: float
    percentage: float
    medal_category: str  # GOLD_MEDALIST, SILVER_MEDALIST, BRONZE_MEDALIST, MERIT_HONORS


class MeritListGenerateRequest(BaseModel):
    session_id: uuid.UUID
    program_name: str = Field("B.Tech Computer Science & Engineering", max_length=120)
    semester_code: str = Field("SEM-5", max_length=32)
    top_n: int = Field(10, ge=1, le=50)


class MeritListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    session_id: uuid.UUID
    program_name: str
    semester_code: str
    academic_year: str
    grading_system: str
    merit_entries: List[MeritListEntryItem]
    published_at: Optional[datetime] = None
    created_at: datetime


# ============================================================================
# PHASE 4 MODULE 13: REVALUATION & SUPPLEMENTARY SCHEMAS
# ============================================================================

class RevaluationApplicationCreate(BaseModel):
    session_id: uuid.UUID
    roll_number: str = Field(..., max_length=48)
    enrollment_no: str = Field(..., max_length=48)
    candidate_name: str = Field(..., max_length=120)
    course_code: str = Field(..., max_length=32)
    course_name: str = Field(..., max_length=120)
    service_type: str = Field("CHALLENGE_REVALUATION", max_length=32)  # RE_TOTALING, PHOTOCOPY_INSPECTION, CHALLENGE_REVALUATION
    original_marks: float = Field(..., ge=0.0, le=100.0)
    original_grade: str = Field("F", max_length=8)
    fee_amount: float = Field(1000.0, ge=0.0)
    payment_reference: Optional[str] = Field(None, max_length=64)


class RevaluationApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    session_id: uuid.UUID
    student_id: uuid.UUID
    roll_number: str
    enrollment_no: str
    candidate_name: str
    course_code: str
    course_name: str
    service_type: str
    application_status: str
    fee_amount: float
    payment_reference: Optional[str] = None
    payment_status: str
    original_marks: float
    original_grade: str
    reval_marks: Optional[float] = None
    third_eval_marks: Optional[float] = None
    final_marks: float
    updated_grade: str
    is_marks_changed: bool
    fee_refunded: bool
    photocopy_url: Optional[str] = None
    evaluator_user_id: Optional[uuid.UUID] = None
    evaluator_name: Optional[str] = None
    evaluator_remarks: Optional[str] = None
    coe_approved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class RevaluationAssignEvaluatorRequest(BaseModel):
    evaluator_user_id: uuid.UUID
    evaluator_name: str = Field(..., max_length=120)


class RevaluationScoreSubmitRequest(BaseModel):
    reval_marks: float = Field(..., ge=0.0, le=100.0)
    evaluator_remarks: Optional[str] = None
    is_third_evaluation: bool = False


class RevaluationFinalizeRequest(BaseModel):
    coe_remarks: Optional[str] = None


class SupplementaryRegistrationCreate(BaseModel):
    session_id: uuid.UUID
    roll_number: str = Field(..., max_length=48)
    enrollment_no: str = Field(..., max_length=48)
    candidate_name: str = Field(..., max_length=120)
    course_code: str = Field(..., max_length=32)
    course_name: str = Field(..., max_length=120)
    credits: float = Field(4.0, ge=1.0, le=8.0)
    original_attempt_session: str = Field("AUTUMN-2025", max_length=64)
    fee_amount: float = Field(750.0, ge=0.0)
    payment_reference: Optional[str] = Field(None, max_length=64)


class SupplementaryRegistrationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    session_id: uuid.UUID
    student_id: uuid.UUID
    roll_number: str
    enrollment_no: str
    candidate_name: str
    course_code: str
    course_name: str
    credits: float
    original_attempt_session: str
    fee_amount: float
    payment_reference: Optional[str] = None
    payment_status: str
    hall_ticket_generated: bool
    exam_status: str
    marks_obtained: Optional[float] = None
    max_marks: float
    grade_obtained: Optional[str] = None
    is_cleared: bool
    created_at: datetime
    updated_at: datetime


class SupplementaryRecordMarksRequest(BaseModel):
    marks_obtained: float = Field(..., ge=0.0, le=100.0)
    exam_status: str = Field("APPEARED", max_length=32)


# ============================================================================
# PHASE 4 MODULE 14: TRANSCRIPTS & CERTIFICATES SCHEMAS
# ============================================================================

class CertificateIssueRequest(BaseModel):
    session_id: uuid.UUID
    roll_number: str = Field(..., max_length=48)
    enrollment_no: str = Field(..., max_length=48)
    candidate_name: str = Field(..., max_length=120)
    program_name: str = Field("B.Tech Computer Science & Engineering", max_length=120)
    department_name: str = Field("Computer Science & Engineering", max_length=120)
    certificate_type: str = Field("CONSOLIDATED_TRANSCRIPT", max_length=48)
    cgpa: float = Field(..., ge=0.0, le=10.0)
    sgpa: Optional[float] = Field(None, ge=0.0, le=10.0)
    division: str = Field("FIRST_CLASS_DISTINCTION", max_length=48)
    academic_year: str = Field("2026-2027", max_length=32)
    transcript_payload: Optional[Dict[str, Any]] = None


class CertificateRegistryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    session_id: uuid.UUID
    student_id: uuid.UUID
    roll_number: str
    enrollment_no: str
    candidate_name: str
    program_name: str
    department_name: str
    certificate_type: str
    serial_number: str
    cgpa: float
    sgpa: Optional[float] = None
    division: str
    academic_year: str
    qr_verification_url: str
    verification_hash: str
    is_revoked: bool
    revocation_reason: Optional[str] = None
    issued_at: datetime
    transcript_payload: Dict[str, Any]
    created_at: datetime
    updated_at: datetime


class CertificateVerificationResponse(BaseModel):
    is_valid: bool
    status: str  # VERIFIED_AUTHENTIC, REVOKED, NOT_FOUND
    serial_number: Optional[str] = None
    certificate_type: Optional[str] = None
    candidate_name: Optional[str] = None
    roll_number: Optional[str] = None
    program_name: Optional[str] = None
    cgpa: Optional[float] = None
    division: Optional[str] = None
    issued_at: Optional[datetime] = None
    verification_hash: Optional[str] = None


class CertificateRevokeRequest(BaseModel):
    revocation_reason: str = Field(..., min_length=5)


class TranscriptRequestCreate(BaseModel):
    roll_number: str = Field(..., max_length=48)
    enrollment_no: str = Field(..., max_length=48)
    candidate_name: str = Field(..., max_length=120)
    request_type: str = Field("OFFICIAL_TRANSCRIPT", max_length=48)
    delivery_mode: str = Field("DIGITAL_DOWNLOAD", max_length=32)
    copies: int = Field(1, ge=1, le=10)
    fee_amount: float = Field(500.0, ge=0.0)
    payment_reference: Optional[str] = Field(None, max_length=64)
    recipient_address: Optional[str] = None


class TranscriptRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    student_id: uuid.UUID
    roll_number: str
    enrollment_no: str
    candidate_name: str
    request_type: str
    delivery_mode: str
    copies: int
    fee_amount: float
    payment_reference: Optional[str] = None
    payment_status: str
    request_status: str
    tracking_number: Optional[str] = None
    recipient_address: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class TranscriptRequestStatusUpdateRequest(BaseModel):
    request_status: str = Field(..., max_length=32)
    tracking_number: Optional[str] = Field(None, max_length=64)


# ============================================================================
# PHASE 4 MODULE 15: COMPLIANCE & UNIVERSITY REPORTS SCHEMAS
# ============================================================================

class ComplianceReportCreateRequest(BaseModel):
    session_id: uuid.UUID
    academic_year: str = Field("2026-2027", max_length=32)
    report_type: str = Field("UGC_AUTONOMOUS_RETURN", max_length=64)
    regulatory_body: str = Field("UGC", max_length=64)
    reporting_period: str = Field("Autumn Semester 2026-27", max_length=64)
    metrics_payload: Optional[Dict[str, Any]] = None


class ComplianceReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    session_id: uuid.UUID
    academic_year: str
    report_type: str
    regulatory_body: str
    reporting_period: str
    status: str
    submission_reference: Optional[str] = None
    submitted_at: Optional[datetime] = None
    document_url: Optional[str] = None
    metrics_payload: Dict[str, Any]
    generated_by: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime


class ComplianceReportSubmitRequest(BaseModel):
    submission_reference: str = Field(..., max_length=64)
    submission_notes: Optional[str] = None


class MalpracticeReportCreateRequest(BaseModel):
    session_id: uuid.UUID
    roll_number: str = Field(..., max_length=48)
    candidate_name: str = Field(..., max_length=120)
    course_code: str = Field(..., max_length=32)
    clause_violated: str = Field(..., max_length=64)
    severity_level: str = Field("LEVEL_1_WARNING", max_length=32)
    committee_resolution: str = Field(..., min_length=5)
    penalty_awarded: str = Field(..., max_length=120)


class MalpracticeDisciplinaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    session_id: uuid.UUID
    student_id: uuid.UUID
    roll_number: str
    candidate_name: str
    course_code: str
    incident_date: datetime
    clause_violated: str
    severity_level: str
    committee_resolution: str
    penalty_awarded: str
    tribunal_status: str
    resolved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class MalpracticeResolveRequest(BaseModel):
    tribunal_status: str = Field("PENALTY_CONFIRMED", max_length=32)
    final_resolution_notes: str = Field(..., min_length=5)


# ============================================================================
# PHASE 4 MODULE 16: EXAMINATION ANALYTICS & PREDICTIVE SCHEMAS
# ============================================================================

class CourseAnalyticsMetricResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    session_id: uuid.UUID
    course_code: str
    course_name: str
    total_candidates: int
    pass_percentage: float
    difficulty_index: float
    discrimination_index: float
    average_marks: float
    standard_deviation: float
    highest_marks: float
    lowest_marks: float
    grade_distribution: Dict[str, Any]
    created_at: datetime
    updated_at: datetime


class CourseAnalyticsCalculateRequest(BaseModel):
    session_id: uuid.UUID
    course_code: Optional[str] = None


class StudentRiskPredictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    session_id: uuid.UUID
    student_id: uuid.UUID
    roll_number: str
    candidate_name: str
    program_name: str
    semester_code: str
    risk_level: str
    predicted_backlog_probability: float
    flagged_courses: List[str]
    recommended_interventions: List[str]
    is_acknowledged: bool
    created_at: datetime
    updated_at: datetime


class ExaminerBiasReportItem(BaseModel):
    examiner_name: str
    evaluator_type: str
    total_scripts_evaluated: int
    mean_marks_awarded: float
    cohort_mean_marks: float
    variance_delta: float
    grading_tendency: str  # LENIENT, MODERATE, STRICT
    standard_deviation: float


class AnalyticsSummaryKPIsResponse(BaseModel):
    total_students_evaluated: int
    overall_institute_pass_rate: float
    median_cgpa: float
    high_risk_students_count: int
    courses_analyzed_count: int
    average_difficulty_index: float
    average_discrimination_index: float


# ============================================================================
# PHASE 4 MODULE 17: STUDENT EXAMINATION PORTAL SCHEMAS
# ============================================================================

class StudentPortalDashboardResponse(BaseModel):
    student_info: Dict[str, Any]
    active_session: Dict[str, Any]
    exam_registration: Dict[str, Any]
    hall_ticket: Optional[Dict[str, Any]] = None
    today_seating: Optional[Dict[str, Any]] = None
    semester_result: Optional[Dict[str, Any]] = None
    active_revaluations: List[Dict[str, Any]] = Field(default_factory=list)
    active_transcripts: List[Dict[str, Any]] = Field(default_factory=list)


class StudentExamRegisterRequest(BaseModel):
    session_id: uuid.UUID
    roll_number: str = Field(..., max_length=48)
    semester_code: str = Field("SEM-5", max_length=32)
    course_codes: List[str] = Field(default_factory=list)


class StudentSeatingLookupResponse(BaseModel):
    roll_number: str
    candidate_name: str
    exam_date: str
    time_slot: str
    course_code: str
    course_name: str
    building_name: str
    floor_number: str
    room_number: str
    bench_label: str
    seat_number: int


# ============================================================================
# PHASE 4 MODULE 18: FACULTY EXAMINATION PORTAL SCHEMAS
# ============================================================================

class FacultyDutyItem(BaseModel):
    id: uuid.UUID
    duty_date: datetime
    slot_time: str
    building_name: str
    room_number: str
    duty_type: str  # ROOM_INVIGILATOR, RELIEVER, CHIEF_SUPERINTENDENT, FLYING_SQUAD
    reporting_time: str
    status: str  # ASSIGNED, COMPLETED, SWAPPED


class FacultyDutySwapRequestCreate(BaseModel):
    session_id: uuid.UUID
    target_faculty_id: uuid.UUID
    target_faculty_name: str = Field(..., max_length=120)
    duty_date: datetime
    slot_time: str = Field(..., max_length=64)
    room_number: str = Field(..., max_length=32)
    reason: str = Field(..., min_length=5)


class FacultyDutySwapResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    session_id: uuid.UUID
    requesting_faculty_id: uuid.UUID
    requesting_faculty_name: str
    target_faculty_id: uuid.UUID
    target_faculty_name: str
    duty_date: datetime
    slot_time: str
    room_number: str
    reason: str
    swap_status: str
    approved_by_coe: bool
    created_at: datetime
    updated_at: datetime


class FacultyDutySwapRespondRequest(BaseModel):
    action: str = Field(..., max_length=16)  # ACCEPT, REJECT
    response_notes: Optional[str] = None


class FacultyPortalDashboardResponse(BaseModel):
    faculty_info: Dict[str, Any]
    upcoming_invigilations: List[FacultyDutyItem] = Field(default_factory=list)
    pending_script_bundles: List[Dict[str, Any]] = Field(default_factory=list)
    marks_entry_submissions: List[Dict[str, Any]] = Field(default_factory=list)
    duty_swaps: List[FacultyDutySwapResponse] = Field(default_factory=list)


# ============================================================================
# PHASE 4 MODULE 19: CONTROLLER OF EXAMINATIONS (COE) MASTER PORTAL SCHEMAS
# ============================================================================

class CoeGovernanceCockpitResponse(BaseModel):
    session_id: uuid.UUID
    session_name: str
    lifecycle_stage: str
    is_registration_locked: bool
    is_timetable_locked: bool
    is_marks_entry_locked: bool
    is_result_declaration_locked: bool
    qp_vault_unlocked: bool
    emergency_override_active: bool
    coe_digital_signature_serial: str
    coe_signed_at: Optional[datetime] = None
    audit_events: List[Dict[str, Any]] = Field(default_factory=list)
    candidate_counts: Dict[str, int] = Field(default_factory=dict)


class CoeStageTransitionRequest(BaseModel):
    session_id: uuid.UUID
    target_stage: str = Field(..., max_length=48)
    justification: str = Field(..., min_length=5)


class CoeLockToggleRequest(BaseModel):
    session_id: uuid.UUID
    lock_target: str = Field(..., max_length=32)  # REGISTRATION, TIMETABLE, MARKS_ENTRY, RESULT_DECLARATION
    lock_state: bool


class CoeQpVaultUnlockRequest(BaseModel):
    session_id: uuid.UUID
    dual_custody_key_part1: str = Field(..., min_length=6)
    dual_custody_key_part2: str = Field(..., min_length=6)
    slot_time: str = Field("10:00 AM - 01:00 PM", max_length=64)


class CoeEmergencyOverrideRequest(BaseModel):
    session_id: uuid.UUID
    action_type: str = Field(..., max_length=64)
    reason: str = Field(..., min_length=5)
    metadata_payload: Optional[Dict[str, Any]] = None


class EmergencyOverrideLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    session_id: uuid.UUID
    action_type: str
    reason: str
    authorized_by_coe: uuid.UUID
    metadata_payload: Dict[str, Any]
    timestamp: datetime


# ============================================================================
# PHASE 4 MODULE 20: ENTERPRISE INTEGRATION & SYSTEM HEALTH SCHEMAS
# ============================================================================

class EmsSystemHealthResponse(BaseModel):
    status: str
    timestamp: datetime
    environment: str
    total_api_endpoints: int
    database_connected: bool
    active_session_id: Optional[uuid.UUID] = None
    modules_operational: int
    security_level: str


class EmsModuleIntegrationStatusItem(BaseModel):
    module_number: int
    module_name: str
    status: str
    route_prefix: str
    endpoints_count: int
    db_table: str


class EmsFullIntegrationMatrixResponse(BaseModel):
    total_modules: int
    operational_modules: int
    readiness_percentage: float
    modules: List[EmsModuleIntegrationStatusItem]
    last_verified_at: datetime
