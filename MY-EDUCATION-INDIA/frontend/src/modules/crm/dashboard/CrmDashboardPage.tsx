import React from "react";
import { Users, PhoneCall, Trophy, TrendingUp, IndianRupee, Target, Megaphone, CheckSquare } from "lucide-react";

export const CrmDashboardPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Enterprise CRM, Sales & Franchise Hub</h1>
          <p className="text-sm text-gray-500 mt-1">Lead acquisition, pipeline progression, marketing campaign ROI, and regional franchise networks</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">New Leads This Month</span>
            <div className="p-2 bg-indigo-50 text-indigo-600 rounded-lg"><Users className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">128 Leads</div>
          <span className="text-xs text-emerald-600 font-medium">+18% vs last month</span>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Today's Follow-ups</span>
            <div className="p-2 bg-blue-50 text-blue-600 rounded-lg"><PhoneCall className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">24 Calls</div>
          <span className="text-xs text-blue-600 font-medium">8 High Priority</span>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Admissions Converted</span>
            <div className="p-2 bg-emerald-50 text-emerald-600 rounded-lg"><Trophy className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">42 Confirmed</div>
          <span className="text-xs text-emerald-600 font-medium">32.8% Conversion Rate</span>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Revenue Forecast</span>
            <div className="p-2 bg-purple-50 text-purple-600 rounded-lg"><IndianRupee className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">₹42.50 Lakh</div>
          <span className="text-xs text-purple-600 font-medium">Weighted Pipeline Value</span>
        </div>
      </div>
    </div>
  );
};
