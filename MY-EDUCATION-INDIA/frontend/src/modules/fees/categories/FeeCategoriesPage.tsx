import React, { useState } from "react";
import { PlusCircle, Tag, Check, IndianRupee } from "lucide-react";
import { FeeCategory, FeeHead } from "../types/fee.types";

export const FeeCategoriesPage: React.FC = () => {
  const [categories, setCategories] = useState<FeeCategory[]>([
    { id: "fc-1", code: "TUITION", name: "Tuition & Instruction Fees", institute_id: "inst-1", is_active: true, created_at: "" },
    { id: "fc-2", code: "ADMISSION", name: "Registration & Admission", institute_id: "inst-1", is_active: true, created_at: "" },
    { id: "fc-3", code: "LAB", name: "Laboratory & Technology", institute_id: "inst-1", is_active: true, created_at: "" },
    { id: "fc-4", code: "EXAM", name: "Examination & Assessment", institute_id: "inst-1", is_active: true, created_at: "" },
    { id: "fc-5", code: "HOSTEL", name: "Hostel & Accommodation", institute_id: "inst-1", is_active: true, created_at: "" },
    { id: "fc-6", code: "TRANSPORT", name: "Campus Transport Service", institute_id: "inst-1", is_active: true, created_at: "" },
  ]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <Tag className="h-7 w-7 text-emerald-600 dark:text-emerald-400" />
            Fee Categories & Account Heads
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Configure unlimited institutional fee categories and designated accounting heads.
          </p>
        </div>
        <button
          type="button"
          onClick={() => alert("Create Category modal")}
          className="flex items-center gap-2 rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold text-white shadow-xs hover:bg-emerald-700 transition"
        >
          <PlusCircle className="h-4 w-4" />
          <span>Add Fee Category</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {categories.map((c) => (
          <div
            key={c.id}
            className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs"
          >
            <div className="flex items-center justify-between">
              <span className="font-mono text-xs font-bold text-slate-500 bg-slate-100 dark:bg-slate-700 px-2 py-0.5 rounded-sm">
                {c.code}
              </span>
              <span className="flex items-center gap-1 text-[11px] font-semibold text-emerald-600 dark:text-emerald-400">
                <Check className="h-3 w-3" /> Active
              </span>
            </div>
            <h3 className="mt-3 text-base font-bold text-slate-900 dark:text-white">{c.name}</h3>
            <p className="mt-1 text-xs text-slate-500">Universal institutional accounting head</p>
          </div>
        ))}
      </div>
    </div>
  );
};
