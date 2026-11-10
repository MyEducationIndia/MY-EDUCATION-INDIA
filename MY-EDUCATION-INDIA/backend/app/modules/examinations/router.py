from app.modules.examinations.system_service import ExamSystemService
from app.modules.examinations.schemas import (
    EmsSystemHealthResponse,
    EmsFullIntegrationMatrixResponse,
)

from app.modules.examinations.coe_portal_service import ExamCoePortalService
from app.modules.examinations.schemas import (
    CoeGovernanceCockpitResponse,
    CoeStageTransitionRequest,
    CoeLockToggleRequest,
    CoeQpVaultUnlockRequest,
    CoeEmergencyOverrideRequest,
    EmergencyOverrideLogResponse,
)

from app.modules.examinations.faculty_portal_service import ExamFacultyPortalService
from app.modules.examinations.schemas import (
    FacultyDutyItem,
    FacultyDutySwapRequestCreate,
    FacultyDutySwapResponse,
    FacultyDutySwapRespondRequest,
    FacultyPortalDashboardResponse,
)

from app.modules.examinations.student_portal_service import ExamStudentPortalService
from app.modules.examinations.schemas import (
    StudentPortalDashboardResponse,
    StudentExamRegisterRequest,
    StudentSeatingLookupResponse,
)

from app.modules.examinations.analytics_service import ExamAnalyticsService
from app.modules.examinations.schemas import (
    CourseAnalyticsMetricResponse,
    CourseAnalyticsCalculateRequest,
    StudentRiskPredictionResponse,
    ExaminerBiasReportItem,
    AnalyticsSummaryKPIsResponse,
)

from app.modules.examinations.compliance_service import ExamComplianceService
from app.modules.examinations.schemas import (
    ComplianceReportCreateRequest,
    ComplianceReportResponse,
    ComplianceReportSubmitRequest,
    MalpracticeReportCreateRequest,
    MalpracticeDisciplinaryResponse,
    MalpracticeResolveRequest,
)

from app.modules.examinations.certificate_service import ExamCertificateService
from app.modules.examinations.schemas import (
    CertificateIssueRequest,
    CertificateRegistryResponse,
    CertificateVerificationResponse,
    CertificateRevokeRequest,
    TranscriptRequestCreate,
    TranscriptRequestResponse,
    TranscriptRequestStatusUpdateRequest,
)

from app.modules.examinations.revaluation_service import ExamRevaluationService
from app.modules.examinations.schemas import (
    RevaluationApplicationCreate,
    RevaluationApplicationResponse,
    RevaluationAssignEvaluatorRequest,
    RevaluationScoreSubmitRequest,
    RevaluationFinalizeRequest,
    SupplementaryRegistrationCreate,
    SupplementaryRegistrationResponse,
    SupplementaryRecordMarksRequest,
)

from app.modules.examinations.result_processing_service import ExamResultProcessingService
from app.modules.examinations.schemas import (
    StudentSemesterResultResponse,
    ResultProcessingCalculateRequest,
    ResultProcessingCalculateResponse,
    MeritListGenerateRequest,
    MeritListResponse,
)

from datetime import date
from typing import Any, Dict, List, Optional
import uuid
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db_session
from app.modules.auth.dependencies import get_current_user, require_permissions
from app.modules.examinations.analytics import ExamAnalyticsEngine
from app.modules.examinations.reports import ExamReportEngine
from app.modules.examinations.schemas import (
    AcademicSessionCreate,
    AcademicSessionResponse,
    AcademicSemesterCreate,
    AcademicSemesterResponse,
    AssessmentComponentTypeCreate,
    AssessmentComponentTypeResponse,
    CourseWeightageSchemeCreate,
    CourseWeightageSchemeResponse,
    EMSDashboardResponse,
    EMSRoleDashboardSummary,
    ExamDashboardSummary,
    ExamScheduleCreate,
    ExamScheduleResponse,
    ExamSessionCreate,
    ExamSessionResponse,
    ExamTypeCreate,
    ExamTypeResponse,
    MarkBatchEntryRequest,
    MarkEntryResponse,
    StudentResultResponse,
    TranscriptResponse,
    # Module 3 Planning schemas
    ExamDepartmentPlanCreate,
    ExamDepartmentPlanResponse,
    ExamTimeSlotCreate,
    ExamTimeSlotResponse,
    ExamCourseMappingCreate,
    ExamCourseMappingResponse,
    ExamRoomPlanningCreate,
    ExamRoomPlanningResponse,
    ExamFacultyDutyPlanningCreate,
    ExamFacultyDutyPlanningResponse,
    ExamPlanningCalendarResponse,
    # Module 4 Timetable Generator schemas
    TimetableScheduleCreate,
    TimetableScheduleUpdate,
    TimetableScheduleResponse,
    TimetableAutoGenerateRequest,
    TimetableAutoGenerateResponse,
    TimetableConflictResponse,
    TimetableConflictResolveRequest,
    # Module 5 Hall Ticket schemas
    HallTicketCreate,
    HallTicketResponse,
    HallTicketBulkGenerateRequest,
    HallTicketBulkGenerateResponse,
    HallTicketVerificationResponse,
    HallTicketStatusUpdateRequest,
    # Module 6 Seating & Room Management schemas
    ExamBuildingCreate,
    ExamBuildingResponse,
    ExamRoomLayoutCreate,
    ExamRoomLayoutResponse,
    SeatingPlanGenerateRequest,
    SeatingPlanResponse,
    SeatingPlanDoorNoticeResponse,
    # Module 7 Invigilator Management schemas
    InvigilatorProfileCreate,
    InvigilatorProfileResponse,
    InvigilatorRosterCreate,
    InvigilatorRosterResponse,
    InvigilatorAttendanceRequest,
    InvigilatorReplacementRequest,
    InvigilatorDutyReportSubmitRequest,
    InvigilatorAutoRosterRequest,
    InvigilatorAutoRosterResponse,
    # Module 8 Practical & Viva schemas
    RubricCriterionItem,
    PracticalAssessmentCreate,
    PracticalAssessmentResponse,
    PracticalScoreRecordCreate,
    PracticalScoreRecordResponse,
    PracticalBatchMarksEntryRequest,
    PracticalBatchMarksEntryResponse,
    PracticalLockApprovalRequest,
    # Module 9 Attendance During Exams schemas
    CandidateAttendanceCreate,
    CandidateAttendanceResponse,
    AttendanceBatchUpdateRequest,
    AttendanceBatchUpdateResponse,
    AttendanceQrScanRequest,
    AttendanceQrScanResponse,
    MalpracticeReportRequest,
    MedicalCaseReportRequest,
    HallAttendanceSummaryResponse,
    # Module 10 Evaluation Management schemas
    EvaluationBatchCreate,
    EvaluationBatchResponse,
    ScriptScoreSubmitRequest,
    ScriptEvaluationResponse,
    ModerationApplyRequest,
    GraceMarksApplyRequest,
    RecheckingProcessRequest,
    # Module 11 Marks Entry schemas
    StudentMarkItemCreate,
    StudentMarkItemResponse,
    MarksSubmissionCreate,
    MarksSubmissionResponse,
    MarksBatchSaveRequest,
    MarksBatchSaveResponse,
    MarksExcelImportRequest,
    MarksExcelImportResponse,
    MarksWorkflowApprovalRequest,
)
from app.modules.examinations.service import ExaminationService
from app.modules.examinations.dashboard_service import EMSDashboardService
from app.modules.examinations.structure_service import AcademicStructureService
from app.modules.examinations.planning_service import ExamPlanningService
from app.modules.examinations.timetable_service import ExamTimetableService
from app.modules.examinations.hall_ticket_service import ExamHallTicketService
from app.modules.examinations.seating_service import ExamSeatingService
from app.modules.examinations.invigilator_service import ExamInvigilatorService
from app.modules.examinations.practical_service import ExamPracticalService
from app.modules.examinations.attendance_service import ExamAttendanceService
from app.modules.examinations.evaluation_service import ExamEvaluationService
from app.modules.examinations.marks_entry_service import ExamMarksEntryService

exam_router = APIRouter(prefix="/exams", tags=["Enterprise Examination & Result Management"])


