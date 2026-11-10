import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Search, Phone, MessageSquare, Plus, CheckCircle2 } from "lucide-react";
import { admissionService } from "../services/admissionService";
import { LeadRecord } from "../types/admission.types";
import { systemApi } from "@/modules/system/api/systemApi";

export const LeadManagementPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [searchTerm, setSearchTerm] = useState("");
  const [priorityFilter, setPriorityFilter] = useState("");

  const { data: institutes = [] } = useQuery({ queryKey: ["systemInstitutes"], queryFn: systemApi.listInstitutes });
  const instId = institutes[0]?.id;

  const { data, isLoading } = useQuery({
    queryKey: ["leadsList", searchTerm, priorityFilter],
    queryFn: () => admissionService.listLeads({ search: searchTerm || undefined, priority: priorityFilter || undefined }),
  });

  const createLeadMutation = useMutation({
    mutationFn: (values: any) => {
      if (!instId) throw new Error("Institute required");
      return admissionService.createLead({ ...values, institute_id: instId });
    },
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["leadsList"] });
    },
  });

  const handleQuickAddLead = () => {
    const name = prompt("Enter Candidate Full Name:");
    const phone = prompt("Enter Candidate Phone (+91):");
    const course = prompt("Interested Course:");
    if (name && phone && instId) {
      createLeadMutation.mutate({
        full_name: name,
        phone_number: phone,
        interested_course: course || "B.Tech Computer Science",
        priority: "HOT",
        source_channel: "WALK_IN",
      });
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-base font-bold text-slate-900 dark:text-white">Lead & Ingestion CRM</h1>
          <p className="text-xs text-slate-500">Capture, qualify, assign counselors, and schedule follow-up interactions.</p>
        </div>
        <button
          type="button"
          onClick={handleQuickAddLead}
          className="inline-flex items-center gap-1.5 rounded-xl bg-brand-600 px-4 py-2 text-xs font-bold text-white shadow-md hover:bg-brand-500"
        >
          <Plus className="h-4 w-4" /> Capture Walk-In Lead
        </button>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs dark:border-slate-800 dark:bg-slate-900">
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
          <div className="relative sm:col-span-2">
            <Search className="pointer-events-none absolute left-3.5 top-3 h-4 w-4 text-slate-400" />
            <input
              type="search"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search Lead Number, Candidate Name, Phone, Course..."
              className="w-full rounded-xl border border-slate-200 bg-slate-50 py-2 pl-10 pr-3.5 text-xs text-slate-900 focus:outline-hidden dark:border-slate-800 dark:bg-slate-950 dark:text-white"
            />
          </div>
          <select
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value)}
            className="w-full rounded-xl border border-slate-200 bg-slate-50 py-2 px-3 text-xs text-slate-900 dark:border-slate-800 dark:bg-slate-950 dark:text-white"
          >
            <option value="">All Priorities (HOT, WARM, COLD)</option>
            <option value="HOT">HOT Priority</option>
            <option value="WARM">WARM Priority</option>
            <option value="COLD">COLD Priority</option>
          </select>
        </div>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200 text-left text-xs dark:divide-slate-800">
            <thead>
              <tr className="bg-slate-50 uppercase text-slate-500 dark:bg-slate-950">
                <th className="px-4 py-3">Lead ID</th>
                <th className="px-4 py-3">Candidate</th>
                <th className="px-4 py-3">Phone</th>
                <th className="px-4 py-3">Course</th>
                <th className="px-4 py-3">Source</th>
                <th className="px-4 py-3">Priority</th>
                <th className="px-4 py-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
              {isLoading ? (
                <tr><td colSpan={7} className="p-8 text-center text-slate-500">Querying Leads from PostgreSQL...</td></tr>
              ) : (data?.items || []).length === 0 ? (
                <tr><td colSpan={7} className="p-8 text-center text-slate-500">No leads recorded. Use 'Capture Walk-In Lead' to start.</td></tr>
              ) : (
                data?.items.map((lead: LeadRecord) => (
                  <tr key={lead.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                    <td className="px-4 py-3 font-mono font-bold text-brand-600">{lead.lead_number}</td>
                    <td className="px-4 py-3 font-bold text-slate-900 dark:text-white">{lead.full_name}</td>
                    <td className="px-4 py-3 font-mono">{lead.phone_number}</td>
                    <td className="px-4 py-3">{lead.interested_course || "General"}</td>
                    <td className="px-4 py-3 font-semibold text-slate-600 dark:text-slate-400">{lead.source_channel}</td>
                    <td className="px-4 py-3">
                      <span className={`rounded-sm px-2 py-0.5 text-[10px] font-bold ${
                        lead.priority === "HOT" ? "bg-rose-50 text-rose-700 dark:bg-rose-950 dark:text-rose-300" : "bg-amber-50 text-amber-700 dark:bg-amber-950 dark:text-amber-300"
                      }`}>
                        {lead.priority}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <span className="rounded-sm bg-blue-50 px-2 py-0.5 font-bold text-blue-700 dark:bg-blue-950 dark:text-blue-300">
                        {lead.status}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
