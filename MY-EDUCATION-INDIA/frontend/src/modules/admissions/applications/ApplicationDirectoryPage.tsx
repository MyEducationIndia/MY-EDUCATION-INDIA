import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Search, CheckCircle2, XCircle, CreditCard, Eye, ShieldCheck } from "lucide-react";
import { admissionService } from "../services/admissionService";
import { ApplicationRecord } from "../types/admission.types";

export const ApplicationDirectoryPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("");

  const { data, isLoading } = useQuery({
    queryKey: ["applicationsList", searchTerm, statusFilter],
    queryFn: () => admissionService.listApplications({ search: searchTerm || undefined, status: statusFilter || undefined }),
  });

  const approveMutation = useMutation({
    mutationFn: (appId: string) => admissionService.approveAdmission(appId, "2026-Batch-A"),
    onSuccess: (res) => {
      alert(`Admission Approved! Successfully created SIMS Student with Reg No: ${res.registration_number}`);
      void queryClient.invalidateQueries({ queryKey: ["applicationsList"] });
    },
  });

  const collectFeeMutation = useMutation({
    mutationFn: (appId: string) => admissionService.collectFee({ application_id: appId, amount_paid: 25000.0 }),
    onSuccess: () => {
      alert("Registration Fee Collected Successfully (Receipt Issued)!");
      void queryClient.invalidateQueries({ queryKey: ["applicationsList"] });
    },
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-base font-bold text-slate-900 dark:text-white">Admission Applications</h1>
          <p className="text-xs text-slate-500">Review submitted online and offline forms, verify documents, and convert candidates into SIMS students.</p>
        </div>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200 text-left text-xs dark:divide-slate-800">
            <thead>
              <tr className="bg-slate-50 uppercase text-slate-500 dark:bg-slate-950">
                <th className="px-4 py-3">Application No</th>
                <th className="px-4 py-3">Candidate</th>
                <th className="px-4 py-3">Course & Batch</th>
                <th className="px-4 py-3">Guardian</th>
                <th className="px-4 py-3">Mode</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3 text-right">Workflow Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
              {isLoading ? (
                <tr><td colSpan={7} className="p-8 text-center text-slate-500">Loading Applications...</td></tr>
              ) : (data?.items || []).length === 0 ? (
                <tr><td colSpan={7} className="p-8 text-center text-slate-500">No applications found. Submit an admission form to start.</td></tr>
              ) : (
                data?.items.map((app: ApplicationRecord) => (
                  <tr key={app.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                    <td className="px-4 py-3 font-mono font-bold text-brand-600">{app.application_number}</td>
                    <td className="px-4 py-3 font-bold text-slate-900 dark:text-white">
                      {app.first_name} {app.last_name}
                      <div className="text-[10px] text-slate-400 font-normal">{app.email}</div>
                    </td>
                    <td className="px-4 py-3">
                      <div>{app.course_name}</div>
                      <div className="text-[10px] text-slate-400">{app.batch_preference}</div>
                    </td>
                    <td className="px-4 py-3">{app.guardian_name}</td>
                    <td className="px-4 py-3 font-semibold text-slate-600 dark:text-slate-400">{app.application_mode}</td>
                    <td className="px-4 py-3">
                      <span className={`rounded-sm px-2 py-0.5 text-[10px] font-bold ${
                        app.status === "CONVERTED"
                          ? "bg-emerald-50 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300"
                          : "bg-blue-50 text-blue-700 dark:bg-blue-950 dark:text-blue-300"
                      }`}>
                        {app.status}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-right">
                      <div className="flex items-center justify-end gap-1.5">
                        {app.status !== "FEE_PAID" && app.status !== "CONVERTED" && (
                          <button
                            type="button"
                            onClick={() => collectFeeMutation.mutate(app.id)}
                            className="inline-flex items-center gap-1 rounded-lg border border-teal-300 bg-teal-50 px-2 py-1 text-[11px] font-semibold text-teal-700 hover:bg-teal-100 dark:bg-teal-950 dark:text-teal-300"
                          >
                            <CreditCard className="h-3 w-3" /> Collect Fee
                          </button>
                        )}
                        {app.status !== "CONVERTED" ? (
                          <button
                            type="button"
                            onClick={() => approveMutation.mutate(app.id)}
                            className="inline-flex items-center gap-1 rounded-lg bg-emerald-600 px-2.5 py-1 text-[11px] font-bold text-white shadow-xs hover:bg-emerald-500"
                          >
                            <CheckCircle2 className="h-3 w-3" /> Approve & Convert to SIMS
                          </button>
                        ) : (
                          <span className="text-[11px] font-bold text-emerald-600">Enrolled in SIMS ✓</span>
                        )}
                      </div>
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
