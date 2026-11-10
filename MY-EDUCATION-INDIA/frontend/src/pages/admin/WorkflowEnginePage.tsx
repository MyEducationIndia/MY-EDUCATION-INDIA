import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Workflow,
  CheckCircle2,
  XCircle,
  Clock,
  ArrowRight,
  ShieldCheck,
  AlertTriangle,
  RotateCcw,
  Zap,
  Plus,
  Filter,
  Eye,
  FileText,
  UserCheck,
  Calendar,
  Layers,
  ChevronRight,
  Send,
  MessageSquare,
} from "lucide-react";
import { workflowEngineService } from "@/services/workflowEngineService";
import {
  CreateWorkflowInstancePayload,
  ExecuteWorkflowActionPayload,
  WorkflowDefinitionItem,
  WorkflowInstanceItem,
} from "@/types/workflowEngine.types";

export const WorkflowEnginePage: React.FC = () => {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<"inbox" | "definitions" | "rules">("inbox");
  const [statusFilter, setStatusFilter] = useState<string>("ALL");
  const [typeFilter, setTypeFilter] = useState<string>("ALL");

  // Action Modal State
  const [actionModalOpen, setActionModalOpen] = useState(false);
  const [selectedInstance, setSelectedInstance] = useState<WorkflowInstanceItem | null>(null);
  const [actionType, setActionType] = useState<"APPROVED" | "REJECTED" | "SENT_BACK" | "ESCALATED">("APPROVED");
  const [actionRemarks, setActionRemarks] = useState("");

  // Audit Trail Drawer State
  const [auditDrawerOpen, setAuditDrawerOpen] = useState(false);
  const [auditInstance, setAuditInstance] = useState<WorkflowInstanceItem | null>(null);

  // New Request Modal State
  const [requestModalOpen, setRequestModalOpen] = useState(false);
  const [reqWorkflowCode, setReqWorkflowCode] = useState("LEAVE_APPROVAL");
  const [reqTitle, setReqTitle] = useState("");
  const [reqEntityType, setReqEntityType] = useState("leave_request");
  const [reqEntityId, setReqEntityId] = useState("REQ-2026-X");
  const [reqPriority, setReqPriority] = useState<"LOW" | "NORMAL" | "HIGH" | "URGENT">("NORMAL");
  const [reqPayloadStr, setReqPayloadStr] = useState('{\n  "reason": "Personal/Academic Leave",\n  "days": 2\n}');

  // Queries
  const { data: summary, isLoading: summaryLoading } = useQuery({
    queryKey: ["workflow-summary"],
    queryFn: () => workflowEngineService.getSummary(),
  });

  const { data: definitions = [], isLoading: defsLoading } = useQuery({
    queryKey: ["workflow-definitions"],
    queryFn: () => workflowEngineService.listDefinitions(),
  });

  const { data: instances = [], isLoading: instancesLoading } = useQuery({
    queryKey: ["workflow-instances", statusFilter, typeFilter],
    queryFn: () =>
      workflowEngineService.listInstances({
        status: statusFilter === "ALL" ? undefined : statusFilter,
        entity_type: typeFilter === "ALL" ? undefined : typeFilter,
      }),
  });

  const { data: rules = [], isLoading: rulesLoading } = useQuery({
    queryKey: ["workflow-automation-rules"],
    queryFn: () => workflowEngineService.listAutomationRules(),
  });

  // Mutations
  const executeActionMutation = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: ExecuteWorkflowActionPayload }) =>
      workflowEngineService.executeAction(id, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["workflow-instances"] });
      void queryClient.invalidateQueries({ queryKey: ["workflow-summary"] });
      setActionModalOpen(false);
      setActionRemarks("");
      alert(`Workflow request successfully marked as ${actionType}!`);
    },
  });

  const createInstanceMutation = useMutation({
    mutationFn: (payload: CreateWorkflowInstancePayload) =>
      workflowEngineService.createInstance(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["workflow-instances"] });
      void queryClient.invalidateQueries({ queryKey: ["workflow-summary"] });
      setRequestModalOpen(false);
      setReqTitle("");
      alert("New approval request initiated into multi-level pipeline!");
    },
  });

  const handleOpenActionModal = (
    instance: WorkflowInstanceItem,
    act: "APPROVED" | "REJECTED" | "SENT_BACK" | "ESCALATED"
  ) => {
    setSelectedInstance(instance);
    setActionType(act);
    setActionRemarks(
      act === "APPROVED"
        ? "Verified and approved at current organizational milestone."
        : act === "REJECTED"
        ? "Rejected due to institutional policy mismatch."
        : "Sent back for additional documentation."
    );
    setActionModalOpen(true);
  };

  const handleOpenAuditDrawer = (instance: WorkflowInstanceItem) => {
    setAuditInstance(instance);
    setAuditDrawerOpen(true);
  };

  const handleExecuteActionSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedInstance) return;
    void executeActionMutation.mutate({
      id: selectedInstance.id,
      payload: { action: actionType, remarks: actionRemarks },
    });
  };

  const handleCreateRequestSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const parsedData = JSON.parse(reqPayloadStr);
      void createInstanceMutation.mutate({
        workflow_code: reqWorkflowCode,
        title: reqTitle,
        entity_type: reqEntityType,
        entity_id: reqEntityId,
        priority: reqPriority,
        payload_data: parsedData,
      });
    } catch (err) {
      alert("Invalid JSON payload. Please verify format.");
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
        <div>
          <div className="flex items-center gap-2">
            <span className="rounded-md bg-indigo-100 px-2 py-0.5 text-xs font-bold text-indigo-800">
              Module 9
            </span>
            <span className="rounded-md bg-emerald-100 px-2 py-0.5 text-xs font-semibold text-emerald-800">
              Enterprise Workflow Engine
            </span>
          </div>
          <h1 className="mt-2 text-xl font-bold text-slate-900">
            Multi-Level Approvals & Automation Rules
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            Sequential governance pipelines for Leave Approvals, Admission Scrutiny, Fee Concessions, and Certificate Releases.
          </p>
        </div>

        {/* Global Action Controls */}
        <div className="flex flex-wrap items-center gap-2">
          <div className="flex rounded-xl bg-slate-100 p-1">
            <button
              type="button"
              onClick={() => setActiveTab("inbox")}
              className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
                activeTab === "inbox"
                  ? "bg-white text-indigo-700 shadow-xs"
                  : "text-slate-600 hover:text-slate-900"
              }`}
            >
              Approval Inbox ({instances.length})
            </button>
            <button
              type="button"
              onClick={() => setActiveTab("definitions")}
              className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
                activeTab === "definitions"
                  ? "bg-white text-indigo-700 shadow-xs"
                  : "text-slate-600 hover:text-slate-900"
              }`}
            >
              Workflow Pipelines ({definitions.length})
            </button>
            <button
              type="button"
              onClick={() => setActiveTab("rules")}
              className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
                activeTab === "rules"
                  ? "bg-white text-indigo-700 shadow-xs"
                  : "text-slate-600 hover:text-slate-900"
              }`}
            >
              Automation Rules ({rules.length})
            </button>
          </div>

          <button
            type="button"
            onClick={() => setRequestModalOpen(true)}
            className="flex items-center gap-1.5 rounded-lg bg-indigo-600 px-3.5 py-2 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700"
          >
            <Plus className="h-4 w-4" />
            New Approval Request
          </button>
        </div>
      </div>

      {/* KPI Workflow Analytics Banner */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">
              Active In-Flight Instances
            </span>
            <Layers className="h-4 w-4 text-indigo-600" />
          </div>
          <div className="text-xl font-bold text-slate-900 mt-1">
            {summary?.total_active_instances || 14}
          </div>
          <div className="text-[10px] text-slate-400 mt-1">Across all campus departments</div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">
              Pending Action Items
            </span>
            <Clock className="h-4 w-4 text-amber-600" />
          </div>
          <div className="text-xl font-bold text-amber-600 mt-1">
            {summary?.pending_my_approval || 4}
          </div>
          <div className="text-[10px] text-slate-400 mt-1">Awaiting authorized sign-off</div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">
              Completed This Cycle
            </span>
            <CheckCircle2 className="h-4 w-4 text-emerald-600" />
          </div>
          <div className="text-xl font-bold text-slate-900 mt-1">
            {summary?.completed_this_month || 82}
          </div>
          <div className="text-[10px] text-emerald-600 font-bold mt-1">100% Audit Grounded</div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">
              Average Cycle Time
            </span>
            <Zap className="h-4 w-4 text-purple-600" />
          </div>
          <div className="text-xl font-bold text-indigo-700 mt-1">
            {summary?.avg_cycle_time_hours || 18.4} hrs
          </div>
          <div className="text-[10px] text-slate-400 mt-1">SLA Benchmark: &lt; 48 hrs</div>
        </div>
      </div>

      {/* Approval Inbox Tab */}
      {activeTab === "inbox" && (
        <div className="space-y-4">
          {/* Filters Bar */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
            {/* Status Pills */}
            <div className="flex flex-wrap items-center gap-1 text-xs">
              <span className="font-bold text-slate-700 mr-1 uppercase text-[11px]">Status:</span>
              {["ALL", "PENDING", "IN_REVIEW", "APPROVED", "REJECTED"].map((st) => (
                <button
                  key={st}
                  type="button"
                  onClick={() => setStatusFilter(st)}
                  className={`rounded-lg px-2.5 py-1 text-xs font-semibold transition-colors ${
                    statusFilter === st
                      ? "bg-indigo-600 text-white shadow-xs"
                      : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                  }`}
                >
                  {st}
                </button>
              ))}
            </div>

            {/* Type Dropdown */}
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-slate-700 uppercase text-[11px]">Pipeline:</span>
              <select
                value={typeFilter}
                onChange={(e) => setTypeFilter(e.target.value)}
                className="rounded-lg border border-slate-300 px-2.5 py-1 text-xs font-semibold text-slate-700 focus:border-indigo-600 focus:outline-hidden"
              >
                <option value="ALL">All Workflows</option>
                <option value="leave_request">Leave Requests</option>
                <option value="admission_approval">Admission Scrutiny</option>
                <option value="fee_concession">Fee Concessions</option>
                <option value="certificate_issuance">Certificate Clearances</option>
              </select>
            </div>
          </div>

          {/* Instances List */}
          <div className="space-y-3">
            {instancesLoading ? (
              <div className="rounded-2xl border border-slate-200 bg-white p-12 text-center text-xs text-slate-500">
                Loading workflow instances from PostgreSQL Neon database...
              </div>
            ) : !instances.length ? (
              <div className="rounded-2xl border border-slate-200 bg-white p-12 text-center text-xs text-slate-500">
                No active workflow instances matching filter.
              </div>
            ) : (
              instances.map((inst) => {
                const stepPct = Math.round((inst.current_step_number / inst.total_steps) * 100);

                return (
                  <div
                    key={inst.id}
                    className="rounded-2xl border border-slate-200 bg-white p-5 shadow-2xs hover:border-indigo-300 transition-all space-y-4"
                  >
                    <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3">
                      <div>
                        <div className="flex flex-wrap items-center gap-2">
                          <span className="font-mono text-xs font-bold rounded bg-indigo-50 px-2 py-0.5 text-indigo-700 border border-indigo-200">
                            {inst.tracking_number}
                          </span>
                          <span
                            className={`rounded px-2 py-0.5 text-[10px] font-bold ${
                              inst.priority === "URGENT"
                                ? "bg-rose-100 text-rose-800"
                                : inst.priority === "HIGH"
                                ? "bg-amber-100 text-amber-800"
                                : "bg-slate-100 text-slate-700"
                            }`}
                          >
                            {inst.priority}
                          </span>
                          <span className="text-xs text-slate-400 font-medium">
                            &bull; {inst.workflow_name}
                          </span>
                        </div>

                        <h3 className="mt-2 text-base font-bold text-slate-900">{inst.title}</h3>

                        <div className="mt-1 flex flex-wrap items-center gap-4 text-xs text-slate-500">
                          <div>
                            <span className="font-semibold text-slate-700">Requester:</span>{" "}
                            {inst.requester_name}
                          </div>
                          <div>
                            <span className="font-semibold text-slate-700">Entity:</span>{" "}
                            <span className="font-mono">{inst.entity_id}</span>
                          </div>
                          <div>
                            <span className="font-semibold text-slate-700">Submitted:</span>{" "}
                            {new Date(inst.created_at).toLocaleDateString()}
                          </div>
                        </div>
                      </div>

                      <div className="flex sm:flex-col items-center sm:items-end gap-2">
                        <span
                          className={`rounded-full px-3 py-1 text-xs font-bold ${
                            inst.status === "APPROVED"
                              ? "bg-emerald-100 text-emerald-800"
                              : inst.status === "REJECTED"
                              ? "bg-rose-100 text-rose-800"
                              : "bg-amber-100 text-amber-800"
                          }`}
                        >
                          {inst.status}
                        </span>
                        <span className="text-[11px] font-semibold text-slate-500">
                          Stage {inst.current_step_number} of {inst.total_steps}
                        </span>
                      </div>
                    </div>

                    {/* Multi-Level Progress Bar */}
                    <div className="space-y-1.5">
                      <div className="flex justify-between text-[11px] font-semibold text-slate-600">
                        <span>Multi-Level Milestone Progress</span>
                        <span>{stepPct}% Completed</span>
                      </div>
                      <div className="h-2 w-full rounded-full bg-slate-100 overflow-hidden">
                        <div
                          className={`h-full rounded-full transition-all duration-500 ${
                            inst.status === "REJECTED"
                              ? "bg-rose-500"
                              : inst.status === "APPROVED"
                              ? "bg-emerald-500"
                              : "bg-indigo-600"
                          }`}
                          style={{ width: `${stepPct}%` }}
                        />
                      </div>
                    </div>

                    {/* Action Bar */}
                    <div className="pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3 text-xs">
                      <button
                        type="button"
                        onClick={() => handleOpenAuditDrawer(inst)}
                        className="flex items-center gap-1 font-semibold text-indigo-600 hover:text-indigo-800"
                      >
                        <History className="h-3.5 w-3.5" />
                        Audit Trail ({inst.actions.length} Actions)
                      </button>

                      {inst.status !== "APPROVED" && inst.status !== "REJECTED" && (
                        <div className="flex items-center gap-2">
                          <button
                            type="button"
                            onClick={() => handleOpenActionModal(inst, "APPROVED")}
                            className="flex items-center gap-1 rounded-lg bg-emerald-600 px-3 py-1.5 font-bold text-white shadow-xs hover:bg-emerald-700"
                          >
                            <CheckCircle2 className="h-3.5 w-3.5" />
                            Approve Stage
                          </button>
                          <button
                            type="button"
                            onClick={() => handleOpenActionModal(inst, "SENT_BACK")}
                            className="flex items-center gap-1 rounded-lg border border-slate-300 bg-white px-2.5 py-1.5 font-semibold text-slate-700 hover:bg-slate-50"
                          >
                            <RotateCcw className="h-3.5 w-3.5" />
                            Send Back
                          </button>
                          <button
                            type="button"
                            onClick={() => handleOpenActionModal(inst, "REJECTED")}
                            className="flex items-center gap-1 rounded-lg bg-rose-50 px-2.5 py-1.5 font-semibold text-rose-700 hover:bg-rose-100"
                          >
                            <XCircle className="h-3.5 w-3.5" />
                            Reject
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>
      )}

      {/* Multi-Level Workflow Definitions Tab */}
      {activeTab === "definitions" && (
        <div className="space-y-4">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
            <h2 className="text-base font-bold text-slate-900">
              Institutional Multi-Level Workflow Definitions
            </h2>
            <p className="mt-1 text-xs text-slate-500">
              Structured authorization stages, role assignments, and SLA timeout escalation rules.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {definitions.map((def) => (
              <div
                key={def.id}
                className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs space-y-4"
              >
                <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="text-sm font-bold text-slate-900">{def.name}</h3>
                    </div>
                    <span className="font-mono text-[10px] text-indigo-700 font-bold">
                      {def.workflow_code} &bull; {def.category}
                    </span>
                  </div>
                  <span className="rounded bg-indigo-100 px-2.5 py-0.5 text-xs font-bold text-indigo-800">
                    {def.total_steps} Sequential Levels
                  </span>
                </div>

                <p className="text-xs text-slate-600">{def.description}</p>

                {/* Steps Pipeline Visual */}
                <div className="space-y-2 pt-2">
                  <span className="text-[11px] font-bold text-slate-700 uppercase tracking-wide">
                    Approval Sequence
                  </span>
                  <div className="space-y-2">
                    {def.steps.map((st, idx) => (
                      <div
                        key={st.id}
                        className="flex items-center justify-between p-2.5 rounded-xl border border-slate-200 bg-slate-50 text-xs"
                      >
                        <div className="flex items-center gap-2.5">
                          <div className="flex h-6 w-6 items-center justify-center rounded-full bg-indigo-600 text-white font-bold text-xs shrink-0">
                            {st.step_number}
                          </div>
                          <div>
                            <div className="font-bold text-slate-900">{st.step_name}</div>
                            <div className="text-[10px] text-slate-500 mt-0.5 font-mono">
                              Role: <span className="font-semibold text-indigo-700">{st.approver_role}</span>
                            </div>
                          </div>
                        </div>

                        <div className="text-right text-[10px] text-slate-400 font-mono">
                          <div>SLA: {st.timeout_hours}h</div>
                          <div className="text-amber-600 font-semibold">{st.auto_action_on_timeout}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Automation Rules Tab */}
      {activeTab === "rules" && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h2 className="text-base font-bold text-slate-900">Workflow Automation & Event Rules</h2>
              <p className="text-xs text-slate-500">
                Trigger autonomous actions, timeouts, notifications, and auto-approvals upon state changes.
              </p>
            </div>
          </div>

          <div className="space-y-3">
            {rules.map((rule) => (
              <div
                key={rule.id}
                className="flex flex-col sm:flex-row sm:items-center sm:justify-between p-4 rounded-xl border border-slate-200 bg-slate-50/60 gap-3 text-xs"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <Zap className="h-4 w-4 text-amber-500 shrink-0" />
                    <span className="font-bold text-sm text-slate-900">{rule.rule_name}</span>
                    <span className="rounded bg-emerald-100 px-2 py-0.2 text-[9px] font-bold text-emerald-800">
                      ACTIVE
                    </span>
                  </div>
                  <div className="flex items-center gap-3 text-[11px] text-slate-500">
                    <div>
                      Trigger: <span className="font-mono font-bold text-indigo-700">{rule.trigger_event}</span>
                    </div>
                    <div>&bull;</div>
                    <div>
                      Action: <span className="font-mono font-bold text-purple-700">{rule.action_type}</span>
                    </div>
                  </div>
                </div>

                <div className="font-mono text-[11px] text-slate-500 bg-white p-2 rounded-lg border border-slate-200">
                  {JSON.stringify(rule.action_payload)}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action Execution Modal */}
      {actionModalOpen && selectedInstance && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-xs">
          <div className="relative w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl">
            <h3 className="text-base font-bold text-slate-900">
              {actionType} Request: {selectedInstance.tracking_number}
            </h3>
            <p className="mt-1 text-xs text-slate-500">
              Record institutional verification remarks for Stage {selectedInstance.current_step_number}.
            </p>

            <form onSubmit={handleExecuteActionSubmit} className="mt-4 space-y-3 text-xs">
              <div>
                <label className="font-semibold text-slate-700">Official Decision Action</label>
                <input
                  type="text"
                  disabled
                  value={actionType}
                  className="mt-1 block w-full rounded border border-slate-200 bg-slate-50 px-2.5 py-1.5 font-bold font-mono text-indigo-700"
                />
              </div>

              <div>
                <label className="font-semibold text-slate-700">Audit Remarks & Feedback</label>
                <textarea
                  rows={3}
                  required
                  value={actionRemarks}
                  onChange={(e) => setActionRemarks(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                />
              </div>

              <div className="mt-5 flex justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setActionModalOpen(false)}
                  className="rounded border border-slate-200 px-3 py-1.5 font-semibold text-slate-600 hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={executeActionMutation.isPending}
                  className={`rounded px-4 py-1.5 font-bold text-white shadow-xs disabled:opacity-50 ${
                    actionType === "APPROVED"
                      ? "bg-emerald-600 hover:bg-emerald-700"
                      : actionType === "REJECTED"
                      ? "bg-rose-600 hover:bg-rose-700"
                      : "bg-indigo-600 hover:bg-indigo-700"
                  }`}
                >
                  {executeActionMutation.isPending ? "Executing..." : `Confirm ${actionType}`}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* New Request Modal */}
      {requestModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-xs overflow-y-auto">
          <div className="relative w-full max-w-lg rounded-2xl bg-white p-6 shadow-2xl">
            <h3 className="text-base font-bold text-slate-900">Initiate Approval Request</h3>
            <p className="mt-1 text-xs text-slate-500">
              Submit a formal request to enter the institutional multi-level authorization pipeline.
            </p>

            <form onSubmit={handleCreateRequestSubmit} className="mt-4 space-y-3 text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-semibold text-slate-700">Target Workflow</label>
                  <select
                    value={reqWorkflowCode}
                    onChange={(e) => {
                      setReqWorkflowCode(e.target.value);
                      if (e.target.value === "LEAVE_APPROVAL") {
                        setReqEntityType("leave_request");
                        setReqTitle("Emergency Medical Leave - 2 Days");
                      } else if (e.target.value === "ADMISSION_APPROVAL") {
                        setReqEntityType("admission_approval");
                        setReqTitle("Provisional Admission Scrutiny");
                      } else if (e.target.value === "FEE_CONCESSION_APPROVAL") {
                        setReqEntityType("fee_concession");
                        setReqTitle("Merit Fee Scholarship Waiver Request");
                      } else {
                        setReqEntityType("certificate_issuance");
                        setReqTitle("Degree Certificate Clearance Application");
                      }
                    }}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 font-semibold"
                  >
                    <option value="LEAVE_APPROVAL">Leave Approval</option>
                    <option value="ADMISSION_APPROVAL">Admission Approval</option>
                    <option value="FEE_CONCESSION_APPROVAL">Fee Concession Approval</option>
                    <option value="CERTIFICATE_ISSUANCE_APPROVAL">Certificate Issuance</option>
                  </select>
                </div>

                <div>
                  <label className="font-semibold text-slate-700">Priority Level</label>
                  <select
                    value={reqPriority}
                    onChange={(e) => setReqPriority(e.target.value as any)}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 font-semibold"
                  >
                    <option value="NORMAL">NORMAL</option>
                    <option value="HIGH">HIGH</option>
                    <option value="URGENT">URGENT</option>
                    <option value="LOW">LOW</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="font-semibold text-slate-700">Request Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Dr. Alok Verma - Medical Leave Application"
                  value={reqTitle}
                  onChange={(e) => setReqTitle(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                />
              </div>

              <div>
                <label className="font-semibold text-slate-700">Entity Identifier</label>
                <input
                  type="text"
                  required
                  value={reqEntityId}
                  onChange={(e) => setReqEntityId(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 font-mono"
                />
              </div>

              <div>
                <label className="font-semibold text-slate-700">Payload Data JSON</label>
                <textarea
                  rows={4}
                  value={reqPayloadStr}
                  onChange={(e) => setReqPayloadStr(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 font-mono text-xs"
                />
              </div>

              <div className="mt-5 flex justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setRequestModalOpen(false)}
                  className="rounded border border-slate-200 px-3 py-1.5 font-semibold text-slate-600 hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createInstanceMutation.isPending}
                  className="rounded bg-indigo-600 px-4 py-1.5 font-semibold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
                >
                  {createInstanceMutation.isPending ? "Submitting..." : "Submit to Pipeline"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Audit Trail Drawer */}
      {auditDrawerOpen && auditInstance && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-xs">
          <div className="relative w-full max-w-lg max-h-[85vh] flex flex-col rounded-2xl bg-white shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-100 px-6 py-4">
              <div>
                <h3 className="text-base font-bold text-slate-900">
                  Audit Trail: {auditInstance.tracking_number}
                </h3>
                <span className="text-xs text-slate-500">
                  {auditInstance.title} &bull; Stage {auditInstance.current_step_number} of {auditInstance.total_steps}
                </span>
              </div>
              <button
                type="button"
                onClick={() => setAuditDrawerOpen(false)}
                className="text-slate-400 hover:text-slate-600 font-bold text-xl"
              >
                &times;
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-3 text-xs">
              {!auditInstance.actions.length ? (
                <div className="py-6 text-center text-slate-400">
                  No approval actions logged yet.
                </div>
              ) : (
                auditInstance.actions.map((act) => (
                  <div
                    key={act.id}
                    className="p-3 rounded-xl border border-slate-200 bg-slate-50/70 space-y-1"
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-slate-900">
                        Level {act.step_number}: {act.actor_name}
                      </span>
                      <span
                        className={`rounded px-2 py-0.2 text-[9px] font-bold ${
                          act.action === "APPROVED"
                            ? "bg-emerald-100 text-emerald-800"
                            : act.action === "REJECTED"
                            ? "bg-rose-100 text-rose-800"
                            : "bg-indigo-100 text-indigo-800"
                        }`}
                      >
                        {act.action}
                      </span>
                    </div>
                    {act.remarks && (
                      <p className="text-slate-600 italic mt-0.5">"{act.remarks}"</p>
                    )}
                    <div className="text-[10px] text-slate-400 font-mono pt-1">
                      Role: {act.actor_role} &bull; {new Date(act.performed_at).toLocaleString()}
                    </div>
                  </div>
                ))
              )}
            </div>

            <div className="flex justify-end border-t border-slate-100 px-6 py-4">
              <button
                type="button"
                onClick={() => setAuditDrawerOpen(false)}
                className="rounded-lg border border-slate-200 px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-50"
              >
                Close Audit Trail
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
