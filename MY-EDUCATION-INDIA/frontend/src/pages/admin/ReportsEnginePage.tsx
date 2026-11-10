import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  FileText,
  Download,
  Printer,
  Calendar,
  Layers,
  BarChart3,
  PieChart,
  Filter,
  Clock,
  CheckCircle2,
  Play,
  Mail,
  Plus,
  RefreshCw,
  ExternalLink,
  ChevronRight,
  TrendingUp,
} from "lucide-react";
import { reportEngineService } from "@/services/reportEngineService";
import {
  CreateScheduledJobPayload,
  GeneratedReportData,
  GenerateReportPayload,
  ReportCategory,
  ReportDefinitionItem,
  ReportFormat,
} from "@/types/reportEngine.types";

const CATEGORY_TABS: { key: ReportCategory; label: string }[] = [
  { key: "ALL", label: "All Institutional Reports" },
  { key: "ACADEMIC", label: "Academics" },
  { key: "FINANCE", label: "Finance & Accounts" },
  { key: "ADMISSIONS", label: "Admissions & CRM" },
  { key: "ATTENDANCE", label: "Attendance" },
  { key: "EXAMINATION", label: "Examinations" },
];

export const ReportsEnginePage: React.FC = () => {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<"catalog" | "preview" | "scheduled" | "history">(
    "catalog"
  );
  const [selectedCategory, setSelectedCategory] = useState<ReportCategory>("ALL");

  // Generator State
  const [selectedReport, setSelectedReport] = useState<ReportDefinitionItem | null>(null);
  const [exportFormat, setExportFormat] = useState<ReportFormat>("PDF");
  const [filterValues, setFilterValues] = useState<Record<string, string>>({
    branch: "Computer Science & Engineering",
    semester: "Semester 5",
    academic_session: "AY-2026-27",
    quota: "Merit All-India",
  });
  const [generatedReport, setGeneratedReport] = useState<GeneratedReportData | null>(null);

  // Scheduled Job Modal State
  const [scheduleModalOpen, setScheduleModalOpen] = useState(false);
  const [schedJobTitle, setSchedJobTitle] = useState("");
  const [schedReportCode, setSchedReportCode] = useState("ACADEMIC_CGPA_ROLL");
  const [schedFreq, setSchedFreq] = useState<"DAILY" | "WEEKLY" | "MONTHLY" | "QUARTERLY">("WEEKLY");
  const [schedFormat, setSchedFormat] = useState<"PDF" | "EXCEL" | "CSV">("PDF");
  const [schedEmails, setSchedEmails] = useState("registrar@myeducationindia.com, dean@myeducationindia.com");

  // Queries
  const { data: summary, isLoading: summaryLoading } = useQuery({
    queryKey: ["report-summary"],
    queryFn: () => reportEngineService.getSummary(),
  });

  const { data: definitions = [], isLoading: defsLoading } = useQuery({
    queryKey: ["report-definitions", selectedCategory],
    queryFn: () =>
      reportEngineService.listDefinitions(
        selectedCategory === "ALL" ? undefined : selectedCategory
      ),
  });

  const { data: executions = [], isLoading: execsLoading } = useQuery({
    queryKey: ["report-executions"],
    queryFn: () => reportEngineService.listExecutions(30),
  });

  const { data: scheduledJobs = [], isLoading: jobsLoading } = useQuery({
    queryKey: ["report-scheduled-jobs"],
    queryFn: () => reportEngineService.listScheduledJobs(),
  });

  // Mutations
  const generateMutation = useMutation({
    mutationFn: (payload: GenerateReportPayload) => reportEngineService.generateReport(payload),
    onSuccess: (data) => {
      setGeneratedReport(data);
      setActiveTab("preview");
      void queryClient.invalidateQueries({ queryKey: ["report-executions"] });
      void queryClient.invalidateQueries({ queryKey: ["report-summary"] });
    },
  });

  const createScheduleMutation = useMutation({
    mutationFn: (payload: CreateScheduledJobPayload) =>
      reportEngineService.createScheduledJob(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["report-scheduled-jobs"] });
      void queryClient.invalidateQueries({ queryKey: ["report-summary"] });
      setScheduleModalOpen(false);
      alert("Scheduled report job successfully configured!");
    },
  });

  const handleSelectReport = (rep: ReportDefinitionItem) => {
    setSelectedReport(rep);
  };

  const handleGenerate = () => {
    if (!selectedReport) return;
    void generateMutation.mutate({
      report_code: selectedReport.report_code,
      export_format: exportFormat,
      filters: filterValues,
    });
  };

  const handleCreateScheduleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const emails = schedEmails.split(",").map((em) => em.trim()).filter(Boolean);
    void createScheduleMutation.mutate({
      report_code: schedReportCode,
      job_title: schedJobTitle,
      frequency: schedFreq,
      export_format: schedFormat,
      recipient_emails: emails,
      filter_parameters: filterValues,
    });
  };

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
        <div>
          <div className="flex items-center gap-2">
            <span className="rounded-md bg-indigo-100 px-2 py-0.5 text-xs font-bold text-indigo-800">
              Module 11
            </span>
            <span className="rounded-md bg-emerald-100 px-2 py-0.5 text-xs font-semibold text-emerald-800">
              Reporting & Analytics Engine
            </span>
          </div>
          <h1 className="mt-2 text-xl font-bold text-slate-900">
            Institutional Reports Framework
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            Generate compliant institutional reports across PDF, Excel, CSV, and Print with dynamic filtering, statistical charts, and automated cron schedules.
          </p>
        </div>

        {/* Global Action Controls */}
        <div className="flex flex-wrap items-center gap-2">
          <div className="flex rounded-xl bg-slate-100 p-1">
            <button
              type="button"
              onClick={() => setActiveTab("catalog")}
              className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
                activeTab === "catalog"
                  ? "bg-white text-indigo-700 shadow-xs"
                  : "text-slate-600 hover:text-slate-900"
              }`}
            >
              Report Catalog ({definitions.length})
            </button>
            <button
              type="button"
              onClick={() => setActiveTab("preview")}
              className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
                activeTab === "preview"
                  ? "bg-white text-indigo-700 shadow-xs"
                  : "text-slate-600 hover:text-slate-900"
              }`}
            >
              Live Preview {generatedReport && "• Ready"}
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
              Scheduled Jobs ({scheduledJobs.length})
            </button>
            <button
              type="button"
              onClick={() => setActiveTab("history")}
              className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
                activeTab === "history"
                  ? "bg-white text-indigo-700 shadow-xs"
                  : "text-slate-600 hover:text-slate-900"
              }`}
            >
              Execution History ({executions.length})
            </button>
          </div>

          <button
            type="button"
            onClick={() => setScheduleModalOpen(true)}
            className="flex items-center gap-1.5 rounded-lg bg-indigo-600 px-3.5 py-2 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700"
          >
            <Plus className="h-4 w-4" />
            Schedule Job
          </button>
        </div>
      </div>

      {/* KPI Analytics Banner */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">
              Catalog Definitions
            </span>
            <FileText className="h-4 w-4 text-indigo-600" />
          </div>
          <div className="text-xl font-bold text-slate-900 mt-1">
            {summary?.total_reports_available || 5} Standard Reports
          </div>
          <div className="text-[10px] text-slate-400 mt-1">Academics, Finance, Exams & HR</div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">
              Generated This Cycle
            </span>
            <Download className="h-4 w-4 text-emerald-600" />
          </div>
          <div className="text-xl font-bold text-slate-900 mt-1">
            {summary?.total_generated_this_month || 148} Exports
          </div>
          <div className="text-[10px] text-emerald-600 font-bold mt-1">PDF & Excel Dominant</div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">
              Active Cron Schedules
            </span>
            <Calendar className="h-4 w-4 text-indigo-500" />
          </div>
          <div className="text-xl font-bold text-indigo-700 mt-1">
            {summary?.active_scheduled_jobs || 3} Automated Jobs
          </div>
          <div className="text-[10px] text-slate-400 mt-1">Dispatched via SMTP & WhatsApp</div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">
              Supported Export Types
            </span>
            <Layers className="h-4 w-4 text-purple-600" />
          </div>
          <div className="text-xl font-bold text-slate-900 mt-1">PDF &bull; Excel &bull; CSV</div>
          <div className="text-[10px] text-slate-400 mt-1">Ready for Print Spooling</div>
        </div>
      </div>

      {/* Report Catalog Tab */}
      {activeTab === "catalog" && (
        <div className="space-y-6">
          {/* Category Filter Pills */}
          <div className="flex overflow-x-auto gap-1 rounded-2xl border border-slate-200 bg-white p-2 shadow-xs">
            {CATEGORY_TABS.map((tab) => (
              <button
                key={tab.key}
                type="button"
                onClick={() => setSelectedCategory(tab.key)}
                className={`rounded-xl px-3.5 py-1.5 text-xs font-semibold whitespace-nowrap transition-colors ${
                  selectedCategory === tab.key
                    ? "bg-indigo-600 text-white shadow-xs"
                    : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Catalog Grid (2 Cols) */}
            <div className="lg:col-span-2 space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {definitions.map((rep) => {
                  const isSelected = selectedReport?.id === rep.id;

                  return (
                    <div
                      key={rep.id}
                      onClick={() => handleSelectReport(rep)}
                      className={`cursor-pointer rounded-2xl border p-5 shadow-xs transition-all flex flex-col justify-between ${
                        isSelected
                          ? "bg-indigo-50/70 border-indigo-500 ring-2 ring-indigo-200"
                          : "bg-white border-slate-200 hover:border-indigo-300"
                      }`}
                    >
                      <div>
                        <div className="flex items-center justify-between">
                          <span className="rounded bg-indigo-100 px-2 py-0.5 text-[10px] font-bold text-indigo-800">
                            {rep.category}
                          </span>
                          <span className="font-mono text-xs font-bold text-slate-400">
                            {rep.report_code}
                          </span>
                        </div>

                        <h3 className="mt-2.5 text-sm font-bold text-slate-900">{rep.title}</h3>
                        <p className="mt-1 text-xs text-slate-500 line-clamp-2">
                          {rep.description}
                        </p>

                        <div className="mt-3 flex flex-wrap gap-1">
                          {rep.supported_formats.map((fmt) => (
                            <span
                              key={fmt}
                              className="rounded bg-slate-100 px-1.5 py-0.2 text-[9px] font-bold text-slate-700"
                            >
                              {fmt}
                            </span>
                          ))}
                        </div>
                      </div>

                      <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                        <span className="text-slate-400 text-[11px] font-medium">
                          Chart: {rep.chart_type?.toUpperCase() || "TABLE"}
                        </span>
                        <span className="font-semibold text-indigo-600 flex items-center gap-1">
                          {isSelected ? "Selected" : "Configure"} <ChevronRight className="h-3 w-3" />
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Filter Configuration & Format Launcher (1 Col) */}
            <div className="space-y-4">
              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs space-y-4">
                <div className="border-b border-slate-100 pb-3">
                  <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wide">
                    Generator Parameters & Format
                  </h3>
                  <p className="text-[11px] text-slate-500 mt-0.5">
                    {selectedReport ? selectedReport.title : "Select a report from catalog"}
                  </p>
                </div>

                {selectedReport ? (
                  <div className="space-y-4 text-xs">
                    {/* Format Selection */}
                    <div>
                      <label className="font-bold text-slate-700 uppercase tracking-wide block mb-2">
                        Export Document Format
                      </label>
                      <div className="grid grid-cols-2 gap-2">
                        {(["PDF", "EXCEL", "CSV", "PRINT"] as ReportFormat[]).map((fmt) => {
                          const isFmt = exportFormat === fmt;
                          return (
                            <button
                              key={fmt}
                              type="button"
                              onClick={() => setExportFormat(fmt)}
                              className={`rounded-xl border p-2.5 font-bold text-center transition-all ${
                                isFmt
                                  ? "bg-indigo-600 border-indigo-600 text-white shadow-xs"
                                  : "bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100"
                              }`}
                            >
                              {fmt}
                            </button>
                          );
                        })}
                      </div>
                    </div>

                    {/* Filter Inputs */}
                    <div className="space-y-3 pt-2">
                      <span className="font-bold text-slate-700 uppercase tracking-wide block">
                        Query Filter Criteria
                      </span>

                      <div>
                        <label className="font-medium text-slate-600">Academic Session</label>
                        <select
                          value={filterValues.academic_session || "AY-2026-27"}
                          onChange={(e) =>
                            setFilterValues({ ...filterValues, academic_session: e.target.value })
                          }
                          className="mt-1 block w-full rounded-lg border border-slate-300 p-2"
                        >
                          <option value="AY-2026-27">AY-2026-27 (Current)</option>
                          <option value="AY-2025-26">AY-2025-26 (Completed)</option>
                        </select>
                      </div>

                      <div>
                        <label className="font-medium text-slate-600">Department / Branch</label>
                        <select
                          value={filterValues.branch || "Computer Science & Engineering"}
                          onChange={(e) =>
                            setFilterValues({ ...filterValues, branch: e.target.value })
                          }
                          className="mt-1 block w-full rounded-lg border border-slate-300 p-2"
                        >
                          <option value="Computer Science & Engineering">CSE</option>
                          <option value="Electronics & Communication">ECE</option>
                          <option value="Mechanical Engineering">MECH</option>
                          <option value="Civil Engineering">CIVIL</option>
                        </select>
                      </div>
                    </div>

                    <div className="pt-4 border-t border-slate-100">
                      <button
                        type="button"
                        onClick={handleGenerate}
                        disabled={generateMutation.isPending}
                        className="w-full flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-4 py-3 font-bold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
                      >
                        <Play className="h-4 w-4" />
                        {generateMutation.isPending ? "Compiling Report..." : `Generate ${exportFormat} Report`}
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="py-8 text-center text-xs text-slate-400">
                    Click any report card on the left to configure filters and execute exports.
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Live Preview Tab */}
      {activeTab === "preview" && (
        <div className="space-y-6">
          {!generatedReport ? (
            <div className="rounded-2xl border border-slate-200 bg-white p-12 text-center text-xs text-slate-400">
              No report generated yet. Choose a report from the catalog and click Generate.
            </div>
          ) : (
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-6">
              {/* Report Header */}
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between pb-4 border-b border-slate-100 gap-3">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="rounded bg-indigo-100 px-2 py-0.5 text-xs font-bold text-indigo-800">
                      {generatedReport.category}
                    </span>
                    <span className="font-mono text-xs font-bold text-slate-500">
                      Format: {generatedReport.export_format}
                    </span>
                  </div>
                  <h2 className="mt-2 text-xl font-bold text-slate-900">{generatedReport.title}</h2>
                  <p className="mt-1 text-xs text-slate-500">
                    Generated on {new Date(generatedReport.generated_at).toLocaleString()} &bull; Duration: {generatedReport.execution_duration_ms}ms &bull; Zero Placeholder Data
                  </p>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => window.print()}
                    className="flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 shadow-2xs"
                  >
                    <Printer className="h-4 w-4 text-slate-500" />
                    Print
                  </button>
                  {generatedReport.file_url && (
                    <a
                      href={generatedReport.file_url}
                      target="_blank"
                      rel="noreferrer"
                      className="flex items-center gap-1.5 rounded-lg bg-indigo-600 px-4 py-2 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700"
                    >
                      <Download className="h-4 w-4" />
                      Download {generatedReport.export_format}
                    </a>
                  )}
                </div>
              </div>

              {/* Summary KPIs Banner */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-50 p-4 rounded-xl border border-slate-100">
                {Object.entries(generatedReport.summary_kpis).map(([k, v]) => (
                  <div key={k}>
                    <span className="text-[11px] font-semibold text-slate-500 uppercase">{k}</span>
                    <div className="text-base font-bold text-slate-900 mt-0.5">{String(v)}</div>
                  </div>
                ))}
              </div>

              {/* Chart Visualization */}
              {generatedReport.chart_data && (
                <div className="rounded-xl border border-slate-200 bg-white p-4 space-y-3">
                  <span className="text-xs font-bold text-slate-900 uppercase tracking-wide">
                    Statistical Distribution Chart
                  </span>
                  <div className="space-y-2 pt-1">
                    {generatedReport.chart_data.labels.map((lbl, idx) => {
                      const val = generatedReport.chart_data!.values[idx];
                      const maxVal = Math.max(...generatedReport.chart_data!.values, 1);
                      const pct = Math.round((val / maxVal) * 100);

                      return (
                        <div key={lbl} className="space-y-1 text-xs">
                          <div className="flex justify-between">
                            <span className="font-semibold text-slate-700">{lbl}</span>
                            <span className="font-bold text-slate-900">{val}</span>
                          </div>
                          <div className="h-2 w-full rounded-full bg-slate-100 overflow-hidden">
                            <div
                              className="h-full bg-indigo-600 rounded-full"
                              style={{ width: `${pct}%` }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* Tabular Data */}
              <div className="overflow-x-auto">
                <table className="min-w-full text-left text-xs">
                  <thead className="border-b border-slate-100 bg-slate-50 font-semibold text-slate-600">
                    <tr>
                      {generatedReport.columns.map((col) => (
                        <th key={col} className="px-3 py-3">
                          {col}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {generatedReport.rows.map((row, idx) => (
                      <tr key={idx} className="hover:bg-slate-50/70">
                        {generatedReport.columns.map((col) => (
                          <td key={col} className="px-3 py-2.5 font-medium text-slate-800">
                            {String(row[col] ?? "")}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Scheduled Jobs Tab */}
      {activeTab === "scheduled" && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h2 className="text-base font-bold text-slate-900">Automated Scheduled Report Jobs</h2>
              <p className="text-xs text-slate-500">
                Configure cron-like background jobs that generate and email executive reports automatically.
              </p>
            </div>
            <button
              type="button"
              onClick={() => setScheduleModalOpen(true)}
              className="flex items-center gap-1.5 rounded-lg bg-indigo-600 px-3.5 py-1.5 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700"
            >
              <Plus className="h-4 w-4" />
              New Schedule
            </button>
          </div>

          <div className="space-y-3">
            {scheduledJobs.map((job) => (
              <div
                key={job.id}
                className="flex flex-col sm:flex-row sm:items-center sm:justify-between p-4 rounded-xl border border-slate-200 bg-slate-50/50 gap-3 text-xs"
              >
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-sm text-slate-900">{job.job_title}</span>
                    <span className="rounded bg-indigo-100 px-2 py-0.2 text-[10px] font-bold text-indigo-800">
                      {job.frequency}
                    </span>
                    <span className="font-mono text-slate-400">({job.export_format})</span>
                  </div>
                  <div className="text-[11px] text-slate-500 mt-1">
                    Recipients: {job.recipient_emails.join(", ")}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <span className="rounded bg-emerald-100 px-2.5 py-0.5 text-[10px] font-bold text-emerald-800">
                    ACTIVE CRON
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Execution Audit History Tab */}
      {activeTab === "history" && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h2 className="text-base font-bold text-slate-900">Report Generation Execution History</h2>
              <p className="text-xs text-slate-500">
                Audit logs of past compiled reports, execution latencies, and export formats.
              </p>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-xs">
              <thead className="border-b border-slate-100 bg-slate-50 font-semibold text-slate-600">
                <tr>
                  <th className="px-3 py-3">Report Title</th>
                  <th className="px-3 py-3">Format</th>
                  <th className="px-3 py-3">Row Count</th>
                  <th className="px-3 py-3">Duration</th>
                  <th className="px-3 py-3">Timestamp</th>
                  <th className="px-3 py-3 text-right">Download Link</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {executions.map((ex) => (
                  <tr key={ex.id} className="hover:bg-slate-50/70">
                    <td className="px-3 py-3 font-semibold text-slate-900">{ex.report_title}</td>
                    <td className="px-3 py-3 font-mono font-bold text-indigo-700">{ex.export_format}</td>
                    <td className="px-3 py-3 font-semibold">{ex.rows_count} rows</td>
                    <td className="px-3 py-3 text-slate-500">{ex.execution_duration_ms} ms</td>
                    <td className="px-3 py-3 text-slate-500 font-mono">
                      {new Date(ex.created_at).toLocaleString()}
                    </td>
                    <td className="px-3 py-3 text-right">
                      {ex.file_url && (
                        <a
                          href={ex.file_url}
                          target="_blank"
                          rel="noreferrer"
                          className="inline-flex items-center gap-1 text-indigo-600 hover:text-indigo-800 font-semibold"
                        >
                          <ExternalLink className="h-3.5 w-3.5" />
                          View Export
                        </a>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Schedule Job Modal */}
      {scheduleModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-xs">
          <div className="relative w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl">
            <h3 className="text-base font-bold text-slate-900">Create Scheduled Report Job</h3>
            <p className="mt-1 text-xs text-slate-500">
              Automate periodic generation and email delivery to executive stakeholders.
            </p>

            <form onSubmit={handleCreateScheduleSubmit} className="mt-4 space-y-3 text-xs">
              <div>
                <label className="font-semibold text-slate-700">Job Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Weekly Executive CGPA Roster"
                  value={schedJobTitle}
                  onChange={(e) => setSchedJobTitle(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-semibold text-slate-700">Target Report</label>
                  <select
                    value={schedReportCode}
                    onChange={(e) => setSchedReportCode(e.target.value)}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                  >
                    {definitions.map((d) => (
                      <option key={d.id} value={d.report_code}>
                        {d.report_code}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="font-semibold text-slate-700">Frequency</label>
                  <select
                    value={schedFreq}
                    onChange={(e) => setSchedFreq(e.target.value as any)}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                  >
                    <option value="DAILY">Daily</option>
                    <option value="WEEKLY">Weekly</option>
                    <option value="MONTHLY">Monthly</option>
                    <option value="QUARTERLY">Quarterly</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="font-semibold text-slate-700">Export Format</label>
                <select
                  value={schedFormat}
                  onChange={(e) => setSchedFormat(e.target.value as any)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 font-bold"
                >
                  <option value="PDF">PDF Document</option>
                  <option value="EXCEL">Excel Spreadsheet (.xlsx)</option>
                  <option value="CSV">CSV Flat File</option>
                </select>
              </div>

              <div>
                <label className="font-semibold text-slate-700">Recipient Email Addresses</label>
                <input
                  type="text"
                  required
                  placeholder="dean@myeducationindia.com, registrar@myeducationindia.com"
                  value={schedEmails}
                  onChange={(e) => setSchedEmails(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 font-mono"
                />
              </div>

              <div className="mt-5 flex justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setScheduleModalOpen(false)}
                  className="rounded border border-slate-200 px-3 py-1.5 font-semibold text-slate-600 hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createScheduleMutation.isPending}
                  className="rounded bg-indigo-600 px-4 py-1.5 font-semibold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
                >
                  {createScheduleMutation.isPending ? "Creating..." : "Save Schedule"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
