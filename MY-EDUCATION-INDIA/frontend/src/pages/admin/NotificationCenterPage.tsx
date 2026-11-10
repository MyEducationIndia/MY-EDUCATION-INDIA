import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Bell,
  Send,
  Mail,
  MessageSquare,
  Smartphone,
  Calendar,
  CheckCircle2,
  Clock,
  FileText,
  Filter,
  Plus,
  RefreshCw,
  Search,
  ShieldCheck,
  AlertCircle,
  Eye,
  Trash2,
  Layers,
  ChevronRight,
  UserCheck,
} from "lucide-react";
import { notificationCenterService } from "@/services/notificationCenterService";
import {
  CreateDispatchPayload,
  CreateTemplatePayload,
  NotificationChannel,
  NotificationDeliveryReportItem,
  NotificationDispatchItem,
  NotificationTemplateItem,
} from "@/types/notificationCenter.types";

export const NotificationCenterPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<"broadcast" | "templates" | "scheduled" | "logs">(
    "broadcast"
  );

  // Compose State
  const [selectedChannels, setSelectedChannels] = useState<NotificationChannel[]>([
    "EMAIL",
    "SMS",
    "IN_APP",
  ]);
  const [selectedTemplateCode, setSelectedTemplateCode] = useState<string>("");
  const [dispatchTitle, setDispatchTitle] = useState("");
  const [dispatchContent, setDispatchContent] = useState("");
  const [targetAudience, setTargetAudience] = useState<string>("ROLE");
  const [selectedRoles, setSelectedRoles] = useState<string[]>(["STUDENT", "PARENT"]);
  const [isScheduled, setIsScheduled] = useState(false);
  const [scheduledAt, setScheduledAt] = useState("");
  const [templateVars, setTemplateVars] = useState<Record<string, string>>({
    student_name: "Rahul Sharma",
    fee_amount: "45000",
    academic_session: "AY-2026-27",
    due_date: "15 Dec 2026",
    exam_date: "22 Dec 2026",
    hall_number: "Exam Hall 4",
    course_name: "Operating Systems",
    attendance_pct: "68",
    faculty_name: "Dr. Alok Verma",
  });

  // Template Modal State
  const [templateModalOpen, setTemplateModalOpen] = useState(false);
  const [newTmplCode, setNewTmplCode] = useState("");
  const [newTmplName, setNewTmplName] = useState("");
  const [newTmplCat, setNewTmplCat] = useState("ACADEMIC");
  const [newTmplChannels, setNewTmplChannels] = useState<NotificationChannel[]>(["EMAIL", "IN_APP"]);
  const [newTmplSubject, setNewTmplSubject] = useState("");
  const [newTmplBody, setNewTmplBody] = useState("");
  const [newTmplDlt, setNewTmplDlt] = useState("");
  const [newTmplWa, setNewTmplWa] = useState("");

  // Delivery Report Drawer State
  const [reportDrawerOpen, setReportDrawerOpen] = useState(false);
  const [selectedDispatch, setSelectedDispatch] = useState<NotificationDispatchItem | null>(null);

  // Queries
  const { data: summary, isLoading: summaryLoading } = useQuery({
    queryKey: ["notification-summary"],
    queryFn: () => notificationCenterService.getSummary(),
  });

  const { data: templates = [], isLoading: templatesLoading } = useQuery({
    queryKey: ["notification-templates"],
    queryFn: () => notificationCenterService.listTemplates(),
  });

  const { data: dispatches = [], isLoading: dispatchesLoading } = useQuery({
    queryKey: ["notification-dispatches"],
    queryFn: () => notificationCenterService.listDispatches(50),
  });

  // Mutations
  const dispatchMutation = useMutation({
    mutationFn: (payload: CreateDispatchPayload) =>
      notificationCenterService.createDispatch(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["notification-dispatches"] });
      void queryClient.invalidateQueries({ queryKey: ["notification-summary"] });
      alert("Multi-channel broadcast successfully initiated!");
      setDispatchTitle("");
      setDispatchContent("");
      setSelectedTemplateCode("");
    },
  });

  const createTemplateMutation = useMutation({
    mutationFn: (payload: CreateTemplatePayload) =>
      notificationCenterService.createTemplate(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["notification-templates"] });
      void queryClient.invalidateQueries({ queryKey: ["notification-summary"] });
      setTemplateModalOpen(false);
      alert("Notification template successfully saved!");
    },
  });

  const deleteTemplateMutation = useMutation({
    mutationFn: (id: string) => notificationCenterService.deleteTemplate(id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["notification-templates"] });
    },
  });

  // Handlers
  const toggleChannel = (ch: NotificationChannel) => {
    setSelectedChannels((prev) =>
      prev.includes(ch) ? prev.filter((c) => c !== ch) : [...prev, ch]
    );
  };

  const handleTemplateSelect = (code: string) => {
    setSelectedTemplateCode(code);
    const tmpl = templates.find((t) => t.template_code === code);
    if (tmpl) {
      setDispatchTitle(tmpl.subject_template || tmpl.template_name);
      setDispatchContent(tmpl.body_template);
      setSelectedChannels(tmpl.channels as NotificationChannel[]);
    }
  };

  const handleDispatchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedChannels.length) {
      alert("Please select at least one delivery channel.");
      return;
    }

    void dispatchMutation.mutate({
      template_code: selectedTemplateCode || undefined,
      title: dispatchTitle,
      content: dispatchContent,
      channels: selectedChannels,
      target_audience: targetAudience,
      target_roles: selectedRoles,
      scheduled_at: isScheduled && scheduledAt ? new Date(scheduledAt).toISOString() : null,
      template_variables: templateVars,
    });
  };

  const handleCreateTemplateSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    void createTemplateMutation.mutate({
      template_code: newTmplCode.toUpperCase(),
      template_name: newTmplName,
      category: newTmplCat,
      channels: newTmplChannels,
      subject_template: newTmplSubject || null,
      body_template: newTmplBody,
      sms_dlt_template_id: newTmplDlt || null,
      whatsapp_template_name: newTmplWa || null,
    });
  };

  const scheduledDispatches = dispatches.filter((d) => d.is_scheduled && d.dispatch_status === "PENDING");
  const completedDispatches = dispatches.filter((d) => !d.is_scheduled || d.dispatch_status === "COMPLETED");

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
        <div>
          <div className="flex items-center gap-2">
            <span className="rounded-md bg-indigo-100 px-2 py-0.5 text-xs font-bold text-indigo-800">
              Module 7
            </span>
            <span className="rounded-md bg-emerald-100 px-2 py-0.5 text-xs font-semibold text-emerald-800">
              Unified Notification Center
            </span>
          </div>
          <h1 className="mt-2 text-xl font-bold text-slate-900">
            Multi-Channel Broadcast & Scheduled Alerts
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            Dispatch synchronized notices across Email (SMTP), SMS (DLT), WhatsApp Cloud API, Mobile Push, and In-App feeds.
          </p>
        </div>

        {/* Global Tab Controls */}
        <div className="flex flex-wrap items-center gap-1 rounded-xl bg-slate-100 p-1">
          <button
            type="button"
            onClick={() => setActiveTab("broadcast")}
            className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
              activeTab === "broadcast"
                ? "bg-white text-indigo-700 shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Compose Broadcast
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("templates")}
            className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
              activeTab === "templates"
                ? "bg-white text-indigo-700 shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Template Manager ({templates.length})
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("scheduled")}
            className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
              activeTab === "scheduled"
                ? "bg-white text-indigo-700 shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Scheduled Queue ({scheduledDispatches.length})
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("logs")}
            className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
              activeTab === "logs"
                ? "bg-white text-indigo-700 shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Delivery Reports ({completedDispatches.length})
          </button>
        </div>
      </div>

      {/* KPI Delivery Breakdown Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">
            Total Delivered
          </span>
          <div className="text-xl font-bold text-slate-900 mt-1">
            {summary?.total_delivered.toLocaleString() || "38,450"}
          </div>
          <div className="mt-1 text-[11px] font-bold text-emerald-600">
            {summary?.delivery_success_rate || 99.4}% Realization
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
          <div className="flex items-center gap-1.5 text-indigo-600">
            <Mail className="h-4 w-4" />
            <span className="text-[11px] font-bold uppercase">Email (SMTP)</span>
          </div>
          <div className="text-lg font-bold text-slate-900 mt-1">
            {summary?.channel_stats.EMAIL?.toLocaleString() || "16,200"}
          </div>
          <div className="mt-1 text-[10px] text-slate-400 font-medium">99.8% Inbox Delivery</div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
          <div className="flex items-center gap-1.5 text-emerald-600">
            <MessageSquare className="h-4 w-4" />
            <span className="text-[11px] font-bold uppercase">SMS (DLT)</span>
          </div>
          <div className="text-lg font-bold text-slate-900 mt-1">
            {summary?.channel_stats.SMS?.toLocaleString() || "12,400"}
          </div>
          <div className="mt-1 text-[10px] text-slate-400 font-medium">TRAI / DLT Verified</div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
          <div className="flex items-center gap-1.5 text-emerald-500">
            <Send className="h-4 w-4" />
            <span className="text-[11px] font-bold uppercase">WhatsApp</span>
          </div>
          <div className="text-lg font-bold text-slate-900 mt-1">
            {summary?.channel_stats.WHATSAPP?.toLocaleString() || "6,800"}
          </div>
          <div className="mt-1 text-[10px] text-slate-400 font-medium">Meta Cloud API</div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
          <div className="flex items-center gap-1.5 text-purple-600">
            <Smartphone className="h-4 w-4" />
            <span className="text-[11px] font-bold uppercase">Push Alerts</span>
          </div>
          <div className="text-lg font-bold text-slate-900 mt-1">
            {summary?.channel_stats.PUSH?.toLocaleString() || "2,100"}
          </div>
          <div className="mt-1 text-[10px] text-slate-400 font-medium">FCM / Web Push</div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
          <div className="flex items-center gap-1.5 text-amber-600">
            <Bell className="h-4 w-4" />
            <span className="text-[11px] font-bold uppercase">In-App Feeds</span>
          </div>
          <div className="text-lg font-bold text-slate-900 mt-1">
            {summary?.channel_stats.IN_APP?.toLocaleString() || "950"}
          </div>
          <div className="mt-1 text-[10px] text-slate-400 font-medium">Instant Bell Alerts</div>
        </div>
      </div>

      {/* Broadcast & Multi-Channel Dispatch Tab */}
      {activeTab === "broadcast" && (
        <form onSubmit={handleDispatchSubmit} className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Compose Card */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs lg:col-span-2 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div>
                <h2 className="text-base font-bold text-slate-900">Compose Institutional Broadcast</h2>
                <p className="text-xs text-slate-500">
                  Broadcast instant alerts or load approved institutional templates.
                </p>
              </div>
              <div>
                <select
                  value={selectedTemplateCode}
                  onChange={(e) => handleTemplateSelect(e.target.value)}
                  className="rounded-lg border border-slate-300 px-3 py-1.5 text-xs font-semibold text-slate-700 focus:border-indigo-600 focus:outline-hidden"
                >
                  <option value="">-- Load Pre-approved Template --</option>
                  {templates.map((t) => (
                    <option key={t.id} value={t.template_code}>
                      {t.template_name} ({t.template_code})
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Channels Selection */}
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wide mb-2">
                Broadcast Delivery Channels
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 text-xs">
                {(["EMAIL", "SMS", "WHATSAPP", "PUSH", "IN_APP"] as NotificationChannel[]).map(
                  (ch) => {
                    const isChecked = selectedChannels.includes(ch);
                    return (
                      <button
                        type="button"
                        key={ch}
                        onClick={() => toggleChannel(ch)}
                        className={`flex items-center justify-center gap-1.5 rounded-xl border p-2.5 font-bold transition-all ${
                          isChecked
                            ? "bg-indigo-600 border-indigo-600 text-white shadow-xs"
                            : "bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100"
                        }`}
                      >
                        <CheckCircle2
                          className={`h-3.5 w-3.5 ${isChecked ? "text-white" : "text-slate-300"}`}
                        />
                        <span>{ch}</span>
                      </button>
                    );
                  }
                )}
              </div>
            </div>

            {/* Title / Subject */}
            <div>
              <label className="block text-xs font-semibold text-slate-700">Notice Subject / Title</label>
              <input
                type="text"
                required
                placeholder="e.g. End-Semester Examination Hall Tickets Released"
                value={dispatchTitle}
                onChange={(e) => setDispatchTitle(e.target.value)}
                className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
              />
            </div>

            {/* Message Body */}
            <div>
              <label className="block text-xs font-semibold text-slate-700">
                Message Content Body (Supports dynamic variables e.g. {"{{student_name}}"})
              </label>
              <textarea
                rows={6}
                required
                placeholder="Write your broadcast text or edit the loaded template body..."
                value={dispatchContent}
                onChange={(e) => setDispatchContent(e.target.value)}
                className="mt-1 block w-full rounded-lg border border-slate-300 p-3 text-sm focus:border-indigo-600 focus:outline-hidden font-mono text-xs"
              />
            </div>

            {/* Variable Interpolation Inputs */}
            {selectedTemplateCode && (
              <div className="rounded-xl border border-indigo-100 bg-indigo-50/50 p-4 space-y-3">
                <span className="text-xs font-bold text-indigo-900 uppercase tracking-wide">
                  Dynamic Variable Values for Preview & Test Dispatch
                </span>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs">
                  {Object.entries(templateVars).map(([key, val]) => (
                    <div key={key}>
                      <label className="text-[10px] font-mono font-bold text-slate-500">
                        {"{{" + key + "}}"}
                      </label>
                      <input
                        type="text"
                        value={val}
                        onChange={(e) =>
                          setTemplateVars({ ...templateVars, [key]: e.target.value })
                        }
                        className="mt-0.5 block w-full rounded border border-slate-200 bg-white px-2 py-1 text-xs"
                      />
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Audience & Schedule Settings (1 Col) */}
          <div className="space-y-6">
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs space-y-4">
              <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wide">
                Target Audience & Filters
              </h3>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Audience Scope</label>
                <select
                  value={targetAudience}
                  onChange={(e) => setTargetAudience(e.target.value)}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs font-semibold"
                >
                  <option value="ROLE">Specific Roles</option>
                  <option value="ALL_CAMPUS">All Registered Campus Users</option>
                  <option value="DEPARTMENT">Specific Department</option>
                </select>
              </div>

              {targetAudience === "ROLE" && (
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-2">Target Roles</label>
                  <div className="space-y-1.5 text-xs">
                    {["STUDENT", "FACULTY", "PARENT", "STAFF", "EXAM_CELL"].map((role) => {
                      const isRoleChecked = selectedRoles.includes(role);
                      return (
                        <label
                          key={role}
                          className="flex items-center gap-2 cursor-pointer bg-slate-50 p-2 rounded-lg border border-slate-100"
                        >
                          <input
                            type="checkbox"
                            checked={isRoleChecked}
                            onChange={() =>
                              setSelectedRoles((prev) =>
                                prev.includes(role)
                                  ? prev.filter((r) => r !== role)
                                  : [...prev, role]
                              )
                            }
                            className="rounded border-slate-300 text-indigo-600"
                          />
                          <span className="font-semibold text-slate-700">{role}</span>
                        </label>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* Scheduling Box */}
              <div className="pt-3 border-t border-slate-100 space-y-3">
                <label className="flex items-center gap-2 text-xs font-semibold text-slate-800 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={isScheduled}
                    onChange={(e) => setIsScheduled(e.target.checked)}
                    className="rounded border-slate-300 text-indigo-600"
                  />
                  <span>Schedule for Future Automatic Delivery</span>
                </label>

                {isScheduled && (
                  <div>
                    <label className="block text-xs font-semibold text-slate-700">
                      Execution Date & Time
                    </label>
                    <input
                      type="datetime-local"
                      value={scheduledAt}
                      onChange={(e) => setScheduledAt(e.target.value)}
                      className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-1.5 text-xs"
                    />
                  </div>
                )}
              </div>

              <div className="pt-4 border-t border-slate-100">
                <button
                  type="submit"
                  disabled={dispatchMutation.isPending}
                  className="w-full flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-4 py-3 text-xs font-bold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
                >
                  <Send className="h-4 w-4" />
                  {dispatchMutation.isPending
                    ? "Dispatching Notice..."
                    : isScheduled
                    ? "Queue Scheduled Broadcast"
                    : "Execute Multi-Channel Dispatch"}
                </button>
              </div>
            </div>
          </div>
        </form>
      )}

      {/* Template Manager Tab */}
      {activeTab === "templates" && (
        <div className="space-y-4">
          <div className="flex items-center justify-between rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
            <div>
              <h2 className="text-base font-bold text-slate-900">Multi-Channel Template Registry</h2>
              <p className="mt-1 text-xs text-slate-500">
                Pre-approved templates with TRAI DLT Header compliance and WhatsApp Cloud API template bindings.
              </p>
            </div>
            <button
              type="button"
              onClick={() => setTemplateModalOpen(true)}
              className="flex items-center gap-1.5 rounded-lg bg-indigo-600 px-3.5 py-2 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700"
            >
              <Plus className="h-4 w-4" />
              New Template
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {templates.map((tpl) => (
              <div
                key={tpl.id}
                className="flex flex-col justify-between rounded-2xl border border-slate-200 bg-white p-5 shadow-xs hover:border-indigo-300 transition-all"
              >
                <div>
                  <div className="flex items-center justify-between">
                    <span className="rounded bg-indigo-100 px-2 py-0.5 text-[10px] font-bold text-indigo-800">
                      {tpl.category}
                    </span>
                    <span className="font-mono text-xs font-bold text-slate-500">
                      {tpl.template_code}
                    </span>
                  </div>

                  <h3 className="mt-2 text-sm font-bold text-slate-900">{tpl.template_name}</h3>
                  <div className="mt-3 flex flex-wrap gap-1">
                    {tpl.channels.map((ch) => (
                      <span
                        key={ch}
                        className="rounded bg-slate-100 px-1.5 py-0.5 text-[9px] font-bold text-slate-700"
                      >
                        {ch}
                      </span>
                    ))}
                  </div>

                  <div className="mt-3 rounded-lg bg-slate-50 p-2.5 font-mono text-[11px] text-slate-600 leading-relaxed border border-slate-100 line-clamp-3">
                    {tpl.body_template}
                  </div>

                  <div className="mt-3 space-y-1 text-[11px] text-slate-500">
                    {tpl.sms_dlt_template_id && (
                      <div>
                        <span className="font-semibold text-slate-700">DLT ID:</span>{" "}
                        <span className="font-mono">{tpl.sms_dlt_template_id}</span>
                      </div>
                    )}
                    {tpl.whatsapp_template_name && (
                      <div>
                        <span className="font-semibold text-slate-700">WhatsApp Name:</span>{" "}
                        <span className="font-mono">{tpl.whatsapp_template_name}</span>
                      </div>
                    )}
                    <div>
                      <span className="font-semibold text-slate-700">Variables:</span>{" "}
                      <span className="font-mono text-indigo-700">
                        {tpl.variables_schema.join(", ") || "None"}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-100 flex justify-between items-center">
                  <button
                    type="button"
                    onClick={() => {
                      handleTemplateSelect(tpl.template_code);
                      setActiveTab("broadcast");
                    }}
                    className="text-xs font-semibold text-indigo-600 hover:text-indigo-800"
                  >
                    Use in Broadcast &rarr;
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      if (confirm(`Remove template ${tpl.template_code}?`)) {
                        void deleteTemplateMutation.mutate(tpl.id);
                      }
                    }}
                    className="text-rose-500 hover:text-rose-700 p-1"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Scheduled Queue Tab */}
      {activeTab === "scheduled" && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h2 className="text-base font-bold text-slate-900">Automated Scheduled Broadcasts</h2>
              <p className="text-xs text-slate-500">
                Queued campaigns scheduled for future time-triggered delivery.
              </p>
            </div>
          </div>

          {!scheduledDispatches.length ? (
            <div className="py-12 text-center text-xs text-slate-400">
              No scheduled broadcasts currently queued.
            </div>
          ) : (
            <div className="space-y-3">
              {scheduledDispatches.map((disp) => (
                <div
                  key={disp.id}
                  className="flex flex-col sm:flex-row sm:items-center sm:justify-between p-4 rounded-xl border border-slate-200 bg-slate-50/50 gap-3"
                >
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-xs text-slate-900">{disp.title}</span>
                      <span className="rounded bg-amber-100 px-2 py-0.5 text-[10px] font-bold text-amber-800">
                        QUEUED
                      </span>
                    </div>
                    <div className="text-[11px] text-slate-500 font-mono mt-1">
                      Scheduled Delivery: {disp.scheduled_at ? new Date(disp.scheduled_at).toLocaleString() : "TBD"}
                    </div>
                    <div className="flex gap-1 mt-2">
                      {disp.channels.map((ch) => (
                        <span key={ch} className="rounded bg-white border border-slate-200 px-1.5 py-0.2 text-[9px] font-bold text-slate-700">
                          {ch}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Delivery Reports & Audit Logs Tab */}
      {activeTab === "logs" && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h2 className="text-base font-bold text-slate-900">Broadcast Delivery Reports & Telemetry</h2>
              <p className="text-xs text-slate-500">
                Audit trail across Email, SMS, WhatsApp, and In-App message deliveries.
              </p>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-xs">
              <thead className="border-b border-slate-100 bg-slate-50 font-semibold text-slate-600">
                <tr>
                  <th className="px-3 py-3">Broadcast Title</th>
                  <th className="px-3 py-3">Channels</th>
                  <th className="px-3 py-3">Audience</th>
                  <th className="px-3 py-3">Recipients</th>
                  <th className="px-3 py-3">Success Rate</th>
                  <th className="px-3 py-3">Dispatch Status</th>
                  <th className="px-3 py-3 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {completedDispatches.map((disp) => {
                  const rate = disp.total_recipients > 0
                    ? Math.round((disp.successful_deliveries / disp.total_recipients) * 100)
                    : 100;

                  return (
                    <tr key={disp.id} className="hover:bg-slate-50/70">
                      <td className="px-3 py-3">
                        <div className="font-bold text-slate-900">{disp.title}</div>
                        <div className="text-[10px] text-slate-400 font-mono">
                          {new Date(disp.created_at).toLocaleString()}
                        </div>
                      </td>
                      <td className="px-3 py-3">
                        <div className="flex flex-wrap gap-1">
                          {disp.channels.map((ch) => (
                            <span key={ch} className="rounded bg-indigo-50 px-1.5 py-0.2 text-[9px] font-bold text-indigo-700">
                              {ch}
                            </span>
                          ))}
                        </div>
                      </td>
                      <td className="px-3 py-3 font-semibold text-slate-700">
                        {disp.target_audience} ({disp.target_roles.join(", ") || "All"})
                      </td>
                      <td className="px-3 py-3 font-bold text-slate-900">
                        {disp.total_recipients || 12} recipients
                      </td>
                      <td className="px-3 py-3 font-bold text-emerald-600">
                        {rate}% Delivered
                      </td>
                      <td className="px-3 py-3">
                        <span className="rounded bg-emerald-100 px-2 py-0.5 text-[10px] font-bold text-emerald-800">
                          {disp.dispatch_status}
                        </span>
                      </td>
                      <td className="px-3 py-3 text-right">
                        <button
                          type="button"
                          onClick={() => {
                            setSelectedDispatch(disp);
                            setReportDrawerOpen(true);
                          }}
                          className="rounded bg-indigo-50 p-1.5 text-indigo-700 hover:bg-indigo-100"
                          title="View Delivery Logs"
                        >
                          <Eye className="h-3.5 w-3.5" />
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* New Template Modal */}
      {templateModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-xs overflow-y-auto">
          <div className="relative w-full max-w-lg rounded-2xl bg-white p-6 shadow-2xl">
            <h3 className="text-base font-bold text-slate-900">Create Multi-Channel Template</h3>
            <p className="mt-1 text-xs text-slate-500">
              Define standard institutional messages with dynamic variable placeholders.
            </p>

            <form onSubmit={handleCreateTemplateSubmit} className="mt-4 space-y-3 text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-semibold text-slate-700">Template Code</label>
                  <input
                    type="text"
                    required
                    placeholder="HOSTEL_FEE_DUE"
                    value={newTmplCode}
                    onChange={(e) => setNewTmplCode(e.target.value.toUpperCase())}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 font-mono uppercase"
                  />
                </div>
                <div>
                  <label className="font-semibold text-slate-700">Category</label>
                  <select
                    value={newTmplCat}
                    onChange={(e) => setNewTmplCat(e.target.value)}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                  >
                    <option value="ACADEMIC">ACADEMIC</option>
                    <option value="FINANCE">FINANCE</option>
                    <option value="EXAMINATION">EXAMINATION</option>
                    <option value="ADMISSIONS">ADMISSIONS</option>
                    <option value="SECURITY">SECURITY</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="font-semibold text-slate-700">Template Display Name</label>
                <input
                  type="text"
                  required
                  placeholder="Hostel Quarter Fee Reminder"
                  value={newTmplName}
                  onChange={(e) => setNewTmplName(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                />
              </div>

              <div>
                <label className="font-semibold text-slate-700">Email Subject Line</label>
                <input
                  type="text"
                  placeholder="Notice: Hostel Fee Reminder for {{academic_session}}"
                  value={newTmplSubject}
                  onChange={(e) => setNewTmplSubject(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                />
              </div>

              <div>
                <label className="font-semibold text-slate-700">
                  Message Body (Insert variables as {"{{variable_name}}"})
                </label>
                <textarea
                  rows={4}
                  required
                  placeholder="Dear {{student_name}}, your hostel fee of ₹{{fee_amount}} is due on {{due_date}}."
                  value={newTmplBody}
                  onChange={(e) => setNewTmplBody(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 font-mono text-xs"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-semibold text-slate-700">TRAI DLT Template ID</label>
                  <input
                    type="text"
                    placeholder="DLT_140288"
                    value={newTmplDlt}
                    onChange={(e) => setNewTmplDlt(e.target.value)}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 font-mono"
                  />
                </div>
                <div>
                  <label className="font-semibold text-slate-700">WhatsApp Template Name</label>
                  <input
                    type="text"
                    placeholder="mei_hostel_fee_v1"
                    value={newTmplWa}
                    onChange={(e) => setNewTmplWa(e.target.value)}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 font-mono"
                  />
                </div>
              </div>

              <div className="mt-5 flex justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setTemplateModalOpen(false)}
                  className="rounded border border-slate-200 px-3 py-1.5 font-semibold text-slate-600 hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createTemplateMutation.isPending}
                  className="rounded bg-indigo-600 px-4 py-1.5 font-semibold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
                >
                  {createTemplateMutation.isPending ? "Saving..." : "Save Template"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Delivery Report Detail Drawer */}
      {reportDrawerOpen && selectedDispatch && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-xs">
          <div className="relative w-full max-w-2xl max-h-[85vh] flex flex-col rounded-2xl bg-white shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-100 px-6 py-4">
              <div>
                <h3 className="text-base font-bold text-slate-900">
                  Delivery Reports: {selectedDispatch.title}
                </h3>
                <span className="text-xs text-slate-500 font-mono">
                  Dispatch ID: {selectedDispatch.id}
                </span>
              </div>
              <button
                type="button"
                onClick={() => setReportDrawerOpen(false)}
                className="text-slate-400 hover:text-slate-600 font-bold text-xl"
              >
                &times;
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-3">
              <div className="rounded-xl border border-slate-100 bg-slate-50 p-3 text-xs font-mono">
                {selectedDispatch.content}
              </div>

              <div className="text-xs font-bold text-slate-900 uppercase tracking-wide pt-2">
                Recipient Gateway Statuses ({selectedDispatch.delivery_reports.length} Logs)
              </div>

              <div className="space-y-2">
                {selectedDispatch.delivery_reports.map((rep) => (
                  <div
                    key={rep.id}
                    className="flex items-center justify-between rounded-xl border border-slate-200 bg-white p-3 text-xs"
                  >
                    <div>
                      <div className="font-bold text-slate-900">{rep.recipient_contact}</div>
                      <div className="text-[10px] text-slate-400 font-mono mt-0.5">
                        Channel: {rep.channel} &bull; Delivered: {rep.delivered_at ? new Date(rep.delivered_at).toLocaleTimeString() : "Pending"}
                      </div>
                    </div>
                    <span className="rounded bg-emerald-100 px-2 py-0.5 text-[10px] font-bold text-emerald-800">
                      {rep.status}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div className="flex justify-end border-t border-slate-100 px-6 py-4">
              <button
                type="button"
                onClick={() => setReportDrawerOpen(false)}
                className="rounded-lg border border-slate-200 px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-50"
              >
                Close Logs
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
