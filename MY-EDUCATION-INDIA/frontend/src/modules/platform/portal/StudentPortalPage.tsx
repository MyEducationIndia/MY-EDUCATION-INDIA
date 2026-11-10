import React from "react";
import { BookOpen, Calendar, Clock, Award, FileCheck2, IndianRupee } from "lucide-react";

export const StudentPortalPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <div className="bg-gradient-to-r from-indigo-600 to-blue-600 rounded-2xl p-6 text-white shadow-lg">
        <h1 className="text-2xl font-bold">Welcome back, Scholar</h1>
        <p className="text-indigo-100 text-sm mt-1">B.Tech Computer Science & Engineering · Semester VI · Roll #2024-CSE-042</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <span className="text-xs font-semibold text-gray-500 uppercase">My Attendance</span>
          <div className="text-2xl font-bold text-gray-900 mt-2">91.5%</div>
          <span className="text-xs text-emerald-600 font-medium">Eligible for Final Examinations</span>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <span className="text-xs font-semibold text-gray-500 uppercase">Fee Status</span>
          <div className="text-2xl font-bold text-emerald-600 mt-2">NO DUES</div>
          <span className="text-xs text-gray-500">Annual Tuition Cleared</span>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <span className="text-xs font-semibold text-gray-500 uppercase">Active LXP Courses</span>
          <div className="text-2xl font-bold text-indigo-600 mt-2">6 Tracks</div>
          <span className="text-xs text-indigo-600 font-medium">12 Day Learning Streak 🔥</span>
        </div>
      </div>
    </div>
  );
};
