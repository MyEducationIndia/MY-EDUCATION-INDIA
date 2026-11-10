import React from "react";
import { FileSpreadsheet, Download, Filter } from "lucide-react";

export const LXPReportsPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">LXP Audit & Progress Reports</h1>
      <p className="text-sm text-gray-500">Export batch-wise course completions, gradebooks, watch hours, and compliance ledgers</p>
    </div>
  );
};
