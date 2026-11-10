import React, { useState } from "react";
import { CalendarCheck, Download, Filter, AlertTriangle } from "lucide-react";

export const AttendanceReportsPage: React.FC = () => {
  const [reportType, setReportType] = useState("DAILY");

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <CalendarCheck className="h-7 w-7 text-indigo-600 dark:text-indigo-400" />
            Attendance Ledgers & Regulatory Deficiency Lists
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Export UGC/AICTE compliant attendance registers, exam debarment lists, and monthly faculty tallies.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => alert("Excel Export")}
            className="flex items-center gap-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-2 text-xs font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 transition"
          >
            <Download className="h-4 w-4" />
            <span>Excel Export</span>
          </button>
          <button
            type="button"
            onClick={() => alert("PDF Print")}
            className="flex items-center gap-2 rounded-lg bg-indigo-600 px-3 py-2 text-xs font-semibold text-white hover:bg-indigo-700 transition"
          >
            <Download className="h-4 w-4" />
            <span>PDF Print</span>
          </button>
        </div>
      </div>

      {/* Deficiency Warning Notice */}
      <div className="rounded-xl border border-rose-200 dark:border-rose-900/60 bg-rose-50 dark:bg-rose-950/20 p-4 flex items-start gap-3">
        <AlertTriangle className="h-5 w-5 text-rose-600 dark:text-rose-400 shrink-0 mt-0.5" />
        <div>
          <h3 className="text-sm font-bold text-rose-900 dark:text-rose-200">UGC/AICTE Statutory 75% Rule Enforcement</h3>
          <p className="text-xs text-rose-700 dark:text-rose-300 mt-0.5">
            14 students currently have attendance below the 75.0% threshold and will be debarred from semester examinations unless medical/duty condonations are approved.
          </p>
        </div>
      </div>
    </div>
  );
};
