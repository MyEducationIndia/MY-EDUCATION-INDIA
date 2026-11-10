import React from "react";
import { Link } from "react-router-dom";
import { Clock, ArrowUpRight } from "lucide-react";
import { DashboardActivityItem } from "../types/dashboard.types";

interface ActivityTimelineWidgetProps {
  activities: DashboardActivityItem[];
}

export const ActivityTimelineWidget: React.FC<ActivityTimelineWidgetProps> = ({ activities }) => {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900">
      <div className="flex items-center justify-between">
        <h2 className="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300">
          Live Enterprise Activity Timeline
        </h2>
        <Link to="/admin/audit-logs" className="text-xs font-semibold text-brand-600 hover:text-brand-500 dark:text-brand-400">
          View All Logs →
        </Link>
      </div>

      <div className="mt-4 space-y-3">
        {activities.map((act) => (
          <div key={act.id} className="flex items-start gap-3 rounded-xl border border-slate-100 p-3 dark:border-slate-800/80 dark:bg-slate-950/40">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300 shrink-0">
              <Clock className="h-4 w-4" />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-900 dark:text-white truncate">{act.actor_name}</span>
                <span className="text-[10px] text-slate-400 font-mono">
                  {new Date(act.occurred_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                </span>
              </div>
              <p className="mt-0.5 text-xs text-slate-600 dark:text-slate-400">{act.summary}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
