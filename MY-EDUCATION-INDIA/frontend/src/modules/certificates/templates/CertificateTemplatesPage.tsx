import React, { useState } from "react";
import { Layers, Plus, FileText, CheckCircle2 } from "lucide-react";

export const CertificateTemplatesPage: React.FC = () => {
  const [templates] = useState([
    { id: "1", code: "DEGREE-BTECH-2026", title: "B.Tech Degree in Computer Science & AI", orientation: "LANDSCAPE", size: "A4", status: "ACTIVE" },
    { id: "2", code: "BONAFIDE-GEN-2026", title: "General Student Bonafide Certificate", orientation: "PORTRAIT", size: "A4", status: "ACTIVE" },
    { id: "3", code: "TC-ACAD-2026", title: "Institutional Transfer Certificate (TC)", orientation: "PORTRAIT", size: "A4", status: "ACTIVE" },
    { id: "4", code: "ID-STUDENT-CR80", title: "Smart Student Campus ID Card", orientation: "LANDSCAPE", size: "ID_CARD_CR80", status: "ACTIVE" },
  ]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <Layers className="h-7 w-7 text-teal-600 dark:text-teal-400" />
            Certificate & Document Template Library
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Define multi-page layout templates, custom borders, watermarks, dynamic field placeholders & typography.
          </p>
        </div>
        <button
          type="button"
          onClick={() => alert("Create Template")}
          className="flex items-center gap-2 rounded-lg bg-teal-600 px-4 py-2 text-sm font-semibold text-white shadow-xs hover:bg-teal-700 transition"
        >
          <Plus className="h-4 w-4" />
          <span>New Document Template</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {templates.map((t) => (
          <div
            key={t.id}
            className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs"
          >
            <div className="flex items-center justify-between">
              <span className="font-mono text-xs font-bold text-teal-600 bg-teal-50 dark:bg-teal-950 px-2 py-0.5 rounded-sm">
                {t.code}
              </span>
              <span className="flex items-center gap-1 text-[11px] font-semibold text-emerald-600">
                <CheckCircle2 className="h-3 w-3" /> {t.status}
              </span>
            </div>
            <h3 className="mt-2 text-base font-bold text-slate-900 dark:text-white">{t.title}</h3>
            <p className="mt-1 text-xs text-slate-500">
              Format: {t.size} ({t.orientation})
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};
