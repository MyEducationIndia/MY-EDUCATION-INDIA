import React, { useState } from "react";
import { Sliders, CheckCircle } from "lucide-react";

export const GradeScaleConfigPage: React.FC = () => {
  const [scale] = useState([
    { grade: "O", point: 10.0, range: "90% - 100%", desc: "Outstanding", passing: true },
    { grade: "A+", point: 9.0, range: "80% - 89.9%", desc: "Excellent", passing: true },
    { grade: "A", point: 8.0, range: "70% - 79.9%", desc: "Very Good", passing: true },
    { grade: "B+", point: 7.0, range: "60% - 69.9%", desc: "Good", passing: true },
    { grade: "B", point: 6.0, range: "55% - 59.9%", desc: "Above Average", passing: true },
    { grade: "C", point: 5.0, range: "50% - 54.9%", desc: "Average", passing: true },
    { grade: "P", point: 4.0, range: "40% - 49.9%", desc: "Pass", passing: true },
    { grade: "F", point: 0.0, range: "Below 40%", desc: "Fail / Backlog", passing: false },
  ]);

  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-5 dark:border-slate-800">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
          <Sliders className="h-7 w-7 text-amber-500" />
          UGC/AICTE Statutory CBCS & NEP 10-Point Grade Scales
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Standardized letter grades, grade points, and percentage conversion matrix.
        </p>
      </div>

      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 overflow-hidden shadow-xs">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 dark:bg-slate-700/50 text-xs uppercase text-slate-500 font-semibold border-b border-slate-200 dark:border-slate-700">
            <tr>
              <th className="px-6 py-3.5">Letter Grade</th>
              <th className="px-6 py-3.5">Grade Point</th>
              <th className="px-6 py-3.5">Percentage Band</th>
              <th className="px-6 py-3.5">Qualitative Description</th>
              <th className="px-6 py-3.5">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-700/60">
            {scale.map((s) => (
              <tr key={s.grade} className="hover:bg-slate-50/50 dark:hover:bg-slate-700/30">
                <td className="px-6 py-4 font-black text-base text-slate-900 dark:text-white">{s.grade}</td>
                <td className="px-6 py-4 font-bold text-indigo-600 dark:text-indigo-400">{s.point.toFixed(1)}</td>
                <td className="px-6 py-4 text-xs font-semibold text-slate-600 dark:text-slate-300">{s.range}</td>
                <td className="px-6 py-4 text-xs text-slate-500">{s.desc}</td>
                <td className="px-6 py-4">
                  <span
                    className={`inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-semibold ${
                      s.passing
                        ? "bg-emerald-50 text-emerald-600 dark:bg-emerald-950/60"
                        : "bg-rose-50 text-rose-600 dark:bg-rose-950/60"
                    }`}
                  >
                    {s.passing ? "Passing" : "Failure"}
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
