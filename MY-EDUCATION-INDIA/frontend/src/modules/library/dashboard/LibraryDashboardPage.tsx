import React from "react";
import { BookOpen, Users, AlertCircle, FileText, IndianRupee, Layers, CheckCircle2 } from "lucide-react";

export const LibraryDashboardPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Enterprise Library & Knowledge Center</h1>
          <p className="text-sm text-gray-500 mt-1">Real-time catalog monitoring, circulation telemetry, and digital knowledge repository</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Total Catalog Titles</span>
            <div className="p-2 bg-indigo-50 text-indigo-600 rounded-lg"><BookOpen className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">4,250</div>
          <span className="text-xs text-emerald-600 font-medium">18,500 Physical Copies</span>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Active Circulations</span>
            <div className="p-2 bg-blue-50 text-blue-600 rounded-lg"><Layers className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">2,300</div>
          <span className="text-xs text-blue-600 font-medium">16,200 On Shelves</span>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Active Members</span>
            <div className="p-2 bg-emerald-50 text-emerald-600 rounded-lg"><Users className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">3,400</div>
          <span className="text-xs text-emerald-600 font-medium">Students & Faculty</span>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Digital Repository</span>
            <div className="p-2 bg-purple-50 text-purple-600 rounded-lg"><FileText className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mt-3">1,280</div>
          <span className="text-xs text-purple-600 font-medium">eBooks, Journals & Papers</span>
        </div>
      </div>
    </div>
  );
};
