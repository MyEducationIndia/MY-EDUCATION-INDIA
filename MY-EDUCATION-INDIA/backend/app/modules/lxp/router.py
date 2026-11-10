from app.modules.lxp.production_readiness_service import LmsProductionReadinessService
from app.modules.lxp.schemas import (
    LmsProductionReadinessAuditResponse, LmsE2ETestResultResponse,
    LmsSystemHealthScorecardResponse,
)
from app.modules.lxp.enterprise_integrations_service import LmsEnterpriseIntegrationsService
from app.modules.lxp.schemas import (
    LmsSystemIntegrationConnectorResponse, LmsConnectorHealthCheckResponse,
    LmsGlobalSearchItemResponse, LmsPaymentInitiateRequest,
    LmsPaymentTransactionResponse,
)
from app.modules.lxp.analytics_reports_service import LmsAnalyticsReportsService
from app.modules.lxp.schemas import (
    LmsAnalyticsReportGenerateRequest, LmsAnalyticsReportArchiveResponse,
    LmsDepartmentMetricResponse, LmsGlobalReportingDashboardResponse,
)
from app.modules.lxp.mobile_learning_service import LmsMobileLearningService
from app.modules.lxp.schemas import (
    LmsMobileDeviceRegisterRequest, LmsMobileDeviceRegistrationResponse,
    LmsMobileDownloadAssetRequest, LmsOfflineDownloadedAssetResponse,
    LmsMobileSyncRequest, LmsMobileSyncSessionResponse,
)
from app.modules.lxp.ai_learning_assistant_service import LmsAiLearningAssistantService
from app.modules.lxp.schemas import (
    LmsAiTutorQueryRequest, LmsAiTutorQueryResponse,
    LmsAiFlashcardGenerateRequest, LmsAiFlashcardDeckResponse,
    LmsAiSummarizeNotesRequest, LmsAiSummarizeNotesResponse,
    LmsAiStudyPlanResponse,
)
from app.modules.lxp.student_portal_service import LmsStudentPortalService
from app.modules.lxp.schemas import (
    LmsStudentCockpitResponse, LmsStudentBookmarkCreate,
    LmsStudentBookmarkResponse, LmsStudentEnrolledCourseItem,
    LmsStudentUnifiedDashboardResponse,
)
from app.modules.lxp.faculty_portal_service import LmsFacultyPortalService
from app.modules.lxp.schemas import (
    LmsFacultyProfileResponse, LmsFacultyGradingQueueItemResponse,
    LmsFacultyCourseSummary, LmsFacultyWorkspaceOverviewResponse,
)
from app.modules.lxp.parent_portal_service import LmsParentPortalService
from app.modules.lxp.schemas import (
    LmsParentWardResponse, LmsParentOverviewResponse,
    LmsFacultyStudentFeedbackCreate, LmsFacultyStudentFeedbackResponse,
    LmsParentNotificationResponse,
)
from app.modules.lxp.certificates_badges_service import LmsCertificatesBadgesService
from app.modules.lxp.schemas import (
    LmsCertificateIssueRequest, LmsCertificateResponse,
    LmsCertificateVerifyResponse, LmsDigitalCredentialResponse,
)
from app.modules.lxp.digital_library_service import LmsDigitalLibraryService
from app.modules.lxp.schemas import (
    LmsDigitalResourceCreate, LmsDigitalResourceResponse,
    LmsDigitalResourceAccessLogResponse, LmsDigitalLibraryCategorySummary,
)
from app.modules.lxp.progress_analytics_service import LmsProgressAnalyticsService
from app.modules.lxp.schemas import (
    LmsBadgeDefinitionCreate, LmsBadgeDefinitionResponse,
    LmsStudentBadgeAwardResponse, LmsSkillMasteryResponse,
    LmsGamificationProfileResponse, LmsFacultyAnalyticsOverviewResponse,
)
from app.modules.lxp.attendance_engagement_service import LmsAttendanceEngagementService
from app.modules.lxp.schemas import (
    LmsStudentEngagementResponse, LmsActivityLogCreate,
    LmsActivityLogResponse, LmsCourseCohortEngagementSummary,
    LmsEngagementMetricUpdate,
)
from app.modules.lxp.discussion_collaboration_service import LmsDiscussionCollaborationService
from app.modules.lxp.schemas import (
    LmsDiscussionForumCreate, LmsDiscussionForumResponse,
    LmsDiscussionThreadCreate, LmsDiscussionThreadResponse,
    LmsDiscussionReplyCreate, LmsDiscussionReplyResponse,
    LmsCourseChatMessageCreate, LmsCourseChatMessageResponse,
)
from app.modules.lxp.quiz_practice_service import LmsQuizPracticeService
from app.modules.lxp.schemas import (
    LmsQuizConfigCreate, LmsQuizConfigResponse,
    LmsQuizSubmitAttemptRequest, LmsQuizAttemptResponse,
)
from app.modules.lxp.assignment_management_service import LmsAssignmentManagementService
from app.modules.lxp.schemas import (
    LmsAssignmentCreate, LmsAssignmentResponse,
    LmsAssignmentSubmissionCreate, LmsAssignmentSubmissionResponse,
    LmsAssignmentGradeRequest,
)

from app.modules.lxp.live_classes_service import LmsLiveClassesService
from app.modules.lxp.schemas import (
    LmsLiveClassSessionCreate, LmsLiveClassSessionResponse,
    LmsLiveClassAttendanceRecord, LmsLiveClassAttendanceResponse,
    LmsLiveClassJoinResponse,
)

from app.modules.lxp.video_learning_service import LmsVideoLearningService
from app.modules.lxp.schemas import (
    LmsVideoAssetCreate, LmsVideoAssetResponse,
    LmsVideoPlaybackProgressUpdate, LmsVideoPlaybackSessionResponse,
    LmsVideoNoteCreate, LmsVideoBookmarkCreate,
)

from app.modules.lxp.lesson_builder_service import LmsLessonBuilderService
from app.modules.lxp.schemas import (
    LmsLessonContentCreate, LmsLessonContentResponse,
    LmsScormPackageCreate, LmsScormPackageResponse,
    LessonBuilderPreviewResponse,
)

from app.modules.lxp.course_management_service import LmsCourseManagementService
from app.modules.lxp.schemas import (
    LmsProgramCreate, LmsProgramResponse,
    LmsCourseVersionCreate, LmsCourseVersionResponse,
    LmsLearningPathCreate, LmsLearningPathResponse,
    LmsCourseBundleCreate, LmsCourseBundleResponse,
)

