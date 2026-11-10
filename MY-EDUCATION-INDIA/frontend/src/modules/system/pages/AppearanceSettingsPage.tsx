import React from "react";
import { Palette, Check } from "lucide-react";
import { useAuth } from "@/modules/auth/context/AuthContext";

export const AppearanceSettingsPage: React.FC = () => {
  const { isDarkMode, toggleDarkMode } = useAuth();

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs dark:border-slate-800 dark:bg-slate-900">
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-rose-50 text-rose-600 dark:bg-rose-950 dark:text-rose-400">
          <Palette className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-base font-bold text-slate-900 dark:text-white">
            Institutional Appearance & Themes
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Configure institutional color palettes, dark mode, typography, and sidebar styles without code modification.
          </p>
        </div>
      </div>

      <div className="mt-6 space-y-6">
        <div>
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300">
            Visual Theme Mode
          </h2>
          <div className="mt-3 flex items-center gap-4">
            <button
              type="button"
              onClick={toggleDarkMode}
              className={`flex items-center gap-3 rounded-xl border p-4 transition ${
                !isDarkMode
                  ? "border-brand-600 bg-brand-50/50 text-brand-900"
                  : "border-slate-200 dark:border-slate-800 dark:text-slate-300"
              }`}
            >
              <span className="h-4 w-4 rounded-full bg-white border border-slate-400" />
              <span className="text-xs font-bold">Standard Light Mode</span>
            </button>

            <button
              type="button"
              onClick={toggleDarkMode}
              className={`flex items-center gap-3 rounded-xl border p-4 transition ${
                isDarkMode
                  ? "border-brand-500 bg-brand-950/60 text-white"
                  : "border-slate-200 dark:border-slate-800 dark:text-slate-300"
              }`}
            >
              <span className="h-4 w-4 rounded-full bg-slate-900 border border-slate-600" />
              <span className="text-xs font-bold">Dark Contrast Mode</span>
            </button>
          </div>
        </div>

        <div>
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300">
            Brand Accent Colors
          </h2>
          <div className="mt-3 flex items-center gap-3">
            <div className="flex items-center gap-2 rounded-xl border border-slate-200 p-3 dark:border-slate-800">
              <span className="h-6 w-6 rounded-full bg-blue-700 shadow-xs" />
              <span className="font-mono text-xs text-slate-700 dark:text-slate-300">#1D4ED8 (Primary)</span>
            </div>
            <div className="flex items-center gap-2 rounded-xl border border-slate-200 p-3 dark:border-slate-800">
              <span className="h-6 w-6 rounded-full bg-teal-600 shadow-xs" />
              <span className="font-mono text-xs text-slate-700 dark:text-slate-300">#0D9488 (Secondary)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
