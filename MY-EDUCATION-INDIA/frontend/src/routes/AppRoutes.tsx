import React from "react";
import { Link, Routes, Route, Navigate, Outlet } from "react-router-dom";
import { PublicWebsiteLayout } from "@/layouts/PublicWebsiteLayout";
import { PublicHomePage } from "@/pages/PublicHomePage";
import { PublicAboutPage } from "@/pages/PublicAboutPage";
import { PublicCoursesPage } from "@/pages/PublicCoursesPage";
import { PublicCourseDetailPage } from "@/pages/PublicCourseDetailPage";
import { PublicAdmissionsPage } from "@/pages/PublicAdmissionsPage";
import { PublicFacultyPage } from "@/pages/PublicFacultyPage";
import { PublicFacultyProfilePage } from "@/pages/PublicFacultyProfilePage";
import { PublicStaffPage } from "@/pages/PublicStaffPage";
import { PublicPlacementsPage } from "@/pages/PublicPlacementsPage";
import { PublicRecruitersPage } from "@/pages/PublicRecruitersPage";
import { PublicSuccessStoriesPage } from "@/pages/PublicSuccessStoriesPage";
import { PublicPlacementDrivesPage } from "@/pages/PublicPlacementDrivesPage";
import { PublicPlacementTrainingPage } from "@/pages/PublicPlacementTrainingPage";
import { PublicPlacementInternshipsPage } from "@/pages/PublicPlacementInternshipsPage";
import { PublicEventsPage } from "@/pages/PublicEventsPage";
import { PublicNewsNoticesPage } from "@/pages/PublicNewsNoticesPage";
import { PublicGalleryPage } from "@/pages/PublicGalleryPage";
import { PublicDownloadsPage } from "@/pages/PublicDownloadsPage";
import { PublicTestimonialsPage } from "@/pages/PublicTestimonialsPage";
import { PublicContactPage } from "@/pages/PublicContactPage";
import { PublicSearchPage } from "@/pages/PublicSearchPage";
import { PublicSitemapPage } from "@/pages/PublicSitemapPage";
import { LoginPage } from "@/pages/auth/LoginPage";
import { SuperAdminLayout } from "@/layouts/SuperAdminLayout";
import { DashboardOverviewPage } from "@/pages/admin/DashboardOverviewPage";
import { SuperAdminDashboardPage } from "@/pages/admin/SuperAdminDashboardPage";
import { InstituteSetupPage } from "@/pages/admin/InstituteSetupPage";
import { DepartmentsManagementPage } from "@/pages/admin/DepartmentsManagementPage";
import { NotificationCenterPage } from "@/pages/admin/NotificationCenterPage";
import { MediaFileManagerPage } from "@/pages/admin/MediaFileManagerPage";
import { WorkflowEnginePage } from "@/pages/admin/WorkflowEnginePage";
import { ReportsEnginePage } from "@/pages/admin/ReportsEnginePage";
import { RolesPermissionsPage } from "@/pages/admin/RolesPermissionsPage";
import { UsersManagementPage } from "@/pages/admin/UsersManagementPage";
import { AuditLogsPage } from "@/pages/admin/AuditLogsPage";
import { WebsiteManagementPage } from "@/pages/admin/WebsiteManagementPage";
import { IntegrationsManagementPage } from "@/pages/admin/IntegrationsManagementPage";
import { CrmMarketingFranchisePage } from "@/pages/admin/CrmMarketingFranchisePage";
import { BiAnalyticsExecutiveReportsPage } from "@/pages/admin/BiAnalyticsExecutiveReportsPage";
import { PlatformDevOpsManagementPage } from "@/pages/admin/PlatformDevOpsManagementPage";
import { EnterpriseExperiencePortalPage } from "@/pages/admin/EnterpriseExperiencePortalPage";
import { ActiveSessionsPage } from "@/pages/admin/ActiveSessionsPage";
import { LoginHistoryAuditPage } from "@/pages/admin/LoginHistoryAuditPage";
import { SecurityPoliciesPage } from "@/pages/admin/SecurityPoliciesPage";
import { StudentsManagementPage } from "@/pages/admin/StudentsManagementPage";
import { AdmissionsPipelinePage } from "@/pages/admin/AdmissionsPipelinePage";
import { AcademicsManagementPage } from "@/pages/admin/AcademicsManagementPage";
import { SystemSettingsManagerPage } from "@/pages/admin/SystemSettingsManagerPage";
import { CertificateDashboardPage } from "@/modules/certificates/dashboard/CertificateDashboardPage";
import { CertificateTemplatesPage } from "@/modules/certificates/templates/CertificateTemplatesPage";
import { VisualCertificateDesignerPage } from "@/modules/certificates/designer/VisualCertificateDesignerPage";
import { BulkDocumentGeneratorPage } from "@/modules/certificates/generator/BulkDocumentGeneratorPage";
import { IDCardGeneratorPage } from "@/modules/certificates/idcards/IDCardGeneratorPage";
import { CertificateReportsPage } from "@/modules/certificates/reports/CertificateReportsPage";
import { CertificateAnalyticsPage } from "@/modules/certificates/analytics/CertificateAnalyticsPage";
import { CertificateSettingsPage } from "@/modules/certificates/settings/CertificateSettingsPage";
import { PublicVerificationPortalPage } from "@/modules/certificates/verification/PublicVerificationPortalPage";
import { LibraryDashboardPage } from "@/modules/library/dashboard/LibraryDashboardPage";
import { BookCatalogPage } from "@/modules/library/catalog/BookCatalogPage";
import { BookCopiesAccessionPage } from "@/modules/library/copies/BookCopiesAccessionPage";
import { IssueReturnTerminalPage } from "@/modules/library/issues/IssueReturnTerminalPage";
import { BookReservationsPage } from "@/modules/library/reservations/BookReservationsPage";
import { LibraryMembersPage } from "@/modules/library/members/LibraryMembersPage";
import { DigitalKnowledgeRepoPage } from "@/modules/library/digital/DigitalKnowledgeRepoPage";
import { OPACPublicCatalogPage } from "@/modules/library/opac/OPACPublicCatalogPage";
import { LibraryReportsPage } from "@/modules/library/reports/LibraryReportsPage";
import { LibraryAnalyticsPage } from "@/modules/library/analytics/LibraryAnalyticsPage";
import { LibraryRulesSettingsPage } from "@/modules/library/settings/LibraryRulesSettingsPage";
import { LearningDashboardPage } from "@/modules/lxp/dashboard/LearningDashboardPage";
import { CoursesCatalogPage } from "@/modules/lxp/courses/CoursesCatalogPage";
import { CourseBuilderPage } from "@/modules/lxp/course-builder/CourseBuilderPage";
import { CourseModulesPage } from "@/modules/lxp/modules/CourseModulesPage";
import { LessonViewerPage } from "@/modules/lxp/lessons/LessonViewerPage";
import { VideoLibraryPage } from "@/modules/lxp/videos/VideoLibraryPage";
import { AssignmentsHubPage } from "@/modules/lxp/assignments/AssignmentsHubPage";
import { PracticeTestsHubPage } from "@/modules/lxp/practice/PracticeTestsHubPage";
import { DiscussionForumPage } from "@/modules/lxp/forum/DiscussionForumPage";
import { StudentProgressPage } from "@/modules/lxp/progress/StudentProgressPage";
import { LXPAnalyticsPage } from "@/modules/lxp/analytics/LXPAnalyticsPage";
import { LXPReportsPage } from "@/modules/lxp/reports/LXPReportsPage";
import { LXPSettingsPage } from "@/modules/lxp/settings/LXPSettingsPage";
import { ApiDashboardPage } from "@/modules/integrations/dashboard/ApiDashboardPage";
import { ProviderDirectoryPage } from "@/modules/integrations/providers/ProviderDirectoryPage";
import { CredentialVaultPage } from "@/modules/integrations/vault/CredentialVaultPage";
import { WebhooksManagerPage } from "@/modules/integrations/webhooks/WebhooksManagerPage";
import { ConnectionTestTerminalPage } from "@/modules/integrations/tester/ConnectionTestTerminalPage";
import { ApiExecutionLogsPage } from "@/modules/integrations/logs/ApiExecutionLogsPage";
import { ApiAnalyticsPage } from "@/modules/integrations/analytics/ApiAnalyticsPage";
import { CrmDashboardPage } from "@/modules/crm/dashboard/CrmDashboardPage";
import { SalesPipelineKanbanPage } from "@/modules/crm/pipeline/SalesPipelineKanbanPage";
import { LeadsDirectoryPage } from "@/modules/crm/leads/LeadsDirectoryPage";
import { EnquiriesInboxPage } from "@/modules/crm/enquiries/EnquiriesInboxPage";
import { FollowupCalendarPage } from "@/modules/crm/followups/FollowupCalendarPage";
import { MarketingCampaignsPage } from "@/modules/crm/campaigns/MarketingCampaignsPage";
import { FranchiseManagementPage } from "@/modules/crm/franchise/FranchiseManagementPage";
import { ReferralProgramsPage } from "@/modules/crm/referrals/ReferralProgramsPage";
import { CrmTasksPage } from "@/modules/crm/tasks/CrmTasksPage";
import { CrmReportsPage } from "@/modules/crm/reports/CrmReportsPage";
import { CrmAnalyticsPage } from "@/modules/crm/analytics/CrmAnalyticsPage";
import { CrmSettingsPage } from "@/modules/crm/settings/CrmSettingsPage";
import { ExecutiveDashboardPage } from "@/modules/bi/dashboard/ExecutiveDashboardPage";
import { ReportBuilderPage } from "@/modules/bi/report-builder/ReportBuilderPage";
import { ReportsDirectoryPage } from "@/modules/bi/reports/ReportsDirectoryPage";
import { ChartStudioPage } from "@/modules/bi/charts/ChartStudioPage";
import { KpiManagementPage } from "@/modules/bi/kpis/KpiManagementPage";
import { CrossModuleAnalyticsPage } from "@/modules/bi/analytics/CrossModuleAnalyticsPage";
import { ExportCenterPage } from "@/modules/bi/exports/ExportCenterPage";
import { AuditReportsPage } from "@/modules/bi/audit/AuditReportsPage";
import { DashboardWidgetsPage } from "@/modules/bi/widgets/DashboardWidgetsPage";
import { SystemHealthDashboardPage } from "@/modules/bi/system-health/SystemHealthDashboardPage";
import { BiSettingsPage } from "@/modules/bi/settings/BiSettingsPage";
import { PlatformDashboardPage } from "@/modules/platform/dashboard/PlatformDashboardPage";
import { BackupManagerPage } from "@/modules/platform/backups/BackupManagerPage";
import { RestoreManagerPage } from "@/modules/platform/restores/RestoreManagerPage";
import { ClusterHealthPage } from "@/modules/platform/health/ClusterHealthPage";
import { SecurityCenterPage } from "@/modules/platform/security/SecurityCenterPage";
import { FeatureFlagsPage } from "@/modules/platform/feature-flags/FeatureFlagsPage";
import { MaintenanceModePage } from "@/modules/platform/maintenance/MaintenanceModePage";
import { StorageManagerPage } from "@/modules/platform/storage/StorageManagerPage";
import { LicenseManagerPage } from "@/modules/platform/licenses/LicenseManagerPage";
import { ThemeBrandingPage } from "@/modules/platform/theme/ThemeBrandingPage";
import { DeveloperConsolePage } from "@/modules/platform/developer/DeveloperConsolePage";
import { AuditCenterPage } from "@/modules/platform/audit/AuditCenterPage";
import { SupportCenterPage } from "@/modules/platform/support/SupportCenterPage";
import { PlatformReportsPage } from "@/modules/platform/reports/PlatformReportsPage";
import { RootOwnerConsolePage } from "@/modules/platform/root-owner/RootOwnerConsolePage";
import { FeatureControlStudioPage } from "@/modules/root/FeatureControlStudioPage";
import { SuperAdminControlCenterPage } from "@/modules/platform/super-admin/SuperAdminControlCenterPage";
import { PortalSelectorPage } from "@/modules/platform/portal/PortalSelectorPage";
import { StudentPortalPage } from "@/modules/platform/portal/StudentPortalPage";
import { FacultyPortalPage } from "@/modules/platform/portal/FacultyPortalPage";
import { GlobalSearchPage } from "@/modules/platform/search/GlobalSearchPage";
import { VisualFormBuilderPage } from "@/modules/platform/form-builder/VisualFormBuilderPage";
import { MenuBuilderPage } from "@/modules/platform/menu-builder/MenuBuilderPage";
import { DashboardBuilderPage } from "@/modules/platform/dashboard-builder/DashboardBuilderPage";
import { CBTDashboardPage } from "@/modules/cbt/dashboard/CBTDashboardPage";
import { CBTFoundationSettingsPage } from "@/modules/cbt/foundation/CBTFoundationSettingsPage";
import { CBTSecuritySettingsPage } from "@/modules/cbt/settings/CBTSecuritySettingsPage";
import { CBTReportsPage } from "@/modules/cbt/reports/CBTReportsPage";
import { QuestionBankManagerPage } from "@/modules/cbt/question-bank/QuestionBankManagerPage";
import { QuestionWorkflowReviewPage } from "@/modules/cbt/workflow/QuestionWorkflowReviewPage";
import { TestBuilderStudioPage } from "@/modules/cbt/test-builder/TestBuilderStudioPage";
import { CandidateManagementPage } from "@/modules/cbt/candidates/CandidateManagementPage";
import { ExamSchedulingCalendarPage } from "@/modules/cbt/scheduling/ExamSchedulingCalendarPage";
import { CandidateExamInterfacePage } from "@/modules/cbt/candidate/CandidateExamInterfacePage";
import { LiveProctorMonitorPage } from "@/modules/cbt/live-monitor/LiveProctorMonitorPage";
import { EvaluationModerationStudioPage } from "@/modules/cbt/evaluation/EvaluationModerationStudioPage";
import { CBTResultsAnalyticsDashboardPage } from "@/modules/cbt/analytics/CBTResultsAnalyticsDashboardPage";
import { CBTCertificateStudioPage } from "@/modules/cbt/certificates/CBTCertificateStudioPage";
import { CBTCandidatePortalPage } from "@/modules/cbt/portal/CBTCandidatePortalPage";
import { CBTMockTestPlatformPage } from "@/modules/cbt/mock-tests/CBTMockTestPlatformPage";
import { CBTAdministrationCommandPage } from "@/modules/cbt/administration/CBTAdministrationCommandPage";
import { CBTEnterpriseIntegrationHubPage } from "@/modules/cbt/integrations/CBTEnterpriseIntegrationHubPage";
import { ExamDashboardPage } from "@/modules/examinations/dashboard/ExamDashboardPage";
import { AcademicExamStructureStudioPage } from "@/modules/examinations/structure/AcademicExamStructureStudioPage";
import { ExamPlanningStudioPage } from "@/modules/examinations/planning/ExamPlanningStudioPage";
import { TimetableGeneratorStudioPage } from "@/modules/examinations/timetable/TimetableGeneratorStudioPage";
import { HallTicketStudioPage } from "@/modules/examinations/halltickets/HallTicketStudioPage";
import { SeatingManagementStudioPage } from "@/modules/examinations/seating/SeatingManagementStudioPage";
import { InvigilatorManagementStudioPage } from "@/modules/examinations/invigilators/InvigilatorManagementStudioPage";
import { PracticalVivaStudioPage } from "@/modules/examinations/practical/PracticalVivaStudioPage";
import { ExamAttendanceStudioPage } from "@/modules/examinations/attendance/ExamAttendanceStudioPage";
import { EvaluationManagementStudioPage } from "@/modules/examinations/evaluation/EvaluationManagementStudioPage";
import { MarksEntryStudioPage } from "@/modules/examinations/marks/MarksEntryStudioPage";
import { ResultProcessingStudioPage } from "@/modules/examinations/results/ResultProcessingStudioPage";
import { RevaluationSupplementaryStudioPage } from "@/modules/examinations/revaluation/RevaluationSupplementaryStudioPage";
import { TranscriptsCertificatesStudioPage } from "@/modules/examinations/certificates/TranscriptsCertificatesStudioPage";
import { ComplianceReportsStudioPage } from "@/modules/examinations/compliance/ComplianceReportsStudioPage";
import { ExamAnalyticsStudioPage } from "@/modules/examinations/analytics/ExamAnalyticsStudioPage";
import { StudentExaminationPortalPage } from "@/modules/examinations/student/StudentExaminationPortalPage";
import { FacultyExaminationPortalPage } from "@/modules/examinations/faculty/FacultyExaminationPortalPage";
import { CoeMasterPortalPage } from "@/modules/examinations/coe/CoeMasterPortalPage";
import { EnterpriseIntegrationStudioPage } from "@/modules/examinations/system/EnterpriseIntegrationStudioPage";
import { LmsDashboardPage } from "@/modules/lms/dashboard/LmsDashboardPage";
import { CourseManagementStudioPage } from "@/modules/lms/courses/CourseManagementStudioPage";
import { LessonBuilderStudioPage } from "@/modules/lms/lessons/LessonBuilderStudioPage";
import { VideoLearningStudioPage } from "@/modules/lms/video/VideoLearningStudioPage";
import { LiveClassesStudioPage } from "@/modules/lms/live/LiveClassesStudioPage";
import { AssignmentManagementStudioPage } from "@/modules/lms/assignments/AssignmentManagementStudioPage";
import { QuizPracticeStudioPage } from "@/modules/lms/quizzes/QuizPracticeStudioPage";
import { DiscussionCollaborationStudioPage } from "@/modules/lms/discussions/DiscussionCollaborationStudioPage";
import { AttendanceEngagementStudioPage } from "@/modules/lms/attendance/AttendanceEngagementStudioPage";
import { ProgressAnalyticsStudioPage } from "@/modules/lms/analytics/ProgressAnalyticsStudioPage";
import { DigitalLibraryStudioPage } from "@/modules/lms/library/DigitalLibraryStudioPage";
import { CertificatesCredentialsStudioPage } from "@/modules/lms/certificates/CertificatesCredentialsStudioPage";
import { ParentPortalStudioPage } from "@/modules/lms/parents/ParentPortalStudioPage";
import { FacultyPortalStudioPage } from "@/modules/lms/faculty/FacultyPortalStudioPage";
import { StudentPortalStudioPage } from "@/modules/lms/student/StudentPortalStudioPage";
import { AiLearningAssistantStudioPage } from "@/modules/lms/ai/AiLearningAssistantStudioPage";
import { MobileLearningStudioPage } from "@/modules/lms/mobile/MobileLearningStudioPage";
import { AnalyticsReportsStudioPage } from "@/modules/lms/reports/AnalyticsReportsStudioPage";
import { EnterpriseIntegrationsStudioPage } from "@/modules/lms/integrations/EnterpriseIntegrationsStudioPage";
import { ProductionReadinessStudioPage } from "@/modules/lms/readiness/ProductionReadinessStudioPage";
import { useAuthSession } from "@/hooks/useAuthSession";
import {
  FileBadge,
  MonitorPlay,
  Award,
  CalendarCheck,
  IndianRupee,
  BookOpen,
  ClipboardList,
  GraduationCap,
  Globe,
  Sliders,
  MessageSquare,
  MonitorSmartphone,
  History,
  CheckCircle2,
  Clock,
} from "lucide-react";

