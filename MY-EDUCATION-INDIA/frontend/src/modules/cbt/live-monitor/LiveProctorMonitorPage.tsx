import React, { useState, useEffect, useMemo } from "react";
import { Link } from "react-router-dom";
import {
  ShieldAlert,
  ShieldCheck,
  Play,
  Pause,
  AlertTriangle,
  RotateCcw,
  UserX,
  Send,
  Camera,
  Monitor,
  Eye,
  Filter,
  Search,
  Bell,
  CheckCircle2,
  XCircle,
  Activity,
  Layers,
  Building2,
  Laptop,
  X,
  Radio,
} from "lucide-react";

interface ProctorCandidate {
  id: string;
  name: string;
  rollNumber: string;
  terminalId: string;
  labName: string;
  currentQuestion: number;
  answeredCount: number;
  totalQuestions: number;
  timeRemaining: string;
  warningsCount: number;
  proctorStatus: "NORMAL" | "WARNING" | "UNDER_SCRUTINY" | "DISQUALIFIED";
  isPaused: boolean;
  webcamStatus: "VERIFIED" | "SUSPICIOUS" | "DISCONNECTED";
  lastIncident?: string;
  ipAddress: string;
}

interface IncidentEvent {
  id: string;
  time: string;
  terminalId: string;
  candidateName: string;
  type: string;
  severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  details: string;
}

