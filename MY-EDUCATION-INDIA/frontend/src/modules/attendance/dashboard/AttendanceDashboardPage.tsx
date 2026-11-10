import React from "react";
import { Link } from "react-router-dom";
import {
  CalendarCheck,
  Users,
  UserCheck,
  UserX,
  Clock,
  QrCode,
  FileCheck2,
  AlertTriangle,
  GraduationCap,
  Briefcase,
  CheckCircle2,
} from "lucide-react";
import { AttendanceDashboardSummary } from "../types/attendance.types";

export const AttendanceDashboardPage: React.FC = () => {
  const summary: AttendanceDashboardSummary = {
    today_date: "2026-11-06",
    total_students_enrolled: 450,
    students_present_count: 412,
    students_absent_count: 28,
    students_late_count: 10,
    overall_attendance_pct: 91.55,
    faculty_present_pct: 96.5,
    staff_present_pct: 95.0,
    pending_leaves_count: 6,
    low_attendance_alert_count: 14,
    weekly_trend: [
      { day: "Mon", attendance_pct: 94.2 },
      { day: "Tue", attendance_pct: 92.8 },
      { day: "Wed", attendance_pct: 91.5 },
      { day: "Thu", attendance_pct: 93.0 },
      { day: "Fri", attendance_pct: 89.6 },
      { day: "Sat", attendance_pct: 88.0 },
    ],
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <CalendarCheck className="h-7 w-7 text-indigo-600 dark:text-indigo-400" />
            Enterprise Attendance & Leave Control Center
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Real-time multi-modal attendance tracking across Students, Faculty, and Staff with instant leave approvals.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Link
            to="/admin/attendance/qr-scanner"
            className="flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-xs hover:bg-indigo-700 transition"
          >
            <QrCode className="h-4 w-4" />
            <span>Launch QR Scanner</span>
          </Link>
          <Link
            to="/admin/attendance/student"
            className="flex items-center gap-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2 text-sm font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 transition"
          >
            <Users className="h-4 w-4" />
            <span>Mark Student Roll</span>
          </Link>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {/* Today's Student Attendance % */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              Student Attendance
            </span>
            <div className="rounded-lg bg-indigo-50 dark:bg-indigo-900/40 p-2 text-indigo-600 dark:text-indigo-400">
              <GraduationCap className="h-5 w-5" />
            </div>
          </div>
          <p className="mt-3 text-2xl font-bold text-slate-900 dark:text-white">
            {summary.overall_attendance_pct}%
          </p>
          <div className="mt-1 flex items-center gap-2 text-xs text-slate-500">
            <span className="font-semibold text-emerald-600">{summary.students_present_count} Present</span>
            <span>•</span>
            <span className="font-semibold text-rose-500">{summary.students_absent_count} Absent</span>
          </div>
        </div>

        {/* Faculty Presence Rate */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">
              Faculty Presence
            </span>
            <div className="rounded-lg bg-emerald-50 dark:bg-emerald-900/40 p-2 text-emerald-600 dark:text-emerald-400">
              <UserCheck className="h-5 w-5" />
            </div>
          </div>
          <p className="mt-3 text-2xl font-bold text-emerald-600 dark:text-emerald-400">
            {summary.faculty_present_pct}%
          </p>
          <p className="mt-1 text-xs text-slate-500">Biometric & RFID verified on campus</p>
        </div>

        {/* Pending Leave Requests */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-amber-500 dark:text-amber-400">
              Pending Leaves
            </span>
            <div className="rounded-lg bg-amber-50 dark:bg-amber-900/40 p-2 text-amber-600 dark:text-amber-400">
              <FileCheck2 className="h-5 w-5" />
            </div>
          </div>
          <p className="mt-3 text-2xl font-bold text-amber-600 dark:text-amber-400">
            {summary.pending_leaves_count} Requests
          </p>
          <p className="mt-1 text-xs text-slate-500">Requires HOD & Admin approval</p>
        </div>

        {/* Low Attendance Alert */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-rose-500 dark:text-rose-400">
              Attendance Deficiency
            </span>
            <div className="rounded-lg bg-rose-50 dark:bg-rose-900/40 p-2 text-rose-600 dark:text-rose-400">
              <AlertTriangle className="h-5 w-5" />
            </div>
          </div>
          <p className="mt-3 text-2xl font-bold text-rose-600 dark:text-rose-400">
            {summary.low_attendance_alert_count} Students
          </p>
          <p className="mt-1 text-xs text-slate-500">Below UGC/AICTE 75% exam threshold</p>
        </div>
      </div>

      {/* Operational Hub Fast Links */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
        <Link
          to="/admin/attendance/student"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-indigo-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-indigo-600 group-hover:text-white transition">
            <GraduationCap className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Student Roll Call</span>
        </Link>

        <Link
          to="/admin/attendance/qr-scanner"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-indigo-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-indigo-600 group-hover:text-white transition">
            <QrCode className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">QR Scanner</span>
        </Link>

        <Link
          to="/admin/attendance/faculty"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-indigo-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-indigo-600 group-hover:text-white transition">
            <Briefcase className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Faculty Log</span>
        </Link>

        <Link
          to="/admin/attendance/staff"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-indigo-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-indigo-600 group-hover:text-white transition">
            <Clock className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Staff Shift Terminal</span>
        </Link>

        <Link
          to="/admin/attendance/leave"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-indigo-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-indigo-600 group-hover:text-white transition">
            <FileCheck2 className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Leave Approvals</span>
        </Link>

        <Link
          to="/admin/attendance/reports"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-indigo-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-indigo-600 group-hover:text-white transition">
            <CalendarCheck className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Ledgers & Registers</span>
        </Link>
      </div>

      {/* Weekly Trend Bar Charts */}
      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs">
        <h2 className="text-base font-bold text-slate-900 dark:text-white mb-4">
          Weekly Attendance Rate Trend (%)
        </h2>
        <div className="grid grid-cols-6 gap-3">
          {summary.weekly_trend.map((item) => (
            <div key={item.day} className="flex flex-col items-center gap-2">
              <div className="h-32 w-full bg-slate-100 dark:bg-slate-700/50 rounded-lg flex items-end p-1.5">
                <div
                  className="w-full bg-indigo-600 rounded-md transition-all duration-300"
                  style={{ height: `${item.attendance_pct}%` }}
                />
              </div>
              <span className="text-xs font-bold text-slate-700 dark:text-slate-300">{item.day}</span>
              <span className="text-[11px] font-semibold text-indigo-600 dark:text-indigo-400">{item.attendance_pct}%</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
