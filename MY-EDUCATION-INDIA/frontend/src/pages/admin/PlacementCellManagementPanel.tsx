import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Briefcase,
  Building,
  Calendar,
  CheckCircle2,
  Code2,
  ExternalLink,
  GraduationCap,
  IndianRupee,
  Layers,
  MapPin,
  Plus,
  Sparkles,
  Trash2,
  TrendingUp,
} from "lucide-react";
import { websiteService } from "@/services/websiteService";
import {
  CmsInternshipOpportunity,
  CmsInternshipOpportunityCreateRequest,
  CmsPlacementDrive,
  CmsPlacementDriveCreateRequest,
  CmsTrainingProgram,
  CmsTrainingProgramCreateRequest,
} from "@/types/website.types";

interface PlacementCellManagementPanelProps {
  initialSubTab?: "drives" | "training" | "internships";
}

export const PlacementCellManagementPanel: React.FC<PlacementCellManagementPanelProps> = ({
  initialSubTab = "drives",
}) => {
  const queryClient = useQueryClient();
  const [subTab, setSubTab] = useState<"drives" | "training" | "internships">(initialSubTab);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  // Queries
  const { data: drives = [] } = useQuery({
    queryKey: ["admin-placement-drives"],
    queryFn: websiteService.listAdminPlacementDrives,
  });

  const { data: trainingPrograms = [] } = useQuery({
    queryKey: ["admin-placement-training"],
    queryFn: websiteService.listAdminTrainingPrograms,
  });

  const { data: internships = [] } = useQuery({
    queryKey: ["admin-placement-internships"],
    queryFn: websiteService.listAdminInternships,
  });

  // Form States: Drive
  const [driveCompany, setDriveCompany] = useState("");
  const [driveSlug, setDriveSlug] = useState("");
  const [driveRole, setDriveRole] = useState("");
  const [driveCtc, setDriveCtc] = useState("₹24.0 LPA");
  const [driveDate, setDriveDate] = useState("2026-04-10");
  const [driveDeadline, setDriveDeadline] = useState("2026-04-02");
  const [driveBranches, setDriveBranches] = useState("B.Tech CSE, AI & Data Science (CGPA >= 7.5)");
  const [driveProcess, setDriveProcess] = useState("1. Online Coding -> 2. Technical System Design -> 3. HR");
  const [driveLocation, setDriveLocation] = useState("Bengaluru / Hyderabad");
  const [driveStatus, setDriveStatus] = useState("UPCOMING");
  const [driveLink, setDriveLink] = useState("");

  // Form States: Training
  const [trnTitle, setTrnTitle] = useState("");
  const [trnSlug, setTrnSlug] = useState("");
  const [trnType, setTrnType] = useState("TECHNICAL_BOOTCAMP");
  const [trnTrainer, setTrnTrainer] = useState("Industry Principal Architects & FAANG Mentors");
  const [trnWeeks, setTrnWeeks] = useState(8);
  const [trnStartDate, setTrnStartDate] = useState("2026-02-15");
  const [trnEndDate, setTrnEndDate] = useState("2026-04-15");
  const [trnSyllabus, setTrnSyllabus] = useState("Microservices, Distributed Systems, High-Concurrency APIs, Docker/Kubernetes");
  const [trnEligibility, setTrnEligibility] = useState("Pre-final & Final Year Students");
  const [trnMode, setTrnMode] = useState("HYBRID");

  // Form States: Internship
  const [intCompany, setIntCompany] = useState("");
  const [intSlug, setIntSlug] = useState("");
  const [intRole, setIntRole] = useState("");
  const [intStipend, setIntStipend] = useState("₹65,000 / Month");
  const [intDuration, setIntDuration] = useState(6);
  const [intLocation, setIntLocation] = useState("Bengaluru (Hybrid)");
  const [intDeadline, setIntDeadline] = useState("2026-04-15");
  const [intEligibility, setIntEligibility] = useState("B.Tech 3rd Year with Python/C++ & Deep Learning coursework");
  const [intApplyUrl, setIntApplyUrl] = useState("https://myeducation.in/placements/internships/apply/...");
  const [intFeatured, setIntFeatured] = useState(false);

  // Mutations: Drive
  const createDriveMutation = useMutation({
    mutationFn: websiteService.createAdminPlacementDrive,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-placement-drives"] });
      void queryClient.invalidateQueries({ queryKey: ["public-placement-cell-bundle"] });
      setStatusMessage("Campus recruitment drive registered successfully.");
      setTimeout(() => setStatusMessage(null), 3500);
      setDriveCompany("");
      setDriveSlug("");
      setDriveRole("");
      setDriveLink("");
    },
  });

  const deleteDriveMutation = useMutation({
    mutationFn: websiteService.deleteAdminPlacementDrive,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-placement-drives"] });
      void queryClient.invalidateQueries({ queryKey: ["public-placement-cell-bundle"] });
      setStatusMessage("Placement drive removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  // Mutations: Training
  const createTrainingMutation = useMutation({
    mutationFn: websiteService.createAdminTrainingProgram,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-placement-training"] });
      void queryClient.invalidateQueries({ queryKey: ["public-placement-cell-bundle"] });
      setStatusMessage("Corporate training program scheduled.");
      setTimeout(() => setStatusMessage(null), 3500);
      setTrnTitle("");
      setTrnSlug("");
      setTrnSyllabus("");
    },
  });

  const deleteTrainingMutation = useMutation({
    mutationFn: websiteService.deleteAdminTrainingProgram,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-placement-training"] });
      void queryClient.invalidateQueries({ queryKey: ["public-placement-cell-bundle"] });
      setStatusMessage("Training program removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  // Mutations: Internship
  const createInternshipMutation = useMutation({
    mutationFn: websiteService.createAdminInternship,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-placement-internships"] });
      void queryClient.invalidateQueries({ queryKey: ["public-placement-cell-bundle"] });
      setStatusMessage("Internship opportunity published.");
      setTimeout(() => setStatusMessage(null), 3500);
      setIntCompany("");
      setIntSlug("");
      setIntRole("");
      setIntEligibility("");
      setIntApplyUrl("");
      setIntFeatured(false);
    },
  });

  const deleteInternshipMutation = useMutation({
    mutationFn: websiteService.deleteAdminInternship,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin-placement-internships"] });
      void queryClient.invalidateQueries({ queryKey: ["public-placement-cell-bundle"] });
      setStatusMessage("Internship opportunity removed.");
      setTimeout(() => setStatusMessage(null), 3500);
    },
  });

  // Handlers
  const handleCreateDrive = (e: React.FormEvent) => {
    e.preventDefault();
    if (!driveCompany.trim() || !driveRole.trim()) return;
    const slug =
      driveSlug.trim().toLowerCase() ||
      driveCompany.trim().toLowerCase().replace(/[^a-z0-9]+/g, "-") + "-drive";

    createDriveMutation.mutate({
      company_name: driveCompany.trim(),
      slug,
      job_role: driveRole.trim(),
      package_ctc: driveCtc.trim(),
      drive_date: driveDate,
      registration_deadline: driveDeadline,
      eligible_branches: driveBranches.trim(),
      selection_process: driveProcess.trim(),
      job_location: driveLocation.trim(),
      drive_status: driveStatus,
      registration_link: driveLink.trim() || null,
      display_order: drives.length + 1,
      is_active: true,
    });
  };

  const handleCreateTraining = (e: React.FormEvent) => {
    e.preventDefault();
    if (!trnTitle.trim() || !trnSyllabus.trim()) return;
    const slug =
      trnSlug.trim().toLowerCase() ||
      trnTitle.trim().toLowerCase().replace(/[^a-z0-9]+/g, "-");

    createTrainingMutation.mutate({
      title: trnTitle.trim(),
      slug,
      training_type: trnType,
      trainer_name: trnTrainer.trim(),
      duration_weeks: Number(trnWeeks) || 8,
      start_date: trnStartDate,
      end_date: trnEndDate || null,
      syllabus_highlights: trnSyllabus.trim(),
      batch_eligibility: trnEligibility.trim(),
      mode: trnMode,
      display_order: trainingPrograms.length + 1,
      is_active: true,
    });
  };

  const handleCreateInternship = (e: React.FormEvent) => {
    e.preventDefault();
    if (!intCompany.trim() || !intRole.trim()) return;
    const slug =
      intSlug.trim().toLowerCase() ||
      intCompany.trim().toLowerCase().replace(/[^a-z0-9]+/g, "-") + "-internship";

    createInternshipMutation.mutate({
      company_name: intCompany.trim(),
      slug,
      role_title: intRole.trim(),
      stipend_monthly: intStipend.trim(),
      duration_months: Number(intDuration) || 6,
      location: intLocation.trim(),
      application_deadline: intDeadline,
      eligibility_criteria: intEligibility.trim(),
      apply_url: intApplyUrl.trim(),
      is_featured: intFeatured,
      display_order: internships.length + 1,
      is_active: true,
    });
  };

  return (
    <div className="space-y-6">
      {/* Status banner */}
      {statusMessage && (
        <div className="flex items-center gap-2 rounded-xl bg-emerald-50 border border-emerald-200 p-4 text-xs font-semibold text-emerald-800 animate-in fade-in">
          <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-600" />
          <span>{statusMessage}</span>
        </div>
      )}

      {/* Subtab Navigation */}
      <div className="flex items-center justify-between border-b border-slate-200 pb-4">
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => setSubTab("drives")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              subTab === "drives"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Briefcase className="h-4 w-4" />
            <span>Recruitment Drives ({drives.length})</span>
          </button>

          <button
            type="button"
            onClick={() => setSubTab("training")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              subTab === "training"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <Code2 className="h-4 w-4" />
            <span>Corporate Bootcamps ({trainingPrograms.length})</span>
          </button>

          <button
            type="button"
            onClick={() => setSubTab("internships")}
            className={`inline-flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-bold transition ${
              subTab === "internships"
                ? "bg-brand-600 text-white shadow-xs"
                : "bg-slate-100 text-slate-600 hover:bg-slate-200"
            }`}
          >
            <IndianRupee className="h-4 w-4" />
            <span>Internships Board ({internships.length})</span>
          </button>
        </div>

        <div className="flex items-center gap-3 text-xs font-semibold text-brand-600">
          <a
            href="/placements/drives"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:underline flex items-center gap-1"
          >
            <span>Live Drives</span>
            <ExternalLink className="h-3 w-3" />
          </a>
          <span>•</span>
          <a
            href="/placements/internships"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:underline flex items-center gap-1"
          >
            <span>Live Internships</span>
            <ExternalLink className="h-3 w-3" />
          </a>
        </div>
      </div>

      {/* SUBTAB 1: DRIVES */}
      {subTab === "drives" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          {/* Create Form */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center gap-2">
              <Plus className="h-4 w-4 text-brand-600" />
              <span>Schedule Recruitment Drive</span>
            </h2>

            <form onSubmit={handleCreateDrive} className="mt-4 space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Company Name</label>
                <input
                  type="text"
                  required
                  value={driveCompany}
                  onChange={(e) => setDriveCompany(e.target.value)}
                  placeholder="e.g. Google Cloud India"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Job Role / Designation</label>
                <input
                  type="text"
                  required
                  value={driveRole}
                  onChange={(e) => setDriveRole(e.target.value)}
                  placeholder="e.g. SDE-1 / Cloud Systems Architect"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">CTC Package</label>
                  <input
                    type="text"
                    required
                    value={driveCtc}
                    onChange={(e) => setDriveCtc(e.target.value)}
                    placeholder="₹38.5 LPA"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Drive Status</label>
                  <select
                    value={driveStatus}
                    onChange={(e) => setDriveStatus(e.target.value)}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  >
                    <option value="UPCOMING">UPCOMING</option>
                    <option value="ONGOING">ONGOING</option>
                    <option value="COMPLETED">COMPLETED</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Drive Date</label>
                  <input
                    type="date"
                    required
                    value={driveDate}
                    onChange={(e) => setDriveDate(e.target.value)}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Deadline</label>
                  <input
                    type="date"
                    required
                    value={driveDeadline}
                    onChange={(e) => setDriveDeadline(e.target.value)}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Eligible Degree Branches</label>
                <input
                  type="text"
                  required
                  value={driveBranches}
                  onChange={(e) => setDriveBranches(e.target.value)}
                  placeholder="e.g. B.Tech CSE, AI & Data Science (CGPA >= 8.0)"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Selection Process Rounds</label>
                <input
                  type="text"
                  required
                  value={driveProcess}
                  onChange={(e) => setDriveProcess(e.target.value)}
                  placeholder="1. Online Test -> 2. Technical Rounds -> 3. HR"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Job Locations</label>
                <input
                  type="text"
                  value={driveLocation}
                  onChange={(e) => setDriveLocation(e.target.value)}
                  placeholder="Bengaluru / Hyderabad / Indore"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <button
                type="submit"
                disabled={createDriveMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>{createDriveMutation.isPending ? "Scheduling..." : "Publish Drive"}</span>
              </button>
            </form>
          </div>

          {/* Drives List */}
          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center justify-between">
              <span>Scheduled Recruitment Drives ({drives.length})</span>
              <span className="text-xs font-normal text-slate-500">Live PostgreSQL Database</span>
            </h2>

            <div className="mt-4 space-y-3">
              {drives.map((d) => (
                <div
                  key={d.id}
                  className="flex items-start justify-between rounded-xl border border-slate-200 bg-white p-4 shadow-2xs hover:border-brand-200 transition-all"
                >
                  <div className="space-y-1.5">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="rounded-md bg-brand-100 px-2 py-0.5 text-[10px] font-bold text-brand-800">
                        {d.drive_status}
                      </span>
                      <span className="rounded-full bg-emerald-100 px-2.5 py-0.5 text-[11px] font-black text-emerald-800">
                        {d.package_ctc}
                      </span>
                      <h4 className="text-xs font-bold text-slate-900">{d.company_name}</h4>
                    </div>

                    <p className="text-xs font-semibold text-slate-700">{d.job_role}</p>

                    <div className="flex items-center gap-4 text-[11px] text-slate-500">
                      <span>Drive Date: {d.drive_date}</span>
                      <span>•</span>
                      <span className="text-rose-600 font-semibold">Deadline: {d.registration_deadline}</span>
                      <span>•</span>
                      <span>Location: {d.job_location}</span>
                    </div>

                    <p className="text-[11px] text-slate-500">
                      <span className="font-semibold text-slate-600">Eligible:</span> {d.eligible_branches}
                    </p>
                  </div>

                  <button
                    onClick={() => {
                      if (confirm(`Remove drive for "${d.company_name}"?`)) {
                        deleteDriveMutation.mutate(d.id);
                      }
                    }}
                    className="p-1 text-slate-400 hover:text-red-600 shrink-0 ml-3"
                    title="Delete drive"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* SUBTAB 2: TRAINING */}
      {subTab === "training" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          {/* Create Training Form */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center gap-2">
              <Plus className="h-4 w-4 text-brand-600" />
              <span>Schedule Training Bootcamp</span>
            </h2>

            <form onSubmit={handleCreateTraining} className="mt-4 space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Bootcamp Title</label>
                <input
                  type="text"
                  required
                  value={trnTitle}
                  onChange={(e) => setTrnTitle(e.target.value)}
                  placeholder="e.g. Enterprise Full-Stack Cloud Bootcamp"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Training Type</label>
                  <select
                    value={trnType}
                    onChange={(e) => setTrnType(e.target.value)}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  >
                    <option value="TECHNICAL_BOOTCAMP">Technical Bootcamp & DSA</option>
                    <option value="MOCK_INTERVIEW">Mock Interviews</option>
                    <option value="APTITUDE_LOGICAL">Aptitude & Reasoning</option>
                    <option value="SOFT_SKILLS">Executive Soft Skills</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Duration (Weeks)</label>
                  <input
                    type="number"
                    min={1}
                    value={trnWeeks}
                    onChange={(e) => setTrnWeeks(Number(e.target.value))}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Lead Trainer / Mentor</label>
                <input
                  type="text"
                  required
                  value={trnTrainer}
                  onChange={(e) => setTrnTrainer(e.target.value)}
                  placeholder="Industry Principal Architects & FAANG Mentors"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Start Date</label>
                  <input
                    type="date"
                    required
                    value={trnStartDate}
                    onChange={(e) => setTrnStartDate(e.target.value)}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Delivery Mode</label>
                  <select
                    value={trnMode}
                    onChange={(e) => setTrnMode(e.target.value)}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  >
                    <option value="HYBRID">HYBRID</option>
                    <option value="OFFLINE">OFFLINE (Campus Labs)</option>
                    <option value="ONLINE">ONLINE</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Syllabus Highlights</label>
                <textarea
                  rows={3}
                  required
                  value={trnSyllabus}
                  onChange={(e) => setTrnSyllabus(e.target.value)}
                  placeholder="Comma-separated modules e.g. Microservices, PostgreSQL, Kubernetes..."
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <button
                type="submit"
                disabled={createTrainingMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Publish Training Track</span>
              </button>
            </form>
          </div>

          {/* Training List */}
          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center justify-between">
              <span>Active Training Bootcamps ({trainingPrograms.length})</span>
            </h2>

            <div className="mt-4 space-y-3">
              {trainingPrograms.map((t) => (
                <div
                  key={t.id}
                  className="flex items-start justify-between rounded-xl border border-slate-200 bg-white p-4 shadow-2xs hover:border-brand-200 transition-all"
                >
                  <div className="space-y-1.5">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="rounded-md bg-purple-100 px-2 py-0.5 text-[10px] font-bold text-purple-700">
                        {t.training_type}
                      </span>
                      <span className="rounded-md bg-slate-100 px-2 py-0.5 text-[10px] font-semibold text-slate-700">
                        {t.duration_weeks} Weeks • {t.mode}
                      </span>
                      <h4 className="text-xs font-bold text-slate-900">{t.title}</h4>
                    </div>

                    <p className="text-[11px] text-slate-500">
                      Instructor: <span className="font-semibold text-slate-700">{t.trainer_name}</span> • Start: {t.start_date}
                    </p>

                    <p className="text-xs text-slate-600 line-clamp-2">{t.syllabus_highlights}</p>
                  </div>

                  <button
                    onClick={() => {
                      if (confirm(`Remove training program "${t.title}"?`)) {
                        deleteTrainingMutation.mutate(t.id);
                      }
                    }}
                    className="p-1 text-slate-400 hover:text-red-600 shrink-0 ml-3"
                    title="Delete program"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* SUBTAB 3: INTERNSHIPS */}
      {subTab === "internships" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          {/* Create Internship Form */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center gap-2">
              <Plus className="h-4 w-4 text-brand-600" />
              <span>Post Internship Opportunity</span>
            </h2>

            <form onSubmit={handleCreateInternship} className="mt-4 space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Company Name</label>
                <input
                  type="text"
                  required
                  value={intCompany}
                  onChange={(e) => setIntCompany(e.target.value)}
                  placeholder="e.g. NVIDIA AI Research"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Role Title</label>
                <input
                  type="text"
                  required
                  value={intRole}
                  onChange={(e) => setIntRole(e.target.value)}
                  placeholder="e.g. Deep Learning Research Intern"
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Monthly Stipend</label>
                  <input
                    type="text"
                    required
                    value={intStipend}
                    onChange={(e) => setIntStipend(e.target.value)}
                    placeholder="₹85,000 / Month"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Duration (Months)</label>
                  <input
                    type="number"
                    min={1}
                    max={12}
                    value={intDuration}
                    onChange={(e) => setIntDuration(Number(e.target.value))}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Location</label>
                  <input
                    type="text"
                    value={intLocation}
                    onChange={(e) => setIntLocation(e.target.value)}
                    placeholder="Bengaluru (Hybrid)"
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Deadline</label>
                  <input
                    type="date"
                    required
                    value={intDeadline}
                    onChange={(e) => setIntDeadline(e.target.value)}
                    className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Eligibility Criteria</label>
                <textarea
                  rows={2}
                  required
                  value={intEligibility}
                  onChange={(e) => setIntEligibility(e.target.value)}
                  placeholder="Required coursework, skills, and minimum CGPA..."
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Apply URL</label>
                <input
                  type="url"
                  required
                  value={intApplyUrl}
                  onChange={(e) => setIntApplyUrl(e.target.value)}
                  placeholder="https://..."
                  className="mt-1.5 w-full rounded-xl border border-slate-300 px-3.5 py-2 text-xs font-medium text-slate-900 focus:border-brand-600 focus:outline-hidden"
                />
              </div>

              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="int-featured"
                  checked={intFeatured}
                  onChange={(e) => setIntFeatured(e.target.checked)}
                  className="h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500"
                />
                <label htmlFor="int-featured" className="text-xs font-medium text-slate-700">
                  Highlight as Flagship Research Internship
                </label>
              </div>

              <button
                type="submit"
                disabled={createInternshipMutation.isPending}
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-brand-700 transition"
              >
                <Plus className="h-4 w-4" />
                <span>Post Opportunity</span>
              </button>
            </form>
          </div>

          {/* Internships List */}
          <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center justify-between">
              <span>Active Internship Postings ({internships.length})</span>
            </h2>

            <div className="mt-4 space-y-3">
              {internships.map((i) => (
                <div
                  key={i.id}
                  className="flex items-start justify-between rounded-xl border border-slate-200 bg-white p-4 shadow-2xs hover:border-brand-200 transition-all"
                >
                  <div className="space-y-1.5">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="rounded-md bg-emerald-100 px-2 py-0.5 text-[10px] font-bold text-emerald-800">
                        {i.stipend_monthly}
                      </span>
                      {i.is_featured && (
                        <span className="rounded-full bg-amber-100 px-2 py-0.5 text-[9px] font-extrabold text-amber-800">
                          FLAGSHIP
                        </span>
                      )}
                      <h4 className="text-xs font-bold text-slate-900">{i.company_name}</h4>
                    </div>

                    <p className="text-xs font-semibold text-brand-600">{i.role_title}</p>

                    <div className="flex items-center gap-4 text-[11px] text-slate-500">
                      <span>Duration: {i.duration_months} Months</span>
                      <span>•</span>
                      <span>Location: {i.location}</span>
                      <span>•</span>
                      <span className="text-rose-600">Deadline: {i.application_deadline}</span>
                    </div>

                    <p className="text-[11px] text-slate-600 line-clamp-2">{i.eligibility_criteria}</p>
                  </div>

                  <button
                    onClick={() => {
                      if (confirm(`Remove internship at "${i.company_name}"?`)) {
                        deleteInternshipMutation.mutate(i.id);
                      }
                    }}
                    className="p-1 text-slate-400 hover:text-red-600 shrink-0 ml-3"
                    title="Delete internship"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
