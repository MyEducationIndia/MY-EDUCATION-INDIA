import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { LoginPage } from "@/modules/auth/pages/LoginPage";
import { UnauthorizedPage } from "@/modules/auth/pages/UnauthorizedPage";
import { ForbiddenPage } from "@/modules/auth/pages/ForbiddenPage";
import { ActiveSessionsPage } from "@/modules/auth/pages/ActiveSessionsPage";
import { LoginHistoryPage } from "@/modules/auth/pages/LoginHistoryPage";
import { ProtectedRoute } from "@/modules/auth/components/ProtectedRoute";
import { SuperAdminLayout } from "@/layouts/SuperAdminLayout";
import { SuperAdminDashboardPage } from "@/pages/admin/SuperAdminDashboardPage";
import { RolesPermissionsPage } from "@/pages/admin/RolesPermissionsPage";
import { UsersManagementPage } from "@/pages/admin/UsersManagementPage";
import { AuditLogsPage } from "@/pages/admin/AuditLogsPage";

// Module 3: Core System Engine Pages
import { SettingsDashboardPage } from "@/modules/system/pages/SettingsDashboardPage";
import { InstituteManagementPage } from "@/modules/system/pages/InstituteManagementPage";
import { BranchManagementPage } from "@/modules/system/pages/BranchManagementPage";
import { AcademicYearPage } from "@/modules/system/pages/AcademicYearPage";
import { FinancialYearPage } from "@/modules/system/pages/FinancialYearPage";
import { NumberGeneratorPage } from "@/modules/system/pages/NumberGeneratorPage";
import { AuthenticationSettingsPage } from "@/modules/system/pages/AuthenticationSettingsPage";
import { AppearanceSettingsPage } from "@/modules/system/pages/AppearanceSettingsPage";
import { GeneralSettingsPage } from "@/modules/system/pages/GeneralSettingsPage";

// Module 4: Enterprise Admin Dashboard & Control Center
import { EnterpriseAdminDashboardPage } from "@/modules/dashboard/pages/EnterpriseAdminDashboardPage";

// Module 5: Enterprise Website CMS & Page Builder
import { DynamicPublicPageView } from "@/modules/cms/pages/DynamicPublicPageView";
import { AdminPagesManagementPage } from "@/modules/cms/pages/AdminPagesManagementPage";
import { AdminEnquiriesPage } from "@/modules/cms/pages/AdminEnquiriesPage";

// Module 6: Enterprise Student Information Management System (SIMS)
import { StudentDirectoryPage } from "@/modules/students/pages/StudentDirectoryPage";

// Module 7: Enterprise Admission & CRM System
import { AdmissionDashboardPage } from "@/modules/admissions/dashboard/AdmissionDashboardPage";
import { LeadManagementPage } from "@/modules/admissions/leads/LeadManagementPage";
import { ApplicationDirectoryPage } from "@/modules/admissions/applications/ApplicationDirectoryPage";
import { OnlineAdmissionFormPage } from "@/modules/admissions/forms/OnlineAdmissionFormPage";

// Module 8: Enterprise Academic Management System
import { AcademicDashboardPage } from "@/modules/academics/dashboard/AcademicDashboardPage";
import { DepartmentsPage } from "@/modules/academics/departments/DepartmentsPage";
import { CoursesDirectoryPage } from "@/modules/academics/courses/CoursesDirectoryPage";
import { BatchesSectionsPage } from "@/modules/academics/batches/BatchesSectionsPage";
import { InteractiveTimetablePage } from "@/modules/academics/timetable/InteractiveTimetablePage";

// Module 9: Enterprise Fee & Finance Management System
import { FeeDashboardPage } from "@/modules/fees/dashboard/FeeDashboardPage";
import { FeeStructuresPage } from "@/modules/fees/structures/FeeStructuresPage";
import { FeeCategoriesPage } from "@/modules/fees/categories/FeeCategoriesPage";
import { FeeCollectionPage } from "@/modules/fees/collections/FeeCollectionPage";
import { ScholarshipsPage } from "@/modules/fees/scholarships/ScholarshipsPage";
import { RefundsManagementPage } from "@/modules/fees/refunds/RefundsManagementPage";
import { FinancialReportsPage } from "@/modules/fees/reports/FinancialReportsPage";

