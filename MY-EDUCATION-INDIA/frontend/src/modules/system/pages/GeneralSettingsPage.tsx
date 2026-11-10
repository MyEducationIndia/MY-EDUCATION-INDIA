import React from "react";
import { Sliders, Globe, DollarSign, Clock, Calendar } from "lucide-react";

export const GeneralSettingsPage: React.FC = () => {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs dark:border-slate-800 dark:bg-slate-900">
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300">
          <Sliders className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-base font-bold text-slate-900 dark:text-white">
            Global Enterprise Settings
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Localized conventions, Indian standard currency (INR ₹), IST timezone (+05:30), and calendar formats.
          </p>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div className="flex items-start gap-3 rounded-xl border border-slate-200 p-4 dark:border-slate-800">
          <DollarSign className="h-5 w-5 text-emerald-600 mt-0.5" />
          <div>
            <h3 className="text-xs font-bold text-slate-900 dark:text-white">Default Currency</h3>
            <p className="mt-1 text-xs text-slate-500">Indian Rupee (INR - ₹) with 2 decimal precision.</p>
          </div>
        </div>

        <div className="flex items-start gap-3 rounded-xl border border-slate-200 p-4 dark:border-slate-800">
          <Clock className="h-5 w-5 text-indigo-600 mt-0.5" />
          <div>
            <h3 className="text-xs font-bold text-slate-900 dark:text-white">Institutional Timezone</h3>
            <p className="mt-1 text-xs text-slate-500">Asia/Kolkata (GMT+05:30 Indian Standard Time).</p>
          </div>
        </div>

        <div className="flex items-start gap-3 rounded-xl border border-slate-200 p-4 dark:border-slate-800">
          <Calendar className="h-5 w-5 text-blue-600 mt-0.5" />
          <div>
            <h3 className="text-xs font-bold text-slate-900 dark:text-white">Fiscal Cycle Schedule</h3>
            <p className="mt-1 text-xs text-slate-500">Financial year begins 1st April; Academic year begins 1st June.</p>
          </div>
        </div>

        <div className="flex items-start gap-3 rounded-xl border border-slate-200 p-4 dark:border-slate-800">
          <Globe className="h-5 w-5 text-amber-600 mt-0.5" />
          <div>
            <h3 className="text-xs font-bold text-slate-900 dark:text-white">Default Language</h3>
            <p className="mt-1 text-xs text-slate-500">English (India) with Hindi localized font support.</p>
          </div>
        </div>
      </div>
    </div>
  );
};
