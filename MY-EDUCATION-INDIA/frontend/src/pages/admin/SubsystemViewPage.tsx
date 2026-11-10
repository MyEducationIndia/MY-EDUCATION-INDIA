import React from "react";
import { Link } from "react-router-dom";
import {
  FileBadge,
  MonitorPlay,
  Award,
  CalendarCheck,
  IndianRupee,
  BookOpen,
  ClipboardList,
  GraduationCap,
  Globe,
  Sliders,
  CheckCircle2,
  Clock,
  Layers,
} from "lucide-react";

interface SubsystemCardProps {
  title: string;
  category: string;
  description: string;
  icon: React.ComponentType<{ className?: string }>;
  features: string[];
  subdomain: string;
  status: "ACTIVE" | "CORE_LOCKED" | "ENTERPRISE";
}

export const SubsystemViewPage: React.FC<SubsystemCardProps> = ({
  title,
  category,
  description,
  icon: Icon,
  features,
  subdomain,
  status,
}) => {
  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-50 text-brand-600">
              <Icon className="h-6 w-6" />
            </div>
            <div>
              <div className="flex items-center gap-2.5">
                <h1 className="text-xl font-bold text-slate-900">{title}</h1>
                <span className="rounded-full bg-emerald-100 px-2.5 py-0.5 text-[11px] font-semibold text-emerald-800">
                  {status}
                </span>
              </div>
              <p className="mt-0.5 text-xs text-slate-500">
                Category: <span className="font-semibold text-slate-700">{category}</span> • Subdomain:{" "}
                <code className="rounded-sm bg-slate-100 px-1.5 py-0.5 text-brand-600">{subdomain}.myeducation.in</code>
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Link
              to="/admin/modules"
              className="rounded-lg border border-slate-200 bg-white px-3.5 py-2 text-xs font-semibold text-slate-700 shadow-2xs hover:bg-slate-50"
            >
              Configure in Module Matrix
            </Link>
          </div>
        </div>
        <p className="mt-4 text-sm text-slate-600 border-t border-slate-100 pt-4">{description}</p>
      </div>

      {/* Capabilities & Operational Matrix */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-6">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-base font-bold text-slate-900 mb-4">Core Operational Workflows</h2>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
              {features.map((feat, idx) => (
                <div key={idx} className="flex items-start gap-3 rounded-xl border border-slate-100 bg-slate-50/50 p-3.5">
                  <CheckCircle2 className="h-5 w-5 text-emerald-600 shrink-0 mt-0.5" />
                  <span className="text-xs font-medium text-slate-700 leading-relaxed">{feat}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-base font-bold text-slate-900 mb-2">Live PostgreSQL Data Pipeline</h2>
            <p className="text-xs text-slate-500 mb-4">
              Real-time synchronization with Neon PostgreSQL Serverless backend.
            </p>
            <div className="rounded-xl border border-dashed border-slate-200 bg-slate-50/50 p-8 text-center">
              <Clock className="h-8 w-8 text-slate-400 mx-auto mb-2 animate-pulse" />
              <p className="text-sm font-semibold text-slate-700">Subsystem Online & Governed</p>
              <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
                All records, audit logs, and access control policies for this subsystem are actively managed by the
                governance matrix.
              </p>
            </div>
          </div>
        </div>

        {/* Sidebar Info Card */}
        <div className="space-y-6">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
            <h3 className="text-sm font-bold text-slate-900 mb-3">Subsystem Architecture</h3>
            <dl className="space-y-3 text-xs">
              <div className="flex justify-between border-b border-slate-100 pb-2">
                <dt className="text-slate-500">Security Model</dt>
                <dd className="font-semibold text-slate-800">RBAC Token Matrix</dd>
              </div>
              <div className="flex justify-between border-b border-slate-100 pb-2">
                <dt className="text-slate-500">Database Engine</dt>
                <dd className="font-semibold text-slate-800">Neon PostgreSQL 16</dd>
              </div>
              <div className="flex justify-between border-b border-slate-100 pb-2">
                <dt className="text-slate-500">Isolation Layer</dt>
                <dd className="font-semibold text-slate-800">Institute Tenant Isolation</dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-slate-500">Audit Trail</dt>
                <dd className="font-semibold text-emerald-600">Active (Encrypted)</dd>
              </div>
            </dl>
          </div>
        </div>
      </div>
    </div>
  );
};