interface SubsystemViewProps {
  title: string;
  category: string;
  description: string;
  icon: React.ComponentType<{ className?: string }>;
  features: string[];
  subdomain: string;
  status: "ACTIVE" | "CORE_LOCKED" | "ENTERPRISE";
}

const SubsystemView: React.FC<SubsystemViewProps> = ({
  title,
  category,
  description,
  icon: Icon,
  features,
  subdomain,
  status,
}) => {
  return (
    <div className="space-y-6">
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-50 text-brand-600">
              <Icon className="h-6 w-6" />
            </div>
            <div>
              <div className="flex items-center gap-2.5">
                <h1 className="text-xl font-bold text-slate-900">{title}</h1>
                <span className="rounded-full bg-emerald-100 px-2.5 py-0.5 text-[11px] font-semibold text-emerald-800">
                  {status}
                </span>
              </div>
              <p className="mt-0.5 text-xs text-slate-500">
                Category: <span className="font-semibold text-slate-700">{category}</span> • Subdomain:{" "}
                <code className="rounded-sm bg-slate-100 px-1.5 py-0.5 text-brand-600">{subdomain}.myeducation.in</code>
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Link
              to="/admin/modules"
              className="rounded-lg border border-slate-200 bg-white px-3.5 py-2 text-xs font-semibold text-slate-700 shadow-2xs hover:bg-slate-50"
            >
              Configure in Module Matrix
            </Link>
          </div>
        </div>
        <p className="mt-4 text-sm text-slate-600 border-t border-slate-100 pt-4">{description}</p>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-6">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-base font-bold text-slate-900 mb-4">Core Operational Workflows</h2>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
              {features.map((feat, idx) => (
                <div key={idx} className="flex items-start gap-3 rounded-xl border border-slate-100 bg-slate-50/50 p-3.5">
                  <CheckCircle2 className="h-5 w-5 text-emerald-600 shrink-0 mt-0.5" />
                  <span className="text-xs font-medium text-slate-700 leading-relaxed">{feat}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-base font-bold text-slate-900 mb-2">Live PostgreSQL Data Pipeline</h2>
            <p className="text-xs text-slate-500 mb-4">
              Real-time synchronization with Neon PostgreSQL Serverless backend.
            </p>
            <div className="rounded-xl border border-dashed border-slate-200 bg-slate-50/50 p-8 text-center">
              <Clock className="h-8 w-8 text-slate-400 mx-auto mb-2 animate-pulse" />
              <p className="text-sm font-semibold text-slate-700">Subsystem Online & Governed</p>
              <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
                All records, audit logs, and access control policies for this subsystem are actively managed by the
                governance matrix.
              </p>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
            <h3 className="text-sm font-bold text-slate-900 mb-3">Subsystem Architecture</h3>
            <dl className="space-y-3 text-xs">
              <div className="flex justify-between border-b border-slate-100 pb-2">
                <dt className="text-slate-500">Security Model</dt>
                <dd className="font-semibold text-slate-800">RBAC Token Matrix</dd>
              </div>
              <div className="flex justify-between border-b border-slate-100 pb-2">
                <dt className="text-slate-500">Database Engine</dt>
                <dd className="font-semibold text-slate-800">Neon PostgreSQL 16</dd>
              </div>
              <div className="flex justify-between border-b border-slate-100 pb-2">
                <dt className="text-slate-500">Isolation Layer</dt>
                <dd className="font-semibold text-slate-800">Tenant Isolation</dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-slate-500">Audit Trail</dt>
                <dd className="font-semibold text-emerald-600">Active (Encrypted)</dd>
              </div>
            </dl>
          </div>
        </div>
      </div>
    </div>
  );
};

const ProtectedRoute: React.FC = () => {
  const { isAuthenticated, isInitializing } = useAuthSession();

  if (isInitializing) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50">
        <div className="flex flex-col items-center gap-3">
          <div className="h-10 w-10 animate-spin rounded-full border-4 border-brand-600 border-t-transparent" />
          <p className="text-sm font-medium text-slate-600">Verifying secure session...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
};

export const AppRoutes: React.FC = () => {
  return (
    <Routes>
      {/* 1. Public Facing Institute Website Layout with Sticky Header, Sticky Ticker & Footer */}
      <Route element={<PublicWebsiteLayout />}>
        <Route path="/" element={<PublicHomePage />} />
        <Route path="/about" element={<PublicAboutPage />} />
        <Route path="/about/vision-mission" element={<PublicAboutPage />} />
        <Route path="/about/directors-message" element={<PublicAboutPage />} />
        <Route path="/about/accreditations" element={<PublicAboutPage />} />
        <Route path="/about/infrastructure" element={<PublicAboutPage />} />
        <Route path="/courses" element={<PublicCoursesPage />} />
        <Route path="/courses/:slug" element={<PublicCourseDetailPage />} />
        <Route path="/admissions" element={<PublicAdmissionsPage />} />
        <Route path="/admissions/process" element={<PublicAdmissionsPage />} />
        <Route path="/admissions/eligibility" element={<PublicAdmissionsPage />} />
        <Route path="/admissions/fees" element={<PublicAdmissionsPage />} />
        <Route path="/admissions/apply" element={<PublicAdmissionsPage />} />
        <Route path="/admissions/scholarships" element={<PublicAdmissionsPage />} />
        <Route path="/admissions/track" element={<PublicAdmissionsPage />} />
        <Route path="/faculty" element={<PublicFacultyPage />} />
        <Route path="/faculty/:slug" element={<PublicFacultyProfilePage />} />
        <Route path="/staff" element={<PublicStaffPage />} />
        <Route path="/placements" element={<PublicPlacementsPage />} />
        <Route path="/placements/recruiters" element={<PublicRecruitersPage />} />
        <Route path="/placements/success-stories" element={<PublicSuccessStoriesPage />} />
        <Route path="/placements/drives" element={<PublicPlacementDrivesPage />} />
        <Route path="/placements/training" element={<PublicPlacementTrainingPage />} />
        <Route path="/placements/internships" element={<PublicPlacementInternshipsPage />} />
        <Route path="/events" element={<PublicEventsPage />} />
        <Route path="/news" element={<PublicNewsNoticesPage />} />
        <Route path="/notices" element={<PublicNewsNoticesPage />} />
        <Route path="/achievements" element={<PublicNewsNoticesPage />} />
        <Route path="/gallery" element={<PublicGalleryPage />} />
        <Route path="/gallery/:slug" element={<PublicGalleryPage />} />
        <Route path="/downloads" element={<PublicDownloadsPage />} />
        <Route path="/downloads/:categorySlug" element={<PublicDownloadsPage />} />
        <Route path="/testimonials" element={<PublicTestimonialsPage />} />
        <Route path="/verify" element={<PublicVerificationPortalPage />} />
        <Route path="/verify/:token" element={<PublicVerificationPortalPage />} />
        <Route path="/contact" element={<PublicContactPage />} />
        <Route path="/search" element={<PublicSearchPage />} />
        <Route path="/sitemap" element={<PublicSitemapPage />} />
      </Route>

      {/* 2. Public Universal Authentication Route ('/login') */}
      <Route path="/login" element={<LoginPage />} />

      {/* 3. Protected Enterprise Command Center Routes ('/admin/*') */}
      <Route element={<ProtectedRoute />}>
        <Route path="/admin" element={<SuperAdminLayout />}>
          <Route index element={<Navigate to="dashboard" replace />} />
          <Route path="dashboard" element={<DashboardOverviewPage />} />
          <Route path="modules" element={<SuperAdminDashboardPage />} />

          {/* Website Management Center for Super Admin */}
          <Route path="cms/pages" element={<WebsiteManagementPage />} />
          <Route path="website" element={<WebsiteManagementPage />} />
          <Route path="media" element={<WebsiteManagementPage />} />
          <Route path="gallery" element={<WebsiteManagementPage />} />
          <Route path="downloads" element={<WebsiteManagementPage />} />
          <Route path="faculty" element={<WebsiteManagementPage />} />
          <Route path="staff" element={<WebsiteManagementPage />} />
          <Route path="placements" element={<WebsiteManagementPage />} />
          <Route path="testimonials" element={<WebsiteManagementPage />} />
          <Route path="contact" element={<WebsiteManagementPage />} />
          <Route path="inquiries" element={<WebsiteManagementPage />} />
          <Route path="navigation" element={<WebsiteManagementPage />} />
          <Route path="sitemap" element={<WebsiteManagementPage />} />
          <Route path="integrations" element={<IntegrationsManagementPage />} />
          <Route path="integrations/dashboard" element={<ApiDashboardPage />} />
          <Route path="integrations/providers" element={<ProviderDirectoryPage />} />
          <Route path="integrations/vault" element={<CredentialVaultPage />} />
          <Route path="integrations/webhooks" element={<WebhooksManagerPage />} />
          <Route path="integrations/tester" element={<ConnectionTestTerminalPage />} />
          <Route path="integrations/logs" element={<ApiExecutionLogsPage />} />
          <Route path="integrations/analytics" element={<ApiAnalyticsPage />} />
          <Route path="crm" element={<CrmMarketingFranchisePage />} />
          <Route path="crm/dashboard" element={<CrmDashboardPage />} />
          <Route path="crm/pipeline" element={<SalesPipelineKanbanPage />} />
          <Route path="crm/leads" element={<LeadsDirectoryPage />} />
          <Route path="crm/enquiries" element={<EnquiriesInboxPage />} />
          <Route path="crm/followups" element={<FollowupCalendarPage />} />
          <Route path="crm/campaigns" element={<MarketingCampaignsPage />} />
          <Route path="crm/franchise" element={<FranchiseManagementPage />} />
          <Route path="crm/referrals" element={<ReferralProgramsPage />} />
          <Route path="crm/tasks" element={<CrmTasksPage />} />
          <Route path="crm/reports" element={<CrmReportsPage />} />
          <Route path="crm/analytics" element={<CrmAnalyticsPage />} />
          <Route path="crm/settings" element={<CrmSettingsPage />} />
          <Route path="bi" element={<BiAnalyticsExecutiveReportsPage />} />
          <Route path="bi/executive" element={<ExecutiveDashboardPage />} />
          <Route path="bi/builder" element={<ReportBuilderPage />} />
          <Route path="bi/reports" element={<ReportsDirectoryPage />} />
          <Route path="bi/charts" element={<ChartStudioPage />} />
          <Route path="bi/kpis" element={<KpiManagementPage />} />
          <Route path="bi/analytics" element={<CrossModuleAnalyticsPage />} />
          <Route path="bi/exports" element={<ExportCenterPage />} />
          <Route path="bi/audit" element={<AuditReportsPage />} />
          <Route path="bi/widgets" element={<DashboardWidgetsPage />} />
          <Route path="bi/health" element={<SystemHealthDashboardPage />} />
          <Route path="bi/settings" element={<BiSettingsPage />} />
          <Route path="platform" element={<PlatformDevOpsManagementPage />} />
          <Route path="platform/dashboard" element={<PlatformDashboardPage />} />
          <Route path="platform/backups" element={<BackupManagerPage />} />
          <Route path="platform/restores" element={<RestoreManagerPage />} />
          <Route path="platform/health" element={<ClusterHealthPage />} />
          <Route path="platform/security" element={<SecurityCenterPage />} />
          <Route path="platform/feature-flags" element={<FeatureFlagsPage />} />
          <Route path="platform/maintenance" element={<MaintenanceModePage />} />
          <Route path="platform/storage" element={<StorageManagerPage />} />
          <Route path="platform/licenses" element={<LicenseManagerPage />} />
          <Route path="platform/theme" element={<ThemeBrandingPage />} />
          <Route path="platform/developer" element={<DeveloperConsolePage />} />
          <Route path="platform/audit" element={<AuditCenterPage />} />
          <Route path="platform/support" element={<SupportCenterPage />} />
          <Route path="platform/reports" element={<PlatformReportsPage />} />
          <Route path="experience" element={<EnterpriseExperiencePortalPage />} />
          <Route path="experience/root-owner" element={<RootOwnerConsolePage />} />
          <Route path="experience/feature-control" element={<FeatureControlStudioPage />} />
          <Route path="experience/security-management" element={<FeatureControlStudioPage />} />
          <Route path="root/feature-control" element={<FeatureControlStudioPage />} />
          <Route path="root/security-management" element={<FeatureControlStudioPage />} />
          <Route path="experience/super-admin" element={<SuperAdminControlCenterPage />} />
          <Route path="experience/portals" element={<PortalSelectorPage />} />
          <Route path="experience/student-portal" element={<StudentPortalPage />} />
          <Route path="experience/faculty-portal" element={<FacultyPortalPage />} />
          <Route path="experience/global-search" element={<GlobalSearchPage />} />
          <Route path="experience/form-builder" element={<VisualFormBuilderPage />} />
          <Route path="experience/menu-builder" element={<MenuBuilderPage />} />
          <Route path="experience/dashboard-builder" element={<DashboardBuilderPage />} />

          {/* Module 13: Enterprise Certificate, Document Generation & Digital Verification Subsystem */}
          <Route path="certificates" element={<CertificateDashboardPage />} />
          <Route path="certificates/templates" element={<CertificateTemplatesPage />} />
          <Route path="certificates/designer" element={<VisualCertificateDesignerPage />} />
          <Route path="certificates/generator" element={<BulkDocumentGeneratorPage />} />
          <Route path="certificates/id-cards" element={<IDCardGeneratorPage />} />
          <Route path="certificates/reports" element={<CertificateReportsPage />} />
          <Route path="certificates/analytics" element={<CertificateAnalyticsPage />} />
          <Route path="certificates/settings" element={<CertificateSettingsPage />} />

          {/* Module 14: Enterprise Library & Digital Knowledge Management Subsystem */}
          <Route path="library" element={<LibraryDashboardPage />} />
          <Route path="library/catalog" element={<BookCatalogPage />} />
          <Route path="library/copies" element={<BookCopiesAccessionPage />} />
          <Route path="library/circulation" element={<IssueReturnTerminalPage />} />
          <Route path="library/reservations" element={<BookReservationsPage />} />
          <Route path="library/members" element={<LibraryMembersPage />} />
          <Route path="library/digital" element={<DigitalKnowledgeRepoPage />} />
          <Route path="library/opac" element={<OPACPublicCatalogPage />} />
          <Route path="library/reports" element={<LibraryReportsPage />} />
          <Route path="library/analytics" element={<LibraryAnalyticsPage />} />
          <Route path="library/settings" element={<LibraryRulesSettingsPage />} />

          {/* Module 15: Enterprise Learning Experience Platform (LXP) Subsystem */}
          <Route path="lxp" element={<LearningDashboardPage />} />
          <Route path="lxp/courses" element={<CoursesCatalogPage />} />
          <Route path="lxp/builder" element={<CourseBuilderPage />} />
          <Route path="lxp/courses/:courseId/modules" element={<CourseModulesPage />} />
          <Route path="lxp/lessons/:lessonId" element={<LessonViewerPage />} />
          <Route path="lxp/videos" element={<VideoLibraryPage />} />
          <Route path="lxp/assignments" element={<AssignmentsHubPage />} />
          <Route path="lxp/practice" element={<PracticeTestsHubPage />} />
          <Route path="lxp/forum" element={<DiscussionForumPage />} />
          <Route path="lxp/progress" element={<StudentProgressPage />} />
          <Route path="lxp/analytics" element={<LXPAnalyticsPage />} />
          <Route path="lxp/reports" element={<LXPReportsPage />} />
          <Route path="lxp/settings" element={<LXPSettingsPage />} />

          {/* Phase 3: Enterprise Computer Based Testing (CBT) Subsystem */}
          <Route path="cbt" element={<CBTDashboardPage />} />
          <Route path="cbt/foundation" element={<CBTFoundationSettingsPage />} />
          <Route path="cbt/questions" element={<QuestionBankManagerPage />} />
          <Route path="cbt/question-bank" element={<QuestionBankManagerPage />} />
          <Route path="cbt/workflow" element={<QuestionWorkflowReviewPage />} />
          <Route path="cbt/builder" element={<TestBuilderStudioPage />} />
          <Route path="cbt/templates" element={<TestBuilderStudioPage />} />
          <Route path="cbt/candidates" element={<CandidateManagementPage />} />
          <Route path="cbt/scheduling" element={<ExamSchedulingCalendarPage />} />
          <Route path="cbt/shifts" element={<ExamSchedulingCalendarPage />} />
          <Route path="cbt/centers" element={<ExamSchedulingCalendarPage />} />
          <Route path="cbt/live" element={<CandidateExamInterfacePage />} />
          <Route path="cbt/candidate-demo" element={<CandidateExamInterfacePage />} />
          <Route path="cbt/exam/:sessionId" element={<CandidateExamInterfacePage />} />
          <Route path="cbt/proctoring" element={<LiveProctorMonitorPage />} />
          <Route path="cbt/monitor" element={<LiveProctorMonitorPage />} />
          <Route path="cbt/security-proctoring" element={<LiveProctorMonitorPage />} />
          <Route path="cbt/settings" element={<CBTSecuritySettingsPage />} />
          <Route path="cbt/reports" element={<CBTReportsPage />} />
          <Route path="cbt/reports-monitoring" element={<CBTReportsPage />} />
          <Route path="cbt/audit-reports" element={<CBTReportsPage />} />

          {/* Phase 4: Enterprise Examination Management System (EMS) */}
          <Route path="exams" element={<ExamDashboardPage />} />
          <Route path="exams/dashboard" element={<ExamDashboardPage />} />
          <Route path="ems" element={<ExamDashboardPage />} />
          <Route path="ems/dashboard" element={<ExamDashboardPage />} />
          <Route path="exams/structure" element={<AcademicExamStructureStudioPage />} />
          <Route path="exams/modalities" element={<AcademicExamStructureStudioPage />} />
          <Route path="ems/structure" element={<AcademicExamStructureStudioPage />} />
          <Route path="exams/planning" element={<ExamPlanningStudioPage />} />
          <Route path="exams/calendar" element={<ExamPlanningStudioPage />} />
          <Route path="exams/rooms" element={<ExamPlanningStudioPage />} />
          <Route path="ems/planning" element={<ExamPlanningStudioPage />} />
          <Route path="exams/timetable" element={<TimetableGeneratorStudioPage />} />
          <Route path="exams/schedules" element={<TimetableGeneratorStudioPage />} />
          <Route path="ems/timetable" element={<TimetableGeneratorStudioPage />} />
          <Route path="exams/hall-tickets" element={<HallTicketStudioPage />} />
          <Route path="exams/admit-cards" element={<HallTicketStudioPage />} />
          <Route path="ems/hall-tickets" element={<HallTicketStudioPage />} />
          <Route path="exams/seating" element={<SeatingManagementStudioPage />} />
          <Route path="exams/rooms-management" element={<SeatingManagementStudioPage />} />
          <Route path="ems/seating" element={<SeatingManagementStudioPage />} />
          <Route path="exams/invigilators" element={<InvigilatorManagementStudioPage />} />
          <Route path="exams/duty-rosters" element={<InvigilatorManagementStudioPage />} />
          <Route path="ems/invigilators" element={<InvigilatorManagementStudioPage />} />
          <Route path="exams/practical" element={<PracticalVivaStudioPage />} />
          <Route path="exams/viva" element={<PracticalVivaStudioPage />} />
          <Route path="exams/osce" element={<PracticalVivaStudioPage />} />
          <Route path="ems/practical" element={<PracticalVivaStudioPage />} />
          <Route path="exams/attendance" element={<ExamAttendanceStudioPage />} />
          <Route path="exams/live-attendance" element={<ExamAttendanceStudioPage />} />
          <Route path="ems/attendance" element={<ExamAttendanceStudioPage />} />
          <Route path="exams/evaluation" element={<EvaluationManagementStudioPage />} />
          <Route path="exams/digital-evaluation" element={<EvaluationManagementStudioPage />} />
          <Route path="exams/moderation" element={<EvaluationManagementStudioPage />} />
          <Route path="ems/evaluation" element={<EvaluationManagementStudioPage />} />
          <Route path="exams/marks-entry" element={<MarksEntryStudioPage />} />
          <Route path="exams/faculty-marks" element={<MarksEntryStudioPage />} />
          <Route path="ems/marks-entry" element={<MarksEntryStudioPage />} />
          <Route path="exams/results-processing" element={<ResultProcessingStudioPage />} />
          <Route path="exams/results" element={<ResultProcessingStudioPage />} />
          <Route path="ems/results" element={<ResultProcessingStudioPage />} />
          <Route path="exams/revaluation" element={<RevaluationSupplementaryStudioPage />} />
          <Route path="exams/supplementary" element={<RevaluationSupplementaryStudioPage />} />
          <Route path="ems/revaluation" element={<RevaluationSupplementaryStudioPage />} />
          <Route path="exams/transcripts" element={<TranscriptsCertificatesStudioPage />} />
          <Route path="exams/certificates" element={<TranscriptsCertificatesStudioPage />} />
          <Route path="ems/transcripts" element={<TranscriptsCertificatesStudioPage />} />
          <Route path="exams/compliance" element={<ComplianceReportsStudioPage />} />
          <Route path="exams/reports" element={<ComplianceReportsStudioPage />} />
          <Route path="ems/compliance" element={<ComplianceReportsStudioPage />} />
          <Route path="exams/analytics-studio" element={<ExamAnalyticsStudioPage />} />
          <Route path="exams/predictive" element={<ExamAnalyticsStudioPage />} />
          <Route path="ems/analytics" element={<ExamAnalyticsStudioPage />} />
          <Route path="exams/student-portal" element={<StudentExaminationPortalPage />} />
          <Route path="student/exams" element={<StudentExaminationPortalPage />} />
          <Route path="ems/student" element={<StudentExaminationPortalPage />} />
          <Route path="exams/faculty-portal" element={<FacultyExaminationPortalPage />} />
          <Route path="faculty/exams" element={<FacultyExaminationPortalPage />} />
          <Route path="ems/faculty" element={<FacultyExaminationPortalPage />} />
          <Route path="exams/coe-portal" element={<CoeMasterPortalPage />} />
          <Route path="coe/exams" element={<CoeMasterPortalPage />} />
          <Route path="ems/coe" element={<CoeMasterPortalPage />} />
          <Route path="exams/enterprise-integration" element={<EnterpriseIntegrationStudioPage />} />
          <Route path="exams/system-health" element={<EnterpriseIntegrationStudioPage />} />
          <Route path="ems/integration" element={<EnterpriseIntegrationStudioPage />} />
          <Route path="lms" element={<LmsDashboardPage />} />
          <Route path="lms/dashboard" element={<LmsDashboardPage />} />
          <Route path="lms/courses" element={<CourseManagementStudioPage />} />
          <Route path="lms/course-management" element={<CourseManagementStudioPage />} />
          <Route path="lms/lessons" element={<LessonBuilderStudioPage />} />
          <Route path="lms/lesson-builder" element={<LessonBuilderStudioPage />} />
          <Route path="lms/video" element={<VideoLearningStudioPage />} />
          <Route path="lms/video-learning" element={<VideoLearningStudioPage />} />
          <Route path="lms/live-classes" element={<LiveClassesStudioPage />} />
          <Route path="lms/live" element={<LiveClassesStudioPage />} />
          <Route path="lms/assignments" element={<AssignmentManagementStudioPage />} />
          <Route path="lms/assignment-management" element={<AssignmentManagementStudioPage />} />
          <Route path="lms/quizzes" element={<QuizPracticeStudioPage />} />
          <Route path="lms/practice" element={<QuizPracticeStudioPage />} />
          <Route path="lms/discussions" element={<DiscussionCollaborationStudioPage />} />
          <Route path="lms/forums" element={<DiscussionCollaborationStudioPage />} />
          <Route path="lms/chat" element={<DiscussionCollaborationStudioPage />} />
          <Route path="lms/engagement" element={<AttendanceEngagementStudioPage />} />
          <Route path="lms/attendance" element={<AttendanceEngagementStudioPage />} />
          <Route path="lms/activity" element={<AttendanceEngagementStudioPage />} />
          <Route path="lms/analytics" element={<ProgressAnalyticsStudioPage />} />
          <Route path="lms/progress" element={<ProgressAnalyticsStudioPage />} />
          <Route path="lms/gamification" element={<ProgressAnalyticsStudioPage />} />
          <Route path="lms/library" element={<DigitalLibraryStudioPage />} />
          <Route path="lms/digital-library" element={<DigitalLibraryStudioPage />} />
          <Route path="lms/certificates" element={<CertificatesCredentialsStudioPage />} />
          <Route path="lms/credentials" element={<CertificatesCredentialsStudioPage />} />
          <Route path="lms/parents" element={<ParentPortalStudioPage />} />
          <Route path="lms/parent-portal" element={<ParentPortalStudioPage />} />
          <Route path="lms/faculty" element={<FacultyPortalStudioPage />} />
          <Route path="lms/faculty-portal" element={<FacultyPortalStudioPage />} />
          <Route path="lms/student" element={<StudentPortalStudioPage />} />
          <Route path="lms/student-portal" element={<StudentPortalStudioPage />} />
          <Route path="lms/ai" element={<AiLearningAssistantStudioPage />} />
          <Route path="lms/ai-tutor" element={<AiLearningAssistantStudioPage />} />
          <Route path="lms/mobile" element={<MobileLearningStudioPage />} />
          <Route path="lms/offline" element={<MobileLearningStudioPage />} />
          <Route path="lms/reports" element={<AnalyticsReportsStudioPage />} />
          <Route path="lms/institution-reports" element={<AnalyticsReportsStudioPage />} />
          <Route path="lms/integrations" element={<EnterpriseIntegrationsStudioPage />} />
          <Route path="lms/connectors" element={<EnterpriseIntegrationsStudioPage />} />
          <Route path="lms/readiness" element={<ProductionReadinessStudioPage />} />
          <Route path="lms/production-readiness" element={<ProductionReadinessStudioPage />} />

          <Route
            path="attendance"
            element={
              <SubsystemView
                title="Attendance & Leave Management"
                category="ACADEMIC"
                description="Biometric and classroom attendance tracking, faculty leave workflows, and shortage alerts."
                icon={CalendarCheck}
                subdomain="attendance"
                status="ACTIVE"
                features={[
                  "Daily period-wise student classroom attendance recording",
                  "Biometric device synchronization and RFID card logging",
                  "Automated parent SMS alert trigger on absence threshold",
                  "Staff and faculty leave application and approval matrix",
                ]}
              />
            }
          />

          <Route
            path="fees"
            element={
              <SubsystemView
                title="Fee & Finance Management"
                category="FINANCE"
                description="Institutional fee collection, installment scheduling, scholarship allocations, and GST receipt generation."
                icon={IndianRupee}
                subdomain="fees"
                status="ACTIVE"
                features={[
                  "Automated fee head allocation and flexible installment scheduling",
                  "Real-time online payment gateway integration (Razorpay/Stripe)",
                  "Instant GST-compliant fee receipt PDF generation and email dispatch",
                  "Scholarship concession management and late-fee calculations",
                ]}
              />
            }
          />

          {/* Module 8 ERP Academic Engine & Timetable Planner */}
          <Route path="academics" element={<AcademicsManagementPage />} />

          <Route path="admissions" element={<AdmissionsPipelinePage />} />

          <Route path="students" element={<StudentsManagementPage />} />

          <Route
            path="cms/enquiries"
            element={
              <SubsystemView
                title="Website Leads & Inquiries"
                category="PLATFORM"
                description="Capture, triage, and route public website contact inquiries and admission leads."
                icon={MessageSquare}
                subdomain="website"
                status="ACTIVE"
                features={[
                  "Real-time public contact form submissions inbox",
                  "Automated email auto-responder to prospective students",
                  "Spam filtering and IP reputation validation",
                  "One-click conversion to admission applicant lead",
                ]}
              />
            }
          />

          <Route path="settings" element={<SystemSettingsManagerPage />} />
          <Route path="system-settings" element={<SystemSettingsManagerPage />} />

          <Route path="sessions" element={<ActiveSessionsPage />} />

          <Route path="login-history" element={<LoginHistoryAuditPage />} />
          <Route path="security-policies" element={<SecurityPoliciesPage />} />

          <Route path="institute" element={<InstituteSetupPage />} />
          <Route path="departments" element={<DepartmentsManagementPage />} />
          <Route path="notifications" element={<NotificationCenterPage />} />
          <Route path="media-manager" element={<MediaFileManagerPage />} />
          <Route path="workflows" element={<WorkflowEnginePage />} />
          <Route path="reports" element={<ReportsEnginePage />} />
          <Route path="roles" element={<RolesPermissionsPage />} />
          <Route path="users" element={<UsersManagementPage />} />
          <Route path="audit-logs" element={<AuditLogsPage />} />
        </Route>
      </Route>

      {/* Fallback to Public Homepage */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};
