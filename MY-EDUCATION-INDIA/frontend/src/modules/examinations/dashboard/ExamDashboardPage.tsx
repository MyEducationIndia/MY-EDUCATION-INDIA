import React, { useState, useMemo } from "react";
import { Link } from "react-router-dom";
import {
  Award,
  Calendar,
  FileCheck2,
  CheckCircle2,
  TrendingUp,
  FileText,
  AlertTriangle,
  QrCode,
  GraduationCap,
  Sliders,
  Users,
  Building2,
  Clock,
  Play,
  RotateCcw,
  Sparkles,
  BookOpen,
  Layers,
  ArrowRight,
  ShieldCheck,
  UserCheck,
  Download,
  Search,
  Filter,
  Check,
  X,
  FileBadge,
  Activity,
  Briefcase,
  HelpCircle,
} from "lucide-react";

type EMSRole =
  | "ROOT_OWNER"
  | "SUPER_ADMIN"
  | "COE"
  | "PRINCIPAL"
  | "HOD"
  | "FACULTY"
  | "EVALUATOR"
  | "STUDENT";

interface RoleMetricState {
  upcomingExams: number;
  runningExams: number;
  pendingResults: number;
  evalProgressPct: number;
  hallTicketsIssued: number;
  revaluationRequests: number;
  supplementaryExams: number;
  overallPassPct: number;
  activeStudents: number;
  label: string;
}

