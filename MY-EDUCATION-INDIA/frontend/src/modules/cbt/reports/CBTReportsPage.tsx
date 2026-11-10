import React, { useState } from "react";
import {
  FileText,
  Download,
  Users,
  Building2,
  UserCheck,
  HelpCircle,
  Activity,
  ShieldAlert,
  Search,
  Filter,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Clock,
  Printer,
  Calendar,
  Layers,
  ChevronRight,
  TrendingUp,
  Server,
  QrCode,
  ShieldCheck,
  Check,
} from "lucide-react";

export const CBTReportsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<"ATTENDANCE" | "CENTERS" | "INVIGILATORS" | "QUESTIONS" | "SYSTEM" | "SECURITY">("ATTENDANCE");
  const [selectedShift, setSelectedShift] = useState<string>("SHIFT-1-MORNING");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [isExporting, setIsExporting] = useState<boolean>(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 4000);
  };

  // 1. Attendance & Absentees Dataset
  const attendanceList = [
    { id: "1", name: "Aarav Sharma", roll: "MEI-2026-84920", center: "TC-IND-01", lab: "Computer Lab 01", seat: "LAB1-WS-42", status: "PRESENT", time: "08:42 AM IST", biometric: true },
    { id: "2", name: "Ananya Patel", roll: "MEI-2026-84921", center: "TC-IND-01", lab: "Computer Lab 01", seat: "LAB1-WS-43", status: "PRESENT", time: "08:48 AM IST", biometric: true },
    { id: "3", name: "Rohan Gupta", roll: "MEI-2026-84922", center: "TC-IND-01", lab: "Computer Lab 01", seat: "LAB1-WS-44", status: "PRESENT", time: "08:52 AM IST", biometric: true },
    { id: "4", name: "Ishita Verma", roll: "MEI-2026-84923", center: "TC-IND-01", lab: "Computer Lab 01", seat: "LAB1-WS-45", status: "PRESENT", time: "08:55 AM IST", biometric: true },
    { id: "5", name: "Kabir Joshi", roll: "MEI-2026-84924", center: "TC-IND-01", lab: "Computer Lab 01", seat: "LAB1-WS-46", status: "PRESENT", time: "09:05 AM IST", biometric: true },
    { id: "6", name: "Sneha Reddy", roll: "MEI-2026-84925", center: "TC-IND-01", lab: "Computer Lab 01", seat: "LAB1-WS-47", status: "PRESENT", time: "08:35 AM IST", biometric: true },
    { id: "7", name: "Devansh Chawla", roll: "MEI-2026-84926", center: "TC-IND-01", lab: "Computer Lab 01", seat: "LAB1-WS-48", status: "ABSENT", time: "NO_SHOW", biometric: false },
  ];

  // 2. Centers & Lab Occupancy
  const labsOccupancy = [
    { lab: "Computer Lab 01", floor: "Ground Floor", total: 100, occupied: 90, buffer: 10, allocPct: 90.0, lanStatus: "ONLINE (192.168.10.1)" },
    { lab: "Computer Lab 02", floor: "1st Floor East", total: 80, occupied: 72, buffer: 8, allocPct: 90.0, lanStatus: "ONLINE (192.168.10.2)" },
    { lab: "Computer Lab 03", floor: "1st Floor West", total: 70, occupied: 63, buffer: 7, allocPct: 90.0, lanStatus: "ONLINE (192.168.10.3)" },
  ];

  // 3. Invigilators Roster
  const invigilators = [
    { name: "Prof. Sunita Deshmukh", role: "CHIEF_SUPERINTENDENT", center: "TC-IND-01", lab: "Computer Lab 01", shift: "Shift 1", status: "REPORTED", dutyDate: "10 Nov 2026" },
    { name: "Dr. Rajeshwari Sen", role: "LAB_INVIGILATOR", center: "TC-IND-01", lab: "Computer Lab 01", shift: "Shift 1", status: "ON_DUTY", dutyDate: "10 Nov 2026" },
    { name: "Eng. Amit Kumar", role: "TECHNICAL_OBSERVER", center: "TC-IND-01", lab: "Computer Lab 01", shift: "Shift 1", status: "ON_DUTY", dutyDate: "10 Nov 2026" },
    { name: "Dr. Manoj Tiwari", role: "LAB_INVIGILATOR", center: "TC-IND-01", lab: "Computer Lab 02", shift: "Shift 1", status: "ON_DUTY", dutyDate: "10 Nov 2026" },
  ];

  // 4. Question Item Discrimination
  const questionsAudit = [
    { number: 1, section: "General Aptitude", type: "MCQ", pValue: 0.85, dValue: 0.25, attempts: 6, correct: 5, acc: 83.3, note: "HEALTHY (Good foundational starter)" },
    { number: 2, section: "General Aptitude", type: "MCQ", pValue: 0.80, dValue: 0.32, attempts: 6, correct: 5, acc: 83.3, note: "HEALTHY (Distracter D trapped 1 candidate)" },
    { number: 4, section: "Computer Science", type: "MCQ", pValue: 0.70, dValue: 0.48, attempts: 6, correct: 4, acc: 66.7, note: "OPTIMAL (High discrimination index)" },
    { number: 5, section: "Computer Science", type: "MCQ", pValue: 0.65, dValue: 0.52, attempts: 6, correct: 4, acc: 66.7, note: "OPTIMAL (AVL tree rotation discriminator)" },
    { number: 6, section: "Computer Science", type: "MCQ", pValue: 0.35, dValue: 0.55, attempts: 6, correct: 2, acc: 33.3, note: "HIGHLY_DISCRIMINATING (FCFS turnaround trap)" },
    { number: 7, section: "Engineering Mathematics", type: "MCQ", pValue: 0.60, dValue: 0.42, attempts: 6, correct: 4, acc: 66.7, note: "HEALTHY (Matrix determinant item)" },
    { number: 8, section: "Engineering Mathematics", type: "MCQ", pValue: 0.30, dValue: 0.60, attempts: 6, correct: 2, acc: 33.3, note: "TOP_TIER_DISCRIMINATOR (Eigenvalue trace)" },
  ];

  // 5. System Telemetry
  const telemetry = {
    centerName: "Indore Flagship Testing Center (TC-IND-01)",
    peakConcurrency: 142,
    avgLatency: "2.1 ms",
    bandwidthConsumed: "18.4 GB",
    packetLoss: "0.0%",
    ntpDrift: "1.2 ms (NPL-India Sync)",
    uptime: "99.98%",
  };

  // 6. Security Audit Log
  const securityLog = [
    { time: "13:42:15", terminal: "LAB1-WS-46", candidate: "Kabir Joshi", event: "FULLSCREEN_EXIT", severity: "CRITICAL", action: "AUTO_DISQUALIFIED (Strike 3/3)" },
    { time: "13:38:02", terminal: "LAB1-WS-45", candidate: "Ishita Verma", event: "CLIPBOARD_COPY", severity: "HIGH", action: "WARNED (Strike 2/3)" },
    { time: "13:31:40", terminal: "LAB1-WS-43", candidate: "Ananya Patel", event: "TAB_SWITCH", severity: "MEDIUM", action: "WARNED (Strike 1/3)" },
    { time: "13:20:10", terminal: "LAB1-WS-46", candidate: "Kabir Joshi", event: "RIGHT_CLICK", severity: "LOW", action: "BLOCKED (Context Menu Intercepted)" },
  ];

  const handleExport = (format: string) => {
    setIsExporting(true);
    setTimeout(() => {
      setIsExporting(false);
      showToast(`Exported CBT Regulatory Monitoring Report in ${format} format successfully.`);
    }, 600);
  };

  return (
    <div className="space-y-6">
      {/* Toast Alert */}
      {toastMessage && (
        <div className="p-4 rounded-xl bg-cyan-50 dark:bg-cyan-950/40 border border-cyan-300 dark:border-cyan-800 text-cyan-900 dark:text-cyan-200 text-xs font-semibold flex items-center gap-3 shadow-xs animate-fade-in">
          <CheckCircle2 className="h-5 w-5 text-cyan-600 shrink-0" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* 1. Header Banner */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <FileText className="h-7 w-7 text-cyan-600 dark:text-cyan-400" />
            CBT Executive Reports & Regulatory Audit Studio
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Multi-dimensional audits: Attendance & absentees, center lab utilizations, invigilator duty rosters, IRT item discrimination, system concurrency, and security logs.
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          <button
            onClick={() => handleExport("PDF")}
            disabled={isExporting}
            className="px-4 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-semibold text-xs tracking-wide shadow-md transition flex items-center gap-2 disabled:opacity-50"
          >
            <Download className="h-4 w-4" />
            Export Audit (PDF)
          </button>
          <button
            onClick={() => handleExport("CSV")}
            disabled={isExporting}
            className="px-3.5 py-2 rounded-xl border border-slate-300 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 font-semibold text-xs transition flex items-center gap-1.5 disabled:opacity-50"
          >
            <Download className="h-4 w-4" /> Export CSV
          </button>
        </div>
      </div>

      {/* 2. Top Navigation Tabs */}
      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-2 shadow-xs flex flex-wrap items-center justify-between gap-2">
        <div className="flex flex-wrap items-center gap-1">
          <button
            onClick={() => setActiveTab("ATTENDANCE")}
            className={`px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              activeTab === "ATTENDANCE"
                ? "bg-cyan-600 text-white shadow-xs"
                : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700/50"
            }`}
          >
            <Users className="h-4 w-4" /> Attendance & Absentees
          </button>

          <button
            onClick={() => setActiveTab("CENTERS")}
            className={`px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              activeTab === "CENTERS"
                ? "bg-cyan-600 text-white shadow-xs"
                : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700/50"
            }`}
          >
            <Building2 className="h-4 w-4" /> Centers & Labs
          </button>

          <button
            onClick={() => setActiveTab("INVIGILATORS")}
            className={`px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              activeTab === "INVIGILATORS"
                ? "bg-cyan-600 text-white shadow-xs"
                : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700/50"
            }`}
          >
            <UserCheck className="h-4 w-4" /> Invigilator Duty Roster
          </button>

          <button
            onClick={() => setActiveTab("QUESTIONS")}
            className={`px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              activeTab === "QUESTIONS"
                ? "bg-cyan-600 text-white shadow-xs"
                : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700/50"
            }`}
          >
            <HelpCircle className="h-4 w-4" /> Question IRT Audit
          </button>

          <button
            onClick={() => setActiveTab("SYSTEM")}
            className={`px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              activeTab === "SYSTEM"
                ? "bg-cyan-600 text-white shadow-xs"
                : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700/50"
            }`}
          >
            <Activity className="h-4 w-4" /> System Telemetry
          </button>

          <button
            onClick={() => setActiveTab("SECURITY")}
            className={`px-3.5 py-2 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              activeTab === "SECURITY"
                ? "bg-cyan-600 text-white shadow-xs"
                : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700/50"
            }`}
          >
            <ShieldAlert className="h-4 w-4" /> Security & Violations
          </button>
        </div>
      </div>

      {/* 3. TAB 1: ATTENDANCE & ABSENTEES */}
      {activeTab === "ATTENDANCE" && (
        <div className="space-y-4">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Registered Candidates</span>
              <p className="mt-2 text-2xl font-bold text-slate-900 dark:text-white">7</p>
              <p className="mt-1 text-xs text-slate-500">Shift 1 • Morning Batch</p>
            </div>

            <div className="rounded-xl border border-emerald-200 dark:border-emerald-900/50 bg-white dark:bg-slate-800 p-5 shadow-xs">
              <span className="text-xs font-semibold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">Present (Appeared)</span>
              <p className="mt-2 text-2xl font-bold text-emerald-600 dark:text-emerald-400">6</p>
              <p className="mt-1 text-xs text-slate-500">85.7% Attendance Rate</p>
            </div>

            <div className="rounded-xl border border-rose-200 dark:border-rose-900/50 bg-white dark:bg-slate-800 p-5 shadow-xs">
              <span className="text-xs font-semibold uppercase tracking-wider text-rose-600 dark:text-rose-400">Absentees (No Show)</span>
              <p className="mt-2 text-2xl font-bold text-rose-600 dark:text-rose-400">1</p>
              <p className="mt-1 text-xs text-slate-500">Gate Closed at 09:15 AM</p>
            </div>

            <div className="rounded-xl border border-cyan-200 dark:border-cyan-900/50 bg-white dark:bg-slate-800 p-5 shadow-xs">
              <span className="text-xs font-semibold uppercase tracking-wider text-cyan-600 dark:text-cyan-400">Biometric Verification</span>
              <p className="mt-2 text-2xl font-bold text-cyan-600 dark:text-cyan-400">100%</p>
              <p className="mt-1 text-xs text-slate-500">UIDAI / Aadhaar matched</p>
            </div>
          </div>

          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 shadow-xs overflow-hidden">
            <div className="px-6 py-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
              <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <Users className="h-5 w-5 text-cyan-600" /> Candidate Attendance & Gate Log
              </h2>
              <span className="text-xs text-slate-500 font-mono">Shift 1 (08:30 - 09:15 AM Entry)</span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 dark:bg-slate-900/60 text-slate-600 dark:text-slate-400 uppercase font-bold tracking-wider border-b border-slate-200 dark:border-slate-800">
                  <tr>
                    <th className="py-3 px-4">Candidate Name</th>
                    <th className="py-3 px-4">Roll Number</th>
                    <th className="py-3 px-4">Center / Lab</th>
                    <th className="py-3 px-4 text-center">Terminal</th>
                    <th className="py-3 px-4 text-center">Reporting Time</th>
                    <th className="py-3 px-4 text-center">Biometric Status</th>
                    <th className="py-3 px-4 text-center">Attendance</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                  {attendanceList.map((row) => (
                    <tr key={row.id} className="hover:bg-slate-50/60 dark:hover:bg-slate-900/30 transition">
                      <td className="py-3.5 px-4 font-bold text-slate-900 dark:text-white">{row.name}</td>
                      <td className="py-3.5 px-4 font-mono text-slate-500">{row.roll}</td>
                      <td className="py-3.5 px-4 text-slate-600 dark:text-slate-300">{row.center} • {row.lab}</td>
                      <td className="py-3.5 px-4 text-center font-mono font-bold text-cyan-600">{row.seat}</td>
                      <td className="py-3.5 px-4 text-center font-mono text-slate-500">{row.time}</td>
                      <td className="py-3.5 px-4 text-center">
                        {row.biometric ? (
                          <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-emerald-600">
                            <CheckCircle2 className="h-3.5 w-3.5" /> Verified
                          </span>
                        ) : (
                          <span className="text-slate-400 text-[11px]">Pending</span>
                        )}
                      </td>
                      <td className="py-3.5 px-4 text-center">
                        <span
                          className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider ${
                            row.status === "PRESENT"
                              ? "bg-emerald-500/10 text-emerald-600 border border-emerald-500/30"
                              : "bg-rose-500/10 text-rose-600 border border-rose-500/30"
                          }`}
                        >
                          {row.status}
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

      {/* 4. TAB 2: CENTERS & COMPUTER LABS */}
      {activeTab === "CENTERS" && (
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 shadow-xs overflow-hidden p-6 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
            <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <Building2 className="h-5 w-5 text-cyan-600" /> Testing Center Facility Occupancy
            </h2>
            <span className="text-xs text-slate-500 font-mono">Center Code: TC-IND-01</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 dark:bg-slate-900/60 text-slate-600 dark:text-slate-400 uppercase font-bold tracking-wider border-b border-slate-200 dark:border-slate-800">
                <tr>
                  <th className="py-3 px-4">Computer Lab</th>
                  <th className="py-3 px-4">Floor</th>
                  <th className="py-3 px-4 text-center">Total Terminals</th>
                  <th className="py-3 px-4 text-center">Allocated Workstations</th>
                  <th className="py-3 px-4 text-center">10% Reserve Buffer</th>
                  <th className="py-3 px-4 text-center">Occupancy Rate</th>
                  <th className="py-3 px-4">LAN Delivery Server</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800 font-mono">
                {labsOccupancy.map((l) => (
                  <tr key={l.lab} className="hover:bg-slate-50/60 dark:hover:bg-slate-900/30 transition">
                    <td className="py-3.5 px-4 font-sans font-bold text-slate-900 dark:text-white">{l.lab}</td>
                    <td className="py-3.5 px-4 font-sans text-slate-500">{l.floor}</td>
                    <td className="py-3.5 px-4 text-center font-bold">{l.total}</td>
                    <td className="py-3.5 px-4 text-center font-bold text-cyan-600">{l.occupied}</td>
                    <td className="py-3.5 px-4 text-center text-amber-600 font-bold">{l.buffer}</td>
                    <td className="py-3.5 px-4 text-center font-bold text-emerald-600">{l.allocPct}%</td>
                    <td className="py-3.5 px-4 font-sans text-slate-600 dark:text-slate-300">
                      <span className="flex items-center gap-1.5">
                        <span className="h-2 w-2 rounded-full bg-emerald-500" /> {l.lanStatus}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* 5. TAB 3: INVIGILATOR DUTY ROSTER */}
      {activeTab === "INVIGILATORS" && (
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 shadow-xs overflow-hidden p-6 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
            <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <UserCheck className="h-5 w-5 text-indigo-600" /> Center Supervisory & Invigilation Duty Roster
            </h2>
            <span className="text-xs text-slate-500 font-mono">Date: 10 Nov 2026</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 dark:bg-slate-900/60 text-slate-600 dark:text-slate-400 uppercase font-bold tracking-wider border-b border-slate-200 dark:border-slate-800">
                <tr>
                  <th className="py-3 px-4">Invigilator / Supervisor</th>
                  <th className="py-3 px-4">Duty Role</th>
                  <th className="py-3 px-4">Assigned Venue</th>
                  <th className="py-3 px-4 text-center">Shift</th>
                  <th className="py-3 px-4 text-center">Duty Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                {invigilators.map((inv) => (
                  <tr key={inv.name} className="hover:bg-slate-50/60 dark:hover:bg-slate-900/30 transition">
                    <td className="py-3.5 px-4 font-bold text-slate-900 dark:text-white">{inv.name}</td>
                    <td className="py-3.5 px-4">
                      <span className="px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 font-mono text-[11px] font-bold">
                        {inv.role.replace("_", " ")}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-slate-600 dark:text-slate-300">{inv.center} • {inv.lab}</td>
                    <td className="py-3.5 px-4 text-center font-mono">{inv.shift}</td>
                    <td className="py-3.5 px-4 text-center">
                      <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 border border-emerald-500/30 font-bold text-[10px]">
                        {inv.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* 6. TAB 4: QUESTION IRT AUDIT */}
      {activeTab === "QUESTIONS" && (
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 shadow-xs overflow-hidden p-6 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
            <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <HelpCircle className="h-5 w-5 text-cyan-600" /> Item Response Theory (IRT) Question Discrimination Audit
            </h2>
            <span className="text-xs text-slate-500 font-mono">P-Value (Difficulty) • D-Value (Discrimination)</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 dark:bg-slate-900/60 text-slate-600 dark:text-slate-400 uppercase font-bold tracking-wider border-b border-slate-200 dark:border-slate-800">
                <tr>
                  <th className="py-3 px-4 text-center">Q#</th>
                  <th className="py-3 px-4">Curricular Section</th>
                  <th className="py-3 px-4 text-center">Difficulty (P)</th>
                  <th className="py-3 px-4 text-center">Discrimination (D)</th>
                  <th className="py-3 px-4 text-center">Attempts</th>
                  <th className="py-3 px-4 text-center">Accuracy %</th>
                  <th className="py-3 px-4">Distracter Diagnostic</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800 font-mono">
                {questionsAudit.map((q) => (
                  <tr key={q.number} className="hover:bg-slate-50/60 dark:hover:bg-slate-900/30 transition">
                    <td className="py-3.5 px-4 text-center font-bold text-cyan-600">#{q.number}</td>
                    <td className="py-3.5 px-4 font-sans text-slate-800 dark:text-slate-200">{q.section}</td>
                    <td className="py-3.5 px-4 text-center font-bold text-slate-700 dark:text-slate-300">{q.pValue.toFixed(2)}</td>
                    <td className="py-3.5 px-4 text-center font-bold text-indigo-600">{q.dValue.toFixed(2)}</td>
                    <td className="py-3.5 px-4 text-center text-slate-500">{q.attempts}</td>
                    <td className="py-3.5 px-4 text-center text-emerald-600 font-bold">{q.acc}%</td>
                    <td className="py-3.5 px-4 font-sans text-[11px] text-slate-600 dark:text-slate-400">{q.note}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* 7. TAB 5: SYSTEM TELEMETRY */}
      {activeTab === "SYSTEM" && (
        <div className="space-y-6">
          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs space-y-4">
            <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2 pb-3 border-b border-slate-100 dark:border-slate-800">
              <Activity className="h-5 w-5 text-cyan-600" /> Center Hardware & Concurrency Telemetry
            </h2>

            <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
              <div className="p-4 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/60">
                <span className="text-xs text-slate-500 block uppercase font-bold">Peak Active Concurrency</span>
                <p className="mt-2 text-2xl font-bold text-slate-900 dark:text-white font-mono">{telemetry.peakConcurrency} Terminals</p>
                <p className="mt-1 text-xs text-slate-500">Smooth high-concurrency delivery</p>
              </div>

              <div className="p-4 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/60">
                <span className="text-xs text-slate-500 block uppercase font-bold">LAN Latency</span>
                <p className="mt-2 text-2xl font-bold text-emerald-600 font-mono">{telemetry.avgLatency}</p>
                <p className="mt-1 text-xs text-slate-500">Zero jitter on local switch core</p>
              </div>

              <div className="p-4 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/60">
                <span className="text-xs text-slate-500 block uppercase font-bold">NTP Time Drift</span>
                <p className="mt-2 text-2xl font-bold text-indigo-600 font-mono">{telemetry.ntpDrift}</p>
                <p className="mt-1 text-xs text-slate-500">Tolerance limit: 50 ms</p>
              </div>

              <div className="p-4 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/60">
                <span className="text-xs text-slate-500 block uppercase font-bold">Packet Loss</span>
                <p className="mt-2 text-2xl font-bold text-emerald-600 font-mono">{telemetry.packetLoss}</p>
                <p className="mt-1 text-xs text-slate-500">Redundant CAT6A LAN drops</p>
              </div>

              <div className="p-4 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/60">
                <span className="text-xs text-slate-500 block uppercase font-bold">Bandwidth Consumed</span>
                <p className="mt-2 text-2xl font-bold text-cyan-600 font-mono">{telemetry.bandwidthConsumed}</p>
                <p className="mt-1 text-xs text-slate-500">Encrypted question packets</p>
              </div>

              <div className="p-4 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/60">
                <span className="text-xs text-slate-500 block uppercase font-bold">Platform Uptime</span>
                <p className="mt-2 text-2xl font-bold text-emerald-600 font-mono">{telemetry.uptime}</p>
                <p className="mt-1 text-xs text-slate-500">Zero unscheduled outages</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 8. TAB 6: SECURITY & INCIDENT AUDIT */}
      {activeTab === "SECURITY" && (
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 shadow-xs overflow-hidden p-6 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
            <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <ShieldAlert className="h-5 w-5 text-rose-500" /> Candidate Security Violations & Proctor Interventions Audit
            </h2>
            <span className="px-2.5 py-0.5 rounded-full bg-rose-500/10 text-rose-600 border border-rose-500/30 text-xs font-bold font-mono">
              4 Violations • 1 Disqualification
            </span>
          </div>

          <div className="space-y-3">
            {securityLog.map((sec, idx) => (
              <div
                key={idx}
                className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/40 flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-mono font-bold text-slate-900 dark:text-white">{sec.candidate}</span>
                    <span className="font-mono text-cyan-600 font-semibold">[{sec.terminal}]</span>
                    <span className="text-[10px] text-slate-400 font-mono">{sec.time}</span>
                  </div>
                  <div className="text-slate-600 dark:text-slate-400">
                    Event: <strong className="text-slate-800 dark:text-slate-200">{sec.event}</strong> • Action: <span className="text-rose-600 font-semibold">{sec.action}</span>
                  </div>
                </div>

                <span
                  className={`px-2.5 py-1 rounded text-[10px] font-bold border uppercase shrink-0 ${
                    sec.severity === "CRITICAL"
                      ? "bg-rose-500/20 text-rose-600 border-rose-400"
                      : sec.severity === "HIGH"
                      ? "bg-orange-500/20 text-orange-600 border-orange-400"
                      : "bg-amber-500/20 text-amber-600 border-amber-400"
                  }`}
                >
                  {sec.severity}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
