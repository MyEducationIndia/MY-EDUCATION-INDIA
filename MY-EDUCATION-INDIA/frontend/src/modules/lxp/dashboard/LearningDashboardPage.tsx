import React from "react";
import { BookOpen, Flame, Award, Clock, CheckCircle2, PlayCircle, AlertCircle } from "lucide-react";

export const LearningDashboardPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Enterprise Learning Experience Platform</h1>
          <p className="text-sm text-gray-500 mt-1">Adaptive curriculum tracks, video lectures, live assessments, and gamification</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Enrolled Courses</span>
            <div className="p-2 bg-indigo-50 text-indigo-600 rounded-lg"><BookOpen className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">6 Courses</div>
          <span className="text-xs text-emerald-600 font-medium">4 Active · 2 Completed</span>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Learning Streak</span>
            <div className="p-2 bg-amber-50 text-amber-600 rounded-lg"><Flame className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">12 Days</div>
          <span className="text-xs text-amber-600 font-medium">Daily Goal Achieved</span>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">XP Points & Badges</span>
            <div className="p-2 bg-purple-50 text-purple-600 rounded-lg"><Award className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">1,450 XP</div>
          <span className="text-xs text-purple-600 font-medium">Level 5 Scholar</span>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Watch & Study Time</span>
            <div className="p-2 bg-emerald-50 text-emerald-600 rounded-lg"><Clock className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">42.5 Hours</div>
          <span className="text-xs text-emerald-600 font-medium">+6.2 hrs this week</span>
        </div>
      </div>
    </div>
  );
};
