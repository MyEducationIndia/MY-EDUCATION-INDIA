import React, { useState } from "react";
import { Link } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Activity,
  ArrowRight,
  Award,
  Bell,
  BookOpen,
  Briefcase,
  Building2,
  Calendar,
  CalendarCheck,
  CheckCircle2,
  Clock,
  Cpu,
  CreditCard,
  Download,
  GraduationCap,
  History,
  IndianRupee,
  Layers,
  Lock,
  Mail,
  MapPin,
  Monitor,
  MonitorPlay,
  Package,
  Plus,
  RefreshCw,
  Server,
  Shield,
  ShieldAlert,
  ShieldCheck,
  TrendingUp,
  User,
  UserCheck,
  Users,
  Video,
} from "lucide-react";
import { dashboardEngineService } from "@/services/dashboardEngineService";
import {
  DashboardKPICard,
  DashboardRoleKey,
} from "@/types/dashboardEngine.types";

const ROLE_OPTIONS: { key: DashboardRoleKey; label: string; badge: string }[] = [
  { key: "SUPER_ADMIN", label: "Super Admin", badge: "ROOT" },
  { key: "ADMIN", label: "Admin", badge: "CAMPUS" },
  { key: "PRINCIPAL", label: "Principal", badge: "EXEC" },
  { key: "FACULTY", label: "Faculty", badge: "TEACHING" },
  { key: "STUDENT", label: "Student", badge: "SIMS" },
  { key: "PARENT", label: "Parent", badge: "GUARDIAN" },
  { key: "RECEPTION", label: "Reception", badge: "DESK" },
  { key: "ACCOUNTANT", label: "Accountant", badge: "BURSAR" },
  { key: "LIBRARY", label: "Library", badge: "STACK" },
  { key: "CBT", label: "CBT Staff", badge: "ONLINE_EXAM" },
  { key: "LMS", label: "LMS Staff", badge: "E_LEARNING" },
  { key: "EXAMINATION_CELL", label: "Exam Cell", badge: "CONTROLLER" },
];

