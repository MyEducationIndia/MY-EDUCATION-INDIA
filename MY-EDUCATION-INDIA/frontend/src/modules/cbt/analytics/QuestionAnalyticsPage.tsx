import React from "react";
import { TrendingUp, BarChart2 } from "lucide-react";

export const QuestionAnalyticsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-5 dark:border-slate-800">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
          <TrendingUp className="h-7 w-7 text-cyan-600 dark:text-cyan-400" />
          Item Response Theory (IRT) & Question Analytics
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Difficulty index (P-value), item discrimination index (D-value), and distracter efficiency metrics.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <span className="text-xs font-bold uppercase text-slate-400">Average Difficulty Index</span>
          <p className="mt-2 text-2xl font-black text-slate-900 dark:text-white">0.68</p>
          <span className="text-xs text-emerald-600">Optimal difficulty balance</span>
        </div>
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <span className="text-xs font-bold uppercase text-slate-400">Discrimination Index (D)</span>
          <p className="mt-2 text-2xl font-black text-cyan-600">0.42</p>
          <span className="text-xs text-slate-500">Strong high/low ability separation</span>
        </div>
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <span className="text-xs font-bold uppercase text-slate-400">Average Time Spent</span>
          <p className="mt-2 text-2xl font-black text-purple-600">54s / Question</p>
          <span className="text-xs text-slate-500">Across 2,450 attempts</span>
        </div>
      </div>
    </div>
  );
};
