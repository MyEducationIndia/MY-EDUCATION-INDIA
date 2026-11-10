import React, { useState } from "react";
import { FileCheck, Save, Upload, Check } from "lucide-react";

export const MarkEntryGridPage: React.FC = () => {
  const [marks, setMarks] = useState([
    { id: "1", roll: "MEI-2026-CS-0042", name: "Aarav Sharma", internal: 28, external: 62, practical: 0, grace: 0, total: 90 },
    { id: "2", roll: "MEI-2026-CS-0043", name: "Ananya Iyer", internal: 30, external: 68, practical: 0, grace: 0, total: 98 },
    { id: "3", roll: "MEI-2026-CS-0045", name: "Diya Nair", internal: 26, external: 65, practical: 0, grace: 0, total: 91 },
    { id: "4", roll: "MEI-2026-CS-0046", name: "Rohan Deshmukh", internal: 24, external: 55, practical: 0, grace: 0, total: 79 },
  ]);

  const updateMark = (id: string, field: "internal" | "external" | "grace", val: number) => {
    setMarks(
      marks.map((m) => {
        if (m.id === id) {
          const updated = { ...m, [field]: val };
          updated.total = updated.internal + updated.external + updated.practical + updated.grace;
          return updated;
        }
        return m;
      })
    );
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <FileCheck className="h-7 w-7 text-amber-500" />
            Subject Mark Entry & Moderation Ledger
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Internal assessment, external theory, practical, grace marks, and automated moderation adjustments.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => alert("Excel uploaded")}
            className="flex items-center gap-1.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-2 text-xs font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 transition"
          >
            <Upload className="h-4 w-4" />
            <span>Bulk Excel Upload</span>
          </button>
          <button
            type="button"
            onClick={() => alert("Marks saved")}
            className="flex items-center gap-1.5 rounded-lg bg-indigo-600 px-4 py-2 text-xs font-bold text-white shadow-xs hover:bg-indigo-700 transition"
          >
            <Save className="h-4 w-4" />
            <span>Save Marks Ledger</span>
          </button>
        </div>
      </div>

      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 overflow-hidden shadow-xs">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 dark:bg-slate-700/50 text-xs uppercase text-slate-500 font-semibold border-b border-slate-200 dark:border-slate-700">
            <tr>
              <th className="px-6 py-3.5">Roll Number</th>
              <th className="px-6 py-3.5">Student Name</th>
              <th className="px-4 py-3.5">Internal (Max 30)</th>
              <th className="px-4 py-3.5">External (Max 70)</th>
              <th className="px-4 py-3.5">Grace Marks</th>
              <th className="px-6 py-3.5">Total (100)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-700/60">
            {marks.map((m) => (
              <tr key={m.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-700/30">
                <td className="px-6 py-4 font-mono text-xs font-bold text-slate-900 dark:text-white">{m.roll}</td>
                <td className="px-6 py-4 font-bold text-slate-900 dark:text-white">{m.name}</td>
                <td className="px-4 py-4">
                  <input
                    type="number"
                    value={m.internal}
                    onChange={(e) => updateMark(m.id, "internal", Number(e.target.value))}
                    className="w-20 rounded-md border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 py-1 px-2 text-xs font-bold"
                  />
                </td>
                <td className="px-4 py-4">
                  <input
                    type="number"
                    value={m.external}
                    onChange={(e) => updateMark(m.id, "external", Number(e.target.value))}
                    className="w-20 rounded-md border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 py-1 px-2 text-xs font-bold"
                  />
                </td>
                <td className="px-4 py-4">
                  <input
                    type="number"
                    value={m.grace}
                    onChange={(e) => updateMark(m.id, "grace", Number(e.target.value))}
                    className="w-20 rounded-md border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 py-1 px-2 text-xs font-bold"
                  />
                </td>
                <td className="px-6 py-4 font-black text-slate-900 dark:text-white">{m.total}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
