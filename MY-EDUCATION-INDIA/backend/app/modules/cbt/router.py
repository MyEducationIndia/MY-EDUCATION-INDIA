from app.modules.cbt.schemas import (
    IntegrationTopologyResponse,
    LMSSyncAssessmentRequest,
    LMSSyncAssessmentResponse,
    WebhookDispatchTestRequest,
    WebhookDispatchTestResponse,
)
from app.modules.cbt.integration_service import CBTEnterpriseIntegrationService
from app.modules.cbt.schemas import (
    AttendanceSummaryResponse,
    InvigilatorDutyReportItem,
    QuestionAuditItemResponse,
    SystemTelemetryReportResponse,
    SecurityAuditSummaryResponse,
    CBTComprehensiveReportBundleResponse,
)
from app.modules.cbt.comprehensive_reports_service import CBTComprehensiveReportsService
from app.modules.cbt.schemas import (
    CBTDeviceHealthResponse,
    SystemDiagnosticRequest,
    SystemDiagnosticResponse,
    CBTIncidentCreateRequest,
    CBTIncidentResponse,
    CapacityPlanningMatrixResponse,
)
from app.modules.cbt.administration_service import CBTAdministrationService
from app.modules.cbt.schemas import (
    MockTestSeriesResponse,
    MockTestRegisterRequest,
    MockAttemptResponse,
    PublicLeaderboardResponse,
    PracticeSubjectCategoryResponse,
)
from app.modules.cbt.mock_test_service import CBTMockTestService
from app.modules.cbt.schemas import (
    CandidatePortalScheduleCard,
    CandidatePortalDashboardResponse,
    CandidateTicketCreateRequest,
    CandidateTicketResponse,
)
from app.modules.cbt.candidate_portal_service import CBTCandidatePortalService
from app.modules.cbt.schemas import (
    CBTCertificateIssueRequest,
    CBTCertificateBatchIssueRequest,
    CBTCertificateResponse,
    CBTPublicVerificationLookupResponse,
)
from app.modules.cbt.certificate_service import CBTCertificateService
from app.modules.cbt.schemas import (
    CandidateScorecardResponse,
    ComparativeCohortAnalyticsResponse,
    SubjectProficiencyItem,
    TopicProficiencyItem,
    AnalyticsExportRequest,
    AnalyticsExportResponse,
)
from app.modules.cbt.results_analytics_service import CBTResultsAnalyticsService
from app.modules.cbt.schemas import (
    EvaluationExecutionRequest,
    EvaluationSummaryResponse,
    GraceMarksApplyRequest,
    ResultModerationRequest,
    EvaluationSessionRosterResponse,
)
from app.modules.cbt.evaluation_service import CBTEvaluationEngineService
from app.modules.cbt.schemas import (
    SecurityViolationReportRequest,
    SecurityViolationReportResponse,
    ProctorIssueWarningRequest,
    ProctorActionRequest,
    ProctorActionResponse,
    LiveProctorDashboardResponse,
)
from app.modules.cbt.proctoring_service import CBTProctoringService
from app.modules.cbt.schemas import (
    CBTHeartbeatRequest,
    CBTHeartbeatResponse,
    LiveExamSessionBundle,
    LiveCandidateAnswerState,
    AutosaveSingleAnswerRequest,
    SubmitLiveExamRequest,
    ClearResponseRequest,
    ToggleReviewRequest,
)
from app.modules.cbt.live_engine_service import CBTLiveEngineService
from datetime import date, datetime
from typing import Any, Dict, List, Optional
import uuid
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db_session
from app.modules.auth.dependencies import get_current_user, require_permissions
from app.modules.cbt.analytics import CBTAnalyticsEngine
from app.modules.cbt.reports import CBTReportEngine
from app.modules.cbt.schemas import (
    CandidateSessionResponse,
    CandidateStartSessionRequest,
    CBTDashboardSummary,
    CBTSessionCreate,
    CBTSessionResponse,
    ExamTemplateCreate,
    ExamTemplateResponse,
    ExamTemplateUpdate,
    QuestionPoolCreate,
    QuestionPoolResponse,
    RandomizationPreviewRequest,
    RandomizationPreviewResponse,
    OfflineBatchSyncRequest,
    QuestionBankCreate,
    QuestionBankResponse,
    QuestionVersionCreate,
    QuestionVersionResponse,
    QuestionCategoryCreate,
    QuestionCategoryResponse,
    QuestionTopicCreate,
    QuestionTopicResponse,
    QuestionTagCreate,
    QuestionTagResponse,
    SaveAnswerItem,
)
from app.modules.cbt.service import CBTService
from app.modules.cbt.foundation_service import CBTFoundationService
from app.modules.cbt.workflow_service import QuestionWorkflowService
from app.modules.cbt.candidate_service import CBTCandidateService
from app.modules.cbt.scheduling_service import CBTSchedulingService
from app.modules.cbt.schemas import (
    ExamCenterCreate,
    ExamCenterResponse,
    ExamLabCreate,
    ExamLabResponse,
    ExamShiftCreate,
    ExamShiftResponse,
    ExamScheduleCalendarEvent,
)
from app.modules.cbt.schemas import (
    CBTCandidateRegisterRequest,
    CBTCandidateResponse,
    BatchCenterAllocationRequest,
    CandidateVerificationRequest,
    AdmitCardResponse,
)
from app.modules.cbt.schemas import (
    QuestionWorkflowTransitionRequest,
    QuestionWorkflowAuditResponse,
    QuestionFeedbackCreate,
    QuestionFeedbackResponse,
    QuestionVersionCloneRequest,
)
from app.modules.cbt.schemas import (
    CBTGlobalConfigResponse,
    CBTGlobalConfigUpdate,
    TimeSyncResponse,
)

cbt_router = APIRouter(prefix="/cbt", tags=["Enterprise CBT Testing Platform"])


