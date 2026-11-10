import React from "react";
import { WifiOff, CheckCircle2, ShieldCheck, RefreshCw } from "lucide-react";

export const OfflineSyncStatusPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-5 dark:border-slate-800">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
          <WifiOff className="h-7 w-7 text-cyan-600 dark:text-cyan-400" />
          Offline LAN Synchronization & Checksum Verification
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Monitor campus LAN test server batch uploads, data integrity hashes, and conflict reconciliation.
        </p>
      </div>

      <div className="rounded-xl border border-emerald-200 dark:border-emerald-900/60 bg-emerald-50 dark:bg-emerald-950/20 p-4 flex items-center gap-3">
        <CheckCircle2 className="h-6 w-6 text-emerald-600 dark:text-emerald-400 shrink-0" />
        <div>
          <h3 className="text-sm font-bold text-emerald-900 dark:text-emerald-200">Local LAN Node Synchronized</h3>
          <p className="text-xs text-emerald-700 dark:text-emerald-300">
            All 64 offline candidate test logs verified against cloud database with zero checksum discrepancies.
          </p>
        </div>
      </div>
    </div>
  );
};
