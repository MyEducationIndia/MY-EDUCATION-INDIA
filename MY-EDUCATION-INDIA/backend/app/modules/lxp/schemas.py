"""
Module 15: LXP Pydantic Schemas (Pydantic v2 / v1 compatible)
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field

class LearningCourseBase(BaseModel):
    course_code: str = Field(..., max_length=50)
    course_name: str = Field(..., max_length=255)
    description: Optional[str] = None
    category: str = Field(..., max_length=100)
    difficulty: str = "BEGINNER"
    language: str = "English"
    duration_minutes: int = 0
    thumbnail_url: Optional[str] = None
    banner_url: Optional[str] = None
    instructor_id: str
    department_id: Optional[str] = None
    academic_program_id: Optional[str] = None
    fee_amount: float = 0.0
    certificate_template_id: Optional[str] = None
    status: str = "DRAFT"
    visibility: str = "PUBLIC"
    tags: Optional[List[str]] = None
    is_free: bool = True

class LearningCourseCreate(LearningCourseBase):
    pass

class LearningCourseResponse(LearningCourseBase):
    id: str
    institute_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class LearningModuleCreate(BaseModel):
    course_id: str
    module_title: str = Field(..., max_length=255)
    description: Optional[str] = None
    order_index: int = 1
    duration_minutes: int = 0
    is_published: bool = True

class LearningModuleResponse(LearningModuleCreate):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True

class LearningLessonCreate(BaseModel):
    module_id: str
    lesson_title: str = Field(..., max_length=255)
    lesson_type: str = "VIDEO"
    content_body: Optional[str] = None
    video_id: Optional[str] = None
    duration_seconds: int = 0
    order_index: int = 1
    is_preview: bool = False
    is_mandatory: bool = True

class LearningLessonResponse(LearningLessonCreate):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True

class CourseEnrollmentRequest(BaseModel):
    course_id: str
    student_id: str
    batch_id: Optional[str] = None
    enrollment_type: str = "FREE"

class CourseEnrollmentResponse(BaseModel):
    id: str
    course_id: str
    student_id: str
    enrollment_status: str
    progress_percentage: float
    enrolled_at: datetime

    class Config:
        orm_mode = True

class LessonProgressUpdate(BaseModel):
    enrollment_id: str
    lesson_id: str
    watch_seconds: int = 0
    last_playback_position_seconds: int = 0
    status: str = "IN_PROGRESS" # NOT_STARTED, IN_PROGRESS, COMPLETED
    quiz_score: Optional[float] = None

class AssignmentSubmissionCreate(BaseModel):
    lesson_id: str
    student_id: str
    submission_text: Optional[str] = None
    attachment_url: Optional[str] = None

class AssignmentEvaluationRequest(BaseModel):
    submission_id: str
    evaluator_id: str
    marks_obtained: float
    feedback_text: str
    rubric_scores: Optional[Dict[str, float]] = None

class DiscussionTopicCreate(BaseModel):
    course_id: str
    lesson_id: Optional[str] = None
    user_id: str
    title: str = Field(..., max_length=255)
    content: str

class DiscussionPostCreate(BaseModel):
    topic_id: str
    user_id: str
    content: str
    parent_post_id: Optional[str] = None
    attachment_url: Optional[str] = None

class VideoUploadMetadata(BaseModel):
    title: str = Field(..., max_length=255)
    raw_file_url: str
    duration_seconds: int
    file_size_bytes: int
    thumbnail_url: Optional[str] = None

class LXPDashboardMetrics(BaseModel):
    total_enrolled_courses: int
    active_courses: int
    completed_courses: int
    total_learning_hours: float
    upcoming_assignments_count: int
    average_quiz_score: float
    xp_points: int
    streak_days: int


# ============================================================================
# PHASE 5 MODULE 1: LMS MULTI-ROLE DASHBOARD SCHEMAS
# ============================================================================

class LmsRoleDashboardResponse(BaseModel):
    role: str
    role_title: str
    kpi_cards: Dict[str, Any]
    active_courses: List[Dict[str, Any]] = Field(default_factory=list)
    upcoming_classes: List[Dict[str, Any]] = Field(default_factory=list)
    pending_assignments: List[Dict[str, Any]] = Field(default_factory=list)
    quiz_results: List[Dict[str, Any]] = Field(default_factory=list)
    learning_hours: Dict[str, Any] = Field(default_factory=dict)
    attendance_summary: Dict[str, Any] = Field(default_factory=dict)
    certificates: List[Dict[str, Any]] = Field(default_factory=list)
    notifications: List[Dict[str, Any]] = Field(default_factory=list)
    recent_activity: List[Dict[str, Any]] = Field(default_factory=list)


class LmsDashboardPreferenceUpdate(BaseModel):
    role: str = Field("STUDENT", max_length=32)
    pinned_widgets: List[str] = Field(default_factory=list)


# ============================================================================
# PHASE 5 MODULE 2: LMS COURSE MANAGEMENT SCHEMAS
# ============================================================================

class LmsProgramCreate(BaseModel):
    program_code: str = Field(..., max_length=50)
    program_name: str = Field(..., max_length=255)
    department_id: Optional[str] = None
    degree_level: str = Field("B_TECH", max_length=50)
    total_credits: float = Field(160.0, ge=1.0)
    duration_semesters: int = Field(8, ge=1, le=12)
    description: Optional[str] = None


class LmsProgramResponse(BaseModel):
    id: str
    program_code: str
    program_name: str
    department_id: Optional[str] = None
    degree_level: str
    total_credits: float
    duration_semesters: int
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LmsCourseVersionCreate(BaseModel):
    course_id: str
    version_tag: str = Field("v1.0", max_length=20)
    changelog: Optional[str] = None
    credit_hours: Optional[Dict[str, int]] = None  # {"theory": 3, "tutorial": 1, "practical": 2}
    semester_number: int = Field(5, ge=1, le=12)
    prerequisites: List[str] = Field(default_factory=list)
    learning_outcomes: List[Dict[str, Any]] = Field(default_factory=list)


class LmsCourseVersionResponse(BaseModel):
    id: str
    course_id: str
    version_tag: str
    changelog: Optional[str] = None
    is_active: bool
    credit_hours: Optional[Dict[str, int]] = None
    semester_number: int
    prerequisites: List[str] = Field(default_factory=list)
    learning_outcomes: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LmsLearningPathCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    target_role: str = Field("Cloud & DevOps Architect", max_length=100)
    course_sequence: List[str] = Field(default_factory=list)
    estimated_hours: float = Field(120.0, ge=1.0)
    badge_reward_id: Optional[str] = None


class LmsLearningPathResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    target_role: str
    course_sequence: List[str]
    estimated_hours: float
    badge_reward_id: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True


class LmsCourseBundleCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    bundled_course_ids: List[str] = Field(default_factory=list)
    pricing_tier: str = Field("ENTERPRISE_INSTITUTE", max_length=50)
    is_franchise_eligible: bool = True


class LmsCourseBundleResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    bundled_course_ids: List[str]
    pricing_tier: str
    is_franchise_eligible: bool
    created_at: datetime

    class Config:
        orm_mode = True


# ============================================================================
# PHASE 5 MODULE 3: LMS LESSON BUILDER SCHEMAS
# ============================================================================

class LmsLessonContentCreate(BaseModel):
    lesson_id: str
    content_type: str = Field("RICH_TEXT", max_length=50)  # RICH_TEXT, PDF, PPT, IMAGE, AUDIO, VIDEO, SCORM, HTML5, EXTERNAL_URL, EMBED_IFRAME, H5P_INTERACTIVE, CODE_PLAYGROUND
    title: str = Field(..., max_length=255)
    order_index: int = Field(1, ge=1)
    content_payload: Dict[str, Any] = Field(default_factory=dict)
    is_mandatory: bool = True
    min_completion_time_seconds: int = Field(0, ge=0)
    pass_score_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)


class LmsLessonContentResponse(BaseModel):
    id: str
    lesson_id: str
    content_type: str
    title: str
    order_index: int
    content_payload: Dict[str, Any]
    is_mandatory: bool
    min_completion_time_seconds: int
    pass_score_percentage: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LmsScormPackageCreate(BaseModel):
    title: str = Field(..., max_length=255)
    scorm_version: str = Field("SCORM_1_2", max_length=20)
    package_url: str = Field(..., max_length=500)
    manifest_json: Dict[str, Any] = Field(default_factory=dict)
    launch_url: str = Field(..., max_length=500)
    mastery_score: float = Field(80.0, ge=0.0, le=100.0)


class LmsScormPackageResponse(BaseModel):
    id: str
    title: str
    scorm_version: str
    package_url: str
    manifest_json: Dict[str, Any]
    launch_url: str
    mastery_score: float
    created_at: datetime

    class Config:
        orm_mode = True


class LessonBuilderPreviewResponse(BaseModel):
    lesson_id: str
    lesson_title: str
    total_contents: int
    contents: List[LmsLessonContentResponse]


# ============================================================================
# PHASE 5 MODULE 4: LMS VIDEO LEARNING SCHEMAS
# ============================================================================

class LmsVideoAssetCreate(BaseModel):
    lesson_id: str
    title: str = Field(..., max_length=255)
    video_url: str = Field(..., max_length=500)
    hls_playlist_url: Optional[str] = Field(None, max_length=500)
    duration_seconds: int = Field(0, ge=0)
    resolutions: List[str] = Field(default_factory=lambda: ["1080p", "720p", "480p", "360p"])
    thumbnail_url: Optional[str] = Field(None, max_length=500)
    allow_download: bool = False
    watermark_enabled: bool = True


class LmsVideoAssetResponse(BaseModel):
    id: str
    lesson_id: str
    title: str
    video_url: str
    hls_playlist_url: Optional[str] = None
    duration_seconds: int
    resolutions: List[str]
    thumbnail_url: Optional[str] = None
    allow_download: bool
    watermark_enabled: bool
    created_at: datetime

    class Config:
        orm_mode = True


class LmsVideoPlaybackProgressUpdate(BaseModel):
    student_id: str
    video_id: str
    last_position_seconds: int = Field(0, ge=0)
    total_watched_seconds: int = Field(0, ge=0)
    is_completed: bool = False


class LmsVideoPlaybackSessionResponse(BaseModel):
    id: str
    student_id: str
    video_id: str
    last_position_seconds: int
    total_watched_seconds: int
    is_completed: bool
    completed_at: Optional[datetime] = None
    notes: List[Dict[str, Any]] = Field(default_factory=list)
    bookmarks: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LmsVideoNoteCreate(BaseModel):
    student_id: str
    video_id: str
    timestamp_seconds: int = Field(..., ge=0)
    note_text: str = Field(..., min_length=1)


class LmsVideoBookmarkCreate(BaseModel):
    student_id: str
    video_id: str
    timestamp_seconds: int = Field(..., ge=0)
    label: str = Field(..., min_length=1, max_length=120)


# ============================================================================
# PHASE 5 MODULE 5: LMS LIVE CLASSES SCHEMAS
# ============================================================================

class LmsLiveClassSessionCreate(BaseModel):
    course_id: str
    title: str = Field(..., max_length=255)
    instructor_id: str = Field("inst_01", max_length=36)
    instructor_name: str = Field("Dr. Rajeshwari Sharma", max_length=120)
    platform: str = Field("GOOGLE_MEET", max_length=32)  # ZOOM, GOOGLE_MEET, MS_TEAMS, JITSI
    meeting_url: str = Field(..., max_length=500)
    meeting_id: str = Field(..., max_length=100)
    passcode: Optional[str] = Field(None, max_length=100)
    start_time: datetime
    end_time: datetime
    duration_minutes: int = Field(90, ge=15, le=360)
    enable_chat: bool = True
    enable_polls: bool = True
    enable_whiteboard: bool = True
    enable_breakout_rooms: bool = True


class LmsLiveClassSessionResponse(BaseModel):
    id: str
    course_id: str
    title: str
    instructor_id: str
    instructor_name: str
    platform: str
    meeting_url: str
    meeting_id: str
    passcode: Optional[str] = None
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    status: str
    recording_url: Optional[str] = None
    recording_duration_seconds: Optional[int] = None
    enable_chat: bool
    enable_polls: bool
    enable_whiteboard: bool
    enable_breakout_rooms: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LmsLiveClassAttendanceRecord(BaseModel):
    live_class_id: str
    student_id: str
    roll_number: str = Field(..., max_length=48)
    candidate_name: str = Field(..., max_length=120)
    active_minutes: int = Field(0, ge=0)
    attendance_status: str = Field("PRESENT", max_length=32)  # PRESENT, PARTIAL, ABSENT
    poll_responses_count: int = Field(0, ge=0)
    raised_hand_count: int = Field(0, ge=0)


class LmsLiveClassAttendanceResponse(BaseModel):
    id: str
    live_class_id: str
    student_id: str
    roll_number: str
    candidate_name: str
    joined_at: datetime
    left_at: Optional[datetime] = None
    active_minutes: int
    attendance_status: str
    poll_responses_count: int
    raised_hand_count: int
    created_at: datetime

    class Config:
        orm_mode = True


class LmsLiveClassJoinResponse(BaseModel):
    session_id: str
    title: str
    platform: str
    join_url: str
    meeting_id: str
    passcode: Optional[str] = None
    status: str


# ============================================================================
# PHASE 5 MODULE 6: LMS ASSIGNMENT MANAGEMENT SCHEMAS
# ============================================================================

class LmsAssignmentCreate(BaseModel):
    course_id: str
    title: str = Field(..., max_length=255)
    description: str
    max_score: float = Field(100.0, ge=1.0)
    due_date: datetime
    cut_off_date: Optional[datetime] = None
    late_penalty_per_day_pct: float = Field(5.0, ge=0.0, le=50.0)
    is_group_assignment: bool = False
    max_group_size: int = Field(1, ge=1, le=10)
    allowed_file_types: List[str] = Field(default_factory=lambda: ["pdf", "zip", "go", "py"])
    max_file_size_mb: int = Field(50, ge=1, le=500)
    rubric_schema: List[Dict[str, Any]] = Field(default_factory=list)
    attachment_urls: List[str] = Field(default_factory=list)
    plagiarism_check_enabled: bool = True


class LmsAssignmentResponse(BaseModel):
    id: str
    course_id: str
    title: str
    description: str
    max_score: float
    due_date: datetime
    cut_off_date: Optional[datetime] = None
    late_penalty_per_day_pct: float
    is_group_assignment: bool
    max_group_size: int
    allowed_file_types: List[str]
    max_file_size_mb: int
    rubric_schema: List[Dict[str, Any]]
    attachment_urls: List[str]
    plagiarism_check_enabled: bool
    status: str
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LmsAssignmentSubmissionCreate(BaseModel):
    assignment_id: str
    student_id: str
    roll_number: str = Field(..., max_length=48)
    candidate_name: str = Field(..., max_length=120)
    group_name: Optional[str] = None
    submission_text: Optional[str] = None
    uploaded_files: List[Dict[str, Any]] = Field(default_factory=list)
    is_draft: bool = False


class LmsAssignmentSubmissionResponse(BaseModel):
    id: str
    assignment_id: str
    student_id: str
    roll_number: str
    candidate_name: str
    group_name: Optional[str] = None
    submission_text: Optional[str] = None
    uploaded_files: List[Dict[str, Any]]
    status: str
    submitted_at: Optional[datetime] = None
    is_late: bool
    late_penalty_applied_pct: float
    score_awarded: Optional[float] = None
    rubric_evaluations: Dict[str, Any]
    similarity_score_pct: Optional[float] = None
    evaluator_feedback: Optional[str] = None
    evaluated_by: Optional[str] = None
    evaluated_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LmsAssignmentGradeRequest(BaseModel):
    score_awarded: float = Field(..., ge=0.0)
    rubric_evaluations: Dict[str, Any] = Field(default_factory=dict)
    evaluator_feedback: str = Field(..., min_length=2)
    evaluator_id: str = "inst_01"


# ============================================================================
# Module 7: LMS Quiz & Practice Tests Schemas
# ============================================================================

class LmsQuizConfigCreate(BaseModel):
    course_id: str
    module_id: Optional[str] = None
    title: str = Field(..., min_length=3, max_length=160)
    quiz_type: str = Field(default="PRACTICE_TEST")  # PRACTICE_TEST, CHAPTER_QUIZ, WEEKLY_ASSESSMENT, ADAPTIVE_PRACTICE
    description: Optional[str] = None
    duration_minutes: int = Field(default=20, ge=1)
    pass_percentage: float = Field(default=60.0, ge=0.0, le=100.0)
    max_attempts: int = Field(default=3, ge=0)
    is_adaptive: bool = False
    instant_feedback: bool = True
    cbt_test_id: Optional[str] = None
    questions_payload: List[Dict[str, Any]] = Field(default_factory=list)
    xp_reward: int = Field(default=50, ge=0)
    status: str = Field(default="PUBLISHED")


class LmsQuizConfigResponse(BaseModel):
    id: str
    course_id: str
    module_id: Optional[str] = None
    title: str
    quiz_type: str
    description: Optional[str] = None
    duration_minutes: int
    pass_percentage: float
    max_attempts: int
    is_adaptive: bool
    instant_feedback: bool
    questions_count: int
    cbt_test_id: Optional[str] = None
    questions_payload: List[Dict[str, Any]]
    xp_reward: int
    status: str
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LmsQuizSubmitAttemptRequest(BaseModel):
    student_id: str
    roll_number: str
    candidate_name: str
    responses: Dict[str, Any] = Field(default_factory=dict)  # {question_id: selected_option}
    time_taken_seconds: int = Field(default=0, ge=0)


class LmsQuizAttemptResponse(BaseModel):
    id: str
    quiz_id: str
    student_id: str
    roll_number: str
    candidate_name: str
    attempt_number: int
    score_obtained: float
    max_score: float
    percentage: float
    is_passed: bool
    xp_awarded: int
    responses_payload: Dict[str, Any]
    started_at: datetime
    submitted_at: Optional[datetime] = None
    time_taken_seconds: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ============================================================================
# Module 8: LMS Discussion & Collaboration Schemas
# ============================================================================

class LmsDiscussionForumCreate(BaseModel):
    course_id: str
    title: str = Field(..., min_length=3, max_length=160)
    category: str = Field(default="GENERAL")  # ANNOUNCEMENT, GENERAL, FACULTY_QA, GROUP_DISCUSSION, PEER_LEARNING
    description: Optional[str] = None
    is_announcement: bool = False
    is_pinned: bool = False
    is_locked: bool = False
    allow_anonymous: bool = False


class LmsDiscussionForumResponse(BaseModel):
    id: str
    course_id: str
    title: str
    category: str
    description: Optional[str] = None
    is_announcement: bool
    is_pinned: bool
    is_locked: bool
    allow_anonymous: bool
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LmsDiscussionThreadCreate(BaseModel):
    forum_id: str
    course_id: str
    title: str = Field(..., min_length=3, max_length=200)
    content: str = Field(..., min_length=5)
    author_id: str = "std_01"
    author_name: str = "Aditya Verma"
    author_role: str = "STUDENT"
    is_announcement: bool = False
    is_pinned: bool = False
    tags: List[str] = Field(default_factory=list)


class LmsDiscussionThreadResponse(BaseModel):
    id: str
    forum_id: str
    course_id: str
    title: str
    content: str
    author_id: str
    author_name: str
    author_role: str
    is_announcement: bool
    is_pinned: bool
    is_resolved: bool
    upvotes_count: int
    replies_count: int
    tags: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LmsDiscussionReplyCreate(BaseModel):
    thread_id: str
    parent_reply_id: Optional[str] = None
    author_id: str = "std_01"
    author_name: str = "Aditya Verma"
    author_role: str = "STUDENT"
    content: str = Field(..., min_length=2)
    is_faculty_answer: bool = False


class LmsDiscussionReplyResponse(BaseModel):
    id: str
    thread_id: str
    parent_reply_id: Optional[str] = None
    author_id: str
    author_name: str
    author_role: str
    content: str
    is_faculty_answer: bool
    is_accepted_answer: bool
    upvotes_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LmsCourseChatMessageCreate(BaseModel):
    course_id: str
    sender_id: str = "std_01"
    sender_name: str = "Aditya Verma"
    sender_role: str = "STUDENT"
    message_text: str = Field(..., min_length=1)
    attachments: List[Dict[str, Any]] = Field(default_factory=list)


class LmsCourseChatMessageResponse(BaseModel):
    id: str
    course_id: str
    sender_id: str
    sender_name: str
    sender_role: str
    message_text: str
    attachments: List[Dict[str, Any]]
    created_at: datetime

    class Config:
        orm_mode = True


# ============================================================================
# Module 9: LMS Attendance & Engagement Tracking Schemas
# ============================================================================

class LmsEngagementMetricUpdate(BaseModel):
    student_id: str
    course_id: str
    activity_type: str  # LESSON_COMPLETION, VIDEO_WATCH, LIVE_CLASS, ASSIGNMENT, QUIZ, LOGIN
    increment_study_minutes: float = Field(default=0.0, ge=0.0)
    additional_details: Dict[str, Any] = Field(default_factory=dict)


class LmsStudentEngagementResponse(BaseModel):
    id: str
    student_id: str
    roll_number: str
    candidate_name: str
    course_id: str
    lessons_completed_count: int
    total_lessons_count: int
    lesson_completion_pct: float
    video_watch_time_minutes: float
    live_classes_attended_count: int
    total_live_classes_count: int
    live_class_attendance_pct: float
    assignments_submitted_count: int
    total_assignments_count: int
    assignment_submission_pct: float
    quizzes_participated_count: int
    total_quizzes_count: int
    quiz_participation_pct: float
    login_frequency_weekly: int
    total_study_time_hours: float
    overall_engagement_score: float
    learning_streak_days: int
    last_activity_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LmsActivityLogCreate(BaseModel):
    student_id: str
    course_id: str
    activity_type: str
    activity_title: str
    activity_details: Dict[str, Any] = Field(default_factory=dict)
    duration_seconds: int = Field(default=0, ge=0)


class LmsActivityLogResponse(BaseModel):
    id: str
    student_id: str
    course_id: str
    activity_type: str
    activity_title: str
    activity_details: Dict[str, Any]
    duration_seconds: int
    created_at: datetime

    class Config:
        orm_mode = True


class LmsCourseCohortEngagementSummary(BaseModel):
    course_id: str
    total_enrolled: int
    average_engagement_score: float
    average_study_hours: float
    average_lesson_completion_pct: float
    average_live_attendance_pct: float
    at_risk_students_count: int
    top_engaged_students_count: int


# ============================================================================
# Module 10: LMS Progress Analytics & Gamification Schemas
# ============================================================================

class LmsBadgeDefinitionCreate(BaseModel):
    code: str = Field(..., min_length=3, max_length=48)
    name: str = Field(..., min_length=3, max_length=120)
    description: str = Field(..., min_length=5)
    category: str = Field(default="SKILL_MASTERY")
    icon_key: str = Field(default="award")
    xp_value: int = Field(default=50, ge=0)
    criteria: Dict[str, Any] = Field(default_factory=dict)


class LmsBadgeDefinitionResponse(BaseModel):
    id: str
    code: str
    name: str
    description: str
    category: str
    icon_key: str
    xp_value: int
    criteria: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LmsStudentBadgeAwardResponse(BaseModel):
    id: str
    student_id: str
    badge: LmsBadgeDefinitionResponse
    course_id: Optional[str] = None
    awarded_at: datetime
    verification_hash: str

    class Config:
        orm_mode = True


class LmsSkillMasteryResponse(BaseModel):
    id: str
    student_id: str
    skill_name: str
    category: str
    mastery_level_pct: float
    competency_status: str
    practice_sessions_count: int
    last_assessed_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LmsGamificationProfileResponse(BaseModel):
    student_id: str
    roll_number: str
    candidate_name: str
    total_xp: int
    current_tier: str  # BRONZE, SILVER, GOLD, PLATINUM, SCHOLAR
    next_tier_xp: int
    learning_streak_days: int
    course_completion_pct: float
    total_badges_earned: int
    earned_badges: List[LmsStudentBadgeAwardResponse]
    skill_masteries: List[LmsSkillMasteryResponse]
    weak_topics: List[Dict[str, Any]]


class LmsFacultyAnalyticsOverviewResponse(BaseModel):
    course_id: str
    course_name: str
    total_students: int
    course_completion_rate_pct: float
    average_cohort_xp: int
    average_streak_days: float
    skill_competency_distribution: Dict[str, int]
    top_achievers: List[Dict[str, Any]]
    struggling_topics: List[Dict[str, Any]]


# ============================================================================
# Module 11: LMS Digital Library Schemas
# ============================================================================

class LmsDigitalResourceCreate(BaseModel):
    course_id: Optional[str] = None
    erp_book_id: Optional[str] = None
    title: str = Field(..., min_length=3, max_length=255)
    author: str = Field(..., min_length=2, max_length=160)
    resource_type: str = Field(default="PDF")  # EBOOK, PDF, LECTURE_NOTES, PREVIOUS_PAPER, JOURNAL, VIDEO, RESEARCH_ARTICLE
    category: str = Field(default="Computer Science")
    file_url: str = Field(..., min_length=5)
    file_format: str = Field(default="pdf")
    file_size_mb: float = Field(default=0.0, ge=0.0)
    download_allowed: bool = True
    isbn: Optional[str] = None
    doi: Optional[str] = None
    publication_year: int = Field(default=2024, ge=1900)
    tags: List[str] = Field(default_factory=list)
    description: Optional[str] = None


class LmsDigitalResourceResponse(BaseModel):
    id: str
    course_id: Optional[str] = None
    erp_book_id: Optional[str] = None
    title: str
    author: str
    resource_type: str
    category: str
    file_url: str
    file_format: str
    file_size_mb: float
    download_allowed: bool
    download_count: int
    view_count: int
    isbn: Optional[str] = None
    doi: Optional[str] = None
    publication_year: int
    tags: List[str]
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LmsDigitalResourceAccessLogResponse(BaseModel):
    id: str
    resource_id: str
    student_id: str
    roll_number: str
    action_type: str
    accessed_at: datetime

    class Config:
        orm_mode = True


class LmsDigitalLibraryCategorySummary(BaseModel):
    category: str
    resource_type: str
    count: int


# ============================================================================
# Module 12: LMS Certificates & Digital Credentials Schemas
# ============================================================================

class LmsCertificateIssueRequest(BaseModel):
    student_id: str
    roll_number: str
    candidate_name: str
    course_id: str
    course_name: str
    certificate_type: str = Field(default="COURSE_COMPLETION")
    completion_percentage: float = Field(default=100.0, ge=0.0, le=100.0)
    grade_or_score: str = Field(default="O (Outstanding)")


class LmsCertificateResponse(BaseModel):
    id: str
    certificate_number: str
    student_id: str
    roll_number: str
    candidate_name: str
    course_id: str
    course_name: str
    certificate_type: str
    issue_date: date
    completion_percentage: float
    grade_or_score: str
    verification_code: str
    qr_payload: str
    digital_signature_hash: str
    pdf_download_url: Optional[str] = None
    status: str
    issued_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LmsCertificateVerifyResponse(BaseModel):
    is_valid: bool
    certificate_number: str
    candidate_name: str
    roll_number: str
    course_name: str
    issue_date: date
    grade_or_score: str
    verification_code: str
    digital_signature_hash: str
    status: str
    issued_by: str


class LmsDigitalCredentialResponse(BaseModel):
    id: str
    student_id: str
    credential_title: str
    credential_type: str
    issuer: str
    skills_covered: List[str]
    issued_at: datetime
    expires_at: Optional[datetime] = None
    verification_url: str
    qr_code_svg: Optional[str] = None

    class Config:
        orm_mode = True


# ============================================================================
# Module 13: LMS Parent Portal Schemas
# ============================================================================

class LmsParentWardResponse(BaseModel):
    id: str
    parent_user_id: str
    parent_name: str
    parent_phone: str
    parent_email: str
    student_id: str
    roll_number: str
    candidate_name: str
    relationship: str
    is_verified: bool
    current_courses: List[Dict[str, Any]] = Field(default_factory=list)


class LmsFacultyStudentFeedbackCreate(BaseModel):
    student_id: str
    roll_number: str
    course_id: str
    faculty_id: str = "fac_01"
    faculty_name: str = "Prof. Rajesh Sharma"
    feedback_type: str = Field(default="ACADEMIC")  # ACADEMIC, ATTENDANCE_CONCERN, PRAISE, DISCIPLINARY
    feedback_text: str = Field(..., min_length=5)
    visible_to_parent: bool = True


class LmsFacultyStudentFeedbackResponse(BaseModel):
    id: str
    student_id: str
    roll_number: str
    course_id: str
    faculty_id: str
    faculty_name: str
    feedback_type: str
    feedback_text: str
    visible_to_parent: bool
    created_at: datetime

    class Config:
        orm_mode = True


class LmsParentNotificationResponse(BaseModel):
    id: str
    parent_user_id: str
    student_id: str
    title: str
    message: str
    notification_type: str
    is_read: bool
    created_at: datetime

    class Config:
        orm_mode = True


class LmsParentOverviewResponse(BaseModel):
    ward_info: Dict[str, Any]
    attendance_overview: Dict[str, Any]
    live_class_attendance: Dict[str, Any]
    assignment_submissions: List[Dict[str, Any]]
    quiz_results: List[Dict[str, Any]]
    progress_summary: Dict[str, Any]
    faculty_feedbacks: List[LmsFacultyStudentFeedbackResponse]
    recent_notifications: List[LmsParentNotificationResponse]


# ============================================================================
# Module 14: LMS Faculty Portal Schemas
# ============================================================================

class LmsFacultyProfileResponse(BaseModel):
    id: str
    faculty_id: str
    full_name: str
    designation: str
    department: str
    specialization: str
    office_hours: str
    virtual_office_room_url: str
    bio: Optional[str] = None
    total_active_courses: int
    total_enrolled_students: int
    rating: float
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LmsFacultyGradingQueueItemResponse(BaseModel):
    id: str
    faculty_id: str
    submission_id: str
    assignment_id: str
    assignment_title: str
    course_id: str
    student_id: str
    roll_number: str
    candidate_name: str
    submitted_at: datetime
    similarity_score_pct: float
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


class LmsFacultyCourseSummary(BaseModel):
    course_id: str
    course_code: str
    course_name: str
    enrolled_count: int
    lessons_published: int
    pending_submissions_count: int
    upcoming_live_class: Optional[str] = None


class LmsFacultyWorkspaceOverviewResponse(BaseModel):
    profile: LmsFacultyProfileResponse
    courses: List[LmsFacultyCourseSummary]
    pending_grading_queue: List[LmsFacultyGradingQueueItemResponse]
    recent_student_inquiries: List[Dict[str, Any]]
    cohort_statistics: Dict[str, Any]


# ============================================================================
# Module 15: LMS Student Portal Schemas
# ============================================================================

class LmsStudentCockpitResponse(BaseModel):
    id: str
    student_id: str
    roll_number: str
    candidate_name: str
    active_term: str
    preferred_language: str
    offline_sync_enabled: bool
    study_goal_hours_weekly: float
    current_streak_days: int
    longest_streak_days: int
    total_xp_earned: int
    current_tier: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LmsStudentBookmarkCreate(BaseModel):
    student_id: str = "std_01"
    resource_id: str
    resource_title: str
    resource_type: str  # VIDEO, LESSON, EBOOK, NOTE, EXAM_PAPER
    target_url: str


class LmsStudentBookmarkResponse(BaseModel):
    id: str
    student_id: str
    resource_id: str
    resource_title: str
    resource_type: str
    target_url: str
    created_at: datetime

    class Config:
        orm_mode = True


class LmsStudentEnrolledCourseItem(BaseModel):
    course_id: str
    course_code: str
    course_name: str
    instructor_name: str
    completion_percentage: float
    next_lesson_title: str
    upcoming_assignment_due: Optional[str] = None
    upcoming_live_class: Optional[str] = None


class LmsStudentUnifiedDashboardResponse(BaseModel):
    cockpit: LmsStudentCockpitResponse
    enrolled_courses: List[LmsStudentEnrolledCourseItem]
    continue_watching_video: Optional[Dict[str, Any]] = None
    pending_assignments_count: int
    available_quizzes_count: int
    earned_certificates_count: int
    recent_bookmarks: List[LmsStudentBookmarkResponse]


# ============================================================================
# Module 16: LMS AI Learning Assistant Schemas
# ============================================================================

class LmsAiTutorQueryRequest(BaseModel):
    student_id: str = "std_01"
    course_id: Optional[str] = "crs_cs301"
    prompt: str = Field(..., min_length=3)
    conversation_id: Optional[str] = None


class LmsAiTutorQueryResponse(BaseModel):
    conversation_id: str
    reply: str
    suggested_followups: List[str] = Field(default_factory=list)
    referenced_topics: List[str] = Field(default_factory=list)
    confidence_score: float = 0.98


class LmsAiFlashcardGenerateRequest(BaseModel):
    student_id: str = "std_01"
    course_id: str = "crs_cs301"
    topic: str = Field(..., min_length=3)
    card_count: int = Field(default=5, ge=1, le=20)


class LmsAiFlashcardDeckResponse(BaseModel):
    id: str
    student_id: str
    course_id: str
    deck_title: str
    topic: str
    cards_payload: List[Dict[str, Any]]
    total_cards_count: int
    created_at: datetime

    class Config:
        orm_mode = True


class LmsAiSummarizeNotesRequest(BaseModel):
    text_content: str = Field(..., min_length=20)
    summary_format: str = Field(default="KEY_BULLETS")  # KEY_BULLETS, EXECUTIVE_SUMMARY, CHEAT_SHEET


class LmsAiSummarizeNotesResponse(BaseModel):
    summary: str
    key_takeaways: List[str]
    suggested_revision_interval_days: int = 3


class LmsAiStudyPlanResponse(BaseModel):
    id: str
    student_id: str
    course_id: str
    target_exam_date: date
    weekly_hours_allocated: float
    milestones_payload: List[Dict[str, Any]]
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


# ============================================================================
# Module 17: LMS Mobile Learning & Offline Sync Schemas
# ============================================================================

class LmsMobileDeviceRegisterRequest(BaseModel):
    student_id: str = "std_01"
    roll_number: str = "2024-MEI-CS-042"
    device_os: str = Field(default="ANDROID")  # ANDROID, IOS, HARMONYOS
    device_model: str = Field(..., min_length=3)
    device_token: str = Field(..., min_length=10)
    app_version: str = "v3.4.0"
    push_notifications_enabled: bool = True
    biometric_login_enabled: bool = True


class LmsMobileDeviceRegistrationResponse(BaseModel):
    id: str
    student_id: str
    roll_number: str
    device_os: str
    device_model: str
    device_token: str
    app_version: str
    push_notifications_enabled: bool
    biometric_login_enabled: bool
    last_sync_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LmsMobileDownloadAssetRequest(BaseModel):
    student_id: str = "std_01"
    device_token: str
    resource_id: str
    resource_title: str
    resource_type: str  # VIDEO, LESSON_SCORM, EBOOK, PDF_NOTES
    file_size_mb: float = Field(default=0.0, ge=0.0)


class LmsOfflineDownloadedAssetResponse(BaseModel):
    id: str
    student_id: str
    device_token: str
    resource_id: str
    resource_title: str
    resource_type: str
    file_size_mb: float
    download_status: str
    expiry_date: Optional[datetime] = None
    downloaded_at: datetime

    class Config:
        orm_mode = True


class LmsMobileSyncRequest(BaseModel):
    student_id: str = "std_01"
    device_token: str
    sync_type: str = Field(default="BACKGROUND")  # BACKGROUND, MANUAL_DELTA, FULL
    sync_payload: Dict[str, Any] = Field(default_factory=dict)


class LmsMobileSyncSessionResponse(BaseModel):
    id: str
    student_id: str
    device_token: str
    sync_type: str
    records_synced_count: int
    status: str
    synced_at: datetime

    class Config:
        orm_mode = True


# ============================================================================
# Module 18: LMS Analytics & Reports Schemas
# ============================================================================

class LmsAnalyticsReportGenerateRequest(BaseModel):
    report_type: str = Field(..., min_length=3)  # STUDENT_PROGRESS, FACULTY_PERFORMANCE, COURSE_COMPLETION, ASSIGNMENT_STATISTICS, QUIZ_PERFORMANCE, ENGAGEMENT_TRENDS, LMS_USAGE, DEPARTMENT_REPORT
    title: str = Field(..., min_length=3, max_length=200)
    department: str = "Computer Science & Engineering"
    academic_year: str = "2026-27"
    export_format: str = Field(default="PDF")  # PDF, CSV, XLSX, JSON
    parameters: Dict[str, Any] = Field(default_factory=dict)


class LmsAnalyticsReportArchiveResponse(BaseModel):
    id: str
    report_code: str
    report_type: str
    title: str
    department: str
    academic_year: str
    parameters: Dict[str, Any]
    metrics_payload: Dict[str, Any]
    export_format: str
    download_url: Optional[str] = None
    generated_by: str
    created_at: datetime

    class Config:
        orm_mode = True


class LmsDepartmentMetricResponse(BaseModel):
    id: str
    department: str
    total_courses: int
    total_faculty: int
    total_students: int
    average_completion_rate: float
    average_attendance_pct: float
    active_learning_hours: float
    certifications_issued: int
    updated_at: datetime

    class Config:
        orm_mode = True


class LmsGlobalReportingDashboardResponse(BaseModel):
    academic_year: str
    total_students_enrolled: int
    total_courses_active: int
    overall_completion_rate_pct: float
    average_attendance_pct: float
    total_study_hours_logged: float
    total_certifications_issued: int
    department_metrics: List[LmsDepartmentMetricResponse]
    recent_reports: List[LmsAnalyticsReportArchiveResponse]


# ============================================================================
# Module 19: LMS Enterprise Integrations Schemas
# ============================================================================

class LmsSystemIntegrationConnectorResponse(BaseModel):
    id: str
    system_name: str
    display_name: str
    connector_type: str
    endpoint_url: str
    status: str
    latency_ms: float
    last_heartbeat_at: datetime
    config_payload: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LmsConnectorHealthCheckResponse(BaseModel):
    system_name: str
    is_healthy: bool
    status: str
    latency_ms: float
    checked_at: datetime


class LmsGlobalSearchItemResponse(BaseModel):
    id: str
    entity_type: str
    entity_id: str
    course_id: Optional[str] = None
    title: str
    snippet: str
    target_route: str
    tags: List[str]
    indexed_at: datetime

    class Config:
        orm_mode = True


class LmsPaymentInitiateRequest(BaseModel):
    student_id: str = "std_01"
    course_id: str
    amount_inr: float = Field(..., gt=0.0)
    gateway_provider: str = Field(default="RAZORPAY")
    payment_method: str = Field(default="UPI")


class LmsPaymentTransactionResponse(BaseModel):
    id: str
    transaction_number: str
    student_id: str
    course_id: str
    amount_inr: float
    gateway_provider: str
    payment_status: str
    payment_method: str
    receipt_url: Optional[str] = None
    paid_at: datetime

    class Config:
        orm_mode = True


# ============================================================================
# Module 20: LMS Production Readiness & Enterprise Validation Schemas
# ============================================================================

class LmsProductionReadinessAuditResponse(BaseModel):
    audit_timestamp: datetime
    overall_status: str  # PRODUCTION_READY, DEGRADED, FAILED
    readiness_score_pct: float
    functional_audit: Dict[str, Any]
    performance_audit: Dict[str, Any]
    security_audit: Dict[str, Any]
    quality_audit: Dict[str, Any]


class LmsE2ETestResultResponse(BaseModel):
    test_suite: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    duration_ms: float
    pass_rate_pct: float
    test_cases: List[Dict[str, Any]]
    executed_at: datetime


class LmsSystemHealthScorecardResponse(BaseModel):
    mesh_status: str
    database_pool_status: str
    cache_hit_ratio_pct: float
    cdn_availability_pct: float
    jwt_auth_status: str
    rbac_compliance_pct: float
    client_storage_violation_count: int
    total_verified_api_routes: int
    total_lxp_api_routes: int
    checked_at: datetime
