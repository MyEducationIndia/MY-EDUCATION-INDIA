import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { auditService } from "@/services/auditService";

export const AuditLogsPage: React.FC = () => {
  const [page, setPage] = useState(1);
  const [actionFilter, setActionFilter] = useState("");

  const { data, isLoading } = useQuery({
    queryKey: ["audit-logs", page, actionFilter],
    queryFn: () =>
      auditService.listAuditLogs({
        action: actionFilter || undefined,
        page,
        page_size: 25,
      }),
  });

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs sm:p-6">
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <h2 className="text-base font-bold text-slate-900">
            Immutable Security & Compliance Audit Trail
          </h2>
          <p className="text-xs text-slate-500">
            Every authentication, role change, and module state mutation recorded in PostgreSQL.
          </p>
        </div>
        <input
          type="search"
          value={actionFilter}
          onChange={(e) => {
            setActionFilter(e.target.value);
            setPage(1);
          }}
          placeholder="Filter by action (e.g. AUTH_LOGIN_SUCCESS)..."
          className="w-full rounded-lg border border-slate-300 px-3.5 py-2 text-sm sm:w-80 focus:border-brand-600 focus:outline-hidden"
        />
      </div>

      <div className="mt-5 overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200 text-left text-xs">
          <thead>
            <tr className="bg-slate-50 font-semibold uppercase tracking-wider text-slate-500">
              <th className="px-4 py-3">Timestamp (UTC)</th>
              <th className="px-4 py-3">Module</th>
              <th className="px-4 py-3">Action</th>
              <th className="px-4 py-3">Endpoint</th>
              <th className="px-4 py-3">IP Address</th>
              <th className="px-4 py-3">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {isLoading ? (
              <tr>
                <td colSpan={6} className="px-4 py-6 text-center text-slate-500">
                  Loading compliance logs...
                </td>
              </tr>
            ) : (
              (data?.items || []).map((entry) => (
                <tr key={entry.id} className="hover:bg-slate-50">
                  <td className="whitespace-nowrap px-4 py-3 font-mono text-slate-600">
                    {new Date(entry.created_at).toISOString()}
                  </td>
                  <td className="px-4 py-3 font-semibold text-slate-800">
                    {entry.module_key}
                  </td>
                  <td className="px-4 py-3 font-mono font-semibold text-brand-700">
                    {entry.action}
                  </td>
                  <td className="px-4 py-3 font-mono text-slate-600">
                    {entry.http_method} {entry.endpoint_path}
                  </td>
                  <td className="px-4 py-3 font-mono text-slate-600">
                    {entry.ip_address}
                  </td>
                  <td className="px-4 py-3">
                    <span
                      className={`rounded-sm px-2 py-0.5 font-mono font-bold ${
                        entry.status_code < 400
                          ? "bg-emerald-50 text-emerald-700"
                          : "bg-rose-50 text-rose-700"
                      }`}
                    >
                      {entry.status_code}
                    </span>
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
