import React from "react";
import { FileBarChart, Download } from "lucide-react";

export const LibraryReportsPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Circulation & Audit Reports</h1>
      <p className="text-sm text-gray-500">Export active issue registers, overdue fine audits, loss reports, and inventory reconciliation</p>
    </div>
  );
};
