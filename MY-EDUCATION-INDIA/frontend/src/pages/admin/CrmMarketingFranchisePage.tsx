import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Users,
  Target,
  Megaphone,
  Building2,
  Calendar,
  Phone,
  Mail,
  Plus,
  Trash2,
  Edit2,
  ArrowRight,
  CheckCircle2,
  AlertCircle,
  TrendingUp,
  IndianRupee,
  Sparkles,
  Filter,
  Search,
  RefreshCw,
  X,
  Send,
  MessageSquare,
  Clock,
  Layers,
  Award,
} from "lucide-react";
import { crmService } from "@/services/crmService";
import {
  CrmLead,
  CrmFollowup,
  CrmCampaign,
  FranchiseCenter,
  CrmPipelineStage,
} from "@/types/crm.types";

export const CrmMarketingFranchisePage: React.FC = () => {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<
    "kanban" | "followups" | "campaigns" | "franchise"
  >("kanban");

  const [searchLead, setSearchLead] = useState("");
  const [stageFilter, setStageFilter] = useState("ALL");

  // Modals state
  const [isLeadModalOpen, setIsLeadModalOpen] = useState(false);
  const [leadForm, setLeadForm] = useState({
    full_name: "",
    mobile: "",
    email: "",
    guardian_name: "",
    course_interested_id: "B.Tech Computer Science & Engineering",
    priority: "HIGH" as "LOW" | "MEDIUM" | "HIGH" | "URGENT",
    assigned_counsellor_id: "Dr. Anita Desai",
    remarks: "",
  });

  const [isFollowupModalOpen, setIsFollowupModalOpen] = useState(false);
  const [selectedLeadForFollowup, setSelectedLeadForFollowup] =
    useState<CrmLead | null>(null);
  const [followupForm, setFollowupForm] = useState({
    channel: "CALL" as "CALL" | "WHATSAPP" | "SMS" | "EMAIL" | "MEETING",
    notes: "",
    outcome: "INTERESTED",
    scheduled_at: new Date().toISOString(),
  });

  const [isCampaignModalOpen, setIsCampaignModalOpen] = useState(false);
  const [campaignForm, setCampaignForm] = useState({
    campaign_name: "",
    channel: "GOOGLE_ADS",
    allocated_budget: 150000,
    utm_source: "google",
    utm_campaign: "admissions_2026",
    start_date: new Date().toISOString().split("T")[0],
  });

  const [isFranchiseModalOpen, setIsFranchiseModalOpen] = useState(false);
  const [franchiseForm, setFranchiseForm] = useState({
    center_name: "",
    center_code: "",
    city: "Indore",
    state: "Madhya Pradesh",
    contact_email: "",
    contact_phone: "",
    royalty_percentage: 15.0,
  });

  // Queries
  const { data: dashboardMetrics } = useQuery({
    queryKey: ["crm_dashboard"],
    queryFn: crmService.getDashboard,
  });

  const { data: pipelineStages = [] } = useQuery<CrmPipelineStage[]>({
    queryKey: ["crm_pipeline_stages"],
    queryFn: crmService.getPipelineStages,
  });

  const {
    data: leads = [],
    isLoading: leadsLoading,
    refetch: refetchLeads,
  } = useQuery<CrmLead[]>({
    queryKey: ["crm_leads", stageFilter, searchLead],
    queryFn: async () => {
      return await crmService.listLeads(stageFilter, searchLead);
    },
  });

  const {
    data: followups = [],
    isLoading: followupsLoading,
    refetch: refetchFollowups,
  } = useQuery<CrmFollowup[]>({
    queryKey: ["crm_followups"],
    queryFn: async () => {
      return await crmService.listFollowups();
    },
  });

  const {
    data: campaigns = [],
    isLoading: campaignsLoading,
    refetch: refetchCampaigns,
  } = useQuery<CrmCampaign[]>({
    queryKey: ["crm_campaigns"],
    queryFn: crmService.listCampaigns,
  });

  const {
    data: franchiseCenters = [],
    isLoading: franchiseLoading,
    refetch: refetchFranchise,
  } = useQuery<FranchiseCenter[]>({
    queryKey: ["crm_franchise_centers"],
    queryFn: crmService.listFranchiseCenters,
  });

  // Mutations
  const createLeadMutation = useMutation({
    mutationFn: async (payload: typeof leadForm) => {
      return await crmService.createLead(payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["crm_leads"] });
      queryClient.invalidateQueries({ queryKey: ["crm_dashboard"] });
      setIsLeadModalOpen(false);
      setLeadForm({
        full_name: "",
        mobile: "",
        email: "",
        guardian_name: "",
        course_interested_id: "B.Tech Computer Science & Engineering",
        priority: "HIGH",
        assigned_counsellor_id: "Dr. Anita Desai",
        remarks: "",
      });
    },
  });

  const updateLeadMutation = useMutation({
    mutationFn: async ({ id, payload }: { id: string; payload: Partial<CrmLead> }) => {
      return await crmService.updateLead(id, payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["crm_leads"] });
      queryClient.invalidateQueries({ queryKey: ["crm_dashboard"] });
    },
  });

  const deleteLeadMutation = useMutation({
    mutationFn: async (id: string) => {
      return await crmService.deleteLead(id);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["crm_leads"] });
    },
  });

  const createFollowupMutation = useMutation({
    mutationFn: async (payload: any) => {
      return await crmService.createFollowup(payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["crm_followups"] });
      setIsFollowupModalOpen(false);
      setSelectedLeadForFollowup(null);
    },
  });

  const createCampaignMutation = useMutation({
    mutationFn: async (payload: typeof campaignForm) => {
      return await crmService.createCampaign(payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["crm_campaigns"] });
      setIsCampaignModalOpen(false);
    },
  });

  const deleteCampaignMutation = useMutation({
    mutationFn: async (id: string) => {
      return await crmService.deleteCampaign(id);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["crm_campaigns"] });
    },
  });

  const createFranchiseMutation = useMutation({
    mutationFn: async (payload: typeof franchiseForm) => {
      return await crmService.createFranchiseCenter(payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["crm_franchise_centers"] });
      setIsFranchiseModalOpen(false);
    },
  });

  const deleteFranchiseMutation = useMutation({
    mutationFn: async (id: string) => {
      return await crmService.deleteFranchiseCenter(id);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["crm_franchise_centers"] });
    },
  });

  const getPriorityBadge = (priority: string) => {
    switch (priority) {
      case "URGENT":
        return "bg-rose-100 text-rose-800 border-rose-200";
      case "HIGH":
        return "bg-amber-100 text-amber-800 border-amber-200";
      case "MEDIUM":
        return "bg-blue-100 text-blue-800 border-blue-200";
      default:
        return "bg-slate-100 text-slate-800 border-slate-200";
    }
  };

  const getStageColor = (stage: string) => {
    switch (stage) {
      case "NEW_LEAD":
        return "border-slate-300 bg-slate-50";
      case "CONTACTED":
        return "border-blue-300 bg-blue-50/40";
      case "COUNSELLING":
        return "border-indigo-300 bg-indigo-50/40";
      case "FEE_DISCUSSION":
        return "border-amber-300 bg-amber-50/40";
      case "ADMISSION_CONFIRMED":
        return "border-emerald-300 bg-emerald-50/40";
      default:
        return "border-slate-200 bg-slate-50/30";
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-xl border border-slate-800">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-indigo-400 font-semibold text-xs tracking-wider uppercase">
              <Target className="w-4 h-4" /> Module 17 Enterprise Sales, CRM & Outreach
            </div>
            <h1 className="text-2xl sm:text-3xl font-black text-white">
              CRM, Marketing & Franchise Control Center
            </h1>
            <p className="text-slate-300 text-xs sm:text-sm max-w-2xl leading-relaxed">
              Track student admissions pipeline, counselor follow-ups, paid ad
              campaign attribution (Google/Meta), and regional partner franchise
              revenue for Indore flagship campus.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => {
                refetchLeads();
                refetchFollowups();
                refetchCampaigns();
                refetchFranchise();
              }}
              className="inline-flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-bold transition border border-slate-700"
            >
              <RefreshCw className="w-4 h-4" /> Refresh Pipeline
            </button>
            <button
              onClick={() => setIsLeadModalOpen(true)}
              className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition shadow-sm"
            >
              <Plus className="w-4 h-4" /> Add Admission Lead
            </button>
          </div>
        </div>

        {/* Real-time KPI Counters */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-6">
          <div className="bg-slate-800/80 rounded-2xl p-4 border border-slate-700/60">
            <p className="text-xs text-slate-400 font-medium">Active Pipeline Leads</p>
            <p className="text-2xl font-bold text-white mt-1">
              {dashboardMetrics?.total_new_leads || leads.length}
            </p>
            <span className="text-xs text-indigo-400 font-medium mt-0.5">
              Across 5 Funnel Stages
            </span>
          </div>

          <div className="bg-slate-800/80 rounded-2xl p-4 border border-slate-700/60">
            <p className="text-xs text-slate-400 font-medium">Admissions Confirmed</p>
            <p className="text-2xl font-bold text-emerald-400 mt-1">
              {dashboardMetrics?.admissions_this_month || 1}
            </p>
            <span className="text-xs text-emerald-400 font-medium flex items-center gap-1 mt-0.5">
              <CheckCircle2 className="w-3 h-3" /> Fee Paid & Enrolled
            </span>
          </div>

          <div className="bg-slate-800/80 rounded-2xl p-4 border border-slate-700/60">
            <p className="text-xs text-slate-400 font-medium">Conversion Rate</p>
            <p className="text-2xl font-bold text-white mt-1">
              {dashboardMetrics?.conversion_rate_percentage || 34.2}%
            </p>
            <span className="text-xs text-amber-400 font-medium mt-0.5">
              Top: {dashboardMetrics?.top_counsellor || "Dr. Anita Desai"}
            </span>
          </div>

          <div className="bg-slate-800/80 rounded-2xl p-4 border border-slate-700/60">
            <p className="text-xs text-slate-400 font-medium">Forecasted Pipeline Revenue</p>
            <p className="text-2xl font-bold text-white mt-1">
              ₹{(dashboardMetrics?.revenue_forecast || 8200000).toLocaleString("en-IN")}
            </p>
            <span className="text-xs text-blue-400 font-medium mt-0.5">
              3 Active Regional Centers
            </span>
          </div>
        </div>
      </div>

      {/* Subtabs Navigation */}
      <div className="flex border-b border-slate-200 space-x-1 sm:space-x-4 overflow-x-auto no-scrollbar">
        <button
          onClick={() => setActiveTab("kanban")}
          className={`pb-3 px-3 text-sm font-bold border-b-2 transition flex items-center gap-2 whitespace-nowrap ${
            activeTab === "kanban"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-slate-600 hover:text-slate-900"
          }`}
        >
          <Target className="w-4 h-4" /> Lead Pipeline Stages ({leads.length})
        </button>
        <button
          onClick={() => setActiveTab("followups")}
          className={`pb-3 px-3 text-sm font-bold border-b-2 transition flex items-center gap-2 whitespace-nowrap ${
            activeTab === "followups"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-slate-600 hover:text-slate-900"
          }`}
        >
          <Phone className="w-4 h-4" /> Counsellor Outreach ({followups.length})
        </button>
        <button
          onClick={() => setActiveTab("campaigns")}
          className={`pb-3 px-3 text-sm font-bold border-b-2 transition flex items-center gap-2 whitespace-nowrap ${
            activeTab === "campaigns"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-slate-600 hover:text-slate-900"
          }`}
        >
          <Megaphone className="w-4 h-4" /> Marketing Campaigns ({campaigns.length})
        </button>
        <button
          onClick={() => setActiveTab("franchise")}
          className={`pb-3 px-3 text-sm font-bold border-b-2 transition flex items-center gap-2 whitespace-nowrap ${
            activeTab === "franchise"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-slate-600 hover:text-slate-900"
          }`}
        >
          <Building2 className="w-4 h-4" /> Regional Franchise Centers ({franchiseCenters.length})
        </button>
      </div>

      {/* Tab 1: Lead Pipeline Kanban */}
      {activeTab === "kanban" && (
        <div className="space-y-4">
          {/* Filter Bar */}
          <div className="bg-white p-4 rounded-2xl border border-slate-200/90 shadow-2xs flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="relative w-full sm:w-80">
              <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
              <input
                type="text"
                placeholder="Search lead name, mobile, code..."
                value={searchLead}
                onChange={(e) => setSearchLead(e.target.value)}
                className="w-full pl-9 pr-4 py-2 border border-slate-300 rounded-xl text-xs outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div className="flex items-center gap-3 w-full sm:w-auto">
              <select
                value={stageFilter}
                onChange={(e) => setStageFilter(e.target.value)}
                className="border border-slate-300 rounded-xl px-3 py-2 text-xs font-semibold bg-white text-slate-700 outline-none"
              >
                <option value="ALL">All Funnel Stages</option>
                <option value="NEW_LEAD">New Inquiries</option>
                <option value="CONTACTED">First Contact</option>
                <option value="COUNSELLING">Academic Counselling</option>
                <option value="FEE_DISCUSSION">Fee Discussion</option>
                <option value="ADMISSION_CONFIRMED">Admission Confirmed</option>
              </select>
            </div>
          </div>

          {/* Kanban / Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {leadsLoading ? (
              <div className="col-span-full py-12 text-center text-slate-400">
                Loading lead pipeline...
              </div>
            ) : leads.length === 0 ? (
              <div className="col-span-full py-12 text-center text-slate-500">
                No admission leads found matching criteria.
              </div>
            ) : (
              leads.map((lead) => (
                <div
                  key={lead.id}
                  className={`rounded-2xl p-5 border shadow-2xs hover:shadow-md transition space-y-3 flex flex-col justify-between ${getStageColor(
                    lead.stage
                  )}`}
                >
                  <div className="space-y-3">
                    <div className="flex items-start justify-between">
                      <div>
                        <div className="flex items-center gap-2">
                          <span
                            className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase border ${getPriorityBadge(
                              lead.priority
                            )}`}
                          >
                            {lead.priority}
                          </span>
                          <span className="font-mono text-[11px] font-semibold text-slate-400">
                            {lead.lead_code}
                          </span>
                        </div>
                        <h3 className="font-bold text-slate-900 text-base mt-1">
                          {lead.full_name}
                        </h3>
                        <p className="text-xs text-indigo-700 font-medium">
                          {lead.course_interested_id}
                        </p>
                      </div>

                      <div className="text-right">
                        <span className="inline-block px-2.5 py-1 rounded-full text-xs font-black bg-indigo-600 text-white shadow-2xs">
                          {lead.score} pts
                        </span>
                      </div>
                    </div>

                    <div className="space-y-1 text-xs text-slate-600">
                      <p className="flex items-center gap-1.5 font-mono">
                        <Phone className="w-3.5 h-3.5 text-slate-400" />
                        <span>{lead.mobile}</span>
                      </p>
                      {lead.email && (
                        <p className="flex items-center gap-1.5 font-mono">
                          <Mail className="w-3.5 h-3.5 text-slate-400" />
                          <span className="truncate">{lead.email}</span>
                        </p>
                      )}
                      {lead.assigned_counsellor_id && (
                        <p className="text-slate-500 text-[11px] pt-1">
                          Counsellor: <strong>{lead.assigned_counsellor_id}</strong>
                        </p>
                      )}
                      {lead.remarks && (
                        <p className="text-slate-500 text-[11px] bg-white/70 p-2 rounded-lg border border-slate-200/60 line-clamp-2">
                          {lead.remarks}
                        </p>
                      )}
                    </div>
                  </div>

                  <div className="pt-3 border-t border-slate-200/80 flex items-center justify-between gap-2">
                    <select
                      value={lead.stage}
                      onChange={(e) =>
                        updateLeadMutation.mutate({
                          id: lead.id,
                          payload: { stage: e.target.value as any },
                        })
                      }
                      className="text-xs font-bold border border-slate-300 rounded-lg px-2 py-1 bg-white text-slate-700 outline-none"
                    >
                      <option value="NEW_LEAD">1. New Inquiry</option>
                      <option value="CONTACTED">2. Contacted</option>
                      <option value="COUNSELLING">3. Counselling</option>
                      <option value="FEE_DISCUSSION">4. Fee Discussion</option>
                      <option value="ADMISSION_CONFIRMED">5. Confirmed</option>
                      <option value="LOST">Dropped</option>
                    </select>

                    <div className="flex items-center gap-1">
                      <button
                        onClick={() => {
                          setSelectedLeadForFollowup(lead);
                          setIsFollowupModalOpen(true);
                        }}
                        className="p-1.5 text-indigo-600 hover:bg-indigo-100 rounded-lg transition"
                        title="Log Outreach Follow-up"
                      >
                        <Phone className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => {
                          if (confirm(`Delete lead record for ${lead.full_name}?`)) {
                            deleteLeadMutation.mutate(lead.id);
                          }
                        }}
                        className="p-1.5 text-slate-400 hover:text-rose-600 rounded-lg transition"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Tab 2: Follow-ups */}
      {activeTab === "followups" && (
        <div className="space-y-4">
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm text-slate-700">
                <thead className="bg-slate-50 border-b border-slate-200 text-xs font-bold text-slate-500 uppercase tracking-wider">
                  <tr>
                    <th className="py-3 px-4">Channel & Lead</th>
                    <th className="py-3 px-4">Counsellor</th>
                    <th className="py-3 px-4">Outreach Notes</th>
                    <th className="py-3 px-4">Outcome</th>
                    <th className="py-3 px-4">Next Scheduled</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 text-xs">
                  {followups.map((f) => (
                    <tr key={f.id} className="hover:bg-slate-50/80 transition">
                      <td className="py-3 px-4">
                        <span className="font-bold text-indigo-700 block">
                          {f.channel}
                        </span>
                        <span className="font-mono text-slate-400">
                          Lead ID: {f.lead_id}
                        </span>
                      </td>
                      <td className="py-3 px-4 font-semibold text-slate-900">
                        {f.counsellor_name}
                      </td>
                      <td className="py-3 px-4 max-w-sm text-slate-600">
                        {f.notes || "Call logged."}
                      </td>
                      <td className="py-3 px-4">
                        <span className="px-2 py-0.5 rounded font-bold uppercase bg-slate-100 text-slate-700 text-[10px]">
                          {f.outcome || "INTERESTED"}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-slate-500 whitespace-nowrap">
                        {f.next_followup_date
                          ? new Date(f.next_followup_date).toLocaleDateString()
                          : "None"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Tab 3: Marketing Campaigns */}
      {activeTab === "campaigns" && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-900">
                Paid Outreach & Marketing Campaigns
              </h2>
              <p className="text-xs text-slate-500">
                Performance tracking, UTM attribution parameters, and admission
                ROI per channel.
              </p>
            </div>
            <button
              onClick={() => setIsCampaignModalOpen(true)}
              className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition shadow-sm"
            >
              <Plus className="w-4 h-4" /> Launch Campaign
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {campaigns.map((cmp) => (
              <div
                key={cmp.id}
                className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-2xs hover:shadow-md transition space-y-4"
              >
                <div className="flex items-start justify-between">
                  <div>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-indigo-50 text-indigo-700">
                      {cmp.channel}
                    </span>
                    <h3 className="font-bold text-slate-900 text-base mt-1.5">
                      {cmp.campaign_name}
                    </h3>
                    <p className="font-mono text-xs text-slate-400">
                      UTM: {cmp.utm_source} / {cmp.utm_campaign}
                    </p>
                  </div>
                  <button
                    onClick={() => {
                      if (confirm(`Remove campaign ${cmp.campaign_name}?`)) {
                        deleteCampaignMutation.mutate(cmp.id);
                      }
                    }}
                    className="text-slate-300 hover:text-rose-600 p-1 transition"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>

                <div className="grid grid-cols-2 gap-2 text-xs bg-slate-50 p-3 rounded-xl border border-slate-100">
                  <div>
                    <span className="text-slate-400 block">Allocated Budget</span>
                    <span className="font-bold text-slate-900">
                      ₹{cmp.allocated_budget.toLocaleString("en-IN")}
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-400 block">Actual Spent</span>
                    <span className="font-bold text-indigo-700">
                      ₹{cmp.actual_spent.toLocaleString("en-IN")}
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-400 block">Leads Generated</span>
                    <span className="font-bold text-slate-900">
                      {cmp.leads_generated} Leads
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-400 block">Confirmed Admissions</span>
                    <span className="font-bold text-emerald-600">
                      {cmp.conversions} Enrolled
                    </span>
                  </div>
                </div>

                <div className="pt-2 flex items-center justify-between text-xs">
                  <span className="font-bold text-emerald-600">
                    Active Channel
                  </span>
                  <span className="text-slate-400 font-mono text-[11px]">
                    Cost/Lead: ₹{cmp.leads_generated ? Math.round(cmp.actual_spent / cmp.leads_generated) : 0}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 4: Regional Franchise Centers */}
      {activeTab === "franchise" && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-900">
                Autonomous Regional Learning & Admission Centers
              </h2>
              <p className="text-xs text-slate-500">
                Branch centers across Madhya Pradesh facilitating off-campus counseling,
                document collection, and fee collection.
              </p>
            </div>
            <button
              onClick={() => setIsFranchiseModalOpen(true)}
              className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition shadow-sm"
            >
              <Plus className="w-4 h-4" /> Onboard Franchise Center
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {franchiseCenters.map((fc) => (
              <div
                key={fc.id}
                className="bg-white rounded-2xl p-5 border border-slate-200/90 shadow-2xs hover:shadow-md transition space-y-4"
              >
                <div className="flex items-start justify-between">
                  <div>
                    <span className="font-mono text-xs font-bold text-indigo-600 block">
                      {fc.center_code}
                    </span>
                    <h3 className="font-bold text-slate-900 text-base mt-0.5">
                      {fc.center_name}
                    </h3>
                    <p className="text-xs text-slate-500">
                      {fc.city}, {fc.state}
                    </p>
                  </div>
                  <button
                    onClick={() => {
                      if (confirm(`Remove franchise center ${fc.center_name}?`)) {
                        deleteFranchiseMutation.mutate(fc.id);
                      }
                    }}
                    className="text-slate-300 hover:text-rose-600 p-1 transition"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>

                <div className="space-y-1.5 text-xs text-slate-600 bg-slate-50 p-3 rounded-xl border border-slate-100">
                  <p className="flex items-center gap-1.5">
                    <Mail className="w-3.5 h-3.5 text-slate-400" />
                    <span>{fc.contact_email}</span>
                  </p>
                  <p className="flex items-center gap-1.5">
                    <Phone className="w-3.5 h-3.5 text-slate-400" />
                    <span>{fc.contact_phone}</span>
                  </p>
                </div>

                <div className="grid grid-cols-2 gap-2 text-xs pt-1">
                  <div>
                    <span className="text-slate-400 block text-[11px]">Enrolled Students</span>
                    <span className="font-bold text-slate-900 text-sm">
                      {fc.active_students}
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[11px]">Royalty Rate</span>
                    <span className="font-bold text-emerald-600 text-sm">
                      {fc.royalty_percentage}%
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Add Lead Modal */}
      {isLeadModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl border border-slate-100 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="font-bold text-slate-900 text-lg">
                Add Admission Lead
              </h3>
              <button
                onClick={() => setIsLeadModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Full Name *
                </label>
                <input
                  type="text"
                  placeholder="Student name"
                  value={leadForm.full_name}
                  onChange={(e) =>
                    setLeadForm({ ...leadForm, full_name: e.target.value })
                  }
                  className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Mobile Number *
                  </label>
                  <input
                    type="text"
                    placeholder="+91 98765 00000"
                    value={leadForm.mobile}
                    onChange={(e) =>
                      setLeadForm({ ...leadForm, mobile: e.target.value })
                    }
                    className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Email Address
                  </label>
                  <input
                    type="email"
                    placeholder="student@example.com"
                    value={leadForm.email}
                    onChange={(e) =>
                      setLeadForm({ ...leadForm, email: e.target.value })
                    }
                    className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Course Interested *
                </label>
                <input
                  type="text"
                  value={leadForm.course_interested_id}
                  onChange={(e) =>
                    setLeadForm({
                      ...leadForm,
                      course_interested_id: e.target.value,
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Priority
                  </label>
                  <select
                    value={leadForm.priority}
                    onChange={(e) =>
                      setLeadForm({
                        ...leadForm,
                        priority: e.target.value as any,
                      })
                    }
                    className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                  >
                    <option value="LOW">LOW</option>
                    <option value="MEDIUM">MEDIUM</option>
                    <option value="HIGH">HIGH</option>
                    <option value="URGENT">URGENT</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Assigned Counsellor
                  </label>
                  <input
                    type="text"
                    value={leadForm.assigned_counsellor_id}
                    onChange={(e) =>
                      setLeadForm({
                        ...leadForm,
                        assigned_counsellor_id: e.target.value,
                      })
                    }
                    className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Counseling Notes / Remarks
                </label>
                <textarea
                  rows={2}
                  placeholder="Exam ranks, scholarship eligibility, preferences..."
                  value={leadForm.remarks}
                  onChange={(e) =>
                    setLeadForm({ ...leadForm, remarks: e.target.value })
                  }
                  className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                />
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-3">
              <button
                onClick={() => setIsLeadModalOpen(false)}
                className="px-4 py-2 border border-slate-300 text-slate-700 rounded-xl text-xs font-bold hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  if (!leadForm.full_name || !leadForm.mobile) {
                    alert("Please provide full name and mobile");
                    return;
                  }
                  createLeadMutation.mutate(leadForm);
                }}
                disabled={createLeadMutation.isPending}
                className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition"
              >
                Save Lead Record
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Schedule Followup Modal */}
      {isFollowupModalOpen && selectedLeadForFollowup && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl border border-slate-100 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="font-bold text-slate-900 text-lg">
                Log Outreach Call / Follow-up
              </h3>
              <button
                onClick={() => setIsFollowupModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-3 bg-slate-50 rounded-xl text-xs space-y-1">
              <p className="font-bold text-slate-900">
                Lead: {selectedLeadForFollowup.full_name} ({selectedLeadForFollowup.mobile})
              </p>
              <p className="text-slate-500">
                Course: {selectedLeadForFollowup.course_interested_id}
              </p>
            </div>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Channel *
                </label>
                <select
                  value={followupForm.channel}
                  onChange={(e) =>
                    setFollowupForm({
                      ...followupForm,
                      channel: e.target.value as any,
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                >
                  <option value="CALL">Phone Call</option>
                  <option value="WHATSAPP">WhatsApp</option>
                  <option value="MEETING">Campus Visit / Face-to-Face</option>
                  <option value="EMAIL">Email</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Conversation Summary *
                </label>
                <textarea
                  rows={3}
                  placeholder="Key discussion points, parent feedback, next steps..."
                  value={followupForm.notes}
                  onChange={(e) =>
                    setFollowupForm({ ...followupForm, notes: e.target.value })
                  }
                  className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Outcome *
                </label>
                <select
                  value={followupForm.outcome}
                  onChange={(e) =>
                    setFollowupForm({ ...followupForm, outcome: e.target.value })
                  }
                  className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                >
                  <option value="INTERESTED">Interested - Follow up next week</option>
                  <option value="ADMISSION_PROMISED">Admission Promised - Fee discussion</option>
                  <option value="CALLBACK_REQUESTED">Busy - Callback requested</option>
                  <option value="NOT_INTERESTED">Not Interested</option>
                </select>
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-3">
              <button
                onClick={() => setIsFollowupModalOpen(false)}
                className="px-4 py-2 border border-slate-300 text-slate-700 rounded-xl text-xs font-bold hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  createFollowupMutation.mutate({
                    lead_id: selectedLeadForFollowup.id,
                    ...followupForm,
                  });
                }}
                disabled={createFollowupMutation.isPending}
                className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition"
              >
                Save Follow-up
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Launch Campaign Modal */}
      {isCampaignModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl border border-slate-100 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="font-bold text-slate-900 text-lg">
                Launch Marketing Campaign
              </h3>
              <button
                onClick={() => setIsCampaignModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Campaign Title *
                </label>
                <input
                  type="text"
                  placeholder="e.g. B.Tech Admissions 2026 Meta Ads"
                  value={campaignForm.campaign_name}
                  onChange={(e) =>
                    setCampaignForm({
                      ...campaignForm,
                      campaign_name: e.target.value,
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Channel *
                  </label>
                  <select
                    value={campaignForm.channel}
                    onChange={(e) =>
                      setCampaignForm({
                        ...campaignForm,
                        channel: e.target.value,
                      })
                    }
                    className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                  >
                    <option value="GOOGLE_ADS">Google Ads</option>
                    <option value="META_ADS">Meta (Insta / FB)</option>
                    <option value="WHATSAPP">WhatsApp Drip</option>
                    <option value="OFFLINE_EVENTS">Education Expo</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Allocated Budget (₹)
                  </label>
                  <input
                    type="number"
                    value={campaignForm.allocated_budget}
                    onChange={(e) =>
                      setCampaignForm({
                        ...campaignForm,
                        allocated_budget: parseFloat(e.target.value) || 0,
                      })
                    }
                    className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    UTM Source
                  </label>
                  <input
                    type="text"
                    value={campaignForm.utm_source}
                    onChange={(e) =>
                      setCampaignForm({
                        ...campaignForm,
                        utm_source: e.target.value,
                      })
                    }
                    className="w-full border border-slate-300 rounded-xl p-2.5 text-xs font-mono outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    UTM Campaign
                  </label>
                  <input
                    type="text"
                    value={campaignForm.utm_campaign}
                    onChange={(e) =>
                      setCampaignForm({
                        ...campaignForm,
                        utm_campaign: e.target.value,
                      })
                    }
                    className="w-full border border-slate-300 rounded-xl p-2.5 text-xs font-mono outline-none"
                  />
                </div>
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-3">
              <button
                onClick={() => setIsCampaignModalOpen(false)}
                className="px-4 py-2 border border-slate-300 text-slate-700 rounded-xl text-xs font-bold hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  if (!campaignForm.campaign_name) {
                    alert("Please provide campaign name");
                    return;
                  }
                  createCampaignMutation.mutate(campaignForm);
                }}
                disabled={createCampaignMutation.isPending}
                className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition"
              >
                Launch Campaign
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Onboard Franchise Center Modal */}
      {isFranchiseModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl border border-slate-100 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="font-bold text-slate-900 text-lg">
                Onboard Regional Franchise Center
              </h3>
              <button
                onClick={() => setIsFranchiseModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Center Name *
                </label>
                <input
                  type="text"
                  placeholder="e.g. Ujjain Mahakal Regional Counseling Center"
                  value={franchiseForm.center_name}
                  onChange={(e) =>
                    setFranchiseForm({
                      ...franchiseForm,
                      center_name: e.target.value,
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Center Code *
                  </label>
                  <input
                    type="text"
                    placeholder="e.g. FC-UJJ-04"
                    value={franchiseForm.center_code}
                    onChange={(e) =>
                      setFranchiseForm({
                        ...franchiseForm,
                        center_code: e.target.value,
                      })
                    }
                    className="w-full border border-slate-300 rounded-xl p-2.5 text-xs font-mono outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    City *
                  </label>
                  <input
                    type="text"
                    value={franchiseForm.city}
                    onChange={(e) =>
                      setFranchiseForm({
                        ...franchiseForm,
                        city: e.target.value,
                      })
                    }
                    className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Email Address *
                  </label>
                  <input
                    type="email"
                    placeholder="center@mei-centers.in"
                    value={franchiseForm.contact_email}
                    onChange={(e) =>
                      setFranchiseForm({
                        ...franchiseForm,
                        contact_email: e.target.value,
                      })
                    }
                    className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Phone *
                  </label>
                  <input
                    type="text"
                    placeholder="+91 734 200 0000"
                    value={franchiseForm.contact_phone}
                    onChange={(e) =>
                      setFranchiseForm({
                        ...franchiseForm,
                        contact_phone: e.target.value,
                      })
                    }
                    className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Royalty Percentage (%) *
                </label>
                <input
                  type="number"
                  value={franchiseForm.royalty_percentage}
                  onChange={(e) =>
                    setFranchiseForm({
                      ...franchiseForm,
                      royalty_percentage: parseFloat(e.target.value) || 15.0,
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl p-2.5 text-xs outline-none"
                />
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-3">
              <button
                onClick={() => setIsFranchiseModalOpen(false)}
                className="px-4 py-2 border border-slate-300 text-slate-700 rounded-xl text-xs font-bold hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  if (
                    !franchiseForm.center_name ||
                    !franchiseForm.center_code ||
                    !franchiseForm.contact_email
                  ) {
                    alert("Please fill in required center fields");
                    return;
                  }
                  createFranchiseMutation.mutate(franchiseForm);
                }}
                disabled={createFranchiseMutation.isPending}
                className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition"
              >
                Onboard Center
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
