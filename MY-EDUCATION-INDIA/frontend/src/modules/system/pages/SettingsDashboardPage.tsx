import React from "react";
import { Link } from "react-router-dom";
import {
  Building2,
  GitBranch,
  CalendarDays,
  Coins,
  Binary,
  KeyRound,
  Palette,
  Sliders,
  ShieldCheck,
} from "lucide-react";

const SETTINGS_SECTIONS = [
  {
    title: "Institute Management",
    description: "Manage multi-institute branding, parent entities, and accreditation profiles.",
    icon: Building2,
    to: "/admin/settings/institutes",
    color: "bg-blue-50 text-blue-600 dark:bg-blue-950 dark:text-blue-400",
  },
  {
    title: "Branch Management",
    description: "Create and govern regional branches, campuses, working hours, and principals.",
    icon: GitBranch,
    to: "/admin/settings/branches",
    color: "bg-teal-50 text-teal-600 dark:bg-teal-950 dark:text-teal-400",
  },
  {
    title: "Academic Year Management",
    description: "Configure academic sessions, start/end dates, locking, and session promotions.",
    icon: CalendarDays,
    to: "/admin/settings/academic-years",
    color: "bg-indigo-50 text-indigo-600 dark:bg-indigo-950 dark:text-indigo-400",
  },
  {
    title: "Financial Year Management",
    description: "Manage fiscal years, GSTIN mapping, audit locking, and accounting books.",
    icon: Coins,
    to: "/admin/settings/financial-years",
    color: "bg-emerald-50 text-emerald-600 dark:bg-emerald-950 dark:text-emerald-400",
  },
  {
    title: "Universal Number Generator",
    description: "Configure custom token numbering formats ({PREFIX}-{BRANCH}-{YEAR}-{NUMBER}) with live preview.",
    icon: Binary,
    to: "/admin/settings/number-generator",
    color: "bg-purple-50 text-purple-600 dark:bg-purple-950 dark:text-purple-400",
  },
  {
    title: "Authentication Settings",
    description: "Set allowed login criteria (Roll No, ERP ID, Mobile), lockout limits, and password policies.",
    icon: KeyRound,
    to: "/admin/settings/authentication",
    color: "bg-amber-50 text-amber-600 dark:bg-amber-950 dark:text-amber-400",
  },
  {
    title: "Appearance Settings",
    description: "Customise theme palettes, primary/secondary colors, typography, and dark mode.",
    icon: Palette,
    to: "/admin/settings/appearance",
    color: "bg-rose-50 text-rose-600 dark:bg-rose-950 dark:text-rose-400",
  },
  {
    title: "General Settings",
    description: "Default currency (INR), language, Indian timezone (+05:30), date formats, and fiscal starts.",
    icon: Sliders,
    to: "/admin/settings/general",
    color: "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300",
  },
];

export const SettingsDashboardPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs dark:border-slate-800 dark:bg-slate-900">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-600 text-white shadow-xs">
            <ShieldCheck className="h-6 w-6" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-slate-900 dark:text-white">
              Core System Engine & Configuration Hub
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Module 3: Multi-Institute, Multi-Branch, Universal Numbering, and Dynamic Configuration Architecture.
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {SETTINGS_SECTIONS.map((sec) => {
          const IconComponent = sec.icon;
          return (
            <Link
              key={sec.to}
              to={sec.to}
              className="flex flex-col justify-between rounded-2xl border border-slate-200 bg-white p-5 shadow-xs transition hover:border-brand-500 hover:shadow-md dark:border-slate-800 dark:bg-slate-900"
            >
              <div>
                <div className={`flex h-10 w-10 items-center justify-center rounded-xl ${sec.color}`}>
                  <IconComponent className="h-5 w-5" />
                </div>
                <h2 className="mt-4 text-sm font-bold text-slate-900 dark:text-white">
                  {sec.title}
                </h2>
                <p className="mt-1 text-xs leading-relaxed text-slate-500 dark:text-slate-400">
                  {sec.description}
                </p>
              </div>
              <span className="mt-4 inline-block text-xs font-semibold text-brand-600 hover:text-brand-500 dark:text-brand-400">
                Configure →
              </span>
            </Link>
          );
        })}
      </div>
    </div>
  );
};
