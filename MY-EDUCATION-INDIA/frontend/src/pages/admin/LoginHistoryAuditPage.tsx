import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  History,
  ShieldAlert,
  ShieldCheck,
  Search,
  Filter,
  CheckCircle2,
  AlertCircle,
  Clock,
  RefreshCw,
  Download,
  Laptop,
  Smartphone,
  Globe,
  MapPin,
} from "lucide-react";
import { authService } from "@/services/authService";
import { LoginHistoryItem } from "@/types/auth.types";

export const LoginHistoryAuditPage: React.FC = () => {
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [searchEmail, setSearchEmail] = useState("");

  const {
    data: history = [],
    isLoading,
    refetch,
  } = useQuery<LoginHistoryItem[]>({
    queryKey: ["login_history"],
    queryFn: async () => {
      return await authService.listLoginHistory(100);
    },
  });

  const filteredHistory = history.filter((item) => {
    const matchesStatus =
      statusFilter === "ALL" || item.status === statusFilter;
    const matchesSearch =
      item.email.toLowerCase().includes(searchEmail.toLowerCase()) ||
      item.ip_address.includes(searchEmail) ||
      item.device_name.toLowerCase().includes(searchEmail.toLowerCase());
    return matchesStatus && matchesSearch;
  });

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "SUCCESS":
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase bg-emerald-100 text-emerald-800">
            <CheckCircle2 className="w-3 h-3" /> Success
          </span>
        );
      case "ACCOUNT_LOCKED":
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase bg-rose-100 text-rose-800">
            <ShieldAlert className="w-3 h-3" /> Account Locked
          </span>
        );
      case "FAILED_CREDENTIALS":
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase bg-amber-100 text-amber-800">
            <AlertCircle className="w-3 h-3" /> Invalid Password
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase bg-slate-100 text-slate-700">
            {status}
          </span>
        );
    }
  };

  const exportCsv = () => {
    const headers = ["Timestamp,Email,Status,IP Address,Device,Location,Failure Reason\n"];
    const rows = filteredHistory.map(
      (h) =>
        `"${new Date(h.created_at).toISOString()}","${h.email}","${h.status}","${h.ip_address}","${h.device_name}","${h.location || ''}","${h.failure_reason || ''}"\n`
    );
    const blob = new Blob([...headers, ...rows], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `login_audit_trail_${new Date().toISOString().split("T")[0]}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-xl border border-slate-800">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="space-y-1.5">
            <div className="flex items-center gap-2 text-indigo-400 font-semibold text-xs tracking-wider uppercase">
              <History className="w-4 h-4" /> Phase 2 Module 1 Access Auditing
            </div>
            <h1 className="text-2xl sm:text-3xl font-black text-white">
              Login History & Access Security Log
            </h1>
            <p className="text-slate-300 text-xs sm:text-sm max-w-2xl leading-relaxed">
              Forensic timeline of all authenticated logins, failed password attempts,
              and account lockout events with client device fingerprints and IP locations.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => refetch()}
              className="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-bold transition border border-slate-700 flex items-center gap-1.5"
            >
              <RefreshCw className="w-3.5 h-3.5" /> Refresh Log
            </button>
            <button
              onClick={exportCsv}
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition flex items-center gap-1.5 shadow-sm"
            >
              <Download className="w-3.5 h-3.5" /> Export Compliance CSV
            </button>
          </div>
        </div>

        {/* Audit Stats */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-6">
          <div className="bg-slate-800/80 rounded-2xl p-4 border border-slate-700/60">
            <span className="text-xs text-slate-400 font-medium">Total Logged Attempts</span>
            <span className="text-2xl font-black text-white block mt-1">
              {history.length}
            </span>
            <span className="text-[11px] text-slate-300 font-medium mt-0.5 block">
              Neon PostgreSQL Ledger
            </span>
          </div>

          <div className="bg-slate-800/80 rounded-2xl p-4 border border-slate-700/60">
            <span className="text-xs text-slate-400 font-medium">Successful Authentications</span>
            <span className="text-2xl font-black text-emerald-400 mt-1">
              {history.filter((h) => h.status === "SUCCESS").length}
            </span>
            <span className="text-[11px] text-emerald-400 font-medium mt-0.5 block">
              Verified Tokens
            </span>
          </div>

          <div className="bg-slate-800/80 rounded-2xl p-4 border border-slate-700/60">
            <span className="text-xs text-slate-400 font-medium">Invalid Password Attempts</span>
            <span className="text-2xl font-black text-amber-400 mt-1">
              {history.filter((h) => h.status === "FAILED_CREDENTIALS").length}
            </span>
            <span className="text-[11px] text-amber-400 font-medium mt-0.5 block">
              Counter Triggered
            </span>
          </div>

          <div className="bg-slate-800/80 rounded-2xl p-4 border border-slate-700/60">
            <span className="text-xs text-slate-400 font-medium">Account Lockout Events</span>
            <span className="text-2xl font-black text-rose-400 mt-1">
              {history.filter((h) => h.status === "ACCOUNT_LOCKED").length}
            </span>
            <span className="text-[11px] text-rose-400 font-medium mt-0.5 block">
              Lockout Duration Enforced
            </span>
          </div>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200/90 shadow-2xs flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
          <input
            type="text"
            placeholder="Search email, IP, or device..."
            value={searchEmail}
            onChange={(e) => setSearchEmail(e.target.value)}
            className="w-full pl-9 pr-4 py-2 border border-slate-300 rounded-xl text-xs outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="border border-slate-300 rounded-xl px-3 py-2 text-xs font-semibold bg-white text-slate-700 outline-none"
          >
            <option value="ALL">All Outcomes</option>
            <option value="SUCCESS">Success Only</option>
            <option value="FAILED_CREDENTIALS">Failed Passwords</option>
            <option value="ACCOUNT_LOCKED">Account Lockouts</option>
          </select>
        </div>
      </div>

      {/* Audit Table */}
      <div className="bg-white rounded-3xl border border-slate-200/90 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-700">
            <thead className="bg-slate-50 border-b border-slate-200 text-xs font-bold text-slate-500 uppercase tracking-wider">
              <tr>
                <th className="py-3 px-4">Timestamp</th>
                <th className="py-3 px-4">User Identifier</th>
                <th className="py-3 px-4">Status & Reason</th>
                <th className="py-3 px-4">Device & Browser</th>
                <th className="py-3 px-4">IP Address</th>
                <th className="py-3 px-4">Location</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-xs">
              {isLoading ? (
                <tr>
                  <td colSpan={6} className="py-12 text-center text-slate-400">
                    Querying login history ledger...
                  </td>
                </tr>
              ) : filteredHistory.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-12 text-center text-slate-500">
                    No login history records found matching filters.
                  </td>
                </tr>
              ) : (
                filteredHistory.map((row) => (
                  <tr key={row.id} className="hover:bg-slate-50/80 transition">
                    <td className="py-3 px-4 font-mono text-slate-500 whitespace-nowrap">
                      {new Date(row.created_at).toLocaleString()}
                    </td>
                    <td className="py-3 px-4 font-bold text-slate-900">
                      {row.email}
                    </td>
                    <td className="py-3 px-4">
                      {getStatusBadge(row.status)}
                      {row.failure_reason && (
                        <p className="text-[11px] text-slate-400 mt-0.5">
                          {row.failure_reason}
                        </p>
                      )}
                    </td>
                    <td className="py-3 px-4 font-semibold text-slate-700">
                      {row.device_name}
                    </td>
                    <td className="py-3 px-4 font-mono text-slate-600">
                      {row.ip_address}
                    </td>
                    <td className="py-3 px-4 text-slate-500 flex items-center gap-1 mt-2.5">
                      <MapPin className="w-3 h-3 text-slate-400 shrink-0" />
                      <span>{row.location || "Indore, MP, India"}</span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
