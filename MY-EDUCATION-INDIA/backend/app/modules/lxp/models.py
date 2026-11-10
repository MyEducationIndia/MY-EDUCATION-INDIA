"""
Module 15: Enterprise Learning Experience Platform (LXP) - Models
Provisions 17 enterprise tables for courses, modules, lessons, video streaming,
assignments, discussions, gamification, and learning analytics.
"""
from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Date, ForeignKey, Text, Index
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.db.base import Base

class LearningCourse(Base):
    __tablename__ = "learning_courses"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    course_code = Column(String(50), nullable=False, index=True)
    course_name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False)
    difficulty = Column(String(30), default="BEGINNER", nullable=False) # BEGINNER, INTERMEDIATE, ADVANCED
    language = Column(String(50), default="English", nullable=False)
    duration_minutes = Column(Integer, default=0, nullable=False)
    thumbnail_url = Column(String(500), nullable=True)
    banner_url = Column(String(500), nullable=True)
    instructor_id = Column(String(36), nullable=False, index=True)
    department_id = Column(String(36), nullable=True)
    academic_program_id = Column(String(36), nullable=True)
    fee_amount = Column(Float, default=0.0, nullable=False)
    certificate_template_id = Column(String(36), nullable=True)
    status = Column(String(30), default="DRAFT", nullable=False) # DRAFT, PUBLISHED, ARCHIVED
    visibility = Column(String(30), default="PUBLIC", nullable=False) # PUBLIC, ENROLLED_ONLY, PRIVATE
    tags = Column(JSONB, nullable=True)
    is_free = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    modules = relationship("LearningModule", back_populates="course", cascade="all, delete-orphan", order_by="LearningModule.order_index")
    enrollments = relationship("CourseEnrollment", back_populates="course", cascade="all, delete-orphan")

class LearningModule(Base):
    __tablename__ = "learning_modules"
    id = Column(String(36), primary_key=True)
    course_id = Column(String(36), ForeignKey("learning_courses.id"), nullable=False, index=True)
    module_title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, default=1, nullable=False)
    duration_minutes = Column(Integer, default=0, nullable=False)
    is_published = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    course = relationship("LearningCourse", back_populates="modules")
    lessons = relationship("LearningLesson", back_populates="module", cascade="all, delete-orphan", order_by="LearningLesson.order_index")

class LearningLesson(Base):
    __tablename__ = "learning_lessons"
    id = Column(String(36), primary_key=True)
    module_id = Column(String(36), ForeignKey("learning_modules.id"), nullable=False, index=True)
    lesson_title = Column(String(255), nullable=False)
    lesson_type = Column(String(40), default="VIDEO", nullable=False) # VIDEO, PDF, PRESENTATION, ARTICLE, HTML_LESSON, EXTERNAL_LINK, YOUTUBE_EMBED, AUDIO, ASSIGNMENT, QUIZ, PRACTICE_TEST, CBT_SESSION
    content_body = Column(Text, nullable=True)
    video_id = Column(String(36), ForeignKey("video_library.id"), nullable=True)
    duration_seconds = Column(Integer, default=0, nullable=False)
    order_index = Column(Integer, default=1, nullable=False)
    is_preview = Column(Boolean, default=False, nullable=False)
    is_mandatory = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    module = relationship("LearningModule", back_populates="lessons")
    resources = relationship("LessonResource", back_populates="lesson", cascade="all, delete-orphan")

class LessonResource(Base):
    __tablename__ = "lesson_resources"
    id = Column(String(36), primary_key=True)
    lesson_id = Column(String(36), ForeignKey("learning_lessons.id"), nullable=False, index=True)
    resource_name = Column(String(255), nullable=False)
    file_format = Column(String(30), nullable=False) # PDF, DOCX, PPT, ZIP, MP4, MP3, IPYNB
    file_url = Column(String(500), nullable=False)
    file_size_bytes = Column(Integer, default=0, nullable=False)
    download_allowed = Column(Boolean, default=True, nullable=False)
    version = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    lesson = relationship("LearningLesson", back_populates="resources")

class VideoLibrary(Base):
    __tablename__ = "video_library"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    duration_seconds = Column(Integer, default=0, nullable=False)
    hls_stream_url = Column(String(500), nullable=True)
    dash_stream_url = Column(String(500), nullable=True)
    raw_file_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500), nullable=True)
    resolutions = Column(JSONB, nullable=True) # ["360p", "720p", "1080p"]
    captions_url = Column(String(500), nullable=True)
    file_size_bytes = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class CourseEnrollment(Base):
    __tablename__ = "course_enrollments"
    id = Column(String(36), primary_key=True)
    course_id = Column(String(36), ForeignKey("learning_courses.id"), nullable=False, index=True)
    student_id = Column(String(36), nullable=False, index=True)
    batch_id = Column(String(36), nullable=True)
    enrollment_type = Column(String(30), default="FREE", nullable=False) # FREE, PAID, BATCH_ASSIGNED
    enrollment_status = Column(String(30), default="ACTIVE", nullable=False) # ACTIVE, COMPLETED, SUSPENDED, EXPIRED
    progress_percentage = Column(Float, default=0.0, nullable=False)
    fee_clearance_verified = Column(Boolean, default=True, nullable=False)
    enrolled_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=True)

    course = relationship("LearningCourse", back_populates="enrollments")
    progress_records = relationship("LearningProgress", back_populates="enrollment", cascade="all, delete-orphan")

