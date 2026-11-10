import React, { useState, useMemo } from "react";
import { Link } from "react-router-dom";
import {
  TrendingUp,
  Award,
  BarChart2,
  PieChart,
  Clock,
  Target,
  CheckCircle2,
  AlertTriangle,
  Download,
  Filter,
  Search,
  ChevronRight,
  Sparkles,
  BookOpen,
  Brain,
  Sliders,
  Layers,
  ArrowUpRight,
  ArrowDownRight,
  User,
  Zap,
  Activity,
  FileText,
  Share2,
} from "lucide-react";

export const CBTResultsAnalyticsDashboardPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<"SCORECARD" | "COHORT" | "REMEDIATION">("SCORECARD");
  const [selectedCandidateId, setSelectedCandidateId] = useState<string>("cand-2");
  const [selectedSession, setSelectedSession] = useState<string>("CBT-2026-ENG101");
  const [isExporting, setIsExporting] = useState<boolean>(false);
  const [exportNotice, setExportNotice] = useState<string | null>(null);

  // Scorecard Candidate Data
  const scorecard = {
    candidateName: "Aarav Sharma",
    rollNumber: "MEI-2026-84920",
    terminalId: "LAB1-WS-42",
    sessionTitle: "MEI CBT National Entrance Examination 2026",
    examDate: "10 Nov 2026",
    nationalRank: 2,
    totalCandidates: 6,
    percentile: 80.0,
    rawScore: 15.0,
    negativeDeductions: 1.0,
    graceMarks: 0.0,
    finalScore: 15.0,
    maxPossibleScore: 16.0,
    accuracyPercentage: 75.0,
    speedQuestionsPerMinute: 1.15,
    totalTimeSpentMinutes: 24.5,
    isPassed: true,
    resultStatus: "QUALIFIED FOR MERIT SCHOLARSHIP",
  };

  // Subject Performance Breakdown
  const subjects = [
    {
      subjectName: "General Aptitude",
      totalQuestions: 3,
      attempted: 3,
      correct: 3,
      score: 6.0,
      maxScore: 6.0,
      accuracy: 100.0,
      percentile: 95.0,
      color: "bg-emerald-500",
    },
    {
      subjectName: "Computer Science",
      totalQuestions: 3,
      attempted: 3,
      correct: 2,
      score: 3.5,
      maxScore: 6.0,
      accuracy: 66.7,
      percentile: 78.5,
      color: "bg-cyan-500",
    },
    {
      subjectName: "Engineering Mathematics",
      totalQuestions: 2,
      attempted: 2,
      correct: 1,
      score: 1.5,
      maxScore: 4.0,
      accuracy: 50.0,
      percentile: 65.0,
      color: "bg-indigo-500",
    },
  ];

  // Topic Diagnostics
  const topics = [
    {
      topic: "Logical Reasoning & Number Series",
      subject: "General Aptitude",
      mastery: 100.0,
      status: "STRENGTH",
      advice: "Flawless deduction skills; maintain high-tempo practice for upcoming national rounds.",
    },
    {
      topic: "Database Management ACID & Transactions",
      subject: "Computer Science",
      mastery: 100.0,
      status: "STRENGTH",
      advice: "Strong relational schema understanding; explore distributed Raft/Paxos consensus next.",
    },
    {
      topic: "AVL Self-Balancing Trees & Complexity",
      subject: "Computer Science",
      mastery: 100.0,
      status: "STRENGTH",
      advice: "Excellent asymptotic time complexity and tree rotation comprehension.",
    },
    {
      topic: "CPU Process Scheduling Algorithms",
      subject: "Computer Science",
      mastery: 0.0,
      status: "IMPROVEMENT_AREA",
      advice: "Confused non-preemptive SJF and FCFS turnaround metrics. Review Gantt chart assignments.",
    },
    {
      topic: "Matrix Eigenvalues, Trace & Determinants",
      subject: "Engineering Mathematics",
      mastery: 50.0,
      status: "IMPROVEMENT_AREA",
      advice: "Revisit characteristic polynomial factorizations and sum of eigenvalues properties.",
    },
  ];

  // Time Pacing Analysis
  const pacing = {
    avgTimePerQuestion: 52.4, // seconds
    avgTimeCorrect: 46.2,
    avgTimeIncorrect: 68.5,
    paceStatus: "OPTIMAL_PACE",
    rating: "Top 15% Time Efficiency",
    rushedCount: 1,
    lingeredCount: 2,
  };

  // Difficulty Analysis (IRT)
  const difficulty = [
    { level: "EASY", questions: 3, accuracy: 100.0, avgTime: 36.0, discrimination: 0.22 },
    { level: "MODERATE", questions: 3, accuracy: 66.7, avgTime: 54.0, discrimination: 0.45 },
    { level: "HARD", questions: 2, accuracy: 50.0, avgTime: 78.0, discrimination: 0.58 },
  ];

  // Cohort Comparative Stats
  const cohort = {
    totalAppeared: 6,
    meanScore: 12.83,
    medianScore: 13.0,
    standardDeviation: 5.82,
    highestScore: 18.0,
    lowestScore: 0.0,
    p90: 17.5,
    p75: 15.0,
    p50: 13.0,
    bands: [
      { label: "Distinction (16 - 20 pts)", count: 2, percentage: 33.3, color: "bg-emerald-500" },
      { label: "First Class (12 - 15.9 pts)", count: 2, percentage: 33.3, color: "bg-cyan-500" },
      { label: "Pass Class (8 - 11.9 pts)", count: 1, percentage: 16.7, color: "bg-amber-500" },
      { label: "Below Cutoff (< 8 pts)", count: 1, percentage: 16.7, color: "bg-rose-500" },
    ],
  };

  const handleExport = (format: string) => {
    setIsExporting(true);
    setTimeout(() => {
      setIsExporting(false);
      setExportNotice(`Exported official CBT Performance & IRT Analytics report in ${format} format successfully.`);
      setTimeout(() => setExportNotice(null), 5000);
    }, 700);
  };

  return (
    <div className="space-y-6">
      {/* 1. Header Banner */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <TrendingUp className="h-7 w-7 text-cyan-600 dark:text-cyan-400" />
            CBT Results & Comparative Analytics Studio
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Multi-dimensional performance diagnostics: national ranks, percentiles, subject radar metrics, IRT difficulty curves, and curricular remediation pathways.
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          <button
            onClick={() => handleExport("PDF")}
            disabled={isExporting}
            className="px-3.5 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-semibold text-xs tracking-wide shadow-md transition flex items-center gap-1.5 disabled:opacity-50"
          >
            <Download className="h-4 w-4" />
            Export Scorecard (PDF)
          </button>
          <button
            onClick={() => handleExport("CSV")}
            disabled={isExporting}
            className="px-3.5 py-2 rounded-xl border border-slate-300 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-200 font-semibold text-xs transition flex items-center gap-1.5 disabled:opacity-50"
          >
            <FileText className="h-4 w-4" />
            Export CSV
          </button>
        </div>
      </div>

      {/* Export Success Notification */}
      {exportNotice && (
        <div className="p-4 rounded-xl bg-cyan-50 dark:bg-cyan-950/40 border border-cyan-300 dark:border-cyan-800 text-cyan-900 dark:text-cyan-200 text-xs font-medium flex items-center gap-3 animate-fade-in shadow-xs">
          <CheckCircle2 className="h-5 w-5 text-cyan-600 shrink-0" />
          <span>{exportNotice}</span>
        </div>
      )}

      {/* 2. Top Tab Switcher & Candidate Selector */}
      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-3 shadow-xs flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-1">
          <button
            onClick={() => setActiveTab("SCORECARD")}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              activeTab === "SCORECARD"
                ? "bg-cyan-600 text-white shadow-xs"
                : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700/50"
            }`}
          >
            <Award className="h-4 w-4" /> Candidate Scorecard & IRT
          </button>

          <button
            onClick={() => setActiveTab("COHORT")}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              activeTab === "COHORT"
                ? "bg-cyan-600 text-white shadow-xs"
                : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700/50"
            }`}
          >
            <BarChart2 className="h-4 w-4" /> Comparative Cohort Distribution
          </button>

          <button
            onClick={() => setActiveTab("REMEDIATION")}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              activeTab === "REMEDIATION"
                ? "bg-cyan-600 text-white shadow-xs"
                : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700/50"
            }`}
          >
            <Brain className="h-4 w-4" /> Curricular Topic Remediation
          </button>
        </div>

        <div className="flex items-center gap-2">
          <User className="h-4 w-4 text-slate-500" />
          <select
            value={selectedCandidateId}
            onChange={(e) => setSelectedCandidateId(e.target.value)}
            className="text-xs font-semibold rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 py-1.5 text-slate-800 dark:text-slate-200"
          >
            <option value="cand-2">Aarav Sharma (MEI-2026-84920)</option>
            <option value="cand-1">Sneha Reddy (MEI-2026-84925)</option>
            <option value="cand-3">Ananya Patel (MEI-2026-84921)</option>
            <option value="cand-4">Rohan Gupta (MEI-2026-84922)</option>
          </select>
        </div>
      </div>

      {/* 3. TAB 1: INDIVIDUAL CANDIDATE SCORECARD & IRT */}
      {activeTab === "SCORECARD" && (
        <div className="space-y-6">
          {/* Scorecard Hero Cards */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">National Rank</span>
                <Award className="h-5 w-5 text-amber-500" />
              </div>
              <p className="mt-3 text-3xl font-black text-slate-900 dark:text-white">
                #{scorecard.nationalRank} <span className="text-sm font-normal text-slate-500">/ {scorecard.totalCandidates}</span>
              </p>
              <p className="mt-1 text-xs text-emerald-600 font-semibold">Top Tier Standing</p>
            </div>

            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Percentile</span>
                <Target className="h-5 w-5 text-cyan-600 dark:text-cyan-400" />
              </div>
              <p className="mt-3 text-3xl font-black text-cyan-600 dark:text-cyan-400">
                {scorecard.percentile.toFixed(1)}%
              </p>
              <p className="mt-1 text-xs text-slate-500">Better than 80% of test takers</p>
            </div>

            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Final Moderated Score</span>
                <Sparkles className="h-5 w-5 text-indigo-600 dark:text-indigo-400" />
              </div>
              <p className="mt-3 text-3xl font-black text-indigo-600 dark:text-indigo-400">
                {scorecard.finalScore.toFixed(2)} <span className="text-sm font-normal text-slate-500">/ {scorecard.maxPossibleScore.toFixed(1)}</span>
              </p>
              <p className="mt-1 text-xs text-slate-500">Raw: {scorecard.rawScore} • Neg: -{scorecard.negativeDeductions}</p>
            </div>

            <div className="rounded-xl border border-emerald-200 dark:border-emerald-900/50 bg-white dark:bg-slate-800 p-5 shadow-xs">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">Accuracy & Speed</span>
                <Zap className="h-5 w-5 text-emerald-600" />
              </div>
              <p className="mt-3 text-3xl font-black text-emerald-600 dark:text-emerald-400">
                {scorecard.accuracyPercentage}%
              </p>
              <p className="mt-1 text-xs text-slate-500">{scorecard.speedQuestionsPerMinute} Q/min pace</p>
            </div>
          </div>

          {/* Subject-Wise Performance Matrix */}
          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs">
            <h2 className="text-base font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
              <Layers className="h-5 w-5 text-cyan-600" /> Subject-Wise Proficiency Matrix
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {subjects.map((sub) => (
                <div
                  key={sub.subjectName}
                  className="p-4 rounded-xl border border-slate-100 dark:border-slate-700/60 bg-slate-50/60 dark:bg-slate-900/40 space-y-3"
                >
                  <div className="flex items-center justify-between">
                    <h3 className="font-bold text-sm text-slate-900 dark:text-white">{sub.subjectName}</h3>
                    <span className="text-xs font-mono font-bold text-cyan-600">
                      {sub.score.toFixed(1)} / {sub.maxScore.toFixed(1)} pts
                    </span>
                  </div>

                  <div className="space-y-1">
                    <div className="flex items-center justify-between text-xs text-slate-500">
                      <span>Accuracy</span>
                      <span className="font-bold text-slate-700 dark:text-slate-300">{sub.accuracy.toFixed(1)}%</span>
                    </div>
                    <div className="h-2 w-full bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                      <div className={`h-full ${sub.color}`} style={{ width: `${sub.accuracy}%` }} />
                    </div>
                  </div>

                  <div className="flex items-center justify-between text-[11px] text-slate-500 border-t border-slate-200 dark:border-slate-800 pt-2">
                    <span>Subject Percentile:</span>
                    <span className="font-bold text-slate-800 dark:text-slate-200 font-mono">
                      {sub.percentile.toFixed(1)}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Time Pacing & Question Difficulty IRT Analysis */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Time-Spent Pacing Matrix */}
            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                  <Clock className="h-5 w-5 text-indigo-600" /> Candidate Time Pacing Diagnostic
                </h2>
                <span className="px-2.5 py-0.5 rounded-full bg-indigo-50 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800 text-[11px] font-bold">
                  {pacing.rating}
                </span>
              </div>

              <div className="grid grid-cols-3 gap-3 text-center">
                <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900/60 border border-slate-100 dark:border-slate-800">
                  <span className="text-xs text-slate-500 block">Overall Pace</span>
                  <span className="text-lg font-bold text-slate-900 dark:text-white font-mono">
                    {pacing.avgTimePerQuestion}s
                  </span>
                  <span className="text-[10px] text-slate-400 block mt-0.5">per question</span>
                </div>
                <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900/60 border border-slate-100 dark:border-slate-800">
                  <span className="text-xs text-slate-500 block">Correct Qs</span>
                  <span className="text-lg font-bold text-emerald-600 font-mono">
                    {pacing.avgTimeCorrect}s
                  </span>
                  <span className="text-[10px] text-emerald-600/80 block mt-0.5">fluent & decisive</span>
                </div>
                <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900/60 border border-slate-100 dark:border-slate-800">
                  <span className="text-xs text-slate-500 block">Incorrect Qs</span>
                  <span className="text-lg font-bold text-rose-500 font-mono">
                    {pacing.avgTimeIncorrect}s
                  </span>
                  <span className="text-[10px] text-rose-500/80 block mt-0.5">hesitation / linger</span>
                </div>
              </div>

              <div className="text-xs text-slate-600 dark:text-slate-300 bg-slate-50 dark:bg-slate-900/40 p-3 rounded-xl border border-slate-100 dark:border-slate-800 leading-relaxed">
                Candidate demonstrated steady pacing across General Aptitude but hesitated on Matrix Determinants (spent 110s before selecting option).
              </div>
            </div>

            {/* Question Difficulty & IRT Curve */}
            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs space-y-4">
              <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <BarChart2 className="h-5 w-5 text-cyan-600" /> Item Response Theory (IRT) Difficulty Index
              </h2>

              <div className="space-y-3">
                {difficulty.map((d) => (
                  <div key={d.level} className="space-y-1">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-semibold text-slate-700 dark:text-slate-300">
                        {d.level} Questions ({d.questions} items)
                      </span>
                      <span className="font-mono text-slate-500 text-[11px]">
                        Acc: <strong>{d.accuracy}%</strong> • Avg Time: {d.avgTime}s • Discrim (D): {d.discrimination}
                      </span>
                    </div>
                    <div className="h-2 w-full bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                      <div
                        className={`h-full ${
                          d.level === "EASY"
                            ? "bg-emerald-500"
                            : d.level === "MODERATE"
                            ? "bg-cyan-500"
                            : "bg-amber-500"
                        }`}
                        style={{ width: `${d.accuracy}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>

              <p className="text-[11px] text-slate-500">
                Discrimination index above 0.40 indicates high question validity and candidate cohort stratification.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* 4. TAB 2: COMPARATIVE COHORT ANALYTICS */}
      {activeTab === "COHORT" && (
        <div className="space-y-6">
          {/* Cohort Bell Curve Metrics Row */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Mean Cohort Score</span>
              <p className="mt-2 text-2xl font-bold text-slate-900 dark:text-white font-mono">{cohort.meanScore} / 20.0</p>
              <p className="mt-1 text-xs text-slate-500">Standard Dev: {cohort.standardDeviation}</p>
            </div>

            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Median Score</span>
              <p className="mt-2 text-2xl font-bold text-cyan-600 font-mono">{cohort.medianScore} / 20.0</p>
              <p className="mt-1 text-xs text-slate-500">50th Percentile Cutoff</p>
            </div>

            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Top 10% Cutoff (P90)</span>
              <p className="mt-2 text-2xl font-bold text-indigo-600 font-mono">{cohort.p90} / 20.0</p>
              <p className="mt-1 text-xs text-slate-500">Scholarship Eligibility Benchmark</p>
            </div>

            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Score Range</span>
              <p className="mt-2 text-2xl font-bold text-emerald-600 font-mono">
                {cohort.lowestScore} - {cohort.highestScore}
              </p>
              <p className="mt-1 text-xs text-slate-500">Max Score: {cohort.highestScore} pts</p>
            </div>
          </div>

          {/* Frequency Bands Histogram */}
          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs space-y-4">
            <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <BarChart2 className="h-5 w-5 text-cyan-600" /> Gaussian Score Distribution Bands
            </h2>

            <div className="space-y-4">
              {cohort.bands.map((band) => (
                <div key={band.label} className="space-y-1.5">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-slate-700 dark:text-slate-300">{band.label}</span>
                    <span className="font-mono text-slate-600 dark:text-slate-400 font-bold">
                      {band.count} candidates ({band.percentage}%)
                    </span>
                  </div>
                  <div className="h-3 w-full bg-slate-100 dark:bg-slate-700/60 rounded-full overflow-hidden">
                    <div className={`h-full ${band.color}`} style={{ width: `${band.percentage}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* 5. TAB 3: CURRICULAR TOPIC REMEDIATION */}
      {activeTab === "REMEDIATION" && (
        <div className="space-y-6">
          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <Brain className="h-5 w-5 text-indigo-600" /> Topic-Level Strengths & Curricular Action Plan
              </h2>
              <span className="text-xs text-slate-500 font-mono">5 Curricular Domains Tested</span>
            </div>

            <div className="space-y-3">
              {topics.map((t) => (
                <div
                  key={t.topic}
                  className={`p-4 rounded-xl border flex flex-col sm:flex-row sm:items-center justify-between gap-3 ${
                    t.status === "STRENGTH"
                      ? "border-emerald-200 dark:border-emerald-900/40 bg-emerald-50/20"
                      : "border-amber-200 dark:border-amber-900/40 bg-amber-50/20"
                  }`}
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-xs text-slate-900 dark:text-white">{t.topic}</span>
                      <span className="text-[10px] px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 font-semibold text-slate-600 dark:text-slate-400">
                        {t.subject}
                      </span>
                    </div>
                    <p className="text-xs text-slate-600 dark:text-slate-400">{t.advice}</p>
                  </div>

                  <div className="flex items-center gap-3 shrink-0">
                    <div className="text-right">
                      <span className="text-[10px] text-slate-500 block uppercase">Mastery</span>
                      <span
                        className={`text-sm font-bold font-mono ${
                          t.status === "STRENGTH" ? "text-emerald-600" : "text-amber-600"
                        }`}
                      >
                        {t.mastery.toFixed(0)}%
                      </span>
                    </div>
                    <span
                      className={`px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider ${
                        t.status === "STRENGTH"
                          ? "bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/30"
                          : "bg-amber-500/10 text-amber-700 dark:text-amber-400 border border-amber-500/30"
                      }`}
                    >
                      {t.status.replace("_", " ")}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
