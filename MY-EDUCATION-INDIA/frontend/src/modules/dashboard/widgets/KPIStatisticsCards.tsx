import React from "react";
import {
  Users,
  GraduationCap,
  Briefcase,
  BookOpen,
  Layers,
  IndianRupee,
  Activity,
  Award,
  Globe,
  Radio,
} from "lucide-react";
import { DashboardKPIStats } from "../types/dashboard.types";

interface KPIStatisticsCardsProps {
  stats: DashboardKPIStats;
}

export const KPIStatisticsCards: React.FC<KPIStatisticsCardsProps> = ({ stats }) => {
  const cards = [
    { label: "Total Students", value: stats.total_students.toLocaleString(), icon: Users, color: "text-blue-600", bg: "bg-blue-50 dark:bg-blue-950" },
    { label: "Active Students", value: stats.active_students.toLocaleString(), icon: GraduationCap, color: "text-emerald-600", bg: "bg-emerald-50 dark:bg-emerald-950" },
    { label: "Admissions Today", value: stats.admissions_today.toString(), icon: Briefcase, color: "text-indigo-600", bg: "bg-indigo-50 dark:bg-indigo-950" },
    { label: "Fee Collection Today", value: `₹${(stats.fee_collection_today / 1000).toFixed(1)}k`, icon: IndianRupee, color: "text-teal-600", bg: "bg-teal-50 dark:bg-teal-950" },
    { label: "Pending Fees", value: `₹${(stats.pending_fees_total / 1000).toFixed(0)}k`, icon: IndianRupee, color: "text-rose-600", bg: "bg-rose-50 dark:bg-rose-950" },
    { label: "Overall Attendance", value: `${stats.overall_attendance_pct}%`, icon: Activity, color: "text-purple-600", bg: "bg-purple-50 dark:bg-purple-950" },
    { label: "Total Faculty", value: stats.total_faculty.toString(), icon: Briefcase, color: "text-cyan-600", bg: "bg-cyan-50 dark:bg-cyan-950" },
    { label: "Courses / Programs", value: stats.total_courses.toString(), icon: BookOpen, color: "text-amber-600", bg: "bg-amber-50 dark:bg-amber-950" },
    { label: "Active Batches", value: stats.total_batches.toString(), icon: Layers, color: "text-blue-600", bg: "bg-blue-50 dark:bg-blue-950" },
    { label: "Certificates Issued", value: stats.certificates_issued.toString(), icon: Award, color: "text-emerald-600", bg: "bg-emerald-50 dark:bg-emerald-950" },
    { label: "Website Visitors", value: stats.website_visitors_today.toLocaleString(), icon: Globe, color: "text-indigo-600", bg: "bg-indigo-50 dark:bg-indigo-950" },
    { label: "Broadcasts Dispatched", value: (stats.sms_sent_count + stats.whatsapp_sent_count + stats.emails_sent_count).toLocaleString(), icon: Radio, color: "text-teal-600", bg: "bg-teal-50 dark:bg-teal-950" },
  ];

  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
      {cards.map((c) => {
        const IconComponent = c.icon;
        return (
          <div
            key={c.label}
            className="flex flex-col justify-between rounded-2xl border border-slate-200 bg-white p-4 shadow-xs transition hover:border-slate-300 dark:border-slate-800 dark:bg-slate-900"
          >
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                {c.label}
              </span>
              <div className={`flex h-7 w-7 items-center justify-center rounded-lg ${c.bg} ${c.color}`}>
                <IconComponent className="h-4 w-4" />
              </div>
            </div>
            <p className="mt-2 text-xl font-extrabold tracking-tight text-slate-900 dark:text-white">
              {c.value}
            </p>
          </div>
        );
      })}
    </div>
  );
};
