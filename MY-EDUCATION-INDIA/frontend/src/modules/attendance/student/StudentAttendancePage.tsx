import React, { useState } from "react";
import { Users, CheckCircle, XCircle, Clock, Save, Filter } from "lucide-react";

export const StudentAttendancePage: React.FC = () => {
  const [selectedBatch, setSelectedBatch] = useState("BTECH-CSE-2026-A");
  const [sessionDate, setSessionDate] = useState("2026-11-06");
  const [period, setPeriod] = useState("Period 1 (09:00 - 10:00 AM)");
  const [students, setStudents] = useState([
    { id: "stu-1", name: "Aarav Sharma", roll: "MEI-2026-CS-0042", status: "PRESENT" },
    { id: "stu-2", name: "Ananya Iyer", roll: "MEI-2026-CS-0043", status: "PRESENT" },
    { id: "stu-3", name: "Kabir Patel", roll: "MEI-2026-CS-0044", status: "ABSENT" },
    { id: "stu-4", name: "Diya Nair", roll: "MEI-2026-CS-0045", status: "LATE" },
    { id: "stu-5", name: "Rohan Deshmukh", roll: "MEI-2026-CS-0046", status: "PRESENT" },
    { id: "stu-6", name: "Isha Kapoor", roll: "MEI-2026-CS-0047", status: "ON_DUTY" },
  ]);

  const toggleStatus = (id: string, newStatus: string) => {
    setStudents(students.map((s) => (s.id === id ? { ...s, status: newStatus } : s)));
  };

  const markAll = (status: string) => {
    setStudents(students.map((s) => ({ ...s, status })));
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <Users className="h-7 w-7 text-indigo-600 dark:text-indigo-400" />
            Classroom Student Roll Call
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Mark daily or period-wise student attendance with one-click status overrides.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => markAll("PRESENT")}
            className="rounded-lg bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-300 dark:border-emerald-800 px-3 py-2 text-xs font-bold text-emerald-700 dark:text-emerald-300 hover:bg-emerald-100 transition"
          >
            Mark All Present
          </button>
          <button
            type="button"
            onClick={() => alert("Attendance saved successfully!")}
            className="flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-xs font-bold text-white shadow-xs hover:bg-indigo-700 transition"
          >
            <Save className="h-4 w-4" />
            <span>Save Roll Call</span>
          </button>
        </div>
      </div>

      {/* Filter Options */}
      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-4 shadow-xs flex flex-wrap items-center gap-4">
        <div>
          <label className="block text-[11px] font-bold uppercase text-slate-400 mb-1">Batch & Section</label>
          <select
            value={selectedBatch}
            onChange={(e) => setSelectedBatch(e.target.value)}
            className="rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/50 py-1.5 px-3 text-xs text-slate-800 dark:text-slate-200"
          >
            <option value="BTECH-CSE-2026-A">B.Tech CSE 2026 - Section A</option>
            <option value="BTECH-CSE-2026-B">B.Tech CSE 2026 - Section B</option>
            <option value="MBA-2026">MBA Executive 2026</option>
          </select>
        </div>
        <div>
          <label className="block text-[11px] font-bold uppercase text-slate-400 mb-1">Session Date</label>
          <input
            type="date"
            value={sessionDate}
            onChange={(e) => setSessionDate(e.target.value)}
            className="rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/50 py-1.5 px-3 text-xs text-slate-800 dark:text-slate-200"
          />
        </div>
        <div>
          <label className="block text-[11px] font-bold uppercase text-slate-400 mb-1">Period</label>
          <select
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
            className="rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/50 py-1.5 px-3 text-xs text-slate-800 dark:text-slate-200"
          >
            <option>Period 1 (09:00 - 10:00 AM)</option>
            <option>Period 2 (10:00 - 11:00 AM)</option>
            <option>Period 3 (11:15 - 12:15 PM)</option>
            <option>Period 4 (01:00 - 02:00 PM)</option>
          </select>
        </div>
      </div>

      {/* Roster Table */}
      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 overflow-hidden shadow-xs">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 dark:bg-slate-700/50 text-xs uppercase text-slate-500 font-semibold border-b border-slate-200 dark:border-slate-700">
            <tr>
              <th className="px-6 py-3.5">Roll Number</th>
              <th className="px-6 py-3.5">Student Name</th>
              <th className="px-6 py-3.5 text-center">Status Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-700/60">
            {students.map((st) => (
              <tr key={st.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-700/30">
                <td className="px-6 py-4 font-mono text-xs font-bold text-slate-900 dark:text-white">
                  {st.roll}
                </td>
                <td className="px-6 py-4 font-bold text-slate-900 dark:text-white">
                  {st.name}
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center justify-center gap-2">
                    {["PRESENT", "ABSENT", "LATE", "ON_DUTY"].map((statusOption) => (
                      <button
                        key={statusOption}
                        type="button"
                        onClick={() => toggleStatus(st.id, statusOption)}
                        className={`rounded-md px-3 py-1 text-xs font-bold border transition ${
                          st.status === statusOption
                            ? statusOption === "PRESENT"
                              ? "bg-emerald-600 text-white border-emerald-600"
                              : statusOption === "ABSENT"
                              ? "bg-rose-600 text-white border-rose-600"
                              : statusOption === "LATE"
                              ? "bg-amber-600 text-white border-amber-600"
                              : "bg-blue-600 text-white border-blue-600"
                            : "border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:bg-slate-100"
                        }`}
                      >
                        {statusOption.replace("_", " ")}
                      </button>
                    ))}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
