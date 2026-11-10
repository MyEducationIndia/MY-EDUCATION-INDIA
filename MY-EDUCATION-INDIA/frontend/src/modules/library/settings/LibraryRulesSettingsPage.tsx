import React from "react";
import { Settings, Save } from "lucide-react";

export const LibraryRulesSettingsPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Circulation Rules & Fine Settings</h1>
      <p className="text-sm text-gray-500">Define daily overdue rates (INR/day), grace periods, max borrow allowances, and RFID scanner gates</p>
    </div>
  );
};