class LearningProgress(Base):
    __tablename__ = "learning_progress"
    id = Column(String(36), primary_key=True)
    enrollment_id = Column(String(36), ForeignKey("course_enrollments.id"), nullable=False, index=True)
    lesson_id = Column(String(36), ForeignKey("learning_lessons.id"), nullable=False, index=True)
    status = Column(String(30), default="NOT_STARTED", nullable=False) # NOT_STARTED, IN_PROGRESS, COMPLETED
    watch_seconds = Column(Integer, default=0, nullable=False)
    last_playback_position_seconds = Column(Integer, default=0, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    quiz_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    enrollment = relationship("CourseEnrollment", back_populates="progress_records")

class AssignmentSubmission(Base):
    __tablename__ = "assignment_submissions"
    id = Column(String(36), primary_key=True)
    lesson_id = Column(String(36), ForeignKey("learning_lessons.id"), nullable=False, index=True)
    student_id = Column(String(36), nullable=False, index=True)
    submission_text = Column(Text, nullable=True)
    attachment_url = Column(String(500), nullable=True)
    submission_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String(30), default="SUBMITTED", nullable=False) # SUBMITTED, GRADED, RESUBMISSION_REQUESTED
    marks_obtained = Column(Float, nullable=True)
    max_marks = Column(Float, default=100.0, nullable=False)
    is_late = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class AssignmentFeedback(Base):
    __tablename__ = "assignment_feedback"
    id = Column(String(36), primary_key=True)
    submission_id = Column(String(36), ForeignKey("assignment_submissions.id"), nullable=False, index=True)
    evaluator_id = Column(String(36), nullable=False)
    feedback_text = Column(Text, nullable=False)
    rubric_scores = Column(JSONB, nullable=True)
    graded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class DiscussionTopic(Base):
    __tablename__ = "discussion_topics"
    id = Column(String(36), primary_key=True)
    course_id = Column(String(36), ForeignKey("learning_courses.id"), nullable=False, index=True)
    lesson_id = Column(String(36), ForeignKey("learning_lessons.id"), nullable=True)
    user_id = Column(String(36), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    is_pinned = Column(Boolean, default=False, nullable=False)
    is_closed = Column(Boolean, default=False, nullable=False)
    upvotes_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    posts = relationship("DiscussionPost", back_populates="topic", cascade="all, delete-orphan")

class DiscussionPost(Base):
    __tablename__ = "discussion_posts"
    id = Column(String(36), primary_key=True)
    topic_id = Column(String(36), ForeignKey("discussion_topics.id"), nullable=False, index=True)
    user_id = Column(String(36), nullable=False, index=True)
    parent_post_id = Column(String(36), ForeignKey("discussion_posts.id"), nullable=True)
    content = Column(Text, nullable=False)
    attachment_url = Column(String(500), nullable=True)
    is_endorsed_by_faculty = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    topic = relationship("DiscussionTopic", back_populates="posts")

class CourseAnnouncement(Base):
    __tablename__ = "course_announcements"
    id = Column(String(36), primary_key=True)
    course_id = Column(String(36), ForeignKey("learning_courses.id"), nullable=False, index=True)
    instructor_id = Column(String(36), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    target_batch_id = Column(String(36), nullable=True)
    is_scheduled = Column(Boolean, default=False, nullable=False)
    publish_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Bookmark(Base):
    __tablename__ = "bookmarks"
    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), nullable=False, index=True)
    lesson_id = Column(String(36), ForeignKey("learning_lessons.id"), nullable=False, index=True)
    timestamp_seconds = Column(Integer, default=0, nullable=False)
    note_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class LearningBadge(Base):
    __tablename__ = "learning_badges"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    badge_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    icon_url = Column(String(500), nullable=False)
    criteria_type = Column(String(50), nullable=False) # COURSE_COMPLETED, HOURS_SPENT, STREAK_DAYS, QUIZ_PERFECT
    criteria_value = Column(Float, default=1.0, nullable=False)
    xp_reward = Column(Integer, default=50, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class LearningAchievement(Base):
    __tablename__ = "learning_achievements"
    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), nullable=False, index=True)
    badge_id = Column(String(36), ForeignKey("learning_badges.id"), nullable=False)
    earned_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    xp_earned = Column(Integer, default=50, nullable=False)

