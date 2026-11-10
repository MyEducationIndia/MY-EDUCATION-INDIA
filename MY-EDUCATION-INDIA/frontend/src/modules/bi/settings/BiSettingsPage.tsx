import React from "react";
import { Sliders, RefreshCw, Clock } from "lucide-react";

export const BiSettingsPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">BI Engine & Query Cache Settings</h1>
      <p className="text-sm text-gray-500">Configure query snapshot TTL, pre-aggregation schedules, default fiscal years, and export quotas</p>
    </div>
  );
};