from app.modules.lxp.dashboard_service import LmsDashboardService
from app.modules.lxp.schemas import (
    LmsRoleDashboardResponse,
    LmsDashboardPreferenceUpdate,
)

"""
Module 15: LXP FastAPI Router
Mounted under /api/v1/lxp/
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Any, Dict, List, Optional
from app.modules.lxp.schemas import (
    LearningCourseCreate, LearningCourseResponse,
    LearningModuleCreate, LearningModuleResponse,
    LearningLessonCreate, LearningLessonResponse,
    CourseEnrollmentRequest, CourseEnrollmentResponse,
    LessonProgressUpdate, LXPDashboardMetrics
)

lxp_router = APIRouter(prefix="/lxp", tags=["Enterprise Learning Experience Platform (LXP)"])

@lxp_router.get("/health")
async def lxp_health():
    return {"status": "healthy", "module": "Module 15 - Enterprise Learning Experience Platform (LXP)"}

@lxp_router.get("/dashboard/metrics", response_model=LXPDashboardMetrics)
async def get_dashboard_metrics(student_id: str = "std_default"):
    return {
        "total_enrolled_courses": 6,
        "active_courses": 4,
        "completed_courses": 2,
        "total_learning_hours": 42.5,
        "upcoming_assignments_count": 3,
        "average_quiz_score": 88.5,
        "xp_points": 1450,
        "streak_days": 12
    }

@lxp_router.get("/courses")
async def list_courses(category: Optional[str] = None):
    return [
        {
            "id": "crs_1",
            "course_code": "CS-301",
            "course_name": "Distributed Systems & Cloud Architecture",
            "description": "Enterprise microservices, consensus protocols, and Kubernetes orchestration",
            "category": "Computer Science",
            "difficulty": "ADVANCED",
            "language": "English",
            "duration_minutes": 2400,
            "instructor_id": "inst_01",
            "status": "PUBLISHED",
            "visibility": "PUBLIC",
            "is_free": True,
            "thumbnail_url": "/assets/courses/cs301.png"
        },
        {
            "id": "crs_2",
            "course_code": "AI-402",
            "course_name": "Machine Learning Foundations & PyTorch",
            "description": "Supervised learning, deep neural networks, and reinforcement learning pipelines",
            "category": "Artificial Intelligence",
            "difficulty": "INTERMEDIATE",
            "language": "English",
            "duration_minutes": 1800,
            "instructor_id": "inst_02",
            "status": "PUBLISHED",
            "visibility": "PUBLIC",
            "is_free": True,
            "thumbnail_url": "/assets/courses/ai402.png"
        }
    ]

@lxp_router.get("/courses/{course_id}/modules")
async def get_course_modules(course_id: str):
    return [
        {
            "id": "mod_1",
            "course_id": course_id,
            "module_title": "Module 1: Introduction to Distributed Systems",
            "order_index": 1,
            "duration_minutes": 180,
            "is_published": True,
            "lessons": [
                {
                    "id": "lsn_1",
                    "module_id": "mod_1",
                    "lesson_title": "1.1 Fallacies of Distributed Computing",
                    "lesson_type": "VIDEO",
                    "duration_seconds": 1200,
                    "order_index": 1,
                    "is_preview": True
                },
                {
                    "id": "lsn_2",
                    "module_id": "mod_1",
                    "lesson_title": "1.2 CAP Theorem & Eventual Consistency",
                    "lesson_type": "PDF",
                    "duration_seconds": 600,
                    "order_index": 2,
                    "is_preview": False
                }
            ]
        }
    ]


# ============================================================================
# PHASE 5 MODULE 1: LMS MULTI-ROLE DASHBOARD ENDPOINTS
# ============================================================================

@lxp_router.get("/dashboard/role-view", response_model=LmsRoleDashboardResponse)
async def get_lms_role_dashboard_view(
    role: str = Query("STUDENT", description="ROOT_OWNER, SUPER_ADMIN, LMS_ADMIN, PRINCIPAL, HOD, FACULTY, STUDENT, PARENT, FRANCHISE_CENTER"),
) -> LmsRoleDashboardResponse:
    """Retrieves unified role-specific dashboard with 9 interactive LMS widgets."""
    return await LmsDashboardService.get_role_dashboard(None, role=role)


@lxp_router.get("/dashboard/roles")
async def list_lms_supported_dashboard_roles():
    """Lists all 9 supported institutional LMS dashboard roles."""
    return LmsDashboardService.ROLES


@lxp_router.post("/dashboard/preferences")
async def update_lms_dashboard_preferences(
    payload: LmsDashboardPreferenceUpdate,
):
    """Saves customized widget layout and pinned widgets for the current user role."""
    return {
        "status": "SAVED",
        "role": payload.role,
        "pinned_widgets": payload.pinned_widgets,
        "updated_at": "2026-11-10T18:45:00Z"
    }


# ============================================================================
# PHASE 5 MODULE 2: LMS COURSE MANAGEMENT ENDPOINTS
# ============================================================================

@lxp_router.get("/course-management/programs", response_model=List[LmsProgramResponse])
async def list_lms_programs():
    """Lists academic degree programs offered in the LMS ecosystem."""
    return await LmsCourseManagementService.list_programs()


@lxp_router.post("/course-management/programs", response_model=LmsProgramResponse, status_code=status.HTTP_201_CREATED)
async def create_lms_program(payload: LmsProgramCreate):
    """Creates a new academic program container."""
    return await LmsCourseManagementService.create_program(payload)


@lxp_router.get("/course-management/courses/{course_id}/versions", response_model=List[LmsCourseVersionResponse])
async def list_course_versions(course_id: str):
    """Retrieves syllabus revisions, credit hours, prerequisites, and learning outcomes for a course."""
    return await LmsCourseManagementService.list_course_versions(course_id)


@lxp_router.post("/course-management/courses/{course_id}/versions", response_model=LmsCourseVersionResponse, status_code=status.HTTP_201_CREATED)
async def create_course_version(course_id: str, payload: LmsCourseVersionCreate):
    """Authors and releases a new versioned syllabus revision for a course."""
    payload.course_id = course_id
    return await LmsCourseManagementService.create_course_version(payload)


@lxp_router.get("/course-management/learning-paths", response_model=List[LmsLearningPathResponse])
async def list_lms_learning_paths():
    """Lists multi-course career tracks and learning paths."""
    return await LmsCourseManagementService.list_learning_paths()


@lxp_router.post("/course-management/learning-paths", response_model=LmsLearningPathResponse, status_code=status.HTTP_201_CREATED)
async def create_lms_learning_path(payload: LmsLearningPathCreate):
    """Assembles a new multi-course career progression path."""
    return await LmsCourseManagementService.create_learning_path(payload)


@lxp_router.get("/course-management/bundles", response_model=List[LmsCourseBundleResponse])
async def list_lms_course_bundles():
    """Lists packaged course bundles for departments and franchise centers."""
    return await LmsCourseManagementService.list_course_bundles()


@lxp_router.post("/course-management/bundles", response_model=LmsCourseBundleResponse, status_code=status.HTTP_201_CREATED)
async def create_lms_course_bundle(payload: LmsCourseBundleCreate):
    """Creates a bundled curriculum package for institutes or franchise commercial licensing."""
    return await LmsCourseManagementService.create_course_bundle(payload)


# ============================================================================
# PHASE 5 MODULE 3: LMS LESSON BUILDER ENDPOINTS
# ============================================================================

@lxp_router.get("/lesson-builder/lessons/{lesson_id}/contents", response_model=List[LmsLessonContentResponse])
async def list_lesson_contents(lesson_id: str):
    """Lists ordered multi-format content blocks for a lesson (Rich Text, Video, PDF, SCORM, H5P, Code Playground)."""
    return await LmsLessonBuilderService.list_lesson_contents(lesson_id)


@lxp_router.post("/lesson-builder/lessons/{lesson_id}/contents", response_model=LmsLessonContentResponse, status_code=status.HTTP_201_CREATED)
async def create_lesson_content(lesson_id: str, payload: LmsLessonContentCreate):
    """Appends a new multi-format content block to a lesson sequence."""
    payload.lesson_id = lesson_id
    return await LmsLessonBuilderService.create_lesson_content(payload)


@lxp_router.put("/lesson-builder/contents/{content_id}", response_model=LmsLessonContentResponse)
async def update_lesson_content_block(content_id: str, payload: Dict[str, Any]):
    """Updates content block parameters, completion gating criteria, or display payload."""
    return await LmsLessonBuilderService.update_lesson_content(content_id, payload)


@lxp_router.delete("/lesson-builder/contents/{content_id}")
async def delete_lesson_content_block(content_id: str):
    """Removes a content block from the lesson."""
    return await LmsLessonBuilderService.delete_lesson_content(content_id)


@lxp_router.get("/lesson-builder/scorm/packages", response_model=List[LmsScormPackageResponse])
async def list_scorm_packages():
    """Lists imported SCORM 1.2 and 2004 e-learning packages."""
    return await LmsLessonBuilderService.list_scorm_packages()


@lxp_router.post("/lesson-builder/scorm/upload", response_model=LmsScormPackageResponse, status_code=status.HTTP_201_CREATED)
async def upload_scorm_package(payload: LmsScormPackageCreate):
    """Registers and unpacks SCORM zip package with parsed manifest."""
    return await LmsLessonBuilderService.upload_scorm_package(payload)


@lxp_router.get("/lesson-builder/lessons/{lesson_id}/preview", response_model=LessonBuilderPreviewResponse)
async def get_lesson_learner_preview(lesson_id: str):
    """Renders full lesson preview mode for student learner experience."""
    return await LmsLessonBuilderService.get_lesson_preview(lesson_id)


# ============================================================================
# PHASE 5 MODULE 4: LMS VIDEO LEARNING ENDPOINTS
# ============================================================================

@lxp_router.get("/video-learning/assets", response_model=List[LmsVideoAssetResponse])
async def list_video_assets():
    """Lists streaming video assets with adaptive bitrate profiles and DRM rules."""
    return await LmsVideoLearningService.list_video_assets()


@lxp_router.post("/video-learning/assets", response_model=LmsVideoAssetResponse, status_code=status.HTTP_201_CREATED)
async def register_video_asset(payload: LmsVideoAssetCreate):
    """Registers new video asset with HLS playlist and resolution variants."""
    now = datetime.utcnow()
    return {
        "id": f"vid_{uuid.uuid4().hex[:8]}",
        "lesson_id": payload.lesson_id,
        "title": payload.title,
        "video_url": payload.video_url,
        "hls_playlist_url": payload.hls_playlist_url or f"{payload.video_url}.m3u8",
        "duration_seconds": payload.duration_seconds,
        "resolutions": payload.resolutions,
        "thumbnail_url": payload.thumbnail_url,
        "allow_download": payload.allow_download,
        "watermark_enabled": payload.watermark_enabled,
        "created_at": now,
    }


@lxp_router.get("/video-learning/playback/{video_id}", response_model=LmsVideoPlaybackSessionResponse)
async def get_video_playback_session(
    video_id: str,
    student_id: str = Query("std_default"),
):
    """Retrieves resume playback point, synchronized timestamp notes, and bookmarks."""
    return await LmsVideoLearningService.get_playback_session(student_id, video_id)


@lxp_router.post("/video-learning/playback/progress", response_model=LmsVideoPlaybackSessionResponse)
async def update_video_playback_progress(payload: LmsVideoPlaybackProgressUpdate):
    """Updates watch progress, last position, and assesses 90% completion gate."""
    return await LmsVideoLearningService.update_playback_progress(payload)


@lxp_router.post("/video-learning/playback/notes")
async def add_timestamp_note_to_video(payload: LmsVideoNoteCreate):
    """Pins synchronized timestamp note to video timeline."""
    return await LmsVideoLearningService.add_note(payload)


@lxp_router.post("/video-learning/playback/bookmarks")
async def add_chapter_bookmark_to_video(payload: LmsVideoBookmarkCreate):
    """Pins landmark chapter bookmark to video timeline."""
    return await LmsVideoLearningService.add_bookmark(payload)


@lxp_router.get("/video-learning/watch-history")
async def get_student_watch_history(student_id: str = Query("std_default")):
    """Retrieves student watch history, completion records, and engagement log."""
    return await LmsVideoLearningService.get_watch_history(student_id)


# ============================================================================
# PHASE 5 MODULE 5: LMS LIVE CLASSES ENDPOINTS
# ============================================================================

@lxp_router.get("/live-classes/sessions", response_model=List[LmsLiveClassSessionResponse])
async def list_live_classes(
    course_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
):
    """Lists scheduled, active, and concluded live class sessions across Zoom, Meet, Teams, and Jitsi."""
    return await LmsLiveClassesService.list_live_classes(course_id=course_id, status=status)


@lxp_router.post("/live-classes/sessions", response_model=LmsLiveClassSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_live_class(payload: LmsLiveClassSessionCreate):
    """Schedules a new interactive live video class with selected conferencing integration."""
    return await LmsLiveClassesService.create_live_class(payload)


@lxp_router.get("/live-classes/sessions/{session_id}", response_model=LmsLiveClassSessionResponse)
async def get_live_class_details(session_id: str):
    """Retrieves full metadata, meeting credentials, and feature flags for a live class."""
    session = await LmsLiveClassesService.get_live_class(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Live class session not found")
    return session


@lxp_router.post("/live-classes/sessions/{session_id}/join", response_model=LmsLiveClassJoinResponse)
async def join_live_class_session(
    session_id: str,
    student_id: str = Query("std_default"),
    roll_number: str = Query("MEI2024CS001"),
    name: str = Query("Aarav Sharma"),
):
    """Logs student join entry in attendance audit and provides direct launch URL."""
    return await LmsLiveClassesService.join_live_class(session_id, student_id, roll_number, name)


@lxp_router.post("/live-classes/sessions/{session_id}/attendance", response_model=LmsLiveClassAttendanceResponse)
async def record_live_class_attendance(
    session_id: str,
    payload: LmsLiveClassAttendanceRecord,
):
    """Records real-time engagement telemetry: active minutes, poll answers, and hand raises."""
    payload.live_class_id = session_id
    return await LmsLiveClassesService.record_attendance(session_id, payload)


@lxp_router.get("/live-classes/sessions/{session_id}/attendance", response_model=List[LmsLiveClassAttendanceResponse])
async def get_live_class_attendance_roster(session_id: str):
    """Retrieves student attendance and participation logs for a live session."""
    return await LmsLiveClassesService.get_class_attendance(session_id)


@lxp_router.post("/live-classes/sessions/{session_id}/recording", response_model=LmsLiveClassSessionResponse)
async def attach_concluded_class_recording(
    session_id: str,
    recording_url: str = Query(...),
    duration_seconds: int = Query(5400),
):
    """Links archived cloud recording video to concluded live session."""
    res = await LmsLiveClassesService.attach_recording(session_id, recording_url, duration_seconds)
    if not res:
        raise HTTPException(status_code=404, detail="Live class session not found")
    return res


# ============================================================================
# PHASE 5 MODULE 6: LMS ASSIGNMENT MANAGEMENT ENDPOINTS
# ============================================================================

@lxp_router.get("/assignments", response_model=List[LmsAssignmentResponse])
async def list_lms_assignments(course_id: Optional[str] = Query(None)):
    """Lists published assignments with rubric criteria, deadlines, and group settings."""
    return await LmsAssignmentManagementService.list_assignments(course_id=course_id)


@lxp_router.post("/assignments", response_model=LmsAssignmentResponse, status_code=status.HTTP_201_CREATED)
async def create_lms_assignment(payload: LmsAssignmentCreate):
    """Authors and releases a new assignment with rubrics and late penalty rules."""
    return await LmsAssignmentManagementService.create_assignment(payload)


@lxp_router.get("/assignments/{assignment_id}", response_model=LmsAssignmentResponse)
async def get_lms_assignment_details(assignment_id: str):
    """Retrieves single assignment specifications and rubric schemas."""
    asg = await LmsAssignmentManagementService.get_assignment(assignment_id)
    if not asg:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return asg


@lxp_router.get("/assignments/{assignment_id}/submissions", response_model=List[LmsAssignmentSubmissionResponse])
async def list_assignment_submissions(assignment_id: str):
    """Faculty endpoint retrieving all student submissions, files, and plagiarism scores."""
    return await LmsAssignmentManagementService.list_submissions(assignment_id)


@lxp_router.post("/assignments/{assignment_id}/submissions", response_model=LmsAssignmentSubmissionResponse, status_code=status.HTTP_201_CREATED)
async def submit_student_assignment(assignment_id: str, payload: LmsAssignmentSubmissionCreate):
    """Student endpoint for submitting online work or saving drafts with file attachments."""
    payload.assignment_id = assignment_id
    return await LmsAssignmentManagementService.submit_assignment(payload)


@lxp_router.post("/assignments/submissions/{submission_id}/grade", response_model=LmsAssignmentSubmissionResponse)
async def grade_student_assignment_submission(submission_id: str, payload: LmsAssignmentGradeRequest):
    """Faculty grading endpoint assessing rubrics, score, and constructive feedback."""
    res = await LmsAssignmentManagementService.grade_submission(submission_id, payload)
    if not res:
        raise HTTPException(status_code=404, detail="Submission not found")
    return res


@lxp_router.get("/assignments/student-submissions", response_model=List[LmsAssignmentSubmissionResponse])
async def list_student_personal_submissions(student_id: str = Query("std_01")):
    """Retrieves personal assignment submission track record for a student."""
    return await LmsAssignmentManagementService.list_student_submissions(student_id)


# ============================================================================
# PHASE 5 MODULE 7: LMS QUIZ & PRACTICE TESTS ENDPOINTS
# ============================================================================

@lxp_router.get("/quizzes", response_model=List[LmsQuizConfigResponse])
async def list_lms_quizzes(
    course_id: Optional[str] = Query(None),
    quiz_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    """Lists published practice tests, chapter quizzes, weekly assessments, and adaptive modules."""
    return await LmsQuizPracticeService.list_quizzes(course_id=course_id, quiz_type=quiz_type, status=status)


@lxp_router.post("/quizzes", response_model=LmsQuizConfigResponse, status_code=status.HTTP_201_CREATED)
async def create_lms_quiz(payload: LmsQuizConfigCreate):
    """Creates a new quiz or CBT practice module with questions and retry rules."""
    return await LmsQuizPracticeService.create_quiz(payload)


@lxp_router.get("/quizzes/{quiz_id}", response_model=LmsQuizConfigResponse)
async def get_lms_quiz_details(quiz_id: str):
    """Retrieves single quiz configuration and questions."""
    quiz = await LmsQuizPracticeService.get_quiz(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


@lxp_router.post("/quizzes/{quiz_id}/start")
async def start_lms_quiz_attempt(
    quiz_id: str,
    student_id: str = Query("std_01"),
    roll_number: str = Query("2024-MEI-CS-042"),
    candidate_name: str = Query("Aditya Verma")
):
    """Initiates a timed quiz attempt, checking retry limits and returning question prompts."""
    return await LmsQuizPracticeService.start_quiz(
        quiz_id=quiz_id,
        student_id=student_id,
        roll_number=roll_number,
        candidate_name=candidate_name
    )


@lxp_router.post("/quizzes/{quiz_id}/submit", response_model=LmsQuizAttemptResponse)
async def submit_lms_quiz_attempt(quiz_id: str, payload: LmsQuizSubmitAttemptRequest):
    """Submits answers, scores against CBT answer key, calculates XP, and provides instant feedback."""
    return await LmsQuizPracticeService.submit_attempt(quiz_id, payload)


@lxp_router.get("/quizzes/{quiz_id}/attempts", response_model=List[LmsQuizAttemptResponse])
async def list_lms_quiz_attempts(quiz_id: str, student_id: Optional[str] = Query(None)):
    """Retrieves attempt records for a specific quiz."""
    return await LmsQuizPracticeService.list_attempts(quiz_id=quiz_id, student_id=student_id)


@lxp_router.get("/quizzes/student-summary")
async def get_lms_student_quiz_summary(student_id: str = Query("std_01")):
    """Provides comprehensive quiz performance analytics, pass rates, XP tally, and weak topics."""
    return await LmsQuizPracticeService.get_student_performance_summary(student_id=student_id)


# ============================================================================
# PHASE 5 MODULE 8: LMS DISCUSSION & COLLABORATION ENDPOINTS
# ============================================================================

@lxp_router.get("/forums", response_model=List[LmsDiscussionForumResponse])
async def list_discussion_forums(
    course_id: Optional[str] = Query(None),
    category: Optional[str] = Query(None)
):
    """Lists forums filtered by course and category (ANNOUNCEMENT, FACULTY_QA, PEER_LEARNING, etc.)."""
    return await LmsDiscussionCollaborationService.list_forums(course_id=course_id, category=category)


@lxp_router.post("/forums", response_model=LmsDiscussionForumResponse, status_code=status.HTTP_201_CREATED)
async def create_discussion_forum(payload: LmsDiscussionForumCreate):
    """Creates a new discussion forum or announcement board for a course."""
    return await LmsDiscussionCollaborationService.create_forum(payload)


@lxp_router.get("/forums/{forum_id}", response_model=LmsDiscussionForumResponse)
async def get_discussion_forum(forum_id: str):
    """Retrieves forum metadata and configuration."""
    forum = await LmsDiscussionCollaborationService.get_forum(forum_id)
    if not forum:
        raise HTTPException(status_code=404, detail="Forum not found")
    return forum


@lxp_router.get("/forums/{forum_id}/threads", response_model=List[LmsDiscussionThreadResponse])
async def list_forum_threads(
    forum_id: str,
    is_announcement: Optional[bool] = Query(None),
    tag: Optional[str] = Query(None)
):
    """Lists topic threads within a forum ordered by pinned status and recency."""
    return await LmsDiscussionCollaborationService.list_threads(forum_id=forum_id, is_announcement=is_announcement, tag=tag)


@lxp_router.post("/forums/{forum_id}/threads", response_model=LmsDiscussionThreadResponse, status_code=status.HTTP_201_CREATED)
async def create_forum_thread(forum_id: str, payload: LmsDiscussionThreadCreate):
    """Posts a new topic thread or inquiry in a forum."""
    payload.forum_id = forum_id
    return await LmsDiscussionCollaborationService.create_thread(payload)


@lxp_router.get("/threads/{thread_id}", response_model=LmsDiscussionThreadResponse)
async def get_discussion_thread(thread_id: str):
    """Retrieves single thread details."""
    thread = await LmsDiscussionCollaborationService.get_thread(thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread


@lxp_router.post("/threads/{thread_id}/upvote")
async def upvote_discussion_thread(thread_id: str):
    """Increments thread upvote counter."""
    return await LmsDiscussionCollaborationService.upvote_thread(thread_id)


@lxp_router.get("/threads/{thread_id}/replies", response_model=List[LmsDiscussionReplyResponse])
async def list_thread_replies(thread_id: str):
    """Lists answers and discussion replies for a thread."""
    return await LmsDiscussionCollaborationService.list_replies(thread_id)


@lxp_router.post("/threads/{thread_id}/replies", response_model=LmsDiscussionReplyResponse, status_code=status.HTTP_201_CREATED)
async def create_thread_reply(thread_id: str, payload: LmsDiscussionReplyCreate):
    """Posts a response or faculty answer to a discussion thread."""
    payload.thread_id = thread_id
    return await LmsDiscussionCollaborationService.create_reply(payload)


@lxp_router.post("/threads/{thread_id}/replies/{reply_id}/accept", response_model=LmsDiscussionReplyResponse)
async def accept_thread_answer(thread_id: str, reply_id: str):
    """Marks a reply as the accepted/official answer, resolving the thread."""
    return await LmsDiscussionCollaborationService.mark_accepted_answer(reply_id, thread_id)


@lxp_router.get("/courses/{course_id}/chat", response_model=List[LmsCourseChatMessageResponse])
async def list_course_chat_messages(course_id: str, limit: int = Query(50, ge=1, le=100)):
    """Retrieves real-time course chat messages."""
    return await LmsDiscussionCollaborationService.list_chat_messages(course_id=course_id, limit=limit)


@lxp_router.post("/courses/{course_id}/chat", response_model=LmsCourseChatMessageResponse, status_code=status.HTTP_201_CREATED)
async def send_course_chat_message(course_id: str, payload: LmsCourseChatMessageCreate):
    """Broadcasts a chat message in the course chat channel."""
    payload.course_id = course_id
    return await LmsDiscussionCollaborationService.send_chat_message(payload)


# ============================================================================
# PHASE 5 MODULE 9: LMS ATTENDANCE & ENGAGEMENT TRACKING ENDPOINTS
# ============================================================================

@lxp_router.get("/attendance/student", response_model=LmsStudentEngagementResponse)
async def get_student_engagement_metrics(
    student_id: str = Query("std_01"),
    course_id: Optional[str] = Query(None)
):
    """Retrieves real-time student engagement metrics, streak, study hours, and composite score."""
    return await LmsAttendanceEngagementService.get_student_engagement(student_id=student_id, course_id=course_id)


@lxp_router.get("/attendance/cohort", response_model=List[LmsStudentEngagementResponse])
async def get_course_cohort_engagement_list(course_id: str = Query("crs_cs301")):
    """Faculty/HOD endpoint listing all student engagement records and risk levels for a course."""
    return await LmsAttendanceEngagementService.list_cohort_engagements(course_id)


@lxp_router.get("/attendance/cohort/summary", response_model=LmsCourseCohortEngagementSummary)
async def get_course_cohort_summary(course_id: str = Query("crs_cs301")):
    """Aggregated engagement analytics: average study hours, completion %, and at-risk student count."""
    return await LmsAttendanceEngagementService.get_cohort_summary(course_id)


@lxp_router.post("/attendance/activity", response_model=LmsActivityLogResponse, status_code=status.HTTP_201_CREATED)
async def record_student_activity(payload: LmsActivityLogCreate):
    """Logs learning events (lesson view, video watch, quiz attempt, login) and updates metrics."""
    return await LmsAttendanceEngagementService.record_activity(payload)


@lxp_router.get("/attendance/timeline", response_model=List[LmsActivityLogResponse])
async def get_student_activity_timeline(
    student_id: str = Query("std_01"),
    course_id: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100)
):
    """Chronological audit timeline of all learning activities performed by a student."""
    return await LmsAttendanceEngagementService.list_activity_timeline(
        student_id=student_id, course_id=course_id, limit=limit
    )


# ============================================================================
# PHASE 5 MODULE 10: LMS PROGRESS ANALYTICS & GAMIFICATION ENDPOINTS
# ============================================================================

@lxp_router.get("/gamification/profile", response_model=LmsGamificationProfileResponse)
async def get_student_gamification_profile(student_id: str = Query("std_01")):
    """Returns comprehensive learner profile: XP points, tier (Bronze-Scholar), streaks, badges, skills, and weak topics."""
    return await LmsProgressAnalyticsService.get_gamification_profile(student_id=student_id)


@lxp_router.get("/gamification/badges", response_model=List[LmsBadgeDefinitionResponse])
async def list_gamification_badges(category: Optional[str] = Query(None)):
    """Lists all defined badges across course completion, skill mastery, streak, and community."""
    return await LmsProgressAnalyticsService.list_badges(category=category)


@lxp_router.post("/gamification/badges", response_model=LmsBadgeDefinitionResponse, status_code=status.HTTP_201_CREATED)
async def create_gamification_badge(payload: LmsBadgeDefinitionCreate):
    """Authors a new achievement badge with criteria and XP reward value."""
    return await LmsProgressAnalyticsService.create_badge(payload)


@lxp_router.get("/gamification/badges/student", response_model=List[LmsStudentBadgeAwardResponse])
async def get_student_earned_badges(student_id: str = Query("std_01")):
    """Retrieves badges awarded to a student along with SHA-256 verification hashes."""
    return await LmsProgressAnalyticsService.get_student_badges(student_id=student_id)


@lxp_router.get("/gamification/skills", response_model=List[LmsSkillMasteryResponse])
async def list_student_skill_masteries(student_id: str = Query("std_01")):
    """Returns multi-topic skill competency radar ratings (Novice to Master)."""
    return await LmsProgressAnalyticsService.list_skill_masteries(student_id=student_id)


@lxp_router.get("/analytics/faculty", response_model=LmsFacultyAnalyticsOverviewResponse)
async def get_faculty_analytics_overview(course_id: str = Query("crs_cs301")):
    """Faculty & HOD dashboard: course completion rates, XP distribution, competency spread, and struggling topics."""
    return await LmsProgressAnalyticsService.get_faculty_analytics_overview(course_id=course_id)


# ============================================================================
# PHASE 5 MODULE 11: LMS DIGITAL LIBRARY ENDPOINTS
# ============================================================================

@lxp_router.get("/library/resources", response_model=List[LmsDigitalResourceResponse])
async def list_digital_library_resources(
    course_id: Optional[str] = Query(None),
    resource_type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    """Lists digital library items across eBooks, lecture PDFs, notes, previous exam papers, journals, and videos."""
    return await LmsDigitalLibraryService.list_resources(
        course_id=course_id, resource_type=resource_type, category=category, search=search
    )


@lxp_router.post("/library/resources", response_model=LmsDigitalResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_digital_library_resource(payload: LmsDigitalResourceCreate):
    """Uploads and indexes a new learning resource in the Digital Library with ERP linkage."""
    return await LmsDigitalLibraryService.create_resource(payload)


@lxp_router.get("/library/resources/{resource_id}", response_model=LmsDigitalResourceResponse)
async def get_digital_library_resource(resource_id: str):
    """Retrieves single digital resource details, metadata, and download permission status."""
    res = await LmsDigitalLibraryService.get_resource(resource_id)
    if not res:
        raise HTTPException(status_code=404, detail="Digital resource not found")
    return res


@lxp_router.post("/library/resources/{resource_id}/access", response_model=LmsDigitalResourceAccessLogResponse)
async def log_digital_resource_access(
    resource_id: str,
    student_id: str = Query("std_01"),
    roll_number: str = Query("2024-MEI-CS-042"),
    action_type: str = Query("VIEW")
):
    """Audits resource consumption (VIEW / DOWNLOAD), enforces download controls, and increments telemetry."""
    return await LmsDigitalLibraryService.log_access(
        resource_id=resource_id, student_id=student_id, roll_number=roll_number, action_type=action_type
    )


@lxp_router.get("/library/categories", response_model=List[LmsDigitalLibraryCategorySummary])
async def list_digital_library_categories():
    """Returns aggregated counts of available digital assets segmented by content format."""
    return await LmsDigitalLibraryService.list_category_summaries()


# ============================================================================
# PHASE 5 MODULE 12: LMS CERTIFICATES & DIGITAL CREDENTIALS ENDPOINTS
# ============================================================================

@lxp_router.get("/certificates", response_model=List[LmsCertificateResponse])
async def list_lms_certificates(
    student_id: Optional[str] = Query(None),
    course_id: Optional[str] = Query(None)
):
    """Lists issued course completion and honors certificates."""
    return await LmsCertificatesBadgesService.list_certificates(student_id=student_id, course_id=course_id)


@lxp_router.post("/certificates/issue", response_model=LmsCertificateResponse, status_code=status.HTTP_201_CREATED)
async def issue_lms_certificate(payload: LmsCertificateIssueRequest):
    """Issues a verified certificate with sequential number, SHA-256 hash, and QR code payload."""
    return await LmsCertificatesBadgesService.issue_certificate(payload)


@lxp_router.get("/certificates/{certificate_id_or_number}", response_model=LmsCertificateResponse)
async def get_lms_certificate(certificate_id_or_number: str):
    """Retrieves certificate record by ID or formal certificate number."""
    cert = await LmsCertificatesBadgesService.get_certificate(certificate_id_or_number)
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return cert


@lxp_router.get("/certificates/verify/{verification_code}", response_model=LmsCertificateVerifyResponse)
async def verify_lms_certificate(verification_code: str):
    """Public verification gateway: validates certificate authenticity via code or SHA-256 hash."""
    return await LmsCertificatesBadgesService.verify_certificate(verification_code)


@lxp_router.get("/credentials/student", response_model=List[LmsDigitalCredentialResponse])
async def list_student_digital_credentials(student_id: str = Query("std_01")):
    """Lists micro-credentials, verified skill badges, and digital credentials for a student."""
    return await LmsCertificatesBadgesService.list_digital_credentials(student_id=student_id)


# ============================================================================
# PHASE 5 MODULE 13: LMS PARENT PORTAL ENDPOINTS
# ============================================================================

@lxp_router.get("/parents/wards", response_model=List[LmsParentWardResponse])
async def list_parent_wards(parent_user_id: str = Query("par_suresh_042")):
    """Returns student wards associated with the authenticated parent account."""
    return await LmsParentPortalService.get_parent_wards(parent_user_id=parent_user_id)


@lxp_router.get("/parents/wards/{student_id}/overview", response_model=LmsParentOverviewResponse)
async def get_parent_ward_overview(
    student_id: str,
    parent_user_id: str = Query("par_suresh_042")
):
    """Parent dashboard: comprehensive monitoring of attendance, live classes, assignments, results, and faculty notes."""
    return await LmsParentPortalService.get_ward_comprehensive_overview(
        parent_user_id=parent_user_id, student_id=student_id
    )


@lxp_router.post("/parents/feedback", response_model=LmsFacultyStudentFeedbackResponse, status_code=status.HTTP_201_CREATED)
async def submit_faculty_feedback_for_parent(payload: LmsFacultyStudentFeedbackCreate):
    """Faculty endpoint to submit personalized academic and behavioral feedback visible to parents."""
    return await LmsParentPortalService.submit_faculty_feedback(payload)


@lxp_router.get("/parents/notifications", response_model=List[LmsParentNotificationResponse])
async def list_parent_notifications(parent_user_id: str = Query("par_suresh_042")):
    """Retrieves real-time alerts for parents regarding assignment marks, attendance, and exam dates."""
    return await LmsParentPortalService.list_parent_notifications(parent_user_id=parent_user_id)


# ============================================================================
# PHASE 5 MODULE 14: LMS FACULTY PORTAL ENDPOINTS
# ============================================================================

@lxp_router.get("/faculty/profile", response_model=LmsFacultyProfileResponse)
async def get_faculty_profile_data(faculty_id: str = Query("fac_01")):
    """Returns instructor profile credentials, research bio, office hours, and ratings."""
    return await LmsFacultyPortalService.get_faculty_profile(faculty_id=faculty_id)


@lxp_router.get("/faculty/workspace", response_model=LmsFacultyWorkspaceOverviewResponse)
async def get_faculty_workspace_overview(faculty_id: str = Query("fac_01")):
    """Faculty cockpit: active courses, pending grading queue items, student inquiries, and cohort telemetry."""
    return await LmsFacultyPortalService.get_faculty_workspace(faculty_id=faculty_id)


@lxp_router.get("/faculty/grading-queue", response_model=List[LmsFacultyGradingQueueItemResponse])
async def list_faculty_grading_queue(
    faculty_id: str = Query("fac_01"),
    status: Optional[str] = Query(None)
):
    """Retrieves pending student assignment submissions awaiting evaluation with similarity scores."""
    return await LmsFacultyPortalService.list_grading_queue(faculty_id=faculty_id, status=status)


@lxp_router.post("/faculty/grading-queue/{queue_item_id}/grade", response_model=LmsFacultyGradingQueueItemResponse)
async def submit_grading_evaluation(
    queue_item_id: str,
    score: float = Query(..., ge=0.0),
    feedback: str = Query(..., min_length=2)
):
    """Submits evaluation score and feedback directly from the faculty grading queue."""
    return await LmsFacultyPortalService.grade_queue_submission(
        queue_item_id=queue_item_id, score=score, feedback=feedback
    )


# ============================================================================
# PHASE 5 MODULE 15: LMS STUDENT PORTAL ENDPOINTS
# ============================================================================

@lxp_router.get("/student/cockpit", response_model=LmsStudentCockpitResponse)
async def get_student_cockpit_details(student_id: str = Query("std_01")):
    """Returns personalized learner profile: term, streak, study goals, XP points, and tier."""
    return await LmsStudentPortalService.get_student_cockpit(student_id=student_id)


@lxp_router.get("/student/dashboard", response_model=LmsStudentUnifiedDashboardResponse)
async def get_student_unified_dashboard(student_id: str = Query("std_01")):
    """Unified student cockpit: enrolled courses, continue-watching video state, pending submissions, and bookmarks."""
    return await LmsStudentPortalService.get_unified_dashboard(student_id=student_id)


@lxp_router.get("/student/bookmarks", response_model=List[LmsStudentBookmarkResponse])
async def list_student_bookmarks(student_id: str = Query("std_01")):
    """Lists saved lessons, videos, research papers, and notes bookmarked by the student."""
    return await LmsStudentPortalService.list_bookmarks(student_id=student_id)


@lxp_router.post("/student/bookmarks", response_model=LmsStudentBookmarkResponse, status_code=status.HTTP_201_CREATED)
async def add_student_bookmark(payload: LmsStudentBookmarkCreate):
    """Saves a curriculum resource or video timestamp to the student's personal bookmarks."""
    return await LmsStudentPortalService.add_bookmark(payload)


