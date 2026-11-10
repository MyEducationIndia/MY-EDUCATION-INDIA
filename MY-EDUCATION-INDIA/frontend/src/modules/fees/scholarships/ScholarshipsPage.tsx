import React, { useState } from "react";
import { Award, Plus, CheckCircle2, IndianRupee } from "lucide-react";
import { Scholarship } from "../types/fee.types";

export const ScholarshipsPage: React.FC = () => {
  const [scholarships, setScholarships] = useState<Scholarship[]>([
    {
      id: "sch-1",
      code: "MERIT-TOP-10",
      name: "Merit Scholarship for Top 10 Percentile",
      scholarship_type: "MERIT",
      calculation_type: "PERCENTAGE",
      value: 25.0,
      eligibility_criteria: "Minimum 90% in qualifying board examinations",
      approval_workflow_status: "APPROVED",
      max_beneficiaries: 50,
      is_active: true,
      created_at: "2026-07-01",
    },
    {
      id: "sch-2",
      code: "SPORTS-STATE",
      name: "State Level Sports Championship Grant",
      scholarship_type: "SPORTS",
      calculation_type: "FIXED_AMOUNT",
      value: 40000.0,
      eligibility_criteria: "Gold or Silver medalist in State Athletics",
      approval_workflow_status: "APPROVED",
      max_beneficiaries: 20,
      is_active: true,
      created_at: "2026-07-01",
    },
    {
      id: "sch-3",
      code: "STAFF-WARD",
      name: "Staff Ward Educational Concession",
      scholarship_type: "STAFF",
      calculation_type: "PERCENTAGE",
      value: 50.0,
      eligibility_criteria: "Children of full-time academic or administrative staff",
      approval_workflow_status: "APPROVED",
      max_beneficiaries: 100,
      is_active: true,
      created_at: "2026-07-01",
    },
  ]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <Award className="h-7 w-7 text-emerald-600 dark:text-emerald-400" />
            Scholarships & Institutional Aid Schemes
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Define merit, sports, government, and staff tuition fee waivers and approval criteria.
          </p>
        </div>
        <button
          type="button"
          onClick={() => alert("Create Scholarship modal")}
          className="flex items-center gap-2 rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold text-white shadow-xs hover:bg-emerald-700 transition"
        >
          <Plus className="h-4 w-4" />
          <span>New Scholarship</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {scholarships.map((sch) => (
          <div
            key={sch.id}
            className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-purple-600 dark:text-purple-400 bg-purple-50 dark:bg-purple-950 px-2 py-0.5 rounded-sm">
                  {sch.code}
                </span>
                <span className="text-xs font-bold text-emerald-600 bg-emerald-50 dark:bg-emerald-950 px-2 py-0.5 rounded-sm">
                  {sch.scholarship_type}
                </span>
              </div>
              <h3 className="mt-3 text-base font-bold text-slate-900 dark:text-white">{sch.name}</h3>
              <p className="mt-2 text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                {sch.eligibility_criteria}
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-700/60 flex items-center justify-between">
              <div>
                <span className="text-[11px] text-slate-400 uppercase font-semibold">Benefit Value</span>
                <p className="text-lg font-extrabold text-slate-900 dark:text-white">
                  {sch.calculation_type === "PERCENTAGE" ? `${sch.value}% Waiver` : `₹${sch.value.toLocaleString("en-IN")}`}
                </p>
              </div>
              <span className="text-xs text-slate-500">Max: {sch.max_beneficiaries} seats</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
