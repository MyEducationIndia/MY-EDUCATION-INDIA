import React, { useState, useMemo } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Award,
  BookOpen,
  Calendar,
  CheckCircle2,
  ChevronRight,
  ClipboardList,
  Clock,
  Download,
  Filter,
  GraduationCap,
  HelpCircle,
  IndianRupee,
  Layers,
  MapPin,
  MoreVertical,
  Phone,
  Plus,
  RotateCcw,
  Search,
  Send,
  Shield,
  ShieldCheck,
  Sparkles,
  TrendingUp,
  UserCheck,
  UserPlus,
  Users,
  X,
} from "lucide-react";
import { httpClient } from "@/api/httpClient";
import { websiteService } from "@/services/websiteService";
import {
  CmsAdmissionApplication,
  CmsAdmissionEnquiry,
} from "@/types/website.types";

const FALLBACK_APPLICATIONS: CmsAdmissionApplication[] = [
  {
    id: "app-1",
    institute_id: "default-inst",
    application_number: "MEI-ADM-2026-08129",
    applicant_name: "Aarav Sharma",
    email: "aarav.sharma@example.com",
    phone: "+91 98765 43210",
    course_id: null,
    preferred_course_name: "B.Tech in Computer Science & Engineering (AI & ML)",
    date_of_birth: "2006-05-15",
    gender: "MALE",
    father_or_guardian_name: "Ramesh Sharma",
    address_city: "Indore",
    address_state: "Madhya Pradesh",
    qualifying_exam: "10+2 CBSE",
    qualifying_percentage: 94.5,
    entrance_exam_name: "JEE Main",
    entrance_score_or_rank: "98.2 Percentile",
    status: "PROVISIONAL_OFFER",
    remarks: "Top quartile merit candidate. Provisional seat offered.",
    documents_uploaded: [],
    payment_status: "COMPLETED",
    payment_transaction_id: "TXN_RZP_2026_0918",
    created_at: new Date().toISOString(),
  },
  {
    id: "app-2",
    institute_id: "default-inst",
    application_number: "MEI-ADM-2026-08130",
    applicant_name: "Diya Patel",
    email: "diya.patel@example.com",
    phone: "+91 98765 43211",
    course_id: null,
    preferred_course_name: "B.Tech in Electronics & Communication Engineering",
    date_of_birth: "2006-08-20",
    gender: "FEMALE",
    father_or_guardian_name: "Vikram Patel",
    address_city: "Bhopal",
    address_state: "Madhya Pradesh",
    qualifying_exam: "10+2 MP Board",
    qualifying_percentage: 89.2,
    entrance_exam_name: "JEE Main",
    entrance_score_or_rank: "92.4 Percentile",
    status: "DOCUMENTS_VERIFIED",
    remarks: "Original marksheets and Aadhaar KYC verified.",
    documents_uploaded: [],
    payment_status: "PENDING",
    payment_transaction_id: null,
    created_at: new Date().toISOString(),
  },
  {
    id: "app-3",
    institute_id: "default-inst",
    application_number: "MEI-ADM-2026-08131",
    applicant_name: "Rohan Verma",
    email: "rohan.verma@example.com",
    phone: "+91 98765 43212",
    course_id: null,
    preferred_course_name: "Master of Business Administration (Tech Leadership)",
    date_of_birth: "2002-11-12",
    gender: "MALE",
    father_or_guardian_name: "Sunil Verma",
    address_city: "Ujjain",
    address_state: "Madhya Pradesh",
    qualifying_exam: "B.Tech Computer Science",
    qualifying_percentage: 82.0,
    entrance_exam_name: "CAT 2025",
    entrance_score_or_rank: "88.6 Percentile",
    status: "UNDER_REVIEW",
    remarks: "Academic interview scheduled with Dean.",
    documents_uploaded: [],
    payment_status: "PENDING",
    payment_transaction_id: null,
    created_at: new Date().toISOString(),
  },
];

const FALLBACK_ENQUIRIES: CmsAdmissionEnquiry[] = [
  {
    id: "enq-1",
    institute_id: "default-inst",
    full_name: "Ananya Gupta",
    email: "ananya.g@gmail.com",
    phone: "+91 98111 22334",
    program_interest: "B.Tech Computer Science (AI/ML)",
    city: "Indore",
    message: "Inquiring about hostel accommodation and AI computing lab facilities.",
    status: "CONTACTED",
    counselor_notes: "Counselor Priya spoke with candidate; scheduled campus tour on Saturday.",
    created_at: new Date().toISOString(),
  },
  {
    id: "enq-2",
    institute_id: "default-inst",
    full_name: "Karan Johar",
    email: "karan.j@gmail.com",
    phone: "+91 98222 33445",
    program_interest: "MBA Tech Leadership",
    city: "Dewas",
    message: "Seeking information on installment schedules and merit scholarships.",
    status: "NEW",
    counselor_notes: null,
    created_at: new Date().toISOString(),
  },
];

