import React, { useState } from "react";
import { FileCheck2, Plus, CheckCircle, XCircle } from "lucide-react";

export const LeaveManagementPage: React.FC = () => {
  const [requests, setRequests] = useState([
    { id: "1", applicant: "Dr. Shalini Verma", type: "Medical Leave", dates: "Nov 06 - Nov 08 (3 days)", reason: "Hospitalization for acute viral fever", status: "PENDING" },
    { id: "2", applicant: "Kabir Patel (Student)", type: "Casual Leave", dates: "Nov 09 - Nov 10 (2 days)", reason: "Family wedding attendance", status: "PENDING" },
    { id: "3", applicant: "Prof. Priya Ramaswamy", type: "Exam Duty", dates: "Nov 04 - Nov 04 (1 day)", reason: "External Viva Examiner at NIT", status: "APPROVED" },
  ]);

  const handleAction = (id: string, action: string) => {
    setRequests(requests.map((r) => (r.id === id ? { ...r, status: action } : r)));
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <FileCheck2 className="h-7 w-7 text-indigo-600 dark:text-indigo-400" />
            Leave Applications & Workflow Management
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Process Casual, Medical, Earned, Duty, and Special leaves for students and employees.
          </p>
        </div>
        <button
          type="button"
          onClick={() => alert("Apply leave modal")}
          className="flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-xs hover:bg-indigo-700 transition"
        >
          <Plus className="h-4 w-4" />
          <span>Apply for Leave</span>
        </button>
      </div>

      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 overflow-hidden shadow-xs">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 dark:bg-slate-700/50 text-xs uppercase text-slate-500 font-semibold border-b border-slate-200 dark:border-slate-700">
            <tr>
              <th className="px-6 py-3.5">Applicant</th>
              <th className="px-6 py-3.5">Leave Scheme</th>
              <th className="px-6 py-3.5">Period</th>
              <th className="px-6 py-3.5">Reason</th>
              <th className="px-6 py-3.5">Status</th>
              <th className="px-6 py-3.5 text-center">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-700/60">
            {requests.map((r) => (
              <tr key={r.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-700/30">
                <td className="px-6 py-4 font-bold text-slate-900 dark:text-white">{r.applicant}</td>
                <td className="px-6 py-4 text-xs font-semibold text-slate-700 dark:text-slate-300">{r.type}</td>
                <td className="px-6 py-4 text-xs text-slate-500">{r.dates}</td>
                <td className="px-6 py-4 text-xs text-slate-600 dark:text-slate-400 max-w-xs truncate">{r.reason}</td>
                <td className="px-6 py-4">
                  <span
                    className={`inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-semibold ${
                      r.status === "APPROVED"
                        ? "bg-emerald-50 text-emerald-600 dark:bg-emerald-950/60"
                        : r.status === "REJECTED"
                        ? "bg-rose-50 text-rose-600 dark:bg-rose-950/60"
                        : "bg-amber-50 text-amber-600 dark:bg-amber-950/60"
                    }`}
                  >
                    {r.status}
                  </span>
                </td>
                <td className="px-6 py-4 text-center">
                  {r.status === "PENDING" ? (
                    <div className="flex items-center justify-center gap-2">
                      <button
                        type="button"
                        onClick={() => handleAction(r.id, "APPROVED")}
                        className="rounded-md bg-emerald-600 p-1.5 text-white hover:bg-emerald-700"
                        title="Approve Leave"
                      >
                        <CheckCircle className="h-4 w-4" />
                      </button>
                      <button
                        type="button"
                        onClick={() => handleAction(r.id, "REJECTED")}
                        className="rounded-md bg-rose-600 p-1.5 text-white hover:bg-rose-700"
                        title="Reject Leave"
                      >
                        <XCircle className="h-4 w-4" />
                      </button>
                    </div>
                  ) : (
                    <span className="text-xs text-slate-400">Processed</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
