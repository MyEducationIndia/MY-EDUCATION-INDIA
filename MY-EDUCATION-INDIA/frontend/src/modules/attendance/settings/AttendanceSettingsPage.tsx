import React, { useState } from "react";
import { Sliders, Save, CheckCircle } from "lucide-react";

export const AttendanceSettingsPage: React.FC = () => {
  const [minPct, setMinPct] = useState(75);
  const [graceTime, setGraceTime] = useState(15);
  const [lockDays, setLockDays] = useState(2);
  const [autoNotify, setAutoNotify] = useState(true);

  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-5 dark:border-slate-800">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
          <Sliders className="h-7 w-7 text-indigo-600 dark:text-indigo-400" />
          Institutional Attendance Rules & Policies
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Configure statutory minimum thresholds, grace windows, past-date lock policies, and parent alert triggers.
        </p>
      </div>

      <div className="max-w-2xl rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs space-y-5">
        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1.5">
            Minimum Statutory Attendance Threshold (%)
          </label>
          <input
            type="number"
            value={minPct}
            onChange={(e) => setMinPct(Number(e.target.value))}
            className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/50 py-2 px-3 text-sm font-bold text-slate-900 dark:text-white"
          />
          <span className="text-[11px] text-slate-400">Mandatory threshold for semester exam eligibility (AICTE/UGC standard: 75%).</span>
        </div>

        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1.5">
            Late Entry Grace Window (Minutes)
          </label>
          <input
            type="number"
            value={graceTime}
            onChange={(e) => setGraceTime(Number(e.target.value))}
            className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/50 py-2 px-3 text-sm font-bold text-slate-900 dark:text-white"
          />
          <span className="text-[11px] text-slate-400">Grace period after period start before a student/faculty is marked 'LATE'.</span>
        </div>

        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1.5">
            Attendance Record Lock Boundary (Days)
          </label>
          <input
            type="number"
            value={lockDays}
            onChange={(e) => setLockDays(Number(e.target.value))}
            className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/50 py-2 px-3 text-sm font-bold text-slate-900 dark:text-white"
          />
          <span className="text-[11px] text-slate-400">Number of elapsed days after which past attendance cannot be modified without Super Admin override.</span>
        </div>

        <button
          type="button"
          onClick={() => alert("Attendance settings updated successfully!")}
          className="flex items-center gap-2 rounded-lg bg-indigo-600 px-5 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-indigo-700 transition"
        >
          <Save className="h-4 w-4" />
          <span>Save Institutional Policies</span>
        </button>
      </div>
    </div>
  );
};
