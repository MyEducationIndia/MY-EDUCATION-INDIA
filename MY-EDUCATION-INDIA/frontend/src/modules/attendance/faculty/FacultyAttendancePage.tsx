import React, { useState } from "react";
import { Briefcase, Clock, CheckCircle, LogIn, LogOut } from "lucide-react";

export const FacultyAttendancePage: React.FC = () => {
  const [facultyLogs, setFacultyLogs] = useState([
    { id: "1", name: "Dr. Vikram Sengupta", department: "Computer Science", inTime: "08:45 AM", outTime: "--", hours: 0.0, status: "PRESENT" },
    { id: "2", name: "Prof. Priya Ramaswamy", department: "Electronics", inTime: "08:52 AM", outTime: "--", hours: 0.0, status: "PRESENT" },
    { id: "3", name: "Dr. Amit Mukherjee", department: "Mechanical Engg", inTime: "09:05 AM", outTime: "--", hours: 0.0, status: "LATE" },
    { id: "4", name: "Dr. Shalini Verma", department: "Biotechnology", inTime: "--", outTime: "--", hours: 0.0, status: "LEAVE" },
  ]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <Briefcase className="h-7 w-7 text-indigo-600 dark:text-indigo-400" />
            Faculty Daily Biometric & Clock-in Log
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Real-time tracking of academic faculty clock-in, clock-out, working hours, and shift compliance.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => alert("Clock-In recorded")}
            className="flex items-center gap-1.5 rounded-lg bg-emerald-600 px-3 py-2 text-xs font-bold text-white hover:bg-emerald-700 transition"
          >
            <LogIn className="h-4 w-4" />
            <span>Clock In</span>
          </button>
          <button
            type="button"
            onClick={() => alert("Clock-Out recorded")}
            className="flex items-center gap-1.5 rounded-lg bg-rose-600 px-3 py-2 text-xs font-bold text-white hover:bg-rose-700 transition"
          >
            <LogOut className="h-4 w-4" />
            <span>Clock Out</span>
          </button>
        </div>
      </div>

      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 overflow-hidden shadow-xs">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 dark:bg-slate-700/50 text-xs uppercase text-slate-500 font-semibold border-b border-slate-200 dark:border-slate-700">
            <tr>
              <th className="px-6 py-3.5">Faculty Member</th>
              <th className="px-6 py-3.5">Department</th>
              <th className="px-6 py-3.5">In Time</th>
              <th className="px-6 py-3.5">Out Time</th>
              <th className="px-6 py-3.5">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-700/60">
            {facultyLogs.map((f) => (
              <tr key={f.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-700/30">
                <td className="px-6 py-4 font-bold text-slate-900 dark:text-white">{f.name}</td>
                <td className="px-6 py-4 text-xs text-slate-600 dark:text-slate-300">{f.department}</td>
                <td className="px-6 py-4 text-xs font-mono font-bold text-slate-800 dark:text-slate-200">{f.inTime}</td>
                <td className="px-6 py-4 text-xs font-mono font-bold text-slate-800 dark:text-slate-200">{f.outTime}</td>
                <td className="px-6 py-4">
                  <span
                    className={`inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-semibold ${
                      f.status === "PRESENT"
                        ? "bg-emerald-50 text-emerald-600 dark:bg-emerald-950/60"
                        : f.status === "LATE"
                        ? "bg-amber-50 text-amber-600 dark:bg-amber-950/60"
                        : "bg-rose-50 text-rose-600 dark:bg-rose-950/60"
                    }`}
                  >
                    {f.status}
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