class LearningReport(Base):
    __tablename__ = "learning_reports"
    id = Column(String(36), primary_key=True)
    institute_id = Column(String(36), nullable=False, index=True)
    report_name = Column(String(150), nullable=False)
    report_type = Column(String(50), nullable=False) # COMPLETION, ASSIGNMENT_AUDIT, LEARNER_HOURS, BATCH_PROGRESS
    filters = Column(JSONB, nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class LearningAnalytics(Base):
    __tablename__ = "learning_analytics"
    id = Column(String(36), primary_key=True)
    course_id = Column(String(36), ForeignKey("learning_courses.id"), nullable=False, index=True)
    date_key = Column(Date, nullable=False, index=True)
    active_learners_count = Column(Integer, default=0, nullable=False)
    average_watch_time_minutes = Column(Float, default=0.0, nullable=False)
    completion_rate = Column(Float, default=0.0, nullable=False)
    discussion_activity_count = Column(Integer, default=0, nullable=False)


class LmsDashboardPreference(Base):
    __tablename__ = "lms_dashboard_preferences"
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), nullable=False, index=True)
    role = Column(String(32), default="STUDENT", nullable=False, index=True)  # ROOT_OWNER, SUPER_ADMIN, LMS_ADMIN, PRINCIPAL, HOD, FACULTY, STUDENT, PARENT, FRANCHISE_CENTER
    pinned_widgets = Column(JSONB, nullable=True)
    layout_preferences = Column(JSONB, nullable=True)
    last_accessed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsProgram(Base):
    __tablename__ = "lms_programs"
    id = Column(String(36), primary_key=True)
    program_code = Column(String(50), nullable=False, unique=True, index=True)
    program_name = Column(String(255), nullable=False, index=True)
    department_id = Column(String(36), nullable=True)
    degree_level = Column(String(50), default="B_TECH", nullable=False)  # B_TECH, M_TECH, DIPLOMA, CERTIFICATION
    total_credits = Column(Float, default=160.0, nullable=False)
    duration_semesters = Column(Integer, default=8, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsCourseVersion(Base):
    __tablename__ = "lms_course_versions"
    id = Column(String(36), primary_key=True)
    course_id = Column(String(36), ForeignKey("learning_courses.id"), nullable=False, index=True)
    version_tag = Column(String(20), default="v1.0", nullable=False)
    changelog = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    credit_hours = Column(JSONB, nullable=True)  # {"theory": 3, "tutorial": 1, "practical": 2}
    semester_number = Column(Integer, default=5, nullable=False)
    prerequisites = Column(JSONB, nullable=True)  # ["CS-201", "CS-202"]
    learning_outcomes = Column(JSONB, nullable=True)  # [{"code": "CLO-1", "outcome": "...", "bloom_level": "APPLY"}]
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsLearningPath(Base):
    __tablename__ = "lms_learning_paths"
    id = Column(String(36), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    target_role = Column(String(100), default="Cloud & DevOps Architect", nullable=False)
    course_sequence = Column(JSONB, nullable=False)  # ["CS-301", "CS-304", "AI-402"]
    estimated_hours = Column(Float, default=120.0, nullable=False)
    badge_reward_id = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class LmsCourseBundle(Base):
    __tablename__ = "lms_course_bundles"
    id = Column(String(36), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    bundled_course_ids = Column(JSONB, nullable=False)  # ["crs_cs301", "crs_cs302", "crs_cs304"]
    pricing_tier = Column(String(50), default="ENTERPRISE_INSTITUTE", nullable=False)
    is_franchise_eligible = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class LmsLessonContent(Base):
    __tablename__ = "lms_lesson_contents"
    id = Column(String(36), primary_key=True)
    lesson_id = Column(String(36), ForeignKey("learning_lessons.id"), nullable=False, index=True)
    content_type = Column(String(50), nullable=False, index=True)  # RICH_TEXT, PDF, PPT, IMAGE, AUDIO, VIDEO, SCORM, HTML5, EXTERNAL_URL, EMBED_IFRAME, H5P_INTERACTIVE, CODE_PLAYGROUND
    title = Column(String(255), nullable=False)
    order_index = Column(Integer, default=1, nullable=False)
    content_payload = Column(JSONB, nullable=False)  # Stores content-specific payload (HTML, URL, manifest, code templates)
    is_mandatory = Column(Boolean, default=True, nullable=False)
    min_completion_time_seconds = Column(Integer, default=0, nullable=False)
    pass_score_percentage = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsScormPackage(Base):
    __tablename__ = "lms_scorm_packages"
    id = Column(String(36), primary_key=True)
    title = Column(String(255), nullable=False)
    scorm_version = Column(String(20), default="SCORM_1_2", nullable=False)  # SCORM_1_2, SCORM_2004_4TH_EDITION
    package_url = Column(String(500), nullable=False)
    manifest_json = Column(JSONB, nullable=False)
    launch_url = Column(String(500), nullable=False)
    mastery_score = Column(Float, default=80.0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class LmsVideoAsset(Base):
    __tablename__ = "lms_video_assets"
    id = Column(String(36), primary_key=True)
    lesson_id = Column(String(36), ForeignKey("learning_lessons.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    video_url = Column(String(500), nullable=False)
    hls_playlist_url = Column(String(500), nullable=True)
    duration_seconds = Column(Integer, default=0, nullable=False)
    resolutions = Column(JSONB, nullable=False, default=list)  # ["1080p", "720p", "480p", "360p"]
    thumbnail_url = Column(String(500), nullable=True)
    allow_download = Column(Boolean, default=False, nullable=False)
    watermark_enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class LmsVideoPlaybackSession(Base):
    __tablename__ = "lms_video_playback_sessions"
    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), nullable=False, index=True)
    video_id = Column(String(36), ForeignKey("lms_video_assets.id"), nullable=False, index=True)
    last_position_seconds = Column(Integer, default=0, nullable=False)
    total_watched_seconds = Column(Integer, default=0, nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    notes = Column(JSONB, default=list, nullable=False)  # [{"timestamp": 142, "text": "Paxos vs Raft log compaction"}]
    bookmarks = Column(JSONB, default=list, nullable=False)  # [{"timestamp": 310, "label": "Leader Election Protocol"}]
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsLiveClassSession(Base):
    __tablename__ = "lms_live_class_sessions"
    id = Column(String(36), primary_key=True)
    course_id = Column(String(36), ForeignKey("learning_courses.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    instructor_id = Column(String(36), nullable=False, index=True)
    instructor_name = Column(String(120), default="Dr. Rajeshwari Sharma", nullable=False)
    platform = Column(String(32), default="GOOGLE_MEET", nullable=False)  # ZOOM, GOOGLE_MEET, MS_TEAMS, JITSI
    meeting_url = Column(String(500), nullable=False)
    meeting_id = Column(String(100), nullable=False)
    passcode = Column(String(100), nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=90, nullable=False)
    status = Column(String(32), default="SCHEDULED", nullable=False)  # SCHEDULED, LIVE_NOW, CONCLUDED, CANCELLED
    recording_url = Column(String(500), nullable=True)
    recording_duration_seconds = Column(Integer, nullable=True)
    enable_chat = Column(Boolean, default=True, nullable=False)
    enable_polls = Column(Boolean, default=True, nullable=False)
    enable_whiteboard = Column(Boolean, default=True, nullable=False)
    enable_breakout_rooms = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsLiveClassAttendance(Base):
    __tablename__ = "lms_live_class_attendances"
    id = Column(String(36), primary_key=True)
    live_class_id = Column(String(36), ForeignKey("lms_live_class_sessions.id"), nullable=False, index=True)
    student_id = Column(String(36), nullable=False, index=True)
    roll_number = Column(String(48), nullable=False, index=True)
    candidate_name = Column(String(120), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    left_at = Column(DateTime, nullable=True)
    active_minutes = Column(Integer, default=0, nullable=False)
    attendance_status = Column(String(32), default="PRESENT", nullable=False)  # PRESENT, PARTIAL, ABSENT
    poll_responses_count = Column(Integer, default=0, nullable=False)
    raised_hand_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class LmsAssignment(Base):
    __tablename__ = "lms_assignments"
    id = Column(String(36), primary_key=True)
    course_id = Column(String(36), ForeignKey("learning_courses.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    max_score = Column(Float, default=100.0, nullable=False)
    due_date = Column(DateTime, nullable=False)
    cut_off_date = Column(DateTime, nullable=True)
    late_penalty_per_day_pct = Column(Float, default=5.0, nullable=False)
    is_group_assignment = Column(Boolean, default=False, nullable=False)
    max_group_size = Column(Integer, default=1, nullable=False)
    allowed_file_types = Column(JSONB, nullable=False)  # ["pdf", "zip", "go", "py"]
    max_file_size_mb = Column(Integer, default=50, nullable=False)
    rubric_schema = Column(JSONB, nullable=False)  # [{"criteria": "Architecture Design", "max_points": 25, "weight": 25.0}]
    attachment_urls = Column(JSONB, default=list, nullable=False)
    plagiarism_check_enabled = Column(Boolean, default=True, nullable=False)
    status = Column(String(32), default="PUBLISHED", nullable=False)  # DRAFT, PUBLISHED, CLOSED
    created_by = Column(String(36), default="inst_01", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsAssignmentSubmissionRecord(Base):
    __tablename__ = "lms_assignment_submissions_v2"
    id = Column(String(36), primary_key=True)
    assignment_id = Column(String(36), ForeignKey("lms_assignments.id"), nullable=False, index=True)
    student_id = Column(String(36), nullable=False, index=True)
    roll_number = Column(String(48), nullable=False, index=True)
    candidate_name = Column(String(120), nullable=False)
    group_name = Column(String(100), nullable=True)
    submission_text = Column(Text, nullable=True)
    uploaded_files = Column(JSONB, default=list, nullable=False)
    status = Column(String(32), default="SUBMITTED", nullable=False)  # DRAFT, SUBMITTED, EVALUATED, RESUBMISSION_REQUESTED
    submitted_at = Column(DateTime, nullable=True)
    is_late = Column(Boolean, default=False, nullable=False)
    late_penalty_applied_pct = Column(Float, default=0.0, nullable=False)
    score_awarded = Column(Float, nullable=True)
    rubric_evaluations = Column(JSONB, default=dict, nullable=False)
    similarity_score_pct = Column(Float, nullable=True)
    evaluator_feedback = Column(Text, nullable=True)
    evaluated_by = Column(String(36), nullable=True)
    evaluated_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsQuizConfig(Base):
    __tablename__ = "lms_quiz_configs"
    id = Column(String(36), primary_key=True)
    course_id = Column(String(36), ForeignKey("learning_courses.id"), nullable=False, index=True)
    module_id = Column(String(36), nullable=True)
    title = Column(String(160), nullable=False)
    quiz_type = Column(String(32), default="PRACTICE_TEST", nullable=False)  # PRACTICE_TEST, CHAPTER_QUIZ, WEEKLY_ASSESSMENT, ADAPTIVE_PRACTICE
    description = Column(Text, nullable=True)
    duration_minutes = Column(Integer, default=20, nullable=False)
    pass_percentage = Column(Float, default=60.0, nullable=False)
    max_attempts = Column(Integer, default=3, nullable=False)  # 0 or -1 for unlimited
    is_adaptive = Column(Boolean, default=False, nullable=False)
    instant_feedback = Column(Boolean, default=True, nullable=False)
    questions_count = Column(Integer, default=10, nullable=False)
    cbt_test_id = Column(String(36), nullable=True)  # Linked CBT test ID for reuse
    questions_payload = Column(JSONB, default=list, nullable=False)  # list of question objects
    xp_reward = Column(Integer, default=50, nullable=False)
    status = Column(String(32), default="PUBLISHED", nullable=False)  # DRAFT, PUBLISHED, ARCHIVED
    created_by = Column(String(36), default="fac_01", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsQuizAttemptRecord(Base):
    __tablename__ = "lms_quiz_attempts"
    id = Column(String(36), primary_key=True)
    quiz_id = Column(String(36), ForeignKey("lms_quiz_configs.id"), nullable=False, index=True)
    student_id = Column(String(36), nullable=False, index=True)
    roll_number = Column(String(48), nullable=False, index=True)
    candidate_name = Column(String(120), nullable=False)
    attempt_number = Column(Integer, default=1, nullable=False)
    score_obtained = Column(Float, default=0.0, nullable=False)
    max_score = Column(Float, default=100.0, nullable=False)
    percentage = Column(Float, default=0.0, nullable=False)
    is_passed = Column(Boolean, default=False, nullable=False)
    xp_awarded = Column(Integer, default=0, nullable=False)
    responses_payload = Column(JSONB, default=dict, nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    submitted_at = Column(DateTime, nullable=True)
    time_taken_seconds = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsDiscussionForum(Base):
    __tablename__ = "lms_discussion_forums"
    id = Column(String(36), primary_key=True)
    course_id = Column(String(36), ForeignKey("learning_courses.id"), nullable=False, index=True)
    title = Column(String(160), nullable=False)
    category = Column(String(48), default="GENERAL", nullable=False)  # ANNOUNCEMENT, GENERAL, FACULTY_QA, GROUP_DISCUSSION, PEER_LEARNING
    description = Column(Text, nullable=True)
    is_announcement = Column(Boolean, default=False, nullable=False)
    is_pinned = Column(Boolean, default=False, nullable=False)
    is_locked = Column(Boolean, default=False, nullable=False)
    allow_anonymous = Column(Boolean, default=False, nullable=False)
    created_by = Column(String(36), default="fac_01", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsDiscussionThread(Base):
    __tablename__ = "lms_discussion_threads"
    id = Column(String(36), primary_key=True)
    forum_id = Column(String(36), ForeignKey("lms_discussion_forums.id"), nullable=False, index=True)
    course_id = Column(String(36), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(String(36), nullable=False, index=True)
    author_name = Column(String(120), nullable=False)
    author_role = Column(String(32), default="STUDENT", nullable=False)  # FACULTY, STUDENT, TA, MODERATOR
    is_announcement = Column(Boolean, default=False, nullable=False)
    is_pinned = Column(Boolean, default=False, nullable=False)
    is_resolved = Column(Boolean, default=False, nullable=False)
    upvotes_count = Column(Integer, default=0, nullable=False)
    replies_count = Column(Integer, default=0, nullable=False)
    tags = Column(JSONB, default=list, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsDiscussionReply(Base):
    __tablename__ = "lms_discussion_replies"
    id = Column(String(36), primary_key=True)
    thread_id = Column(String(36), ForeignKey("lms_discussion_threads.id"), nullable=False, index=True)
    parent_reply_id = Column(String(36), nullable=True)
    author_id = Column(String(36), nullable=False, index=True)
    author_name = Column(String(120), nullable=False)
    author_role = Column(String(32), default="STUDENT", nullable=False)
    content = Column(Text, nullable=False)
    is_faculty_answer = Column(Boolean, default=False, nullable=False)
    is_accepted_answer = Column(Boolean, default=False, nullable=False)
    upvotes_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsCourseChatMessage(Base):
    __tablename__ = "lms_course_chat_messages"
    id = Column(String(36), primary_key=True)
    course_id = Column(String(36), nullable=False, index=True)
    sender_id = Column(String(36), nullable=False, index=True)
    sender_name = Column(String(120), nullable=False)
    sender_role = Column(String(32), default="STUDENT", nullable=False)
    message_text = Column(Text, nullable=False)
    attachments = Column(JSONB, default=list, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class LmsStudentEngagementRecord(Base):
    __tablename__ = "lms_student_engagements"
    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), nullable=False, index=True)
    roll_number = Column(String(48), nullable=False, index=True)
    candidate_name = Column(String(120), nullable=False)
    course_id = Column(String(36), ForeignKey("learning_courses.id"), nullable=False, index=True)
    lessons_completed_count = Column(Integer, default=0, nullable=False)
    total_lessons_count = Column(Integer, default=10, nullable=False)
    lesson_completion_pct = Column(Float, default=0.0, nullable=False)
    video_watch_time_minutes = Column(Float, default=0.0, nullable=False)
    live_classes_attended_count = Column(Integer, default=0, nullable=False)
    total_live_classes_count = Column(Integer, default=5, nullable=False)
    live_class_attendance_pct = Column(Float, default=0.0, nullable=False)
    assignments_submitted_count = Column(Integer, default=0, nullable=False)
    total_assignments_count = Column(Integer, default=4, nullable=False)
    assignment_submission_pct = Column(Float, default=0.0, nullable=False)
    quizzes_participated_count = Column(Integer, default=0, nullable=False)
    total_quizzes_count = Column(Integer, default=4, nullable=False)
    quiz_participation_pct = Column(Float, default=0.0, nullable=False)
    login_frequency_weekly = Column(Integer, default=0, nullable=False)
    total_study_time_hours = Column(Float, default=0.0, nullable=False)
    overall_engagement_score = Column(Float, default=0.0, nullable=False)
    learning_streak_days = Column(Integer, default=1, nullable=False)
    last_activity_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsActivityLogEntry(Base):
    __tablename__ = "lms_activity_logs"
    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), nullable=False, index=True)
    course_id = Column(String(36), nullable=False, index=True)
    activity_type = Column(String(48), nullable=False, index=True)  # LESSON_VIEW, VIDEO_WATCH, LIVE_CLASS_ATTENDED, ASSIGNMENT_SUBMISSION, QUIZ_ATTEMPT, FORUM_REPLY, LOGIN
    activity_title = Column(String(200), nullable=False)
    activity_details = Column(JSONB, default=dict, nullable=False)
    duration_seconds = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class LmsBadgeDefinition(Base):
    __tablename__ = "lms_badge_definitions"
    id = Column(String(36), primary_key=True)
    code = Column(String(48), unique=True, nullable=False, index=True)
    name = Column(String(120), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(48), default="SKILL_MASTERY", nullable=False)  # COURSE_COMPLETION, SKILL_MASTERY, STREAK, COMMUNITY, EXAMINATION
    icon_key = Column(String(64), default="award", nullable=False)
    xp_value = Column(Integer, default=50, nullable=False)
    criteria = Column(JSONB, default=dict, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsStudentBadgeAward(Base):
    __tablename__ = "lms_student_badge_awards"
    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), nullable=False, index=True)
    badge_id = Column(String(36), ForeignKey("lms_badge_definitions.id"), nullable=False, index=True)
    course_id = Column(String(36), nullable=True, index=True)
    awarded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    verification_hash = Column(String(64), nullable=False)


class LmsSkillMasteryRecord(Base):
    __tablename__ = "lms_skill_mastery_records"
    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), nullable=False, index=True)
    skill_name = Column(String(100), nullable=False, index=True)
    category = Column(String(64), default="Distributed Systems", nullable=False)
    mastery_level_pct = Column(Float, default=0.0, nullable=False)
    competency_status = Column(String(32), default="NOVICE", nullable=False)  # NOVICE, COMPETENT, PROFICIENT, MASTER
    practice_sessions_count = Column(Integer, default=0, nullable=False)
    last_assessed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsDigitalResource(Base):
    __tablename__ = "lms_digital_resources"
    id = Column(String(36), primary_key=True)
    course_id = Column(String(36), ForeignKey("learning_courses.id"), nullable=True, index=True)
    erp_book_id = Column(String(36), nullable=True, index=True)  # Integration with ERP LibraryBook
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(160), nullable=False)
    resource_type = Column(String(48), nullable=False, index=True)  # EBOOK, PDF, LECTURE_NOTES, PREVIOUS_PAPER, JOURNAL, VIDEO, RESEARCH_ARTICLE
    category = Column(String(64), nullable=False)
    file_url = Column(String(255), nullable=False)
    file_format = Column(String(16), default="pdf", nullable=False)
    file_size_mb = Column(Float, default=0.0, nullable=False)
    download_allowed = Column(Boolean, default=True, nullable=False)
    download_count = Column(Integer, default=0, nullable=False)
    view_count = Column(Integer, default=0, nullable=False)
    isbn = Column(String(32), nullable=True)
    doi = Column(String(64), nullable=True)
    publication_year = Column(Integer, default=2024, nullable=False)
    tags = Column(JSONB, default=list, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsDigitalResourceAccessLog(Base):
    __tablename__ = "lms_digital_resource_access_logs"
    id = Column(String(36), primary_key=True)
    resource_id = Column(String(36), ForeignKey("lms_digital_resources.id"), nullable=False, index=True)
    student_id = Column(String(36), nullable=False, index=True)
    roll_number = Column(String(48), nullable=False)
    action_type = Column(String(32), nullable=False)  # VIEW, DOWNLOAD
    accessed_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class LmsIssuedCertificate(Base):
    __tablename__ = "lms_issued_certificates"
    id = Column(String(36), primary_key=True)
    certificate_number = Column(String(64), unique=True, nullable=False, index=True)
    student_id = Column(String(36), nullable=False, index=True)
    roll_number = Column(String(48), nullable=False, index=True)
    candidate_name = Column(String(120), nullable=False)
    course_id = Column(String(36), ForeignKey("learning_courses.id"), nullable=False, index=True)
    course_name = Column(String(255), nullable=False)
    certificate_type = Column(String(48), default="COURSE_COMPLETION", nullable=False)  # COURSE_COMPLETION, SKILL_MASTERY, HONORS_CREDENTIAL, BOOTCAMP_DIPLOMA
    issue_date = Column(Date, default=date.today, nullable=False)
    completion_percentage = Column(Float, default=100.0, nullable=False)
    grade_or_score = Column(String(32), default="O (Outstanding)", nullable=False)
    verification_code = Column(String(64), unique=True, nullable=False, index=True)
    qr_payload = Column(Text, nullable=False)
    digital_signature_hash = Column(String(64), nullable=False)
    pdf_download_url = Column(String(255), nullable=True)
    status = Column(String(32), default="ISSUED", nullable=False)  # ISSUED, REVOKED
    issued_by = Column(String(120), default="Registrar & Director of Academics, MEI-HQ Indore", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsDigitalCredentialRecord(Base):
    __tablename__ = "lms_digital_credentials"
    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), nullable=False, index=True)
    credential_title = Column(String(160), nullable=False)
    credential_type = Column(String(48), nullable=False)  # BADGE, MICRO_CREDENTIAL, CERTIFICATE
    issuer = Column(String(120), default="MY EDUCATION INDIA Autonomous Campus", nullable=False)
    skills_covered = Column(JSONB, default=list, nullable=False)
    issued_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    verification_url = Column(String(255), nullable=False)
    qr_code_svg = Column(Text, nullable=True)


class LmsParentWardMapping(Base):
    __tablename__ = "lms_parent_ward_mappings"
    id = Column(String(36), primary_key=True)
    parent_user_id = Column(String(36), nullable=False, index=True)
    parent_name = Column(String(120), nullable=False)
    parent_phone = Column(String(20), nullable=False)
    parent_email = Column(String(120), nullable=False)
    student_id = Column(String(36), nullable=False, index=True)
    roll_number = Column(String(48), nullable=False, index=True)
    relationship = Column(String(32), default="FATHER", nullable=False)
    is_verified = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsFacultyStudentFeedback(Base):
    __tablename__ = "lms_faculty_feedbacks"
    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), nullable=False, index=True)
    roll_number = Column(String(48), nullable=False, index=True)
    course_id = Column(String(36), ForeignKey("learning_courses.id"), nullable=False, index=True)
    faculty_id = Column(String(36), nullable=False, index=True)
    faculty_name = Column(String(120), nullable=False)
    feedback_type = Column(String(32), default="ACADEMIC", nullable=False)  # ACADEMIC, ATTENDANCE_CONCERN, PRAISE, DISCIPLINARY
    feedback_text = Column(Text, nullable=False)
    visible_to_parent = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class LmsParentNotification(Base):
    __tablename__ = "lms_parent_notifications"
    id = Column(String(36), primary_key=True)
    parent_user_id = Column(String(36), nullable=False, index=True)
    student_id = Column(String(36), nullable=False, index=True)
    title = Column(String(160), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(32), default="GENERAL", nullable=False)  # ATTENDANCE_SHORTAGE, ASSIGNMENT_DUE, RESULT_PUBLISHED, LIVE_CLASS_MISSED, GENERAL
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class LmsFacultyProfile(Base):
    __tablename__ = "lms_faculty_profiles"
    id = Column(String(36), primary_key=True)
    faculty_id = Column(String(36), unique=True, nullable=False, index=True)
    full_name = Column(String(120), nullable=False)
    designation = Column(String(64), default="Associate Professor", nullable=False)
    department = Column(String(100), default="Computer Science & Engineering", nullable=False)
    specialization = Column(String(160), default="Distributed Systems, Consensus & Storage Architecture", nullable=False)
    office_hours = Column(String(100), default="Mon, Wed 15:00 - 17:00 IST", nullable=False)
    virtual_office_room_url = Column(String(255), default="https://meet.google.com/mei-fac-01", nullable=False)
    bio = Column(Text, nullable=True)
    total_active_courses = Column(Integer, default=2, nullable=False)
    total_enrolled_students = Column(Integer, default=184, nullable=False)
    rating = Column(Float, default=4.9, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsFacultyGradingQueueItem(Base):
    __tablename__ = "lms_faculty_grading_queue"
    id = Column(String(36), primary_key=True)
    faculty_id = Column(String(36), nullable=False, index=True)
    submission_id = Column(String(36), nullable=False, index=True)
    assignment_id = Column(String(36), nullable=False, index=True)
    assignment_title = Column(String(255), nullable=False)
    course_id = Column(String(36), nullable=False, index=True)
    student_id = Column(String(36), nullable=False, index=True)
    roll_number = Column(String(48), nullable=False, index=True)
    candidate_name = Column(String(120), nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    similarity_score_pct = Column(Float, default=0.0, nullable=False)
    status = Column(String(32), default="PENDING", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class LmsStudentLearningCockpit(Base):
    __tablename__ = "lms_student_cockpits"
    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), unique=True, nullable=False, index=True)
    roll_number = Column(String(48), unique=True, nullable=False, index=True)
    candidate_name = Column(String(120), nullable=False)
    active_term = Column(String(32), default="Semester V (2026-27)", nullable=False)
    preferred_language = Column(String(20), default="en", nullable=False)
    offline_sync_enabled = Column(Boolean, default=True, nullable=False)
    study_goal_hours_weekly = Column(Float, default=15.0, nullable=False)
    current_streak_days = Column(Integer, default=12, nullable=False)
    longest_streak_days = Column(Integer, default=16, nullable=False)
    total_xp_earned = Column(Integer, default=1450, nullable=False)
    current_tier = Column(String(32), default="GOLD", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsStudentBookmarkedResource(Base):
    __tablename__ = "lms_student_bookmarks"
    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), nullable=False, index=True)
    resource_id = Column(String(36), nullable=False, index=True)
    resource_title = Column(String(255), nullable=False)
    resource_type = Column(String(48), nullable=False)  # VIDEO, LESSON, EBOOK, NOTE, EXAM_PAPER
    target_url = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class LmsAiTutorConversation(Base):
    __tablename__ = "lms_ai_conversations"
    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), nullable=False, index=True)
    course_id = Column(String(36), nullable=True, index=True)
    session_title = Column(String(160), default="AI Tutor Concept Clarification", nullable=False)
    messages_payload = Column(JSONB, default=list, nullable=False)
    weak_topic_tagged = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsAiFlashcardDeck(Base):
    __tablename__ = "lms_ai_flashcard_decks"
    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), nullable=False, index=True)
    course_id = Column(String(36), nullable=False, index=True)
    deck_title = Column(String(160), nullable=False)
    topic = Column(String(100), nullable=False)
    cards_payload = Column(JSONB, default=list, nullable=False)
    total_cards_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class LmsAiStudyPlan(Base):
    __tablename__ = "lms_ai_study_plans"
    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), nullable=False, index=True)
    course_id = Column(String(36), nullable=False, index=True)
    target_exam_date = Column(Date, nullable=False)
    weekly_hours_allocated = Column(Float, default=15.0, nullable=False)
    milestones_payload = Column(JSONB, default=list, nullable=False)
    status = Column(String(32), default="ACTIVE", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class LmsMobileDeviceRegistration(Base):
    __tablename__ = "lms_mobile_device_registrations"
    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), nullable=False, index=True)
    roll_number = Column(String(48), nullable=False, index=True)
    device_os = Column(String(32), nullable=False)  # ANDROID, IOS, HARMONYOS, WEAROS
    device_model = Column(String(120), nullable=False)
    device_token = Column(String(255), unique=True, nullable=False, index=True)
    app_version = Column(String(32), default="v3.4.0", nullable=False)
    push_notifications_enabled = Column(Boolean, default=True, nullable=False)
    biometric_login_enabled = Column(Boolean, default=True, nullable=False)
    last_sync_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsOfflineDownloadedAsset(Base):
    __tablename__ = "lms_offline_downloaded_assets"
    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), nullable=False, index=True)
    device_token = Column(String(255), nullable=False, index=True)
    resource_id = Column(String(36), nullable=False, index=True)
    resource_title = Column(String(255), nullable=False)
    resource_type = Column(String(48), nullable=False)  # VIDEO, LESSON_SCORM, EBOOK, PDF_NOTES
    file_size_mb = Column(Float, default=0.0, nullable=False)
    download_status = Column(String(32), default="COMPLETED", nullable=False)  # DOWNLOADING, COMPLETED, EXPIRED
    expiry_date = Column(DateTime, nullable=True)
    downloaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class LmsMobileSyncSession(Base):
    __tablename__ = "lms_mobile_sync_sessions"
    id = Column(String(36), primary_key=True)
    student_id = Column(String(36), nullable=False, index=True)
    device_token = Column(String(255), nullable=False)
    sync_type = Column(String(32), default="BACKGROUND", nullable=False)  # BACKGROUND, MANUAL_DELTA, FULL
    records_synced_count = Column(Integer, default=0, nullable=False)
    sync_payload = Column(JSONB, default=dict, nullable=False)
    status = Column(String(32), default="SUCCESS", nullable=False)
    synced_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class LmsAnalyticsReportArchive(Base):
    __tablename__ = "lms_analytics_report_archives"
    id = Column(String(36), primary_key=True)
    report_code = Column(String(48), unique=True, nullable=False, index=True)
    report_type = Column(String(48), nullable=False, index=True)  # STUDENT_PROGRESS, FACULTY_PERFORMANCE, COURSE_COMPLETION, ASSIGNMENT_STATISTICS, QUIZ_PERFORMANCE, ENGAGEMENT_TRENDS, LMS_USAGE, DEPARTMENT_REPORT
    title = Column(String(200), nullable=False)
    department = Column(String(100), default="Computer Science & Engineering", nullable=False)
    academic_year = Column(String(32), default="2026-27", nullable=False)
    parameters = Column(JSONB, default=dict, nullable=False)
    metrics_payload = Column(JSONB, default=dict, nullable=False)
    export_format = Column(String(16), default="PDF", nullable=False)
    download_url = Column(String(255), nullable=True)
    generated_by = Column(String(120), default="Dean of Academic Computing, MEI-HQ Indore", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class LmsDepartmentPerformanceMetric(Base):
    __tablename__ = "lms_department_metrics"
    id = Column(String(36), primary_key=True)
    department = Column(String(100), unique=True, nullable=False, index=True)
    total_courses = Column(Integer, default=0, nullable=False)
    total_faculty = Column(Integer, default=0, nullable=False)
    total_students = Column(Integer, default=0, nullable=False)
    average_completion_rate = Column(Float, default=0.0, nullable=False)
    average_attendance_pct = Column(Float, default=0.0, nullable=False)
    active_learning_hours = Column(Float, default=0.0, nullable=False)
    certifications_issued = Column(Integer, default=0, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsSystemIntegrationConnector(Base):
    __tablename__ = "lms_system_connectors"
    id = Column(String(36), primary_key=True)
    system_name = Column(String(64), unique=True, nullable=False, index=True)
    display_name = Column(String(120), nullable=False)
    connector_type = Column(String(32), default="INTERNAL_RPC", nullable=False)  # INTERNAL_RPC, REST_WEBHOOK, OAUTH2, S3_COMPATIBLE
    endpoint_url = Column(String(255), nullable=False)
    status = Column(String(32), default="CONNECTED", nullable=False)  # CONNECTED, SYNCING, ERROR, DISABLED
    latency_ms = Column(Float, default=12.5, nullable=False)
    last_heartbeat_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    config_payload = Column(JSONB, default=dict, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class LmsGlobalSearchIndexEntry(Base):
    __tablename__ = "lms_global_search_index"
    id = Column(String(36), primary_key=True)
    entity_type = Column(String(48), nullable=False, index=True)  # COURSE, LESSON, ASSIGNMENT, QUIZ, EBOOK, RESEARCH_PAPER, FACULTY, FORUM_THREAD
    entity_id = Column(String(36), nullable=False, index=True)
    course_id = Column(String(36), nullable=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    snippet = Column(Text, nullable=False)
    target_route = Column(String(255), nullable=False)
    tags = Column(JSONB, default=list, nullable=False)
    indexed_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class LmsPaymentTransaction(Base):
    __tablename__ = "lms_payment_transactions"
    id = Column(String(36), primary_key=True)
    transaction_number = Column(String(64), unique=True, nullable=False, index=True)
    student_id = Column(String(36), nullable=False, index=True)
    course_id = Column(String(36), ForeignKey("learning_courses.id"), nullable=False, index=True)
    amount_inr = Column(Float, default=0.0, nullable=False)
    gateway_provider = Column(String(32), default="RAZORPAY", nullable=False)  # RAZORPAY, STRIPE, UPI_AUTOPAY
    payment_status = Column(String(32), default="PAID", nullable=False)  # INITIATED, PAID, FAILED, REFUNDED
    payment_method = Column(String(32), default="UPI", nullable=False)  # UPI, NET_BANKING, DEBIT_CARD, CREDIT_CARD
    receipt_url = Column(String(255), nullable=True)
    paid_at = Column(DateTime, default=datetime.utcnow, nullable=False)
