import uuid
from datetime import date, datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


# ------------------- Question Bank & Questions -------------------
class QuestionBankCreate(BaseModel):
    institute_id: uuid.UUID
    code: str = Field(..., min_length=2, max_length=32)
    name: str = Field(..., min_length=2, max_length=150)
    description: Optional[str] = None
    subject_id: Optional[uuid.UUID] = None


class QuestionBankResponse(QuestionBankCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    is_active: bool
    created_at: datetime


class QuestionCategoryCreate(BaseModel):
    question_bank_id: uuid.UUID
    code: str = Field(..., min_length=2, max_length=32)
    name: str = Field(..., min_length=2, max_length=120)


class QuestionCategoryResponse(QuestionCategoryCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime


class QuestionTopicCreate(BaseModel):
    category_id: uuid.UUID
    name: str = Field(..., min_length=2, max_length=150)


class QuestionTopicResponse(QuestionTopicCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime


class QuestionTagCreate(BaseModel):
    institute_id: uuid.UUID
    tag_name: str = Field(..., min_length=2, max_length=48)


class QuestionTagResponse(QuestionTagCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime


class QuestionVersionCreate(BaseModel):
    topic_id: uuid.UUID
    question_code: str = Field(..., min_length=2, max_length=48)
    question_type: str = "MCQ" # MCQ, MSQ, TRUE_FALSE, NUMERICAL, FILL_BLANKS, PROGRAMMING, AUDIO_COMPREHENSION, ESSAY
    difficulty_level: str = "MEDIUM" # EASY, MEDIUM, HARD, EXPERT
    bloom_level: str = "UNDERSTAND"
    language: str = "English" # English, Hindi, etc.
    question_text: str = Field(..., min_length=3)
    latex_equations: List[str] = Field(default_factory=list)
    programming_metadata: Dict[str, Any] = Field(default_factory=dict) # language, starter_code, test_cases
    options: List[Dict[str, Any]] = Field(default_factory=list)
    correct_answers: List[Any] = Field(default_factory=list)
    explanation: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    default_marks: float = Field(1.0, gt=0.0)
    negative_marks: float = Field(0.25, ge=0.0)


class QuestionVersionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    topic_id: uuid.UUID
    question_code: str
    question_type: str
    difficulty_level: str
    bloom_level: str
    language: str
    question_text: str
    latex_equations_json: List[str] = Field(default_factory=list)
    programming_metadata_json: Dict[str, Any] = Field(default_factory=dict)
    options_json: List[Dict[str, Any]] = Field(default_factory=list)
    correct_answers_json: List[Any] = Field(default_factory=list)
    explanation: Optional[str] = None
    tags_json: List[str] = Field(default_factory=list)
    default_marks: float
    negative_marks: float
    approval_status: str
    is_active: bool
    created_at: datetime


# ------------------- Phase 3 Module 4: Test Builder & Blueprint Schemas -------------------
class SectionBlueprintItem(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    duration_minutes: Optional[int] = None
    total_questions: int = Field(10, gt=0)
    marks_per_question: float = Field(2.0, gt=0.0)
    negative_marks: float = Field(0.5, ge=0.0)
    partial_marking: bool = False
    selection_mode: str = Field("FIXED", description="FIXED, POOL_RANDOM")
    question_ids: List[str] = Field(default_factory=list)
    pool_id: Optional[str] = None
    pool_rules: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ExamTemplateCreate(BaseModel):
    institute_id: uuid.UUID
    title: str = Field(..., min_length=3, max_length=180)
    duration_minutes: int = Field(60, gt=0)
    total_marks: float = Field(100.0, gt=0.0)
    passing_marks: float = Field(40.0, gt=0.0)
    allow_calculator: bool = False
    shuffle_questions: bool = True
    shuffle_options: bool = True
    allow_offline_sync: bool = True
    sections: List[SectionBlueprintItem] = Field(default_factory=list)
    instructions: Optional[str] = None


class ExamTemplateUpdate(BaseModel):
    title: Optional[str] = None
    duration_minutes: Optional[int] = None
    total_marks: Optional[float] = None
    passing_marks: Optional[float] = None
    allow_calculator: Optional[bool] = None
    shuffle_questions: Optional[bool] = None
    shuffle_options: Optional[bool] = None
    allow_offline_sync: Optional[bool] = None
    sections: Optional[List[SectionBlueprintItem]] = None
    instructions: Optional[str] = None


class ExamTemplateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    institute_id: uuid.UUID
    title: str
    duration_minutes: int
    total_marks: float
    passing_marks: float
    allow_calculator: bool
    shuffle_questions: bool
    shuffle_options: bool
    allow_offline_sync: bool
    sections_json: List[Dict[str, Any]] = Field(default_factory=list)
    instructions: Optional[str] = None
    created_at: datetime


class QuestionPoolCreate(BaseModel):
    institute_id: uuid.UUID
    name: str = Field(..., min_length=3, max_length=150)
    description: Optional[str] = None
    selection_rules: Dict[str, Any] = Field(default_factory=dict) # topic_id, difficulty_distribution, tags


class QuestionPoolResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    institute_id: uuid.UUID
    name: str
    description: Optional[str] = None
    selection_rules_json: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


class RandomizationPreviewRequest(BaseModel):
    template_id: uuid.UUID
    candidate_seed: int = Field(12345, description="Deterministic seed e.g. hash of user_id + session_id")
    shuffle_options: bool = True


class RandomizationPreviewResponse(BaseModel):
    candidate_seed: int
    template_title: str
    duration_minutes: int
    total_sections: int
    total_questions: int
    total_marks: float
    sections_preview: List[Dict[str, Any]]


class CBTSessionCreate(BaseModel):
    institute_id: uuid.UUID
    template_id: uuid.UUID
    exam_subject_id: Optional[uuid.UUID] = None # Sync to Module 11 ExamSubject
    session_code: str = Field(..., min_length=3, max_length=48)
    start_window: datetime
    end_window: datetime
    delivery_mode: str = "ONLINE" # ONLINE, LAN, OFFLINE, HYBRID


class CBTSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    session_code: str
    delivery_mode: str
    status: str
    start_window: datetime
    end_window: datetime
    created_at: datetime


# ------------------- Candidate Interface & Answers -------------------
class CandidateStartSessionRequest(BaseModel):
    cbt_session_id: uuid.UUID
    student_id: uuid.UUID
    device_fingerprint: Optional[str] = None
    ip_address: Optional[str] = None


class CandidateSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    cbt_session_id: uuid.UUID
    student_id: uuid.UUID
    remaining_seconds: int
    status: str
    total_score: float
    marks_synced_to_module11: bool
    created_at: datetime


class SaveAnswerItem(BaseModel):
    question_id: uuid.UUID
    selected_options: List[Any] = Field(default_factory=list)
    text_answer: Optional[str] = None
    is_marked_for_review: bool = False
    time_spent_seconds: int = Field(0, ge=0)


class OfflineBatchSyncRequest(BaseModel):
    candidate_session_id: uuid.UUID
    answers: List[SaveAnswerItem]
    checksum: str = Field(..., min_length=10)


# ------------------- Dashboard & Live Monitoring -------------------
class LiveCandidateStatus(BaseModel):
    candidate_session_id: uuid.UUID
    student_id: uuid.UUID
    student_name: str
    roll_number: str
    current_question_index: int
    answered_count: int
    remaining_seconds: int
    status: str
    warnings_count: int


class CBTDashboardSummary(BaseModel):
    total_questions_in_bank: int
    active_cbt_sessions_count: int
    live_active_candidates_count: int
    total_exams_delivered_today: int
    offline_syncs_processed: int
    average_candidate_score: float
    recent_sessions: List[Dict[str, Any]]


# ------------------- Phase 3 Module 1: CBT Foundation Schemas -------------------
class CBTGlobalConfigBase(BaseModel):
    system_title: str = "MY EDUCATION INDIA Enterprise CBT System"
    active_environment: str = "HYBRID"  # ONLINE, LAN, OFFLINE, HYBRID
    ntp_server: str = "time.google.com"
    time_sync_tolerance_seconds: int = 2
    browser_lockdown_strict: bool = True
    min_browser_versions_json: Dict[str, int] = Field(default_factory=lambda: {"Chrome": 110, "Edge": 110, "Firefox": 115, "Safari": 16})
    allowed_os_list_json: List[str] = Field(default_factory=lambda: ["Windows 10", "Windows 11", "macOS", "Ubuntu Linux", "Fedora Linux"])
    fullscreen_enforced: bool = True
    tab_switch_limit: int = 3
    clipboard_blocked: bool = True
    right_click_blocked: bool = True
    screen_capture_blocked: bool = True
    auto_save_interval_seconds: int = 3
    heartbeat_interval_seconds: int = 5
    offline_sync_batch_size: int = 10
    offline_storage_retention_days: int = 30
    disconnection_grace_seconds: int = 300
    calculator_allowed_global: bool = False
    exam_policy_html: Optional[str] = None


class CBTGlobalConfigCreate(CBTGlobalConfigBase):
    institute_id: uuid.UUID


class CBTGlobalConfigUpdate(BaseModel):
    system_title: Optional[str] = None
    active_environment: Optional[str] = None
    ntp_server: Optional[str] = None
    time_sync_tolerance_seconds: Optional[int] = None
    browser_lockdown_strict: Optional[bool] = None
    min_browser_versions_json: Optional[Dict[str, int]] = None
    allowed_os_list_json: Optional[List[str]] = None
    fullscreen_enforced: Optional[bool] = None
    tab_switch_limit: Optional[int] = None
    clipboard_blocked: Optional[bool] = None
    right_click_blocked: Optional[bool] = None
    screen_capture_blocked: Optional[bool] = None
    auto_save_interval_seconds: Optional[int] = None
    heartbeat_interval_seconds: Optional[int] = None
    offline_sync_batch_size: Optional[int] = None
    offline_storage_retention_days: Optional[int] = None
    disconnection_grace_seconds: Optional[int] = None
    calculator_allowed_global: Optional[bool] = None
    exam_policy_html: Optional[str] = None


class CBTGlobalConfigResponse(CBTGlobalConfigBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    institute_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class TimeSyncResponse(BaseModel):
    server_time_utc: datetime
    server_time_ist: str
    server_timestamp_ms: int
    ntp_server: str
    tolerance_seconds: int
    environment: str


# ------------------- Phase 3 Module 3: Question Workflow Schemas -------------------
class QuestionWorkflowTransitionRequest(BaseModel):
    target_status: str = Field(..., description="DRAFT, REVIEW, EXPERT_REVIEW, APPROVED, PUBLISHED, REJECTED")
    action: str = Field("TRANSITION", description="SUBMIT_REVIEW, APPROVE_REVIEW, SUBMIT_EXPERT, APPROVE_FINAL, PUBLISH, REJECT, ROLLBACK")
    actor_role: str = Field("AUTHOR", description="AUTHOR, REVIEWER, SUBJECT_EXPERT, EXAM_CONTROLLER")
    comments: Optional[str] = None


class QuestionWorkflowAuditResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    question_id: uuid.UUID
    from_status: str
    to_status: str
    action: str
    actor_user_id: uuid.UUID
    actor_role: str
    comments: Optional[str]
    timestamp: datetime


class QuestionFeedbackCreate(BaseModel):
    review_type: str = Field("PEER_REVIEW", description="PEER_REVIEW, EXPERT_VETTING")
    verdict: str = Field("APPROVED", description="APPROVED, REVISION_NEEDED, REJECTED")
    feedback_notes: Optional[str] = None
    rubric_scores: Dict[str, Any] = Field(default_factory=dict)


class QuestionFeedbackResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    question_id: uuid.UUID
    reviewer_user_id: uuid.UUID
    review_type: str
    verdict: str
    feedback_notes: Optional[str]
    rubric_scores_json: Dict[str, Any]
    created_at: datetime


class QuestionVersionCloneRequest(BaseModel):
    changelog: Optional[str] = "Incremented revision for updated options / LaTeX formula"


# ------------------- Phase 3 Module 5: Candidate Management Schemas -------------------
class CBTCandidateRegisterRequest(BaseModel):
    institute_id: uuid.UUID
    cbt_session_id: uuid.UUID
    user_id: uuid.UUID
    candidate_type: str = Field("INTERNAL_STUDENT", description="INTERNAL_STUDENT, EXTERNAL_APPLICANT")
    application_number: Optional[str] = None
    identity_document_type: str = Field("Aadhaar Card", description="Aadhaar Card, Voter ID, Passport")
    identity_document_number: str = Field("XXXXXXXX1234", description="Government document reference")


class BatchCenterAllocationRequest(BaseModel):
    center_name: str = Field("MEI Central Campus Testing Center", min_length=3)
    center_code: str = Field("TC-IND-01", min_length=2)
    batch_code: str = Field("SHIFT-1-MORNING", min_length=2)
    allocated_lab: str = Field("Computer Lab 1", min_length=2)
    seat_number: str = Field("DESK-01", min_length=2)
    reporting_time: str = Field("08:30 AM IST")
    gate_closing_time: str = Field("09:15 AM IST")


class CandidateVerificationRequest(BaseModel):
    verification_status: str = Field("VERIFIED", description="PENDING, VERIFIED, REJECTED, FLAGGED")
    biometric_verified: bool = True
    is_present: bool = True
    notes: Optional[str] = None


class CBTCandidateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    institute_id: uuid.UUID
    cbt_session_id: uuid.UUID
    user_id: uuid.UUID
    candidate_type: str
    roll_number: str
    application_number: str
    admit_card_number: str
    center_name: str
    center_code: str
    batch_code: str
    allocated_lab: str
    seat_number: str
    reporting_time: str
    gate_closing_time: str
    verification_status: str
    identity_document_type: str
    identity_document_number: str
    biometric_verified: bool
    admit_card_downloaded: bool
    is_present: bool
    created_at: datetime


class AdmitCardResponse(BaseModel):
    admit_card_number: str
    roll_number: str
    candidate_name: str
    exam_title: str
    session_code: str
    start_window: datetime
    center_name: str
    center_code: str
    batch_code: str
    allocated_lab: str
    seat_number: str
    reporting_time: str
    gate_closing_time: str
    admit_card_html: str


# ------------------- Phase 3 Module 6: Exam Scheduling Schemas -------------------
class ExamCenterCreate(BaseModel):
    institute_id: uuid.UUID
    center_code: str = Field(..., min_length=2, max_length=32)
    name: str = Field(..., min_length=3, max_length=180)
    city: str = Field("Indore", max_length=80)
    state: str = Field("Madhya Pradesh", max_length=80)
    address: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    total_workstations: int = Field(250, gt=0)
    buffer_capacity_percentage: int = Field(10, ge=0, le=50)


class ExamCenterResponse(ExamCenterCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    is_active: bool
    created_at: datetime


class ExamLabCreate(BaseModel):
    center_id: uuid.UUID
    lab_code: str = Field(..., min_length=2, max_length=32)
    name: str = Field(..., min_length=2, max_length=100)
    floor: str = Field("Ground Floor", max_length=32)
    capacity: int = Field(60, gt=0)
    is_lan_enabled: bool = True


class ExamLabResponse(ExamLabCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    is_active: bool
    created_at: datetime


class ExamShiftCreate(BaseModel):
    cbt_session_id: uuid.UUID
    shift_code: str = Field("SHIFT-1-MORNING", max_length=32)
    shift_name: str = Field("Morning Shift", max_length=100)
    exam_date: date
    reporting_time: str = Field("08:30 AM IST")
    gate_closing_time: str = Field("09:15 AM IST")
    start_time: str = Field("09:30 AM IST")
    end_time: str = Field("12:30 PM IST")


class ExamShiftResponse(ExamShiftCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    total_allocated_candidates: int
    conflict_holiday_flag: bool
    reminder_dispatched: bool
    created_at: datetime


class ExamScheduleCalendarEvent(BaseModel):
    id: uuid.UUID
    cbt_session_id: uuid.UUID
    shift_code: str
    shift_name: str
    exam_date: date
    start_time: str
    end_time: str
    reporting_time: str
    session_code: str
    template_title: str
    allocated_candidates: int
    is_holiday_collision: bool
    holiday_name: Optional[str] = None


# ------------------- Phase 3 Module 7: Live Examination Engine Schemas -------------------
class CBTHeartbeatRequest(BaseModel):
    candidate_session_id: uuid.UUID
    current_question_index: int = 0
    elapsed_seconds: int = 5
    is_fullscreen: bool = True
    tab_switches_detected: int = 0


class CBTHeartbeatResponse(BaseModel):
    candidate_session_id: uuid.UUID
    remaining_seconds: int
    server_time: datetime
    status: str
    is_expired: bool
    current_question_index: int
    message: Optional[str] = None


class LiveQuestionOption(BaseModel):
    id: str
    label: str
    content: str


class LiveQuestionItem(BaseModel):
    id: uuid.UUID
    question_number: int
    section_name: str
    question_type: str = "MCQ"
    content: str
    options: List[LiveQuestionOption] = Field(default_factory=list)
    languages_content: Dict[str, Any] = Field(default_factory=dict)
    marks: float = 2.0
    negative_marks: float = 0.5
    allow_partial_marking: bool = False
    is_calculator_allowed: bool = True


class LiveCandidateAnswerState(BaseModel):
    question_id: uuid.UUID
    selected_options: List[Any] = Field(default_factory=list)
    text_answer: Optional[str] = None
    is_marked_for_review: bool = False
    status: str = "NOT_VISITED"
    time_spent_seconds: int = 0
    last_saved_at: Optional[datetime] = None


class LiveExamSessionBundle(BaseModel):
    candidate_session_id: uuid.UUID
    cbt_session_id: uuid.UUID
    student_id: uuid.UUID
    candidate_name: str
    roll_number: str
    exam_title: str
    exam_code: str
    total_questions: int
    duration_minutes: int
    remaining_seconds: int
    server_time: datetime
    calculator_allowed: bool = True
    supported_languages: List[str] = Field(default_factory=lambda: ["en", "hi"])
    sections: List[str] = Field(default_factory=list)
    questions: List[LiveQuestionItem] = Field(default_factory=list)
    answers: Dict[str, LiveCandidateAnswerState] = Field(default_factory=dict)
    current_question_index: int = 0
    status: str = "IN_PROGRESS"


class AutosaveSingleAnswerRequest(BaseModel):
    candidate_session_id: uuid.UUID
    question_id: uuid.UUID
    selected_options: List[Any] = Field(default_factory=list)
    text_answer: Optional[str] = None
    is_marked_for_review: bool = False
    time_spent_seconds: int = 0


class SubmitLiveExamRequest(BaseModel):
    candidate_session_id: uuid.UUID
    submission_reason: str = Field("MANUAL")
    feedback: Optional[str] = None


class ClearResponseRequest(BaseModel):
    candidate_session_id: uuid.UUID
    question_id: uuid.UUID


class ToggleReviewRequest(BaseModel):
    candidate_session_id: uuid.UUID
    question_id: uuid.UUID
    is_marked_for_review: bool


# ------------------- Phase 3 Module 8: Security & Proctoring Schemas -------------------
class SecurityViolationReportRequest(BaseModel):
    candidate_session_id: uuid.UUID
    incident_type: str = Field(..., description="TAB_SWITCH, FULLSCREEN_EXIT, CLIPBOARD_COPY, RIGHT_CLICK, DEVTOOLS_OPEN, MULTIPLE_FACES, NO_FACE")
    severity: str = Field("MEDIUM", description="LOW, MEDIUM, HIGH, CRITICAL")
    details: Optional[str] = None
    current_question_index: int = 0


class SecurityViolationReportResponse(BaseModel):
    id: uuid.UUID
    candidate_session_id: uuid.UUID
    incident_type: str
    warning_index: int
    max_warnings_allowed: int = 3
    action_taken: str  # "WARNED", "DISQUALIFIED", "LOGGED"
    proctor_status: str
    message: str


class ProctorIssueWarningRequest(BaseModel):
    candidate_session_id: uuid.UUID
    message_text: str = Field(..., min_length=3, max_length=500)


class ProctorActionRequest(BaseModel):
    candidate_session_id: uuid.UUID
    reason: str = Field("Administrative Decision", min_length=3, max_length=255)


class ProctorActionResponse(BaseModel):
    status: str
    candidate_session_id: uuid.UUID
    proctor_status: str
    message: str


class LiveProctorCandidateItem(BaseModel):
    candidate_session_id: uuid.UUID
    student_id: uuid.UUID
    student_name: str
    roll_number: str
    terminal_id: str
    current_question_index: int
    answered_count: int
    warnings_count: int
    proctor_status: str  # NORMAL, WARNING, UNDER_SCRUTINY, DISQUALIFIED
    is_fullscreen_locked: bool
    webcam_verified: bool
    screen_active: bool
    last_heartbeat_at: Optional[datetime]
    recent_incident: Optional[str] = None


class LiveProctorDashboardResponse(BaseModel):
    cbt_session_id: uuid.UUID
    session_name: str
    center_name: str
    total_active_candidates: int
    flagged_candidates_count: int
    disqualified_count: int
    candidates: List[LiveProctorCandidateItem]
    recent_incidents: List[Dict[str, Any]]


# ------------------- Phase 3 Module 9: Evaluation Engine Schemas -------------------
class EvaluationExecutionRequest(BaseModel):
    cbt_session_id: uuid.UUID
    evaluation_type: str = Field("OBJECTIVE_AUTO", description="OBJECTIVE_AUTO, MODERATED, MANUAL_HYBRID")
    apply_negative_marking: bool = True
    apply_partial_marking: bool = True
    passing_cutoff_percentage: float = Field(40.0, ge=0.0, le=100.0)


class EvaluationSummaryResponse(BaseModel):
    evaluation_run_id: uuid.UUID
    cbt_session_id: uuid.UUID
    total_candidates_evaluated: int
    average_raw_score: float
    average_moderated_score: float
    highest_score: float
    lowest_score: float
    pass_percentage: float
    status: str
    created_at: datetime


class GraceMarksApplyRequest(BaseModel):
    cbt_session_id: uuid.UUID
    question_id: Optional[uuid.UUID] = None
    rule_type: str = Field("DISPUTED_QUESTION_BONUS", description="DISPUTED_QUESTION_BONUS, BORDERLINE_PASS_ADJUSTMENT, SYSTEM_COMPENSATION")
    grace_marks: float = Field(2.0, ge=0.5, le=10.0)
    reason: str = Field(..., min_length=5, max_length=255)


class ResultModerationRequest(BaseModel):
    cbt_session_id: uuid.UUID
    moderation_strategy: str = Field("PERCENTAGE_SCALING", description="PERCENTAGE_SCALING, NORMALIZATION_CURVE, BORDERLINE_PASS_ADJUSTMENT")
    adjustment_value: float = Field(5.0, description="Percentage boost or raw point adjustment")
    notes: Optional[str] = None


class CandidateScoreDetailItem(BaseModel):
    candidate_session_id: uuid.UUID
    student_id: uuid.UUID
    student_name: str
    roll_number: str
    total_attempted: int
    correct_count: int
    incorrect_count: int
    raw_score: float
    negative_deductions: float
    partial_marks_earned: float
    grace_marks: float
    moderated_score: float
    percentile: float
    rank: int
    is_passed: bool
    status: str
    synced_to_module11: bool


class EvaluationSessionRosterResponse(BaseModel):
    cbt_session_id: uuid.UUID
    session_title: str
    evaluation_status: str
    summary: EvaluationSummaryResponse
    candidates: List[CandidateScoreDetailItem]


# ------------------- Phase 3 Module 10: Results & Analytics Schemas -------------------
class SubjectProficiencyItem(BaseModel):
    subject_name: str
    total_questions: int
    attempted: int
    correct: int
    score: float
    max_score: float
    accuracy: float
    percentile_in_subject: float


class TopicProficiencyItem(BaseModel):
    topic_name: str
    subject_name: str
    mastery_percentage: float
    proficiency_status: str  # "STRENGTH", "AVERAGE", "IMPROVEMENT_AREA"
    recommended_action: str


class DifficultyBreakdownItem(BaseModel):
    difficulty_level: str  # "EASY", "MODERATE", "HARD"
    total_questions: int
    accuracy_percentage: float
    average_time_seconds: float
    discrimination_index: float


class TimePacingAnalysisItem(BaseModel):
    avg_time_per_question_seconds: float
    avg_time_correct_questions_seconds: float
    avg_time_incorrect_questions_seconds: float
    pace_status: str  # "OPTIMAL_PACE", "RUSHED", "LINGERING"
    time_efficiency_rating: str


class CandidateScorecardResponse(BaseModel):
    candidate_session_id: uuid.UUID
    student_id: uuid.UUID
    candidate_name: str
    roll_number: str
    session_title: str
    exam_date: str
    national_rank: int
    total_candidates: int
    percentile: float
    raw_score: float
    negative_deductions: float
    grace_marks: float
    final_score: float
    max_possible_score: float
    accuracy_percentage: float
    speed_questions_per_minute: float
    total_time_spent_minutes: float
    is_passed: bool
    result_status: str
    subject_breakdowns: List[SubjectProficiencyItem]
    topic_insights: List[TopicProficiencyItem]
    time_pacing_analysis: TimePacingAnalysisItem
    difficulty_breakdown: List[DifficultyBreakdownItem]


class ComparativeCohortAnalyticsResponse(BaseModel):
    cbt_session_id: uuid.UUID
    session_title: str
    total_appeared: int
    mean_score: float
    median_score: float
    standard_deviation: float
    highest_score: float
    lowest_score: float
    percentile_90_cutoff: float
    percentile_75_cutoff: float
    percentile_50_cutoff: float
    score_distribution_bands: List[Dict[str, Any]]
    subject_averages: Dict[str, float]


class AnalyticsExportRequest(BaseModel):
    cbt_session_id: uuid.UUID
    export_format: str = Field("CSV", description="CSV, JSON, PDF")
    include_item_analysis: bool = True


class AnalyticsExportResponse(BaseModel):
    download_url: str
    export_format: str
    record_count: int
    generated_at: datetime


# ------------------- Phase 3 Module 11: Certificate Integration Schemas -------------------
class CBTCertificateIssueRequest(BaseModel):
    candidate_session_id: uuid.UUID
    certificate_type: str = Field("MERIT_SCHOLARSHIP", description="MERIT_SCHOLARSHIP, PARTICIPATION, COURSE_COMPLETION")
    template_id: Optional[uuid.UUID] = None
    custom_title: Optional[str] = None


class CBTCertificateBatchIssueRequest(BaseModel):
    cbt_session_id: uuid.UUID
    min_score_cutoff: float = Field(8.0, ge=0.0)
    certificate_type: str = Field("MERIT_SCHOLARSHIP")


class CBTCertificateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    cbt_session_id: uuid.UUID
    candidate_session_id: uuid.UUID
    erp_certificate_id: uuid.UUID
    certificate_number: str
    verification_code: str
    hmac_signature: str
    certificate_type: str
    candidate_name: str
    roll_number: str
    score: float
    rank: int
    percentile: float
    pdf_download_url: str
    qr_payload_url: str
    email_dispatched: bool
    email_dispatched_at: Optional[datetime] = None
    created_at: datetime


class CBTPublicVerificationLookupResponse(BaseModel):
    is_valid: bool
    certificate_number: str
    verification_code: str
    candidate_name: str
    roll_number: str
    exam_title: str
    issue_date: str
    score: float
    rank: int
    percentile: float
    institution: str = "MY EDUCATION INDIA Autonomous Campus, Indore"
    hmac_verified: bool = True
    qr_verify_url: str


# ------------------- Phase 3 Module 12: Candidate Portal Schemas -------------------
class CandidatePortalScheduleCard(BaseModel):
    session_id: uuid.UUID
    session_title: str
    session_code: str
    exam_date: str
    shift_code: str
    reporting_time: str
    gate_closing_time: str
    start_time: str
    end_time: str
    center_name: str
    allocated_lab: str
    seat_number: str
    admit_card_available: bool
    exam_status: str  # "UPCOMING", "LIVE_NOW", "COMPLETED"
    can_launch_exam: bool


class CandidatePortalDashboardResponse(BaseModel):
    student_id: uuid.UUID
    student_name: str
    roll_number: str
    application_number: str
    admit_card_number: str
    center_name: str
    seat_number: str
    upcoming_schedules: List[CandidatePortalScheduleCard]
    active_exam_session_id: Optional[uuid.UUID] = None
    has_published_results: bool
    scorecard_summary: Optional[Dict[str, Any]] = None
    certificates_count: int
    open_tickets_count: int


class CandidateTicketCreateRequest(BaseModel):
    cbt_session_id: Optional[uuid.UUID] = None
    category: str = Field("ADMIT_CARD_DISCREPANCY", description="ADMIT_CARD_DISCREPANCY, SCHEDULE_CHANGE, TERMINAL_TECHNICAL_ISSUE, SCORE_RE_EVALUATION, OTHER")
    subject: str = Field(..., min_length=4, max_length=180)
    description: str = Field(..., min_length=10)
    priority: str = Field("MEDIUM", description="LOW, MEDIUM, HIGH, URGENT")


class CandidateTicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    ticket_number: str
    cbt_session_id: Optional[uuid.UUID] = None
    student_id: uuid.UUID
    category: str
    subject: str
    description: str
    priority: str
    status: str
    resolution_notes: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime


# ------------------- Phase 3 Module 13: Mock Test Platform Schemas -------------------
class MockTestSeriesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    series_code: str
    title: str
    description: str
    category: str
    subject_name: Optional[str] = None
    total_questions: int
    duration_minutes: int
    is_free: bool
    is_active: bool
    registered_count: int
    created_at: datetime


class MockTestRegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    email: str = Field(..., min_length=5, max_length=120)
    phone_number: str = Field(..., min_length=10, max_length=15)
    target_exam: str = Field("ENGINEERING_ENTRANCE_2026")
    city: str = Field("Indore")
    series_id: Optional[uuid.UUID] = None


class MockAttemptResponse(BaseModel):
    id: uuid.UUID
    series_id: uuid.UUID
    series_title: str
    score: float
    max_score: float
    accuracy_percentage: float
    time_spent_seconds: int
    percentile: float
    rank: int
    attempted_at: datetime


class PublicLeaderboardItem(BaseModel):
    rank: int
    student_id: uuid.UUID
    candidate_name: str
    roll_number: str
    score: float
    accuracy: float
    time_spent_seconds: int
    percentile: float
    institute_badge: str
    achieved_at: datetime


class PublicLeaderboardResponse(BaseModel):
    series_id: uuid.UUID
    series_title: str
    total_participants: int
    top_entries: List[PublicLeaderboardItem]


class PracticeChapterWiseItem(BaseModel):
    chapter_id: str
    chapter_name: str
    difficulty: str
    total_questions: int
    estimated_time_minutes: int
    attempted_count: int


class PracticeSubjectCategoryResponse(BaseModel):
    subject_name: str
    total_chapters: int
    total_questions: int
    chapters: List[PracticeChapterWiseItem]


# ------------------- Phase 3 Module 14: CBT Administration Schemas -------------------
class CBTDeviceHealthResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    lab_id: uuid.UUID
    terminal_code: str
    ip_address: str
    mac_address: Optional[str] = None
    os_version: str
    browser_version: str
    cpu_load_percentage: float
    ram_usage_percentage: float
    ping_latency_ms: int
    kiosk_mode_locked: bool
    webcam_ready: bool
    status: str
    last_heartbeat: datetime


class SystemDiagnosticRequest(BaseModel):
    center_id: uuid.UUID
    lab_id: Optional[uuid.UUID] = None
    test_bandwidth: bool = True
    test_ntp_sync: bool = True
    test_webrtc_camera: bool = True


class SystemDiagnosticResponse(BaseModel):
    id: uuid.UUID
    center_id: uuid.UUID
    lab_id: Optional[uuid.UUID] = None
    bandwidth_download_mbps: float
    bandwidth_upload_mbps: float
    ntp_time_drift_ms: float
    lan_packet_loss_percentage: float
    webrtc_stun_passed: bool
    overall_readiness_status: str  # "PASSED", "WARNING", "FAILED"
    diagnostic_details: str
    executed_at: datetime


class CBTIncidentCreateRequest(BaseModel):
    center_id: uuid.UUID
    lab_id: Optional[uuid.UUID] = None
    terminal_code: Optional[str] = None
    severity: str = Field("MEDIUM", description="LOW, MEDIUM, HIGH, CRITICAL")
    category: str = Field("HARDWARE_FAILURE", description="HARDWARE_FAILURE, NETWORK_OUTAGE, POWER_DISRUPTION, SECURITY_MALPRACTICE, INVIGILATOR_REPORT")
    description: str = Field(..., min_length=5)


class CBTIncidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    incident_code: str
    center_id: uuid.UUID
    lab_id: Optional[uuid.UUID] = None
    terminal_code: Optional[str] = None
    severity: str
    category: str
    description: str
    status: str
    resolution_summary: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime


class CapacityPlanningMatrixResponse(BaseModel):
    center_id: uuid.UUID
    center_name: str
    center_code: str
    total_physical_workstations: int
    buffer_capacity_count: int
    net_allocatable_capacity: int
    total_labs_count: int
    active_shifts_scheduled: int
    concurrent_capacity_limit: int
    lab_utilization_breakdown: List[Dict[str, Any]]


# ------------------- Phase 3 Module 15: Reports & Monitoring Schemas -------------------
class AttendanceReportItem(BaseModel):
    student_id: uuid.UUID
    student_name: str
    roll_number: str
    center_code: str
    lab_name: str
    seat_number: str
    status: str  # "PRESENT", "ABSENT", "LATE"
    reporting_time_logged: str
    biometric_verified: bool


class AttendanceSummaryResponse(BaseModel):
    session_title: str
    shift_code: str
    total_registered: int
    total_present: int
    total_absent: int
    attendance_percentage: float
    records: List[AttendanceReportItem]


class InvigilatorDutyReportItem(BaseModel):
    id: uuid.UUID
    center_name: str
    lab_name: str
    shift_code: str
    invigilator_name: str
    role: str
    reporting_status: str
    duty_date: str


class QuestionAuditItemResponse(BaseModel):
    question_number: int
    section_name: str
    question_type: str
    difficulty_index: float  # P-value
    discrimination_index: float  # D-value
    total_attempts: int
    correct_count: int
    accuracy_percentage: float
    distracter_efficiency: str


class SystemTelemetryReportResponse(BaseModel):
    center_name: str
    peak_concurrency_workstations: int
    average_latency_ms: float
    bandwidth_consumption_gb: float
    packet_loss_rate: float
    ntp_time_drift_ms: float
    uptime_percentage: float


class SecurityAuditSummaryResponse(BaseModel):
    total_violations_recorded: int
    tab_switches_count: int
    fullscreen_exits_count: int
    clipboard_attempts_count: int
    disqualifications_count: int
    recent_incidents: List[Dict[str, Any]]


class CBTComprehensiveReportBundleResponse(BaseModel):
    session_id: uuid.UUID
    session_title: str
    attendance: AttendanceSummaryResponse
    invigilators: List[InvigilatorDutyReportItem]
    question_audit: List[QuestionAuditItemResponse]
    system_telemetry: SystemTelemetryReportResponse
    security_audit: SecurityAuditSummaryResponse


# ------------------- Phase 3 Module 16: Enterprise Integrations Schemas -------------------
class IntegrationSurfaceItem(BaseModel):
    surface_name: str
    service_endpoint: str
    auth_mechanism: str
    health_status: str  # "HEALTHY", "DEGRADED", "SYNCHRONIZED"
    last_heartbeat_at: datetime
    total_events_dispatched: int
    active_sync_enabled: bool
    description: str


class IntegrationTopologyResponse(BaseModel):
    system_name: str = "MY EDUCATION INDIA Enterprise CBT Engine"
    platform_version: str = "3.0.0-ENTERPRISE-PHASE3"
    total_connected_services: int
    overall_connectivity_health: str  # "100% OPERATIONAL", "PARTIAL_SYNC"
    surfaces: List[IntegrationSurfaceItem]


class LMSSyncAssessmentRequest(BaseModel):
    cbt_session_id: uuid.UUID
    course_id: uuid.UUID
    competency_codes: List[str] = Field(default_factory=lambda: ["COMP-CS-ALGO-01", "COMP-MATH-LA-02"])


class LMSSyncAssessmentResponse(BaseModel):
    status: str
    course_id: uuid.UUID
    cbt_session_id: uuid.UUID
    synced_competencies_count: int
    synced_students_count: int
    synced_at: datetime


class WebhookDispatchTestRequest(BaseModel):
    surface_name: str = Field("API_GATEWAY", description="PHASE1_WEBSITE, NOTIFICATION_CENTER, etc.")
    payload_event: str = Field("EXAM_SESSION_SCHEDULED")


class WebhookDispatchTestResponse(BaseModel):
    status: str
    surface_name: str
    latency_ms: int
    dispatched_at: datetime
    acknowledgement_id: str
