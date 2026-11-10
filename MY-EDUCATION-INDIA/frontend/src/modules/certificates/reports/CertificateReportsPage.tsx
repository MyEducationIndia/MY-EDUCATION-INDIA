import React from "react";
import { Download, FileBadge, TrendingUp } from "lucide-react";

export const CertificateReportsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <FileBadge className="h-7 w-7 text-teal-600 dark:text-teal-400" />
            Institutional Credential Registers & Audit Logs
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Export official degree issuance registers, revoked document ledgers, and public verification logs.
          </p>
        </div>
        <button
          type="button"
          onClick={() => alert("Export Excel")}
          className="flex items-center gap-2 rounded-lg bg-teal-600 px-4 py-2 text-xs font-bold text-white hover:bg-teal-700 transition"
        >
          <Download className="h-4 w-4" />
          <span>Export Issuance Register</span>
        </button>
      </div>

      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs">
        <h3 className="text-sm font-bold text-slate-900 dark:text-white mb-2">Permanent Audit Immutability</h3>
        <p className="text-xs text-slate-500 leading-relaxed">
          Every generated degree, transcript, and certificate receives a permanently registered serial number and cryptographic verification token that can never be purged from the institutional audit history.
        </p>
      </div>
    </div>
  );
};
