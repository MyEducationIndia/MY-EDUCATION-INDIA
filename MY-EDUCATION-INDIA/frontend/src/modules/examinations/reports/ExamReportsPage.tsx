import React, { useState } from "react";
import { TrendingUp, Download, Filter, Award } from "lucide-react";

export const ExamReportsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <TrendingUp className="h-7 w-7 text-amber-500" />
            Institutional Examination & Merit Analytics
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Batch-wise pass percentage, rank lists, subject failure analysis, and backlog statistics.
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

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Computer Science & AI</span>
          <p className="mt-2 text-2xl font-black text-emerald-600">98.2% Pass</p>
          <p className="mt-1 text-xs text-slate-500">120 Students • 0 Backlogs</p>
        </div>
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Electronics & Communication</span>
          <p className="mt-2 text-2xl font-black text-emerald-600">94.5% Pass</p>
          <p className="mt-1 text-xs text-slate-500">80 Students • 4 Backlogs</p>
        </div>
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-400">MBA Executive</span>
          <p className="mt-2 text-2xl font-black text-emerald-600">100.0% Pass</p>
          <p className="mt-1 text-xs text-slate-500">60 Students • All Distinction</p>
        </div>
      </div>
    </div>
  );
};
