import React, { useState } from "react";
import { Clock, LogIn, LogOut, CheckCircle } from "lucide-react";

export const StaffAttendancePage: React.FC = () => {
  const [staffLogs] = useState([
    { id: "1", name: "Sunil Joshi", role: "Chief Accountant", shift: "General (09:00 - 17:30)", inTime: "08:50 AM", outTime: "--", status: "PRESENT" },
    { id: "2", name: "Meena Nair", role: "Head Librarian", shift: "General (09:00 - 17:30)", inTime: "08:55 AM", outTime: "--", status: "PRESENT" },
    { id: "3", name: "Gopal Yadav", role: "Campus Security Officer", shift: "Morning Shift (06:00 - 14:00)", inTime: "05:55 AM", outTime: "14:00 PM", status: "COMPLETED" },
  ]);

  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-5 dark:border-slate-800">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
          <Clock className="h-7 w-7 text-indigo-600 dark:text-indigo-400" />
          Administrative & Support Staff Shift Terminal
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Monitor staff shifts, break times, overtime eligibility, and daily presence logs.
        </p>
      </div>

      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 overflow-hidden shadow-xs">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 dark:bg-slate-700/50 text-xs uppercase text-slate-500 font-semibold border-b border-slate-200 dark:border-slate-700">
            <tr>
              <th className="px-6 py-3.5">Staff Member</th>
              <th className="px-6 py-3.5">Assigned Role</th>
              <th className="px-6 py-3.5">Shift Window</th>
              <th className="px-6 py-3.5">In Time</th>
              <th className="px-6 py-3.5">Out Time</th>
              <th className="px-6 py-3.5">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-700/60">
            {staffLogs.map((s) => (
              <tr key={s.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-700/30">
                <td className="px-6 py-4 font-bold text-slate-900 dark:text-white">{s.name}</td>
                <td className="px-6 py-4 text-xs text-slate-600 dark:text-slate-300">{s.role}</td>
                <td className="px-6 py-4 text-xs text-slate-500">{s.shift}</td>
                <td className="px-6 py-4 text-xs font-mono font-bold text-slate-800 dark:text-slate-200">{s.inTime}</td>
                <td className="px-6 py-4 text-xs font-mono font-bold text-slate-800 dark:text-slate-200">{s.outTime}</td>
                <td className="px-6 py-4">
                  <span className="inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-semibold bg-emerald-50 text-emerald-600 dark:bg-emerald-950/60">
                    {s.status}
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
