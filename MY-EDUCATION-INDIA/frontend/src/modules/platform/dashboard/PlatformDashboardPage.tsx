import React from "react";
import { Server, Database, ShieldCheck, HardDrive, Cpu, Play, CheckCircle2, AlertTriangle, KeyRound } from "lucide-react";

export const PlatformDashboardPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Platform Administration & Operations Command</h1>
          <p className="text-sm text-gray-500 mt-1">Multi-tenant cluster governance, automated backups, security policies, and feature flags</p>
        </div>
        <div className="flex items-center gap-2 bg-emerald-50 text-emerald-700 px-4 py-2 rounded-xl border border-emerald-200">
          <CheckCircle2 className="w-5 h-5 text-emerald-600" />
          <span className="text-xs font-bold uppercase tracking-wider">Cluster: All Systems Operational (99.98%)</span>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Database Status</span>
            <div className="p-2 bg-indigo-50 text-indigo-600 rounded-lg"><Database className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">PostgreSQL Neon</div>
          <span className="text-xs text-emerald-600 font-medium">14 Active Pools · 6.5ms latency</span>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Storage Pool</span>
            <div className="p-2 bg-blue-50 text-blue-600 rounded-lg"><HardDrive className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">42.8 / 500 GB</div>
          <span className="text-xs text-blue-600 font-medium">8.5% Quota Consumed</span>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Disaster Recovery</span>
            <div className="p-2 bg-emerald-50 text-emerald-600 rounded-lg"><Server className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">Nightly Verified</div>
          <span className="text-xs text-emerald-600 font-medium">SHA-256 Checksum Intact</span>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">License & Security</span>
            <div className="p-2 bg-purple-50 text-purple-600 rounded-lg"><KeyRound className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">Enterprise Lifetime</div>
          <span className="text-xs text-purple-600 font-medium">Tier 1 Security Enforced</span>
        </div>
      </div>
    </div>
  );
};
