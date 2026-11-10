import React from "react";
import { Users, BookOpen, CheckSquare, Calendar, Award } from "lucide-react";

export const FacultyPortalPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <div className="bg-gradient-to-r from-slate-800 to-indigo-900 rounded-2xl p-6 text-white shadow-lg">
        <h1 className="text-2xl font-bold">Faculty Professor Command View</h1>
        <p className="text-slate-200 text-sm mt-1">Department of Computer Science & Engineering · Academic Session 2026-2027</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <span className="text-xs font-semibold text-gray-500 uppercase">Classes Today</span>
          <div className="text-2xl font-bold text-gray-900 mt-2">3 Lectures</div>
          <span className="text-xs text-indigo-600 font-medium">CS-301, CS-402, LAB-2</span>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <span className="text-xs font-semibold text-gray-500 uppercase">Pending Evaluations</span>
          <div className="text-2xl font-bold text-amber-600 mt-2">14 Submissions</div>
          <span className="text-xs text-gray-500">Distributed Systems Assignment 2</span>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <span className="text-xs font-semibold text-gray-500 uppercase">LXP Course Enrollments</span>
          <div className="text-2xl font-bold text-emerald-600 mt-2">184 Scholars</div>
          <span className="text-xs text-emerald-600 font-medium">94.2% Attendance Average</span>
        </div>
      </div>
    </div>
  );
};
