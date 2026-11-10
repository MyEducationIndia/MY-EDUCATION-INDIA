import React, { useState } from "react";
import { Layers, Plus, Calendar, IndianRupee, CheckCircle2 } from "lucide-react";
import { FeeStructure } from "../types/fee.types";

export const FeeStructuresPage: React.FC = () => {
  const [structures, setStructures] = useState<FeeStructure[]>([
    {
      id: "fs-1",
      code: "BTECH-CSE-2026",
      name: "B.Tech Computer Science & AI (Annual Structure)",
      version: 1,
      institute_id: "inst-1",
      academic_year_id: "ay-2026",
      effective_date: "2026-08-01",
      validity_date: "2027-06-30",
      total_amount: 145000.0,
      status: "ACTIVE",
      items: [
        { id: "it-1", fee_structure_id: "fs-1", fee_head_id: "fh-1", amount: 100000.0, is_optional: false, frequency: "ANNUAL", created_at: "" },
        { id: "it-2", fee_structure_id: "fs-1", fee_head_id: "fh-2", amount: 25000.0, is_optional: false, frequency: "ANNUAL", created_at: "" },
        { id: "it-3", fee_structure_id: "fs-1", fee_head_id: "fh-3", amount: 20000.0, is_optional: false, frequency: "ONE_TIME", created_at: "" },
      ],
      installments: [
        { id: "in-1", fee_structure_id: "fs-1", installment_number: 1, title: "Admission & 1st Semester", due_date: "2026-08-15", percentage: 50.0, amount: 72500.0, grace_days: 7, status: "OPEN", created_at: "" },
        { id: "in-2", fee_structure_id: "fs-1", installment_number: 2, title: "2nd Semester Fee", due_date: "2027-01-15", percentage: 50.0, amount: 72500.0, grace_days: 7, status: "SCHEDULED", created_at: "" },
      ],
      created_at: "2026-07-01",
    },
    {
      id: "fs-2",
      code: "MBA-EXEC-2026",
      name: "MBA Executive Leadership Program",
      version: 1,
      institute_id: "inst-1",
      academic_year_id: "ay-2026",
      effective_date: "2026-08-01",
      validity_date: "2027-06-30",
      total_amount: 220000.0,
      status: "ACTIVE",
      items: [
        { id: "it-4", fee_structure_id: "fs-2", fee_head_id: "fh-1", amount: 180000.0, is_optional: false, frequency: "ANNUAL", created_at: "" },
        { id: "it-5", fee_structure_id: "fs-2", fee_head_id: "fh-4", amount: 40000.0, is_optional: false, frequency: "ONE_TIME", created_at: "" },
      ],
      installments: [
        { id: "in-3", fee_structure_id: "fs-2", installment_number: 1, title: "Q1 Advance", due_date: "2026-08-10", percentage: 40.0, amount: 88000.0, grace_days: 5, status: "OPEN", created_at: "" },
        { id: "in-4", fee_structure_id: "fs-2", installment_number: 2, title: "Q2 Installment", due_date: "2026-11-10", percentage: 30.0, amount: 66000.0, grace_days: 5, status: "SCHEDULED", created_at: "" },
        { id: "in-5", fee_structure_id: "fs-2", installment_number: 3, title: "Q3 Final Balance", due_date: "2027-02-10", percentage: 30.0, amount: 66000.0, grace_days: 5, status: "SCHEDULED", created_at: "" },
      ],
      created_at: "2026-07-05",
    },
  ]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <Layers className="h-7 w-7 text-emerald-600 dark:text-emerald-400" />
            Institutional Fee Structures
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Define multi-tiered fee templates, installment payment schedules, and fee heads.
          </p>
        </div>
        <button
          type="button"
          onClick={() => alert("Fee structure creator modal")}
          className="flex items-center gap-2 rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold text-white shadow-xs hover:bg-emerald-700 transition"
        >
          <Plus className="h-4 w-4" />
          <span>New Fee Structure</span>
        </button>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {structures.map((s) => (
          <div
            key={s.id}
            className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs"
          >
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-100 dark:border-slate-700/60 pb-4">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950 px-2 py-0.5 rounded-sm">
                    {s.code}
                  </span>
                  <span className="text-xs text-slate-400">v{s.version}</span>
                </div>
                <h3 className="mt-1 text-lg font-bold text-slate-900 dark:text-white">{s.name}</h3>
              </div>
              <div className="flex items-center gap-4">
                <div className="text-right">
                  <span className="text-xs font-semibold text-slate-400 uppercase">Annual Structure Total</span>
                  <p className="text-xl font-extrabold text-slate-900 dark:text-white">
                    ₹{s.total_amount.toLocaleString("en-IN")}
                  </p>
                </div>
                <span className="inline-flex items-center gap-1 rounded-full bg-emerald-50 dark:bg-emerald-950/60 px-3 py-1 text-xs font-semibold text-emerald-600 dark:text-emerald-400">
                  <CheckCircle2 className="h-3.5 w-3.5" />
                  {s.status}
                </span>
              </div>
            </div>

            {/* Installments Breakdown */}
            <div className="mt-4">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-3">
                Scheduled Installment Plan ({s.installments.length} Installments)
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                {s.installments.map((inst) => (
                  <div
                    key={inst.id}
                    className="rounded-lg bg-slate-50 dark:bg-slate-700/40 border border-slate-200/60 dark:border-slate-700 p-3"
                  >
                    <div className="flex justify-between items-center text-xs font-semibold text-slate-800 dark:text-slate-200">
                      <span>#{inst.installment_number} {inst.title}</span>
                      <span className="text-emerald-600 dark:text-emerald-400">{inst.percentage}%</span>
                    </div>
                    <p className="mt-2 text-base font-bold text-slate-900 dark:text-white">
                      ₹{inst.amount.toLocaleString("en-IN")}
                    </p>
                    <div className="mt-1 flex items-center gap-1.5 text-[11px] text-slate-500">
                      <Calendar className="h-3.5 w-3.5" />
                      <span>Due: {inst.due_date} (Grace: {inst.grace_days}d)</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
