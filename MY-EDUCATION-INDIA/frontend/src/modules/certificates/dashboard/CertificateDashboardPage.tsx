import React from "react";
import { Link } from "react-router-dom";
import {
  FileBadge,
  FileCheck2,
  ShieldCheck,
  QrCode,
  Layers,
  Contact,
  TrendingUp,
  XCircle,
  Plus,
  Search,
} from "lucide-react";
import { CertificateDashboardSummary } from "../types/certificate.types";

export const CertificateDashboardPage: React.FC = () => {
  const summary: CertificateDashboardSummary = {
    total_issued_certificates: 520,
    pending_approvals_count: 8,
    revoked_certificates_count: 3,
    public_verifications_count: 1480,
    active_templates_count: 14,
    id_cards_active_count: 450,
    document_distribution: {
      "Course Completion": 220,
      "Marksheets / Grade Cards": 180,
      "Bonafide Certificates": 65,
      "Transfer Certificates": 42,
      "Internship Experience": 13,
    },
    monthly_trend: [
      { month: "Jul 2026", issued: 45, verified: 110 },
      { month: "Aug 2026", issued: 120, verified: 280 },
      { month: "Sep 2026", issued: 90, verified: 310 },
      { month: "Oct 2026", issued: 110, verified: 390 },
      { month: "Nov 2026", issued: 155, verified: 390 },
    ],
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <FileBadge className="h-7 w-7 text-teal-600 dark:text-teal-400" />
            Enterprise Certificate & Digital Verification Control Center
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Generate, approve, issue, digitally verify, and revoke institutional certificates, degrees, and ID cards.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Link
            to="/admin/certificates/generator"
            className="flex items-center gap-2 rounded-lg bg-teal-600 px-4 py-2 text-sm font-semibold text-white shadow-xs hover:bg-teal-700 transition"
          >
            <Plus className="h-4 w-4" />
            <span>Generate Certificates</span>
          </Link>
          <Link
            to="/verify"
            target="_blank"
            className="flex items-center gap-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2 text-sm font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 transition"
          >
            <Search className="h-4 w-4" />
            <span>Public Verify Portal</span>
          </Link>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {/* Total Issued */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              Total Issued Credentials
            </span>
            <div className="rounded-lg bg-teal-50 dark:bg-teal-900/40 p-2 text-teal-600 dark:text-teal-400">
              <FileCheck2 className="h-5 w-5" />
            </div>
          </div>
          <p className="mt-3 text-2xl font-bold text-slate-900 dark:text-white">
            {summary.total_issued_certificates} Issued
          </p>
          <p className="mt-1 text-xs text-slate-500">Degrees, marksheets, bonafide & transfer certificates</p>
        </div>

        {/* Public Verifications */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">
              Public Verifications
            </span>
            <div className="rounded-lg bg-emerald-50 dark:bg-emerald-900/40 p-2 text-emerald-600 dark:text-emerald-400">
              <ShieldCheck className="h-5 w-5" />
            </div>
          </div>
          <p className="mt-3 text-2xl font-bold text-emerald-600 dark:text-emerald-400">
            {summary.public_verifications_count.toLocaleString("en-IN")} Hits
          </p>
          <p className="mt-1 text-xs text-slate-500">QR & Verification ID authenticated</p>
        </div>

        {/* Pending Approvals */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-amber-500 dark:text-amber-400">
              Pending Approvals
            </span>
            <div className="rounded-lg bg-amber-50 dark:bg-amber-900/40 p-2 text-amber-500 dark:text-amber-400">
              <FileBadge className="h-5 w-5" />
            </div>
          </div>
          <p className="mt-3 text-2xl font-bold text-amber-500 dark:text-amber-400">
            {summary.pending_approvals_count} In Review
          </p>
          <p className="mt-1 text-xs text-slate-500">Requires Registrar / Principal sign-off</p>
        </div>

        {/* Revoked Credentials */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-rose-500 dark:text-rose-400">
              Revoked Credentials
            </span>
            <div className="rounded-lg bg-rose-50 dark:bg-rose-900/40 p-2 text-rose-600 dark:text-rose-400">
              <XCircle className="h-5 w-5" />
            </div>
          </div>
          <p className="mt-3 text-2xl font-bold text-rose-600 dark:text-rose-400">
            {summary.revoked_certificates_count} Revoked
          </p>
          <p className="mt-1 text-xs text-slate-500">Blacklisted on public portal</p>
        </div>
      </div>

      {/* Operational Hub Fast Links */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
        <Link
          to="/admin/certificates/templates"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-teal-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-teal-600 group-hover:text-white transition">
            <Layers className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Template Library</span>
        </Link>

        <Link
          to="/admin/certificates/designer"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-teal-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-teal-600 group-hover:text-white transition">
            <FileBadge className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Visual Designer</span>
        </Link>

        <Link
          to="/admin/certificates/generator"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-teal-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-teal-600 group-hover:text-white transition">
            <Plus className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Bulk Generator</span>
        </Link>

        <Link
          to="/admin/certificates/id-cards"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-teal-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-teal-600 group-hover:text-white transition">
            <Contact className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Campus ID Cards</span>
        </Link>

        <Link
          to="/admin/certificates/reports"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-teal-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-teal-600 group-hover:text-white transition">
            <QrCode className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Issuance Registers</span>
        </Link>

        <Link
          to="/admin/certificates/settings"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-teal-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-teal-600 group-hover:text-white transition">
            <ShieldCheck className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Security & DSC</span>
        </Link>
      </div>

      {/* Document Distribution Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs">
          <h2 className="text-base font-bold text-slate-900 dark:text-white mb-4">
            Document Type Issuance Breakdown
          </h2>
          <div className="space-y-3">
            {Object.entries(summary.document_distribution).map(([type, count]) => {
              const pct = ((count / summary.total_issued_certificates) * 100).toFixed(1);
              return (
                <div key={type} className="space-y-1">
                  <div className="flex justify-between text-xs font-medium text-slate-700 dark:text-slate-300">
                    <span className="font-bold">{type}</span>
                    <span>{count} Issued ({pct}%)</span>
                  </div>
                  <div className="h-2 w-full rounded-full bg-slate-100 dark:bg-slate-700 overflow-hidden">
                    <div
                      className="h-full bg-teal-600 rounded-full"
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs flex flex-col justify-between">
          <div>
            <h2 className="text-base font-bold text-slate-900 dark:text-white mb-3">
              Instant Public Digital Verification (Zero-Login)
            </h2>
            <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              Employers, embassies, and universities can authenticate any credential issued by MY EDUCATION INDIA in real time using the 2D optical QR code or verification identifier.
            </p>
            <div className="mt-4 p-4 rounded-lg bg-teal-50 dark:bg-teal-950/40 border border-teal-200/60 dark:border-teal-800">
              <span className="text-xs font-bold text-teal-800 dark:text-teal-300">Public Portal URL</span>
              <p className="font-mono text-xs font-semibold text-teal-900 dark:text-teal-200 mt-1">
                https://myeducationindia.com/verify
              </p>
            </div>
          </div>
          <Link
            to="/verify"
            target="_blank"
            className="mt-4 w-full flex items-center justify-center gap-2 rounded-lg bg-teal-600 py-2.5 text-xs font-bold text-white hover:bg-teal-700 transition"
          >
            <ShieldCheck className="h-4 w-4" />
            <span>Open Public Verification Portal</span>
          </Link>
        </div>
      </div>
    </div>
  );
};
