import React from "react";
import { Sliders, Shield, Bell } from "lucide-react";

export const CrmSettingsPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">CRM Engine & Pipeline Configuration</h1>
      <p className="text-sm text-gray-500">Define custom pipeline stages, lead scoring weighting rules, automated round-robin assignment, and SMS/WhatsApp hooks</p>
    </div>
  );
};
