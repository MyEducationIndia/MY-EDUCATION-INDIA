import React from "react";
import { FileSpreadsheet, Download, Filter } from "lucide-react";

export const CrmReportsPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">CRM Conversion & Performance Reports</h1>
      <p className="text-sm text-gray-500">Export lead qualification audits, counselor efficiency scores, campaign ROI balance sheets, and dropout logs</p>
    </div>
  );
};
