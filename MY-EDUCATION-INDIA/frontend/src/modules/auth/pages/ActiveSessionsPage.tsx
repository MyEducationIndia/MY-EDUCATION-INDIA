import React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Smartphone, Monitor, ShieldCheck, LogOut } from "lucide-react";
import { authApi } from "../api/authApi";
import { useAuth } from "../context/AuthContext";

export const ActiveSessionsPage: React.FC = () => {
  const queryClient = useQueryClient();
  const { user } = useAuth();

  const { data: sessions = [], isLoading } = useQuery({
    queryKey: ["activeSessions", user?.id],
    queryFn: () => (user?.id ? authApi.getActiveSessions(user.id) : Promise.resolve([])),
    enabled: Boolean(user?.id),
  });

  const revokeMutation = useMutation({
    mutationFn: (sessionId: string) => authApi.forceLogoutSession(sessionId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["activeSessions"] });
    },
  });

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900 sm:p-6">
      <div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-center">
        <div>
          <h2 className="text-base font-bold text-slate-900 dark:text-white">
            Active Security Sessions ({sessions.length})
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Monitor and manage active PostgreSQL refresh token sessions across authorized devices.
          </p>
        </div>
      </div>

      <div className="mt-5 space-y-3">
        {isLoading ? (
          <p className="text-xs text-slate-500">Loading active sessions...</p>
        ) : sessions.length === 0 ? (
          <p className="text-xs text-slate-500">No active sessions found.</p>
        ) : (
          sessions.map((s) => (
            <div
              key={s.id}
              className="flex flex-col justify-between gap-3 rounded-xl border border-slate-200 bg-slate-50/50 p-4 dark:border-slate-800 dark:bg-slate-950/50 sm:flex-row sm:items-center"
            >
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-50 text-brand-600 dark:bg-brand-950 dark:text-brand-400">
                  {s.device_info.toLowerCase().includes("mobile") ? (
                    <Smartphone className="h-5 w-5" />
                  ) : (
                    <Monitor className="h-5 w-5" />
                  )}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-slate-900 dark:text-white">
                      {s.device_info}
                    </span>
                    {s.is_current && (
                      <span className="inline-flex items-center gap-1 rounded-sm bg-emerald-50 px-2 py-0.5 text-[10px] font-semibold text-emerald-700 dark:bg-emerald-950 dark:text-emerald-400">
                        <ShieldCheck className="h-3 w-3" /> Current Session
                      </span>
                    )}
                  </div>
                  <p className="mt-0.5 font-mono text-[11px] text-slate-500 dark:text-slate-400">
                    IP: {s.ip_address} • Logged in: {new Date(s.created_at).toLocaleString()}
                  </p>
                </div>
              </div>

              {!s.is_current && (
                <button
                  type="button"
                  disabled={revokeMutation.isPending}
                  onClick={() => revokeMutation.mutate(s.id)}
                  className="inline-flex items-center justify-center gap-1.5 rounded-lg border border-rose-300 bg-rose-50 px-3 py-1.5 text-xs font-semibold text-rose-700 hover:bg-rose-100 dark:border-rose-800 dark:bg-rose-950 dark:text-rose-300"
                >
                  <LogOut className="h-3.5 w-3.5" />
                  <span>Force Logout</span>
                </button>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};