# ------------------- Phase 3 Module 1: CBT Foundation -------------------
@cbt_router.get("/foundation/config", response_model=CBTGlobalConfigResponse)
async def get_cbt_foundation_config(
    institute_id: uuid.UUID = Query(default=uuid.UUID("00000000-0000-0000-0000-000000000001")),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> CBTGlobalConfigResponse:
    service = CBTFoundationService(db)
    config = await service.get_or_create_config(institute_id)
    return CBTGlobalConfigResponse.model_validate(config)


@cbt_router.put("/foundation/config", response_model=CBTGlobalConfigResponse)
async def update_cbt_foundation_config(
    payload: CBTGlobalConfigUpdate,
    institute_id: uuid.UUID = Query(default=uuid.UUID("00000000-0000-0000-0000-000000000001")),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("cbt.manage")),
) -> CBTGlobalConfigResponse:
    service = CBTFoundationService(db)
    config = await service.update_config(institute_id, payload)
    return CBTGlobalConfigResponse.model_validate(config)


@cbt_router.get("/time/sync", response_model=TimeSyncResponse)
async def get_time_sync(
    institute_id: uuid.UUID = Query(default=uuid.UUID("00000000-0000-0000-0000-000000000001")),
    db: AsyncSession = Depends(get_db_session),
) -> TimeSyncResponse:
    service = CBTFoundationService(db)
    return await service.get_time_sync(institute_id)



# 1. Dashboard & KPIs
@cbt_router.get("/dashboard", response_model=CBTDashboardSummary)
async def get_cbt_dashboard(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("cbt.view")),
) -> CBTDashboardSummary:
    summary = await CBTAnalyticsEngine.get_dashboard_kpis(db, institute_id)
    return CBTDashboardSummary.model_validate(summary)


# 2. Question Bank
@cbt_router.get("/question-bank", response_model=List[QuestionBankResponse])
async def list_question_banks(
    institute_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[QuestionBankResponse]:
    service = CBTService(db)
    items = await service.repo.get_question_banks(institute_id)
    return [QuestionBankResponse.model_validate(it) for it in items]


@cbt_router.post("/question-bank", response_model=QuestionBankResponse, status_code=status.HTTP_201_CREATED)
async def create_question_bank(
    payload: QuestionBankCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("cbt.manage")),
) -> QuestionBankResponse:
    service = CBTService(db)
    qb = await service.create_question_bank(payload)
    return QuestionBankResponse.model_validate(qb)


@cbt_router.get("/categories", response_model=List[QuestionCategoryResponse])
async def list_categories(
    question_bank_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[QuestionCategoryResponse]:
    service = CBTService(db)
    items = await service.list_categories(question_bank_id)
    return [QuestionCategoryResponse.model_validate(it) for it in items]


@cbt_router.post("/categories", response_model=QuestionCategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    payload: QuestionCategoryCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("cbt.manage")),
) -> QuestionCategoryResponse:
    service = CBTService(db)
    cat = await service.create_category(payload.question_bank_id, payload.code, payload.name)
    return QuestionCategoryResponse.model_validate(cat)


@cbt_router.get("/topics", response_model=List[QuestionTopicResponse])
async def list_topics(
    category_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[QuestionTopicResponse]:
    service = CBTService(db)
    items = await service.list_topics(category_id)
    return [QuestionTopicResponse.model_validate(it) for it in items]


@cbt_router.post("/topics", response_model=QuestionTopicResponse, status_code=status.HTTP_201_CREATED)
async def create_topic(
    payload: QuestionTopicCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("cbt.manage")),
) -> QuestionTopicResponse:
    service = CBTService(db)
    topic = await service.create_topic(payload.category_id, payload.name)
    return QuestionTopicResponse.model_validate(topic)


@cbt_router.get("/questions", response_model=List[QuestionVersionResponse])
async def list_questions(
    topic_id: Optional[uuid.UUID] = Query(default=None),
    difficulty_level: Optional[str] = Query(default=None),
    question_type: Optional[str] = Query(default=None),
    language: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[QuestionVersionResponse]:
    service = CBTService(db)
    items = await service.list_questions(
        topic_id=topic_id,
        difficulty_level=difficulty_level,
        question_type=question_type,
        language=language,
        search=search,
    )
    return [QuestionVersionResponse.model_validate(it) for it in items]


@cbt_router.get("/questions/{question_id}", response_model=QuestionVersionResponse)
async def get_question(
    question_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> QuestionVersionResponse:
    service = CBTService(db)
    q = await service.get_question(question_id)
    if not q:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Question not found")
    return QuestionVersionResponse.model_validate(q)


@cbt_router.post("/questions", response_model=QuestionVersionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    payload: QuestionVersionCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("cbt.manage")),
) -> QuestionVersionResponse:
    service = CBTService(db)
    q = await service.create_question(payload)
    return QuestionVersionResponse.model_validate(q)


@cbt_router.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
    question_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("cbt.manage")),
) -> None:
    service = CBTService(db)
    success = await service.delete_question(question_id)
    if not success:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Question not found")


@cbt_router.get("/tags", response_model=List[QuestionTagResponse])
async def list_tags(
    institute_id: uuid.UUID = Query(default=uuid.UUID("00000000-0000-0000-0000-000000000001")),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[QuestionTagResponse]:
    service = CBTService(db)
    tags = await service.list_tags(institute_id)
    return [QuestionTagResponse.model_validate(it) for it in tags]


@cbt_router.post("/tags", response_model=QuestionTagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    payload: QuestionTagCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("cbt.manage")),
) -> QuestionTagResponse:
    service = CBTService(db)
    tag = await service.create_tag(payload.institute_id, payload.tag_name)
    return QuestionTagResponse.model_validate(tag)

