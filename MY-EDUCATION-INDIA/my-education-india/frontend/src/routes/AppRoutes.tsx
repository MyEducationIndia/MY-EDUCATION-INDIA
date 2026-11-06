import React from "react";
import { Routes, Route, Navigate, Outlet } from "react-router-dom";
import { LoginPage } from "@/pages/auth/LoginPage";
import { SuperAdminLayout } from "@/layouts/SuperAdminLayout";
import { DashboardOverviewPage } from "@/pages/admin/DashboardOverviewPage";
import { SuperAdminDashboardPage } from "@/pages/admin/SuperAdminDashboardPage";
import { RolesPermissionsPage } from "@/pages/admin/RolesPermissionsPage";
import { UsersManagementPage } from "@/pages/admin/UsersManagementPage";
import { AuditLogsPage } from "@/pages/admin/AuditLogsPage";
import { SubsystemViewPage } from "@/pages/admin/SubsystemViewPage";
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
} from "lucide-react";

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
      <Route path="/login" element={<LoginPage />} />

      <Route element={<ProtectedRoute />}>
        <Route path="/admin" element={<SuperAdminLayout />}>
          <Route index element={<Navigate to="dashboard" replace />} />
          <Route path="dashboard" element={<DashboardOverviewPage />} />
          <Route path="modules" element={<SuperAdminDashboardPage />} />

          <Route
            path="certificates"
            element={
              <SubsystemViewPage
                title="Certificates & Verification Platform"
                category="ACADEMIC"
                description="Digital tamper-proof credential engine with QR verification, automated PDF issuing, and revocation ledger."
                icon={FileBadge}
                subdomain="certificate"
                status="ENTERPRISE"
                features={[
                  "High-resolution cryptographic certificate generation with QR hash validation",
                  "Public zero-login document verification ledger (/verify/:token)",
                  "Automated certificate revocation and tamper-alert audit trail",
                  "Direct student and faculty download links",
                ]}
              />
            }
          />

          <Route
            path="cbt"
            element={
              <SubsystemViewPage
                title="Computer Based Testing (CBT) Platform"
                category="EXAMINATION"
                description="Secure national examination delivery platform with automated timer, shuffle engine, and proctoring controls."
                icon={MonitorPlay}
                subdomain="cbt"
                status="ENTERPRISE"
                features={[
                  "Secure timed test delivery engine with anti-cheating window blur detector",
                  "Dynamic question bank with automated section-wise shuffling",
                  "Real-time student attempt state persistence in PostgreSQL",
                  "Instant objective grading and percentile calculation",
                ]}
              />
            }
          />

          <Route
            path="exams"
            element={
              <SubsystemViewPage
                title="Examinations & Results Governance"
                category="EXAMINATION"
                description="Comprehensive examination scheduling, marks entry registers, grade calculation, and report cards."
                icon={Award}
                subdomain="exam"
                status="ACTIVE"
                features={[
                  "Term-wise and semester exam timetable scheduling with hall ticket generation",
                  "Faculty marks entry portal with two-tier moderation workflows",
                  "Automated SGPA/CGPA grade calculation engine",
                  "Bulk student marksheet PDF compilation",
                ]}
              />
            }
          />

          <Route
            path="attendance"
            element={
              <SubsystemViewPage
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
              <SubsystemViewPage
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

          <Route
            path="academics"
            element={
              <SubsystemViewPage
                title="Academic Management System"
                category="ACADEMIC"
                description="Curriculum governance, syllabus tracking, interactive timetable builder, and course allocation."
                icon={BookOpen}
                subdomain="academics"
                status="ACTIVE"
                features={[
                  "Degree programs, departments, and course curriculum registry",
                  "Interactive drag-and-drop weekly timetable schedule planner",
                  "Faculty course allocation and lecture workload tracking",
                  "Academic session and term calendar milestones",
                ]}
              />
            }
          />

          <Route
            path="admissions"
            element={
              <SubsystemViewPage
                title="Admission & CRM Pipeline"
                category="ADMISSION"
                description="Online application workflows, lead scoring, applicant inquiry tracking, and document verification."
                icon={ClipboardList}
                subdomain="admissions"
                status="ACTIVE"
                features={[
                  "Public digital admission form with document upload support",
                  "Multi-stage inquiry to admission conversion funnel",
                  "Counsellor lead allocation and follow-up call logging",
                  "Automated provisional offer letter generation",
                ]}
              />
            }
          />

          <Route
            path="students"
            element={
              <SubsystemViewPage
                title="Student Information Management (SIMS)"
                category="CORE"
                description="Unified 360-degree scholar repository, enrollment ledger, guardian contacts, and academic history."
                icon={GraduationCap}
                subdomain="student"
                status="ACTIVE"
                features={[
                  "Comprehensive scholar master profile and admission enrollment register",
                  "Guardian and emergency contact directory",
                  "Document vault for certificates, KYC, and transfer certificates",
                  "Academic transcript and disciplinary conduct ledger",
                ]}
              />
            }
          />

          <Route
            path="cms/pages"
            element={
              <SubsystemViewPage
                title="Website CMS & Page Builder"
                category="PLATFORM"
                description="Public website content management, dynamic page layout builder, and announcements editor."
                icon={Globe}
                subdomain="website"
                status="ACTIVE"
                features={[
                  "Dynamic page builder with customizable hero, about, and faculty blocks",
                  "Institutional noticeboard and press release publisher",
                  "SEO meta tags, OpenGraph images, and sitemap generation",
                  "Media gallery and Cloudinary CDN asset integration",
                ]}
              />
            }
          />

          <Route
            path="cms/enquiries"
            element={
              <SubsystemViewPage
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

          <Route
            path="settings"
            element={
              <SubsystemViewPage
                title="Core System Engine & Settings"
                category="CORE"
                description="Global institutional parameters, campus branch management, and financial year definitions."
                icon={Sliders}
                subdomain="admin"
                status="CORE_LOCKED"
                features={[
                  "Multi-branch campus location registry (MEI-HQ Indore)",
                  "Academic year and financial accounting year lifecycle transitions",
                  "Dynamic number series generator for roll numbers and invoices",
                  "Institutional branding colors, logos, and portal theme preferences",
                ]}
              />
            }
          />

          <Route
            path="sessions"
            element={
              <SubsystemViewPage
                title="Active Sessions & Security"
                category="SECURITY"
                description="Monitor active user sessions across all devices, inspect IP addresses, and enforce logout."
                icon={MonitorSmartphone}
                subdomain="admin"
                status="CORE_LOCKED"
                features={[
                  "Live inspect authenticated sessions in PostgreSQL",
                  "One-click remote session revocation across devices",
                  "IP address, user-agent, and login geolocation audit",
                  "Automated token family rotation on suspicious activity",
                ]}
              />
            }
          />

          <Route
            path="login-history"
            element={
              <SubsystemViewPage
                title="Login History & Access Log"
                category="SECURITY"
                description="Detailed audit log of successful and failed authentication attempts with security alerts."
                icon={History}
                subdomain="admin"
                status="CORE_LOCKED"
                features={[
                  "Historical login timeline with precise timestamps and status codes",
                  "Failed login attempt counter and automatic account lockout alerts",
                  "Device and browser fingerprint tracking",
                  "Direct export to compliance CSV audit reports",
                ]}
              />
            }
          />

          <Route path="roles" element={<RolesPermissionsPage />} />
          <Route path="users" element={<UsersManagementPage />} />
          <Route path="audit-logs" element={<AuditLogsPage />} />
        </Route>
      </Route>

      <Route path="/" element={<Navigate to="/admin/dashboard" replace />} />
      <Route path="*" element={<Navigate to="/admin/dashboard" replace />} />
    </Routes>
  );
};