// Module 10: Enterprise Attendance & Leave Management System
import { AttendanceDashboardPage } from "@/modules/attendance/dashboard/AttendanceDashboardPage";
import { StudentAttendancePage } from "@/modules/attendance/student/StudentAttendancePage";
import { QRAttendanceScannerPage } from "@/modules/attendance/qr/QRAttendanceScannerPage";
import { FacultyAttendancePage } from "@/modules/attendance/faculty/FacultyAttendancePage";
import { StaffAttendancePage } from "@/modules/attendance/staff/StaffAttendancePage";
import { LeaveManagementPage } from "@/modules/attendance/leave/LeaveManagementPage";
import { AttendanceReportsPage } from "@/modules/attendance/reports/AttendanceReportsPage";
import { AttendanceSettingsPage } from "@/modules/attendance/settings/AttendanceSettingsPage";

// Module 11: Enterprise Examination & Result Management System
import { ExamDashboardPage } from "@/modules/examinations/dashboard/ExamDashboardPage";
import { ExamScheduleCalendarPage } from "@/modules/examinations/calendar/ExamScheduleCalendarPage";
import { HallTicketsPage } from "@/modules/examinations/halltickets/HallTicketsPage";
import { MarkEntryGridPage } from "@/modules/examinations/marks/MarkEntryGridPage";
import { ResultPublicationPage } from "@/modules/examinations/results/ResultPublicationPage";
import { GradeScaleConfigPage } from "@/modules/examinations/grades/GradeScaleConfigPage";
import { TranscriptsDirectoryPage } from "@/modules/examinations/transcripts/TranscriptsDirectoryPage";
import { ExamReportsPage } from "@/modules/examinations/reports/ExamReportsPage";

// Module 12: Enterprise Computer Based Testing (CBT) Platform
import { CBTDashboardPage } from "@/modules/cbt/dashboard/CBTDashboardPage";
import { QuestionBankPage } from "@/modules/cbt/question-bank/QuestionBankPage";
import { ExamBuilderPage } from "@/modules/cbt/exam-builder/ExamBuilderPage";
import { CandidateExamInterfacePage } from "@/modules/cbt/candidate/CandidateExamInterfacePage";
import { LiveProctorMonitorPage } from "@/modules/cbt/live-monitor/LiveProctorMonitorPage";
import { CBTReportsPage } from "@/modules/cbt/reports/CBTReportsPage";
import { QuestionAnalyticsPage } from "@/modules/cbt/analytics/QuestionAnalyticsPage";
import { OfflineSyncStatusPage } from "@/modules/cbt/offline/OfflineSyncStatusPage";
import { CBTSecuritySettingsPage } from "@/modules/cbt/settings/CBTSecuritySettingsPage";

// Module 13: Enterprise Certificate, Document Generation & Digital Verification System
import { CertificateDashboardPage } from "@/modules/certificates/dashboard/CertificateDashboardPage";
import { CertificateTemplatesPage } from "@/modules/certificates/templates/CertificateTemplatesPage";
import { VisualCertificateDesignerPage } from "@/modules/certificates/designer/VisualCertificateDesignerPage";
import { BulkDocumentGeneratorPage } from "@/modules/certificates/generator/BulkDocumentGeneratorPage";
import { PublicVerificationPortalPage } from "@/modules/certificates/verification/PublicVerificationPortalPage";
import { IDCardGeneratorPage } from "@/modules/certificates/idcards/IDCardGeneratorPage";
import { CertificateReportsPage } from "@/modules/certificates/reports/CertificateReportsPage";
import { CertificateAnalyticsPage } from "@/modules/certificates/analytics/CertificateAnalyticsPage";
import { CertificateSettingsPage } from "@/modules/certificates/settings/CertificateSettingsPage";

