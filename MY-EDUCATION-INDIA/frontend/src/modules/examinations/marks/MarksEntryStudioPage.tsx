import React, { useState, useMemo } from "react";
import { Link } from "react-router-dom";
import {
  FileSpreadsheet,
  Upload,
  Download,
  Lock,
  Unlock,
  CheckCircle2,
  Clock,
  ShieldCheck,
  Search,
  Filter,
  Check,
  X,
  FileText,
  AlertTriangle,
  ChevronRight,
  Edit2,
  Save,
  Sliders,
  Sparkles,
  ArrowRight,
  Send,
  HelpCircle,
  FileCheck,
  Award,
} from "lucide-react";

interface StudentMark {
  id: string;
  studentId: string;
  rollNumber: string;
  enrollmentNo: string;
  candidateName: string;
  marksObtained: number;
  isAbsent: boolean;
  isMalpractice: boolean;
  isPassed: boolean;
  gradeLetter: string;
  facultyRemarks: string;
}

interface MarksSubmission {
  id: string;
  courseCode: string;
  courseTitle: string;
  componentType: "THEORY_INTERNAL" | "THEORY_EXTERNAL" | "PRACTICAL_INTERNAL" | "ASSIGNMENT";
  semesterCode: string;
  facultyName: string;
  departmentName: string;
  maxMarks: number;
  passingMarks: number;
  status: "DRAFT" | "SUBMITTED" | "HOD_APPROVED" | "COE_LOCKED" | "REJECTED_REVISION";
  isLocked: boolean;
  lockedAt?: string;
  hodApprovedAt?: string;
  coeApprovedAt?: string;
  approvalNotes?: string;
}

