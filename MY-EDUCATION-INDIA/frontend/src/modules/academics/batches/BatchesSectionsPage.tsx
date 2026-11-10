import React from "react";
import { useQuery } from "@tanstack/react-query";
import { Layers, Plus, Users, Calendar } from "lucide-react";
import { academicService } from "../services/academicService";

export const BatchesSectionsPage: React.FC = () => {
  const { data: batches = [], isLoading } = useQuery({ queryKey: ["academicBatches"], queryFn: academicService.listBatches });

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs dark:border-slate-800 dark:bg-slate-900 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-base font-bold text-slate-900 dark:text-white">Batches & Classroom Sections</h1>
          <p className="text-xs text-slate-500">Manage academic cohorts, student capacities, and section groups (Section A, B, Evening).</p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {isLoading ? (
          <p className="text-xs text-slate-500">Loading batches...</p>
        ) : batches.length === 0 ? (
          <p className="text-xs text-slate-500">No active batches created yet.</p>
        ) : (
          batches.map((b) => (
            <div key={b.id} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900">
              <div className="flex items-center justify-between">
                <span className="text-sm font-bold text-slate-900 dark:text-white">{b.name}</span>
                <span className="rounded-sm bg-purple-50 px-2 py-0.5 font-mono text-[11px] font-bold text-purple-700 dark:bg-purple-950 dark:text-purple-300">
                  {b.code}
                </span>
              </div>
              <p className="mt-1 text-xs text-slate-500">Academic Session: {b.academic_year_code}</p>

              <div className="mt-4 flex items-center justify-between border-t border-slate-100 pt-3 text-xs text-slate-600 dark:border-slate-800 dark:text-slate-400">
                <span>Capacity: {b.intake_capacity}</span>
                <span className="font-bold text-brand-600">{b.sections?.length || 1} Sections</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
