import React from "react";
import { ShieldAlert, Key, Lock, Server, Terminal, AlertOctagon, RotateCcw, Copy, CheckCircle2 } from "lucide-react";

export const RootOwnerConsolePage: React.FC = () => {
  return (
    <div className="p-6 space-y-6 bg-slate-900 text-slate-100 min-h-screen">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <ShieldAlert className="w-6 h-6 text-amber-400" />
            <h1 className="text-2xl font-bold tracking-tight text-white">System Root Owner Master Console</h1>
          </div>
          <p className="text-xs text-slate-400 mt-1">Tier-0 Sovereign Authority. Above Super Admin. Permanent non-deletable platform ownership.</p>
        </div>
        <div className="flex items-center gap-2 bg-amber-500/10 border border-amber-500/20 px-3 py-1.5 rounded-lg text-amber-400 text-xs font-mono">
          ROOT_OWNER SESSION: ACTIVE
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-slate-800/60 p-5 rounded-xl border border-slate-700">
          <div className="flex justify-between items-center text-xs text-slate-400 font-semibold uppercase">
            Emergency Lockdown
            <AlertOctagon className="w-5 h-5 text-red-400" />
          </div>
          <div className="text-xl font-bold text-emerald-400 mt-2">Disarmed (Normal)</div>
          <span className="text-xs text-slate-500">1-click complete ERP freeze</span>
        </div>

        <div className="bg-slate-800/60 p-5 rounded-xl border border-slate-700">
          <div className="flex justify-between items-center text-xs text-slate-400 font-semibold uppercase">
            Global Encryption
            <Key className="w-5 h-5 text-indigo-400" />
          </div>
          <div className="text-xl font-bold text-white mt-2">AES-256 GCM</div>
          <span className="text-xs text-indigo-400">Master Secret Intact</span>
        </div>

        <div className="bg-slate-800/60 p-5 rounded-xl border border-slate-700">
          <div className="flex justify-between items-center text-xs text-slate-400 font-semibold uppercase">
            Platform Clone Token
            <Copy className="w-5 h-5 text-blue-400" />
          </div>
          <div className="text-xl font-bold text-white mt-2">READY</div>
          <span className="text-xs text-blue-400">Multi-tenant clone token</span>
        </div>

        <div className="bg-slate-800/60 p-5 rounded-xl border border-slate-700">
          <div className="flex justify-between items-center text-xs text-slate-400 font-semibold uppercase">
            Developer Mode
            <Terminal className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="text-xl font-bold text-emerald-400 mt-2">ENABLED</div>
          <span className="text-xs text-slate-500">Telemetry & Debug on</span>
        </div>
      </div>
    </div>
  );
};
