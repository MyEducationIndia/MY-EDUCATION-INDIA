import React from "react";
import { Server, Database, HardDrive, Cpu } from "lucide-react";
import { SystemHealthData } from "../types/dashboard.types";

interface SystemHealthWidgetProps {
  health: SystemHealthData;
}

export const SystemHealthWidget: React.FC<SystemHealthWidgetProps> = ({ health }) => {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900">
      <h2 className="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300">
        Infrastructure & Server Health
      </h2>

      <div className="mt-4 grid grid-cols-2 gap-3 text-xs">
        <div className="rounded-xl border border-slate-200 p-3 dark:border-slate-800">
          <div className="flex items-center gap-2 text-slate-500">
            <Database className="h-4 w-4 text-emerald-600" />
            <span>Database</span>
          </div>
          <p className="mt-1 font-bold text-slate-900 dark:text-white">{health.database_status}</p>
          <p className="text-[10px] text-slate-400">{health.database_version}</p>
        </div>

        <div className="rounded-xl border border-slate-200 p-3 dark:border-slate-800">
          <div className="flex items-center gap-2 text-slate-500">
            <Server className="h-4 w-4 text-blue-600" />
            <span>API Gateway</span>
          </div>
          <p className="mt-1 font-bold text-slate-900 dark:text-white">{health.api_status}</p>
          <p className="text-[10px] text-slate-400">Uptime: {(health.uptime_seconds / 3600).toFixed(1)} hrs</p>
        </div>

        <div className="rounded-xl border border-slate-200 p-3 dark:border-slate-800">
          <div className="flex items-center gap-2 text-slate-500">
            <Cpu className="h-4 w-4 text-purple-600" />
            <span>Memory Usage</span>
          </div>
          <p className="mt-1 font-bold text-slate-900 dark:text-white">{health.memory_usage_mb} MB</p>
          <p className="text-[10px] text-slate-400">Total: {health.total_memory_mb} MB</p>
        </div>

        <div className="rounded-xl border border-slate-200 p-3 dark:border-slate-800">
          <div className="flex items-center gap-2 text-slate-500">
            <HardDrive className="h-4 w-4 text-amber-600" />
            <span>Storage Usage</span>
          </div>
          <p className="mt-1 font-bold text-slate-900 dark:text-white">{health.storage_usage_mb} MB</p>
          <p className="text-[10px] text-slate-400">Version: v{health.app_version}</p>
        </div>
      </div>
    </div>
  );
};
