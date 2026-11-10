import React from "react";
import { LifeBuoy, Plus, MessageSquare, CheckCircle, HelpCircle } from "lucide-react";

export const SupportCenterPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Institutional Support & Helpdesk Hub</h1>
          <p className="text-sm text-gray-500">Manage support tickets, institutional knowledge base, bug tracking, and service SLAs</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm font-medium">
          <Plus className="w-4 h-4" /> Open Ticket
        </button>
      </div>
    </div>
  );
};