// Module 14: Enterprise Library & Digital Knowledge Management System
import { LibraryDashboardPage } from "@/modules/library/dashboard/LibraryDashboardPage";
import { BookCatalogPage } from "@/modules/library/catalog/BookCatalogPage";
import { BookCopiesAccessionPage } from "@/modules/library/copies/BookCopiesAccessionPage";
import { LibraryMembersPage } from "@/modules/library/members/LibraryMembersPage";
import { IssueReturnTerminalPage } from "@/modules/library/issues/IssueReturnTerminalPage";
import { BookReservationsPage } from "@/modules/library/reservations/BookReservationsPage";
import { DigitalKnowledgeRepoPage } from "@/modules/library/digital/DigitalKnowledgeRepoPage";
import { OPACPublicCatalogPage } from "@/modules/library/opac/OPACPublicCatalogPage";
import { LibraryReportsPage } from "@/modules/library/reports/LibraryReportsPage";
import { LibraryAnalyticsPage } from "@/modules/library/analytics/LibraryAnalyticsPage";
import { LibraryRulesSettingsPage } from "@/modules/library/settings/LibraryRulesSettingsPage";

// Module 15: Enterprise Learning Experience Platform (LXP)
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
import { LXPReportsPage } from "@/modules/lxp/reports/LXPReportsPage";
import { LXPAnalyticsPage } from "@/modules/lxp/analytics/LXPAnalyticsPage";
import { LXPSettingsPage } from "@/modules/lxp/settings/LXPSettingsPage";

// Universal API Integration Framework Pages
import { ApiDashboardPage } from "@/modules/integrations/dashboard/ApiDashboardPage";
import { ProviderDirectoryPage } from "@/modules/integrations/providers/ProviderDirectoryPage";
import { CredentialVaultPage } from "@/modules/integrations/vault/CredentialVaultPage";
import { ConnectionTestTerminalPage } from "@/modules/integrations/tester/ConnectionTestTerminalPage";
import { WebhooksManagerPage } from "@/modules/integrations/webhooks/WebhooksManagerPage";
import { ApiExecutionLogsPage } from "@/modules/integrations/logs/ApiExecutionLogsPage";
import { ApiAnalyticsPage } from "@/modules/integrations/analytics/ApiAnalyticsPage";

// Module 17: Enterprise CRM, Sales, Marketing & Franchise Pages
import { CrmDashboardPage } from "@/modules/crm/dashboard/CrmDashboardPage";
import { LeadsDirectoryPage } from "@/modules/crm/leads/LeadsDirectoryPage";
import { EnquiriesInboxPage } from "@/modules/crm/enquiries/EnquiriesInboxPage";
import { FollowupCalendarPage } from "@/modules/crm/followups/FollowupCalendarPage";
import { SalesPipelineKanbanPage } from "@/modules/crm/pipeline/SalesPipelineKanbanPage";
import { MarketingCampaignsPage } from "@/modules/crm/campaigns/MarketingCampaignsPage";
import { ReferralProgramsPage } from "@/modules/crm/referrals/ReferralProgramsPage";
import { CrmTasksPage } from "@/modules/crm/tasks/CrmTasksPage";
import { FranchiseManagementPage } from "@/modules/crm/franchise/FranchiseManagementPage";
import { CrmReportsPage } from "@/modules/crm/reports/CrmReportsPage";
import { CrmAnalyticsPage } from "@/modules/crm/analytics/CrmAnalyticsPage";
import { CrmSettingsPage } from "@/modules/crm/settings/CrmSettingsPage";

