import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  MonitorSmartphone,
  ShieldCheck,
  Laptop,
  Smartphone,
  Globe,
  Trash2,
  RefreshCw,
  LogOut,
  Clock,
  AlertTriangle,
  CheckCircle2,
} from "lucide-react";
import { authService } from "@/services/authService";
import { ActiveSessionItem } from "@/types/auth.types";

export const ActiveSessionsPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  const {
    data: sessions = [],
    isLoading,
    refetch,
  } = useQuery<ActiveSessionItem[]>({
    queryKey: ["active_sessions"],
    queryFn: authService.listActiveSessions,
  });

  const revokeSessionMutation = useMutation({
    mutationFn: async (id: string) => {
      return await authService.revokeSession(id);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["active_sessions"] });
      setStatusMessage("Device session revoked successfully.");
      setTimeout(() => setStatusMessage(null), 3000);
    },
  });

  const revokeAllMutation = useMutation({
    mutationFn: async () => {
      return await authService.revokeAllSessions();
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["active_sessions"] });
      setStatusMessage(data.message || "All other device sessions revoked.");
      setTimeout(() => setStatusMessage(null), 3000);
    },
  });

  const getDeviceIcon = (deviceName: string) => {
    const d = deviceName.toLowerCase();
    if (d.includes("iphone") || d.includes("android") || d.includes("phone")) {
      return <Smartphone className="w-5 h-5 text-indigo-500" />;
    }
    return <Laptop className="w-5 h-5 text-indigo-500" />;
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-xl border border-slate-800">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="space-y-1.5">
            <div className="flex items-center gap-2 text-indigo-400 font-semibold text-xs tracking-wider uppercase">
              <MonitorSmartphone className="w-4 h-4" /> Phase 2 Module 1 Session Governance
            </div>
            <h1 className="text-2xl sm:text-3xl font-black text-white">
              Active Sessions & Device Management
            </h1>
            <p className="text-slate-300 text-xs sm:text-sm max-w-2xl leading-relaxed">
              Real-time PostgreSQL tracking of active authenticated JWT refresh token
              families across desktop browsers, mobile devices, and campus terminals.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => refetch()}
              className="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-bold transition border border-slate-700 flex items-center gap-1.5"
            >
              <RefreshCw className="w-3.5 h-3.5" /> Refresh
            </button>
            <button
              onClick={() => {
                if (confirm("Revoke all other active device sessions?")) {
                  revokeAllMutation.mutate();
                }
              }}
              disabled={revokeAllMutation.isPending}
              className="px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white rounded-xl text-xs font-bold transition flex items-center gap-1.5 shadow-sm disabled:opacity-50"
            >
              <LogOut className="w-3.5 h-3.5" /> Revoke Other Devices
            </button>
          </div>
        </div>

        {/* Counter Summary */}
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 mt-6">
          <div className="bg-slate-800/80 rounded-2xl p-4 border border-slate-700/60">
            <span className="text-xs text-slate-400 font-medium">Active Devices</span>
            <span className="text-2xl font-black text-white block mt-1">
              {sessions.length}
            </span>
            <span className="text-[11px] text-emerald-400 font-semibold mt-0.5 block flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3" /> Token Families Validated
            </span>
          </div>

          <div className="bg-slate-800/80 rounded-2xl p-4 border border-slate-700/60">
            <span className="text-xs text-slate-400 font-medium">Session Policy</span>
            <span className="text-2xl font-black text-white block mt-1">
              Strict Rotation
            </span>
            <span className="text-[11px] text-indigo-400 font-semibold mt-0.5 block">
              Reuse Detection Armed
            </span>
          </div>

          <div className="bg-slate-800/80 rounded-2xl p-4 border border-slate-700/60 col-span-2 sm:col-span-1">
            <span className="text-xs text-slate-400 font-medium">Security Perimeter</span>
            <span className="text-2xl font-black text-white block mt-1">
              Indore HQ
            </span>
            <span className="text-[11px] text-slate-400 font-semibold mt-0.5 block">
              Campus & Remote Sockets
            </span>
          </div>
        </div>
      </div>

      {statusMessage && (
        <div className="p-4 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-2xl text-xs font-semibold flex items-center gap-2 animate-in fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
          <span>{statusMessage}</span>
        </div>
      )}

      {/* Sessions Grid */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200/90 shadow-sm space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-slate-100">
          <div>
            <h2 className="text-base font-bold text-slate-900">
              Authenticated Devices Ledger
            </h2>
            <p className="text-xs text-slate-500">
              Select any session to immediately invalidate its refresh token family and enforce re-authentication.
            </p>
          </div>
        </div>

        {isLoading ? (
          <div className="py-12 text-center text-slate-400">
            Querying active refresh token families...
          </div>
        ) : sessions.length === 0 ? (
          <div className="py-12 text-center text-slate-500">
            No active sessions found.
          </div>
        ) : (
          <div className="divide-y divide-slate-100">
            {sessions.map((session) => (
              <div
                key={session.id}
                className="py-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 hover:bg-slate-50/60 px-3 rounded-2xl transition"
              >
                <div className="flex items-start gap-3.5">
                  <div className="p-3 bg-indigo-50 rounded-2xl border border-indigo-100/80 shrink-0 mt-0.5">
                    {getDeviceIcon(session.device_name)}
                  </div>
                  <div className="space-y-0.5">
                    <div className="flex items-center gap-2">
                      <h4 className="font-bold text-slate-900 text-sm">
                        {session.device_name}
                      </h4>
                      {session.is_current && (
                        <span className="px-2 py-0.5 rounded-full text-[10px] font-black uppercase bg-emerald-100 text-emerald-800">
                          Current Device
                        </span>
                      )}
                    </div>
                    <p className="font-mono text-xs text-slate-500">
                      IP: {session.ip_address} • User-Agent: {session.user_agent.slice(0, 45)}...
                    </p>
                    <div className="flex items-center gap-3 text-[11px] text-slate-400 pt-0.5">
                      <span>Logged in: {new Date(session.created_at).toLocaleString()}</span>
                      <span>Expires: {new Date(session.expires_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>

                <div>
                  {!session.is_current && (
                    <button
                      onClick={() => {
                        if (confirm(`Revoke session for ${session.device_name}?`)) {
                          revokeSessionMutation.mutate(session.id);
                        }
                      }}
                      className="px-3.5 py-1.5 border border-slate-300 hover:border-rose-300 hover:bg-rose-50 hover:text-rose-700 text-slate-600 rounded-xl text-xs font-bold transition flex items-center gap-1.5"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                      <span>Revoke Session</span>
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
