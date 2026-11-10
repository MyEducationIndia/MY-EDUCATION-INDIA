import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Mail,
  Phone,
  Building2,
  HelpCircle,
  MessageSquare,
  Search,
  Filter,
  CheckCircle2,
  Clock,
  AlertCircle,
  Plus,
  Trash2,
  Edit2,
  Eye,
  Send,
  MapPin,
  Sparkles,
  RefreshCw,
  ChevronDown,
  ChevronUp,
  X,
  ThumbsUp,
  MessageCircle,
} from "lucide-react";
import { websiteService } from "@/services/websiteService";
import {
  CmsContactInquiry,
  CmsDepartmentContact,
  CmsFaqItem,
  CmsSupportFeedback,
} from "@/types/website.types";

export const ContactInquiriesManagementPanel: React.FC = () => {
  const queryClient = useQueryClient();
  const [subTab, setSubTab] = useState<
    "inquiries" | "departments" | "faqs" | "feedback"
  >("inquiries");

  // Filter state for inquiries
  const [inquirySearch, setInquirySearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<string>("ALL");
  const [categoryFilter, setCategoryFilter] = useState<string>("ALL");

  // Selection & modal states
  const [selectedInquiry, setSelectedInquiry] =
    useState<CmsContactInquiry | null>(null);
  const [adminNotes, setAdminNotes] = useState("");
  const [newStatus, setNewStatus] = useState("NEW");

  // Department modal state
  const [isDeptModalOpen, setIsDeptModalOpen] = useState(false);
  const [deptForm, setDeptForm] = useState({
    department_name: "",
    contact_person: "",
    email: "",
    phone_numbers: "",
    office_location: "",
    operating_hours: "Monday - Friday: 9:00 AM - 5:30 PM",
    display_order: 1,
    is_active: true,
  });

  // FAQ modal state
  const [isFaqModalOpen, setIsFaqModalOpen] = useState(false);
  const [faqForm, setFaqForm] = useState({
    category: "ADMISSIONS",
    question: "",
    answer: "",
    display_order: 1,
    is_featured: true,
    is_active: true,
  });

  // Queries
  const {
    data: inquiries = [],
    isLoading: inquiriesLoading,
    refetch: refetchInquiries,
  } = useQuery<CmsContactInquiry[]>({
    queryKey: ["admin_contact_inquiries"],
    queryFn: async () => {
      return await websiteService.getAdminContactInquiries();
    },
  });

  const {
    data: departments = [],
    isLoading: departmentsLoading,
    refetch: refetchDepartments,
  } = useQuery<CmsDepartmentContact[]>({
    queryKey: ["admin_department_contacts"],
    queryFn: async () => {
      return await websiteService.getAdminDepartmentContacts();
    },
  });

  const {
    data: faqs = [],
    isLoading: faqsLoading,
    refetch: refetchFaqs,
  } = useQuery<CmsFaqItem[]>({
    queryKey: ["admin_faqs"],
    queryFn: async () => {
      return await websiteService.getAdminFaqs();
    },
  });

  const {
    data: feedbackList = [],
    isLoading: feedbackLoading,
    refetch: refetchFeedback,
  } = useQuery<CmsSupportFeedback[]>({
    queryKey: ["admin_support_feedback"],
    queryFn: async () => {
      return await websiteService.getAdminSupportFeedback();
    },
  });

  // Mutations
  const updateInquiryMutation = useMutation({
    mutationFn: async ({
      id,
      status,
      notes,
    }: {
      id: string;
      status: string;
      notes?: string;
    }) => {
      return await websiteService.updateContactInquiryStatus(id, status, notes);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin_contact_inquiries"] });
      setSelectedInquiry(null);
    },
  });

  const createDepartmentMutation = useMutation({
    mutationFn: async (payload: typeof deptForm) => {
      return await websiteService.createDepartmentContact(payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["admin_department_contacts"],
      });
      setIsDeptModalOpen(false);
      setDeptForm({
        department_name: "",
        contact_person: "",
        email: "",
        phone_numbers: "",
        office_location: "",
        operating_hours: "Monday - Friday: 9:00 AM - 5:30 PM",
        display_order: 1,
        is_active: true,
      });
    },
  });

  const deleteDepartmentMutation = useMutation({
    mutationFn: async (id: string) => {
      return await websiteService.deleteDepartmentContact(id);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["admin_department_contacts"],
      });
    },
  });

  const createFaqMutation = useMutation({
    mutationFn: async (payload: typeof faqForm) => {
      return await websiteService.createFaq(payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin_faqs"] });
      setIsFaqModalOpen(false);
      setFaqForm({
        category: "ADMISSIONS",
        question: "",
        answer: "",
        display_order: 1,
        is_featured: true,
        is_active: true,
      });
    },
  });

  const deleteFaqMutation = useMutation({
    mutationFn: async (id: string) => {
      return await websiteService.deleteFaq(id);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin_faqs"] });
    },
  });

  const updateFeedbackMutation = useMutation({
    mutationFn: async ({
      id,
      status,
      notes,
    }: {
      id: string;
      status: string;
      notes?: string;
    }) => {
      return await websiteService.updateSupportFeedbackStatus(
        id,
        status,
        notes
      );
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin_support_feedback"] });
    },
  });

  // Filter inquiries
  const filteredInquiries = inquiries.filter((inq) => {
    const matchesSearch =
      inq.full_name.toLowerCase().includes(inquirySearch.toLowerCase()) ||
      inq.email.toLowerCase().includes(inquirySearch.toLowerCase()) ||
      inq.subject.toLowerCase().includes(inquirySearch.toLowerCase()) ||
      inq.message.toLowerCase().includes(inquirySearch.toLowerCase());
    const matchesStatus =
      statusFilter === "ALL" || inq.status === statusFilter;
    const matchesCategory =
      categoryFilter === "ALL" || inq.category === categoryFilter;
    return matchesSearch && matchesStatus && matchesCategory;
  });

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "NEW":
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 border border-amber-200">
            <Clock className="w-3 h-3" /> New
          </span>
        );
      case "IN_PROGRESS":
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-100 text-blue-800 border border-blue-200">
            <RefreshCw className="w-3 h-3 animate-spin" /> In Progress
          </span>
        );
      case "RESPONDED":
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200">
            <CheckCircle2 className="w-3 h-3" /> Responded
          </span>
        );
      case "CLOSED":
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-200">
            Closed
          </span>
        );
      default:
        return (
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-800">
            {status}
          </span>
        );
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-2xl p-6 sm:p-8 shadow-xl border border-slate-800">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-indigo-400 font-semibold text-xs tracking-wider uppercase mb-1">
              <Mail className="w-4 h-4" /> Module 14 Enterprise Governance
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
              Contact & Inquiries Control Center
            </h1>
            <p className="text-slate-300 text-sm mt-1 max-w-2xl">
              Triage public inquiries, coordinate campus departmental
              directories, curate institutional FAQs, and manage student and
              visitor feedback.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={() => {
                refetchInquiries();
                refetchDepartments();
                refetchFaqs();
                refetchFeedback();
              }}
              className="inline-flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-sm font-semibold transition border border-slate-700"
            >
              <RefreshCw className="w-4 h-4" /> Refresh Data
            </button>
          </div>
        </div>

        {/* Metric Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-6">
          <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-700/60">
            <p className="text-xs text-slate-400 font-medium">Total Inquiries</p>
            <p className="text-2xl font-bold text-white mt-1">
              {inquiries.length}
            </p>
            <span className="text-xs text-amber-400 font-medium">
              {inquiries.filter((i) => i.status === "NEW").length} Awaiting Response
            </span>
          </div>
          <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-700/60">
            <p className="text-xs text-slate-400 font-medium">Active Departments</p>
            <p className="text-2xl font-bold text-white mt-1">
              {departments.length}
            </p>
            <span className="text-xs text-emerald-400 font-medium">
              {departments.filter((d) => d.is_active).length} Listed Publicly
            </span>
          </div>
          <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-700/60">
            <p className="text-xs text-slate-400 font-medium">Published FAQs</p>
            <p className="text-2xl font-bold text-white mt-1">{faqs.length}</p>
            <span className="text-xs text-indigo-400 font-medium">
              {faqs.filter((f) => f.is_featured).length} Featured
            </span>
          </div>
          <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-700/60">
            <p className="text-xs text-slate-400 font-medium">Feedback Logged</p>
            <p className="text-2xl font-bold text-white mt-1">
              {feedbackList.length}
            </p>
            <span className="text-xs text-blue-400 font-medium">
              Grievance Redressal
            </span>
          </div>
        </div>
      </div>

      {/* Sub Tabs */}
      <div className="flex border-b border-slate-200 space-x-1 sm:space-x-4">
        <button
          onClick={() => setSubTab("inquiries")}
          className={`pb-3 px-3 text-sm font-bold border-b-2 transition flex items-center gap-2 ${
            subTab === "inquiries"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-slate-600 hover:text-slate-900"
          }`}
        >
          <Mail className="w-4 h-4" /> Inquiries Triage Queue (
          {inquiries.length})
        </button>
        <button
          onClick={() => setSubTab("departments")}
          className={`pb-3 px-3 text-sm font-bold border-b-2 transition flex items-center gap-2 ${
            subTab === "departments"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-slate-600 hover:text-slate-900"
          }`}
        >
          <Building2 className="w-4 h-4" /> Department Directory (
          {departments.length})
        </button>
        <button
          onClick={() => setSubTab("faqs")}
          className={`pb-3 px-3 text-sm font-bold border-b-2 transition flex items-center gap-2 ${
            subTab === "faqs"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-slate-600 hover:text-slate-900"
          }`}
        >
          <HelpCircle className="w-4 h-4" /> Institutional FAQs ({faqs.length})
        </button>
        <button
          onClick={() => setSubTab("feedback")}
          className={`pb-3 px-3 text-sm font-bold border-b-2 transition flex items-center gap-2 ${
            subTab === "feedback"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-slate-600 hover:text-slate-900"
          }`}
        >
          <MessageCircle className="w-4 h-4" /> Student & Visitor Feedback (
          {feedbackList.length})
        </button>
      </div>

      {/* Tab 1: Inquiries Triage Queue */}
      {subTab === "inquiries" && (
        <div className="space-y-4">
          {/* Filters Bar */}
          <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="relative w-full sm:w-72">
              <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
              <input
                type="text"
                placeholder="Search name, email, subject..."
                value={inquirySearch}
                onChange={(e) => setInquirySearch(e.target.value)}
                className="w-full pl-9 pr-4 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
              />
            </div>
            <div className="flex items-center gap-3 w-full sm:w-auto">
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="border border-slate-300 rounded-lg px-3 py-2 text-sm text-slate-700 bg-white focus:ring-2 focus:ring-indigo-500 outline-none"
              >
                <option value="ALL">All Statuses</option>
                <option value="NEW">New</option>
                <option value="IN_PROGRESS">In Progress</option>
                <option value="RESPONDED">Responded</option>
                <option value="CLOSED">Closed</option>
              </select>
              <select
                value={categoryFilter}
                onChange={(e) => setCategoryFilter(e.target.value)}
                className="border border-slate-300 rounded-lg px-3 py-2 text-sm text-slate-700 bg-white focus:ring-2 focus:ring-indigo-500 outline-none"
              >
                <option value="ALL">All Categories</option>
                <option value="ADMISSIONS">Admissions</option>
                <option value="ACADEMIC">Academics</option>
                <option value="EXAMINATIONS">Examinations</option>
                <option value="ACCOUNTS_FEES">Accounts & Fees</option>
                <option value="PLACEMENTS">Placements</option>
                <option value="GENERAL">General</option>
              </select>
            </div>
          </div>

          {/* Inquiries Table */}
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm text-slate-700">
                <thead className="bg-slate-50 border-b border-slate-200 text-xs font-bold text-slate-500 uppercase tracking-wider">
                  <tr>
                    <th className="py-3 px-4">Contact Person</th>
                    <th className="py-3 px-4">Category & Subject</th>
                    <th className="py-3 px-4">Date</th>
                    <th className="py-3 px-4">Status</th>
                    <th className="py-3 px-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {inquiriesLoading ? (
                    <tr>
                      <td colSpan={5} className="py-8 text-center text-slate-400">
                        Loading inquiries...
                      </td>
                    </tr>
                  ) : filteredInquiries.length === 0 ? (
                    <tr>
                      <td colSpan={5} className="py-8 text-center text-slate-500">
                        No inquiries found matching your filters.
                      </td>
                    </tr>
                  ) : (
                    filteredInquiries.map((inq) => (
                      <tr key={inq.id} className="hover:bg-slate-50/80 transition">
                        <td className="py-3 px-4">
                          <p className="font-semibold text-slate-900">
                            {inq.full_name}
                          </p>
                          <p className="text-xs text-slate-500 flex items-center gap-1">
                            <Mail className="w-3 h-3" /> {inq.email}
                          </p>
                          {inq.phone && (
                            <p className="text-xs text-slate-500 flex items-center gap-1">
                              <Phone className="w-3 h-3" /> {inq.phone}
                            </p>
                          )}
                        </td>
                        <td className="py-3 px-4 max-w-xs">
                          <span className="inline-block px-2 py-0.5 rounded text-[10px] font-bold tracking-wider uppercase bg-indigo-50 text-indigo-700 mb-1">
                            {inq.category}
                          </span>
                          <p className="font-medium text-slate-800 truncate">
                            {inq.subject}
                          </p>
                          <p className="text-xs text-slate-500 line-clamp-1">
                            {inq.message}
                          </p>
                        </td>
                        <td className="py-3 px-4 text-xs text-slate-500 whitespace-nowrap">
                          {new Date(inq.created_at).toLocaleDateString("en-IN", {
                            day: "numeric",
                            month: "short",
                            year: "numeric",
                          })}
                        </td>
                        <td className="py-3 px-4 whitespace-nowrap">
                          {getStatusBadge(inq.status)}
                        </td>
                        <td className="py-3 px-4 text-right whitespace-nowrap">
                          <button
                            onClick={() => {
                              setSelectedInquiry(inq);
                              setNewStatus(inq.status);
                              setAdminNotes(inq.admin_notes || "");
                            }}
                            className="inline-flex items-center gap-1 px-3 py-1.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 rounded-lg text-xs font-semibold transition"
                          >
                            <Eye className="w-3.5 h-3.5" /> Triage
                          </button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Department Directory */}
      {subTab === "departments" && (
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-lg font-bold text-slate-900">
                Campus Departmental Contacts
              </h2>
              <p className="text-xs text-slate-500">
                Maintain official campus department hotlines, office extensions,
                and operating hours.
              </p>
            </div>
            <button
              onClick={() => setIsDeptModalOpen(true)}
              className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-semibold transition shadow-sm"
            >
              <Plus className="w-4 h-4" /> Add Department
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {departmentsLoading ? (
              <div className="col-span-full py-8 text-center text-slate-400">
                Loading departments...
              </div>
            ) : departments.length === 0 ? (
              <div className="col-span-full py-8 text-center text-slate-500">
                No departmental contacts configured.
              </div>
            ) : (
              departments.map((dept) => (
                <div
                  key={dept.id}
                  className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm relative group hover:shadow-md transition"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="font-bold text-slate-900">
                        {dept.department_name}
                      </h3>
                      {dept.contact_person && (
                        <p className="text-xs text-indigo-600 font-medium">
                          Lead: {dept.contact_person}
                        </p>
                      )}
                    </div>
                    <button
                      onClick={() => {
                        if (
                          confirm(
                            `Delete ${dept.department_name} from public directory?`
                          )
                        ) {
                          deleteDepartmentMutation.mutate(dept.id);
                        }
                      }}
                      className="text-slate-400 hover:text-rose-600 p-1 rounded-lg transition"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>

                  <div className="mt-4 space-y-2 text-xs text-slate-600">
                    <div className="flex items-center gap-2">
                      <Mail className="w-3.5 h-3.5 text-slate-400" />
                      <span className="font-mono">{dept.email}</span>
                    </div>
                    {dept.phone_numbers && (
                      <div className="flex items-center gap-2">
                        <Phone className="w-3.5 h-3.5 text-slate-400" />
                        <span>{dept.phone_numbers}</span>
                      </div>
                    )}
                    {dept.office_location && (
                      <div className="flex items-center gap-2">
                        <MapPin className="w-3.5 h-3.5 text-slate-400" />
                        <span>{dept.office_location}</span>
                      </div>
                    )}
                    {dept.operating_hours && (
                      <div className="flex items-center gap-2">
                        <Clock className="w-3.5 h-3.5 text-slate-400" />
                        <span>{dept.operating_hours}</span>
                      </div>
                    )}
                  </div>

                  <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                    <span
                      className={`inline-flex items-center gap-1 font-semibold ${
                        dept.is_active ? "text-emerald-600" : "text-slate-400"
                      }`}
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      {dept.is_active ? "Public Active" : "Hidden"}
                    </span>
                    <span className="text-slate-400">Order: {dept.display_order}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Tab 3: Institutional FAQs */}
      {subTab === "faqs" && (
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-lg font-bold text-slate-900">
                Institutional FAQs Builder
              </h2>
              <p className="text-xs text-slate-500">
                Curate verified institutional answers across Admissions,
                Academics, Placements, and Campus Life.
              </p>
            </div>
            <button
              onClick={() => setIsFaqModalOpen(true)}
              className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-semibold transition shadow-sm"
            >
              <Plus className="w-4 h-4" /> Add FAQ Item
            </button>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-slate-200 divide-y divide-slate-100">
            {faqsLoading ? (
              <div className="py-8 text-center text-slate-400">
                Loading FAQs...
              </div>
            ) : faqs.length === 0 ? (
              <div className="py-8 text-center text-slate-500">
                No FAQs curated yet.
              </div>
            ) : (
              faqs.map((faq) => (
                <div key={faq.id} className="p-5 hover:bg-slate-50/60 transition">
                  <div className="flex items-start justify-between gap-4">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-slate-100 text-slate-700">
                          {faq.category}
                        </span>
                        {faq.is_featured && (
                          <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-amber-100 text-amber-800">
                            Featured
                          </span>
                        )}
                      </div>
                      <h3 className="font-bold text-slate-900 text-base">
                        {faq.question}
                      </h3>
                      <p className="text-sm text-slate-600 leading-relaxed pt-1">
                        {faq.answer}
                      </p>
                    </div>
                    <button
                      onClick={() => {
                        if (confirm("Delete this FAQ item?")) {
                          deleteFaqMutation.mutate(faq.id);
                        }
                      }}
                      className="text-slate-400 hover:text-rose-600 p-1 rounded-lg transition shrink-0"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Tab 4: Student & Visitor Feedback */}
      {subTab === "feedback" && (
        <div className="space-y-4">
          <div>
            <h2 className="text-lg font-bold text-slate-900">
              Visitor Feedback & Grievance Submissions
            </h2>
            <p className="text-xs text-slate-500">
              Direct stakeholder feedback and grievance escalation log for quality
              assurance.
            </p>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm text-slate-700">
                <thead className="bg-slate-50 border-b border-slate-200 text-xs font-bold text-slate-500 uppercase tracking-wider">
                  <tr>
                    <th className="py-3 px-4">Stakeholder</th>
                    <th className="py-3 px-4">Type & Rating</th>
                    <th className="py-3 px-4">Description</th>
                    <th className="py-3 px-4">Status</th>
                    <th className="py-3 px-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {feedbackLoading ? (
                    <tr>
                      <td colSpan={5} className="py-8 text-center text-slate-400">
                        Loading feedback...
                      </td>
                    </tr>
                  ) : feedbackList.length === 0 ? (
                    <tr>
                      <td colSpan={5} className="py-8 text-center text-slate-500">
                        No feedback logs received yet.
                      </td>
                    </tr>
                  ) : (
                    feedbackList.map((fb) => (
                      <tr key={fb.id} className="hover:bg-slate-50/80 transition">
                        <td className="py-3 px-4">
                          <p className="font-semibold text-slate-900">
                            {fb.name || "Anonymous"}
                          </p>
                          <span className="inline-block px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-slate-100 text-slate-600">
                            {fb.user_type}
                          </span>
                          {fb.email && (
                            <p className="text-xs text-slate-500 mt-0.5">
                              {fb.email}
                            </p>
                          )}
                        </td>
                        <td className="py-3 px-4">
                          <span className="font-bold text-indigo-700 text-xs">
                            {fb.feedback_type}
                          </span>
                          {fb.rating_satisfaction && (
                            <div className="text-amber-500 text-xs font-bold mt-0.5">
                              {"★".repeat(fb.rating_satisfaction)}
                              {"☆".repeat(5 - fb.rating_satisfaction)}
                            </div>
                          )}
                        </td>
                        <td className="py-3 px-4 max-w-sm text-xs text-slate-600">
                          {fb.description}
                          {fb.resolution_notes && (
                            <p className="mt-1 text-slate-400 italic">
                              Note: {fb.resolution_notes}
                            </p>
                          )}
                        </td>
                        <td className="py-3 px-4 whitespace-nowrap">
                          <span
                            className={`px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                              fb.status === "RESOLVED"
                                ? "bg-emerald-100 text-emerald-800"
                                : fb.status === "UNDER_REVIEW"
                                ? "bg-blue-100 text-blue-800"
                                : "bg-amber-100 text-amber-800"
                            }`}
                          >
                            {fb.status}
                          </span>
                        </td>
                        <td className="py-3 px-4 text-right whitespace-nowrap">
                          {fb.status !== "RESOLVED" && (
                            <button
                              onClick={() => {
                                const notes = prompt(
                                  "Enter resolution notes (optional):",
                                  fb.resolution_notes || ""
                                );
                                if (notes !== null) {
                                  updateFeedbackMutation.mutate({
                                    id: fb.id,
                                    status: "RESOLVED",
                                    notes: notes || undefined,
                                  });
                                }
                              }}
                              className="px-3 py-1 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 rounded-lg text-xs font-semibold transition"
                            >
                              Resolve
                            </button>
                          )}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Inquiry Detail & Triage Modal */}
      {selectedInquiry && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div className="bg-white rounded-2xl max-w-xl w-full p-6 shadow-2xl border border-slate-100 space-y-5">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div className="flex items-center gap-2">
                <Mail className="w-5 h-5 text-indigo-600" />
                <h3 className="font-bold text-slate-900 text-lg">
                  Inquiry Triage & Response
                </h3>
              </div>
              <button
                onClick={() => setSelectedInquiry(null)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="bg-slate-50 p-4 rounded-xl space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-slate-500 font-medium">From:</span>
                <span className="font-semibold text-slate-900">
                  {selectedInquiry.full_name} ({selectedInquiry.email})
                </span>
              </div>
              {selectedInquiry.phone && (
                <div className="flex justify-between">
                  <span className="text-slate-500 font-medium">Phone:</span>
                  <span className="font-semibold text-slate-900">
                    {selectedInquiry.phone}
                  </span>
                </div>
              )}
              <div className="flex justify-between">
                <span className="text-slate-500 font-medium">Category:</span>
                <span className="font-bold text-indigo-700">
                  {selectedInquiry.category}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500 font-medium">Subject:</span>
                <span className="font-semibold text-slate-900">
                  {selectedInquiry.subject}
                </span>
              </div>
              <div className="pt-2 border-t border-slate-200">
                <p className="text-slate-500 font-medium mb-1">Message Body:</p>
                <p className="text-slate-800 text-sm whitespace-pre-line bg-white p-3 rounded-lg border border-slate-200">
                  {selectedInquiry.message}
                </p>
              </div>
            </div>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                  Status
                </label>
                <select
                  value={newStatus}
                  onChange={(e) => setNewStatus(e.target.value)}
                  className="w-full border border-slate-300 rounded-lg p-2.5 text-sm outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="NEW">NEW</option>
                  <option value="IN_PROGRESS">IN_PROGRESS</option>
                  <option value="RESPONDED">RESPONDED</option>
                  <option value="CLOSED">CLOSED</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                  Admin Notes / Triage Remarks
                </label>
                <textarea
                  rows={3}
                  value={adminNotes}
                  onChange={(e) => setAdminNotes(e.target.value)}
                  placeholder="Internal audit notes, desk routing remarks, or dispatch confirmation..."
                  className="w-full border border-slate-300 rounded-lg p-2.5 text-sm outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-2">
              <button
                onClick={() => setSelectedInquiry(null)}
                className="px-4 py-2 border border-slate-300 text-slate-700 rounded-xl text-sm font-semibold hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  updateInquiryMutation.mutate({
                    id: selectedInquiry.id,
                    status: newStatus,
                    notes: adminNotes || undefined,
                  });
                }}
                disabled={updateInquiryMutation.isPending}
                className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-semibold transition flex items-center gap-2"
              >
                {updateInquiryMutation.isPending ? (
                  <RefreshCw className="w-4 h-4 animate-spin" />
                ) : (
                  <Send className="w-4 h-4" />
                )}
                Save Status
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Add Department Modal */}
      {isDeptModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-100 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="font-bold text-slate-900 text-lg">
                Add Campus Department Contact
              </h3>
              <button
                onClick={() => setIsDeptModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Department Name *
                </label>
                <input
                  type="text"
                  placeholder="e.g. Training & Placement Cell"
                  value={deptForm.department_name}
                  onChange={(e) =>
                    setDeptForm({ ...deptForm, department_name: e.target.value })
                  }
                  className="w-full border border-slate-300 rounded-lg p-2.5 text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Contact Person / Officer *
                </label>
                <input
                  type="text"
                  placeholder="e.g. Dr. Rajesh Sharma (Director)"
                  value={deptForm.contact_person}
                  onChange={(e) =>
                    setDeptForm({ ...deptForm, contact_person: e.target.value })
                  }
                  className="w-full border border-slate-300 rounded-lg p-2.5 text-sm"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Email Address *
                  </label>
                  <input
                    type="email"
                    placeholder="dept@mei-hq.edu.in"
                    value={deptForm.email}
                    onChange={(e) =>
                      setDeptForm({ ...deptForm, email: e.target.value })
                    }
                    className="w-full border border-slate-300 rounded-lg p-2.5 text-sm"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Phone Numbers / Ext
                  </label>
                  <input
                    type="text"
                    placeholder="+91 731 2999000, Ext: 104"
                    value={deptForm.phone_numbers}
                    onChange={(e) =>
                      setDeptForm({ ...deptForm, phone_numbers: e.target.value })
                    }
                    className="w-full border border-slate-300 rounded-lg p-2.5 text-sm"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Office Location
                </label>
                <input
                  type="text"
                  placeholder="Administrative Block, Level 2, Room 204"
                  value={deptForm.office_location}
                  onChange={(e) =>
                    setDeptForm({
                      ...deptForm,
                      office_location: e.target.value,
                    })
                  }
                  className="w-full border border-slate-300 rounded-lg p-2.5 text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Operating Hours
                </label>
                <input
                  type="text"
                  value={deptForm.operating_hours}
                  onChange={(e) =>
                    setDeptForm({
                      ...deptForm,
                      operating_hours: e.target.value,
                    })
                  }
                  className="w-full border border-slate-300 rounded-lg p-2.5 text-sm"
                />
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-3">
              <button
                onClick={() => setIsDeptModalOpen(false)}
                className="px-4 py-2 border border-slate-300 text-slate-700 rounded-xl text-sm font-semibold hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  if (!deptForm.department_name || !deptForm.email) {
                    alert("Please provide department name and email");
                    return;
                  }
                  createDepartmentMutation.mutate(deptForm);
                }}
                disabled={createDepartmentMutation.isPending}
                className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-semibold transition"
              >
                Save Department
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Add FAQ Modal */}
      {isFaqModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-100 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="font-bold text-slate-900 text-lg">
                Add Institutional FAQ
              </h3>
              <button
                onClick={() => setIsFaqModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Category *
                </label>
                <select
                  value={faqForm.category}
                  onChange={(e) =>
                    setFaqForm({ ...faqForm, category: e.target.value })
                  }
                  className="w-full border border-slate-300 rounded-lg p-2.5 text-sm"
                >
                  <option value="ADMISSIONS">ADMISSIONS</option>
                  <option value="ACADEMICS">ACADEMICS</option>
                  <option value="PLACEMENTS">PLACEMENTS</option>
                  <option value="EXAMINATIONS">EXAMINATIONS</option>
                  <option value="CAMPUS_LIFE">CAMPUS_LIFE</option>
                  <option value="GENERAL">GENERAL</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Question *
                </label>
                <input
                  type="text"
                  placeholder="e.g. How can I apply for merit-based scholarships?"
                  value={faqForm.question}
                  onChange={(e) =>
                    setFaqForm({ ...faqForm, question: e.target.value })
                  }
                  className="w-full border border-slate-300 rounded-lg p-2.5 text-sm"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Answer *
                </label>
                <textarea
                  rows={4}
                  placeholder="Detailed institutional answer with policy guidelines..."
                  value={faqForm.answer}
                  onChange={(e) =>
                    setFaqForm({ ...faqForm, answer: e.target.value })
                  }
                  className="w-full border border-slate-300 rounded-lg p-2.5 text-sm"
                />
              </div>

              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="faq_featured"
                  checked={faqForm.is_featured}
                  onChange={(e) =>
                    setFaqForm({ ...faqForm, is_featured: e.target.checked })
                  }
                  className="w-4 h-4 text-indigo-600 rounded"
                />
                <label htmlFor="faq_featured" className="text-xs font-semibold text-slate-700">
                  Feature on Public Contact page highlight reel
                </label>
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-3">
              <button
                onClick={() => setIsFaqModalOpen(false)}
                className="px-4 py-2 border border-slate-300 text-slate-700 rounded-xl text-sm font-semibold hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  if (!faqForm.question || !faqForm.answer) {
                    alert("Please provide both question and answer");
                    return;
                  }
                  createFaqMutation.mutate(faqForm);
                }}
                disabled={createFaqMutation.isPending}
                className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-semibold transition"
              >
                Save FAQ
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