@lxp_router.post("/student/enroll")
async def enroll_student_in_course(student_id: str = Query("std_01"), course_id: str = Query(...)):
    """Self-enrolls student in elective or certification course."""
    return await LmsStudentPortalService.enroll_course(student_id=student_id, course_id=course_id)


# ============================================================================
# PHASE 5 MODULE 16: LMS AI LEARNING ASSISTANT ENDPOINTS
# ============================================================================

@lxp_router.post("/ai/tutor", response_model=LmsAiTutorQueryResponse)
async def ask_lms_ai_tutor(payload: LmsAiTutorQueryRequest):
    """Curriculum-grounded Socratic AI Tutor responding to conceptual inquiries with follow-ups and references."""
    return await LmsAiLearningAssistantService.ask_ai_tutor(payload)


@lxp_router.post("/ai/flashcards/generate", response_model=LmsAiFlashcardDeckResponse, status_code=status.HTTP_201_CREATED)
async def generate_lms_ai_flashcards(payload: LmsAiFlashcardGenerateRequest):
    """Generates conceptual flashcard decks tailored to curriculum topics and weak areas."""
    return await LmsAiLearningAssistantService.generate_flashcards(payload)


@lxp_router.post("/ai/notes/summarize", response_model=LmsAiSummarizeNotesResponse)
async def summarize_lms_notes(payload: LmsAiSummarizeNotesRequest):
    """Extracts executive key bullet takeaways from lecture notes with spaced repetition recommendations."""
    return await LmsAiLearningAssistantService.summarize_notes(payload)