# 1. Exam Types
@exam_router.get("/types", response_model=List[ExamTypeResponse])
async def list_exam_types(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[ExamTypeResponse]:
    service = ExaminationService(db)
    items = await service.repo.get_exam_types(institute_id)
    return [ExamTypeResponse.model_validate(it) for it in items]


@exam_router.post("/types", response_model=ExamTypeResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_type(
    payload: ExamTypeCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> ExamTypeResponse:
    service = ExaminationService(db)
    item = await service.create_exam_type(payload)
    return ExamTypeResponse.model_validate(item)


# 2. Exam Sessions
@exam_router.get("/sessions", response_model=List[ExamSessionResponse])
async def list_exam_sessions(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[ExamSessionResponse]:
    service = ExaminationService(db)
    items = await service.repo.get_exam_sessions(institute_id)
    return [ExamSessionResponse.model_validate(it) for it in items]


@exam_router.post("/sessions", response_model=ExamSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_session(
    payload: ExamSessionCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> ExamSessionResponse:
    service = ExaminationService(db)
    sess = await service.create_exam_session(payload)
    return ExamSessionResponse.model_validate(sess)


# 3. Exam Schedules
@exam_router.post("/schedules", response_model=ExamScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_schedule(
    payload: ExamScheduleCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> ExamScheduleResponse:
    service = ExaminationService(db)
    sched = await service.create_exam_schedule(payload)
    return ExamScheduleResponse.model_validate(sched)


# 4. Mark Entry
@exam_router.post("/marks", response_model=List[MarkEntryResponse])
async def enter_subject_marks(
    payload: MarkBatchEntryRequest,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(require_permissions("exams.marks_entry")),
) -> List[MarkEntryResponse]:
    service = ExaminationService(db)
    user_id = getattr(user, "id", uuid.uuid4())
    saved = await service.enter_subject_marks(payload, entered_by_user_id=user_id)
    return [MarkEntryResponse.model_validate(s) for s in saved]


# 5. Result Publication
@exam_router.post("/results/publish", response_model=List[StudentResultResponse])
async def publish_results(
    session_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.publish")),
) -> List[StudentResultResponse]:
    service = ExaminationService(db)
    results = await service.compute_and_publish_results(session_id)
    return [StudentResultResponse.model_validate(r) for r in results]


# 6. Reports & Analytics
@exam_router.get("/reports/merit-list")
async def get_merit_list(
    exam_session_id: uuid.UUID = Query(...),
    top_n: int = Query(default=10),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> List[Dict[str, Any]]:
    return await ExamReportEngine.get_merit_list(db, exam_session_id, top_n)


@exam_router.get("/analytics", response_model=ExamDashboardSummary)
async def get_exam_analytics(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> ExamDashboardSummary:
    summary = await ExamAnalyticsEngine.get_dashboard_kpis(db, institute_id)
    return ExamDashboardSummary.model_validate(summary)


# ------------------- Phase 4 Module 1: EMS Dashboard Endpoints -------------------
@exam_router.get("/dashboard/role-view", response_model=EMSDashboardResponse)
async def get_ems_role_dashboard(
    role: str = Query("CONTROLLER_OF_EXAMINATION", description="ROOT_OWNER, SUPER_ADMIN, CONTROLLER_OF_EXAMINATION, PRINCIPAL, HOD, FACULTY, EVALUATOR, STUDENT"),
    institute_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> EMSDashboardResponse:
    """Generates role-tailored examination command telemetry and operational widgets."""
    inst_id = institute_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-institute-indore")
    service = EMSDashboardService(db)
    return await service.get_role_dashboard(role, inst_id)


@exam_router.get("/dashboard/kpis", response_model=EMSRoleDashboardSummary)
async def get_ems_role_kpis(
    role: str = Query("CONTROLLER_OF_EXAMINATION"),
    institute_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> EMSRoleDashboardSummary:
    """Returns high-level KPI card metrics for the specified institutional role."""
    inst_id = institute_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-institute-indore")
    service = EMSDashboardService(db)
    dash = await service.get_role_dashboard(role, inst_id)
    return dash.metrics


# ------------------- Phase 4 Module 2: Academic Examination Structure Endpoints -------------------
@exam_router.get("/structure/sessions", response_model=List[AcademicSessionResponse])
async def list_academic_sessions(
    institute_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[AcademicSessionResponse]:
    """Lists configured academic years/sessions for the institution."""
    inst_id = institute_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-institute-indore")
    service = AcademicStructureService(db)
    return await service.list_academic_sessions(inst_id)


@exam_router.post("/structure/sessions", response_model=AcademicSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_academic_session(
    payload: AcademicSessionCreate,
    institute_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> AcademicSessionResponse:
    """Configures a new academic session with start and end dates."""
    inst_id = institute_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-institute-indore")
    service = AcademicStructureService(db)
    return await service.create_academic_session(inst_id, payload)


@exam_router.get("/structure/sessions/{session_id}/semesters", response_model=List[AcademicSemesterResponse])
async def list_academic_semesters(
    session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[AcademicSemesterResponse]:
    """Lists semesters (Odd, Even, Trimesters) under an academic session."""
    service = AcademicStructureService(db)
    return await service.list_semesters(session_id)


@exam_router.post("/structure/semesters", response_model=AcademicSemesterResponse, status_code=status.HTTP_201_CREATED)
async def create_academic_semester(
    payload: AcademicSemesterCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> AcademicSemesterResponse:
    """Creates a semester term under an active academic session."""
    service = AcademicStructureService(db)
    return await service.create_semester(payload)


@exam_router.get("/structure/modalities", response_model=List[AssessmentComponentTypeResponse])
async def list_assessment_modalities(
    institute_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[AssessmentComponentTypeResponse]:
    """Lists all 10 assessment modalities (Annual, Semester, Mid, Unit, Practical, Viva, etc.)."""
    inst_id = institute_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-institute-indore")
    service = AcademicStructureService(db)
    return await service.list_assessment_modalities(inst_id)


@exam_router.post("/structure/modalities", response_model=AssessmentComponentTypeResponse, status_code=status.HTTP_201_CREATED)
async def create_assessment_modality(
    payload: AssessmentComponentTypeCreate,
    institute_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> AssessmentComponentTypeResponse:
    """Configures a customized assessment component type."""
    inst_id = institute_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-institute-indore")
    service = AcademicStructureService(db)
    return await service.create_assessment_modality(inst_id, payload)


@exam_router.get("/structure/semesters/{semester_id}/schemes", response_model=List[CourseWeightageSchemeResponse])
async def list_course_weightage_schemes(
    semester_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[CourseWeightageSchemeResponse]:
    """Lists course evaluation weightage schemes configured under a semester."""
    service = AcademicStructureService(db)
    return await service.list_weightage_schemes(semester_id)


@exam_router.post("/structure/schemes", response_model=CourseWeightageSchemeResponse, status_code=status.HTTP_201_CREATED)
async def create_course_weightage_scheme(
    payload: CourseWeightageSchemeCreate,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user),
) -> CourseWeightageSchemeResponse:
    """Creates a 100% normalized weightage scheme with passing floor thresholds."""
    approved_by = getattr(user, "id", uuid.uuid4())
    service = AcademicStructureService(db)
    return await service.create_weightage_scheme(payload, approved_by)


# ------------------- Phase 4 Module 3: Exam Planning Endpoints -------------------
@exam_router.get("/planning/calendar", response_model=ExamPlanningCalendarResponse)
async def get_exam_planning_calendar(
    session_id: Optional[uuid.UUID] = Query(None),
    institute_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> ExamPlanningCalendarResponse:
    """Retrieves unified master examination calendar with department plans, time slots, room halls, and faculty duty rosters."""
    sess_id = session_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-session-2026")
    inst_id = institute_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-institute-indore")
    service = ExamPlanningService(db)
    return await service.get_planning_calendar(sess_id, inst_id)


@exam_router.get("/planning/department-plans", response_model=List[ExamDepartmentPlanResponse])
async def list_exam_department_plans(
    session_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[ExamDepartmentPlanResponse]:
    """Lists all department examination plans submitted for an academic examination session."""
    sess_id = session_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-session-2026")
    service = ExamPlanningService(db)
    return await service.list_department_plans(sess_id)


@exam_router.post("/planning/department-plans", response_model=ExamDepartmentPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_department_plan(
    payload: ExamDepartmentPlanCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> ExamDepartmentPlanResponse:
    """Creates or submits a new department-wise examination logistics plan."""
    service = ExamPlanningService(db)
    return await service.create_department_plan(payload)


@exam_router.get("/planning/time-slots", response_model=List[ExamTimeSlotResponse])
async def list_exam_time_slots(
    institute_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[ExamTimeSlotResponse]:
    """Lists standardized campus exam time shifts and session reporting slots."""
    inst_id = institute_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-institute-indore")
    service = ExamPlanningService(db)
    return await service.list_time_slots(inst_id)


@exam_router.post("/planning/time-slots", response_model=ExamTimeSlotResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_time_slot(
    payload: ExamTimeSlotCreate,
    institute_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> ExamTimeSlotResponse:
    """Configures a standardized examination shift time slot."""
    inst_id = institute_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-institute-indore")
    service = ExamPlanningService(db)
    return await service.create_time_slot(inst_id, payload)


@exam_router.get("/planning/department-plans/{plan_id}/mappings", response_model=List[ExamCourseMappingResponse])
async def list_exam_course_mappings(
    plan_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[ExamCourseMappingResponse]:
    """Lists subject-to-examination components, question paper codes, and duration mappings under a plan."""
    service = ExamPlanningService(db)
    return await service.list_course_mappings(plan_id)


@exam_router.post("/planning/course-mappings", response_model=ExamCourseMappingResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_course_mapping(
    payload: ExamCourseMappingCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> ExamCourseMappingResponse:
    """Maps a course to an examination component with paper code, maximum marks, and duration."""
    service = ExamPlanningService(db)
    return await service.create_course_mapping(payload)


@exam_router.get("/planning/rooms", response_model=List[ExamRoomPlanningResponse])
async def list_exam_room_plannings(
    institute_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[ExamRoomPlanningResponse]:
    """Lists examination halls, classroom clusters, lab spaces, bench setups, and buffer capacities."""
    inst_id = institute_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-institute-indore")
    service = ExamPlanningService(db)
    return await service.list_room_plannings(inst_id)


@exam_router.post("/planning/rooms", response_model=ExamRoomPlanningResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_room_planning(
    payload: ExamRoomPlanningCreate,
    institute_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> ExamRoomPlanningResponse:
    """Configures a room or hall for examination seating allocation."""
    inst_id = institute_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-institute-indore")
    service = ExamPlanningService(db)
    return await service.create_room_planning(inst_id, payload)


@exam_router.get("/planning/faculty-allocations", response_model=List[ExamFacultyDutyPlanningResponse])
async def list_exam_faculty_allocations(
    assigned_date: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[ExamFacultyDutyPlanningResponse]:
    """Lists faculty allocations for examination duties (Superintendents, Invigilators, Squads)."""
    service = ExamPlanningService(db)
    return await service.list_faculty_allocations(assigned_date)


@exam_router.post("/planning/faculty-allocations", response_model=ExamFacultyDutyPlanningResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_faculty_allocation(
    payload: ExamFacultyDutyPlanningCreate,
    institute_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> ExamFacultyDutyPlanningResponse:
    """Allocates a faculty member to an examination duty roster."""
    inst_id = institute_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-institute-indore")
    service = ExamPlanningService(db)
    return await service.create_faculty_allocation(inst_id, payload)


# ------------------- Phase 4 Module 4: Timetable Generator Endpoints -------------------
@exam_router.post("/timetable/generate", response_model=TimetableAutoGenerateResponse, status_code=status.HTTP_201_CREATED)
async def auto_generate_exam_timetable(
    payload: TimetableAutoGenerateRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> TimetableAutoGenerateResponse:
    """Generates an automated, conflict-free examination timetable honoring study gaps, room availability, and lab batching."""
    service = ExamTimetableService(db)
    return await service.auto_generate_timetable(payload)


@exam_router.get("/timetable/schedules", response_model=List[TimetableScheduleResponse])
async def list_exam_timetable_schedules(
    session_id: Optional[uuid.UUID] = Query(None),
    department_id: Optional[uuid.UUID] = Query(None),
    semester_code: Optional[str] = Query(None),
    exam_date: Optional[date] = Query(None),
    room_number: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[TimetableScheduleResponse]:
    """Lists scheduled examination slots with multi-dimensional filtering."""
    sess_id = session_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-session-2026")
    service = ExamTimetableService(db)
    return await service.list_schedules(
        session_id=sess_id,
        department_id=department_id,
        semester_code=semester_code,
        exam_date=exam_date,
        room_number=room_number,
        status=status,
    )


@exam_router.post("/timetable/schedules", response_model=TimetableScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_timetable_schedule(
    payload: TimetableScheduleCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> TimetableScheduleResponse:
    """Creates a manual examination timetable schedule slot with conflict validation."""
    service = ExamTimetableService(db)
    return await service.create_schedule(payload)


@exam_router.put("/timetable/schedules/{schedule_id}", response_model=TimetableScheduleResponse)
async def update_exam_timetable_schedule(
    schedule_id: uuid.UUID,
    payload: TimetableScheduleUpdate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> TimetableScheduleResponse:
    """Updates an existing examination timetable schedule slot."""
    service = ExamTimetableService(db)
    return await service.update_schedule(schedule_id, payload)


@exam_router.delete("/timetable/schedules/{schedule_id}")
async def delete_exam_timetable_schedule(
    schedule_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> Dict[str, Any]:
    """Deletes an examination timetable schedule slot."""
    service = ExamTimetableService(db)
    return await service.delete_schedule(schedule_id)


@exam_router.get("/timetable/conflicts", response_model=List[TimetableConflictResponse])
async def list_exam_timetable_conflicts(
    session_id: Optional[uuid.UUID] = Query(None),
    is_resolved: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[TimetableConflictResponse]:
    """Lists detected timetable clashes (room, faculty, cohort, study gap)."""
    sess_id = session_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-session-2026")
    service = ExamTimetableService(db)
    return await service.list_conflicts(sess_id, is_resolved)


@exam_router.post("/timetable/conflicts/{conflict_id}/resolve", response_model=TimetableConflictResponse)
async def resolve_exam_timetable_conflict(
    conflict_id: uuid.UUID,
    payload: TimetableConflictResolveRequest,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user),
) -> TimetableConflictResponse:
    """Resolves an examination timetable conflict with an override or shift reschedule action."""
    user_id = getattr(user, "id", None)
    service = ExamTimetableService(db)
    return await service.resolve_conflict(conflict_id, payload, user_id)


@exam_router.post("/timetable/publish")
async def publish_exam_timetable(
    session_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.publish")),
) -> Dict[str, Any]:
    """Publishes finalized examination timetable, locking all schedules and notifying stakeholders."""
    sess_id = session_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-session-2026")
    service = ExamTimetableService(db)
    return await service.publish_timetable(sess_id)



# ------------------- Phase 4 Module 5: Hall Ticket System Endpoints -------------------
@exam_router.get("/hall-tickets", response_model=List[HallTicketResponse])
async def list_exam_hall_tickets(
    session_id: Optional[uuid.UUID] = Query(None),
    department_name: Optional[str] = Query(None),
    semester_code: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[HallTicketResponse]:
    """Lists generated examination admit cards / hall tickets with seat allocations and eligibility status."""
    sess_id = session_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-session-2026")
    service = ExamHallTicketService(db)
    return await service.list_hall_tickets(
        session_id=sess_id,
        department_name=department_name,
        semester_code=semester_code,
        status=status,
        search=search,
    )


@exam_router.get("/hall-tickets/{ticket_id}", response_model=HallTicketResponse)
async def get_exam_hall_ticket(
    ticket_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> HallTicketResponse:
    """Retrieves single hall ticket details including QR verification code and seating particulars."""
    service = ExamHallTicketService(db)
    return await service.get_hall_ticket(ticket_id)


@exam_router.post("/hall-tickets/bulk-generate", response_model=HallTicketBulkGenerateResponse, status_code=status.HTTP_201_CREATED)
async def bulk_generate_exam_hall_tickets(
    payload: HallTicketBulkGenerateRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> HallTicketBulkGenerateResponse:
    """Generates admit cards in bulk for eligible students, creating barcode, QR code, and CoE digital signature."""
    service = ExamHallTicketService(db)
    return await service.bulk_generate_hall_tickets(payload)


@exam_router.get("/hall-tickets/verify/{code_or_ticket}", response_model=HallTicketVerificationResponse)
async def verify_exam_hall_ticket(
    code_or_ticket: str,
    db: AsyncSession = Depends(get_db_session),
) -> HallTicketVerificationResponse:
    """Public digital verification endpoint for gate proctors scanning QR codes or entering ticket numbers."""
    service = ExamHallTicketService(db)
    return await service.verify_hall_ticket(code_or_ticket)


@exam_router.post("/hall-tickets/{ticket_id}/download", response_model=HallTicketResponse)
async def record_hall_ticket_download(
    ticket_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> HallTicketResponse:
    """Logs admit card download timestamp and increments download counter."""
    service = ExamHallTicketService(db)
    return await service.record_download(ticket_id)


@exam_router.put("/hall-tickets/{ticket_id}/status", response_model=HallTicketResponse)
async def update_hall_ticket_status(
    ticket_id: uuid.UUID,
    payload: HallTicketStatusUpdateRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> HallTicketResponse:
    """Updates admit card status (ISSUED, BLOCKED, CANCELLED)."""
    service = ExamHallTicketService(db)
    return await service.update_status(ticket_id, payload)


@exam_router.post("/hall-tickets/bulk-print")
async def bulk_print_hall_tickets(
    session_id: Optional[uuid.UUID] = Query(None),
    department_name: Optional[str] = Query(None),
    semester_code: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> Dict[str, Any]:
    """Generates bulk print payload formatted for institutional batch admit card printing."""
    sess_id = session_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-session-2026")
    service = ExamHallTicketService(db)
    tickets = await service.list_hall_tickets(
        session_id=sess_id,
        department_name=department_name,
        semester_code=semester_code,
        status="ISSUED",
    )
    return {
        "status": "success",
        "session_id": str(sess_id),
        "total_admit_cards": len(tickets),
        "tickets": [t.model_dump() for t in tickets],
        "format": "STANDARD_A4_TWO_PER_PAGE",
    }



# ------------------- Phase 4 Module 6: Seating & Room Management Endpoints -------------------
@exam_router.get("/seating/buildings", response_model=List[ExamBuildingResponse])
async def list_exam_buildings(
    institute_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[ExamBuildingResponse]:
    """Lists examination building complexes with floor and elevator accessibility details."""
    inst_id = institute_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-institute-indore")
    service = ExamSeatingService(db)
    return await service.list_buildings(inst_id)


@exam_router.post("/seating/buildings", response_model=ExamBuildingResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_building(
    payload: ExamBuildingCreate,
    institute_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> ExamBuildingResponse:
    """Configures a new examination building complex."""
    inst_id = institute_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-institute-indore")
    service = ExamSeatingService(db)
    return await service.create_building(inst_id, payload)


@exam_router.get("/seating/rooms", response_model=List[ExamRoomLayoutResponse])
async def list_exam_room_layouts(
    building_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[ExamRoomLayoutResponse]:
    """Lists examination rooms and labs with bench layout grids, CCTV, and AC specifications."""
    service = ExamSeatingService(db)
    return await service.list_rooms(building_id)


@exam_router.post("/seating/rooms", response_model=ExamRoomLayoutResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_room_layout(
    payload: ExamRoomLayoutCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> ExamRoomLayoutResponse:
    """Configures an examination hall or laboratory bench layout."""
    service = ExamSeatingService(db)
    return await service.create_room_layout(payload)


@exam_router.post("/seating/plans/generate", response_model=SeatingPlanResponse, status_code=status.HTTP_201_CREATED)
async def generate_exam_seating_plan(
    payload: SeatingPlanGenerateRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> SeatingPlanResponse:
    """Executes randomized or checkerboard alternating department seating allocation for a room."""
    service = ExamSeatingService(db)
    return await service.generate_seating_plan(payload)


@exam_router.get("/seating/plans", response_model=List[SeatingPlanResponse])
async def list_exam_seating_plans(
    session_id: Optional[uuid.UUID] = Query(None),
    exam_date: Optional[date] = Query(None),
    slot_code: Optional[str] = Query(None),
    room_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[SeatingPlanResponse]:
    """Lists generated seating plans across examination halls and dates."""
    sess_id = session_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-session-2026")
    service = ExamSeatingService(db)
    return await service.list_seating_plans(sess_id, exam_date, slot_code, room_id)


@exam_router.get("/seating/plans/{plan_id}", response_model=SeatingPlanResponse)
async def get_exam_seating_plan(
    plan_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> SeatingPlanResponse:
    """Retrieves full 2D bench seating grid matrix for an examination hall."""
    service = ExamSeatingService(db)
    return await service.get_seating_plan(plan_id)


@exam_router.get("/seating/plans/{plan_id}/door-notice", response_model=SeatingPlanDoorNoticeResponse)
async def get_seating_plan_door_notice(
    plan_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> SeatingPlanDoorNoticeResponse:
    """Generates official printable examination hall door notice with roll number ranges and invigilator rosters."""
    service = ExamSeatingService(db)
    return await service.generate_door_notice(plan_id)



# ------------------- Phase 4 Module 7: Invigilator Management Endpoints -------------------
@exam_router.get("/invigilators/profiles", response_model=List[InvigilatorProfileResponse])
async def list_exam_invigilators(
    institute_id: Optional[uuid.UUID] = Query(None),
    is_external: Optional[bool] = Query(None),
    department_name: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[InvigilatorProfileResponse]:
    """Lists internal faculty invigilators and external state university examiners."""
    inst_id = institute_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-institute-indore")
    service = ExamInvigilatorService(db)
    return await service.list_profiles(inst_id, is_external, department_name)


@exam_router.post("/invigilators/profiles", response_model=InvigilatorProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_invigilator_profile(
    payload: InvigilatorProfileCreate,
    institute_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> InvigilatorProfileResponse:
    """Registers an internal faculty member or external university examiner."""
    inst_id = institute_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-institute-indore")
    service = ExamInvigilatorService(db)
    return await service.create_profile(inst_id, payload)


@exam_router.get("/invigilators/rosters", response_model=List[InvigilatorRosterResponse])
async def list_exam_invigilator_rosters(
    session_id: Optional[uuid.UUID] = Query(None),
    duty_date: Optional[date] = Query(None),
    slot_code: Optional[str] = Query(None),
    room_number: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[InvigilatorRosterResponse]:
    """Lists examination duty rosters with invigilator relations, check-in status, and role assignments."""
    sess_id = session_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-session-2026")
    service = ExamInvigilatorService(db)
    return await service.list_rosters(sess_id, duty_date, slot_code, room_number, status)


@exam_router.post("/invigilators/rosters/auto-allocate", response_model=InvigilatorAutoRosterResponse, status_code=status.HTTP_201_CREATED)
async def auto_allocate_invigilator_rosters(
    payload: InvigilatorAutoRosterRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> InvigilatorAutoRosterResponse:
    """Automates fair duty roster allocation ensuring non-departmental invigilation and workload limits."""
    service = ExamInvigilatorService(db)
    return await service.auto_allocate_roster(payload)


@exam_router.post("/invigilators/rosters/{roster_id}/attendance", response_model=InvigilatorRosterResponse)
async def record_invigilator_attendance(
    roster_id: uuid.UUID,
    payload: InvigilatorAttendanceRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> InvigilatorRosterResponse:
    """Records invigilator check-in timestamp and reporting status (REPORTED_PRESENT, LATE, ABSENT)."""
    service = ExamInvigilatorService(db)
    return await service.record_attendance(roster_id, payload)


@exam_router.post("/invigilators/rosters/{roster_id}/replace", response_model=InvigilatorRosterResponse)
async def replace_exam_invigilator(
    roster_id: uuid.UUID,
    payload: InvigilatorReplacementRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> InvigilatorRosterResponse:
    """Replaces an absent or late invigilator with a standby reliever, maintaining complete audit trail."""
    service = ExamInvigilatorService(db)
    return await service.replace_invigilator(roster_id, payload)


@exam_router.post("/invigilators/rosters/{roster_id}/report", response_model=InvigilatorRosterResponse)
async def submit_exam_duty_report(
    roster_id: uuid.UUID,
    payload: InvigilatorDutyReportSubmitRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> InvigilatorRosterResponse:
    """Submits end-of-examination duty report logging booklets issued/collected and malpractice incidents."""
    service = ExamInvigilatorService(db)
    return await service.submit_duty_report(roster_id, payload)



# ------------------- Phase 4 Module 8: Practical & Viva Management Endpoints -------------------
@exam_router.get("/practical/assessments", response_model=List[PracticalAssessmentResponse])
async def list_exam_practical_assessments(
    session_id: Optional[uuid.UUID] = Query(None),
    assessment_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[PracticalAssessmentResponse]:
    """Lists practical examinations, viva voce sessions, and OSCE/OSPE clinical stations."""
    sess_id = session_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-session-2026")
    service = ExamPracticalService(db)
    return await service.list_assessments(sess_id, assessment_type, status)


@exam_router.post("/practical/assessments", response_model=PracticalAssessmentResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_practical_assessment(
    payload: PracticalAssessmentCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> PracticalAssessmentResponse:
    """Configures a new practical lab exam, viva defense, or clinical OSCE station with scoring rubrics."""
    service = ExamPracticalService(db)
    return await service.create_assessment(payload)


@exam_router.get("/practical/assessments/{assessment_id}", response_model=PracticalAssessmentResponse)
async def get_exam_practical_assessment(
    assessment_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> PracticalAssessmentResponse:
    """Retrieves practical assessment station details, examiner pairings, and rubric definitions."""
    service = ExamPracticalService(db)
    return await service.get_assessment(assessment_id)


@exam_router.get("/practical/assessments/{assessment_id}/scores", response_model=List[PracticalScoreRecordResponse])
async def list_practical_student_scores(
    assessment_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[PracticalScoreRecordResponse]:
    """Lists candidate marks awarded across internal, external, viva, and rubric station components."""
    service = ExamPracticalService(db)
    return await service.list_scores(assessment_id)


@exam_router.post("/practical/assessments/{assessment_id}/scores", response_model=PracticalBatchMarksEntryResponse)
async def enter_batch_practical_scores(
    assessment_id: uuid.UUID,
    payload: PracticalBatchMarksEntryRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.marks_entry")),
) -> PracticalBatchMarksEntryResponse:
    """Records batch marks entries awarded by internal and external examiner panels."""
    service = ExamPracticalService(db)
    return await service.enter_batch_scores(assessment_id, payload)


@exam_router.post("/practical/assessments/{assessment_id}/lock", response_model=PracticalAssessmentResponse)
async def lock_practical_assessment_marks(
    assessment_id: uuid.UUID,
    payload: PracticalLockApprovalRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> PracticalAssessmentResponse:
    """Locks practical and viva marks with mutual sign-off from both Internal and External examiners."""
    service = ExamPracticalService(db)
    return await service.lock_and_approve(assessment_id, payload)



# ------------------- Phase 4 Module 9: Attendance During Exams Endpoints -------------------
@exam_router.get("/attendance/records", response_model=List[CandidateAttendanceResponse])
async def list_exam_attendance_records(
    schedule_id: uuid.UUID = Query(...),
    room_number: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[CandidateAttendanceResponse]:
    """Lists candidate examination hall attendance records with barcode binding and status flags."""
    service = ExamAttendanceService(db)
    return await service.list_attendance(schedule_id, room_number, status)


@exam_router.post("/attendance/scan-entry", response_model=AttendanceQrScanResponse)
async def record_candidate_qr_scan_entry(
    payload: AttendanceQrScanRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> AttendanceQrScanResponse:
    """Verifies candidate entrance scanning via QR code or barcode reader, binding the main answer booklet."""
    service = ExamAttendanceService(db)
    return await service.record_qr_scan(payload)


@exam_router.post("/attendance/batch-update", response_model=AttendanceBatchUpdateResponse)
async def batch_update_candidate_attendance(
    payload: AttendanceBatchUpdateRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> AttendanceBatchUpdateResponse:
    """Batch updates attendance statuses, booklet barcodes, and supplementary sheet counts."""
    service = ExamAttendanceService(db)
    return await service.batch_update_attendance(payload)


@exam_router.post("/attendance/{attendance_id}/malpractice", response_model=CandidateAttendanceResponse)
async def log_exam_malpractice_incident(
    attendance_id: uuid.UUID,
    payload: MalpracticeReportRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> CandidateAttendanceResponse:
    """Logs an examination malpractice incident with evidence notes and confiscated materials."""
    service = ExamAttendanceService(db)
    return await service.log_malpractice(attendance_id, payload)


@exam_router.post("/attendance/{attendance_id}/medical-case", response_model=CandidateAttendanceResponse)
async def log_exam_medical_contingency(
    attendance_id: uuid.UUID,
    payload: MedicalCaseReportRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> CandidateAttendanceResponse:
    """Logs a medical contingency during examinations with compensatory time notes."""
    service = ExamAttendanceService(db)
    return await service.log_medical_case(attendance_id, payload)


@exam_router.get("/attendance/hall-summary", response_model=HallAttendanceSummaryResponse)
async def get_exam_hall_attendance_summary(
    schedule_id: uuid.UUID = Query(...),
    room_number: str = Query(..., description="e.g. HALL-A1"),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> HallAttendanceSummaryResponse:
    """Returns hall sealing attendance reconciliation summary for packaging with answer scripts."""
    service = ExamAttendanceService(db)
    return await service.get_hall_summary(schedule_id, room_number)



# ------------------- Phase 4 Module 10: Evaluation Management Endpoints -------------------
@exam_router.get("/evaluation/batches", response_model=List[EvaluationBatchResponse])
async def list_exam_evaluation_batches(
    session_id: Optional[uuid.UUID] = Query(None),
    evaluation_mode: Optional[str] = Query(None),
    evaluation_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[EvaluationBatchResponse]:
    """Lists digital on-screen and physical manual evaluation batches."""
    sess_id = session_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-session-2026")
    service = ExamEvaluationService(db)
    return await service.list_batches(sess_id, evaluation_mode, evaluation_type, status)


@exam_router.post("/evaluation/batches", response_model=EvaluationBatchResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_evaluation_batch(
    payload: EvaluationBatchCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> EvaluationBatchResponse:
    """Configures a new double-blind or single evaluation batch."""
    service = ExamEvaluationService(db)
    return await service.create_batch(payload)


@exam_router.get("/evaluation/batches/{batch_id}/scripts", response_model=List[ScriptEvaluationResponse])
async def list_batch_scripts_for_evaluation(
    batch_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[ScriptEvaluationResponse]:
    """Retrieves masked scripts with dummy barcodes for unbiased on-screen digital evaluation."""
    service = ExamEvaluationService(db)
    return await service.list_scripts_for_evaluator(batch_id)


@exam_router.post("/evaluation/scripts/{script_id}/score", response_model=ScriptEvaluationResponse)
async def submit_evaluator_script_score(
    script_id: uuid.UUID,
    payload: ScriptScoreSubmitRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.marks_entry")),
) -> ScriptEvaluationResponse:
    """Submits question-wise scores from Evaluator 1 or 2, calculating deviation discrepancy."""
    service = ExamEvaluationService(db)
    return await service.submit_script_score(script_id, payload)


@exam_router.post("/evaluation/scripts/{script_id}/moderation", response_model=ScriptEvaluationResponse)
async def apply_chief_moderation_score(
    script_id: uuid.UUID,
    payload: ModerationApplyRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> ScriptEvaluationResponse:
    """Applies Chief Moderator score to resolve >15% discrepancy between double evaluators."""
    service = ExamEvaluationService(db)
    return await service.apply_moderation(script_id, payload)


@exam_router.post("/evaluation/scripts/{script_id}/grace-marks", response_model=ScriptEvaluationResponse)
async def apply_script_grace_marks(
    script_id: uuid.UUID,
    payload: GraceMarksApplyRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> ScriptEvaluationResponse:
    """Applies statutory university ordinance grace marks (up to 5 marks) to clear passing threshold."""
    service = ExamEvaluationService(db)
    return await service.apply_grace_marks(script_id, payload)


@exam_router.post("/evaluation/scripts/{script_id}/recheck", response_model=ScriptEvaluationResponse)
async def process_script_rechecking(
    script_id: uuid.UUID,
    payload: RecheckingProcessRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> ScriptEvaluationResponse:
    """Processes arithmetic scrutiny and unmarked question verification for rechecking requests."""
    service = ExamEvaluationService(db)
    return await service.process_rechecking(script_id, payload)



# ------------------- Phase 4 Module 11: Marks Entry Endpoints -------------------
@exam_router.get("/marks-entry/submissions", response_model=List[MarksSubmissionResponse])
async def list_exam_marks_submissions(
    session_id: Optional[uuid.UUID] = Query(None),
    faculty_user_id: Optional[uuid.UUID] = Query(None),
    department_name: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[MarksSubmissionResponse]:
    """Lists marks submission packets with course, component, and multi-level approval status."""
    sess_id = session_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-session-2026")
    service = ExamMarksEntryService(db)
    return await service.list_submissions(sess_id, faculty_user_id, department_name, status)


@exam_router.post("/marks-entry/submissions", response_model=MarksSubmissionResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_marks_submission(
    payload: MarksSubmissionCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> MarksSubmissionResponse:
    """Configures a new marks entry submission packet for a course component."""
    service = ExamMarksEntryService(db)
    return await service.create_submission(payload)


@exam_router.get("/marks-entry/submissions/{submission_id}", response_model=MarksSubmissionResponse)
async def get_exam_marks_submission(
    submission_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> MarksSubmissionResponse:
    """Retrieves single marks submission packet details."""
    service = ExamMarksEntryService(db)
    return await service.get_submission(submission_id)


@exam_router.get("/marks-entry/submissions/{submission_id}/entries", response_model=List[StudentMarkItemResponse])
async def list_submission_student_mark_entries(
    submission_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[StudentMarkItemResponse]:
    """Lists student mark rows with roll numbers, marks, and auto-computed UGC grade letters."""
    service = ExamMarksEntryService(db)
    return await service.list_entries(submission_id)


@exam_router.post("/marks-entry/submissions/{submission_id}/entries", response_model=MarksBatchSaveResponse)
async def save_batch_student_marks(
    submission_id: uuid.UUID,
    payload: MarksBatchSaveRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.marks_entry")),
) -> MarksBatchSaveResponse:
    """Saves candidate marks with ceiling validation, grade letter calculation, and pass/fail auditing."""
    service = ExamMarksEntryService(db)
    return await service.save_batch_marks(submission_id, payload)


@exam_router.post("/marks-entry/submissions/{submission_id}/import-excel", response_model=MarksExcelImportResponse)
async def import_student_marks_from_excel(
    submission_id: uuid.UUID,
    payload: MarksExcelImportRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.marks_entry")),
) -> MarksExcelImportResponse:
    """Imports offline Excel/CSV marks rows and reconciles against registered candidates."""
    service = ExamMarksEntryService(db)
    return await service.import_excel_marks(submission_id, payload)


@exam_router.post("/marks-entry/submissions/{submission_id}/workflow", response_model=MarksSubmissionResponse)
async def update_marks_approval_workflow(
    submission_id: uuid.UUID,
    payload: MarksWorkflowApprovalRequest,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(require_permissions("exams.manage")),
) -> MarksSubmissionResponse:
    """Transitions marks submission across approval hierarchy (Faculty Submit -> HOD Approve -> COE Lock)."""
    user_id = getattr(user, "id", None)
    service = ExamMarksEntryService(db)
    return await service.approve_workflow(submission_id, payload, user_id)


@exam_router.get("/marks-entry/template")
async def get_marks_excel_template_structure(
    course_code: str = Query("CS-301"),
    max_marks: float = Query(30.0),
) -> Dict[str, Any]:
    """Returns official pre-filled Excel import template structure for faculty offline entry."""
    return {
        "course_code": course_code,
        "max_marks": max_marks,
        "columns": ["Roll Number", "Enrollment No", "Candidate Name", "Marks Obtained", "Is Absent (Y/N)", "Remarks"],
        "sample_rows": [
            {"Roll Number": "230105001", "Enrollment No": "MEI2023CS001", "Candidate Name": "Aarav Sharma", "Marks Obtained": 27.0, "Is Absent": "N", "Remarks": "Good"},
            {"Roll Number": "230105002", "Enrollment No": "MEI2023CS002", "Candidate Name": "Ananya Verma", "Marks Obtained": 28.5, "Is Absent": "N", "Remarks": "Excellent"},
        ],
    }


# ============================================================================
# PHASE 4 MODULE 12: RESULT PROCESSING & MERIT LIST ENDPOINTS
# ============================================================================

@exam_router.get("/results/processed", response_model=List[StudentSemesterResultResponse])
async def list_processed_semester_results(
    session_id: uuid.UUID = Query(...),
    semester_code: Optional[str] = Query(None),
    department_name: Optional[str] = Query(None),
    is_published: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> List[StudentSemesterResultResponse]:
    """Retrieves processed student semester results with SGPA, CGPA, grades, and division classification."""
    return await ExamResultProcessingService.list_processed_results(
        db, session_id, semester_code=semester_code, department_name=department_name, is_published=is_published
    )


@exam_router.post("/results/process-cohort", response_model=ResultProcessingCalculateResponse)
async def process_cohort_semester_results(
    payload: ResultProcessingCalculateRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> ResultProcessingCalculateResponse:
    """Executes automated cohort result calculation (UGC Absolute or Gaussian Relative curve, SGPA/CGPA, ranks)."""
    return await ExamResultProcessingService.process_cohort_results(db, payload)


@exam_router.get("/results/student/{roll_number}", response_model=StudentSemesterResultResponse)
async def get_student_semester_result(
    roll_number: str,
    session_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> StudentSemesterResultResponse:
    """Fetches an individual student comprehensive semester result transcript card."""
    result = await ExamResultProcessingService.get_student_result(db, session_id, roll_number)
    if not result:
        raise HTTPException(status_code=404, detail=f"Result for roll number '{roll_number}' not found")
    return result


@exam_router.get("/results/merit-list", response_model=MeritListResponse)
async def get_institutional_merit_list(
    session_id: uuid.UUID = Query(...),
    program_name: str = Query("B.Tech Computer Science & Engineering"),
    semester_code: str = Query("SEM-5"),
    top_n: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> MeritListResponse:
    """Generates or retrieves official institutional merit list with Gold/Silver/Bronze medalist rankings."""
    req = MeritListGenerateRequest(
        session_id=session_id,
        program_name=program_name,
        semester_code=semester_code,
        top_n=top_n,
    )
    return await ExamResultProcessingService.generate_merit_list(db, req)


@exam_router.post("/results/merit-list/publish", response_model=MeritListResponse)
async def publish_merit_list(
    payload: MeritListGenerateRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> MeritListResponse:
    """Generates and officially publishes institutional merit list."""
    return await ExamResultProcessingService.generate_merit_list(db, payload)


@exam_router.post("/results/publish-session")
async def publish_all_session_results(
    session_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> Dict[str, Any]:
    """Publishes all processed semester results for an examination session to the student portal."""
    return await ExamResultProcessingService.publish_session_results(db, session_id)


# ============================================================================
# PHASE 4 MODULE 13: REVALUATION & SUPPLEMENTARY EXAMINATION ENDPOINTS
# ============================================================================

@exam_router.get("/revaluation/applications", response_model=List[RevaluationApplicationResponse])
async def list_revaluation_applications(
    session_id: uuid.UUID = Query(...),
    service_type: Optional[str] = Query(None),
    application_status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> List[RevaluationApplicationResponse]:
    """Retrieves list of revaluation, script photocopy, and re-totaling applications."""
    return await ExamRevaluationService.list_revaluation_applications(
        db, session_id, service_type=service_type, application_status=application_status
    )


@exam_router.post("/revaluation/apply", response_model=RevaluationApplicationResponse, status_code=status.HTTP_201_CREATED)
async def submit_revaluation_application(
    payload: RevaluationApplicationCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> RevaluationApplicationResponse:
    """Submits student application for re-totaling, photocopy inspection, or challenge revaluation."""
    return await ExamRevaluationService.create_revaluation_application(db, payload)


@exam_router.post("/revaluation/{application_id}/assign-evaluator", response_model=RevaluationApplicationResponse)
async def assign_revaluation_evaluator(
    application_id: uuid.UUID,
    payload: RevaluationAssignEvaluatorRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> RevaluationApplicationResponse:
    """Assigns independent external evaluator to conduct blinded re-evaluation of answer script."""
    res = await ExamRevaluationService.assign_evaluator(db, application_id, payload)
    if not res:
        raise HTTPException(status_code=404, detail="Revaluation application not found")
    return res


@exam_router.post("/revaluation/{application_id}/submit-score", response_model=RevaluationApplicationResponse)
async def submit_revaluation_evaluation_score(
    application_id: uuid.UUID,
    payload: RevaluationScoreSubmitRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> RevaluationApplicationResponse:
    """Records re-evaluated score and verifies autonomous rule threshold (15% difference triggers fee refund)."""
    res = await ExamRevaluationService.submit_revaluation_score(db, application_id, payload)
    if not res:
        raise HTTPException(status_code=404, detail="Revaluation application not found")
    return res


@exam_router.post("/revaluation/{application_id}/finalize", response_model=RevaluationApplicationResponse)
async def finalize_revaluation_case(
    application_id: uuid.UUID,
    payload: RevaluationFinalizeRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> RevaluationApplicationResponse:
    """Finalizes revaluation application with official approval by the Controller of Examinations."""
    res = await ExamRevaluationService.finalize_revaluation(db, application_id, payload)
    if not res:
        raise HTTPException(status_code=404, detail="Revaluation application not found")
    return res


@exam_router.get("/supplementary/registrations", response_model=List[SupplementaryRegistrationResponse])
async def list_supplementary_registrations(
    session_id: uuid.UUID = Query(...),
    course_code: Optional[str] = Query(None),
    is_cleared: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> List[SupplementaryRegistrationResponse]:
    """Lists backlog candidates registered for supplementary / remedial examinations."""
    return await ExamRevaluationService.list_supplementary_registrations(
        db, session_id, course_code=course_code, is_cleared=is_cleared
    )


@exam_router.post("/supplementary/register", response_model=SupplementaryRegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register_supplementary_exam(
    payload: SupplementaryRegistrationCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> SupplementaryRegistrationResponse:
    """Enrolls backlog student for upcoming supplementary examination and generates hall ticket."""
    return await ExamRevaluationService.register_supplementary(db, payload)


@exam_router.post("/supplementary/{registration_id}/record-marks", response_model=SupplementaryRegistrationResponse)
async def record_supplementary_exam_marks(
    registration_id: uuid.UUID,
    payload: SupplementaryRecordMarksRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> SupplementaryRegistrationResponse:
    """Records supplementary examination marks, evaluates pass/fail status, and clears backlog."""
    res = await ExamRevaluationService.record_supplementary_marks(db, registration_id, payload)
    if not res:
        raise HTTPException(status_code=404, detail="Supplementary registration record not found")
    return res


# ============================================================================
# PHASE 4 MODULE 14: TRANSCRIPTS & CERTIFICATES ENDPOINTS
# ============================================================================

@exam_router.get("/certificates/registry", response_model=List[CertificateRegistryResponse])
async def list_registered_certificates(
    session_id: uuid.UUID = Query(...),
    certificate_type: Optional[str] = Query(None),
    roll_number: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> List[CertificateRegistryResponse]:
    """Lists issued official degree certificates, grade cards, and transcripts."""
    return await ExamCertificateService.list_certificates(
        db, session_id, certificate_type=certificate_type, roll_number=roll_number
    )


@exam_router.post("/certificates/issue", response_model=CertificateRegistryResponse, status_code=status.HTTP_201_CREATED)
async def issue_official_certificate(
    payload: CertificateIssueRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> CertificateRegistryResponse:
    """Issues tamper-evident credential embedded with QR verification and SHA-256 digital fingerprint."""
    return await ExamCertificateService.issue_certificate(db, payload)


@exam_router.get("/certificates/{certificate_id}", response_model=CertificateRegistryResponse)
async def get_certificate_by_id(
    certificate_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> CertificateRegistryResponse:
    """Retrieves full credential metadata and digital transcript payload."""
    cert = await ExamCertificateService.get_certificate(db, certificate_id)
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found in institutional registry")
    return cert


@exam_router.get("/certificates/verify/{serial_or_hash}", response_model=CertificateVerificationResponse)
async def verify_certificate_authenticity(
    serial_or_hash: str,
    db: AsyncSession = Depends(get_db_session),
) -> CertificateVerificationResponse:
    """Public instant verification endpoint for employers, universities, and background verification agencies."""
    return await ExamCertificateService.verify_certificate(db, serial_or_hash)


@exam_router.post("/certificates/{certificate_id}/revoke", response_model=CertificateRegistryResponse)
async def revoke_compromised_certificate(
    certificate_id: uuid.UUID,
    payload: CertificateRevokeRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> CertificateRegistryResponse:
    """Revokes invalid, duplicate, or compromised credential with audit reason."""
    cert = await ExamCertificateService.revoke_certificate(db, certificate_id, payload)
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return cert


@exam_router.get("/transcripts/requests", response_model=List[TranscriptRequestResponse])
async def list_transcript_dispatch_requests(
    roll_number: Optional[str] = Query(None),
    request_status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> List[TranscriptRequestResponse]:
    """Lists student official transcript and degree requisition orders."""
    return await ExamCertificateService.list_transcript_requests(
        db, roll_number=roll_number, request_status=request_status
    )


@exam_router.post("/transcripts/request", response_model=TranscriptRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_transcript_dispatch_request(
    payload: TranscriptRequestCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> TranscriptRequestResponse:
    """Places order for official transcripts (digital, postal, or WES direct dispatch)."""
    return await ExamCertificateService.create_transcript_request(db, payload)


@exam_router.post("/transcripts/requests/{request_id}/status", response_model=TranscriptRequestResponse)
async def update_transcript_dispatch_status(
    request_id: uuid.UUID,
    payload: TranscriptRequestStatusUpdateRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> TranscriptRequestResponse:
    """Updates courier tracking number and fulfillment status for transcript orders."""
    res = await ExamCertificateService.update_transcript_request_status(db, request_id, payload)
    if not res:
        raise HTTPException(status_code=404, detail="Transcript request not found")
    return res


# ============================================================================
# PHASE 4 MODULE 15: COMPLIANCE & UNIVERSITY REPORTS ENDPOINTS
# ============================================================================

@exam_router.get("/compliance/reports", response_model=List[ComplianceReportResponse])
async def list_compliance_reports(
    session_id: uuid.UUID = Query(...),
    regulatory_body: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> List[ComplianceReportResponse]:
    """Retrieves statutory compliance returns and result gazettes for UGC, AICTE, and State University."""
    return await ExamComplianceService.list_compliance_reports(
        db, session_id, regulatory_body=regulatory_body, status=status
    )


@exam_router.post("/compliance/generate-report", response_model=ComplianceReportResponse, status_code=status.HTTP_201_CREATED)
async def generate_compliance_report(
    payload: ComplianceReportCreateRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> ComplianceReportResponse:
    """Generates official regulatory report or statistical pass percentage gazette."""
    return await ExamComplianceService.generate_compliance_report(db, payload)


@exam_router.get("/compliance/reports/{report_id}", response_model=ComplianceReportResponse)
async def get_compliance_report_by_id(
    report_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> ComplianceReportResponse:
    """Retrieves compliance report details and metrics payload."""
    report = await ExamComplianceService.get_compliance_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Compliance report not found")
    return report


@exam_router.post("/compliance/reports/{report_id}/submit", response_model=ComplianceReportResponse)
async def submit_compliance_report(
    report_id: uuid.UUID,
    payload: ComplianceReportSubmitRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> ComplianceReportResponse:
    """Formally submits report to regulatory portal with official submission reference number."""
    res = await ExamComplianceService.submit_compliance_report(db, report_id, payload)
    if not res:
        raise HTTPException(status_code=404, detail="Compliance report not found")
    return res


@exam_router.get("/compliance/malpractice/cases", response_model=List[MalpracticeDisciplinaryResponse])
async def list_malpractice_cases(
    session_id: uuid.UUID = Query(...),
    severity_level: Optional[str] = Query(None),
    tribunal_status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> List[MalpracticeDisciplinaryResponse]:
    """Lists examination malpractice cases investigated by the Institute Disciplinary Tribunal."""
    return await ExamComplianceService.list_malpractice_records(
        db, session_id, severity_level=severity_level, tribunal_status=tribunal_status
    )


@exam_router.post("/compliance/malpractice/report", response_model=MalpracticeDisciplinaryResponse, status_code=status.HTTP_201_CREATED)
async def report_malpractice_incident(
    payload: MalpracticeReportCreateRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> MalpracticeDisciplinaryResponse:
    """Files a formal malpractice charge sheet against candidate under Examination Ordinance Clause 14."""
    return await ExamComplianceService.create_malpractice_record(db, payload)


@exam_router.post("/compliance/malpractice/{case_id}/resolve", response_model=MalpracticeDisciplinaryResponse)
async def resolve_malpractice_tribunal_case(
    case_id: uuid.UUID,
    payload: MalpracticeResolveRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> MalpracticeDisciplinaryResponse:
    """Records final Disciplinary Tribunal ruling, penalty confirmation, or appeal outcome."""
    res = await ExamComplianceService.resolve_malpractice_record(db, case_id, payload)
    if not res:
        raise HTTPException(status_code=404, detail="Malpractice case not found")
    return res


# ============================================================================
# PHASE 4 MODULE 16: EXAMINATION ANALYTICS & PREDICTIVE OUTCOMES ENDPOINTS
# ============================================================================

@exam_router.get("/analytics/courses", response_model=List[CourseAnalyticsMetricResponse])
async def list_course_difficulty_analytics(
    session_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> List[CourseAnalyticsMetricResponse]:
    """Retrieves course-by-course difficulty index, discrimination index, and grade dispersion metrics."""
    return await ExamAnalyticsService.list_course_metrics(db, session_id)


@exam_router.get("/analytics/examiner-bias", response_model=List[ExaminerBiasReportItem])
async def get_examiner_grading_variance_analysis(
    session_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> List[ExaminerBiasReportItem]:
    """Detects evaluator grading bias (leniency vs strictness) across internal and external examiners."""
    return await ExamAnalyticsService.get_examiner_bias_report(db, session_id)


@exam_router.get("/analytics/student-risk", response_model=List[StudentRiskPredictionResponse])
async def list_student_risk_predictions(
    session_id: uuid.UUID = Query(...),
    risk_level: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> List[StudentRiskPredictionResponse]:
    """Retrieves machine learning / rule-based predictive failure risk models for proactive academic counseling."""
    return await ExamAnalyticsService.list_student_risk_predictions(db, session_id, risk_level=risk_level)


@exam_router.post("/analytics/student-risk/{risk_id}/acknowledge", response_model=StudentRiskPredictionResponse)
async def acknowledge_student_risk_case(
    risk_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> StudentRiskPredictionResponse:
    """Marks student academic risk intervention as acknowledged by faculty mentor or HOD."""
    res = await ExamAnalyticsService.acknowledge_risk_prediction(db, risk_id)
    if not res:
        raise HTTPException(status_code=404, detail="Risk prediction case not found")
    return res


@exam_router.get("/analytics/summary-kpis", response_model=AnalyticsSummaryKPIsResponse)
async def get_examination_analytics_summary_kpis(
    session_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> AnalyticsSummaryKPIsResponse:
    """Returns institute-level executive KPI metrics for examination performance and quality assurance."""
    return await ExamAnalyticsService.get_summary_kpis(db, session_id)


# ============================================================================
# PHASE 4 MODULE 17: STUDENT EXAMINATION PORTAL ENDPOINTS
# ============================================================================

@exam_router.get("/student-portal/dashboard", response_model=StudentPortalDashboardResponse)
async def get_student_examination_portal_dashboard(
    roll_number: str = Query("MEI2024CS001"),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> StudentPortalDashboardResponse:
    """Aggregates unified self-service student examination portal dashboard (hall ticket, seating, results, requests)."""
    return await ExamStudentPortalService.get_student_portal_dashboard(db, roll_number)


@exam_router.get("/student-portal/seating", response_model=StudentSeatingLookupResponse)
async def get_student_exam_seating_allocation(
    roll_number: str = Query("MEI2024CS001"),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> StudentSeatingLookupResponse:
    """Instant room, floor, building, and bench lookup for candidate's scheduled examination today."""
    return await ExamStudentPortalService.get_student_seating_lookup(db, roll_number)


@exam_router.post("/student-portal/register-exam")
async def self_service_student_exam_registration(
    payload: StudentExamRegisterRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> Dict[str, Any]:
    """Candidate self-service semester / supplementary examination registration."""
    return await ExamStudentPortalService.register_student_exam(db, payload)


# ============================================================================
# PHASE 4 MODULE 18: FACULTY EXAMINATION PORTAL ENDPOINTS
# ============================================================================

@exam_router.get("/faculty-portal/dashboard", response_model=FacultyPortalDashboardResponse)
async def get_faculty_examination_portal_dashboard(
    session_id: uuid.UUID = Query(...),
    faculty_id: Optional[uuid.UUID] = Query(None),
    faculty_name: str = Query("Dr. Rajeshwari Sharma"),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> FacultyPortalDashboardResponse:
    """Aggregates unified faculty examination dashboard (assigned invigilations, evaluation bundles, marks submissions, swaps)."""
    return await ExamFacultyPortalService.get_faculty_portal_dashboard(
        db, session_id, faculty_id=faculty_id, faculty_name=faculty_name
    )


@exam_router.post("/faculty-portal/duty-swap/request", response_model=FacultyDutySwapResponse, status_code=status.HTTP_201_CREATED)
async def request_invigilation_duty_swap(
    payload: FacultyDutySwapRequestCreate,
    requesting_faculty_id: uuid.UUID = Query(...),
    requesting_faculty_name: str = Query("Dr. Rajeshwari Sharma"),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> FacultyDutySwapResponse:
    """Submits request to exchange scheduled invigilation duty slot with a peer faculty member."""
    return await ExamFacultyPortalService.create_duty_swap(
        db, payload, requesting_faculty_id, requesting_faculty_name
    )


@exam_router.post("/faculty-portal/duty-swap/{swap_id}/respond", response_model=FacultyDutySwapResponse)
async def respond_to_invigilation_duty_swap(
    swap_id: uuid.UUID,
    payload: FacultyDutySwapRespondRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> FacultyDutySwapResponse:
    """Accepts or declines peer invigilation duty swap request."""
    res = await ExamFacultyPortalService.respond_to_duty_swap(db, swap_id, payload)
    if not res:
        raise HTTPException(status_code=404, detail="Duty swap request not found")
    return res


# ============================================================================
# PHASE 4 MODULE 19: CONTROLLER OF EXAMINATIONS (COE) MASTER PORTAL ENDPOINTS
# ============================================================================

@exam_router.get("/coe-portal/cockpit", response_model=CoeGovernanceCockpitResponse)
async def get_coe_governance_master_cockpit(
    session_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> CoeGovernanceCockpitResponse:
    """Master governance cockpit for Controller of Examinations (lifecycle stage, system locks, vault state)."""
    return await ExamCoePortalService.get_governance_cockpit(db, session_id)


@exam_router.post("/coe-portal/stage-transition", response_model=CoeGovernanceCockpitResponse)
async def transition_examination_lifecycle_stage(
    payload: CoeStageTransitionRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> CoeGovernanceCockpitResponse:
    """Transitions institute-wide examination session lifecycle stage with audit entry."""
    return await ExamCoePortalService.transition_lifecycle_stage(db, payload)


@exam_router.post("/coe-portal/lock-toggle", response_model=CoeGovernanceCockpitResponse)
async def toggle_coe_system_security_lock(
    payload: CoeLockToggleRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> CoeGovernanceCockpitResponse:
    """Toggles critical system locks (Registration, Timetable, Marks Entry, Result Declaration)."""
    return await ExamCoePortalService.toggle_lock(db, payload)


@exam_router.post("/coe-portal/qp-vault/unlock")
async def unlock_confidential_question_paper_vault(
    payload: CoeQpVaultUnlockRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> Dict[str, Any]:
    """Dual-custody verification releasing encrypted confidential question paper bundle."""
    return await ExamCoePortalService.unlock_qp_vault(db, payload)


@exam_router.post("/coe-portal/emergency-override", response_model=EmergencyOverrideLogResponse)
async def execute_coe_emergency_override(
    payload: CoeEmergencyOverrideRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> EmergencyOverrideLogResponse:
    """Executes high-privilege emergency action (Question Paper Set Swap, Emergency Room Allocation, Postponement)."""
    return await ExamCoePortalService.execute_emergency_override(db, payload)


@exam_router.get("/coe-portal/audit-trail", response_model=List[EmergencyOverrideLogResponse])
async def list_coe_emergency_override_audit_logs(
    session_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.manage")),
) -> List[EmergencyOverrideLogResponse]:
    """Retrieves immutable audit trail of emergency interventions authorized by the COE."""
    return await ExamCoePortalService.list_emergency_overrides(db, session_id)


# ============================================================================
# PHASE 4 MODULE 20: ENTERPRISE INTEGRATION & SYSTEM READINESS ENDPOINTS
# ============================================================================

@exam_router.get("/system/health", response_model=EmsSystemHealthResponse)
async def get_examination_system_health(
    db: AsyncSession = Depends(get_db_session),
) -> EmsSystemHealthResponse:
    """Returns real-time health diagnostic for the Autonomous Campus Examination System."""
    return await ExamSystemService.get_system_health(db)


@exam_router.get("/system/integration-status", response_model=EmsFullIntegrationMatrixResponse)
async def get_examination_module_integration_matrix(
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> EmsFullIntegrationMatrixResponse:
    """Returns complete 20-module operational status and verification matrix."""
    return await ExamSystemService.get_integration_status(db)


@exam_router.get("/system/summary")
async def get_autonomous_campus_examination_executive_summary(
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("exams.view")),
) -> Dict[str, Any]:
    """Provides high-level executive metrics for Autonomous Campus leadership."""
    return await ExamSystemService.get_system_summary(db)
