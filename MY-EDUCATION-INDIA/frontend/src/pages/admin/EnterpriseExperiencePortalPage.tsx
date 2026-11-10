import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Sparkles,
  ShieldAlert,
  ShieldCheck,
  Building2,
  GraduationCap,
  BookOpen,
  Target,
  IndianRupee,
  PhoneCall,
  Award,
  Briefcase,
  Sliders,
  CheckCircle2,
  AlertCircle,
  Radio,
  Bell,
  RefreshCw,
  ExternalLink,
  Layers,
  Zap,
  Lock,
  Unlock,
  Plus,
  Send,
  X,
  Eye,
  Check,
} from "lucide-react";
import { experienceService } from "@/services/experienceService";
import {
  PortalItem,
  RootOwnerOverview,
  NotificationItem,
  ModulesRegistryResponse,
  PortalProfileResponse,
} from "@/types/experience.types";

export const EnterpriseExperiencePortalPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<
    "portals" | "simulator" | "notifications" | "blueprint" | "diagnostics"
  >("portals");

  const [selectedPortalType, setSelectedPortalType] = useState<string>("STUDENT");

  // Broadcast modal state
  const [isBroadcastModalOpen, setIsBroadcastModalOpen] = useState(false);
  const [broadcastForm, setBroadcastForm] = useState({
    title: "",
    category: "ACADEMIC",
    message: "",
    priority: "HIGH",
  });

  // Queries
  const { data: rootOverview, isLoading: rootLoading, refetch: refetchRoot } =
    useQuery<RootOwnerOverview>({
      queryKey: ["experience_root_overview"],
      queryFn: experienceService.getRootOverview,
    });

  const { data: portals = [], isLoading: portalsLoading } =
    useQuery<PortalItem[]>({
      queryKey: ["experience_portals"],
      queryFn: experienceService.listPortals,
    });

  const { data: portalProfile, isLoading: profileLoading } =
    useQuery<PortalProfileResponse>({
      queryKey: ["experience_portal_profile", selectedPortalType],
      queryFn: async () => {
        return await experienceService.getPortalProfile(selectedPortalType);
      },
    });

  const { data: notifications = [], isLoading: notifsLoading, refetch: refetchNotifs } =
    useQuery<NotificationItem[]>({
      queryKey: ["experience_notifications"],
      queryFn: experienceService.listNotifications,
    });

  const { data: registry, isLoading: registryLoading } =
    useQuery<ModulesRegistryResponse>({
      queryKey: ["experience_modules_registry"],
      queryFn: experienceService.getModulesRegistry,
    });

  // Mutations
  const toggleLockdownMutation = useMutation({
    mutationFn: async (active?: boolean) => {
      return await experienceService.toggleLockdown(active);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["experience_root_overview"] });
    },
  });

  const broadcastMutation = useMutation({
    mutationFn: async (payload: typeof broadcastForm) => {
      return await experienceService.broadcastNotification(payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["experience_notifications"] });
      setIsBroadcastModalOpen(false);
      setBroadcastForm({
        title: "",
        category: "ACADEMIC",
        message: "",
        priority: "HIGH",
      });
    },
  });

  const getPortalIcon = (iconName: string) => {
    switch (iconName) {
      case "ShieldAlert":
        return <ShieldAlert className="w-5 h-5 text-indigo-500" />;
      case "Sliders":
        return <Sliders className="w-5 h-5 text-blue-500" />;
      case "Building2":
        return <Building2 className="w-5 h-5 text-teal-500" />;
      case "GraduationCap":
        return <GraduationCap className="w-5 h-5 text-emerald-500" />;
      case "BookOpen":
        return <BookOpen className="w-5 h-5 text-indigo-600" />;
      case "Target":
        return <Target className="w-5 h-5 text-amber-500" />;
      case "IndianRupee":
        return <IndianRupee className="w-5 h-5 text-cyan-500" />;
      case "PhoneCall":
        return <PhoneCall className="w-5 h-5 text-purple-500" />;
      case "Award":
        return <Award className="w-5 h-5 text-orange-500" />;
      case "Briefcase":
        return <Briefcase className="w-5 h-5 text-pink-500" />;
      default:
        return <Sparkles className="w-5 h-5 text-indigo-500" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner - Flagship Autonomous Campus Completion */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-xl border border-slate-800">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-indigo-400 font-semibold text-xs tracking-wider uppercase">
              <Sparkles className="w-4 h-4 text-amber-400" /> Module 20 Enterprise Experience Platform (Final Milestone)
            </div>
            <h1 className="text-2xl sm:text-3xl font-black text-white">
              Unified Campus Experience & Portals Hub
            </h1>
            <p className="text-slate-300 text-xs sm:text-sm max-w-2xl leading-relaxed">
              Consolidated persona experiences across 10 specialized portals:
              Students, Faculty, Parents, Counsellors, Recruiters, and Sovereign
              Root Administration for Indore Flagship Campus (`MEI-HQ`).
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => {
                refetchRoot();
                refetchNotifs();
              }}
              className="inline-flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-bold transition border border-slate-700"
            >
              <RefreshCw className="w-4 h-4" /> Refresh Engine
            </button>
            <button
              onClick={() => setIsBroadcastModalOpen(true)}
              className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition shadow-sm"
            >
              <Radio className="w-4 h-4" /> Broadcast Announcement
            </button>
          </div>
        </div>

        {/* Master Blueprint Completion Counters */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-6">
          <div className="bg-slate-800/80 rounded-2xl p-4 border border-slate-700/60">
            <p className="text-xs text-slate-400 font-medium">Master Blueprint Scope</p>
            <p className="text-2xl font-black text-emerald-400 mt-1 flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-400" /> 20 / 20 Complete
            </p>
            <span className="text-xs text-slate-300 font-medium mt-0.5">
              100% Subsystems Live
            </span>
          </div>

          <div className="bg-slate-800/80 rounded-2xl p-4 border border-slate-700/60">
            <p className="text-xs text-slate-400 font-medium">Provisioned Persona Portals</p>
            <p className="text-2xl font-bold text-white mt-1">
              10 Specialized Portals
            </p>
            <span className="text-xs text-indigo-400 font-medium mt-0.5">
              Single Universal Auth
            </span>
          </div>

          <div className="bg-slate-800/80 rounded-2xl p-4 border border-slate-700/60">
            <p className="text-xs text-slate-400 font-medium">Autonomous Campus</p>
            <p className="text-2xl font-bold text-white mt-1">MEI-HQ</p>
            <span className="text-xs text-slate-300 font-medium mt-0.5">
              Indore, Madhya Pradesh
            </span>
          </div>

          <div className="bg-slate-800/80 rounded-2xl p-4 border border-slate-700/60">
            <p className="text-xs text-slate-400 font-medium">Emergency Lockdown</p>
            <div className="mt-1 flex items-center justify-between">
              <span
                className={`text-sm font-black ${
                  rootOverview?.emergency_lockdown_active
                    ? "text-rose-400"
                    : "text-emerald-400"
                }`}
              >
                {rootOverview?.emergency_lockdown_active ? "LOCKED DOWN" : "NORMAL"}
              </span>
              <button
                onClick={() =>
                  toggleLockdownMutation.mutate(!rootOverview?.emergency_lockdown_active)
                }
                className={`px-2.5 py-1 rounded text-[10px] font-bold uppercase transition flex items-center gap-1 ${
                  rootOverview?.emergency_lockdown_active
                    ? "bg-rose-600 text-white hover:bg-rose-700"
                    : "bg-slate-700 text-slate-300 hover:bg-slate-600"
                }`}
              >
                {rootOverview?.emergency_lockdown_active ? (
                  <>
                    <Unlock className="w-3 h-3" /> Unlock
                  </>
                ) : (
                  <>
                    <Lock className="w-3 h-3" /> Lock
                  </>
                )}
              </button>
            </div>
            <span className="text-[11px] text-slate-400 font-mono mt-0.5 block">
              Sovereign Root Protection
            </span>
          </div>
        </div>
      </div>

      {/* Main Subtabs Navigation */}
      <div className="flex border-b border-slate-200 space-x-1 sm:space-x-4 overflow-x-auto no-scrollbar">
        <button
          onClick={() => setActiveTab("portals")}
          className={`pb-3 px-3 text-sm font-bold border-b-2 transition flex items-center gap-2 whitespace-nowrap ${
            activeTab === "portals"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-slate-600 hover:text-slate-900"
          }`}
        >
          <Layers className="w-4 h-4" /> Persona Portals ({portals.length})
        </button>
        <button
          onClick={() => setActiveTab("simulator")}
          className={`pb-3 px-3 text-sm font-bold border-b-2 transition flex items-center gap-2 whitespace-nowrap ${
            activeTab === "simulator"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-slate-600 hover:text-slate-900"
          }`}
        >
          <Eye className="w-4 h-4" /> Experience Simulator
        </button>
        <button
          onClick={() => setActiveTab("notifications")}
          className={`pb-3 px-3 text-sm font-bold border-b-2 transition flex items-center gap-2 whitespace-nowrap ${
            activeTab === "notifications"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-slate-600 hover:text-slate-900"
          }`}
        >
          <Bell className="w-4 h-4" /> Universal Notification Center ({notifications.length})
        </button>
        <button
          onClick={() => setActiveTab("blueprint")}
          className={`pb-3 px-3 text-sm font-bold border-b-2 transition flex items-center gap-2 whitespace-nowrap ${
            activeTab === "blueprint"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-slate-600 hover:text-slate-900"
          }`}
        >
          <Sparkles className="w-4 h-4" /> 20-Module ERP Blueprint Matrix (20)
        </button>
      </div>

      {/* Tab 1: Persona Portals Switcher */}
      {activeTab === "portals" && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-bold text-slate-900">
                10 Provisioned Persona Portals
              </h2>
              <p className="text-xs text-slate-500">
                Select any portal to inspect its allowed roles, theme palette, and
                default navigation route.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {portals.map((p) => {
              const isSelected = selectedPortalType === p.portal_type;
              return (
                <div
                  key={p.portal_type}
                  onClick={() => setSelectedPortalType(p.portal_type)}
                  className={`rounded-2xl p-5 border shadow-2xs hover:shadow-md transition cursor-pointer space-y-3 flex flex-col justify-between ${
                    isSelected
                      ? "border-indigo-600 bg-indigo-50/40 ring-2 ring-indigo-500/20"
                      : "border-slate-200/90 bg-white"
                  }`}
                >
                  <div className="space-y-2">
                    <div className="flex items-start justify-between">
                      <div className="p-2.5 bg-slate-50 rounded-xl border border-slate-100">
                        {getPortalIcon(p.icon)}
                      </div>
                      <span
                        className="w-3 h-3 rounded-full"
                        style={{ backgroundColor: p.accent_color }}
                        title="Theme Accent Color"
                      />
                    </div>

                    <h3 className="font-bold text-slate-900 text-base">
                      {p.display_title}
                    </h3>
                    <p className="text-xs text-slate-500 leading-relaxed">
                      {p.tagline}
                    </p>
                  </div>

                  <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                    <span className="font-mono text-[11px] text-slate-400">
                      Route: {p.default_route}
                    </span>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setSelectedPortalType(p.portal_type);
                        setActiveTab("simulator");
                      }}
                      className="text-xs font-bold text-indigo-600 hover:text-indigo-800 flex items-center gap-1"
                    >
                      Simulate <Eye className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Tab 2: Persona Experience Simulator */}
      {activeTab === "simulator" && portalProfile && (
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-4 border-b border-slate-100">
            <div className="space-y-1">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                Active Simulation Persona
              </span>
              <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
                {portalProfile.portal.display_title}
              </h2>
              <p className="text-xs text-slate-500">
                {portalProfile.portal.tagline}
              </p>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold text-slate-500">
                Select Persona:
              </span>
              <select
                value={selectedPortalType}
                onChange={(e) => setSelectedPortalType(e.target.value)}
                className="border border-slate-300 rounded-xl px-3 py-1.5 text-xs font-bold bg-white text-slate-700 outline-none focus:ring-2 focus:ring-indigo-500"
              >
                {portals.map((p) => (
                  <option key={p.portal_type} value={p.portal_type}>
                    {p.display_title}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-5 bg-slate-50 rounded-2xl border border-slate-100 space-y-3">
              <h4 className="font-bold text-slate-900 text-sm">
                Persona Profile Parameters
              </h4>
              <div className="space-y-2 text-xs text-slate-600">
                <p>Default Landing Route: <strong className="font-mono">{portalProfile.portal.default_route}</strong></p>
                <p>Allowed Roles: <strong className="font-mono">{portalProfile.portal.allowed_roles.join(", ")}</strong></p>
                <p>Theme Accent: <strong className="font-mono">{portalProfile.portal.accent_color}</strong></p>
                <p>Notifications: <strong className="text-emerald-600 font-bold">Enabled (Push/SMS/Email)</strong></p>
              </div>
            </div>

            <div className="md:col-span-2 p-5 bg-slate-50 rounded-2xl border border-slate-100 space-y-3">
              <h4 className="font-bold text-slate-900 text-sm">
                Active Accessible Subsystems (Across 20 Master Modules)
              </h4>
              <div className="flex flex-wrap gap-1.5 max-h-48 overflow-y-auto">
                {portalProfile.allowed_subsystems.map((sub, idx) => (
                  <span
                    key={idx}
                    className="px-2.5 py-1 bg-white border border-slate-200 rounded-lg text-xs font-semibold text-slate-700 shadow-2xs"
                  >
                    {sub}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 3: Universal Notification Center */}
      {activeTab === "notifications" && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-900">
                Universal Notification Broadcast Ledger
              </h2>
              <p className="text-xs text-slate-500">
                Real-time operational alerts dispatched across all student, faculty, and administrative portals.
              </p>
            </div>
            <button
              onClick={() => setIsBroadcastModalOpen(true)}
              className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition shadow-sm"
            >
              <Radio className="w-4 h-4" /> Broadcast Announcement
            </button>
          </div>

          <div className="divide-y divide-slate-100 bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
            {notifications.map((n) => (
              <div key={n.id} className="p-4 sm:p-5 flex items-start gap-4 hover:bg-slate-50/70 transition">
                <div className="p-2.5 bg-indigo-50 text-indigo-600 rounded-xl shrink-0 mt-0.5">
                  <Bell className="w-5 h-5" />
                </div>
                <div className="flex-1 space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-slate-100 text-slate-700">
                      {n.category}
                    </span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-indigo-50 text-indigo-700">
                      {n.priority}
                    </span>
                    <span className="text-[11px] text-slate-400 ml-auto">
                      {new Date(n.timestamp).toLocaleTimeString()} • {new Date(n.timestamp).toLocaleDateString()}
                    </span>
                  </div>
                  <h4 className="font-bold text-slate-900 text-sm">
                    {n.title}
                  </h4>
                  <p className="text-xs text-slate-600 leading-relaxed">
                    {n.message}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 4: 20-Module ERP Blueprint Matrix */}
      {activeTab === "blueprint" && registry && (
        <div className="space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-slate-200">
            <div>
              <h2 className="text-lg font-bold text-slate-900">
                MY EDUCATION INDIA ERP Master Blueprint (All 20 Modules)
              </h2>
              <p className="text-xs text-slate-500">
                Complete system verification ledger for Indore Central Campus (`MEI-HQ`).
              </p>
            </div>
            <span className="px-3 py-1 bg-emerald-100 text-emerald-800 rounded-full text-xs font-black">
              100% COMPLETE & VERIFIED
            </span>
          </div>

          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm text-slate-700">
                <thead className="bg-slate-50 border-b border-slate-200 text-xs font-bold text-slate-500 uppercase tracking-wider">
                  <tr>
                    <th className="py-3 px-4">Module #</th>
                    <th className="py-3 px-4">Subsystem Name</th>
                    <th className="py-3 px-4">Category</th>
                    <th className="py-3 px-4">Subdomain</th>
                    <th className="py-3 px-4 text-right">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 text-xs">
                  {registry.modules.map((m) => (
                    <tr key={m.id} className="hover:bg-slate-50/80 transition">
                      <td className="py-3 px-4 font-mono font-bold text-indigo-700">
                        Module {m.id}
                      </td>
                      <td className="py-3 px-4 font-bold text-slate-900">
                        {m.name}
                      </td>
                      <td className="py-3 px-4">
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-slate-100 text-slate-700">
                          {m.category}
                        </span>
                      </td>
                      <td className="py-3 px-4 font-mono text-slate-500">
                        {m.subdomain}.myeducationindia.edu.in
                      </td>
                      <td className="py-3 px-4 text-right">
                        <span className="inline-flex items-center gap-1 font-bold text-emerald-600">
                          <CheckCircle2 className="w-3.5 h-3.5" /> LIVE
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Broadcast Modal */}
      {isBroadcastModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl border border-slate-100 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="font-bold text-slate-900 text-lg flex items-center gap-2">
                <Radio className="w-5 h-5 text-indigo-600" /> Broadcast Campus Announcement
              </h3>
              <button
                onClick={() => setIsBroadcastModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Announcement Title *
                </label>
                <input
                  type="text"
                  placeholder="e.g. End-Semester Examination Admit Cards Available"
                  value={broadcastForm.title}
                  onChange={(e) =>
                    setBroadcastForm({ ...broadcastForm, title: e.target.value })
                  }
                  className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Category *
                  </label>
                  <select
                    value={broadcastForm.category}
                    onChange={(e) =>
                      setBroadcastForm({
                        ...broadcastForm,
                        category: e.target.value,
                      })
                    }
                    className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                  >
                    <option value="ACADEMIC">ACADEMIC</option>
                    <option value="ADMISSIONS">ADMISSIONS</option>
                    <option value="FINANCE">FINANCE</option>
                    <option value="DEVOPS">DEVOPS</option>
                    <option value="GENERAL">GENERAL</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Priority *
                  </label>
                  <select
                    value={broadcastForm.priority}
                    onChange={(e) =>
                      setBroadcastForm({
                        ...broadcastForm,
                        priority: e.target.value,
                      })
                    }
                    className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                  >
                    <option value="HIGH">HIGH</option>
                    <option value="MEDIUM">MEDIUM</option>
                    <option value="LOW">LOW</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Broadcast Message Body *
                </label>
                <textarea
                  rows={3}
                  placeholder="Official institutional message dispatched in real-time across all portals..."
                  value={broadcastForm.message}
                  onChange={(e) =>
                    setBroadcastForm({ ...broadcastForm, message: e.target.value })
                  }
                  className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                />
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-3">
              <button
                onClick={() => setIsBroadcastModalOpen(false)}
                className="px-4 py-2 border border-slate-300 text-slate-700 rounded-xl text-xs font-bold hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  if (!broadcastForm.title || !broadcastForm.message) {
                    alert("Please provide title and message");
                    return;
                  }
                  broadcastMutation.mutate(broadcastForm);
                }}
                disabled={broadcastMutation.isPending}
                className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition flex items-center gap-2"
              >
                <Send className="w-4 h-4" /> Dispatch Broadcast
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
