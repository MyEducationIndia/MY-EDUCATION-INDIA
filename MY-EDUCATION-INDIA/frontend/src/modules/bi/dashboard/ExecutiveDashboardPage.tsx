import React from "react";
import { Activity, TrendingUp, IndianRupee, Users, CheckCircle2, GraduationCap, AlertCircle, BarChart3, ShieldCheck } from "lucide-react";

export const ExecutiveDashboardPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Executive BI & Analytics Command Center</h1>
          <p className="text-sm text-gray-500 mt-1">Cross-institutional telemetry, revenue velocity, academic KPIs, and operational health</p>
        </div>
        <div className="flex items-center gap-2 bg-emerald-50 text-emerald-700 px-4 py-2 rounded-xl border border-emerald-200">
          <ShieldCheck className="w-5 h-5 text-emerald-600" />
          <span className="text-xs font-bold uppercase tracking-wider">Health Score: 92.4 / 100</span>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Total Revenue Realized</span>
            <div className="p-2 bg-emerald-50 text-emerald-600 rounded-lg"><IndianRupee className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">₹8.45 Cr</div>
          <span className="text-xs text-emerald-600 font-medium">87.2% Fee Collection Rate</span>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Confirmed Admissions</span>
            <div className="p-2 bg-indigo-50 text-indigo-600 rounded-lg"><Users className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">1,420 Enrolled</div>
          <span className="text-xs text-indigo-600 font-medium">34.2% Lead Conversion</span>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Aggregate Attendance</span>
            <div className="p-2 bg-blue-50 text-blue-600 rounded-lg"><Activity className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">91.5%</div>
          <span className="text-xs text-blue-600 font-medium">+3.2% above benchmark</span>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Academic Pass Rate</span>
            <div className="p-2 bg-purple-50 text-purple-600 rounded-lg"><GraduationCap className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">94.8%</div>
          <span className="text-xs text-purple-600 font-medium">3,850 Active Scholars</span>
        </div>
      </div>
    </div>
  );
};