export const MarksEntryStudioPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<"THEORY_INTERNAL" | "THEORY_EXTERNAL" | "ASSIGNMENT">("THEORY_INTERNAL");
  const [searchQuery, setSearchQuery] = useState("");
  const [isExcelModalOpen, setIsExcelModalOpen] = useState(false);
  const [isWorkflowModalOpen, setIsWorkflowModalOpen] = useState(false);
  const [workflowAction, setWorkflowAction] = useState<"SUBMIT" | "HOD_APPROVE" | "COE_LOCK" | "REJECT_REVISION">("SUBMIT");
  const [approvalNotes, setApprovalNotes] = useState("Marks verified against continuous assessment records. Approved for result processing.");
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 4000);
  };

  // Submissions state
  const [submission, setSubmission] = useState<MarksSubmission>({
    id: "sub-1",
    courseCode: "CS-301",
    courseTitle: "Database Management Systems",
    componentType: "THEORY_INTERNAL",
    semesterCode: "SEM-5",
    facultyName: "Prof. K. K. Sharma",
    departmentName: "Computer Science & Engineering",
    maxMarks: 30,
    passingMarks: 12,
    status: "DRAFT",
    isLocked: false,
  });

  // Marks Records state
  const [marksList, setMarksList] = useState<StudentMark[]>([
    {
      id: "mk-1",
      studentId: "std-1",
      rollNumber: "230105001",
      enrollmentNo: "MEI2023CS001",
      candidateName: "Aarav Sharma",
      marksObtained: 27,
      isAbsent: false,
      isMalpractice: false,
      isPassed: true,
      gradeLetter: "A+",
      facultyRemarks: "Consistent top performer in quizzes and mid-terms.",
    },
    {
      id: "mk-2",
      studentId: "std-2",
      rollNumber: "230105002",
      enrollmentNo: "MEI2023CS002",
      candidateName: "Ananya Verma",
      marksObtained: 28.5,
      isAbsent: false,
      isMalpractice: false,
      isPassed: true,
      gradeLetter: "A+",
      facultyRemarks: "Flawless schema normalization assignment.",
    },
    {
      id: "mk-3",
      studentId: "std-3",
      rollNumber: "230105003",
      enrollmentNo: "MEI2023CS003",
      candidateName: "Rohan Patel",
      marksObtained: 22,
      isAbsent: false,
      isMalpractice: false,
      isPassed: true,
      gradeLetter: "B+",
      facultyRemarks: "Good query tuning performance.",
    },
    {
      id: "mk-4",
      studentId: "std-4",
      rollNumber: "230105004",
      enrollmentNo: "MEI2023CS004",
      candidateName: "Priya Deshmukh",
      marksObtained: 24.5,
      isAbsent: false,
      isMalpractice: false,
      isPassed: true,
      gradeLetter: "A",
      facultyRemarks: "High attendance and timely tutorial submissions.",
    },
    {
      id: "mk-5",
      studentId: "std-5",
      rollNumber: "230105005",
      enrollmentNo: "MEI2023CS005",
      candidateName: "Vikramaditya Singh",
      marksObtained: 19,
      isAbsent: false,
      isMalpractice: false,
      isPassed: true,
      gradeLetter: "B",
      facultyRemarks: "Satisfactory mid-term results.",
    },
  ]);

  // Compute Grade Letter (UGC 10-Point Scale)
  const computeGrade = (score: number, max: number): string => {
    const pct = (score / max) * 100;
    if (pct >= 90) return "A+";
    if (pct >= 80) return "A";
    if (pct >= 70) return "B+";
    if (pct >= 60) return "B";
    if (pct >= 50) return "C";
    if (pct >= 40) return "P";
    return "F";
  };

  // Filtered Marks
  const filteredMarks = useMemo(() => {
    return marksList.filter((m) => {
      const match =
        m.candidateName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        m.rollNumber.toLowerCase().includes(searchQuery.toLowerCase()) ||
        m.enrollmentNo.toLowerCase().includes(searchQuery.toLowerCase());
      return match;
    });
  }, [marksList, searchQuery]);

  // Aggregate Metrics
  const totalEnrolled = marksList.length;
  const validMarks = marksList.filter((m) => !m.isAbsent).map((m) => m.marksObtained);
  const highestScore = validMarks.length > 0 ? Math.max(...validMarks) : 0;
  const lowestScore = validMarks.length > 0 ? Math.min(...validMarks) : 0;
  const averageScore = validMarks.length > 0 ? (validMarks.reduce((a, b) => a + b, 0) / validMarks.length).toFixed(1) : "0.0";
  const passedCount = marksList.filter((m) => m.isPassed).length;

  // Handle Mark Change
  const handleScoreChange = (recordId: string, val: number) => {
    if (val > submission.maxMarks) {
      showToast(`Warning: Marks cannot exceed maximum ceiling of ${submission.maxMarks}!`);
      return;
    }
    if (val < 0) return;

    setMarksList(
      marksList.map((m) => {
        if (m.id === recordId) {
          const isPass = val >= submission.passingMarks;
          const grade = computeGrade(val, submission.maxMarks);
          return {
            ...m,
            marksObtained: val,
            isAbsent: false,
            isPassed: isPass,
            gradeLetter: grade,
          };
        }
        return m;
      })
    );
  };

  // Handle Absent Toggle
  const handleToggleAbsent = (recordId: string) => {
    setMarksList(
      marksList.map((m) => {
        if (m.id === recordId) {
          const newAbsent = !m.isAbsent;
          return {
            ...m,
            isAbsent: newAbsent,
            marksObtained: newAbsent ? 0 : m.marksObtained,
            isPassed: !newAbsent && m.marksObtained >= submission.passingMarks,
            gradeLetter: newAbsent ? "AB" : computeGrade(m.marksObtained, submission.maxMarks),
          };
        }
        return m;
      })
    );
  };

  // Handle Workflow Action
  const handleExecuteWorkflow = (e: React.FormEvent) => {
    e.preventDefault();
    let newStatus = submission.status;
    let locked = submission.isLocked;

    if (workflowAction === "SUBMIT") {
      newStatus = "SUBMITTED";
      locked = true;
      showToast("Marks submitted to Head of Department (HOD) for scrutiny. Editing locked.");
    } else if (workflowAction === "HOD_APPROVE") {
      newStatus = "HOD_APPROVED";
      locked = true;
      showToast("HOD approval granted. Forwarded to Controller of Examination (COE).");
    } else if (workflowAction === "COE_LOCK") {
      newStatus = "COE_LOCKED";
      locked = true;
      showToast("Controller of Examination sealed marks! Permanently locked for result publication.");
    } else if (workflowAction === "REJECT_REVISION") {
      newStatus = "REJECTED_REVISION";
      locked = false;
      showToast("Marks rejected and returned to course faculty for revision.");
    }

    setSubmission({
      ...submission,
      status: newStatus,
      isLocked: locked,
      approvalNotes: approvalNotes,
    });
    setIsWorkflowModalOpen(false);
  };

  // Handle Excel Template Download
  const handleDownloadTemplate = () => {
    const csvContent =
      "Roll Number,Enrollment No,Candidate Name,Marks Obtained,Is Absent (Y/N),Faculty Remarks\n" +
      marksList.map((m) => `"${m.rollNumber}","${m.enrollmentNo}","${m.candidateName}",${m.marksObtained},"N",""`).join("\n");
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `Marks_Template_${submission.courseCode}_${submission.componentType}.csv`;
    a.click();
    showToast("Official Excel/CSV marks template downloaded.");
  };

  // Simulate Excel Import
  const handleImportExcel = () => {
    showToast("Excel file imported successfully! 5 candidate records reconciled with zero errors.");
    setIsExcelModalOpen(false);
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 p-4 md:p-8">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed bottom-6 right-6 z-50 bg-indigo-900 text-white px-4 py-3 rounded-xl shadow-2xl flex items-center gap-3 border border-indigo-700 animate-in fade-in slide-in-from-bottom-2">
          <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
          <span className="text-xs font-semibold">{toastMessage}</span>
        </div>
      )}

      <div className="max-w-7xl mx-auto space-y-6">
        {/* Breadcrumb & Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-5">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-indigo-600 dark:text-indigo-400 mb-1">
              <Link to="/exams" className="hover:underline">EMS</Link>
              <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
              <Link to="/exams/planning" className="hover:underline">Planning</Link>
              <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
              <span>Marks Entry</span>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-100 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 ml-2">
                Phase 4 Module 11
              </span>
            </div>
            <h1 className="text-2xl md:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight flex items-center gap-3">
              <FileSpreadsheet className="w-8 h-8 text-indigo-600 dark:text-indigo-400" />
              Faculty Marks Entry & Approval Studio
            </h1>
            <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
              CS-301 Database Management Systems • {submission.departmentName} • {submission.facultyName}
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <button
              onClick={handleDownloadTemplate}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-semibold rounded-lg border border-slate-300 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 transition"
            >
              <Download className="w-4 h-4 text-slate-500" />
              Download Template
            </button>

            <button
              onClick={() => setIsExcelModalOpen(true)}
              disabled={submission.isLocked}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-semibold rounded-lg border border-slate-300 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 transition disabled:opacity-50"
            >
              <Upload className="w-4 h-4 text-slate-500" />
              Import Excel / CSV
            </button>

            <button
              onClick={() => {
                if (submission.status === "DRAFT") setWorkflowAction("SUBMIT");
                else if (submission.status === "SUBMITTED") setWorkflowAction("HOD_APPROVE");
                else if (submission.status === "HOD_APPROVED") setWorkflowAction("COE_LOCK");
                setIsWorkflowModalOpen(true);
              }}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm transition"
            >
              <ShieldCheck className="w-4 h-4" />
              {submission.status === "DRAFT"
                ? "Submit to HOD"
                : submission.status === "SUBMITTED"
                ? "HOD Approval"
                : submission.status === "HOD_APPROVED"
                ? "COE Final Lock"
                : "Sealed & Locked"}
            </button>
          </div>
        </div>

        {/* Multi-Level Approval Hierarchy Stepper */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-sm">
          <div className="flex items-center justify-between max-w-3xl mx-auto text-xs font-semibold">
            {/* Step 1 */}
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold">
                1
              </div>
              <div>
                <div className="text-slate-900 dark:text-white font-bold">Faculty Submission</div>
                <div className="text-[10px] text-slate-500">
                  {submission.status !== "DRAFT" ? "Completed" : "Active Editing"}
                </div>
              </div>
            </div>

            <ChevronRight className="w-4 h-4 text-slate-400" />

            {/* Step 2 */}
            <div className="flex items-center gap-2">
              <div
                className={`w-7 h-7 rounded-full flex items-center justify-center font-bold ${
                  submission.status === "HOD_APPROVED" || submission.status === "COE_LOCKED"
                    ? "bg-indigo-600 text-white"
                    : submission.status === "SUBMITTED"
                    ? "bg-amber-500 text-white ring-4 ring-amber-100 dark:ring-amber-950"
                    : "bg-slate-200 dark:bg-slate-800 text-slate-400"
                }`}
              >
                2
              </div>
              <div>
                <div className="text-slate-900 dark:text-white font-bold">HOD Scrutiny</div>
                <div className="text-[10px] text-slate-500">
                  {submission.status === "HOD_APPROVED" || submission.status === "COE_LOCKED"
                    ? "Approved"
                    : submission.status === "SUBMITTED"
                    ? "Pending Review"
                    : "Waiting"}
                </div>
              </div>
            </div>

            <ChevronRight className="w-4 h-4 text-slate-400" />

            {/* Step 3 */}
            <div className="flex items-center gap-2">
              <div
                className={`w-7 h-7 rounded-full flex items-center justify-center font-bold ${
                  submission.status === "COE_LOCKED"
                    ? "bg-emerald-600 text-white"
                    : "bg-slate-200 dark:bg-slate-800 text-slate-400"
                }`}
              >
                3
              </div>
              <div>
                <div className="text-slate-900 dark:text-white font-bold">COE Final Seal</div>
                <div className="text-[10px] text-slate-500">
                  {submission.status === "COE_LOCKED" ? "Locked for Tabulation" : "Pending Lock"}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Institutional Summary KPIs */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-sm">
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-slate-500 dark:text-slate-400">Total Enrolled</span>
              <Users className="w-4 h-4 text-indigo-500" />
            </div>
            <div className="mt-2 text-2xl font-black text-slate-900 dark:text-white">{totalEnrolled}</div>
            <div className="text-[11px] text-slate-500 mt-0.5">100% Marks Entered</div>
          </div>

          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-sm">
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-slate-500 dark:text-slate-400">Average Class Score</span>
              <Award className="w-4 h-4 text-emerald-500" />
            </div>
            <div className="mt-2 text-2xl font-black text-slate-900 dark:text-white">
              {averageScore} / {submission.maxMarks}
            </div>
            <div className="text-[11px] text-emerald-600 dark:text-emerald-400 mt-0.5">
              High: {highestScore} • Low: {lowestScore}
            </div>
          </div>

          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-sm">
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-slate-500 dark:text-slate-400">Passed Candidates</span>
              <CheckCircle2 className="w-4 h-4 text-blue-500" />
            </div>
            <div className="mt-2 text-2xl font-black text-blue-600 dark:text-blue-400">
              {passedCount} / {totalEnrolled}
            </div>
            <div className="text-[11px] text-blue-600 dark:text-blue-400 mt-0.5">
              Passing Floor: {submission.passingMarks} Marks
            </div>
          </div>

          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-sm">
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-slate-500 dark:text-slate-400">Lock Status</span>
              {submission.isLocked ? <Lock className="w-4 h-4 text-emerald-500" /> : <Unlock className="w-4 h-4 text-amber-500" />}
            </div>
            <div className="mt-2 text-2xl font-black text-slate-900 dark:text-white">
              {submission.status.replace("_", " ")}
            </div>
            <div className="text-[11px] text-slate-500 mt-0.5">
              {submission.isLocked ? "Read-Only Lock Enabled" : "Faculty Draft Editable"}
            </div>
          </div>
        </div>

        {/* Component Selector Tabs */}
        <div className="border-b border-slate-200 dark:border-slate-800">
          <nav className="flex space-x-2 md:space-x-4 overflow-x-auto pb-px" aria-label="Tabs">
            {[
              { id: "THEORY_INTERNAL", label: "Mid-Term Theory Internal (Max 30, Pass 12)" },
              { id: "THEORY_EXTERNAL", label: "End-Semester External Exam (Max 70, Pass 28)" },
              { id: "ASSIGNMENT", label: "Assignment & Continuous Evaluation (Max 20)" },
            ].map((tab) => {
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => {
                    setActiveTab(tab.id as any);
                    const newMax = tab.id === "THEORY_EXTERNAL" ? 70 : tab.id === "THEORY_INTERNAL" ? 30 : 20;
                    const newPass = tab.id === "THEORY_EXTERNAL" ? 28 : tab.id === "THEORY_INTERNAL" ? 12 : 8;
                    setSubmission({
                      ...submission,
                      componentType: tab.id as any,
                      maxMarks: newMax,
                      passingMarks: newPass,
                    });
                  }}
                  className={`py-3 px-3 text-xs md:text-sm font-semibold border-b-2 whitespace-nowrap transition-colors ${
                    isActive
                      ? "border-indigo-600 text-indigo-600 dark:border-indigo-400 dark:text-indigo-400"
                      : "border-transparent text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200"
                  }`}
                >
                  {tab.label}
                </button>
              );
            })}
          </nav>
        </div>

        {/* ONLINE MARKS ENTRY GRID */}
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="relative flex-1 min-w-[200px] max-w-sm">
              <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                placeholder="Search candidate, roll, or enrollment..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => {
                  showToast("Candidate marks saved successfully!");
                }}
                disabled={submission.isLocked}
                className="px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 shadow-sm disabled:opacity-50"
              >
                <Save className="w-3.5 h-3.5" /> Save Changes
              </button>
            </div>
          </div>

          {/* Table */}
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden shadow-sm">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 dark:bg-slate-800/50 text-slate-500 dark:text-slate-400 uppercase tracking-wider font-semibold border-b border-slate-200 dark:border-slate-800">
                  <tr>
                    <th className="px-4 py-3">Roll & Enrollment No.</th>
                    <th className="px-4 py-3">Candidate Name</th>
                    <th className="px-4 py-3 text-center">Marks Obtained (Max {submission.maxMarks})</th>
                    <th className="px-4 py-3 text-center">Absent (AB)</th>
                    <th className="px-4 py-3 text-center">Grade Letter</th>
                    <th className="px-4 py-3">Status</th>
                    <th className="px-4 py-3">Faculty Remarks</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 dark:divide-slate-800 font-medium">
                  {filteredMarks.map((m) => (
                    <tr key={m.id} className="hover:bg-slate-50/60 dark:hover:bg-slate-800/40 transition">
                      <td className="px-4 py-3">
                        <div className="font-mono font-bold text-slate-900 dark:text-white">{m.rollNumber}</div>
                        <div className="text-[10px] text-slate-500 font-mono">{m.enrollmentNo}</div>
                      </td>

                      <td className="px-4 py-3 font-semibold text-slate-800 dark:text-slate-200">
                        {m.candidateName}
                      </td>

                      <td className="px-4 py-3 text-center">
                        <input
                          type="number"
                          min="0"
                          max={submission.maxMarks}
                          step="0.5"
                          disabled={submission.isLocked || m.isAbsent}
                          value={m.isAbsent ? 0 : m.marksObtained}
                          onChange={(e) => handleScoreChange(m.id, Number(e.target.value))}
                          className={`w-20 px-2 py-1 rounded border font-mono font-bold text-center focus:ring-2 focus:ring-indigo-500 ${
                            m.marksObtained > submission.maxMarks
                              ? "border-rose-500 bg-rose-50 text-rose-600"
                              : "border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800"
                          }`}
                        />
                      </td>

                      <td className="px-4 py-3 text-center">
                        <input
                          type="checkbox"
                          checked={m.isAbsent}
                          disabled={submission.isLocked}
                          onChange={() => handleToggleAbsent(m.id)}
                          className="rounded text-indigo-600 focus:ring-indigo-500"
                        />
                      </td>

                      <td className="px-4 py-3 text-center font-mono font-bold text-indigo-600 dark:text-indigo-400">
                        {m.gradeLetter}
                      </td>

                      <td className="px-4 py-3">
                        <span
                          className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold ${
                            m.isPassed
                              ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300"
                              : "bg-rose-100 text-rose-700 dark:bg-rose-950 dark:text-rose-300"
                          }`}
                        >
                          {m.isPassed ? "PASS" : "FAIL"}
                        </span>
                      </td>

                      <td className="px-4 py-3 text-slate-500 text-[11px] max-w-[200px] truncate" title={m.facultyRemarks}>
                        {m.facultyRemarks}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      {/* MODAL 1: EXCEL / CSV IMPORT */}
      {isExcelModalOpen && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
              <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <Upload className="w-5 h-5 text-indigo-600" />
                Import Marks from Excel / CSV
              </h3>
              <button
                onClick={() => setIsExcelModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-4 text-xs">
              <p className="text-slate-600 dark:text-slate-400">
                Upload your completed offline marksheet. Ensure roll numbers match enrolled student IDs and marks do not exceed {submission.maxMarks}.
              </p>

              <div className="border-2 border-dashed border-slate-300 dark:border-slate-700 rounded-xl p-6 text-center space-y-2 bg-slate-50 dark:bg-slate-800/40">
                <FileSpreadsheet className="w-8 h-8 text-indigo-500 mx-auto" />
                <div className="font-semibold text-slate-800 dark:text-slate-200">
                  Drag & Drop Excel (.xlsx) or CSV file
                </div>
                <div className="text-[10px] text-slate-500">Supports standard UTF-8 CSV exports</div>
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-100 dark:border-slate-800">
                <button
                  type="button"
                  onClick={() => setIsExcelModalOpen(false)}
                  className="px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={handleImportExcel}
                  className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white font-semibold"
                >
                  Confirm & Import
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* MODAL 2: MULTI-LEVEL APPROVAL WORKFLOW */}
      {isWorkflowModalOpen && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
              <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-indigo-600" />
                Marks Approval Hierarchy
              </h3>
              <button
                onClick={() => setIsWorkflowModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleExecuteWorkflow} className="space-y-4 text-xs">
              <div>
                <label className="block font-semibold mb-1">Select Approval Action</label>
                <select
                  value={workflowAction}
                  onChange={(e) => setWorkflowAction(e.target.value as any)}
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800"
                >
                  <option value="SUBMIT">Faculty Submission (Lock Marks against edits)</option>
                  <option value="HOD_APPROVE">HOD Scrutiny Approval (Forward to COE)</option>
                  <option value="COE_LOCK">COE Final Seal & Lock (Ready for Result Tabulation)</option>
                  <option value="REJECT_REVISION">Reject & Return to Faculty for Revision</option>
                </select>
              </div>

              <div>
                <label className="block font-semibold mb-1">Approval / Scrutiny Notes</label>
                <textarea
                  rows={2}
                  required
                  value={approvalNotes}
                  onChange={(e) => setApprovalNotes(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-100 dark:border-slate-800">
                <button
                  type="button"
                  onClick={() => setIsWorkflowModalOpen(false)}
                  className="px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white font-semibold"
                >
                  Execute Transition
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
export default MarksEntryStudioPage;
