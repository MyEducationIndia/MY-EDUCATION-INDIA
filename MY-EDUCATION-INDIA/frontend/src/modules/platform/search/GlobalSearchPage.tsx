import React, { useState } from "react";
import { Search, ArrowRight, User, BookOpen, FileBadge, IndianRupee } from "lucide-react";

export const GlobalSearchPage: React.FC = () => {
  const [query, setQuery] = useState("");
  return (
    <div className="p-6 space-y-6 max-w-4xl mx-auto">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold text-gray-900">Global ERP Cross-Module Search</h1>
        <p className="text-sm text-gray-500">Instant full-text discovery across Students, Faculty, Courses, Certificates, Fees, Leads & Reports</p>
      </div>

      <div className="relative">
        <Search className="w-6 h-6 absolute left-4 top-3.5 text-gray-400" />
        <input
          type="text"
          placeholder="Search by student name, roll number, course code, lead, receipt ID, certificate hash..."
          className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-2xl shadow-sm text-base focus:outline-none focus:ring-2 focus:ring-indigo-500"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </div>
    </div>
  );
};
