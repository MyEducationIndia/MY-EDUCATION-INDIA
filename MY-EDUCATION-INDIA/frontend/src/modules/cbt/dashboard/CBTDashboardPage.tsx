import React from "react";
import { Link } from "react-router-dom";
import {
  MonitorPlay,
  Settings,
  Sparkles,
  FileBadge,
  Award,
  Layers,
  FileCheck2,
  Users,
  Calendar,
  Building2,
  WifiOff,
  TrendingUp,
  Sliders,
  Play,
  CheckCircle2,
  Clock,
  ShieldAlert,
} from "lucide-react";
import { CBTDashboardSummary } from "../types/cbt.types";

export const CBTDashboardPage: React.FC = () => {
  const summary: CBTDashboardSummary = {
    total_questions_in_bank: 2450,
    active_cbt_sessions_count: 3,
    live_active_candidates_count: 142,
    total_exams_delivered_today: 380,
    offline_syncs_processed: 64,
    average_candidate_score: 78.4,
    recent_sessions: [
      { code: "CBT-CS101-MAIN", mode: "LAN", candidates: 120, status: "LIVE" },
      { code: "CBT-MBA201-MID", mode: "ONLINE", candidates: 60, status: "COMPLETED" },
      { code: "CBT-ENG101-MOCK", mode: "HYBRID", candidates: 200, status: "SCHEDULED" },
    ],
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <MonitorPlay className="h-7 w-7 text-cyan-600 dark:text-cyan-400" />
            Enterprise Computer Based Testing (CBT) Platform
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            High-concurrency exam delivery engine: question bank, exam builder, offline LAN sync, and live proctor monitor.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Link
            to="/admin/cbt/live"
            className="flex items-center gap-2 rounded-lg bg-cyan-600 px-4 py-2 text-sm font-semibold text-white shadow-xs hover:bg-cyan-700 transition"
          >
            <Play className="h-4 w-4" />
            <span>Live Monitor</span>
          </Link>
          <Link
            to="/admin/cbt/portal"
            className="flex items-center gap-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2 text-sm font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 transition"
          >
            <MonitorPlay className="h-4 w-4" />
            <span>Launch Exam UI</span>
          </Link>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {/* Total Questions in Bank */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              Total Question Bank
            </span>
            <div className="rounded-lg bg-blue-50 dark:bg-blue-900/40 p-2 text-blue-600 dark:text-blue-400">
              <Layers className="h-5 w-5" />
            </div>
          </div>
          <p className="mt-3 text-2xl font-bold text-slate-900 dark:text-white">
            {summary.total_questions_in_bank.toLocaleString("en-IN")} Questions
          </p>
          <p className="mt-1 text-xs text-slate-500">MCQ, MSQ, Numerical, Case Study</p>
        </div>

        {/* Live Active Candidates */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">
              Live Testing Candidates
            </span>
            <div className="rounded-lg bg-emerald-50 dark:bg-emerald-900/40 p-2 text-emerald-600 dark:text-emerald-400">
              <Users className="h-5 w-5" />
            </div>
          </div>
          <p className="mt-3 text-2xl font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-2">
            <span className="h-3 w-3 rounded-full bg-emerald-500 animate-pulse" />
            {summary.live_active_candidates_count} Live
          </p>
          <p className="mt-1 text-xs text-slate-500">Real-time heartbeat & autosave active</p>
        </div>

        {/* Offline LAN Syncs */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-purple-600 dark:text-purple-400">
              Offline LAN Syncs
            </span>
            <div className="rounded-lg bg-purple-50 dark:bg-purple-900/40 p-2 text-purple-600 dark:text-purple-400">
              <Settings className="h-5 w-5" />
            </div>
          </div>
          <p className="mt-3 text-2xl font-bold text-purple-600 dark:text-purple-400">
            {summary.offline_syncs_processed} Batches
          </p>
          <p className="mt-1 text-xs text-slate-500">100% SHA-256 Checksum verified</p>
        </div>

        {/* Average Score */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-cyan-600 dark:text-cyan-400">
              Average Performance
            </span>
            <div className="rounded-lg bg-cyan-50 dark:bg-cyan-900/40 p-2 text-cyan-600 dark:text-cyan-400">
              <TrendingUp className="h-5 w-5" />
            </div>
          </div>
          <p className="mt-3 text-2xl font-bold text-cyan-600 dark:text-cyan-400">
            {summary.average_candidate_score}%
          </p>
          <p className="mt-1 text-xs text-slate-500">Directly synchronized to Module 11 marks</p>
        </div>
      </div>

      {/* Operational Fast Links */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-4">
        <Link
          to="/admin/cbt/question-bank"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-cyan-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-cyan-600 group-hover:text-white transition">
            <Layers className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Question Bank</span>
        </Link>

        <Link
          to="/admin/cbt/exam-builder"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-cyan-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-cyan-600 group-hover:text-white transition">
            <Sliders className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Exam Builder</span>
        </Link>

        <Link
          to="/admin/cbt/proctoring"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-cyan-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-cyan-600 group-hover:text-white transition">
            <ShieldAlert className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Live Proctor</span>
        </Link>

        <Link
          to="/admin/cbt/certificates"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-cyan-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-cyan-600 group-hover:text-white transition">
            <FileBadge className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Certificates</span>
        </Link>

        <Link
          to="/admin/cbt/mock-tests"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-cyan-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-cyan-600 group-hover:text-white transition">
            <Sparkles className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Mock Tests</span>
        </Link>

        <Link
          to="/admin/cbt/administration"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-cyan-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-cyan-600 group-hover:text-white transition">
            <Settings className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Administration</span>
        </Link>

        <Link
          to="/admin/cbt/analytics"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-cyan-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-cyan-600 group-hover:text-white transition">
            <TrendingUp className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Item Analytics</span>
        </Link>

        <Link
          to="/admin/cbt/evaluation"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-cyan-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-cyan-600 group-hover:text-white transition">
            <Award className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Evaluation</span>
        </Link>

        <Link
          to="/admin/cbt/reports"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-cyan-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-cyan-600 group-hover:text-white transition">
            <FileCheck2 className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Test Ledgers</span>
        </Link>
        <Link
          to="/admin/cbt/candidates"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-cyan-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-cyan-600 group-hover:text-white transition">
            <Users className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Candidates</span>
        </Link>

        <Link
          to="/admin/cbt/scheduling"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-cyan-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-cyan-600 group-hover:text-white transition">
            <Calendar className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Scheduling</span>
        </Link>

      </div>

      {/* Active CBT Sessions Overview */}
      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs">
        <h2 className="text-base font-bold text-slate-900 dark:text-white mb-4">
          Active Examination Delivery Pipelines
        </h2>
        <div className="space-y-3">
          {summary.recent_sessions.map((sess) => (
            <div
              key={sess.code}
              className="flex items-center justify-between rounded-lg bg-slate-50 dark:bg-slate-700/40 border border-slate-200/60 dark:border-slate-700 p-4"
            >
              <div>
                <span className="font-mono text-xs font-bold text-cyan-600 bg-cyan-50 dark:bg-cyan-950 px-2 py-0.5 rounded-sm">
                  {sess.code}
                </span>
                <p className="mt-1 text-sm font-bold text-slate-900 dark:text-white">
                  Delivery Mode: {sess.mode} Lab Network
                </p>
              </div>
              <div className="flex items-center gap-4">
                <span className="text-xs text-slate-500 font-semibold">{sess.candidates} Candidates</span>
                <span
                  className={`inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-semibold ${
                    sess.status === "LIVE"
                      ? "bg-emerald-50 text-emerald-600 dark:bg-emerald-950/60"
                      : "bg-blue-50 text-blue-600 dark:bg-blue-950/60"
                  }`}
                >
                  {sess.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
