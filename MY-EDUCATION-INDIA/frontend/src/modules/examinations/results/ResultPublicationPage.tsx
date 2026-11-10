import React, { useState } from "react";
import { Award, CheckCircle2, AlertCircle, Share2, Printer } from "lucide-react";

export const ResultPublicationPage: React.FC = () => {
  const [results] = useState([
    { id: "1", roll: "MEI-2026-CS-0043", name: "Ananya Iyer", credits: 24, sgpa: 9.85, cgpa: 9.85, status: "PASSED", classification: "First Class with Distinction", backlogs: 0 },
    { id: "2", roll: "MEI-2026-CS-0042", name: "Aarav Sharma", credits: 24, sgpa: 9.72, cgpa: 9.72, status: "PASSED", classification: "First Class with Distinction", backlogs: 0 },
    { id: "3", roll: "MEI-2026-CS-0045", name: "Diya Nair", credits: 24, sgpa: 9.60, cgpa: 9.60, status: "PASSED", classification: "First Class with Distinction", backlogs: 0 },
    { id: "4", roll: "MEI-2026-CS-0046", name: "Rohan Deshmukh", credits: 24, sgpa: 7.90, cgpa: 7.90, status: "PASSED", classification: "First Class", backlogs: 0 },
  ]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <Award className="h-7 w-7 text-amber-500" />
            Official Result Computation & Publication Center
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Publish finalized semester results, calculate SGPA/CGPA, and unlock student transcript downloads.
          </p>
        </div>
        <button
          type="button"
          onClick={() => alert("Published to student portal")}
          className="flex items-center gap-2 rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold text-white shadow-xs hover:bg-emerald-700 transition"
        >
          <Share2 className="h-4 w-4" />
          <span>Publish to Student Portal</span>
        </button>
      </div>

      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 overflow-hidden shadow-xs">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 dark:bg-slate-700/50 text-xs uppercase text-slate-500 font-semibold border-b border-slate-200 dark:border-slate-700">
            <tr>
              <th className="px-6 py-3.5">Student</th>
              <th className="px-6 py-3.5">Earned Credits</th>
              <th className="px-6 py-3.5">SGPA</th>
              <th className="px-6 py-3.5">CGPA</th>
              <th className="px-6 py-3.5">Classification</th>
              <th className="px-6 py-3.5">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-700/60">
            {results.map((r) => (
              <tr key={r.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-700/30">
                <td className="px-6 py-4">
                  <p className="font-bold text-slate-900 dark:text-white">{r.name}</p>
                  <p className="font-mono text-xs text-slate-500">{r.roll}</p>
                </td>
                <td className="px-6 py-4 font-bold text-slate-900 dark:text-white">{r.credits} Credits</td>
                <td className="px-6 py-4 font-extrabold text-indigo-600 dark:text-indigo-400">{r.sgpa}</td>
                <td className="px-6 py-4 font-extrabold text-emerald-600 dark:text-emerald-400">{r.cgpa}</td>
                <td className="px-6 py-4 text-xs font-semibold text-slate-700 dark:text-slate-300">{r.classification}</td>
                <td className="px-6 py-4">
                  <span className="inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-semibold bg-emerald-50 text-emerald-600 dark:bg-emerald-950/60">
                    <CheckCircle2 className="h-3.5 w-3.5" />
                    {r.status}
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
