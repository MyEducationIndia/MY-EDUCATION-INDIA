import React, { useState } from "react";
import { Plus, CheckCircle2, Download, Printer } from "lucide-react";

export const BulkDocumentGeneratorPage: React.FC = () => {
  const [selectedTemplate, setSelectedTemplate] = useState("DEGREE-BTECH-2026");
  const [selectedBatch, setSelectedBatch] = useState("BTECH-CSE-2026-A");

  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-5 dark:border-slate-800">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
          <Plus className="h-7 w-7 text-teal-600 dark:text-teal-400" />
          Batch Document & Certificate Generator
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Bulk generate degree certificates, bonafides, or transcripts with automated Universal Numbering and QR codes.
        </p>
      </div>

      <div className="max-w-2xl rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs space-y-4">
        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-1.5">Document Template</label>
          <select
            value={selectedTemplate}
            onChange={(e) => setSelectedTemplate(e.target.value)}
            className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 py-2 px-3 text-sm font-semibold"
          >
            <option value="DEGREE-BTECH-2026">B.Tech Degree in Computer Science & AI</option>
            <option value="BONAFIDE-GEN-2026">General Student Bonafide Certificate</option>
            <option value="TC-ACAD-2026">Institutional Transfer Certificate (TC)</option>
          </select>
        </div>

        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-1.5">Target Student Cohort</label>
          <select
            value={selectedBatch}
            onChange={(e) => setSelectedBatch(e.target.value)}
            className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 py-2 px-3 text-sm font-semibold"
          >
            <option value="BTECH-CSE-2026-A">B.Tech CSE 2026 (Section A - 60 Students)</option>
            <option value="BTECH-CSE-2026-B">B.Tech CSE 2026 (Section B - 60 Students)</option>
            <option value="MBA-2026">MBA Executive 2026 (60 Students)</option>
          </select>
        </div>

        <button
          type="button"
          onClick={() => alert("Batch job initiated in background: 60 certificates queued with unique QR tokens!")}
          className="w-full flex items-center justify-center gap-2 rounded-lg bg-teal-600 py-3 text-sm font-bold text-white shadow-xs hover:bg-teal-700 transition"
        >
          <CheckCircle2 className="h-5 w-5" />
          <span>Queue Bulk Generation Job (60 Credentials)</span>
        </button>
      </div>
    </div>
  );
};
