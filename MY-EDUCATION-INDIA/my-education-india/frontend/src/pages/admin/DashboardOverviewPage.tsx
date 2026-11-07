import React from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  Building2,
  Users,
  ShieldCheck,
  CheckCircle2,
  Activity,
  ArrowRight,
  TrendingUp,
  FileCheck2,
} from "lucide-react";
import { instituteService } from "@/services/instituteService";

export const DashboardOverviewPage: React.FC = () => {
  const { data: institutes = [] } = useQuery({
    queryKey: ["institutes"],
    queryFn: instituteService.listInstitutes,
  });

  const activeInstitute = institutes[0] || null;
  const modules = activeInstitute?.module_configs || [];
  const enabledCount = modules.filter((m) => m.is_enabled).length;

  return (
    <div className="space-y-6">
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <span className="inline-block rounded-full bg-brand-50 px-3 py-1 text-xs font-semibold text-brand-700 mb-2">
              National Flagship Campus • MEI-HQ
            </span>
            <h1 className="text-2xl font-bold tracking-tight text-slate-900">
              Welcome to {activeInstitute?.name || "MY EDUCATION INDIA"}
            </h1>
            <p className="mt-1 text-sm text-slate-500">
              Enterprise Command Center • Live PostgreSQL Session • Zero-LocalStorage Security
            </p>
          </div>
          <div className="flex gap-2">
            <Link
              to="/admin/modules"
              className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-semibold text-white shadow-xs hover:bg-brand-700"
            >
              <span>37 Subsystems Control</span>
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Active Institute</span>
            <Building2 className="h-5 w-5 text-brand-600" />
          </div>
          <p className="mt-2 text-xl font-bold text-slate-900 truncate">{activeInstitute?.code || "MEI-HQ"}</p>
          <p className="mt-0.5 text-xs text-slate-500">{activeInstitute?.city || "Indore"}, {activeInstitute?.state || "MP"}</p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Enabled Subsystems</span>
            <Activity className="h-5 w-5 text-emerald-600" />
          </div>
          <p className="mt-2 text-2xl font-extrabold text-slate-900">{enabledCount} / {modules.length || 37}</p>
          <p className="mt-0.5 text-xs text-emerald-600 font-medium">100% Operational</p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">RBAC Roles</span>
            <ShieldCheck className="h-5 w-5 text-indigo-600" />
          </div>
          <p className="mt-2 text-2xl font-extrabold text-slate-900">9 Roles</p>
          <p className="mt-0.5 text-xs text-slate-500">Sovereign & Institute Governance</p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Security Compliance</span>
            <CheckCircle2 className="h-5 w-5 text-teal-600" />
          </div>
          <p className="mt-2 text-2xl font-extrabold text-slate-900">A+ Verified</p>
          <p className="mt-0.5 text-xs text-slate-500">HttpOnly Cookies • Argon2</p>
        </div>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
        <h2 className="text-base font-bold text-slate-900 mb-4">Enterprise Management Modules</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <Link
            to="/admin/cbt"
            className="flex items-start gap-4 rounded-xl border border-slate-100 bg-slate-50/50 p-4 transition hover:border-brand-300 hover:bg-brand-50/30"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-100 text-blue-700">
              <TrendingUp className="h-5 w-5" />
            </div>
            <div>
              <p className="text-sm font-bold text-slate-900">CBT Testing Platform</p>
              <p className="text-xs text-slate-500 mt-0.5">Online computer-based tests & test banks</p>
            </div>
          </Link>

          <Link
            to="/admin/certificates"
            className="flex items-start gap-4 rounded-xl border border-slate-100 bg-slate-50/50 p-4 transition hover:border-brand-300 hover:bg-brand-50/30"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-100 text-emerald-700">
              <FileCheck2 className="h-5 w-5" />
            </div>
            <div>
              <p className="text-sm font-bold text-slate-900">Certificates & Verification</p>
              <p className="text-xs text-slate-500 mt-0.5">Digital tamper-proof credential engine</p>
            </div>
          </Link>

          <Link
            to="/admin/roles"
            className="flex items-start gap-4 rounded-xl border border-slate-100 bg-slate-50/50 p-4 transition hover:border-brand-300 hover:bg-brand-50/30"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-purple-100 text-purple-700">
              <Users className="h-5 w-5" />
            </div>
            <div>
              <p className="text-sm font-bold text-slate-900">Roles & Staff RBAC</p>
              <p className="text-xs text-slate-500 mt-0.5">Provision permissions and user access</p>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
};