export const LiveProctorMonitorPage: React.FC = () => {
  // Center & Lab Selection
  const [selectedCenter, setSelectedCenter] = useState<string>("TC-IND-01");
  const [selectedLab, setSelectedLab] = useState<string>("LAB-01");
  const [statusFilter, setStatusFilter] = useState<string>("ALL");
  const [searchQuery, setSearchQuery] = useState<string>("");

  // Modals
  const [selectedCandidate, setSelectedCandidate] = useState<ProctorCandidate | null>(null);
  const [isWarningModalOpen, setIsWarningModalOpen] = useState<boolean>(false);
  const [isDisqualifyModalOpen, setIsDisqualifyModalOpen] = useState<boolean>(false);
  const [isTelemetryModalOpen, setIsTelemetryModalOpen] = useState<boolean>(false);
  const [warningMessage, setWarningMessage] = useState<string>("Navigating away from the examination window is strictly forbidden.");
  const [disqualifyReason, setDisqualifyReason] = useState<string>("Repeated unauthorized tab navigation and clipboard violations.");

  // Candidates Surveillance Matrix
  const [candidates, setCandidates] = useState<ProctorCandidate[]>([
    {
      id: "cand-1",
      name: "Aarav Sharma",
      rollNumber: "MEI-2026-84920",
      terminalId: "LAB1-WS-42",
      labName: "Computer Lab 01",
      currentQuestion: 4,
      answeredCount: 3,
      totalQuestions: 20,
      timeRemaining: "02:44:18",
      warningsCount: 0,
      proctorStatus: "NORMAL",
      isPaused: false,
      webcamStatus: "VERIFIED",
      ipAddress: "192.168.10.42",
    },
    {
      id: "cand-2",
      name: "Ananya Patel",
      rollNumber: "MEI-2026-84921",
      terminalId: "LAB1-WS-43",
      labName: "Computer Lab 01",
      currentQuestion: 5,
      answeredCount: 4,
      totalQuestions: 20,
      timeRemaining: "02:41:05",
      warningsCount: 1,
      proctorStatus: "WARNING",
      isPaused: false,
      webcamStatus: "VERIFIED",
      lastIncident: "Tab switch detected (1/3)",
      ipAddress: "192.168.10.43",
    },
    {
      id: "cand-3",
      name: "Rohan Gupta",
      rollNumber: "MEI-2026-84922",
      terminalId: "LAB1-WS-44",
      labName: "Computer Lab 01",
      currentQuestion: 2,
      answeredCount: 1,
      totalQuestions: 20,
      timeRemaining: "02:46:50",
      warningsCount: 0,
      proctorStatus: "NORMAL",
      isPaused: false,
      webcamStatus: "VERIFIED",
      ipAddress: "192.168.10.44",
    },
    {
      id: "cand-4",
      name: "Ishita Verma",
      rollNumber: "MEI-2026-84923",
      terminalId: "LAB1-WS-45",
      labName: "Computer Lab 01",
      currentQuestion: 6,
      answeredCount: 5,
      totalQuestions: 20,
      timeRemaining: "02:38:12",
      warningsCount: 2,
      proctorStatus: "UNDER_SCRUTINY",
      isPaused: false,
      webcamStatus: "SUSPICIOUS",
      lastIncident: "Clipboard copy attempt (2/3)",
      ipAddress: "192.168.10.45",
    },
    {
      id: "cand-5",
      name: "Kabir Joshi",
      rollNumber: "MEI-2026-84924",
      terminalId: "LAB1-WS-46",
      labName: "Computer Lab 01",
      currentQuestion: 1,
      answeredCount: 0,
      totalQuestions: 20,
      timeRemaining: "00:00:00",
      warningsCount: 3,
      proctorStatus: "DISQUALIFIED",
      isPaused: true,
      webcamStatus: "DISCONNECTED",
      lastIncident: "Automatic strike threshold exceeded (3/3)",
      ipAddress: "192.168.10.46",
    },
    {
      id: "cand-6",
      name: "Sneha Reddy",
      rollNumber: "MEI-2026-84925",
      terminalId: "LAB1-WS-47",
      labName: "Computer Lab 01",
      currentQuestion: 8,
      answeredCount: 7,
      totalQuestions: 20,
      timeRemaining: "02:35:40",
      warningsCount: 0,
      proctorStatus: "NORMAL",
      isPaused: false,
      webcamStatus: "VERIFIED",
      ipAddress: "192.168.10.47",
    },
  ]);

  // Real-Time Incident Stream
  const [incidents, setIncidents] = useState<IncidentEvent[]>([
    {
      id: "inc-1",
      time: "13:42:15",
      terminalId: "LAB1-WS-46",
      candidateName: "Kabir Joshi",
      type: "FULLSCREEN_EXIT",
      severity: "CRITICAL",
      details: "Repeatedly exited fullscreen window (Strike 3/3 - Disqualified).",
    },
    {
      id: "inc-2",
      time: "13:38:02",
      terminalId: "LAB1-WS-45",
      candidateName: "Ishita Verma",
      type: "CLIPBOARD_COPY",
      severity: "HIGH",
      details: "Attempted keyboard shortcut copy on Question 6.",
    },
    {
      id: "inc-3",
      time: "13:31:40",
      terminalId: "LAB1-WS-43",
      candidateName: "Ananya Patel",
      type: "TAB_SWITCH",
      severity: "MEDIUM",
      details: "Browser visibility change detected. Warning 1/3 dispatched.",
    },
    {
      id: "inc-4",
      time: "13:20:10",
      terminalId: "LAB1-WS-46",
      candidateName: "Kabir Joshi",
      type: "RIGHT_CLICK",
      severity: "LOW",
      details: "Context menu right-click blocked by client security hook.",
    },
  ]);

  // Auto-refresh simulation
  const [lastRefreshed, setLastRefreshed] = useState<string>("Just now");
  useEffect(() => {
    const timer = setInterval(() => {
      setLastRefreshed(new Date().toLocaleTimeString());
    }, 4000);
    return () => clearInterval(timer);
  }, []);

  // Filtered candidate list
  const filteredCandidates = useMemo(() => {
    return candidates.filter((c) => {
      const matchSearch =
        c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        c.rollNumber.toLowerCase().includes(searchQuery.toLowerCase()) ||
        c.terminalId.toLowerCase().includes(searchQuery.toLowerCase());

      const matchStatus = statusFilter === "ALL" || c.proctorStatus === statusFilter;
      return matchSearch && matchStatus;
    });
  }, [candidates, searchQuery, statusFilter]);

  // Summary counts
  const summary = useMemo(() => {
    const normal = candidates.filter((c) => c.proctorStatus === "NORMAL").length;
    const warning = candidates.filter((c) => c.proctorStatus === "WARNING" || c.proctorStatus === "UNDER_SCRUTINY").length;
    const disqualified = candidates.filter((c) => c.proctorStatus === "DISQUALIFIED").length;
    return {
      total: candidates.length,
      normal,
      warning,
      disqualified,
    };
  }, [candidates]);

  // Actions
  const handleOpenWarning = (cand: ProctorCandidate) => {
    setSelectedCandidate(cand);
    setIsWarningModalOpen(true);
  };

  const handleSendWarning = () => {
    if (!selectedCandidate) return;
    setCandidates((prev) =>
      prev.map((c) => {
        if (c.id === selectedCandidate.id) {
          const newWarn = c.warningsCount + 1;
          const newStatus = newWarn >= 3 ? "DISQUALIFIED" : "WARNING";
          return {
            ...c,
            warningsCount: newWarn,
            proctorStatus: newStatus,
            lastIncident: `Proctor warning: ${warningMessage}`,
          };
        }
        return c;
      })
    );

    // Append to incident feed
    setIncidents((prev) => [
      {
        id: `inc-${Date.now()}`,
        time: new Date().toLocaleTimeString(),
        terminalId: selectedCandidate.terminalId,
        candidateName: selectedCandidate.name,
        type: "PROCTOR_BROADCAST_WARNING",
        severity: "HIGH",
        details: warningMessage,
      },
      ...prev,
    ]);

    setIsWarningModalOpen(false);
  };

  const handleOpenDisqualify = (cand: ProctorCandidate) => {
    setSelectedCandidate(cand);
    setIsDisqualifyModalOpen(true);
  };

  const handleConfirmDisqualify = () => {
    if (!selectedCandidate) return;
    setCandidates((prev) =>
      prev.map((c) => {
        if (c.id === selectedCandidate.id) {
          return {
            ...c,
            warningsCount: 3,
            proctorStatus: "DISQUALIFIED",
            timeRemaining: "00:00:00",
            isPaused: true,
            lastIncident: `Disqualified by Proctor: ${disqualifyReason}`,
          };
        }
        return c;
      })
    );

    setIncidents((prev) => [
      {
        id: `inc-${Date.now()}`,
        time: new Date().toLocaleTimeString(),
        terminalId: selectedCandidate.terminalId,
        candidateName: selectedCandidate.name,
        type: "FORCE_DISQUALIFICATION",
        severity: "CRITICAL",
        details: disqualifyReason,
      },
      ...prev,
    ]);

    setIsDisqualifyModalOpen(false);
  };

  const handleTogglePause = (candId: string) => {
    setCandidates((prev) =>
      prev.map((c) => {
        if (c.id === candId) {
          return {
            ...c,
            isPaused: !c.isPaused,
          };
        }
        return c;
      })
    );
  };

  return (
    <div className="space-y-6">
      {/* 1. Header Banner */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <ShieldAlert className="h-7 w-7 text-cyan-600 dark:text-cyan-400" />
            Live CBT Proctoring & Candidate Surveillance Center
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Real-time terminal telemetry, full-screen lock enforcement, tab-switch strikes, and live supervisor interventions.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 text-xs font-semibold text-emerald-700 dark:text-emerald-300">
            <Radio className="h-4 w-4 animate-pulse text-emerald-600 dark:text-emerald-400" />
            <span>Telemetry Stream Active</span>
          </div>
          <Link
            to="/admin/cbt/live"
            className="px-3.5 py-1.5 rounded-lg border border-slate-300 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-xs font-semibold text-slate-700 dark:text-slate-200 transition"
          >
            Launch Candidate Demo
          </Link>
        </div>
      </div>

      {/* 2. Overview Metrics Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Active Terminals</span>
            <Laptop className="h-5 w-5 text-cyan-600 dark:text-cyan-400" />
          </div>
          <p className="mt-3 text-2xl font-bold text-slate-900 dark:text-white">{summary.total}</p>
          <p className="mt-1 text-xs text-slate-500">Lab 01 • High-speed LAN synced</p>
        </div>

        <div className="rounded-xl border border-emerald-200 dark:border-emerald-900/50 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">
              Clean Integrity
            </span>
            <CheckCircle2 className="h-5 w-5 text-emerald-600" />
          </div>
          <p className="mt-3 text-2xl font-bold text-emerald-600 dark:text-emerald-400">{summary.normal}</p>
          <p className="mt-1 text-xs text-slate-500">Zero security violations</p>
        </div>

        <div className="rounded-xl border border-amber-200 dark:border-amber-900/50 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-amber-600 dark:text-amber-400">
              Flagged with Strikes
            </span>
            <AlertTriangle className="h-5 w-5 text-amber-600" />
          </div>
          <p className="mt-3 text-2xl font-bold text-amber-600 dark:text-amber-400">{summary.warning}</p>
          <p className="mt-1 text-xs text-slate-500">1 to 2 strikes issued</p>
        </div>

        <div className="rounded-xl border border-rose-200 dark:border-rose-900/50 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-rose-600 dark:text-rose-400">
              Terminated / Disqualified
            </span>
            <UserX className="h-5 w-5 text-rose-600" />
          </div>
          <p className="mt-3 text-2xl font-bold text-rose-600 dark:text-rose-400">{summary.disqualified}</p>
          <p className="mt-1 text-xs text-slate-500">3-strike auto-lockouts</p>
        </div>
      </div>

      {/* 3. Filter Bar & Center Switcher */}
      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-4 shadow-xs flex flex-wrap items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-2">
            <Building2 className="h-4 w-4 text-slate-500" />
            <select
              value={selectedCenter}
              onChange={(e) => setSelectedCenter(e.target.value)}
              className="text-xs font-semibold rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 py-1.5 text-slate-800 dark:text-slate-200"
            >
              <option value="TC-IND-01">Indore Campus (TC-IND-01)</option>
              <option value="TC-BPL-02">Bhopal Hub (TC-BPL-02)</option>
            </select>
          </div>

          <div className="flex items-center gap-2">
            <Layers className="h-4 w-4 text-slate-500" />
            <select
              value={selectedLab}
              onChange={(e) => setSelectedLab(e.target.value)}
              className="text-xs font-semibold rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 py-1.5 text-slate-800 dark:text-slate-200"
            >
              <option value="LAB-01">Computer Lab 01 (Terminals 1-50)</option>
              <option value="LAB-02">Computer Lab 02 (Terminals 51-100)</option>
            </select>
          </div>

          <div className="flex items-center gap-1 border-l border-slate-200 dark:border-slate-700 pl-3">
            {["ALL", "NORMAL", "WARNING", "UNDER_SCRUTINY", "DISQUALIFIED"].map((st) => (
              <button
                key={st}
                onClick={() => setStatusFilter(st)}
                className={`px-2.5 py-1 rounded-md text-xs font-medium transition ${
                  statusFilter === st
                    ? "bg-cyan-600 text-white font-semibold"
                    : "hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-400"
                }`}
              >
                {st.replace("_", " ")}
              </button>
            ))}
          </div>
        </div>

        <div className="flex items-center gap-2">
          <div className="relative">
            <Search className="absolute left-2.5 top-2.5 h-3.5 w-3.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search candidate / WS / roll..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-8 pr-3 py-1.5 rounded-lg border border-slate-300 dark:border-slate-700 text-xs bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-200 w-56"
            />
          </div>
        </div>
      </div>

      {/* 4. Split Grid: Workstations Matrix (Left) & Real-Time Incident Feed (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Candidate Terminal Surveillance Cards */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <Laptop className="h-5 w-5 text-cyan-600" /> Workstation Surveillance Grid
            </h2>
            <span className="text-xs text-slate-500 font-mono">
              Showing {filteredCandidates.length} of {candidates.length} terminals
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filteredCandidates.map((cand) => {
              let badgeColor = "bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border-emerald-200 dark:border-emerald-800";
              if (cand.proctorStatus === "WARNING") {
                badgeColor = "bg-amber-500/10 text-amber-700 dark:text-amber-400 border-amber-200 dark:border-amber-800";
              } else if (cand.proctorStatus === "UNDER_SCRUTINY") {
                badgeColor = "bg-orange-500/10 text-orange-700 dark:text-orange-400 border-orange-200 dark:border-orange-800";
              } else if (cand.proctorStatus === "DISQUALIFIED") {
                badgeColor = "bg-rose-500/10 text-rose-700 dark:text-rose-400 border-rose-200 dark:border-rose-800";
              }

              return (
                <div
                  key={cand.id}
                  className={`rounded-xl border p-4 bg-white dark:bg-slate-800/90 shadow-xs flex flex-col justify-between transition ${
                    cand.proctorStatus === "DISQUALIFIED"
                      ? "border-rose-300 dark:border-rose-800/60 bg-rose-50/20"
                      : cand.warningsCount > 0
                      ? "border-amber-300 dark:border-amber-800/60"
                      : "border-slate-200 dark:border-slate-800"
                  }`}
                >
                  <div>
                    {/* Workstation Header */}
                    <div className="flex items-center justify-between pb-2.5 border-b border-slate-100 dark:border-slate-800">
                      <div className="flex items-center gap-2">
                        <span className="px-2 py-0.5 rounded font-mono text-xs font-bold bg-slate-100 dark:bg-slate-700 text-slate-800 dark:text-slate-200">
                          {cand.terminalId}
                        </span>
                        <span className="text-xs text-slate-500 font-mono">{cand.ipAddress}</span>
                      </div>
                      <span className={`px-2 py-0.5 rounded-full border text-[10px] font-bold uppercase tracking-wider ${badgeColor}`}>
                        {cand.proctorStatus.replace("_", " ")}
                      </span>
                    </div>

                    {/* Candidate Details */}
                    <div className="flex items-start gap-3 mt-3">
                      <div className="h-10 w-10 rounded-full bg-cyan-700/20 border border-cyan-500/40 text-cyan-700 dark:text-cyan-300 font-bold flex items-center justify-center text-xs">
                        {cand.name.split(" ").map((n) => n[0]).join("")}
                      </div>
                      <div className="flex-1">
                        <h3 className="text-sm font-bold text-slate-900 dark:text-white leading-tight">
                          {cand.name}
                        </h3>
                        <p className="text-xs text-slate-500 font-mono">{cand.rollNumber}</p>
                      </div>
                    </div>

                    {/* Telemetry Progress */}
                    <div className="grid grid-cols-3 gap-2 mt-3 p-2.5 rounded-lg bg-slate-50 dark:bg-slate-900/60 border border-slate-100 dark:border-slate-800 text-[11px]">
                      <div>
                        <span className="text-slate-500 block">Question</span>
                        <span className="font-bold text-slate-800 dark:text-slate-200">
                          #{cand.currentQuestion} / {cand.totalQuestions}
                        </span>
                      </div>
                      <div>
                        <span className="text-slate-500 block">Attempted</span>
                        <span className="font-bold text-emerald-600 dark:text-emerald-400">
                          {cand.answeredCount} answered
                        </span>
                      </div>
                      <div>
                        <span className="text-slate-500 block">Timer</span>
                        <span className="font-mono font-bold text-cyan-600 dark:text-cyan-400">
                          {cand.timeRemaining}
                        </span>
                      </div>
                    </div>

                    {/* Webcam & Strikes indicator */}
                    <div className="mt-2.5 flex items-center justify-between text-xs">
                      <div className="flex items-center gap-1.5">
                        <Camera className="h-3.5 w-3.5 text-slate-400" />
                        <span className="text-[11px] text-slate-600 dark:text-slate-300">
                          Webcam: <strong className={cand.webcamStatus === "VERIFIED" ? "text-emerald-600" : "text-amber-500"}>{cand.webcamStatus}</strong>
                        </span>
                      </div>
                      <div className="flex items-center gap-1 text-[11px]">
                        <span className="text-slate-500">Strikes:</span>
                        <div className="flex items-center gap-0.5">
                          {[1, 2, 3].map((s) => (
                            <span
                              key={s}
                              className={`h-2.5 w-2.5 rounded-full ${
                                s <= cand.warningsCount
                                  ? "bg-rose-500"
                                  : "bg-slate-200 dark:bg-slate-700"
                              }`}
                            />
                          ))}
                        </div>
                      </div>
                    </div>

                    {cand.lastIncident && (
                      <div className="mt-2 px-2.5 py-1 rounded bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800/50 text-[11px] text-amber-800 dark:text-amber-300">
                        {cand.lastIncident}
                      </div>
                    )}
                  </div>

                  {/* Proctor Intervention Controls */}
                  <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between gap-2">
                    <div className="flex items-center gap-1">
                      <button
                        onClick={() => handleOpenWarning(cand)}
                        disabled={cand.proctorStatus === "DISQUALIFIED"}
                        className="px-2.5 py-1 rounded-md bg-amber-500 hover:bg-amber-400 text-slate-900 font-semibold text-xs transition disabled:opacity-40"
                      >
                        Issue Warning
                      </button>

                      <button
                        onClick={() => handleTogglePause(cand.id)}
                        disabled={cand.proctorStatus === "DISQUALIFIED"}
                        className="p-1 rounded-md border border-slate-300 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 text-xs transition disabled:opacity-40"
                        title={cand.isPaused ? "Resume Candidate" : "Pause Candidate"}
                      >
                        {cand.isPaused ? <Play className="h-3.5 w-3.5 text-emerald-500" /> : <Pause className="h-3.5 w-3.5 text-amber-500" />}
                      </button>
                    </div>

                    <div className="flex items-center gap-1">
                      <button
                        onClick={() => {
                          setSelectedCandidate(cand);
                          setIsTelemetryModalOpen(true);
                        }}
                        className="p-1 rounded-md border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-300 transition"
                        title="View Telemetry"
                      >
                        <Eye className="h-3.5 w-3.5" />
                      </button>

                      <button
                        onClick={() => handleOpenDisqualify(cand)}
                        disabled={cand.proctorStatus === "DISQUALIFIED"}
                        className="p-1 rounded-md bg-rose-50 dark:bg-rose-950/50 hover:bg-rose-100 border border-rose-200 dark:border-rose-800 text-rose-600 text-xs font-semibold transition disabled:opacity-40"
                        title="Force Disqualify"
                      >
                        <UserX className="h-3.5 w-3.5" />
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right: Live Chronological Incident Feed */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <Activity className="h-5 w-5 text-rose-500" /> Security Incident Feed
            </h2>
            <span className="text-xs text-slate-500 font-mono">Real-time</span>
          </div>

          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-4 shadow-xs space-y-3 max-h-[640px] overflow-y-auto">
            {incidents.map((inc) => {
              let sevColor = "bg-slate-100 text-slate-700 border-slate-300";
              if (inc.severity === "CRITICAL") sevColor = "bg-rose-500/20 text-rose-600 border-rose-400";
              else if (inc.severity === "HIGH") sevColor = "bg-orange-500/20 text-orange-600 border-orange-400";
              else if (inc.severity === "MEDIUM") sevColor = "bg-amber-500/20 text-amber-600 border-amber-400";

              return (
                <div
                  key={inc.id}
                  className="p-3 rounded-lg border border-slate-100 dark:border-slate-700/60 bg-slate-50/50 dark:bg-slate-900/50 text-xs space-y-1.5"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-[10px] text-slate-400">{inc.time}</span>
                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold border ${sevColor}`}>
                      {inc.severity}
                    </span>
                  </div>
                  <div className="flex items-center justify-between font-semibold text-slate-800 dark:text-slate-200">
                    <span>{inc.candidateName}</span>
                    <span className="font-mono text-[11px] text-slate-500">{inc.terminalId}</span>
                  </div>
                  <div className="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed">
                    {inc.details}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* 5. Issue Warning Modal */}
      {isWarningModalOpen && selectedCandidate && (
        <div className="fixed inset-0 z-50 bg-slate-950/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl w-full max-w-md p-6 shadow-2xl text-slate-900 dark:text-white">
            <div className="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-800 mb-4">
              <h3 className="font-bold text-base flex items-center gap-2 text-amber-600">
                <AlertTriangle className="h-5 w-5" /> Issue Proctor Warning
              </h3>
              <button
                onClick={() => setIsWarningModalOpen(false)}
                className="text-slate-400 hover:text-white p-1 rounded"
              >
                <X className="h-4 w-4" />
              </button>
            </div>

            <div className="text-xs mb-3 text-slate-600 dark:text-slate-400">
              Broadcasting to <strong>{selectedCandidate.name}</strong> ({selectedCandidate.terminalId}). Current Strikes: <strong>{selectedCandidate.warningsCount}/3</strong>.
            </div>

            <div className="space-y-2 mb-4 text-xs">
              <label className="font-semibold block text-slate-700 dark:text-slate-300">Warning Message:</label>
              <textarea
                rows={3}
                value={warningMessage}
                onChange={(e) => setWarningMessage(e.target.value)}
                className="w-full p-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-950 text-slate-800 dark:text-slate-200 text-xs"
              />
            </div>

            <div className="flex items-center justify-end gap-2">
              <button
                onClick={() => setIsWarningModalOpen(false)}
                className="px-3 py-1.5 rounded-lg border border-slate-300 dark:border-slate-700 text-xs font-semibold"
              >
                Cancel
              </button>
              <button
                onClick={handleSendWarning}
                className="px-4 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-900 text-xs font-bold transition flex items-center gap-1.5"
              >
                <Send className="h-3.5 w-3.5" /> Dispatch Warning
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 6. Force Disqualify Confirmation Modal */}
      {isDisqualifyModalOpen && selectedCandidate && (
        <div className="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl w-full max-w-md p-6 shadow-2xl text-slate-900 dark:text-white">
            <div className="flex items-center gap-3 text-rose-600 mb-4">
              <UserX className="h-6 w-6" />
              <h3 className="font-bold text-base">Confirm Force Disqualification</h3>
            </div>

            <p className="text-xs text-slate-600 dark:text-slate-400 mb-4">
              Are you sure you want to terminate the examination session for <strong>{selectedCandidate.name}</strong> ({selectedCandidate.terminalId})? This action is irreversible and recorded in the audit registry.
            </p>

            <div className="space-y-2 mb-6 text-xs">
              <label className="font-semibold block text-slate-700 dark:text-slate-300">Mandatory Justification Reason:</label>
              <input
                type="text"
                value={disqualifyReason}
                onChange={(e) => setDisqualifyReason(e.target.value)}
                className="w-full p-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-950 text-slate-800 dark:text-slate-200 text-xs"
              />
            </div>

            <div className="flex items-center justify-end gap-2">
              <button
                onClick={() => setIsDisqualifyModalOpen(false)}
                className="px-3 py-1.5 rounded-lg border border-slate-300 dark:border-slate-700 text-xs font-semibold"
              >
                Cancel
              </button>
              <button
                onClick={handleConfirmDisqualify}
                className="px-4 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold transition"
              >
                Yes, Disqualify Candidate
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 7. Candidate Telemetry Snapshot Modal */}
      {isTelemetryModalOpen && selectedCandidate && (
        <div className="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl w-full max-w-lg p-6 shadow-2xl text-slate-900 dark:text-white max-h-[85vh] overflow-y-auto">
            <div className="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-800 mb-4">
              <h3 className="font-bold text-base flex items-center gap-2">
                <Laptop className="h-5 w-5 text-cyan-600" /> Workstation Telemetry & Biometrics
              </h3>
              <button
                onClick={() => setIsTelemetryModalOpen(false)}
                className="text-slate-400 hover:text-white p-1 rounded"
              >
                <X className="h-4 w-4" />
              </button>
            </div>

            <div className="space-y-4 text-xs">
              <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 grid grid-cols-2 gap-3">
                <div>
                  <span className="text-slate-500 block">Candidate</span>
                  <span className="font-bold text-slate-800 dark:text-slate-200">{selectedCandidate.name}</span>
                </div>
                <div>
                  <span className="text-slate-500 block">Roll Number</span>
                  <span className="font-mono text-slate-800 dark:text-slate-200">{selectedCandidate.rollNumber}</span>
                </div>
                <div>
                  <span className="text-slate-500 block">Terminal ID</span>
                  <span className="font-mono text-cyan-600 font-bold">{selectedCandidate.terminalId}</span>
                </div>
                <div>
                  <span className="text-slate-500 block">IP Address</span>
                  <span className="font-mono text-slate-800 dark:text-slate-200">{selectedCandidate.ipAddress}</span>
                </div>
              </div>

              <div className="border border-slate-200 dark:border-slate-800 rounded-lg p-3">
                <h4 className="font-bold mb-2 flex items-center gap-2">
                  <Camera className="h-4 w-4 text-cyan-500" /> AI Face Verification & Webcam Monitor
                </h4>
                <div className="flex items-center gap-4">
                  <div className="h-24 w-24 bg-slate-800 rounded-lg border border-slate-700 flex items-center justify-center text-slate-400 font-mono text-[10px] text-center p-2">
                    Live Feed [Simulated Stream]
                  </div>
                  <div className="space-y-1.5 text-[11px]">
                    <div className="text-emerald-500 font-semibold flex items-center gap-1">
                      <CheckCircle2 className="h-3.5 w-3.5" /> Single Face Matched (Confidence 98.4%)
                    </div>
                    <div className="text-slate-400">Ambient Sound: Low (32 dB)</div>
                    <div className="text-slate-400">Screen Lock Status: Fullscreen Active</div>
                    <div className="text-slate-400">Browser: Chromium Embedded Kiosk Mode</div>
                  </div>
                </div>
              </div>

              <div className="border border-slate-200 dark:border-slate-800 rounded-lg p-3">
                <h4 className="font-bold mb-2">Security Enforcement Checklist</h4>
                <ul className="space-y-1 text-slate-600 dark:text-slate-300">
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" /> Fullscreen Enforcement Active
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" /> Context Menu (Right Click) Disabled
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" /> Clipboard Operations Blocked
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" /> DevTools Shortcuts Locked
                  </li>
                </ul>
              </div>
            </div>

            <div className="mt-6 pt-3 border-t border-slate-200 dark:border-slate-800 text-right">
              <button
                onClick={() => setIsTelemetryModalOpen(false)}
                className="px-4 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold transition"
              >
                Close Telemetry
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