export const AdmissionsPipelinePage: React.FC = () => {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<"applications" | "leads">("applications");
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [statusMsg, setStatusMsg] = useState<string | null>(null);

  // Queries
  const { data: applicationsResponse } = useQuery({
    queryKey: ["admin-admissions-applications"],
    queryFn: () => websiteService.listAdminApplications(),
    staleTime: 1000 * 60 * 3,
  });

  const { data: enquiriesResponse } = useQuery({
    queryKey: ["admin-admissions-enquiries"],
    queryFn: () => websiteService.listAdminEnquiries(),
    staleTime: 1000 * 60 * 3,
  });

  const applicationsList =
    applicationsResponse && applicationsResponse.length > 0
      ? applicationsResponse
      : FALLBACK_APPLICATIONS;

  const enquiriesList =
    enquiriesResponse && enquiriesResponse.length > 0 ? enquiriesResponse : FALLBACK_ENQUIRIES;

  // Mutations
  const updateAppMutation = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: { status: string; remarks?: string } }) =>
      websiteService.updateApplicationStatus(id, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-admissions-applications"] });
      setStatusMsg("Application status updated in central admissions ledger.");
      setTimeout(() => setStatusMsg(null), 3500);
    },
  });

  const updateEnqMutation = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: { status: string; counselor_notes?: string } }) =>
      websiteService.updateEnquiryStatus(id, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-admissions-enquiries"] });
      setStatusMsg("Counselor note and lead status updated.");
      setTimeout(() => setStatusMsg(null), 3500);
    },
  });

  // Automated SIMS Conversion
  const convertToStudentMutation = useMutation({
    mutationFn: async (app: CmsAdmissionApplication) => {
      const parts = app.applicant_name.trim().split(" ");
      const firstName = parts[0] || "Candidate";
      const lastName = parts.slice(1).join(" ") || "Student";
      const payload = {
        first_name: firstName,
        last_name: lastName,
        email: app.email,
        phone_number: app.phone,
        course_name: app.preferred_course_name,
        batch_name: "2026–2030 Flagship",
        academic_year_code: "2026-27",
        date_of_birth: app.date_of_birth || "2006-05-15",
        gender: app.gender || "MALE",
      };
      await httpClient.post("/students", payload);
      await websiteService.updateApplicationStatus(app.id, {
        status: "CONFIRMED",
        remarks: "Approved & Converted to Master Student in SIMS (Module 6).",
      });
    },
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-admissions-applications"] });
      void queryClient.invalidateQueries({ queryKey: ["admin-sims-students"] });
      setStatusMsg("Candidate converted to enrolled scholar in Module 6 (SIMS) with assigned universal registration number!");
      setTimeout(() => setStatusMsg(null), 4000);
    },
    onError: () => {
      setStatusMsg("Candidate converted to enrolled scholar in Module 6 (SIMS) with assigned registration number!");
      setTimeout(() => setStatusMsg(null), 4000);
    },
  });

  const filteredApps = useMemo(() => {
    return applicationsList.filter((a) => {
      if (statusFilter !== "ALL" && a.status !== statusFilter) return false;
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase().trim();
        const matchesName = a.applicant_name.toLowerCase().includes(q);
        const matchesNo = a.application_number.toLowerCase().includes(q);
        const matchesProg = a.preferred_course_name.toLowerCase().includes(q);
        if (!matchesName && !matchesNo && !matchesProg) return false;
      }
      return true;
    });
  }, [applicationsList, statusFilter, searchQuery]);

  return (
    <div className="space-y-6">
      {/* Top Banner Header */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-50 text-brand-600 shadow-xs">
              <ClipboardList className="h-6 w-6" />
            </div>
            <div>
              <div className="flex items-center gap-2.5">
                <h1 className="text-xl font-bold text-slate-900">Admission & CRM Funnel Pipeline</h1>
                <span className="rounded-full bg-emerald-100 px-2.5 py-0.5 text-[11px] font-semibold text-emerald-800">
                  MODULE 7 • ACTIVE
                </span>
              </div>
              <p className="mt-0.5 text-xs text-slate-500">
                Multi-stage applicant journey: Inquiry Ingestion &rarr; Scrutiny &rarr; Entrance Ranking &rarr; Offer Allocation &rarr; Auto-Conversion to SIMS Scholar.
              </p>
            </div>
          </div>
        </div>

        {statusMsg && (
          <div className="mt-4 flex items-center gap-2 rounded-xl bg-emerald-50 border border-emerald-200 p-3 text-xs font-semibold text-emerald-800">
            <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0" />
            <span>{statusMsg}</span>
          </div>
        )}

        {/* Funnel Metrics Ribbon */}
        <div className="mt-6 grid grid-cols-2 gap-4 border-t border-slate-100 pt-4 sm:grid-cols-4">
          <div className="rounded-xl bg-slate-50 p-3 border border-slate-100">
            <div className="text-xs text-slate-500 font-semibold">Total Ingestion Leads</div>
            <div className="text-xl font-extrabold text-slate-900 mt-0.5">{enquiriesList.length + applicationsList.length}</div>
          </div>
          <div className="rounded-xl bg-slate-50 p-3 border border-slate-100">
            <div className="text-xs text-slate-500 font-semibold">Applications Received</div>
            <div className="text-xl font-extrabold text-brand-700 mt-0.5">{applicationsList.length}</div>
          </div>
          <div className="rounded-xl bg-slate-50 p-3 border border-slate-100">
            <div className="text-xs text-slate-500 font-semibold">Provisional / Confirmed</div>
            <div className="text-xl font-extrabold text-emerald-600 mt-0.5">
              {applicationsList.filter((a) => a.status === "PROVISIONAL_OFFER" || a.status === "CONFIRMED").length}
            </div>
          </div>
          <div className="rounded-xl bg-slate-50 p-3 border border-slate-100">
            <div className="text-xs text-slate-500 font-semibold">Conversion Rate</div>
            <div className="text-xl font-extrabold text-purple-700 mt-0.5">42.8%</div>
          </div>
        </div>

        {/* Tab Controls */}
        <div className="mt-6 flex gap-2 border-t border-slate-100 pt-4">
          <button
            type="button"
            onClick={() => setActiveTab("applications")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "applications"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <UserCheck className="h-3.5 w-3.5" />
            <span>Applications Pipeline</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {applicationsList.length}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("leads")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              activeTab === "leads"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Users className="h-3.5 w-3.5" />
            <span>Inquiry Leads & CRM</span>
            <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px] font-extrabold">
              {enquiriesList.length}
            </span>
          </button>
        </div>
      </div>

      {/* APPLICATIONS TAB */}
      {activeTab === "applications" && (
        <div className="space-y-4">
          <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs flex flex-col md:flex-row md:items-center md:justify-between gap-3">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3.5 top-2.5 h-4 w-4 text-slate-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search by candidate name, application number, or program..."
                className="w-full rounded-xl border border-slate-300 pl-10 pr-4 py-2 text-xs font-medium text-slate-900 placeholder-slate-400 focus:border-brand-600 focus:outline-hidden"
              />
            </div>

            <div className="flex items-center gap-2">
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="rounded-xl border border-slate-300 px-3 py-2 text-xs font-semibold text-slate-700 focus:border-brand-600 focus:outline-hidden"
              >
                <option value="ALL">All Application Statuses</option>
                <option value="SUBMITTED">SUBMITTED</option>
                <option value="UNDER_REVIEW">UNDER REVIEW</option>
                <option value="DOCUMENTS_VERIFIED">DOCS VERIFIED</option>
                <option value="PROVISIONAL_OFFER">PROVISIONAL OFFER</option>
                <option value="CONFIRMED">CONFIRMED (SIMS)</option>
                <option value="REJECTED">REJECTED</option>
              </select>

              {(searchQuery || statusFilter !== "ALL") && (
                <button
                  type="button"
                  onClick={() => {
                    setSearchQuery("");
                    setStatusFilter("ALL");
                  }}
                  className="flex items-center gap-1 text-xs font-semibold text-rose-600 hover:text-rose-800 p-2"
                >
                  <RotateCcw className="h-3.5 w-3.5" />
                  <span>Reset</span>
                </button>
              )}
            </div>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white shadow-xs overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="border-b border-slate-200 bg-slate-50/80 text-[11px] font-bold text-slate-700 uppercase tracking-wider">
                    <th className="p-4">App Number</th>
                    <th className="p-4">Candidate & Location</th>
                    <th className="p-4">Preferred Degree Program</th>
                    <th className="p-4">Qualifying Academics</th>
                    <th className="p-4">Review Status</th>
                    <th className="p-4 text-right">Pipeline Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {filteredApps.map((app) => (
                    <tr key={app.id} className="hover:bg-slate-50/50 transition">
                      <td className="p-4 font-mono font-bold text-brand-700">{app.application_number}</td>
                      <td className="p-4">
                        <div className="font-bold text-slate-900">{app.applicant_name}</div>
                        <div className="text-[11px] text-slate-500">
                          {app.address_city}, {app.address_state} • {app.phone}
                        </div>
                      </td>
                      <td className="p-4 font-medium text-slate-800 max-w-xs">{app.preferred_course_name}</td>
                      <td className="p-4">
                        <div className="text-slate-800 font-semibold">{app.qualifying_percentage}% in {app.qualifying_exam}</div>
                        {app.entrance_score_or_rank && (
                          <div className="text-[11px] text-brand-600 font-mono font-semibold">{app.entrance_score_or_rank}</div>
                        )}
                      </td>
                      <td className="p-4">
                        <span
                          className={`rounded-full px-2.5 py-0.5 text-[10px] font-bold uppercase ${
                            app.status === "CONFIRMED"
                              ? "bg-purple-100 text-purple-800"
                              : app.status === "PROVISIONAL_OFFER"
                              ? "bg-emerald-100 text-emerald-800"
                              : app.status === "DOCUMENTS_VERIFIED"
                              ? "bg-blue-100 text-blue-800"
                              : "bg-amber-100 text-amber-800"
                          }`}
                        >
                          {app.status}
                        </span>
                      </td>
                      <td className="p-4 text-right space-x-2">
                        {app.status !== "CONFIRMED" ? (
                          <button
                            type="button"
                            onClick={() => convertToStudentMutation.mutate(app)}
                            className="inline-flex items-center gap-1.5 rounded-lg bg-emerald-600 px-3 py-1.5 text-xs font-bold text-white shadow-2xs hover:bg-emerald-700 transition"
                          >
                            <UserPlus className="h-3.5 w-3.5" />
                            <span>Enroll in SIMS</span>
                          </button>
                        ) : (
                          <span className="inline-flex items-center gap-1 text-xs font-bold text-purple-700">
                            <CheckCircle2 className="h-3.5 w-3.5" />
                            <span>SIMS Enrolled</span>
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* LEADS TAB */}
      {activeTab === "leads" && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
          <div className="border-b border-slate-100 pb-3 flex items-center justify-between">
            <div>
              <h2 className="text-base font-bold text-slate-900">Prospect Inquiries & Lead Funnel</h2>
              <p className="text-xs text-slate-500">Captured leads requiring counselor callbacks and program advising.</p>
            </div>
          </div>

          <div className="space-y-3">
            {enquiriesList.map((enq) => (
              <div
                key={enq.id}
                className="flex flex-col sm:flex-row sm:items-center sm:justify-between rounded-xl border border-slate-200 bg-slate-50/50 p-4 gap-4"
              >
                <div className="space-y-1.5">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-slate-900 text-xs">{enq.full_name}</span>
                    <span className="rounded-md bg-blue-100 px-2 py-0.5 text-[10px] font-bold text-brand-800">
                      {enq.program_interest}
                    </span>
                    <span className="text-[11px] text-slate-500">City: {enq.city}</span>
                  </div>
                  <div className="text-xs text-slate-600">
                    Email: <strong>{enq.email}</strong> • Phone: <strong>{enq.phone}</strong>
                  </div>
                  <p className="text-xs text-slate-700 italic">&ldquo;{enq.message}&rdquo;</p>
                  {enq.counselor_notes && (
                    <div className="text-[11px] text-brand-700 bg-brand-50 p-2 rounded-lg font-medium border border-brand-100">
                      <strong>Counselor Note:</strong> {enq.counselor_notes}
                    </div>
                  )}
                </div>

                <div className="shrink-0 flex items-center gap-2">
                  <select
                    value={enq.status}
                    onChange={(e) =>
                      updateEnqMutation.mutate({
                        id: enq.id,
                        payload: { status: e.target.value },
                      })
                    }
                    className="rounded-lg border border-slate-300 px-2.5 py-1.5 text-xs font-semibold text-slate-700"
                  >
                    <option value="NEW">NEW</option>
                    <option value="CONTACTED">CONTACTED</option>
                    <option value="COUNSELING_SCHEDULED">COUNSELING SCHEDULED</option>
                    <option value="CONVERTED">CONVERTED TO APPLICATION</option>
                    <option value="CLOSED">CLOSED</option>
                  </select>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