# ------------------- Phase 3 Module 3: Question Workflow Endpoints -------------------
@cbt_router.post("/questions/{question_id}/workflow/transition", response_model=QuestionVersionResponse)
async def transition_question_workflow(
    question_id: uuid.UUID,
    payload: QuestionWorkflowTransitionRequest,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user),
) -> QuestionVersionResponse:
    service = QuestionWorkflowService(db)
    actor_id = getattr(user, "id", uuid.uuid4())
    q = await service.transition_question_status(question_id, payload, actor_id)
    return QuestionVersionResponse.model_validate(q)


@cbt_router.get("/questions/{question_id}/workflow/history", response_model=List[QuestionWorkflowAuditResponse])
async def get_question_workflow_history(
    question_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[QuestionWorkflowAuditResponse]:
    service = QuestionWorkflowService(db)
    items = await service.get_workflow_history(question_id)
    return [QuestionWorkflowAuditResponse.model_validate(it) for it in items]


@cbt_router.post("/questions/{question_id}/workflow/feedback", response_model=QuestionFeedbackResponse, status_code=status.HTTP_201_CREATED)
async def submit_question_feedback(
    question_id: uuid.UUID,
    payload: QuestionFeedbackCreate,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user),
) -> QuestionFeedbackResponse:
    service = QuestionWorkflowService(db)
    reviewer_id = getattr(user, "id", uuid.uuid4())
    fb = await service.submit_review_feedback(question_id, payload, reviewer_id)
    return QuestionFeedbackResponse.model_validate(fb)


@cbt_router.get("/questions/{question_id}/workflow/feedbacks", response_model=List[QuestionFeedbackResponse])
async def list_question_feedbacks(
    question_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[QuestionFeedbackResponse]:
    service = QuestionWorkflowService(db)
    items = await service.get_feedbacks(question_id)
    return [QuestionFeedbackResponse.model_validate(it) for it in items]


@cbt_router.post("/questions/{question_id}/workflow/new-version", response_model=QuestionVersionResponse, status_code=status.HTTP_201_CREATED)
async def clone_question_version(
    question_id: uuid.UUID,
    payload: QuestionVersionCloneRequest,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user),
) -> QuestionVersionResponse:
    service = QuestionWorkflowService(db)
    actor_id = getattr(user, "id", uuid.uuid4())
    new_q = await service.clone_as_new_version(question_id, payload.changelog, actor_id)
    return QuestionVersionResponse.model_validate(new_q)



# 3. Exam Templates & CBT Sessions
@cbt_router.get("/templates", response_model=List[ExamTemplateResponse])
async def list_exam_templates(
    institute_id: uuid.UUID = Query(default=uuid.UUID("00000000-0000-0000-0000-000000000001")),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[ExamTemplateResponse]:
    service = CBTService(db)
    items = await service.list_templates(institute_id)
    return [ExamTemplateResponse.model_validate(it) for it in items]


@cbt_router.get("/templates/{template_id}", response_model=ExamTemplateResponse)
async def get_exam_template(
    template_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> ExamTemplateResponse:
    service = CBTService(db)
    t = await service.get_template(template_id)
    if not t:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Exam template not found")
    return ExamTemplateResponse.model_validate(t)


@cbt_router.post("/templates", response_model=ExamTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_template(
    payload: ExamTemplateCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("cbt.manage")),
) -> ExamTemplateResponse:
    service = CBTService(db)
    t = await service.create_exam_template(payload)
    return ExamTemplateResponse.model_validate(t)


@cbt_router.put("/templates/{template_id}", response_model=ExamTemplateResponse)
async def update_exam_template(
    template_id: uuid.UUID,
    payload: ExamTemplateUpdate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("cbt.manage")),
) -> ExamTemplateResponse:
    service = CBTService(db)
    t = await service.update_template(template_id, payload)
    if not t:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Exam template not found")
    return ExamTemplateResponse.model_validate(t)


@cbt_router.delete("/templates/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exam_template(
    template_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("cbt.manage")),
) -> None:
    service = CBTService(db)
    success = await service.delete_template(template_id)
    if not success:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Exam template not found")


@cbt_router.get("/pools", response_model=List[QuestionPoolResponse])
async def list_question_pools(
    institute_id: uuid.UUID = Query(default=uuid.UUID("00000000-0000-0000-0000-000000000001")),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[QuestionPoolResponse]:
    service = CBTService(db)
    items = await service.list_pools(institute_id)
    return [QuestionPoolResponse.model_validate(it) for it in items]


@cbt_router.post("/pools", response_model=QuestionPoolResponse, status_code=status.HTTP_201_CREATED)
async def create_question_pool(
    payload: QuestionPoolCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("cbt.manage")),
) -> QuestionPoolResponse:
    service = CBTService(db)
    p = await service.create_pool(payload)
    return QuestionPoolResponse.model_validate(p)


@cbt_router.post("/templates/preview-randomization", response_model=RandomizationPreviewResponse)
async def preview_template_randomization(
    payload: RandomizationPreviewRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> RandomizationPreviewResponse:
    service = CBTService(db)
    data = await service.preview_randomization(
        template_id=payload.template_id,
        candidate_seed=payload.candidate_seed,
        shuffle_options=payload.shuffle_options,
    )
    return RandomizationPreviewResponse(**data)

# ------------------- Phase 3 Module 5: Candidate Management Endpoints -------------------
@cbt_router.post("/candidates/register", response_model=CBTCandidateResponse, status_code=status.HTTP_201_CREATED)
async def register_candidate(
    payload: CBTCandidateRegisterRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("cbt.manage")),
) -> CBTCandidateResponse:
    service = CBTCandidateService(db)
    cand = await service.register_candidate(payload)
    return CBTCandidateResponse.model_validate(cand)