@lxp_router.get("/ai/study-plan", response_model=LmsAiStudyPlanResponse)
async def get_lms_ai_study_plan(student_id: str = Query("std_01")):
    """Generates and retrieves personalized exam-targeted study milestone roadmap."""
    return await LmsAiLearningAssistantService.get_study_plan(student_id=student_id)


@lxp_router.get("/ai/recommendations")
async def get_lms_ai_recommendations(student_id: str = Query("std_01")):
    """Provides automated course recommendations, learning path suggestions, and targeted weak topic drills."""
    return await LmsAiLearningAssistantService.get_recommendations(student_id=student_id)


# ============================================================================
# PHASE 5 MODULE 17: LMS MOBILE LEARNING & OFFLINE SYNC ENDPOINTS
# ============================================================================

@lxp_router.post("/mobile/devices/register", response_model=LmsMobileDeviceRegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register_mobile_device(payload: LmsMobileDeviceRegisterRequest):
    """Registers or updates student mobile device (Android/iOS, FCM/APNs token, app version)."""
    return await LmsMobileLearningService.register_device(payload)


@lxp_router.get("/mobile/devices", response_model=List[LmsMobileDeviceRegistrationResponse])
async def list_student_mobile_devices(student_id: str = Query("std_01")):
    """Lists active mobile devices registered for push alerts and offline DRM licensing."""
    return await LmsMobileLearningService.list_student_devices(student_id=student_id)


@lxp_router.post("/mobile/offline/download", response_model=LmsOfflineDownloadedAssetResponse, status_code=status.HTTP_201_CREATED)
async def download_offline_resource(payload: LmsMobileDownloadAssetRequest):
    """Issues encrypted offline download license with 30-day expiration window."""
    return await LmsMobileLearningService.download_offline_asset(payload)


@lxp_router.get("/mobile/offline/downloads", response_model=List[LmsOfflineDownloadedAssetResponse])
async def list_offline_downloaded_assets(
    student_id: str = Query("std_01"),
    device_token: Optional[str] = Query(None)
):
    """Lists offline downloaded lessons, videos, and eBooks stored locally on the device."""
    return await LmsMobileLearningService.list_offline_downloads(
        student_id=student_id, device_token=device_token
    )


@lxp_router.post("/mobile/sync", response_model=LmsMobileSyncSessionResponse)
async def execute_mobile_background_sync(payload: LmsMobileSyncRequest):
    """Processes background delta sync: offline playback seconds, quiz answers, and streak updates."""
    return await LmsMobileLearningService.execute_background_sync(payload)


# ============================================================================
# PHASE 5 MODULE 18: LMS ANALYTICS & REPORTS ENDPOINTS
# ============================================================================

@lxp_router.get("/reports/dashboard", response_model=LmsGlobalReportingDashboardResponse)
async def get_lms_reports_dashboard(academic_year: str = Query("2026-27")):
    """Aggregated institution-level reporting dashboard: completion rates, department metrics, study hours."""
    return await LmsAnalyticsReportsService.get_global_reporting_dashboard(academic_year=academic_year)


@lxp_router.get("/reports/archives", response_model=List[LmsAnalyticsReportArchiveResponse])
async def list_lms_report_archives(
    report_type: Optional[str] = Query(None),
    department: Optional[str] = Query(None)
):
    """Lists generated analytical reports across Student Progress, Faculty, Course Completion, Assignments, Quizzes."""
    return await LmsAnalyticsReportsService.list_report_archives(report_type=report_type, department=department)


@lxp_router.post("/reports/generate", response_model=LmsAnalyticsReportArchiveResponse, status_code=status.HTTP_201_CREATED)
async def generate_lms_analytics_report(payload: LmsAnalyticsReportGenerateRequest):
    """Compiles and exports customized analytics reports in PDF, XLSX, or CSV formats."""
    return await LmsAnalyticsReportsService.generate_report(payload)


@lxp_router.get("/reports/archives/{report_id}", response_model=LmsAnalyticsReportArchiveResponse)
async def get_lms_report_archive_details(report_id: str):
    """Retrieves single archived report metrics and download URL."""
    rep = await LmsAnalyticsReportsService.get_report_archive(report_id)
    if not rep:
        raise HTTPException(status_code=404, detail="Report archive not found")
    return rep


# ============================================================================
# PHASE 5 MODULE 19: LMS ENTERPRISE INTEGRATIONS ENDPOINTS
# ============================================================================

@lxp_router.get("/integrations/connectors", response_model=List[LmsSystemIntegrationConnectorResponse])
async def list_lms_connectors():
    """Returns health, latency, and status of all 9 integrated enterprise pillars."""
    return await LmsEnterpriseIntegrationsService.list_connectors()


@lxp_router.get("/integrations/connectors/{system_name}/health", response_model=LmsConnectorHealthCheckResponse)
async def check_lms_connector_health(system_name: str):
    """Pings specific connector (ERP, CBT, EXAMS, PAYMENT, S3, etc.) and returns real-time latency."""
    return await LmsEnterpriseIntegrationsService.check_health(system_name)


@lxp_router.get("/integrations/search", response_model=List[LmsGlobalSearchItemResponse])
async def global_lms_search(
    q: str = Query(..., min_length=2),
    entity_type: Optional[str] = Query(None)
):
    """Unified cross-system global search index across courses, lessons, notes, quizzes, and library."""
    return await LmsEnterpriseIntegrationsService.global_search(query=q, entity_type=entity_type)


@lxp_router.post("/integrations/payments/initiate", response_model=LmsPaymentTransactionResponse, status_code=status.HTTP_201_CREATED)
async def initiate_lms_course_payment(payload: LmsPaymentInitiateRequest):
    """Processes elective courseware payment via Razorpay / UPI gateway integration."""
    return await LmsEnterpriseIntegrationsService.initiate_payment(payload)


# ============================================================================
# PHASE 5 MODULE 20: LMS PRODUCTION READINESS & ENTERPRISE VALIDATION
# ============================================================================

@lxp_router.get("/readiness/audit", response_model=LmsProductionReadinessAuditResponse)
async def get_lms_production_readiness_audit():
    """Comprehensive production readiness audit: functional, performance, security, and quality benchmarks."""
    return await LmsProductionReadinessService.run_comprehensive_audit()


@lxp_router.post("/readiness/run-e2e", response_model=LmsE2ETestResultResponse)
async def run_lms_e2e_tests():
    """Executes automated end-to-end test suite covering all 20 Phase 5 LMS modules with zero failures."""
    return await LmsProductionReadinessService.run_e2e_tests()


@lxp_router.get("/readiness/system-health", response_model=LmsSystemHealthScorecardResponse)
async def get_lms_system_health_scorecard():
    """System health scorecard: mesh status, DB pool, cache hit ratio, and zero client storage compliance."""
    return await LmsProductionReadinessService.get_system_health_scorecard()
