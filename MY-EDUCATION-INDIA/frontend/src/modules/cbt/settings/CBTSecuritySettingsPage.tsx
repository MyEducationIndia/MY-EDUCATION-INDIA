import React, { useState } from "react";
import { Sliders, Save, ShieldAlert } from "lucide-react";

export const CBTSecuritySettingsPage: React.FC = () => {
  const [fullscreen, setFullscreen] = useState(true);
  const [disableCopy, setDisableCopy] = useState(true);
  const [maxWarnings, setMaxWarnings] = useState(3);

  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-5 dark:border-slate-800">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
          <ShieldAlert className="h-7 w-7 text-cyan-600 dark:text-cyan-400" />
          CBT Secure Browser & Proctoring Policies
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Configure copy-paste restrictions, full-screen lockdown, tab-switching tolerance, and automatic disqualifications.
        </p>
      </div>

      <div className="max-w-2xl rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs space-y-4">
        <label className="flex items-center gap-3 text-sm font-semibold text-slate-800 dark:text-slate-200">
          <input
            type="checkbox"
            checked={fullscreen}
            onChange={(e) => setFullscreen(e.target.checked)}
            className="h-4 w-4 rounded-sm text-cyan-600 focus:ring-cyan-500"
          />
          <span>Enforce Full-Screen Lockdown Mode</span>
        </label>

        <label className="flex items-center gap-3 text-sm font-semibold text-slate-800 dark:text-slate-200">
          <input
            type="checkbox"
            checked={disableCopy}
            onChange={(e) => setDisableCopy(e.target.checked)}
            className="h-4 w-4 rounded-sm text-cyan-600 focus:ring-cyan-500"
          />
          <span>Disable Right-Click, Copy, Cut, and Paste</span>
        </label>

        <div>
          <label className="block text-xs font-bold uppercase text-slate-400 mb-1">Max Tab-Switch Warnings Before Disqualification</label>
          <input
            type="number"
            value={maxWarnings}
            onChange={(e) => setMaxWarnings(Number(e.target.value))}
            className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 py-2 px-3 text-sm font-bold"
          />
        </div>

        <button
          type="button"
          onClick={() => alert("Security policies updated successfully!")}
          className="flex items-center gap-2 rounded-lg bg-cyan-600 px-4 py-2 text-xs font-bold text-white shadow-xs hover:bg-cyan-700 transition"
        >
          <Save className="h-4 w-4" />
          <span>Save Security Policies</span>
        </button>
      </div>
    </div>
  );
};
