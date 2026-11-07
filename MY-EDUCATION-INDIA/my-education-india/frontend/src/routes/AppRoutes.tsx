import React from "react";
import { Link, Routes, Route, Navigate, Outlet } from "react-router-dom";
import { PublicHomePage } from "@/pages/PublicHomePage";
import { LoginPage } from "@/pages/auth/LoginPage";
import { SuperAdminLayout } from "@/layouts/SuperAdminLayout";
import { DashboardOverviewPage } from "@/pages/admin/DashboardOverviewPage";
import { SuperAdminDashboardPage } from "@/pages/admin/SuperAdminDashboardPage";
import { RolesPermissionsPage } from "@/pages/admin/RolesPermissionsPage";
import { UsersManagementPage } from "@/pages/admin/UsersManagementPage";
import { AuditLogsPage } from "@/pages/admin/AuditLogsPage";
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

/**
 * Self-contained Subsystem View component
 */
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
      {/* 1. Public Facing Institute Website (Default Root '/') */}
      <Route path="/" element={<PublicHomePage />} />

      {/* 2. Public Authentication Route ('/login') */}
      <Route path="/login" element={<LoginPage />} />

      {/* 3. Protected Enterprise Command Center Routes ('/admin/*') */}
      <Route element={<ProtectedRoute />}>
        <Route path="/admin" element={<SuperAdminLayout />}>
          <Route index element={<Navigate to="dashboard" replace />} />
          <Route path="dashboard" element={<DashboardOverviewPage />} />
          <Route path="modules" element={<SuperAdminDashboardPage />} />

          <Route
            path="certificates"
            element={
              <SubsystemView
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
              <SubsystemView
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
              <SubsystemView
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

          <Route
            path="academics"
            element={
              <SubsystemView
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
              <SubsystemView
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
              <SubsystemView
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
              <SubsystemView
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

          <Route
            path="settings"
            element={
              <SubsystemView
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
              <SubsystemView
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
              <SubsystemView
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

      {/* Fallback to Public Homepage */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};
