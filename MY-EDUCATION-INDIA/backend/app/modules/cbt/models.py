import uuid
from datetime import date, datetime, time, timezone
from typing import List, Optional
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    Time,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class QuestionBank(Base):
    __tablename__ = "question_banks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    subject_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    categories: Mapped[List["QuestionCategory"]] = relationship("QuestionCategory", back_populates="question_bank", cascade="all, delete-orphan")


class QuestionCategory(Base):
    __tablename__ = "question_categories"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_bank_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("question_banks.id", ondelete="CASCADE"), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    question_bank: Mapped["QuestionBank"] = relationship("QuestionBank", back_populates="categories")
    topics: Mapped[List["QuestionTopic"]] = relationship("QuestionTopic", back_populates="category", cascade="all, delete-orphan")


class QuestionTopic(Base):
    __tablename__ = "question_topics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("question_categories.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    category: Mapped["QuestionCategory"] = relationship("QuestionCategory", back_populates="topics")
    questions: Mapped[List["QuestionVersion"]] = relationship("QuestionVersion", back_populates="topic")


class QuestionTag(Base):
    __tablename__ = "question_tags"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    tag_name: Mapped[str] = mapped_column(String(48), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class QuestionVersion(Base):
    __tablename__ = "question_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("question_topics.id", ondelete="CASCADE"), nullable=False, index=True)
    question_code: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    question_type: Mapped[str] = mapped_column(String(32), default="MCQ", nullable=False) # MCQ, MSQ, TRUE_FALSE, FILL_BLANKS, NUMERICAL, ESSAY
    difficulty_level: Mapped[str] = mapped_column(String(20), default="MEDIUM", nullable=False) # EASY, MEDIUM, HARD, EXPERT
    bloom_level: Mapped[str] = mapped_column(String(24), default="UNDERSTAND", nullable=False) # REMEMBER, UNDERSTAND, APPLY, ANALYZE, EVALUATE, CREATE
    language: Mapped[str] = mapped_column(String(32), default="English", nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    latex_equations_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    programming_metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    tags_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    options_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    correct_answers_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    default_marks: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    negative_marks: Mapped[float] = mapped_column(Float, default=0.25, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    approval_status: Mapped[str] = mapped_column(String(24), default="APPROVED", nullable=False) # DRAFT, PENDING, APPROVED, REJECTED
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    topic: Mapped["QuestionTopic"] = relationship("QuestionTopic", back_populates="questions")
    media: Mapped[List["QuestionMedia"]] = relationship("QuestionMedia", back_populates="question", cascade="all, delete-orphan")


class QuestionMedia(Base):
    __tablename__ = "question_media"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("question_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    media_type: Mapped[str] = mapped_column(String(20), nullable=False) # IMAGE, AUDIO, VIDEO, DIAGRAM
    media_url: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    question: Mapped["QuestionVersion"] = relationship("QuestionVersion", back_populates="media")


class QuestionPool(Base):
    __tablename__ = "question_pools"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    selection_rules_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ExamTemplate(Base):
    __tablename__ = "exam_templates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    total_marks: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    passing_marks: Mapped[float] = mapped_column(Float, default=40.0, nullable=False)
    allow_calculator: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    shuffle_questions: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    shuffle_options: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    allow_offline_sync: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sections_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    instructions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    cbt_sessions: Mapped[List["CBTSession"]] = relationship("CBTSession", back_populates="template")


class CBTSession(Base):
    __tablename__ = "cbt_sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    template_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_templates.id", ondelete="RESTRICT"), nullable=False, index=True)
    exam_subject_id: Optional[Mapped[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True) # Direct integration with Module 11 ExamSubject
    session_code: Mapped[str] = mapped_column(String(48), unique=True, nullable=False, index=True)
    start_window: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_window: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    delivery_mode: Mapped[str] = mapped_column(String(24), default="ONLINE", nullable=False) # ONLINE, LAN, OFFLINE, HYBRID
    status: Mapped[str] = mapped_column(String(24), default="SCHEDULED", nullable=False) # SCHEDULED, LIVE, COMPLETED, RESULTS_SYNCED
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    template: Mapped["ExamTemplate"] = relationship("ExamTemplate", back_populates="cbt_sessions")
    candidates: Mapped[List["CandidateSession"]] = relationship("CandidateSession", back_populates="cbt_session", cascade="all, delete-orphan")


class CandidateSession(Base):
    __tablename__ = "candidate_sessions"
    __table_args__ = (
        UniqueConstraint("cbt_session_id", "student_id", name="uq_candidate_cbt_session"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cbt_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cbt_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    random_seed: Mapped[int] = mapped_column(Integer, default=12345, nullable=False)
    device_fingerprint: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(48), nullable=True)
    start_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    submit_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    remaining_seconds: Mapped[int] = mapped_column(Integer, default=3600, nullable=False)
    status: Mapped[str] = mapped_column(String(24), default="IN_PROGRESS", nullable=False) # IN_PROGRESS, SUBMITTED, FORCE_SUBMITTED, PAUSED, DISQUALIFIED
    total_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    marks_synced_to_module11: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    current_question_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_heartbeat_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    submission_reason: Mapped[str] = mapped_column(String(32), default="MANUAL", nullable=False)
    warnings_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_fullscreen_locked: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    proctor_status: Mapped[str] = mapped_column(String(32), default="NORMAL", nullable=False)
    webcam_verified: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    cbt_session: Mapped["CBTSession"] = relationship("CBTSession", back_populates="candidates")
    answers: Mapped[List["CandidateAnswer"]] = relationship("CandidateAnswer", back_populates="candidate_session", cascade="all, delete-orphan")


class CandidateAnswer(Base):
    __tablename__ = "candidate_answers"
    __table_args__ = (
        UniqueConstraint("candidate_session_id", "question_id", name="uq_candidate_question_answer"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidate_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("question_versions.id", ondelete="RESTRICT"), nullable=False, index=True)
    selected_options_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    text_answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_marked_for_review: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_correct: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    awarded_marks: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    time_spent_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    answer_status: Mapped[str] = mapped_column(String(32), default="NOT_VISITED", nullable=False)
    last_autosaved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    candidate_session: Mapped["CandidateSession"] = relationship("CandidateSession", back_populates="answers")
    question: Mapped["QuestionVersion"] = relationship("QuestionVersion")


class AnswerLog(Base):
    __tablename__ = "answer_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidate_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    action_type: Mapped[str] = mapped_column(String(32), nullable=False) # SELECT, CLEAR, MARK_REVIEW, UNMARK_REVIEW
    payload_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class OfflineSyncLog(Base):
    __tablename__ = "offline_sync_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidate_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    batch_count: Mapped[int] = mapped_column(Integer, nullable=False)
    checksum: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(24), default="SYNCED", nullable=False) # SYNCED, CONFLICT, FAILED
    synced_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class LiveMonitorLog(Base):
    __tablename__ = "live_monitor_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cbt_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cbt_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    candidate_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(32), nullable=False) # TAB_SWITCH, FULLSCREEN_EXIT, RIGHT_CLICK, HEARTBEAT
    warning_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    logged_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class QuestionStatistic(Base):
    __tablename__ = "question_statistics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("question_versions.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    total_attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_correct: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_incorrect: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    difficulty_index: Mapped[float] = mapped_column(Float, default=0.5, nullable=False) # P-value
    discrimination_index: Mapped[float] = mapped_column(Float, default=0.3, nullable=False) # D-value
    average_time_seconds: Mapped[float] = mapped_column(Float, default=45.0, nullable=False)


class CandidateStatistic(Base):
    __tablename__ = "candidate_statistics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidate_sessions.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    attempted_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    correct_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    incorrect_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    accuracy_percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    speed_questions_per_minute: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)


class ExamStatistic(Base):
    __tablename__ = "exam_statistics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cbt_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cbt_sessions.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    total_registered: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_appeared: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    average_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    highest_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    lowest_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)


class CBTReport(Base):
    __tablename__ = "cbt_reports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    report_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    parameters_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    generated_by_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CBTGlobalConfig(Base):
    """
    Phase 3 Module 1: CBT Foundation & Global Settings
    Controls testing environment, NTP server synchronization, browser lockdown requirements,
    and institutional examination conduct policies.
    """
    __tablename__ = "cbt_global_configs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, unique=True, index=True)
    system_title: Mapped[str] = mapped_column(String(150), default="MY EDUCATION INDIA Enterprise CBT System", nullable=False)
    active_environment: Mapped[str] = mapped_column(String(32), default="HYBRID", nullable=False)  # ONLINE, LAN, OFFLINE, HYBRID
    ntp_server: Mapped[str] = mapped_column(String(120), default="time.google.com", nullable=False)
    time_sync_tolerance_seconds: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    browser_lockdown_strict: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    min_browser_versions_json: Mapped[dict] = mapped_column(
        JSONB,
        default=lambda: {"Chrome": 110, "Edge": 110, "Firefox": 115, "Safari": 16},
        nullable=False,
    )
    allowed_os_list_json: Mapped[list] = mapped_column(
        JSONB,
        default=lambda: ["Windows 10", "Windows 11", "macOS", "Ubuntu Linux", "Fedora Linux"],
        nullable=False,
    )
    fullscreen_enforced: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    tab_switch_limit: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    clipboard_blocked: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    right_click_blocked: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    screen_capture_blocked: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    auto_save_interval_seconds: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    heartbeat_interval_seconds: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    offline_sync_batch_size: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    offline_storage_retention_days: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    disconnection_grace_seconds: Mapped[int] = mapped_column(Integer, default=300, nullable=False)
    calculator_allowed_global: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    exam_policy_html: Mapped[str] = mapped_column(
        Text,
        default="""<div class='exam-policy'>
<h3>Institutional Examination Conduct & Code of Ethics</h3>
<p>Candidates must maintain strict testing integrity. Full-screen mode is enforced throughout the examination session.</p>
<ul>
<li>Exiting full-screen or switching tabs will be logged and may lead to automatic test disqualification after the permitted warning limit.</li>
<li>Ensure computer time is synchronized with the institutional testing server.</li>
<li>Responses are automatically saved every 3 seconds to ensure zero data loss during network disruptions.</li>
</ul>
</div>""",
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


# ------------------- Phase 3 Module 3: Question Workflow & Audit -------------------
class QuestionWorkflowAudit(Base):
    """
    Audit trail for multi-stage question approval workflow:
    DRAFT -> REVIEW -> EXPERT_REVIEW -> APPROVED -> PUBLISHED / REJECTED
    """
    __tablename__ = "question_workflow_audits"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("question_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    from_status: Mapped[str] = mapped_column(String(24), default="DRAFT", nullable=False)
    to_status: Mapped[str] = mapped_column(String(24), nullable=False)
    action: Mapped[str] = mapped_column(String(32), nullable=False)
    actor_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    actor_role: Mapped[str] = mapped_column(String(32), default="AUTHOR", nullable=False)
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class QuestionReviewFeedback(Base):
    """
    Peer review and Subject Matter Expert (SME) feedback comments and rubric scores.
    """
    __tablename__ = "question_review_feedbacks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("question_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    reviewer_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    review_type: Mapped[str] = mapped_column(String(24), default="PEER_REVIEW", nullable=False) # PEER_REVIEW, EXPERT_VETTING
    verdict: Mapped[str] = mapped_column(String(24), default="APPROVED", nullable=False) # APPROVED, REVISION_NEEDED, REJECTED
    feedback_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    rubric_scores_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


# ------------------- Phase 3 Module 5: Candidate Management -------------------
class CBTCandidate(Base):
    """
    Phase 3 Module 5: Candidate Management
    Integrated with ERP User Directory (Module 4) for both internal students and external candidates.
    Governs exam center allocation, lab/seat assignments, biometric/identity verification, and admit cards.
    """
    __tablename__ = "cbt_candidates"
    __table_args__ = (
        UniqueConstraint("cbt_session_id", "user_id", name="uq_cbt_session_user_candidate"),
        UniqueConstraint("admit_card_number", name="uq_cbt_candidate_admit_card_num"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    cbt_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cbt_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True) # Direct integration with ERP users.id
    candidate_type: Mapped[str] = mapped_column(String(32), default="INTERNAL_STUDENT", nullable=False) # INTERNAL_STUDENT, EXTERNAL_APPLICANT
    roll_number: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    application_number: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    admit_card_number: Mapped[str] = mapped_column(String(48), nullable=False, index=True)
    center_name: Mapped[str] = mapped_column(String(180), default="MEI Central Campus Testing Center", nullable=False)
    center_code: Mapped[str] = mapped_column(String(32), default="TC-IND-01", nullable=False)
    batch_code: Mapped[str] = mapped_column(String(48), default="SHIFT-1-MORNING", nullable=False)
    allocated_lab: Mapped[str] = mapped_column(String(64), default="Computer Lab 1", nullable=False)
    seat_number: Mapped[str] = mapped_column(String(32), default="DESK-01", nullable=False)
    reporting_time: Mapped[str] = mapped_column(String(32), default="08:30 AM IST", nullable=False)
    gate_closing_time: Mapped[str] = mapped_column(String(32), default="09:15 AM IST", nullable=False)
    verification_status: Mapped[str] = mapped_column(String(24), default="PENDING", nullable=False) # PENDING, VERIFIED, REJECTED, FLAGGED
    identity_document_type: Mapped[str] = mapped_column(String(48), default="Aadhaar Card", nullable=False)
    identity_document_number: Mapped[str] = mapped_column(String(64), default="XXXXXXXX1234", nullable=False)
    biometric_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    admit_card_downloaded: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_present: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    instructions_acknowledged: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    admit_card_html: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


# ------------------- Phase 3 Module 6: Exam Scheduling & Centers -------------------
class ExamCenter(Base):
    """
    Phase 3 Module 6: Testing Center Facilities & Regional Venues
    Tracks testing center capacity, computer labs, and buffer allocations.
    """
    __tablename__ = "exam_centers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    center_code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    city: Mapped[str] = mapped_column(String(80), default="Indore", nullable=False)
    state: Mapped[str] = mapped_column(String(80), default="Madhya Pradesh", nullable=False)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    contact_email: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    total_workstations: Mapped[int] = mapped_column(Integer, default=250, nullable=False)
    buffer_capacity_percentage: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    labs: Mapped[List["ExamLab"]] = relationship("ExamLab", back_populates="center", cascade="all, delete-orphan")


class ExamLab(Base):
    """
    Computer Laboratory rooms within an examination testing center.
    """
    __tablename__ = "exam_labs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    center_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_centers.id", ondelete="CASCADE"), nullable=False, index=True)
    lab_code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    floor: Mapped[str] = mapped_column(String(32), default="Ground Floor", nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    is_lan_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    center: Mapped["ExamCenter"] = relationship("ExamCenter", back_populates="labs")


class ExamShiftSchedule(Base):
    """
    Multi-shift timetable scheduling for examination sessions.
    Automatically cross-references Module 12 campus holidays to prevent date collisions.
    """
    __tablename__ = "exam_shift_schedules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cbt_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cbt_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    shift_code: Mapped[str] = mapped_column(String(32), nullable=False, index=True) # SHIFT-1-MORNING, SHIFT-2-AFTERNOON, SHIFT-3-EVENING
    shift_name: Mapped[str] = mapped_column(String(100), nullable=False)
    exam_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    reporting_time: Mapped[str] = mapped_column(String(32), default="08:30 AM IST", nullable=False)
    gate_closing_time: Mapped[str] = mapped_column(String(32), default="09:15 AM IST", nullable=False)
    start_time: Mapped[str] = mapped_column(String(32), default="09:30 AM IST", nullable=False)
    end_time: Mapped[str] = mapped_column(String(32), default="12:30 PM IST", nullable=False)
    total_allocated_candidates: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    conflict_holiday_flag: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    reminder_dispatched: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


# ------------------- Phase 3 Module 8: Security & Proctoring Models -------------------
class ProctorIncident(Base):
    __tablename__ = "cbt_proctor_incidents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidate_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    cbt_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    incident_type: Mapped[str] = mapped_column(String(48), nullable=False)  # TAB_SWITCH, FULLSCREEN_EXIT, CLIPBOARD_COPY, CLIPBOARD_PASTE, RIGHT_CLICK, DEVTOOLS_OPEN, MULTIPLE_FACES, NO_FACE, SCREEN_CAPTURE
    severity: Mapped[str] = mapped_column(String(16), default="MEDIUM", nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    warning_index: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    snapshot_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    incident_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ProctorBroadcastMessage(Base):
    __tablename__ = "cbt_proctor_messages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cbt_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    candidate_session_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    proctor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    message_type: Mapped[str] = mapped_column(String(32), default="WARNING", nullable=False)  # WARNING, PAUSE, RESUME, DISQUALIFICATION, GENERAL
    message_text: Mapped[str] = mapped_column(Text, nullable=False)
    acknowledged: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


# ------------------- Phase 3 Module 9: Evaluation Engine Models -------------------
class CBTEvaluationRun(Base):
    __tablename__ = "cbt_evaluation_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cbt_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cbt_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    evaluated_by_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    evaluation_type: Mapped[str] = mapped_column(String(32), default="OBJECTIVE_AUTO", nullable=False)
    total_candidates: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    average_raw_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    average_moderated_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    highest_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    lowest_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    pass_percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="EVALUATED", nullable=False)  # EVALUATED, MODERATED, PUBLISHED_TO_MODULE11
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class GraceMarksAllocation(Base):
    __tablename__ = "cbt_grace_marks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cbt_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cbt_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("question_versions.id", ondelete="SET NULL"), nullable=True, index=True)
    rule_type: Mapped[str] = mapped_column(String(48), default="DISPUTED_QUESTION_BONUS", nullable=False)
    grace_marks_awarded: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    approved_by_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CandidateModeratedResult(Base):
    __tablename__ = "cbt_candidate_moderated_results"
    __table_args__ = (
        UniqueConstraint("cbt_session_id", "candidate_session_id", name="uq_cbt_candidate_moderated"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cbt_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cbt_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    candidate_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidate_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    raw_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    negative_deductions: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    partial_marks_earned: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    grace_marks: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    moderated_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    percentile: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    rank: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_passed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="PENDING", nullable=False)  # PENDING, APPROVED, SYNCED_TO_MODULE11
    synced_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


# ------------------- Phase 3 Module 10: Results & Analytics Models -------------------
class CBTTopicMasteryAnalytics(Base):
    __tablename__ = "cbt_topic_mastery_analytics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cbt_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cbt_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    subject_name: Mapped[str] = mapped_column(String(100), nullable=False)
    topic_name: Mapped[str] = mapped_column(String(100), nullable=False)
    total_questions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    correct_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    accuracy_percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    proficiency_level: Mapped[str] = mapped_column(String(32), default="PROFICIENT", nullable=False)  # MASTERY, PROFICIENT, NEEDS_IMPROVEMENT
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CBTDifficultyTimeAnalysis(Base):
    __tablename__ = "cbt_difficulty_time_analytics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cbt_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cbt_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    difficulty_level: Mapped[str] = mapped_column(String(24), nullable=False)  # EASY, MODERATE, HARD
    average_time_seconds: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    accuracy_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    discrimination_index: Mapped[float] = mapped_column(Float, default=0.3, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


# ------------------- Phase 3 Module 11: Certificate Integration Models -------------------
class CBTIssuedCertificate(Base):
    __tablename__ = "cbt_issued_certificates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cbt_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cbt_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    candidate_session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidate_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    erp_certificate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("issued_certificates.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    certificate_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    verification_code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    hmac_signature: Mapped[str] = mapped_column(String(128), nullable=False)
    certificate_type: Mapped[str] = mapped_column(String(48), default="MERIT_SCHOLARSHIP", nullable=False)
    candidate_name: Mapped[str] = mapped_column(String(120), nullable=False)
    roll_number: Mapped[str] = mapped_column(String(48), nullable=False)
    score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    rank: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    percentile: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    pdf_download_url: Mapped[str] = mapped_column(String(255), nullable=False)
    qr_payload_url: Mapped[str] = mapped_column(String(255), nullable=False)
    email_dispatched: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    email_dispatched_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


# ------------------- Phase 3 Module 12: Candidate Portal Models -------------------
class CBTCandidateSupportTicket(Base):
    __tablename__ = "cbt_candidate_tickets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_number: Mapped[str] = mapped_column(String(48), unique=True, nullable=False, index=True)
    cbt_session_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("cbt_sessions.id", ondelete="SET NULL"), nullable=True, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    candidate_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("cbt_candidates.id", ondelete="SET NULL"), nullable=True, index=True)
    category: Mapped[str] = mapped_column(String(48), default="ADMIT_CARD_DISCREPANCY", nullable=False)
    subject: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[str] = mapped_column(String(24), default="MEDIUM", nullable=False)  # LOW, MEDIUM, HIGH, URGENT
    status: Mapped[str] = mapped_column(String(24), default="OPEN", nullable=False)  # OPEN, IN_PROGRESS, RESOLVED, CLOSED
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


# ------------------- Phase 3 Module 13: Mock Test Platform Models -------------------
class CBTMockTestSeries(Base):
    __tablename__ = "cbt_mock_series"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    series_code: Mapped[str] = mapped_column(String(48), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(48), default="ALL_INDIA_FULL_LENGTH", nullable=False)  # ALL_INDIA_FULL_LENGTH, SUBJECT_MASTERY, CHAPTER_DRILL
    subject_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    total_questions: Mapped[int] = mapped_column(Integer, default=20, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    is_free: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    registered_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CBTMockAttempt(Base):
    __tablename__ = "cbt_mock_attempts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    series_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cbt_mock_series.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    max_score: Mapped[float] = mapped_column(Float, default=20.0, nullable=False)
    accuracy_percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    time_spent_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    percentile: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    rank: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    attempted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CBTPublicLeaderboard(Base):
    __tablename__ = "cbt_public_leaderboard"
    __table_args__ = (
        UniqueConstraint("series_id", "student_id", name="uq_cbt_mock_leaderboard"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    series_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cbt_mock_series.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    candidate_name: Mapped[str] = mapped_column(String(120), nullable=False)
    roll_number: Mapped[str] = mapped_column(String(48), nullable=False)
    score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    accuracy: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    time_spent_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    rank: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    percentile: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    institute_badge: Mapped[str] = mapped_column(String(80), default="MY EDUCATION INDIA", nullable=False)
    achieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


# ------------------- Phase 3 Module 14: CBT Administration Models -------------------
class CBTTerminalDeviceHealth(Base):
    __tablename__ = "cbt_terminal_devices"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lab_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_labs.id", ondelete="CASCADE"), nullable=False, index=True)
    terminal_code: Mapped[str] = mapped_column(String(48), unique=True, nullable=False, index=True)
    ip_address: Mapped[str] = mapped_column(String(48), nullable=False)
    mac_address: Mapped[Optional[str]] = mapped_column(String(48), nullable=True)
    os_version: Mapped[str] = mapped_column(String(80), default="Ubuntu 24.04 LTS (Kiosk Lockdown)", nullable=False)
    browser_version: Mapped[str] = mapped_column(String(80), default="Chromium 128.0 (CBT Kiosk)", nullable=False)
    cpu_load_percentage: Mapped[float] = mapped_column(Float, default=15.0, nullable=False)
    ram_usage_percentage: Mapped[float] = mapped_column(Float, default=42.0, nullable=False)
    ping_latency_ms: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    kiosk_mode_locked: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    webcam_ready: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    status: Mapped[str] = mapped_column(String(24), default="HEALTHY", nullable=False)  # HEALTHY, WARNING, OFFLINE, MAINTENANCE
    last_heartbeat: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CBTSystemDiagnosticRun(Base):
    __tablename__ = "cbt_diagnostic_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    center_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_centers.id", ondelete="CASCADE"), nullable=False, index=True)
    lab_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_labs.id", ondelete="SET NULL"), nullable=True, index=True)
    run_by_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    bandwidth_download_mbps: Mapped[float] = mapped_column(Float, default=450.0, nullable=False)
    bandwidth_upload_mbps: Mapped[float] = mapped_column(Float, default=380.0, nullable=False)
    ntp_time_drift_ms: Mapped[float] = mapped_column(Float, default=1.2, nullable=False)
    lan_packet_loss_percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    webrtc_stun_passed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    overall_readiness_status: Mapped[str] = mapped_column(String(24), default="PASSED", nullable=False)  # PASSED, WARNING, FAILED
    diagnostic_details: Mapped[str] = mapped_column(Text, nullable=False)
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CBTIncidentReport(Base):
    __tablename__ = "cbt_incidents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_code: Mapped[str] = mapped_column(String(48), unique=True, nullable=False, index=True)
    center_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_centers.id", ondelete="CASCADE"), nullable=False, index=True)
    lab_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_labs.id", ondelete="SET NULL"), nullable=True, index=True)
    terminal_code: Mapped[Optional[str]] = mapped_column(String(48), nullable=True)
    severity: Mapped[str] = mapped_column(String(24), default="MEDIUM", nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    category: Mapped[str] = mapped_column(String(48), default="HARDWARE_FAILURE", nullable=False)  # HARDWARE_FAILURE, NETWORK_OUTAGE, POWER_DISRUPTION, SECURITY_MALPRACTICE, INVIGILATOR_REPORT
    description: Mapped[str] = mapped_column(Text, nullable=False)
    reported_by_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    status: Mapped[str] = mapped_column(String(24), default="OPEN", nullable=False)  # OPEN, INVESTIGATING, RESOLVED, ESCALATED
    resolution_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


# ------------------- Phase 3 Module 15: Reports & Monitoring Models -------------------
class CBTInvigilatorAllocation(Base):
    __tablename__ = "cbt_invigilator_allocations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    center_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_centers.id", ondelete="CASCADE"), nullable=False, index=True)
    lab_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_labs.id", ondelete="CASCADE"), nullable=False, index=True)
    shift_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_shifts.id", ondelete="SET NULL"), nullable=True, index=True)
    invigilator_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    invigilator_name: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[str] = mapped_column(String(48), default="LAB_INVIGILATOR", nullable=False)  # CHIEF_SUPERINTENDENT, LAB_INVIGILATOR, TECHNICAL_OBSERVER, ROVING_PROCTOR
    reporting_status: Mapped[str] = mapped_column(String(24), default="REPORTED", nullable=False)  # REPORTED, ON_DUTY, RELIEVED, ABSENT
    duty_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CBTExecutiveMonitoringSnapshot(Base):
    __tablename__ = "cbt_monitoring_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    center_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("exam_centers.id", ondelete="CASCADE"), nullable=False, index=True)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cbt_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    shift_code: Mapped[str] = mapped_column(String(48), default="SHIFT-1-MORNING", nullable=False)
    total_registered: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_present: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_absent: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    attendance_percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    workstations_occupied: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    incidents_reported: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    violations_detected: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    average_turnaround_time_seconds: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


# ------------------- Phase 3 Module 16: Enterprise Integrations Models -------------------
class CBTIntegrationSurface(Base):
    __tablename__ = "cbt_integration_surfaces"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    surface_name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    service_endpoint: Mapped[str] = mapped_column(String(255), nullable=False)
    auth_mechanism: Mapped[str] = mapped_column(String(32), default="OAUTH2_JWT", nullable=False)
    health_status: Mapped[str] = mapped_column(String(24), default="HEALTHY", nullable=False)  # HEALTHY, DEGRADED, SYNCHRONIZED
    total_events_dispatched: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    active_sync_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    integration_metadata: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    last_heartbeat_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
