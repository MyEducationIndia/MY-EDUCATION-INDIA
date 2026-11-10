import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { authApi } from "../api/authApi";
import { useAuth } from "../context/AuthContext";

export const LoginHistoryPage: React.FC = () => {
  const { user } = useAuth();
  const [page, setPage] = useState<number>(1);

  const { data, isLoading } = useQuery({
    queryKey: ["loginHistory", page, user?.id],
    queryFn: () => authApi.getLoginHistory({ page, pageSize: 20 }),
  });

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900 sm:p-6">
      <div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-center">
        <div>
          <h2 className="text-base font-bold text-slate-900 dark:text-white">
            Institutional Login History
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Immutable audit record of authentication attempts, used criteria, and session durations.
          </p>
        </div>
      </div>

      <div className="mt-5 overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200 text-left text-xs dark:divide-slate-800">
          <thead>
            <tr className="bg-slate-50 font-semibold uppercase tracking-wider text-slate-500 dark:bg-slate-950 dark:text-slate-400">
              <th className="px-4 py-3">Timestamp (UTC)</th>
              <th className="px-4 py-3">Identifier Used</th>
              <th className="px-4 py-3">Criterion</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3">Device & Browser</th>
              <th className="px-4 py-3">IP Address</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
            {isLoading ? (
              <tr>
                <td colSpan={6} className="px-4 py-6 text-center text-slate-500">
                  Loading login history from PostgreSQL...
                </td>
              </tr>
            ) : (data?.items || []).length === 0 ? (
              <tr>
                <td colSpan={6} className="px-4 py-6 text-center text-slate-500">
                  No login history records found.
                </td>
              </tr>
            ) : (
              (data?.items || []).map((h) => (
                <tr key={h.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/50">
                  <td className="whitespace-nowrap px-4 py-3 font-mono text-slate-600 dark:text-slate-400">
                    {new Date(h.logged_in_at).toISOString()}
                  </td>
                  <td className="px-4 py-3 font-semibold text-slate-900 dark:text-white">
                    {h.identifier_used}
                  </td>
                  <td className="px-4 py-3 font-mono text-slate-600 dark:text-slate-400">
                    {h.login_criterion}
                  </td>
                  <td className="px-4 py-3">
                    <span
                      className={`rounded-sm px-2 py-0.5 font-mono text-[11px] font-bold ${
                        h.status === "SUCCESS"
                          ? "bg-emerald-50 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300"
                          : "bg-rose-50 text-rose-700 dark:bg-rose-950 dark:text-rose-300"
                      }`}
                    >
                      {h.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-slate-600 dark:text-slate-400">
                    {h.browser} on {h.os} ({h.device_type})
                  </td>
                  <td className="px-4 py-3 font-mono text-slate-600 dark:text-slate-400">
                    {h.ip_address}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
