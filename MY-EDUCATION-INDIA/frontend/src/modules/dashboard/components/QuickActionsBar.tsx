import React from "react";
import { Link } from "react-router-dom";
import {
  UserPlus,
  GraduationCap,
  CreditCard,
  Award,
  Send,
  Database,
  Globe,
  FileSpreadsheet,
} from "lucide-react";

const QUICK_ACTIONS = [
  { label: "Add Student", icon: UserPlus, to: "/admin/users", color: "bg-blue-600 hover:bg-blue-500" },
  { label: "New Admission", icon: GraduationCap, to: "/admin/users", color: "bg-emerald-600 hover:bg-emerald-500" },
  { label: "Collect Fees", icon: CreditCard, to: "/admin/settings", color: "bg-teal-600 hover:bg-teal-500" },
  { label: "Issue Certificate", icon: Award, to: "/admin/settings/number-generator", color: "bg-purple-600 hover:bg-purple-500" },
  { label: "Send Broadcast", icon: Send, to: "/admin/settings", color: "bg-amber-600 hover:bg-amber-500" },
  { label: "Backup Database", icon: Database, to: "/admin/settings", color: "bg-slate-700 hover:bg-slate-600" },
  { label: "Website CMS", icon: Globe, to: "/admin/dashboard", color: "bg-indigo-600 hover:bg-indigo-500" },
  { label: "Generate Report", icon: FileSpreadsheet, to: "/admin/audit-logs", color: "bg-rose-600 hover:bg-rose-500" },
];

export const QuickActionsBar: React.FC = () => {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900">
      <h2 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
        Enterprise Quick Actions
      </h2>
      <div className="mt-3 grid grid-cols-2 gap-2.5 sm:grid-cols-4 lg:grid-cols-8">
        {QUICK_ACTIONS.map((action) => {
          const IconComponent = action.icon;
          return (
            <Link
              key={action.label}
              to={action.to}
              className={`flex flex-col items-center justify-center rounded-xl p-3 text-white shadow-xs transition ${action.color}`}
            >
              <IconComponent className="h-5 w-5" />
              <span className="mt-1.5 text-center text-xs font-semibold leading-tight">{action.label}</span>
            </Link>
          );
        })}
      </div>
    </div>
  );
};