export const ExamDashboardPage: React.FC = () => {
  const [selectedRole, setSelectedRole] = useState<EMSRole>("COE");
  const [selectedSession, setSelectedSession] = useState<string>("EXAM-2026-AUTUMN-01");
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 4000);
  };

  // 8 Role Personas Metrics
  const roleMetrics: Record<EMSRole, RoleMetricState> = {
    ROOT_OWNER: {
      upcomingExams: 18,
      runningExams: 4,
      pendingResults: 2,
      evalProgressPct: 82.0,
      hallTicketsIssued: 3120,
      revaluationRequests: 18,
      supplementaryExams: 24,
      overallPassPct: 91.2,
      activeStudents: 3120,
      label: "Institutional Owner & Board of Governors Command",
    },
    SUPER_ADMIN: {
      upcomingExams: 18,
      runningExams: 4,
      pendingResults: 2,
      evalProgressPct: 82.0,
      hallTicketsIssued: 3120,
      revaluationRequests: 18,
      supplementaryExams: 24,
      overallPassPct: 91.2,
      activeStudents: 3120,
      label: "Campus System Administration & Operations",
    },
    COE: {
      upcomingExams: 12,
      runningExams: 4,
      pendingResults: 3,
      evalProgressPct: 78.5,
      hallTicketsIssued: 2450,
      revaluationRequests: 18,
      supplementaryExams: 24,
      overallPassPct: 89.4,
      activeStudents: 2450,
      label: "Office of the Controller of Examinations (COE)",
    },
    PRINCIPAL: {
      upcomingExams: 8,
      runningExams: 2,
      pendingResults: 1,
      evalProgressPct: 75.0,
      hallTicketsIssued: 850,
      revaluationRequests: 6,
      supplementaryExams: 8,
      overallPassPct: 88.6,
      activeStudents: 850,
      label: "Academic Head & Principal Governance",
    },
    HOD: {
      upcomingExams: 4,
      runningExams: 2,
      pendingResults: 1,
      evalProgressPct: 80.0,
      hallTicketsIssued: 420,
      revaluationRequests: 4,
      supplementaryExams: 5,
      overallPassPct: 90.5,
      activeStudents: 420,
      label: "Department of Computer Science & Engineering",
    },
    FACULTY: {
      upcomingExams: 3,
      runningExams: 1,
      pendingResults: 1,
      evalProgressPct: 72.0,
      hallTicketsIssued: 240,
      revaluationRequests: 3,
      supplementaryExams: 4,
      overallPassPct: 85.0,
      activeStudents: 240,
      label: "Faculty Invigilation & Internal Marks Portal",
    },
    EVALUATOR: {
      upcomingExams: 2,
      runningExams: 1,
      pendingResults: 1,
      evalProgressPct: 68.0,
      hallTicketsIssued: 240,
      revaluationRequests: 2,
      supplementaryExams: 3,
      overallPassPct: 82.5,
      activeStudents: 240,
      label: "Answer Script Evaluation & Moderation Portal",
    },
    STUDENT: {
      upcomingExams: 4,
      runningExams: 1,
      pendingResults: 1,
      evalProgressPct: 100.0,
      hallTicketsIssued: 1,
      revaluationRequests: 0,
      supplementaryExams: 0,
      overallPassPct: 94.5,
      activeStudents: 1,
      label: "Candidate Exam Hall Tickets & Result Transcripts",
    },
  };

  const currentMetrics = roleMetrics[selectedRole];

  // Upcoming Exams List
  const upcomingExams = [
    {
      id: "ue-1",
      title: "End-Semester Theory Examinations (Autumn 2026)",
      type: "UNIVERSITY_THEORY",
      date: "18 Nov 2026",
      sessionCode: "EXAM-2026-AUTUMN-01",
      studentsCount: 1240,
      center: "TC-IND-01",
    },
    {
      id: "ue-2",
      title: "B.Tech Computer Science Practical & Viva-Voce",
      type: "PRACTICAL_VIVA",
      date: "22 Nov 2026",
      sessionCode: "PRAC-2026-CS-02",
      studentsCount: 420,
      center: "TC-IND-01",
    },
    {
      id: "ue-3",
      title: "Mid-Semester Unit Tests & Continuous Assessment",
      type: "MID_TERM_INTERNAL",
      date: "28 Nov 2026",
      sessionCode: "MID-2026-SEM3",
      studentsCount: 890,
      center: "TC-IND-01",
    },
  ];

  // Running Exams Shift Status
  const runningExams = [
    {
      id: "re-1",
      subject: "Data Structures & Algorithms (CS301)",
      venue: "Computer Lab 01 (Terminals 1-50)",
      timing: "Shift 1: 09:30 AM - 12:30 PM",
      attendancePct: 98.5,
      status: "RUNNING_IN_PROGRESS",
    },
    {
      id: "re-2",
      subject: "Discrete Mathematics & Graph Theory (MA201)",
      venue: "Examination Hall A (Ground Floor)",
      timing: "Shift 1: 09:30 AM - 12:30 PM",
      attendancePct: 96.0,
      status: "RUNNING_IN_PROGRESS",
    },
  ];

  // Evaluation Progress Matrix
  const evaluationTasks = [
    {
      course: "Database Management Systems (CS402)",
      evaluator: "Dr. Rajeshwari Sen (External Examiner)",
      total: 240,
      evaluated: 192,
      progressPct: 80.0,
      deadline: "15 Nov 2026",
    },
    {
      course: "Operating Systems & Concurrency (CS401)",
      evaluator: "Prof. Amit Kumar (Internal Evaluator)",
      total: 240,
      evaluated: 144,
      progressPct: 60.0,
      deadline: "16 Nov 2026",
    },
    {
      course: "Engineering Linear Algebra (MA101)",
      evaluator: "Dr. Manoj Tiwari (Moderation Panel)",
      total: 320,
      evaluated: 320,
      progressPct: 100.0,
      deadline: "Completed (Awaiting COE Lock)",
    },
  ];

  return (
    <div className="space-y-6">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="p-4 rounded-xl bg-cyan-50 dark:bg-cyan-950/40 border border-cyan-300 dark:border-cyan-800 text-cyan-900 dark:text-cyan-200 text-xs font-semibold flex items-center gap-3 shadow-xs animate-fade-in">
          <CheckCircle2 className="h-5 w-5 text-cyan-600 shrink-0" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* 1. Header Banner */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <Award className="h-7 w-7 text-amber-500" />
            Phase 4: Enterprise Examination Management System (EMS)
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            End-to-end examination command: scheduling, timetables, hall tickets, seating plans, invigilators, practicals/viva, evaluation, marks entry, and regulatory compliance.
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          <button
            onClick={() => showToast("Synchronized real-time telemetry across all 8 examination command roles.")}
            className="px-3.5 py-2 rounded-xl border border-slate-300 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 font-semibold text-xs transition flex items-center gap-1.5 shadow-xs"
          >
            <RotateCcw className="h-4 w-4" /> Live Refresh
          </button>
          <Link
            to="/admin/cbt"
            className="px-4 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-semibold text-xs tracking-wide shadow-md transition flex items-center gap-2"
          >
            <Layers className="h-4 w-4" />
            Switch to Phase 3 CBT Engine
          </Link>
        </div>
      </div>

      {/* 2. Persona Role Selector Bar */}
      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-3 shadow-xs space-y-2">
        <div className="flex items-center justify-between text-xs font-semibold text-slate-500 px-1">
          <span className="uppercase tracking-wider">Select Examination Role Persona:</span>
          <span className="font-mono text-cyan-600 dark:text-cyan-400 font-bold">{currentMetrics.label}</span>
        </div>

        <div className="flex flex-wrap items-center gap-1.5 overflow-x-auto pb-1">
          {[
            { id: "ROOT_OWNER", label: "Root Owner", icon: Briefcase },
            { id: "SUPER_ADMIN", label: "Super Admin", icon: ShieldCheck },
            { id: "COE", label: "Controller of Exams", icon: Award },
            { id: "PRINCIPAL", label: "Principal", icon: Building2 },
            { id: "HOD", label: "Head of Dept (HOD)", icon: Layers },
            { id: "FACULTY", label: "Faculty Invigilator", icon: UserCheck },
            { id: "EVALUATOR", label: "Evaluator / Grader", icon: Sliders },
            { id: "STUDENT", label: "Student Candidate", icon: GraduationCap },
          ].map((r) => {
            const Icon = r.icon;
            const isSelected = selectedRole === r.id;
            return (
              <button
                key={r.id}
                onClick={() => setSelectedRole(r.id as EMSRole)}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 shrink-0 ${
                  isSelected
                    ? "bg-amber-500 text-slate-950 shadow-xs"
                    : "bg-slate-100 hover:bg-slate-200 text-slate-700 dark:bg-slate-700/60 dark:text-slate-300 dark:hover:bg-slate-700"
                }`}
              >
                <Icon className="h-3.5 w-3.5" />
                {r.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* 3. Core Operational Widgets (8 Key Metrics) */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {/* Widget 1: Upcoming Exams */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Upcoming Exams</span>
            <Calendar className="h-5 w-5 text-indigo-600 dark:text-indigo-400" />
          </div>
          <p className="mt-3 text-3xl font-bold text-slate-900 dark:text-white font-mono">
            {currentMetrics.upcomingExams}
          </p>
          <p className="mt-1 text-xs text-slate-500">Theory, Practical & Unit Tests</p>
        </div>

        {/* Widget 2: Running Exams */}
        <div className="rounded-xl border border-emerald-200 dark:border-emerald-900/50 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">
              Running Exams (Live)
            </span>
            <Activity className="h-5 w-5 text-emerald-600" />
          </div>
          <p className="mt-3 text-3xl font-bold text-emerald-600 dark:text-emerald-400 font-mono">
            {currentMetrics.runningExams}
          </p>
          <p className="mt-1 text-xs text-slate-500">Shift 1 currently underway</p>
        </div>

        {/* Widget 3: Pending Results */}
        <div className="rounded-xl border border-amber-200 dark:border-amber-900/50 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-amber-600 dark:text-amber-400">
              Pending Results
            </span>
            <Clock className="h-5 w-5 text-amber-600" />
          </div>
          <p className="mt-3 text-3xl font-bold text-amber-600 dark:text-amber-400 font-mono">
            {currentMetrics.pendingResults}
          </p>
          <p className="mt-1 text-xs text-slate-500">Under COE moderation lock</p>
        </div>

        {/* Widget 4: Evaluation Progress */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Evaluation Progress</span>
            <Sliders className="h-5 w-5 text-cyan-600 dark:text-cyan-400" />
          </div>
          <p className="mt-3 text-3xl font-bold text-cyan-600 dark:text-cyan-400 font-mono">
            {currentMetrics.evalProgressPct}%
          </p>
          <p className="mt-1 text-xs text-slate-500">Double evaluation active</p>
        </div>

        {/* Widget 5: Hall Tickets Issued */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Hall Tickets Issued</span>
            <QrCode className="h-5 w-5 text-slate-600 dark:text-slate-300" />
          </div>
          <p className="mt-3 text-3xl font-bold text-slate-900 dark:text-white font-mono">
            {currentMetrics.hallTicketsIssued.toLocaleString()}
          </p>
          <p className="mt-1 text-xs text-slate-500">QR & barcode verified</p>
        </div>

        {/* Widget 6: Revaluation Requests */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Revaluation Requests</span>
            <AlertTriangle className="h-5 w-5 text-rose-500" />
          </div>
          <p className="mt-3 text-3xl font-bold text-rose-600 dark:text-rose-400 font-mono">
            {currentMetrics.revaluationRequests}
          </p>
          <p className="mt-1 text-xs text-slate-500">Fee verified applications</p>
        </div>

        {/* Widget 7: Supplementary Exams */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Supplementary Exams</span>
            <BookOpen className="h-5 w-5 text-indigo-500" />
          </div>
          <p className="mt-3 text-3xl font-bold text-indigo-600 dark:text-indigo-400 font-mono">
            {currentMetrics.supplementaryExams}
          </p>
          <p className="mt-1 text-xs text-slate-500">Registrations open</p>
        </div>

        {/* Widget 8: Overall Statistics */}
        <div className="rounded-xl border border-emerald-200 dark:border-emerald-900/50 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">
              Overall Pass Rate
            </span>
            <TrendingUp className="h-5 w-5 text-emerald-600" />
          </div>
          <p className="mt-3 text-3xl font-bold text-emerald-600 dark:text-emerald-400 font-mono">
            {currentMetrics.overallPassPct}%
          </p>
          <p className="mt-1 text-xs text-slate-500">{currentMetrics.activeStudents} enrolled students</p>
        </div>
      </div>

      {/* 4. Live Running Exams & Evaluation Progress Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Running Exams Shift Telemetry */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
            <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <Activity className="h-5 w-5 text-emerald-600 animate-pulse" /> Live Running Exam Shifts
            </h2>
            <span className="text-xs text-slate-500 font-mono">Real-Time Hall Monitoring</span>
          </div>

          <div className="space-y-3">
            {runningExams.map((re) => (
              <div
                key={re.id}
                className="p-4 rounded-xl border border-slate-200 dark:border-slate-700/80 bg-slate-50/50 dark:bg-slate-900/40 space-y-2 text-xs"
              >
                <div className="flex items-center justify-between">
                  <h3 className="font-bold text-sm text-slate-900 dark:text-white">{re.subject}</h3>
                  <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 border border-emerald-500/30 text-[10px] font-bold">
                    IN PROGRESS
                  </span>
                </div>
                <div className="flex items-center justify-between text-slate-600 dark:text-slate-400">
                  <span>Venue: <strong>{re.venue}</strong></span>
                  <span className="font-mono">{re.timing}</span>
                </div>
                <div className="space-y-1 pt-1">
                  <div className="flex items-center justify-between text-[11px] text-slate-500">
                    <span>Attendance Marked</span>
                    <span className="font-bold text-emerald-600">{re.attendancePct}%</span>
                  </div>
                  <div className="h-2 w-full bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                    <div className="h-full bg-emerald-500" style={{ width: `${re.attendancePct}%` }} />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Evaluation & Grading Progress */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
            <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <Sliders className="h-5 w-5 text-cyan-600" /> Answer Book Evaluation Progress
            </h2>
            <span className="text-xs text-slate-500 font-mono">Centralized Valuation Board</span>
          </div>

          <div className="space-y-3">
            {evaluationTasks.map((et, idx) => (
              <div
                key={idx}
                className="p-4 rounded-xl border border-slate-200 dark:border-slate-700/80 bg-slate-50/50 dark:bg-slate-900/40 space-y-2 text-xs"
              >
                <div className="flex items-center justify-between">
                  <h3 className="font-bold text-sm text-slate-900 dark:text-white">{et.course}</h3>
                  <span className="font-mono text-cyan-600 font-bold">
                    {et.evaluated} / {et.total} scripts
                  </span>
                </div>
                <div className="text-slate-500 text-[11px]">{et.evaluator} • Deadline: {et.deadline}</div>
                <div className="space-y-1 pt-1">
                  <div className="flex items-center justify-between text-[11px] text-slate-500">
                    <span>Grading Completed</span>
                    <span className="font-bold text-cyan-600">{et.progressPct}%</span>
                  </div>
                  <div className="h-2 w-full bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                    <div className="h-full bg-cyan-500" style={{ width: `${et.progressPct}%` }} />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 5. Upcoming Examination Calendar Table */}
      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 shadow-xs overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
          <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Calendar className="h-5 w-5 text-amber-500" /> Upcoming Examination Sessions & Timetables
          </h2>
          <span className="text-xs text-slate-500 font-mono">Autumn Session 2026</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 dark:bg-slate-900/60 text-slate-600 dark:text-slate-400 uppercase font-bold tracking-wider border-b border-slate-200 dark:border-slate-800">
              <tr>
                <th className="py-3 px-4">Examination Session</th>
                <th className="py-3 px-4">Exam Modality</th>
                <th className="py-3 px-4 text-center">Date</th>
                <th className="py-3 px-4 text-center">Candidates</th>
                <th className="py-3 px-4 text-center">Testing Venue</th>
                <th className="py-3 px-4 text-center">Hall Ticket Status</th>
                <th className="py-3 px-4 text-center">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {upcomingExams.map((ue) => (
                <tr key={ue.id} className="hover:bg-slate-50/60 dark:hover:bg-slate-900/30 transition">
                  <td className="py-3.5 px-4">
                    <div className="font-bold text-slate-900 dark:text-white">{ue.title}</div>
                    <div className="text-[11px] text-slate-500 font-mono">{ue.sessionCode}</div>
                  </td>
                  <td className="py-3.5 px-4">
                    <span className="px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 font-mono text-[10px] font-bold">
                      {ue.type.replace("_", " ")}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-center font-mono font-bold text-slate-800 dark:text-slate-200">
                    {ue.date}
                  </td>
                  <td className="py-3.5 px-4 text-center font-mono font-semibold text-cyan-600">
                    {ue.studentsCount} Students
                  </td>
                  <td className="py-3.5 px-4 text-center font-mono">{ue.center}</td>
                  <td className="py-3.5 px-4 text-center">
                    <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-emerald-600">
                      <CheckCircle2 className="h-3.5 w-3.5" /> Ready for Print
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-center">
                    <button
                      onClick={() => showToast(`Initiated hall ticket batch download for ${ue.sessionCode}.`)}
                      className="px-2.5 py-1 rounded bg-slate-100 hover:bg-slate-200 dark:bg-slate-700 dark:hover:bg-slate-600 text-slate-800 dark:text-slate-200 font-semibold text-[11px] transition"
                    >
                      Download Admit Cards
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
