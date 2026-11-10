import React from "react";
import { Layers, ArrowRight, UserCheck } from "lucide-react";

export const SalesPipelineKanbanPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Visual Admissions Pipeline (Kanban)</h1>
      <p className="text-sm text-gray-500">Drag-and-drop progression: New Lead → Contacted → Counselling → Demo → Interested → Fee Discussion → Won</p>
    </div>
  );
};
