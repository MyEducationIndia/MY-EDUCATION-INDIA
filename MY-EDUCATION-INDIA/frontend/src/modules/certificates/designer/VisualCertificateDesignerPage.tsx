import React, { useState } from "react";
import { FileBadge, Save, Eye, Layers, Type, Image as ImageIcon, QrCode } from "lucide-react";

export const VisualCertificateDesignerPage: React.FC = () => {
  const [templateName, setTemplateName] = useState("Degree of Bachelor of Technology");
  const [orientation, setOrientation] = useState("LANDSCAPE");

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <FileBadge className="h-7 w-7 text-teal-600 dark:text-teal-400" />
            Visual Certificate & Document Layout Designer
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Drag-and-drop elements: institutional seals, dynamic placeholders, signatures, and tamper-proof verification QR codes.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => alert("Preview rendered HTML")}
            className="flex items-center gap-1.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-2 text-xs font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 transition"
          >
            <Eye className="h-4 w-4" />
            <span>Live Preview</span>
          </button>
          <button
            type="button"
            onClick={() => alert("Template saved successfully")}
            className="flex items-center gap-1.5 rounded-lg bg-teal-600 px-4 py-2 text-xs font-bold text-white shadow-xs hover:bg-teal-700 transition"
          >
            <Save className="h-4 w-4" />
            <span>Save Designer Layout</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Tool Palette */}
        <div className="lg:col-span-1 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">Layout Palette</h3>
          <div className="space-y-2">
            <div className="flex items-center gap-2.5 p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 cursor-move text-xs font-semibold">
              <Type className="h-4 w-4 text-teal-600" />
              <span>Dynamic Text Placeholder</span>
            </div>
            <div className="flex items-center gap-2.5 p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 cursor-move text-xs font-semibold">
              <ImageIcon className="h-4 w-4 text-teal-600" />
              <span>Institutional Crest / Logo</span>
            </div>
            <div className="flex items-center gap-2.5 p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 cursor-move text-xs font-semibold">
              <QrCode className="h-4 w-4 text-teal-600" />
              <span>Verification QR Code</span>
            </div>
          </div>
        </div>

        {/* Canvas Workspace */}
        <div className="lg:col-span-3 rounded-xl border-2 border-dashed border-slate-300 dark:border-slate-700 bg-slate-100 dark:bg-slate-900 p-8 flex flex-col items-center justify-center min-h-[460px]">
          <div className="w-full max-w-2xl bg-white dark:bg-slate-800 rounded-lg shadow-xl border-8 border-double border-amber-600 p-8 text-center space-y-4">
            <h2 className="text-xl font-serif font-bold text-slate-900 dark:text-white uppercase tracking-widest">MY EDUCATION INDIA</h2>
            <p className="text-xs text-slate-500 italic">Established under Section 2(f) of the UGC Act, 1956</p>
            <div className="py-4">
              <p className="text-sm font-serif text-slate-700 dark:text-slate-300">This is to certify that</p>
              <h3 className="text-2xl font-serif font-black text-teal-700 dark:text-teal-400 mt-1">{"{{student_name}}"}</h3>
              <p className="text-xs text-slate-500 mt-1">Enrollment No: {"{{enrollment_number}}"}</p>
              <p className="text-sm font-serif text-slate-700 dark:text-slate-300 mt-3">
                has successfully completed the curriculum and examinations for the degree of
              </p>
              <h4 className="text-lg font-serif font-bold text-slate-900 dark:text-white mt-1">{"{{course_name}}"}</h4>
              <p className="text-xs text-slate-500 mt-1">with CGPA: {"{{cgpa}}"} ({"{{classification}}"})</p>
            </div>
            <div className="flex justify-between items-end pt-4 border-t border-slate-200 dark:border-slate-700 text-xs text-slate-500">
              <div>
                <span>Issue Date: {"{{issue_date}}"}</span>
              </div>
              <div className="flex flex-col items-center">
                <QrCode className="h-10 w-10 text-slate-700 dark:text-slate-300 mb-1" />
                <span className="text-[10px]">Verify Credential</span>
              </div>
              <div>
                <p className="font-serif font-bold text-slate-900 dark:text-white">Registrar</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