@cbt_router.get("/candidates", response_model=List[CBTCandidateResponse])
async def list_candidates(
    institute_id: uuid.UUID = Query(default=uuid.UUID("00000000-0000-0000-0000-000000000001")),
    session_id: Optional[uuid.UUID] = Query(default=None),
    verification_status: Optional[str] = Query(default=None),
    candidate_type: Optional[str] = Query(default=None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[CBTCandidateResponse]:
    service = CBTCandidateService(db)
    items = await service.list_candidates(
        institute_id=institute_id,
        session_id=session_id,
        verification_status=verification_status,
        candidate_type=candidate_type,
    )
    return [CBTCandidateResponse.model_validate(it) for it in items]


@cbt_router.get("/candidates/{candidate_id}", response_model=CBTCandidateResponse)
async def get_candidate(
    candidate_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> CBTCandidateResponse:
    service = CBTCandidateService(db)
    cand = await service.get_candidate_by_id(candidate_id)
    if not cand:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Candidate not found")
    return CBTCandidateResponse.model_validate(cand)


@cbt_router.post("/candidates/{candidate_id}/allocate", response_model=CBTCandidateResponse)
async def allocate_batch_center(
    candidate_id: uuid.UUID,
    payload: BatchCenterAllocationRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("cbt.manage")),
) -> CBTCandidateResponse:
    service = CBTCandidateService(db)
    cand = await service.allocate_batch_center(candidate_id, payload)
    return CBTCandidateResponse.model_validate(cand)


@cbt_router.post("/candidates/{candidate_id}/verify-identity", response_model=CBTCandidateResponse)
async def verify_candidate_identity(
    candidate_id: uuid.UUID,
    payload: CandidateVerificationRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("cbt.proctor")),
) -> CBTCandidateResponse:
    service = CBTCandidateService(db)
    cand = await service.verify_identity(candidate_id, payload)
    return CBTCandidateResponse.model_validate(cand)


@cbt_router.get("/candidates/{candidate_id}/admit-card", response_model=AdmitCardResponse)
async def get_candidate_admit_card(
    candidate_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> AdmitCardResponse:
    service = CBTCandidateService(db)
    return await service.get_admit_card(candidate_id)

# ------------------- Phase 3 Module 6: Exam Scheduling & Centers Endpoints -------------------
@cbt_router.get("/scheduling/centers", response_model=List[ExamCenterResponse])
async def list_exam_centers(
    institute_id: uuid.UUID = Query(default=uuid.UUID("00000000-0000-0000-0000-000000000001")),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[ExamCenterResponse]:
    service = CBTSchedulingService(db)
    items = await service.list_centers(institute_id)
    return [ExamCenterResponse.model_validate(it) for it in items]


@cbt_router.post("/scheduling/centers", response_model=ExamCenterResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_center(
    payload: ExamCenterCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("cbt.manage")),
) -> ExamCenterResponse:
    service = CBTSchedulingService(db)
    center = await service.create_center(payload)
    return ExamCenterResponse.model_validate(center)


@cbt_router.get("/scheduling/centers/{center_id}/labs", response_model=List[ExamLabResponse])
async def list_center_labs(
    center_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[ExamLabResponse]:
    service = CBTSchedulingService(db)
    items = await service.list_labs(center_id)
    return [ExamLabResponse.model_validate(it) for it in items]


@cbt_router.post("/scheduling/centers/{center_id}/labs", response_model=ExamLabResponse, status_code=status.HTTP_201_CREATED)
async def create_center_lab(
    center_id: uuid.UUID,
    payload: ExamLabCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("cbt.manage")),
) -> ExamLabResponse:
    service = CBTSchedulingService(db)
    lab = await service.create_lab(payload)
    return ExamLabResponse.model_validate(lab)


@cbt_router.get("/scheduling/shifts", response_model=List[ExamShiftResponse])
async def list_exam_shifts(
    session_id: Optional[uuid.UUID] = Query(default=None),
    exam_date: Optional[date] = Query(default=None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[ExamShiftResponse]:
    service = CBTSchedulingService(db)
    items = await service.list_shifts(session_id, exam_date)
    return [ExamShiftResponse.model_validate(it) for it in items]


@cbt_router.post("/scheduling/shifts", response_model=ExamShiftResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_shift(
    payload: ExamShiftCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("cbt.manage")),
) -> ExamShiftResponse:
    service = CBTSchedulingService(db)
    shift = await service.create_shift(payload)
    return ExamShiftResponse.model_validate(shift)


@cbt_router.get("/scheduling/calendar", response_model=List[ExamScheduleCalendarEvent])
async def get_schedule_calendar(
    institute_id: uuid.UUID = Query(default=uuid.UUID("00000000-0000-0000-0000-000000000001")),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[ExamScheduleCalendarEvent]:
    service = CBTSchedulingService(db)
    return await service.get_calendar_events(institute_id)


@cbt_router.post("/scheduling/shifts/{shift_id}/dispatch-reminders", response_model=Dict[str, Any])
async def dispatch_shift_reminders(
    shift_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("cbt.manage")),
) -> Dict[str, Any]:
    service = CBTSchedulingService(db)
    return await service.dispatch_shift_reminders(shift_id)




@cbt_router.post("/sessions", response_model=CBTSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_cbt_session(
    payload: CBTSessionCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(require_permissions("cbt.manage")),
) -> CBTSessionResponse:
    service = CBTService(db)
    s = await service.create_cbt_session(payload)
    return CBTSessionResponse.model_validate(s)


# 4. Candidate Delivery
@cbt_router.post("/delivery/start", response_model=CandidateSessionResponse)
async def start_exam(
    payload: CandidateStartSessionRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> CandidateSessionResponse:
    service = CBTService(db)
    cs = await service.start_candidate_session(
        payload.cbt_session_id,
        payload.student_id,
        payload.device_fingerprint,
        payload.ip_address,
    )
    return CandidateSessionResponse.model_validate(cs)


@cbt_router.post("/delivery/autosave", status_code=status.HTTP_200_OK)
async def autosave_answers(
    candidate_session_id: uuid.UUID = Query(...),
    answers: List[SaveAnswerItem] = ...,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> Dict[str, Any]:
    service = CBTService(db)
    await service.save_candidate_answers(candidate_session_id, answers)
    return {"status": "saved", "count": len(answers)}


@cbt_router.post("/delivery/submit", response_model=CandidateSessionResponse)
async def submit_exam(
    candidate_session_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> CandidateSessionResponse:
    service = CBTService(db)
    cs = await service.submit_candidate_exam(candidate_session_id)
    return CandidateSessionResponse.model_validate(cs)


# 5. Offline Sync
@cbt_router.post("/offline-sync", status_code=status.HTTP_200_OK)
async def sync_offline_answers(
    payload: OfflineBatchSyncRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> Dict[str, Any]:
    service = CBTService(db)
    await service.save_candidate_answers(payload.candidate_session_id, payload.answers)
    return {"status": "synced", "batch_count": len(payload.answers), "checksum": payload.checksum}


# 6. Reports
@cbt_router.get("/reports/score", response_model=Dict[str, Any])
async def get_candidate_score(
    candidate_session_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> Dict[str, Any]:
    return await CBTReportEngine.get_candidate_score_report(db, candidate_session_id)


# ------------------- Phase 3 Module 7: Live Examination Engine Endpoints -------------------
@cbt_router.get("/delivery/bundle", response_model=LiveExamSessionBundle)
async def get_live_exam_bundle(
    cbt_session_id: uuid.UUID = Query(...),
    student_id: Optional[uuid.UUID] = Query(None),
    device_fingerprint: Optional[str] = Query(None),
    ip_address: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user),
) -> LiveExamSessionBundle:
    """Initializes or restores complete examination state bundle for the candidate."""
    active_student_id = student_id or getattr(user, "id", uuid.uuid4())
    live_service = CBTLiveEngineService(db)
    return await live_service.get_or_create_live_session(
        cbt_session_id=cbt_session_id,
        student_id=active_student_id,
        device_fingerprint=device_fingerprint,
        ip_address=ip_address,
    )


@cbt_router.get("/delivery/resume/{candidate_session_id}", response_model=LiveExamSessionBundle)
async def resume_live_exam(
    candidate_session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> LiveExamSessionBundle:
    """Restores candidate examination bundle upon network reconnect or page reload."""
    live_service = CBTLiveEngineService(db)
    return await live_service.resume_session(candidate_session_id)


@cbt_router.post("/delivery/heartbeat", response_model=CBTHeartbeatResponse)
async def process_live_heartbeat(
    payload: CBTHeartbeatRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> CBTHeartbeatResponse:
    """Synchronizes remaining exam timer, checks timer expiration, and updates question index."""
    live_service = CBTLiveEngineService(db)
    return await live_service.process_heartbeat(payload)


@cbt_router.post("/delivery/autosave-single", response_model=LiveCandidateAnswerState)
async def autosave_single_answer(
    payload: AutosaveSingleAnswerRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> LiveCandidateAnswerState:
    """Autosaves candidate answer in real-time, computing palette state."""
    live_service = CBTLiveEngineService(db)
    return await live_service.autosave_answer(payload)


@cbt_router.post("/delivery/clear-response", response_model=LiveCandidateAnswerState)
async def clear_candidate_response(
    payload: ClearResponseRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> LiveCandidateAnswerState:
    """Clears candidate response for a specific question."""
    live_service = CBTLiveEngineService(db)
    return await live_service.clear_response(payload.candidate_session_id, payload.question_id)


@cbt_router.post("/delivery/toggle-review", response_model=LiveCandidateAnswerState)
async def toggle_question_review(
    payload: ToggleReviewRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> LiveCandidateAnswerState:
    """Toggles mark for review status without altering selected answer."""
    live_service = CBTLiveEngineService(db)
    return await live_service.toggle_review(payload.candidate_session_id, payload.question_id, payload.is_marked_for_review)


@cbt_router.post("/delivery/submit-live", response_model=CandidateSessionResponse)
async def submit_live_examination(
    payload: SubmitLiveExamRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> CandidateSessionResponse:
    """Submits examination, evaluates objective scoring, freezes session, and logs reason."""
    live_service = CBTLiveEngineService(db)
    return await live_service.submit_live_exam(payload)


# ------------------- Phase 3 Module 8: Security & Proctoring Endpoints -------------------
@cbt_router.post("/security/incident", response_model=SecurityViolationReportResponse)
async def report_candidate_security_incident(
    payload: SecurityViolationReportRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> SecurityViolationReportResponse:
    """Logs a candidate security breach (tab switch, exit fullscreen, clipboard, devtools)."""
    proctor_service = CBTProctoringService(db)
    return await proctor_service.report_security_incident(payload)


@cbt_router.get("/proctor/live-dashboard", response_model=LiveProctorDashboardResponse)
async def get_live_proctor_dashboard(
    cbt_session_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> LiveProctorDashboardResponse:
    """Streams real-time candidate surveillance grid, integrity states, and incident feed."""
    sess_id = cbt_session_id or uuid.uuid5(uuid.NAMESPACE_DNS, "mei-cbt-default-live-session")
    proctor_service = CBTProctoringService(db)
    return await proctor_service.get_live_proctor_dashboard(sess_id)


@cbt_router.post("/proctor/issue-warning", response_model=ProctorActionResponse)
async def issue_proctor_warning_to_candidate(
    payload: ProctorIssueWarningRequest,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user),
) -> ProctorActionResponse:
    """Broadcasts an official proctor warning directly to candidate workstation."""
    proctor_id = getattr(user, "id", uuid.uuid4())
    proctor_service = CBTProctoringService(db)
    return await proctor_service.issue_proctor_warning(
        candidate_session_id=payload.candidate_session_id,
        proctor_id=proctor_id,
        message_text=payload.message_text,
    )


@cbt_router.post("/proctor/force-disqualify", response_model=ProctorActionResponse)
async def force_disqualify_candidate(
    payload: ProctorActionRequest,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user),
) -> ProctorActionResponse:
    """Immediately disqualifies candidate for severe malpractice."""
    proctor_id = getattr(user, "id", uuid.uuid4())
    proctor_service = CBTProctoringService(db)
    return await proctor_service.force_disqualify(
        candidate_session_id=payload.candidate_session_id,
        proctor_id=proctor_id,
        reason=payload.reason,
    )


@cbt_router.post("/proctor/toggle-pause", response_model=ProctorActionResponse)
async def toggle_candidate_pause(
    candidate_session_id: uuid.UUID = Query(...),
    action: str = Query("PAUSE", description="PAUSE or RESUME"),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> ProctorActionResponse:
    """Pauses or resumes candidate examination timer during local hardware issues."""
    proctor_service = CBTProctoringService(db)
    return await proctor_service.toggle_session_pause(candidate_session_id, action)


# ------------------- Phase 3 Module 9: Evaluation Engine Endpoints -------------------
@cbt_router.post("/evaluation/run", response_model=EvaluationSummaryResponse)
async def run_cbt_evaluation(
    payload: EvaluationExecutionRequest,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user),
) -> EvaluationSummaryResponse:
    """Runs automated objective scoring, negative marking, and rank calculation."""
    eval_service = CBTEvaluationEngineService(db)
    user_id = getattr(user, "id", uuid.uuid4())
    return await eval_service.run_batch_evaluation(payload, user_id)


@cbt_router.get("/evaluation/session/{cbt_session_id}/roster", response_model=EvaluationSessionRosterResponse)
async def get_cbt_evaluation_roster(
    cbt_session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> EvaluationSessionRosterResponse:
    """Retrieves candidate score matrix, ranks, percentiles, and moderation summary."""
    eval_service = CBTEvaluationEngineService(db)
    return await eval_service.get_evaluation_roster(cbt_session_id)


@cbt_router.post("/evaluation/grace-marks", response_model=EvaluationSummaryResponse)
async def apply_cbt_grace_marks(
    payload: GraceMarksApplyRequest,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user),
) -> EvaluationSummaryResponse:
    """Allocates grace marks for disputed questions or marginal pass adjustments."""
    eval_service = CBTEvaluationEngineService(db)
    user_id = getattr(user, "id", uuid.uuid4())
    return await eval_service.apply_grace_marks(payload, user_id)


@cbt_router.post("/evaluation/moderation", response_model=EvaluationSummaryResponse)
async def apply_cbt_result_moderation(
    payload: ResultModerationRequest,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user),
) -> EvaluationSummaryResponse:
    """Applies score curve normalization or percentage scaling across shifts."""
    eval_service = CBTEvaluationEngineService(db)
    user_id = getattr(user, "id", uuid.uuid4())
    return await eval_service.apply_result_moderation(payload, user_id)


@cbt_router.post("/evaluation/publish-to-module11", response_model=Dict[str, Any])
async def publish_results_to_module11(
    cbt_session_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user),
) -> Dict[str, Any]:
    """Publishes finalized moderated marks directly to Module 11 Examination Ledger."""
    eval_service = CBTEvaluationEngineService(db)
    user_id = getattr(user, "id", uuid.uuid4())
    return await eval_service.publish_and_sync_to_module11(cbt_session_id, user_id)


# ------------------- Phase 3 Module 10: Results & Analytics Endpoints -------------------
@cbt_router.get("/analytics/candidate/{candidate_session_id}/scorecard", response_model=CandidateScorecardResponse)
async def get_candidate_cbt_scorecard(
    candidate_session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> CandidateScorecardResponse:
    """Generates itemized candidate scorecard with national rank, percentile, and subject proficiency."""
    analytics_service = CBTResultsAnalyticsService(db)
    return await analytics_service.get_candidate_scorecard(candidate_session_id)


@cbt_router.get("/analytics/session/{cbt_session_id}/cohort-comparative", response_model=ComparativeCohortAnalyticsResponse)
async def get_cohort_comparative_analytics(
    cbt_session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> ComparativeCohortAnalyticsResponse:
    """Calculates statistical cohort metrics (mean, median, standard deviation, percentile cutoffs)."""
    analytics_service = CBTResultsAnalyticsService(db)
    return await analytics_service.get_cohort_comparative_analytics(cbt_session_id)


@cbt_router.get("/analytics/session/{cbt_session_id}/subject-breakdown", response_model=List[SubjectProficiencyItem])
async def get_session_subject_breakdown(
    cbt_session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[SubjectProficiencyItem]:
    """Aggregates subject-level performance across the examination cohort."""
    analytics_service = CBTResultsAnalyticsService(db)
    return await analytics_service.get_subject_breakdown(cbt_session_id)


@cbt_router.get("/analytics/session/{cbt_session_id}/topic-strengths", response_model=List[TopicProficiencyItem])
async def get_session_topic_strengths(
    cbt_session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[TopicProficiencyItem]:
    """Identifies topic strengths and weaknesses with targeted remediation pointers."""
    analytics_service = CBTResultsAnalyticsService(db)
    return await analytics_service.get_topic_strengths(cbt_session_id)


@cbt_router.post("/analytics/export-report", response_model=AnalyticsExportResponse)
async def export_cbt_analytics_report(
    payload: AnalyticsExportRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> AnalyticsExportResponse:
    """Generates export report payload integrated with Module 18 BI Reports Engine."""
    analytics_service = CBTResultsAnalyticsService(db)
    return await analytics_service.export_analytics_report(payload)


# ------------------- Phase 3 Module 11: Certificate Integration Endpoints -------------------
@cbt_router.post("/certificates/issue", response_model=CBTCertificateResponse)
async def issue_candidate_cbt_certificate(
    payload: CBTCertificateIssueRequest,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user),
) -> CBTCertificateResponse:
    """Issues an official HMAC-signed, QR-verifiable CBT certificate via ERP Module 13."""
    cert_service = CBTCertificateService(db)
    issuer_id = getattr(user, "id", uuid.uuid4())
    return await cert_service.issue_candidate_certificate(payload, issuer_id)


@cbt_router.post("/certificates/batch-issue", response_model=List[CBTCertificateResponse])
async def batch_issue_session_cbt_certificates(
    payload: CBTCertificateBatchIssueRequest,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user),
) -> List[CBTCertificateResponse]:
    """Batch issues certificates for all qualified candidates in a CBT examination session."""
    cert_service = CBTCertificateService(db)
    issuer_id = getattr(user, "id", uuid.uuid4())
    return await cert_service.batch_issue_session_certificates(payload, issuer_id)


@cbt_router.get("/certificates/session/{cbt_session_id}", response_model=List[CBTCertificateResponse])
async def list_session_issued_certificates(
    cbt_session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[CBTCertificateResponse]:
    """Lists all issued certificates for a CBT examination session."""
    cert_service = CBTCertificateService(db)
    return await cert_service.list_session_certificates(cbt_session_id)


@cbt_router.post("/certificates/{certificate_id}/dispatch-email", response_model=CBTCertificateResponse)
async def dispatch_certificate_by_email(
    certificate_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user),
) -> CBTCertificateResponse:
    """Emails official certificate to candidate via Module 7 Notification Center."""
    cert_service = CBTCertificateService(db)
    sender_id = getattr(user, "id", uuid.uuid4())
    return await cert_service.dispatch_certificate_email(certificate_id, sender_id)


@cbt_router.get("/certificates/verify/{verification_code}", response_model=CBTPublicVerificationLookupResponse)
async def public_verify_cbt_certificate(
    verification_code: str,
    db: AsyncSession = Depends(get_db_session),
) -> CBTPublicVerificationLookupResponse:
    """Validates certificate against ERP Module 13 verification ledger with HMAC check."""
    cert_service = CBTCertificateService(db)
    return await cert_service.public_verify_certificate(verification_code)


# ------------------- Phase 3 Module 12: Candidate Portal Endpoints -------------------
@cbt_router.get("/portal/dashboard", response_model=CandidatePortalDashboardResponse)
async def get_candidate_portal_dashboard(
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user),
) -> CandidatePortalDashboardResponse:
    """Unified candidate portal feed: upcoming shifts, hall tickets, scores, certificates, and tickets."""
    user_id = getattr(user, "id", uuid.uuid4())
    portal_service = CBTCandidatePortalService(db)
    return await portal_service.get_candidate_portal_dashboard(user_id)


@cbt_router.get("/portal/schedules", response_model=List[CandidatePortalScheduleCard])
async def list_candidate_portal_schedules(
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user),
) -> List[CandidatePortalScheduleCard]:
    """Lists candidate's enrolled examination shifts with admit card readiness."""
    user_id = getattr(user, "id", uuid.uuid4())
    portal_service = CBTCandidatePortalService(db)
    return await portal_service.list_candidate_schedules(user_id)


@cbt_router.post("/portal/tickets", response_model=CandidateTicketResponse)
async def raise_candidate_support_ticket(
    payload: CandidateTicketCreateRequest,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user),
) -> CandidateTicketResponse:
    """Files a candidate helpdesk ticket regarding exam day logistics or re-evaluations."""
    user_id = getattr(user, "id", uuid.uuid4())
    portal_service = CBTCandidatePortalService(db)
    return await portal_service.create_support_ticket(user_id, payload)


@cbt_router.get("/portal/tickets", response_model=List[CandidateTicketResponse])
async def list_candidate_support_tickets(
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user),
) -> List[CandidateTicketResponse]:
    """Lists candidate's filed support tickets in reverse chronological order."""
    user_id = getattr(user, "id", uuid.uuid4())
    portal_service = CBTCandidatePortalService(db)
    return await portal_service.list_candidate_tickets(user_id)


# ------------------- Phase 3 Module 13: Mock Test Platform Endpoints -------------------
@cbt_router.get("/mock/series", response_model=List[MockTestSeriesResponse])
async def list_available_mock_series(
    db: AsyncSession = Depends(get_db_session),
) -> List[MockTestSeriesResponse]:
    """Public endpoint: lists active free and institutional CBT mock test series."""
    mock_service = CBTMockTestService(db)
    return await mock_service.list_mock_series()


@cbt_router.post("/mock/register", response_model=Dict[str, Any])
async def register_public_mock_aspirant(
    payload: MockTestRegisterRequest,
    db: AsyncSession = Depends(get_db_session),
) -> Dict[str, Any]:
    """Public endpoint: registers external applicant for free mock entrance examination series."""
    mock_service = CBTMockTestService(db)
    return await mock_service.register_public_aspirant(payload)


@cbt_router.get("/mock/leaderboard/{series_id}", response_model=PublicLeaderboardResponse)
async def get_public_mock_leaderboard(
    series_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
) -> PublicLeaderboardResponse:
    """Public endpoint: streams top national rankers and percentiles on public leaderboard."""
    mock_service = CBTMockTestService(db)
    return await mock_service.get_public_leaderboard(series_id)


@cbt_router.get("/mock/practice/subjects", response_model=List[PracticeSubjectCategoryResponse])
async def list_subject_chapter_practice_drills(
    db: AsyncSession = Depends(get_db_session),
) -> List[PracticeSubjectCategoryResponse]:
    """Public practice hub: chapter-wise and topic-wise self-assessment drills."""
    mock_service = CBTMockTestService(db)
    return await mock_service.list_subject_chapter_practice()


@cbt_router.get("/mock/candidate/history", response_model=List[MockAttemptResponse])
async def get_candidate_mock_attempt_history(
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user),
) -> List[MockAttemptResponse]:
    """Authenticated endpoint: lists candidate's past mock attempts and progress milestones."""
    student_id = getattr(user, "id", uuid.uuid4())
    mock_service = CBTMockTestService(db)
    return await mock_service.get_candidate_mock_history(student_id)


# ------------------- Phase 3 Module 14: CBT Administration Endpoints -------------------
@cbt_router.get("/admin/centers/capacity", response_model=CapacityPlanningMatrixResponse)
async def get_center_capacity_planning_matrix(
    center_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> CapacityPlanningMatrixResponse:
    """Calculates physical capacity, 10% reserve buffer, and shift capacity matrix."""
    cid = center_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-exam-center")
    admin_service = CBTAdministrationService(db)
    return await admin_service.get_center_capacity_planning(cid)


@cbt_router.get("/admin/terminals/health", response_model=List[CBTDeviceHealthResponse])
async def list_terminals_device_health_telemetry(
    lab_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[CBTDeviceHealthResponse]:
    """Streams workstation hardware telemetry: CPU, RAM, ping, and kiosk lock status."""
    admin_service = CBTAdministrationService(db)
    return await admin_service.list_terminal_device_health(lab_id)


@cbt_router.post("/admin/diagnostics/run", response_model=SystemDiagnosticResponse)
async def run_preflight_system_diagnostics(
    payload: SystemDiagnosticRequest,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user),
) -> SystemDiagnosticResponse:
    """Runs comprehensive pre-flight test: LAN bandwidth, NTP drift, and WebRTC STUN."""
    user_id = getattr(user, "id", uuid.uuid4())
    admin_service = CBTAdministrationService(db)
    return await admin_service.execute_system_diagnostics(payload, user_id)


@cbt_router.post("/admin/incidents", response_model=CBTIncidentResponse)
async def create_administrative_incident(
    payload: CBTIncidentCreateRequest,
    db: AsyncSession = Depends(get_db_session),
    user: Any = Depends(get_current_user),
) -> CBTIncidentResponse:
    """Reports hardware failure, network outage, or invigilator incident during test shifts."""
    user_id = getattr(user, "id", uuid.uuid4())
    admin_service = CBTAdministrationService(db)
    return await admin_service.create_incident(payload, user_id)


@cbt_router.get("/admin/incidents", response_model=List[CBTIncidentResponse])
async def list_administrative_incidents(
    center_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[CBTIncidentResponse]:
    """Lists administrative incidents in reverse chronological order."""
    admin_service = CBTAdministrationService(db)
    return await admin_service.list_incidents(center_id)


# ------------------- Phase 3 Module 15: Reports & Monitoring Endpoints -------------------
@cbt_router.get("/reports/attendance", response_model=AttendanceSummaryResponse)
async def get_cbt_attendance_report(
    session_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> AttendanceSummaryResponse:
    """Generates attendance, absentees, and biometric reporting compliance report."""
    sid = session_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-session")
    service = CBTComprehensiveReportsService(db)
    return await service.get_attendance_report(sid)


@cbt_router.get("/reports/invigilators", response_model=List[InvigilatorDutyReportItem])
async def get_cbt_invigilators_duty_report(
    session_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[InvigilatorDutyReportItem]:
    """Lists assigned proctors, chief superintendents, and lab duty allocations."""
    service = CBTComprehensiveReportsService(db)
    return await service.get_invigilator_duty_report(session_id)


@cbt_router.get("/reports/question-audit", response_model=List[QuestionAuditItemResponse])
async def get_cbt_question_audit_report(
    session_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> List[QuestionAuditItemResponse]:
    """Provides psychometric Item Response Theory (IRT) diagnostics per question."""
    sid = session_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-session")
    service = CBTComprehensiveReportsService(db)
    return await service.get_question_audit_report(sid)


@cbt_router.get("/reports/system-telemetry", response_model=SystemTelemetryReportResponse)
async def get_cbt_system_telemetry_report(
    session_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> SystemTelemetryReportResponse:
    """Aggregates center hardware concurrency and network backbone performance."""
    sid = session_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-session")
    service = CBTComprehensiveReportsService(db)
    return await service.get_system_telemetry_report(sid)


@cbt_router.get("/reports/security-audit", response_model=SecurityAuditSummaryResponse)
async def get_cbt_security_audit_report(
    session_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> SecurityAuditSummaryResponse:
    """Returns security violations, proctor warnings, and auto-disqualification audit logs."""
    sid = session_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-session")
    service = CBTComprehensiveReportsService(db)
    return await service.get_security_audit_report(sid)


@cbt_router.get("/reports/comprehensive-bundle", response_model=CBTComprehensiveReportBundleResponse)
async def get_cbt_comprehensive_report_bundle(
    session_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> CBTComprehensiveReportBundleResponse:
    """Constructs unified multi-dimensional audit bundle for executive oversight."""
    sid = session_id or uuid.uuid5(uuid.NAMESPACE_DNS, "default-session")
    service = CBTComprehensiveReportsService(db)
    return await service.get_comprehensive_report_bundle(sid)


# ------------------- Phase 3 Module 16: Enterprise Integrations Endpoints -------------------
@cbt_router.get("/integrations/topology", response_model=IntegrationTopologyResponse)
async def get_enterprise_cbt_integration_topology(
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> IntegrationTopologyResponse:
    """Returns real-time connectivity matrix and health status across all 9 centralized services."""
    service = CBTEnterpriseIntegrationService(db)
    return await service.get_integration_topology()


@cbt_router.post("/integrations/lms/sync", response_model=LMSSyncAssessmentResponse)
async def sync_cbt_assessment_to_lms(
    payload: LMSSyncAssessmentRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> LMSSyncAssessmentResponse:
    """Maps candidate CBT assessment scores to Module 15 LXP learning competencies."""
    service = CBTEnterpriseIntegrationService(db)
    return await service.sync_lms_assessments(payload)


@cbt_router.post("/integrations/test-probe", response_model=WebhookDispatchTestResponse)
async def test_integration_webhook_probe(
    payload: WebhookDispatchTestRequest,
    db: AsyncSession = Depends(get_db_session),
    _user: Any = Depends(get_current_user),
) -> WebhookDispatchTestResponse:
    """Dispatches test probe event to verify connectivity with centralized ERP services."""
    service = CBTEnterpriseIntegrationService(db)
    return await service.test_webhook_dispatch(payload)
