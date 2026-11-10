import React from "react";
import { TrendingUp, Award, ShieldCheck } from "lucide-react";

export const CertificateAnalyticsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-5 dark:border-slate-800">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
          <TrendingUp className="h-7 w-7 text-teal-600 dark:text-teal-400" />
          Credential Issuance & Public Verification Analytics
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Monthly credential generation volume, employer verification trends, and document classification metrics.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <span className="text-xs font-bold uppercase text-slate-400">Monthly Issuance Growth</span>
          <p className="mt-2 text-2xl font-black text-teal-600">+42%</p>
          <span className="text-xs text-slate-500">Graduation semester surge</span>
        </div>
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <span className="text-xs font-bold uppercase text-slate-400">Verification Rate</span>
          <p className="mt-2 text-2xl font-black text-emerald-600">2.8x</p>
          <span className="text-xs text-slate-500">Average verifications per credential</span>
        </div>
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <span className="text-xs font-bold uppercase text-slate-400">Revocation Ratio</span>
          <p className="mt-2 text-2xl font-black text-rose-500">0.57%</p>
          <span className="text-xs text-slate-500">3 revoked out of 520 issued</span>
        </div>
      </div>
    </div>
  );
};
