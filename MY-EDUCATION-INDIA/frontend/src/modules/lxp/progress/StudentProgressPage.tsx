import React from "react";
import { BarChart, Trophy, Calendar } from "lucide-react";

export const StudentProgressPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Learning Progress & Telemetry</h1>
      <p className="text-sm text-gray-500">Track lesson completion percentages, watch time logs, and completion certificates</p>
    </div>
  );
};
