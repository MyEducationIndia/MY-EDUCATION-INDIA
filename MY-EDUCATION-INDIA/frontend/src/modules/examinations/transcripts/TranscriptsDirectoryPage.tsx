import React, { useState } from "react";
import { FileText, Download, QrCode, ShieldCheck } from "lucide-react";

export const TranscriptsDirectoryPage: React.FC = () => {
  const [transcripts] = useState([
    { id: "1", trnNumber: "TRN-MEI-2026-F982A1", student: "Ananya Iyer", roll: "MEI-2026-CS-0043", cgpa: 9.85, type: "Semester 1 Grade Card", issued: "2026-11-06" },
    { id: "2", trnNumber: "TRN-MEI-2026-C441E2", student: "Aarav Sharma", roll: "MEI-2026-CS-0042", cgpa: 9.72, type: "Semester 1 Grade Card", issued: "2026-11-06" },
    { id: "3", trnNumber: "TRN-MEI-2026-B110D8", student: "Diya Nair", roll: "MEI-2026-CS-0045", cgpa: 9.60, type: "Semester 1 Grade Card", issued: "2026-11-06" },
  ]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <FileText className="h-7 w-7 text-amber-500" />
            Official Transcripts & Grade Cards
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Digitally signed transcripts, semester marksheets, and migration certificates with QR validation.
          </p>
        </div>
      </div>

      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 overflow-hidden shadow-xs">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 dark:bg-slate-700/50 text-xs uppercase text-slate-500 font-semibold border-b border-slate-200 dark:border-slate-700">
            <tr>
              <th className="px-6 py-3.5">Transcript Serial</th>
              <th className="px-6 py-3.5">Student Name</th>
              <th className="px-6 py-3.5">Final CGPA</th>
              <th className="px-6 py-3.5">Document Type</th>
              <th className="px-6 py-3.5">Issue Date</th>
              <th className="px-6 py-3.5 text-center">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-700/60">
            {transcripts.map((t) => (
              <tr key={t.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-700/30">
                <td className="px-6 py-4 font-mono text-xs font-bold text-slate-900 dark:text-white">{t.trnNumber}</td>
                <td className="px-6 py-4 font-bold text-slate-900 dark:text-white">{t.student}</td>
                <td className="px-6 py-4 font-extrabold text-emerald-600 dark:text-emerald-400">{t.cgpa}</td>
                <td className="px-6 py-4 text-xs font-semibold text-slate-700 dark:text-slate-300">{t.type}</td>
                <td className="px-6 py-4 text-xs text-slate-500">{t.issued}</td>
                <td className="px-6 py-4 text-center">
                  <button
                    type="button"
                    onClick={() => alert(`Downloading Transcript: ${t.trnNumber}`)}
                    className="inline-flex items-center gap-1 rounded-lg bg-indigo-600 px-3 py-1.5 text-xs font-bold text-white hover:bg-indigo-700"
                  >
                    <Download className="h-3.5 w-3.5" />
                    <span>Download PDF</span>
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