// Module 18: Enterprise Reports, Analytics & BI Pages
import { ExecutiveDashboardPage } from "@/modules/bi/dashboard/ExecutiveDashboardPage";
import { ReportsDirectoryPage } from "@/modules/bi/reports/ReportsDirectoryPage";
import { ReportBuilderPage } from "@/modules/bi/report-builder/ReportBuilderPage";
import { ChartStudioPage } from "@/modules/bi/charts/ChartStudioPage";
import { CrossModuleAnalyticsPage } from "@/modules/bi/analytics/CrossModuleAnalyticsPage";
import { DashboardWidgetsPage } from "@/modules/bi/widgets/DashboardWidgetsPage";
import { KpiManagementPage } from "@/modules/bi/kpis/KpiManagementPage";
import { ExportCenterPage } from "@/modules/bi/exports/ExportCenterPage";
import { SystemHealthDashboardPage } from "@/modules/bi/system-health/SystemHealthDashboardPage";
import { AuditReportsPage } from "@/modules/bi/audit/AuditReportsPage";
import { BiSettingsPage } from "@/modules/bi/settings/BiSettingsPage";

// Module 19: Enterprise Platform Administration, Security, Backup & DevOps Pages
import { PlatformDashboardPage } from "@/modules/platform/dashboard/PlatformDashboardPage";
import { SystemSettingsPage } from "@/modules/platform/settings/SystemSettingsPage";
import { SecurityCenterPage } from "@/modules/platform/security/SecurityCenterPage";
import { BackupManagerPage } from "@/modules/platform/backups/BackupManagerPage";
import { RestoreManagerPage } from "@/modules/platform/restores/RestoreManagerPage";
import { FeatureFlagsPage } from "@/modules/platform/feature-flags/FeatureFlagsPage";
import { StorageManagerPage } from "@/modules/platform/storage/StorageManagerPage";
import { ClusterHealthPage } from "@/modules/platform/health/ClusterHealthPage";
import { AuditCenterPage } from "@/modules/platform/audit/AuditCenterPage";
import { LicenseManagerPage } from "@/modules/platform/licenses/LicenseManagerPage";
import { MaintenanceModePage } from "@/modules/platform/maintenance/MaintenanceModePage";
import { PlatformReportsPage } from "@/modules/platform/reports/PlatformReportsPage";

// Module 20: Enterprise Experience Platform Pages
import { RootOwnerConsolePage } from "@/modules/platform/root-owner/RootOwnerConsolePage";
import { SuperAdminControlCenterPage } from "@/modules/platform/super-admin/SuperAdminControlCenterPage";
import { PortalSelectorPage } from "@/modules/platform/portal/PortalSelectorPage";
import { StudentPortalPage } from "@/modules/platform/portal/StudentPortalPage";
import { FacultyPortalPage } from "@/modules/platform/portal/FacultyPortalPage";
import { DeveloperConsolePage } from "@/modules/platform/developer/DeveloperConsolePage";
import { DashboardBuilderPage } from "@/modules/platform/dashboard-builder/DashboardBuilderPage";
import { VisualFormBuilderPage } from "@/modules/platform/form-builder/VisualFormBuilderPage";
import { MenuBuilderPage } from "@/modules/platform/menu-builder/MenuBuilderPage";
import { GlobalSearchPage } from "@/modules/platform/search/GlobalSearchPage";
import { SupportCenterPage } from "@/modules/platform/support/SupportCenterPage";
import { ThemeBrandingPage } from "@/modules/platform/theme/ThemeBrandingPage";

