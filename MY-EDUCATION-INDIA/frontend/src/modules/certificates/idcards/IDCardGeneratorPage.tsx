import React, { useState } from "react";
import { Contact, Printer, Download, CheckCircle2 } from "lucide-react";

export const IDCardGeneratorPage: React.FC = () => {
  const [cards] = useState([
    { id: "1", cardNo: "ID-STU-8821941A", name: "Aarav Sharma", type: "STUDENT", roll: "MEI-2026-CS-0042", blood: "O+", valid: "2030-06-30" },
    { id: "2", cardNo: "ID-STU-8821941B", name: "Ananya Iyer", type: "STUDENT", roll: "MEI-2026-CS-0043", blood: "A+", valid: "2030-06-30" },
    { id: "3", cardNo: "ID-FAC-4412909C", name: "Dr. Vikram Sengupta", type: "FACULTY", roll: "EMP-CS-012", blood: "B+", valid: "2029-12-31" },
  ]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <Contact className="h-7 w-7 text-teal-600 dark:text-teal-400" />
            Smart Campus Identity Cards & Visitor Badges
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Generate printable CR80 identity cards with 2D QR access tokens, emergency contacts, and blood groups.
          </p>
        </div>
        <button
          type="button"
          onClick={() => alert("Batch Print CR80 Cards")}
          className="flex items-center gap-2 rounded-lg bg-teal-600 px-4 py-2 text-sm font-semibold text-white shadow-xs hover:bg-teal-700 transition"
        >
          <Printer className="h-4 w-4" />
          <span>Batch Print CR80 ID Cards</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {cards.map((c) => (
          <div
            key={c.id}
            className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs flex flex-col justify-between"
          >
            <div>
              <div className="flex justify-between items-center border-b border-slate-100 dark:border-slate-700 pb-3">
                <span className="font-bold text-xs text-teal-600">MY EDUCATION INDIA</span>
                <span className="text-[11px] font-bold uppercase bg-teal-50 dark:bg-teal-950 px-2 py-0.5 rounded-sm text-teal-700 dark:text-teal-300">{c.type}</span>
              </div>
              <div className="mt-4 flex gap-3">
                <div className="h-16 w-14 bg-slate-200 dark:bg-slate-700 rounded-md flex items-center justify-center text-xs text-slate-400">
                  PHOTO
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900 dark:text-white">{c.name}</h3>
                  <p className="font-mono text-xs text-slate-500">{c.roll}</p>
                  <p className="text-xs text-slate-500 mt-1">Blood Group: {c.blood}</p>
                </div>
              </div>
            </div>
            <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-700 flex justify-between items-center text-[11px] text-slate-400">
              <span className="font-mono">{c.cardNo}</span>
              <span>Valid Thru: {c.valid}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
