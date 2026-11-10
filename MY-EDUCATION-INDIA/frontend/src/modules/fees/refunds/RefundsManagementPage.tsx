import React, { useState } from "react";
import { RotateCcw, Plus, CheckCircle, Clock } from "lucide-react";
import { Refund } from "../types/fee.types";

export const RefundsManagementPage: React.FC = () => {
  const [refunds, setRefunds] = useState<Refund[]>([
    {
      id: "ref-1",
      refund_number: "REF-MEI-20261101-0021",
      payment_id: "pay-1",
      student_id: "stu-1",
      amount: 15000.0,
      refund_type: "PARTIAL",
      reason: "Hostel security deposit refund upon semester completion",
      approval_status: "PROCESSED",
      payment_mode: "BANK_TRANSFER",
      reference_number: "NEFT-98421094",
      created_at: "2026-11-01",
    },
    {
      id: "ref-2",
      refund_number: "REF-MEI-20261104-0022",
      payment_id: "pay-2",
      student_id: "stu-2",
      amount: 25000.0,
      refund_type: "FULL",
      reason: "Admission withdrawal within UGC stipulated cancellation window",
      approval_status: "PENDING",
      payment_mode: "BANK_TRANSFER",
      created_at: "2026-11-04",
    },
  ]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <RotateCcw className="h-7 w-7 text-emerald-600 dark:text-emerald-400" />
            Refunds & Security Deposit Settlement
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Audit trail, approval workflow, and ledger adjustments for student refunds.
          </p>
        </div>
        <button
          type="button"
          onClick={() => alert("Initiate refund modal")}
          className="flex items-center gap-2 rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold text-white shadow-xs hover:bg-emerald-700 transition"
        >
          <Plus className="h-4 w-4" />
          <span>New Refund Request</span>
        </button>
      </div>

      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 overflow-hidden shadow-xs">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 dark:bg-slate-700/50 text-xs uppercase text-slate-500 font-semibold border-b border-slate-200 dark:border-slate-700">
            <tr>
              <th className="px-6 py-3.5">Refund ID</th>
              <th className="px-6 py-3.5">Amount</th>
              <th className="px-6 py-3.5">Type</th>
              <th className="px-6 py-3.5">Reason</th>
              <th className="px-6 py-3.5">Mode</th>
              <th className="px-6 py-3.5">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-700/60">
            {refunds.map((r) => (
              <tr key={r.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-700/30">
                <td className="px-6 py-4 font-mono text-xs font-bold text-slate-900 dark:text-white">
                  {r.refund_number}
                </td>
                <td className="px-6 py-4 font-bold text-slate-900 dark:text-white">
                  ₹{r.amount.toLocaleString("en-IN")}
                </td>
                <td className="px-6 py-4 text-xs font-medium text-slate-600 dark:text-slate-300">
                  {r.refund_type}
                </td>
                <td className="px-6 py-4 text-xs text-slate-500 max-w-xs truncate">
                  {r.reason}
                </td>
                <td className="px-6 py-4 text-xs font-semibold text-slate-700 dark:text-slate-300">
                  {r.payment_mode}
                </td>
                <td className="px-6 py-4">
                  <span
                    className={`inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-semibold ${
                      r.approval_status === "PROCESSED"
                        ? "bg-emerald-50 text-emerald-600 dark:bg-emerald-950/60 dark:text-emerald-400"
                        : "bg-amber-50 text-amber-600 dark:bg-amber-950/60 dark:text-amber-400"
                    }`}
                  >
                    {r.approval_status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