export const AppRoutes: React.FC = () => {
  return (
    <Routes>
      {/* Public Authentication Routes */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/401" element={<UnauthorizedPage />} />
      <Route path="/403" element={<ForbiddenPage />} />

      {/* Public Online Admission Application Page */}
      <Route path="/admissions/apply" element={<OnlineAdmissionFormPage />} />

      {/* Public Digital Credential Verification Portal (Zero Login) */}
      <Route path="/verify" element={<PublicVerificationPortalPage />} />
      <Route path="/verify/:token" element={<PublicVerificationPortalPage />} />

      {/* Module 5: Dynamic Public Website Pages */}
      <Route path="/" element={<DynamicPublicPageView />} />
      <Route path="/:slug" element={<DynamicPublicPageView />} />

      {/* Protected Admin Routes Enforced by Enterprise ProtectedRoute */}
      <Route element={<ProtectedRoute />}>
        <Route path="/admin" element={<SuperAdminLayout />}>
          <Route index element={<Navigate to="dashboard" replace />} />
          <Route path="dashboard" element={<EnterpriseAdminDashboardPage />} />
          <Route path="modules" element={<SuperAdminDashboardPage />} />
          <Route path="roles" element={<RolesPermissionsPage />} />
          <Route path="users" element={<UsersManagementPage />} />

                                                                                {/* Module 20: Experience Master Control & Studios */}
          <Route path="master-control" element={<SuperAdminControlCenterPage />} />
          <Route path="portals" element={<PortalSelectorPage />} />
          <Route path="builder/dashboards" element={<DashboardBuilderPage />} />
          <Route path="builder/forms" element={<VisualFormBuilderPage />} />
          <Route path="builder/menus" element={<MenuBuilderPage />} />
          <Route path="branding" element={<ThemeBrandingPage />} />
          <Route path="support" element={<SupportCenterPage />} />

          {/* Module 19: Enterprise Platform Administration & DevOps Routes */}
          <Route path="platform" element={<PlatformDashboardPage />} />
          <Route path="platform/settings" element={<SystemSettingsPage />} />
          <Route path="platform/security" element={<SecurityCenterPage />} />
          <Route path="platform/backups" element={<BackupManagerPage />} />
          <Route path="platform/restores" element={<RestoreManagerPage />} />
          <Route path="platform/feature-flags" element={<FeatureFlagsPage />} />
          <Route path="platform/storage" element={<StorageManagerPage />} />
          <Route path="platform/health" element={<ClusterHealthPage />} />
          <Route path="platform/audit" element={<AuditCenterPage />} />
          <Route path="platform/licenses" element={<LicenseManagerPage />} />
          <Route path="platform/maintenance" element={<MaintenanceModePage />} />
          <Route path="platform/reports" element={<PlatformReportsPage />} />

          {/* Module 18: Enterprise Reports, Analytics & BI Routes */}
          <Route path="bi" element={<ExecutiveDashboardPage />} />
          <Route path="bi/reports" element={<ReportsDirectoryPage />} />
          <Route path="bi/builder" element={<ReportBuilderPage />} />
          <Route path="bi/charts" element={<ChartStudioPage />} />
          <Route path="bi/analytics" element={<CrossModuleAnalyticsPage />} />
          <Route path="bi/widgets" element={<DashboardWidgetsPage />} />
          <Route path="bi/kpis" element={<KpiManagementPage />} />
          <Route path="bi/exports" element={<ExportCenterPage />} />
          <Route path="bi/health" element={<SystemHealthDashboardPage />} />
          <Route path="bi/audit" element={<AuditReportsPage />} />
          <Route path="bi/settings" element={<BiSettingsPage />} />

          {/* Module 17: Enterprise CRM, Sales, Marketing & Franchise Routes */}
          <Route path="crm" element={<CrmDashboardPage />} />
          <Route path="crm/leads" element={<LeadsDirectoryPage />} />
          <Route path="crm/enquiries" element={<EnquiriesInboxPage />} />
          <Route path="crm/followups" element={<FollowupCalendarPage />} />
          <Route path="crm/pipeline" element={<SalesPipelineKanbanPage />} />
          <Route path="crm/campaigns" element={<MarketingCampaignsPage />} />
          <Route path="crm/referrals" element={<ReferralProgramsPage />} />
          <Route path="crm/tasks" element={<CrmTasksPage />} />
          <Route path="crm/franchise" element={<FranchiseManagementPage />} />
          <Route path="crm/reports" element={<CrmReportsPage />} />
          <Route path="crm/analytics" element={<CrmAnalyticsPage />} />
          <Route path="crm/settings" element={<CrmSettingsPage />} />

          {/* Universal API Integration Framework Routes */}
          <Route path="integrations" element={<ApiDashboardPage />} />
          <Route path="integrations/providers" element={<ProviderDirectoryPage />} />
          <Route path="integrations/vault" element={<CredentialVaultPage />} />
          <Route path="integrations/tester" element={<ConnectionTestTerminalPage />} />
          <Route path="integrations/webhooks" element={<WebhooksManagerPage />} />
          <Route path="integrations/logs" element={<ApiExecutionLogsPage />} />
          <Route path="integrations/analytics" element={<ApiAnalyticsPage />} />

          {/* Module 15: Enterprise Learning Experience Platform (LXP) Routes */}
          <Route path="lxp" element={<LearningDashboardPage />} />
          <Route path="lxp/courses" element={<CoursesCatalogPage />} />
          <Route path="lxp/builder" element={<CourseBuilderPage />} />
          <Route path="lxp/modules" element={<CourseModulesPage />} />
          <Route path="lxp/lessons" element={<LessonViewerPage />} />
          <Route path="lxp/videos" element={<VideoLibraryPage />} />
          <Route path="lxp/assignments" element={<AssignmentsHubPage />} />
          <Route path="lxp/practice" element={<PracticeTestsHubPage />} />
          <Route path="lxp/forum" element={<DiscussionForumPage />} />
          <Route path="lxp/progress" element={<StudentProgressPage />} />
          <Route path="lxp/reports" element={<LXPReportsPage />} />
          <Route path="lxp/analytics" element={<LXPAnalyticsPage />} />
          <Route path="lxp/settings" element={<LXPSettingsPage />} />

          {/* Module 14: Enterprise Library & Knowledge Management Routes */}
          <Route path="library" element={<LibraryDashboardPage />} />
          <Route path="library/catalog" element={<BookCatalogPage />} />
          <Route path="library/copies" element={<BookCopiesAccessionPage />} />
          <Route path="library/members" element={<LibraryMembersPage />} />
          <Route path="library/circulation" element={<IssueReturnTerminalPage />} />
          <Route path="library/reservations" element={<BookReservationsPage />} />
          <Route path="library/digital" element={<DigitalKnowledgeRepoPage />} />
          <Route path="library/reports" element={<LibraryReportsPage />} />
          <Route path="library/analytics" element={<LibraryAnalyticsPage />} />
          <Route path="library/settings" element={<LibraryRulesSettingsPage />} />

          {/* Module 13: Certificate & Document Management Routes */}
          <Route path="certificates" element={<CertificateDashboardPage />} />
          <Route path="certificates/templates" element={<CertificateTemplatesPage />} />
          <Route path="certificates/designer" element={<VisualCertificateDesignerPage />} />
          <Route path="certificates/generator" element={<BulkDocumentGeneratorPage />} />
          <Route path="certificates/id-cards" element={<IDCardGeneratorPage />} />
          <Route path="certificates/reports" element={<CertificateReportsPage />} />
          <Route path="certificates/analytics" element={<CertificateAnalyticsPage />} />
          <Route path="certificates/settings" element={<CertificateSettingsPage />} />

          {/* Module 12: CBT Platform Routes */}
          <Route path="cbt" element={<CBTDashboardPage />} />
          <Route path="cbt/question-bank" element={<QuestionBankPage />} />
          <Route path="cbt/exam-builder" element={<ExamBuilderPage />} />
          <Route path="cbt/candidate-demo" element={<CandidateExamInterfacePage />} />
          <Route path="cbt/live" element={<LiveProctorMonitorPage />} />
          <Route path="cbt/reports" element={<CBTReportsPage />} />
          <Route path="cbt/analytics" element={<QuestionAnalyticsPage />} />
          <Route path="cbt/offline" element={<OfflineSyncStatusPage />} />
          <Route path="cbt/settings" element={<CBTSecuritySettingsPage />} />

          {/* Module 11: Examination & Result Management Routes */}
          <Route path="exams" element={<ExamDashboardPage />} />
          <Route path="exams/calendar" element={<ExamScheduleCalendarPage />} />
          <Route path="exams/hall-tickets" element={<HallTicketsPage />} />
          <Route path="exams/marks" element={<MarkEntryGridPage />} />
          <Route path="exams/results" element={<ResultPublicationPage />} />
          <Route path="exams/grades" element={<GradeScaleConfigPage />} />
          <Route path="exams/transcripts" element={<TranscriptsDirectoryPage />} />
          <Route path="exams/reports" element={<ExamReportsPage />} />

          {/* Module 10: Attendance & Leave Management Routes */}
          <Route path="attendance" element={<AttendanceDashboardPage />} />
          <Route path="attendance/student" element={<StudentAttendancePage />} />
          <Route path="attendance/qr-scanner" element={<QRAttendanceScannerPage />} />
          <Route path="attendance/faculty" element={<FacultyAttendancePage />} />
          <Route path="attendance/staff" element={<StaffAttendancePage />} />
          <Route path="attendance/leave" element={<LeaveManagementPage />} />
          <Route path="attendance/reports" element={<AttendanceReportsPage />} />
          <Route path="attendance/settings" element={<AttendanceSettingsPage />} />

          {/* Module 9: Fee & Finance Management Routes */}
          <Route path="fees" element={<FeeDashboardPage />} />
          <Route path="fees/structures" element={<FeeStructuresPage />} />
          <Route path="fees/categories" element={<FeeCategoriesPage />} />
          <Route path="fees/collect" element={<FeeCollectionPage />} />
          <Route path="fees/scholarships" element={<ScholarshipsPage />} />
          <Route path="fees/refunds" element={<RefundsManagementPage />} />
          <Route path="fees/reports" element={<FinancialReportsPage />} />

          {/* Module 8: Academic Management System Routes */}
          <Route path="academics" element={<AcademicDashboardPage />} />
          <Route path="academics/departments" element={<DepartmentsPage />} />
          <Route path="academics/courses" element={<CoursesDirectoryPage />} />
          <Route path="academics/batches" element={<BatchesSectionsPage />} />
          <Route path="academics/timetable" element={<InteractiveTimetablePage />} />

          {/* Module 7: Admission & CRM Routes */}
          <Route path="admissions" element={<AdmissionDashboardPage />} />
          <Route path="admissions/leads" element={<LeadManagementPage />} />
          <Route path="admissions/applications" element={<ApplicationDirectoryPage />} />
          <Route path="admissions/applications/new" element={<OnlineAdmissionFormPage />} />

          {/* Module 6: SIMS Routes */}
          <Route path="students" element={<StudentDirectoryPage />} />

          {/* Module 5: Admin CMS Governance Routes */}
          <Route path="cms/pages" element={<AdminPagesManagementPage />} />
          <Route path="cms/enquiries" element={<AdminEnquiriesPage />} />

          {/* Module 3: Core System Engine Routes */}
          <Route path="settings" element={<SettingsDashboardPage />} />
          <Route path="settings/institutes" element={<InstituteManagementPage />} />
          <Route path="settings/branches" element={<BranchManagementPage />} />
          <Route path="settings/academic-years" element={<AcademicYearPage />} />
          <Route path="settings/financial-years" element={<FinancialYearPage />} />
          <Route path="settings/number-generator" element={<NumberGeneratorPage />} />
          <Route path="settings/authentication" element={<AuthenticationSettingsPage />} />
          <Route path="settings/appearance" element={<AppearanceSettingsPage />} />
          <Route path="settings/general" element={<GeneralSettingsPage />} />

          {/* Security & Audit Routes */}
          <Route path="audit-logs" element={<AuditLogsPage />} />
          <Route path="sessions" element={<ActiveSessionsPage />} />
          <Route path="login-history" element={<LoginHistoryPage />} />
        </Route>
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};
