import React, { useState } from "react";
import { QrCode, Download, Printer, ShieldCheck, CheckCircle2 } from "lucide-react";

export const HallTicketsPage: React.FC = () => {
  const [hallTickets] = useState([
    { id: "1", htNumber: "HT-NOV2026-CS0042", student: "Aarav Sharma", roll: "MEI-2026-CS-0042", room: "Hall A-102", seat: "A-12", status: "ISSUED" },
    { id: "2", htNumber: "HT-NOV2026-CS0043", student: "Ananya Iyer", roll: "MEI-2026-CS-0043", room: "Hall A-102", seat: "A-14", status: "ISSUED" },
    { id: "3", htNumber: "HT-NOV2026-CS0045", student: "Diya Nair", roll: "MEI-2026-CS-0045", room: "Hall A-102", seat: "A-16", status: "ISSUED" },
  ]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <QrCode className="h-7 w-7 text-amber-500" />
            Automated Examination Hall Tickets (Admit Cards)
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Generate and distribute verified admit cards with student photos, seating plan & optical QR codes.
          </p>
        </div>
        <button
          type="button"
          onClick={() => alert("Batch generate hall tickets")}
          className="flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-xs hover:bg-indigo-700 transition"
        >
          <Printer className="h-4 w-4" />
          <span>Batch Print Admit Cards</span>
        </button>
      </div>

      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 overflow-hidden shadow-xs">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 dark:bg-slate-700/50 text-xs uppercase text-slate-500 font-semibold border-b border-slate-200 dark:border-slate-700">
            <tr>
              <th className="px-6 py-3.5">Hall Ticket Number</th>
              <th className="px-6 py-3.5">Student Name</th>
              <th className="px-6 py-3.5">Assigned Hall & Seat</th>
              <th className="px-6 py-3.5">Verification</th>
              <th className="px-6 py-3.5">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-700/60">
            {hallTickets.map((ht) => (
              <tr key={ht.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-700/30">
                <td className="px-6 py-4 font-mono text-xs font-bold text-slate-900 dark:text-white">
                  {ht.htNumber}
                </td>
                <td className="px-6 py-4">
                  <p className="font-bold text-slate-900 dark:text-white">{ht.student}</p>
                  <p className="font-mono text-xs text-slate-500">{ht.roll}</p>
                </td>
                <td className="px-6 py-4 text-xs font-semibold text-slate-700 dark:text-slate-300">
                  {ht.room} (Seat {ht.seat})
                </td>
                <td className="px-6 py-4 text-xs text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
                  <ShieldCheck className="h-4 w-4" />
                  <span>Fee & Attendance Cleared</span>
                </td>
                <td className="px-6 py-4">
                  <span className="inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-semibold bg-emerald-50 text-emerald-600 dark:bg-emerald-950/60">
                    <CheckCircle2 className="h-3.5 w-3.5" />
                    {ht.status}
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
