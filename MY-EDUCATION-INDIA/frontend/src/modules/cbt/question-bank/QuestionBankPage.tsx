import React, { useState } from "react";
import { Layers, Plus, Upload, Filter, CheckCircle2 } from "lucide-react";

export const QuestionBankPage: React.FC = () => {
  const [banks] = useState([
    { id: "1", code: "CS101-BANK", name: "Data Structures & Algorithms Repository", questionsCount: 420, topics: 14, status: "ACTIVE" },
    { id: "2", code: "CS102-BANK", name: "Object Oriented Java Concepts", questionsCount: 350, topics: 10, status: "ACTIVE" },
    { id: "3", code: "MBA201-BANK", name: "Corporate Financial Analysis", questionsCount: 280, topics: 8, status: "ACTIVE" },
  ]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <Layers className="h-7 w-7 text-cyan-600 dark:text-cyan-400" />
            Master Question Bank Repositories
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Categorized question bank covering MCQ, MSQ, Numerical, LaTeX formulas, and multi-media questions.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => alert("Bulk Question Import modal")}
            className="flex items-center gap-1.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-2 text-xs font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 transition"
          >
            <Upload className="h-4 w-4" />
            <span>Import Excel/JSON</span>
          </button>
          <button
            type="button"
            onClick={() => alert("Add question bank")}
            className="flex items-center gap-1.5 rounded-lg bg-cyan-600 px-3 py-2 text-xs font-bold text-white shadow-xs hover:bg-cyan-700 transition"
          >
            <Plus className="h-4 w-4" />
            <span>New Repository</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {banks.map((b) => (
          <div
            key={b.id}
            className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-cyan-600 bg-cyan-50 dark:bg-cyan-950 px-2 py-0.5 rounded-sm">
                  {b.code}
                </span>
                <span className="flex items-center gap-1 text-[11px] font-semibold text-emerald-600">
                  <CheckCircle2 className="h-3 w-3" /> {b.status}
                </span>
              </div>
              <h3 className="mt-3 text-base font-bold text-slate-900 dark:text-white">{b.name}</h3>
              <p className="mt-1 text-xs text-slate-500">{b.topics} Curricular Topics Defined</p>
            </div>
            <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-700 flex justify-between items-center text-xs">
              <span className="font-bold text-slate-900 dark:text-white">{b.questionsCount} Questions</span>
              <button
                type="button"
                onClick={() => alert(`Opening Question Editor for ${b.code}`)}
                className="text-cyan-600 font-bold hover:underline"
              >
                Manage Questions &rarr;
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
