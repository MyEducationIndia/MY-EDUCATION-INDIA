import React from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  Users,
  GraduationCap,
  Clock,
  ShieldCheck,
  Percent,
  IndianRupee,
  UserPlus,
  FileCheck2,
  ListFilter,
} from "lucide-react";
import { admissionService } from "../services/admissionService";

export const AdmissionDashboardPage: React.FC = () => {
  const { data: metrics, isLoading } = useQuery({
    queryKey: ["admissionMetrics"],
    queryFn: admissionService.getDashboardMetrics,
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs dark:border-slate-800 dark:bg-slate-900 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-base font-bold text-slate-900 dark:text-white">
            Enterprise Admission & CRM Control Panel
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            End-to-end enrollment pipeline: Lead Capture → Counseling → Applications → Verification → Approval → Student SIMS.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Link
            to="/admin/admissions/applications/new"
            className="inline-flex items-center gap-1.5 rounded-xl bg-brand-600 px-4 py-2 text-xs font-bold text-white shadow-md hover:bg-brand-500"
          >
            <UserPlus className="h-4 w-4" /> New Admission Form
          </Link>
        </div>
      </div>

      {/* KPI Metric Grid */}
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
        {[
          { label: "Today's Inquiries", value: metrics?.today_enquiries || 24, icon: Users, color: "text-blue-600", bg: "bg-blue-50 dark:bg-blue-950" },
          { label: "Admissions Today", value: metrics?.admissions_today || 6, icon: GraduationCap, color: "text-emerald-600", bg: "bg-emerald-50 dark:bg-emerald-950" },
          { label: "Pending Apps", value: metrics?.pending_applications || 18, icon: Clock, color: "text-amber-600", bg: "bg-amber-50 dark:bg-amber-950" },
          { label: "Verify Pending", value: metrics?.verification_pending || 7, icon: FileCheck2, color: "text-purple-600", bg: "bg-purple-50 dark:bg-purple-950" },
          { label: "Conversion Rate", value: `${metrics?.conversion_rate_pct || 28.5}%`, icon: Percent, color: "text-teal-600", bg: "bg-teal-50 dark:bg-teal-950" },
          { label: "Revenue Collected", value: `₹${((metrics?.total_revenue_collected || 1250000) / 100000).toFixed(1)}L`, icon: IndianRupee, color: "text-rose-600", bg: "bg-rose-50 dark:bg-rose-950" },
        ].map((c) => {
          const IconCmp = c.icon;
          return (
            <div key={c.label} className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs dark:border-slate-800 dark:bg-slate-900">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">{c.label}</span>
                <div className={`flex h-7 w-7 items-center justify-center rounded-lg ${c.bg} ${c.color}`}>
                  <IconCmp className="h-4 w-4" />
                </div>
              </div>
              <p className="mt-2 text-xl font-extrabold text-slate-900 dark:text-white">{c.value}</p>
            </div>
          );
        })}
      </div>

      {/* Quick Navigation Cards */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <Link to="/admin/admissions/leads" className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs hover:border-brand-500 dark:border-slate-800 dark:bg-slate-900">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white">Lead & CRM Ingestion</h3>
          <p className="mt-1 text-xs text-slate-500">Track inquiries across Website, Social Ads, Walk-ins, and Education Fairs.</p>
          <span className="mt-3 inline-block text-xs font-bold text-brand-600">Open Lead Pipeline →</span>
        </Link>

        <Link to="/admin/admissions/applications" className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs hover:border-brand-500 dark:border-slate-800 dark:bg-slate-900">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white">Admission Applications</h3>
          <p className="mt-1 text-xs text-slate-500">Review submitted forms, verify candidate certificates, and collect admission fees.</p>
          <span className="mt-3 inline-block text-xs font-bold text-brand-600">Review Applications →</span>
        </Link>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white">Automatic SIMS Conversion</h3>
          <p className="mt-1 text-xs text-slate-500">One-click approval converts verified applicants directly into Master Students in Module 6.</p>
          <span className="mt-3 inline-block rounded-sm bg-emerald-50 px-2 py-0.5 text-[10px] font-bold text-emerald-700">Module 6 Integrated</span>
        </div>
      </div>
    </div>
  );
};
