import React from "react";
import { Activity, ShieldCheck, Zap, Globe, Cpu, ArrowUpRight, CheckCircle2, AlertTriangle } from "lucide-react";

export const ApiDashboardPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 tracking-tight">API Integration Manager & Provider Hub</h1>
          <p className="text-sm text-gray-500 mt-1">Universal API orchestration, credential vault, circuit breakers, and rate limit telemetry</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">24h API Dispatches</span>
            <div className="p-2 bg-indigo-50 text-indigo-600 rounded-lg"><Activity className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">14,820 Calls</div>
          <span className="text-xs text-emerald-600 font-medium">99.4% Success Rate</span>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Avg Gateway Latency</span>
            <div className="p-2 bg-blue-50 text-blue-600 rounded-lg"><Zap className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">164.2 ms</div>
          <span className="text-xs text-blue-600 font-medium">p95: 320 ms</span>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Credential Vault</span>
            <div className="p-2 bg-emerald-50 text-emerald-600 rounded-lg"><ShieldCheck className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">12 Encrypted Keys</div>
          <span className="text-xs text-emerald-600 font-medium">AES-256 Vault Active</span>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Circuit Breakers</span>
            <div className="p-2 bg-purple-50 text-purple-600 rounded-lg"><Cpu className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">All Healthy</div>
          <span className="text-xs text-purple-600 font-medium">0 Breakers Tripped</span>
        </div>
      </div>
    </div>
  );
};