export const DashboardOverviewPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [selectedRole, setSelectedRole] = useState<DashboardRoleKey>("SUPER_ADMIN");
  const [taskModalOpen, setTaskModalOpen] = useState(false);
  const [taskTitle, setTaskTitle] = useState("");
  const [taskDesc, setTaskDesc] = useState("");
  const [taskPriority, setTaskPriority] = useState("NORMAL");

  // Fetch role-tailored dashboard bundle
  const { data: dashboard, isLoading, refetch } = useQuery({
    queryKey: ["role-dashboard", selectedRole],
    queryFn: () => dashboardEngineService.getRoleDashboard(selectedRole),
  });

  // Task creation mutation
  const createTaskMutation = useMutation({
    mutationFn: (payload: { title: string; description: string; priority: string; role_target: string }) =>
      dashboardEngineService.createTask(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["role-dashboard", selectedRole] });
      setTaskModalOpen(false);
      setTaskTitle("");
      setTaskDesc("");
      alert("New operational task added to role worklist!");
    },
  });

  const handleCreateTask = (e: React.FormEvent) => {
    e.preventDefault();
    void createTaskMutation.mutate({
      title: taskTitle,
      description: taskDesc,
      priority: taskPriority,
      role_target: selectedRole,
    });
  };

  const renderIcon = (iconName: string) => {
    const props = { className: "h-5 w-5" };
    switch (iconName) {
      case "building":
        return <Building2 {...props} />;
      case "users":
        return <Users {...props} />;
      case "server":
        return <Server {...props} />;
      case "shield":
      case "shield-check":
        return <ShieldCheck {...props} />;
      case "graduation-cap":
        return <GraduationCap {...props} />;
      case "briefcase":
        return <Briefcase {...props} />;
      case "clock":
        return <Clock {...props} />;
      case "indian-rupee":
        return <IndianRupee {...props} />;
      case "award":
        return <Award {...props} />;
      case "calendar-check":
        return <CalendarCheck {...props} />;
      case "trending-up":
        return <TrendingUp {...props} />;
      case "book-open":
        return <BookOpen {...props} />;
      case "monitor":
      case "monitor-play":
        return <MonitorPlay {...props} />;
      case "cpu":
        return <Cpu {...props} />;
      case "package":
        return <Package {...props} />;
      default:
        return <Activity {...props} />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Role Switcher Navigation Bar */}
      <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 pb-3 border-b border-slate-100">
          <div>
            <div className="flex items-center gap-2">
              <span className="rounded-md bg-indigo-100 px-2 py-0.5 text-xs font-bold text-indigo-800">
                Module 6
              </span>
              <span className="text-xs font-bold text-slate-900 uppercase tracking-wide">
                Dynamic Role Dashboard Engine
              </span>
            </div>
            <p className="mt-0.5 text-xs text-slate-500">
              Select any of the 12 institutional roles to simulate tailored widgets, analytics, tasks, and quick actions.
            </p>
          </div>
          <button
            type="button"
            onClick={() => void refetch()}
            className="flex items-center gap-1.5 self-start sm:self-center rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 hover:bg-slate-50 shadow-2xs"
          >
            <RefreshCw className="h-3.5 w-3.5" />
            Refresh Feed
          </button>
        </div>

        {/* 12 Role Selector Pills */}
        <div className="mt-3 flex overflow-x-auto gap-1.5 pb-1">
          {ROLE_OPTIONS.map((r) => {
            const isSelected = selectedRole === r.key;
            return (
              <button
                key={r.key}
                type="button"
                onClick={() => setSelectedRole(r.key)}
                className={`flex items-center gap-1.5 rounded-xl px-3 py-1.5 text-xs font-semibold whitespace-nowrap transition-all ${
                  isSelected
                    ? "bg-indigo-600 text-white shadow-xs"
                    : "bg-slate-50 text-slate-600 hover:bg-slate-100 hover:text-slate-900 border border-slate-200"
                }`}
              >
                <span>{r.label}</span>
                <span
                  className={`rounded px-1.5 py-0.2 text-[9px] font-mono font-bold ${
                    isSelected ? "bg-indigo-700 text-indigo-100" : "bg-slate-200 text-slate-700"
                  }`}
                >
                  {r.badge}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {isLoading ? (
        <div className="rounded-2xl border border-slate-200 bg-white p-16 text-center text-sm text-slate-500">
          Loading role-tailored dashboard from PostgreSQL Neon serverless backend...
        </div>
      ) : !dashboard ? null : (
        <>
          {/* Role Welcome Banner */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <div className="flex items-center gap-2">
                  <span className="rounded-full bg-emerald-100 px-3 py-0.5 text-xs font-bold text-emerald-800">
                    Live Session Active
                  </span>
                  <span className="font-mono text-xs text-slate-400">
                    Flagship: MEI-HQ Indore &bull; AY-2026-27
                  </span>
                </div>
                <h1 className="mt-2 text-2xl font-bold tracking-tight text-slate-900">
                  {dashboard.role_title}
                </h1>
                <p className="mt-1 text-xs text-slate-500">
                  Role Scope: <span className="font-mono font-bold text-indigo-700">{dashboard.role_key}</span> &bull; Synchronized with Neon PostgreSQL &bull; Zero Client Storage
                </p>
              </div>

              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setTaskModalOpen(true)}
                  className="flex items-center gap-1.5 rounded-xl bg-indigo-600 px-4 py-2 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700"
                >
                  <Plus className="h-4 w-4" />
                  Add Operational Task
                </button>
              </div>
            </div>
          </div>

          {/* KPI Statistics Grid */}
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {dashboard.kpis.map((kpi) => (
              <div
                key={kpi.key}
                className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs hover:border-indigo-300 transition-all"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">
                    {kpi.label}
                  </span>
                  <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600">
                    {renderIcon(kpi.icon)}
                  </div>
                </div>
                <div className="mt-2 text-2xl font-bold tracking-tight text-slate-900">
                  {kpi.value}
                </div>
                <div className="mt-2 flex items-center justify-between text-xs">
                  <span
                    className={`font-semibold ${
                      kpi.is_positive ? "text-emerald-600" : "text-rose-600"
                    }`}
                  >
                    {kpi.delta}
                  </span>
                  <span className="text-slate-400 text-[11px]">{kpi.trend}</span>
                </div>
              </div>
            ))}
          </div>

          {/* Quick Actions Bar */}
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
            <h2 className="text-xs font-bold text-slate-900 uppercase tracking-wide mb-3">
              Role Quick Actions & Subsystem Launchers
            </h2>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {dashboard.quick_actions.map((act) => (
                <Link
                  key={act.action_key}
                  to={act.route}
                  className={`flex items-center gap-2.5 rounded-xl border p-3 text-xs font-semibold transition-all ${
                    act.is_primary
                      ? "bg-indigo-50/80 border-indigo-200 text-indigo-900 hover:bg-indigo-100"
                      : "bg-slate-50/60 border-slate-200 text-slate-700 hover:bg-slate-100"
                  }`}
                >
                  <div className="text-indigo-600">{renderIcon(act.icon)}</div>
                  <span className="truncate">{act.label}</span>
                </Link>
              ))}
            </div>
          </div>

          {/* Middle Analytics & Tasks Section */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Charts & Analytics (2 Cols) */}
            <div className="lg:col-span-2 space-y-6">
              {dashboard.charts.map((chart) => (
                <div
                  key={chart.chart_key}
                  className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs"
                >
                  <div className="flex items-center justify-between pb-4 border-b border-slate-100">
                    <div>
                      <h3 className="text-sm font-bold text-slate-900">{chart.title}</h3>
                      <span className="font-mono text-[10px] text-slate-400 uppercase">
                        Type: {chart.chart_type} chart
                      </span>
                    </div>
                    <span className="rounded bg-indigo-50 px-2 py-0.5 text-[10px] font-bold text-indigo-700">
                      LIVE DATA
                    </span>
                  </div>

                  {/* Clean CSS Visualization of Chart Data */}
                  <div className="mt-5 space-y-3">
                    {chart.chart_type === "donut" ? (
                      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                        {chart.labels.map((lbl, idx) => {
                          const val = chart.datasets[0]?.data[idx] || 0;
                          return (
                            <div
                              key={lbl}
                              className="rounded-xl border border-slate-100 bg-slate-50/60 p-3"
                            >
                              <div className="text-[11px] font-medium text-slate-500">{lbl}</div>
                              <div className="text-lg font-bold text-slate-900 mt-1">{val}%</div>
                              <div className="mt-1.5 h-1.5 w-full rounded-full bg-slate-200 overflow-hidden">
                                <div
                                  className="h-full bg-indigo-600 rounded-full"
                                  style={{ width: `${val}%` }}
                                />
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    ) : (
                      <div className="space-y-2">
                        {chart.labels.map((lbl, idx) => {
                          const val1 = chart.datasets[0]?.data[idx] || 0;
                          const maxVal = Math.max(...chart.datasets[0].data, 1);
                          const pct = Math.round((val1 / maxVal) * 100);

                          return (
                            <div key={lbl} className="space-y-1">
                              <div className="flex justify-between text-xs">
                                <span className="font-medium text-slate-700">{lbl}</span>
                                <span className="font-bold text-slate-900">
                                  {val1} {chart.chart_key === "academic_attendance" ? "%" : ""}
                                </span>
                              </div>
                              <div className="h-2 w-full rounded-full bg-slate-100 overflow-hidden">
                                <div
                                  className="h-full bg-indigo-600 rounded-full transition-all duration-500"
                                  style={{ width: `${pct}%` }}
                                />
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {/* Actionable Tasks & Calendar (1 Col) */}
            <div className="space-y-6">
              {/* Task Worklist */}
              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
                <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                  <div className="flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-indigo-600" />
                    <h3 className="text-xs font-bold text-slate-900 uppercase">
                      Role Tasks ({dashboard.tasks.length})
                    </h3>
                  </div>
                  <button
                    type="button"
                    onClick={() => setTaskModalOpen(true)}
                    className="text-xs font-semibold text-indigo-600 hover:text-indigo-800"
                  >
                    + Add
                  </button>
                </div>

                <div className="mt-3 space-y-2.5">
                  {!dashboard.tasks.length ? (
                    <div className="py-6 text-center text-xs text-slate-400">
                      No pending tasks for this role.
                    </div>
                  ) : (
                    dashboard.tasks.map((task) => (
                      <div
                        key={task.id}
                        className="rounded-xl border border-slate-100 bg-slate-50/60 p-3 text-xs space-y-1 hover:border-indigo-200 transition-colors"
                      >
                        <div className="flex items-start justify-between gap-2">
                          <span className="font-bold text-slate-900 leading-snug">
                            {task.title}
                          </span>
                          <span
                            className={`rounded px-1.5 py-0.2 text-[9px] font-bold ${
                              task.priority === "URGENT"
                                ? "bg-rose-100 text-rose-800"
                                : task.priority === "HIGH"
                                ? "bg-amber-100 text-amber-800"
                                : "bg-slate-200 text-slate-700"
                            }`}
                          >
                            {task.priority}
                          </span>
                        </div>
                        {task.description && (
                          <p className="text-[11px] text-slate-500 leading-relaxed">
                            {task.description}
                          </p>
                        )}
                        <div className="flex items-center justify-between text-[10px] text-slate-400 pt-1">
                          <span>Target: {task.role_target}</span>
                          <span className="font-semibold text-emerald-600">{task.status}</span>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>

              {/* Academic & Examination Calendar */}
              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
                <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
                  <Calendar className="h-4 w-4 text-indigo-600" />
                  <h3 className="text-xs font-bold text-slate-900 uppercase">
                    Upcoming Calendar Schedule
                  </h3>
                </div>

                <div className="mt-3 space-y-2.5 text-xs">
                  {dashboard.calendar_events.map((ev) => (
                    <div
                      key={ev.id}
                      className="rounded-xl border border-slate-100 bg-slate-50/50 p-3 space-y-1"
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-slate-900 text-xs">{ev.title}</span>
                        <span
                          className={`rounded px-1.5 py-0.2 text-[9px] font-bold ${
                            ev.category === "EXAM"
                              ? "bg-purple-100 text-purple-800"
                              : "bg-indigo-100 text-indigo-800"
                          }`}
                        >
                          {ev.category}
                        </span>
                      </div>
                      <div className="text-[11px] text-slate-500 font-medium">
                        {ev.event_date} &bull; {ev.time_slot}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Priority Notifications */}
              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
                <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
                  <Bell className="h-4 w-4 text-indigo-600" />
                  <h3 className="text-xs font-bold text-slate-900 uppercase">
                    Live Notification Feed
                  </h3>
                </div>

                <div className="mt-3 space-y-2.5 text-xs">
                  {dashboard.notifications.map((n) => (
                    <div
                      key={n.id}
                      className="rounded-xl border border-slate-100 bg-slate-50/50 p-3 space-y-1"
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-slate-900">{n.title}</span>
                        <span className="text-[9px] font-mono text-slate-400">{n.category}</span>
                      </div>
                      <p className="text-[11px] text-slate-500 leading-relaxed">{n.message}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </>
      )}

      {/* Add Task Modal */}
      {taskModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-xs">
          <div className="relative w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl">
            <h3 className="text-base font-bold text-slate-900">
              Create Role Task ({selectedRole})
            </h3>
            <p className="mt-1 text-xs text-slate-500">
              Assign an actionable item to the {selectedRole} dashboard worklist.
            </p>

            <form onSubmit={handleCreateTask} className="mt-4 space-y-3 text-xs">
              <div>
                <label className="font-semibold text-slate-700">Task Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Audit Mid-Term Moderation Curves"
                  value={taskTitle}
                  onChange={(e) => setTaskTitle(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                />
              </div>

              <div>
                <label className="font-semibold text-slate-700">Description</label>
                <textarea
                  rows={3}
                  placeholder="Provide detailed instructions..."
                  value={taskDesc}
                  onChange={(e) => setTaskDesc(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                />
              </div>

              <div>
                <label className="font-semibold text-slate-700">Priority Level</label>
                <select
                  value={taskPriority}
                  onChange={(e) => setTaskPriority(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 font-semibold"
                >
                  <option value="LOW">LOW</option>
                  <option value="NORMAL">NORMAL</option>
                  <option value="HIGH">HIGH</option>
                  <option value="URGENT">URGENT</option>
                </select>
              </div>

              <div className="mt-5 flex justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setTaskModalOpen(false)}
                  className="rounded border border-slate-200 px-3 py-1.5 font-semibold text-slate-600 hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createTaskMutation.isPending}
                  className="rounded bg-indigo-600 px-4 py-1.5 font-semibold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
                >
                  {createTaskMutation.isPending ? "Adding..." : "Add Task"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
