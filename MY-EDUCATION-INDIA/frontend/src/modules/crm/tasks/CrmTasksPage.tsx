import React from "react";
import { CheckSquare, Clock, User, AlertCircle } from "lucide-react";

export const CrmTasksPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Sales & Counsellor Task Management</h1>
      <p className="text-sm text-gray-500">Assign admission quotas, document verification tasks, callback deadlines, and priority alerts</p>
    </div>
  );
};
