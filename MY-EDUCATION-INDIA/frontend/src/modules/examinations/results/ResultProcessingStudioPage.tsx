import React, { useState, useMemo } from "react";
import { Link } from "react-router-dom";
import {
  Calculator,
  Award,
  Trophy,
  GraduationCap,
  Sparkles,
  TrendingUp,
  Percent,
  Sliders,
  CheckCircle2,
  AlertCircle,
  FileText,
  Search,
  Filter,
  Download,
  Share2,
  Send,
  Eye,
  RefreshCw,
  ChevronRight,
  ShieldCheck,
  Check,
  BarChart3,
  Layers,
  ArrowUpRight,
  BookOpen,
} from "lucide-react";

interface CourseGrade {
  courseCode: string;
  courseName: string;
  credits: number;
  maxMarks: number;
  marksObtained: number;
  gradeLetter: string;
  gradePoints: number;
  isPassed: boolean;
}

interface StudentResult {
  id: string;
  rollNumber: string;
  enrollmentNo: string;
  candidateName: string;
  programName: string;
  semesterCode: string;
  gradingSystem: "ABSOLUTE" | "RELATIVE";
  totalCreditsRegistered: number;
  totalCreditsEarned: number;
  totalMarksObtained: number;
  totalMaxMarks: number;
  percentage: number;
  sgpa: number;
  cgpa: number;
  overallGrade: string;
  division: "FIRST_CLASS_DISTINCTION" | "FIRST_CLASS" | "SECOND_CLASS" | "PASS_CLASS" | "FAIL";
  classRank: number;
  resultStatus: "PASSED" | "PROMOTED_WITH_BACKLOG" | "DETAINED";
  isPublished: boolean;
  publishedAt?: string;
  courses: CourseGrade[];
}

const initialCohortResults: StudentResult[] = [
  {
    id: "res-001",
    rollNumber: "MEI2024CS001",
    enrollmentNo: "EN202409001",
    candidateName: "Aarav Sharma",
    programName: "B.Tech Computer Science & Engineering",
    semesterCode: "SEM-5",
    gradingSystem: "ABSOLUTE",
    totalCreditsRegistered: 20.0,
    totalCreditsEarned: 20.0,
    totalMarksObtained: 565.0,
    totalMaxMarks: 600.0,
    percentage: 94.17,
    sgpa: 9.42,
    cgpa: 9.50,
    overallGrade: "O",
    division: "FIRST_CLASS_DISTINCTION",
    classRank: 1,
    resultStatus: "PASSED",
    isPublished: true,
    publishedAt: "2026-11-10T11:30:00Z",
    courses: [
      { courseCode: "CS-501", courseName: "Advanced Operating Systems", credits: 4.0, maxMarks: 100.0, marksObtained: 95.0, gradeLetter: "O", gradePoints: 10.0, isPassed: true },
      { courseCode: "CS-502", courseName: "Database Management Systems", credits: 4.0, maxMarks: 100.0, marksObtained: 92.0, gradeLetter: "O", gradePoints: 10.0, isPassed: true },
      { courseCode: "CS-503", courseName: "Theory of Computation", credits: 4.0, maxMarks: 100.0, marksObtained: 94.0, gradeLetter: "O", gradePoints: 10.0, isPassed: true },
      { courseCode: "CS-504", courseName: "Computer Networks & Security", credits: 4.0, maxMarks: 100.0, marksObtained: 91.0, gradeLetter: "O", gradePoints: 10.0, isPassed: true },
      { courseCode: "CS-505P", courseName: "OS & Networks Lab", credits: 2.0, maxMarks: 50.0, marksObtained: 48.0, gradeLetter: "O", gradePoints: 10.0, isPassed: true },
      { courseCode: "CS-506P", courseName: "DBMS Design Project", credits: 2.0, maxMarks: 50.0, marksObtained: 47.0, gradeLetter: "O", gradePoints: 10.0, isPassed: true },
    ],
  },
  {
    id: "res-002",
    rollNumber: "MEI2024CS002",
    enrollmentNo: "EN202409002",
    candidateName: "Diya Patel",
    programName: "B.Tech Computer Science & Engineering",
    semesterCode: "SEM-5",
    gradingSystem: "ABSOLUTE",
    totalCreditsRegistered: 20.0,
    totalCreditsEarned: 20.0,
    totalMarksObtained: 542.0,
    totalMaxMarks: 600.0,
    percentage: 90.33,
    sgpa: 9.15,
    cgpa: 9.20,
    overallGrade: "O",
    division: "FIRST_CLASS_DISTINCTION",
    classRank: 2,
    resultStatus: "PASSED",
    isPublished: true,
    publishedAt: "2026-11-10T11:30:00Z",
    courses: [
      { courseCode: "CS-501", courseName: "Advanced Operating Systems", credits: 4.0, maxMarks: 100.0, marksObtained: 90.0, gradeLetter: "O", gradePoints: 10.0, isPassed: true },
      { courseCode: "CS-502", courseName: "Database Management Systems", credits: 4.0, maxMarks: 100.0, marksObtained: 88.0, gradeLetter: "A+", gradePoints: 9.0, isPassed: true },
      { courseCode: "CS-503", courseName: "Theory of Computation", credits: 4.0, maxMarks: 100.0, marksObtained: 89.0, gradeLetter: "A+", gradePoints: 9.0, isPassed: true },
      { courseCode: "CS-504", courseName: "Computer Networks & Security", credits: 4.0, maxMarks: 100.0, marksObtained: 92.0, gradeLetter: "O", gradePoints: 10.0, isPassed: true },
      { courseCode: "CS-505P", courseName: "OS & Networks Lab", credits: 2.0, maxMarks: 50.0, marksObtained: 46.0, gradeLetter: "O", gradePoints: 10.0, isPassed: true },
      { courseCode: "CS-506P", courseName: "DBMS Design Project", credits: 2.0, maxMarks: 50.0, marksObtained: 46.0, gradeLetter: "O", gradePoints: 10.0, isPassed: true },
    ],
  },
  {
    id: "res-003",
    rollNumber: "MEI2024CS003",
    enrollmentNo: "EN202409003",
    candidateName: "Rohan Verma",
    programName: "B.Tech Computer Science & Engineering",
    semesterCode: "SEM-5",
    gradingSystem: "ABSOLUTE",
    totalCreditsRegistered: 20.0,
    totalCreditsEarned: 20.0,
    totalMarksObtained: 515.0,
    totalMaxMarks: 600.0,
    percentage: 85.83,
    sgpa: 8.75,
    cgpa: 8.80,
    overallGrade: "A+",
    division: "FIRST_CLASS_DISTINCTION",
    classRank: 3,
    resultStatus: "PASSED",
    isPublished: true,
    publishedAt: "2026-11-10T11:30:00Z",
    courses: [
      { courseCode: "CS-501", courseName: "Advanced Operating Systems", credits: 4.0, maxMarks: 100.0, marksObtained: 85.0, gradeLetter: "A+", gradePoints: 9.0, isPassed: true },
      { courseCode: "CS-502", courseName: "Database Management Systems", credits: 4.0, maxMarks: 100.0, marksObtained: 86.0, gradeLetter: "A+", gradePoints: 9.0, isPassed: true },
      { courseCode: "CS-503", courseName: "Theory of Computation", credits: 4.0, maxMarks: 100.0, marksObtained: 82.0, gradeLetter: "A+", gradePoints: 9.0, isPassed: true },
      { courseCode: "CS-504", courseName: "Computer Networks & Security", credits: 4.0, maxMarks: 100.0, marksObtained: 84.0, gradeLetter: "A+", gradePoints: 9.0, isPassed: true },
      { courseCode: "CS-505P", courseName: "OS & Networks Lab", credits: 2.0, maxMarks: 50.0, marksObtained: 43.0, gradeLetter: "A+", gradePoints: 9.0, isPassed: true },
      { courseCode: "CS-506P", courseName: "DBMS Design Project", credits: 2.0, maxMarks: 50.0, marksObtained: 44.0, gradeLetter: "A+", gradePoints: 9.0, isPassed: true },
    ],
  },
  {
    id: "res-004",
    rollNumber: "MEI2024CS004",
    enrollmentNo: "EN202409004",
    candidateName: "Ananya Iyer",
    programName: "B.Tech Computer Science & Engineering",
    semesterCode: "SEM-5",
    gradingSystem: "ABSOLUTE",
    totalCreditsRegistered: 20.0,
    totalCreditsEarned: 20.0,
    totalMarksObtained: 496.0,
    totalMaxMarks: 600.0,
    percentage: 82.67,
    sgpa: 8.40,
    cgpa: 8.45,
    overallGrade: "A+",
    division: "FIRST_CLASS_DISTINCTION",
    classRank: 4,
    resultStatus: "PASSED",
    isPublished: true,
    publishedAt: "2026-11-10T11:30:00Z",
    courses: [
      { courseCode: "CS-501", courseName: "Advanced Operating Systems", credits: 4.0, maxMarks: 100.0, marksObtained: 81.0, gradeLetter: "A+", gradePoints: 9.0, isPassed: true },
      { courseCode: "CS-502", courseName: "Database Management Systems", credits: 4.0, maxMarks: 100.0, marksObtained: 83.0, gradeLetter: "A+", gradePoints: 9.0, isPassed: true },
      { courseCode: "CS-503", courseName: "Theory of Computation", credits: 4.0, maxMarks: 100.0, marksObtained: 79.0, gradeLetter: "A", gradePoints: 8.0, isPassed: true },
      { courseCode: "CS-504", courseName: "Computer Networks & Security", credits: 4.0, maxMarks: 100.0, marksObtained: 82.0, gradeLetter: "A+", gradePoints: 9.0, isPassed: true },
      { courseCode: "CS-505P", courseName: "OS & Networks Lab", credits: 2.0, maxMarks: 50.0, marksObtained: 42.0, gradeLetter: "A+", gradePoints: 9.0, isPassed: true },
      { courseCode: "CS-506P", courseName: "DBMS Design Project", credits: 2.0, maxMarks: 50.0, marksObtained: 41.0, gradeLetter: "A+", gradePoints: 9.0, isPassed: true },
    ],
  },
  {
    id: "res-005",
    rollNumber: "MEI2024CS005",
    enrollmentNo: "EN202409005",
    candidateName: "Vikram Malhotra",
    programName: "B.Tech Computer Science & Engineering",
    semesterCode: "SEM-5",
    gradingSystem: "ABSOLUTE",
    totalCreditsRegistered: 20.0,
    totalCreditsEarned: 20.0,
    totalMarksObtained: 465.0,
    totalMaxMarks: 600.0,
    percentage: 77.50,
    sgpa: 7.85,
    cgpa: 7.90,
    overallGrade: "A",
    division: "FIRST_CLASS",
    classRank: 5,
    resultStatus: "PASSED",
    isPublished: true,
    publishedAt: "2026-11-10T11:30:00Z",
    courses: [
      { courseCode: "CS-501", courseName: "Advanced Operating Systems", credits: 4.0, maxMarks: 100.0, marksObtained: 76.0, gradeLetter: "A", gradePoints: 8.0, isPassed: true },
      { courseCode: "CS-502", courseName: "Database Management Systems", credits: 4.0, maxMarks: 100.0, marksObtained: 78.0, gradeLetter: "A", gradePoints: 8.0, isPassed: true },
      { courseCode: "CS-503", courseName: "Theory of Computation", credits: 4.0, maxMarks: 100.0, marksObtained: 72.0, gradeLetter: "A", gradePoints: 8.0, isPassed: true },
      { courseCode: "CS-504", courseName: "Computer Networks & Security", credits: 4.0, maxMarks: 100.0, marksObtained: 75.0, gradeLetter: "A", gradePoints: 8.0, isPassed: true },
      { courseCode: "CS-505P", courseName: "OS & Networks Lab", credits: 2.0, maxMarks: 50.0, marksObtained: 38.0, gradeLetter: "A", gradePoints: 8.0, isPassed: true },
      { courseCode: "CS-506P", courseName: "DBMS Design Project", credits: 2.0, maxMarks: 50.0, marksObtained: 39.0, gradeLetter: "A", gradePoints: 8.0, isPassed: true },
    ],
  },
];

export const ResultProcessingStudioPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<"cohort" | "merit" | "transcript" | "statistics">("cohort");
  const [selectedGradingModel, setSelectedGradingModel] = useState<"ABSOLUTE" | "RELATIVE">("ABSOLUTE");
  const [relativeTopPct, setRelativeTopPct] = useState<number>(10.0);
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [selectedStudent, setSelectedStudent] = useState<StudentResult | null>(initialCohortResults[0]);
  const [cohortResults, setCohortResults] = useState<StudentResult[]>(initialCohortResults);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [publishSuccessBanner, setPublishSuccessBanner] = useState<boolean>(false);

  // Recalculate cohort results on grading model change
  const handleRecalculate = (model: "ABSOLUTE" | "RELATIVE") => {
    setIsProcessing(true);
    setTimeout(() => {
      setSelectedGradingModel(model);
      const updated = cohortResults.map((s, idx) => {
        if (model === "RELATIVE") {
          let grade = "A";
          let sgpa = s.sgpa;
          if (idx === 0) { grade = "O"; sgpa = 9.80; }
          else if (idx === 1) { grade = "A+"; sgpa = 9.25; }
          else if (idx === 2) { grade = "A"; sgpa = 8.60; }
          else if (idx === 3) { grade = "B+"; sgpa = 8.10; }
          else { grade = "B"; sgpa = 7.50; }
          return { ...s, gradingSystem: "RELATIVE" as const, overallGrade: grade, sgpa };
        } else {
          // UGC Absolute
          let grade = "A";
          if (s.percentage >= 90) grade = "O";
          else if (s.percentage >= 80) grade = "A+";
          else if (s.percentage >= 70) grade = "A";
          else if (s.percentage >= 60) grade = "B+";
          return { ...s, gradingSystem: "ABSOLUTE" as const, overallGrade: grade };
        }
      });
      setCohortResults(updated);
      if (selectedStudent) {
        setSelectedStudent(updated.find(u => u.rollNumber === selectedStudent.rollNumber) || updated[0]);
      }
      setIsProcessing(false);
    }, 400);
  };

  const handlePublishAll = () => {
    setPublishSuccessBanner(true);
    setTimeout(() => setPublishSuccessBanner(false), 5000);
  };

  const filteredStudents = useMemo(() => {
    return cohortResults.filter(
      (s) =>
        s.candidateName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        s.rollNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
        s.enrollmentNo.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [cohortResults, searchTerm]);

  // Statistics
  const stats = useMemo(() => {
    const total = cohortResults.length;
    const passed = cohortResults.filter((s) => s.resultStatus === "PASSED").length;
    const avgSgpa = (cohortResults.reduce((acc, s) => acc + s.sgpa, 0) / total).toFixed(2);
    const avgCgpa = (cohortResults.reduce((acc, s) => acc + s.cgpa, 0) / total).toFixed(2);
    const passRate = ((passed / total) * 100).toFixed(1);
    const distinctionCount = cohortResults.filter((s) => s.division === "FIRST_CLASS_DISTINCTION").length;
    return { total, passed, avgSgpa, avgCgpa, passRate, distinctionCount };
  }, [cohortResults]);

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-gray-200 dark:border-gray-700 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-100 text-indigo-800 dark:bg-indigo-900/40 dark:text-indigo-300">
              Phase 4 • Module 12
            </span>
            <span className="text-xs text-gray-500 dark:text-gray-400">Autumn Semester 2026-27</span>
          </div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mt-1 flex items-center gap-2">
            <Calculator className="w-7 h-7 text-indigo-600 dark:text-indigo-400" />
            Result Processing Studio & Merit Engine
          </h1>
          <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
            UGC 10-Point Scale & Gaussian Bell Curve Processing, SGPA/CGPA Calculation, Class Rankings & Official Merit List Publication
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handlePublishAll}
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg shadow-sm transition-colors"
          >
            <Send className="w-4 h-4" />
            Publish All Results to Portal
          </button>
          <Link
            to="/exams"
            className="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-200 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-lg transition-colors"
          >
            Examination Hub
            <ChevronRight className="w-4 h-4" />
          </Link>
        </div>
      </div>

      {publishSuccessBanner && (
        <div className="p-4 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            <div>
              <h4 className="text-sm font-semibold text-emerald-900 dark:text-emerald-200">
                Results Published to Student Portal
              </h4>
              <p className="text-xs text-emerald-700 dark:text-emerald-300">
                All 5 student semester result cards and official merit lists have been published and encrypted with COE digital signatures.
              </p>
            </div>
          </div>
          <button
            onClick={() => setPublishSuccessBanner(false)}
            className="text-emerald-600 hover:text-emerald-800 dark:text-emerald-400 text-xs font-semibold"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        <div className="p-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm">
          <div className="flex items-center justify-between text-gray-500 dark:text-gray-400 text-xs">
            <span>Enrolled Batch</span>
            <GraduationCap className="w-4 h-4 text-indigo-500" />
          </div>
          <div className="mt-2 text-2xl font-bold text-gray-900 dark:text-white">{stats.total}</div>
          <div className="text-[11px] text-gray-500 dark:text-gray-400">B.Tech CSE SEM-5</div>
        </div>

        <div className="p-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm">
          <div className="flex items-center justify-between text-gray-500 dark:text-gray-400 text-xs">
            <span>Batch Pass Rate</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-500" />
          </div>
          <div className="mt-2 text-2xl font-bold text-emerald-600 dark:text-emerald-400">{stats.passRate}%</div>
          <div className="text-[11px] text-emerald-600 dark:text-emerald-400">100% Cleared</div>
        </div>

        <div className="p-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm">
          <div className="flex items-center justify-between text-gray-500 dark:text-gray-400 text-xs">
            <span>Class Avg SGPA</span>
            <TrendingUp className="w-4 h-4 text-blue-500" />
          </div>
          <div className="mt-2 text-2xl font-bold text-blue-600 dark:text-blue-400">{stats.avgSgpa}</div>
          <div className="text-[11px] text-gray-500 dark:text-gray-400">On 10.0 UGC Scale</div>
        </div>

        <div className="p-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm">
          <div className="flex items-center justify-between text-gray-500 dark:text-gray-400 text-xs">
            <span>Cumulative CGPA</span>
            <BarChart3 className="w-4 h-4 text-purple-500" />
          </div>
          <div className="mt-2 text-2xl font-bold text-purple-600 dark:text-purple-400">{stats.avgCgpa}</div>
          <div className="text-[11px] text-gray-500 dark:text-gray-400">Semesters 1 to 5</div>
        </div>

        <div className="p-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm">
          <div className="flex items-center justify-between text-gray-500 dark:text-gray-400 text-xs">
            <span>Distinction</span>
            <Award className="w-4 h-4 text-amber-500" />
          </div>
          <div className="mt-2 text-2xl font-bold text-amber-600 dark:text-amber-400">{stats.distinctionCount}</div>
          <div className="text-[11px] text-amber-600 dark:text-amber-400">CGPA ≥ 8.00</div>
        </div>

        <div className="p-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm">
          <div className="flex items-center justify-between text-gray-500 dark:text-gray-400 text-xs">
            <span>Grading Model</span>
            <Sliders className="w-4 h-4 text-teal-500" />
          </div>
          <div className="mt-2 text-lg font-bold text-teal-600 dark:text-teal-400">{selectedGradingModel}</div>
          <div className="text-[11px] text-gray-500 dark:text-gray-400">UGC Standard</div>
        </div>
      </div>

      {/* Tabs and Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gray-200 dark:border-gray-700 pb-3">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setActiveTab("cohort")}
            className={`px-3 py-1.5 text-sm font-medium rounded-lg transition-colors ${
              activeTab === "cohort"
                ? "bg-indigo-600 text-white shadow-sm"
                : "text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800"
            }`}
          >
            Cohort Grade Sheet
          </button>
          <button
            onClick={() => setActiveTab("merit")}
            className={`px-3 py-1.5 text-sm font-medium rounded-lg transition-colors flex items-center gap-1.5 ${
              activeTab === "merit"
                ? "bg-indigo-600 text-white shadow-sm"
                : "text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800"
            }`}
          >
            <Trophy className="w-4 h-4 text-amber-400" />
            Institutional Merit List
          </button>
          <button
            onClick={() => setActiveTab("transcript")}
            className={`px-3 py-1.5 text-sm font-medium rounded-lg transition-colors ${
              activeTab === "transcript"
                ? "bg-indigo-600 text-white shadow-sm"
                : "text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800"
            }`}
          >
            Individual Transcript Card
          </button>
          <button
            onClick={() => setActiveTab("statistics")}
            className={`px-3 py-1.5 text-sm font-medium rounded-lg transition-colors ${
              activeTab === "statistics"
                ? "bg-indigo-600 text-white shadow-sm"
                : "text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800"
            }`}
          >
            Distribution Analytics
          </button>
        </div>

        {/* Grading System Model Switcher */}
        <div className="flex items-center gap-2 bg-gray-100 dark:bg-gray-800 p-1 rounded-lg">
          <span className="text-xs font-medium text-gray-500 dark:text-gray-400 px-2">Grading Model:</span>
          <button
            onClick={() => handleRecalculate("ABSOLUTE")}
            disabled={isProcessing}
            className={`px-2.5 py-1 text-xs font-semibold rounded-md transition-all ${
              selectedGradingModel === "ABSOLUTE"
                ? "bg-white dark:bg-gray-700 text-indigo-700 dark:text-indigo-300 shadow-sm"
                : "text-gray-600 dark:text-gray-400 hover:text-gray-900"
            }`}
          >
            UGC Absolute (10-Pt)
          </button>
          <button
            onClick={() => handleRecalculate("RELATIVE")}
            disabled={isProcessing}
            className={`px-2.5 py-1 text-xs font-semibold rounded-md transition-all ${
              selectedGradingModel === "RELATIVE"
                ? "bg-white dark:bg-gray-700 text-indigo-700 dark:text-indigo-300 shadow-sm"
                : "text-gray-600 dark:text-gray-400 hover:text-gray-900"
            }`}
          >
            Gaussian Curve (Relative)
          </button>
        </div>
      </div>

      {/* Main Tab Views */}
      {activeTab === "cohort" && (
        <div className="space-y-4">
          {/* Search bar & filter */}
          <div className="flex items-center justify-between gap-4">
            <div className="relative flex-1 max-w-md">
              <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Search by student name, roll number, enrollment..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-9 pr-4 py-2 text-sm border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <div className="text-xs text-gray-500 dark:text-gray-400">
              Showing {filteredStudents.length} of {cohortResults.length} registered candidates
            </div>
          </div>

          {/* Results Table */}
          <div className="border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden bg-white dark:bg-gray-800 shadow-sm">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-gray-50 dark:bg-gray-900/60 text-gray-500 dark:text-gray-400 text-xs uppercase font-semibold border-b border-gray-200 dark:border-gray-700">
                  <tr>
                    <th className="px-4 py-3">Rank</th>
                    <th className="px-4 py-3">Roll & Enrollment</th>
                    <th className="px-4 py-3">Candidate Name</th>
                    <th className="px-4 py-3 text-center">Marks / 600</th>
                    <th className="px-4 py-3 text-center">Percentage</th>
                    <th className="px-4 py-3 text-center">SGPA</th>
                    <th className="px-4 py-3 text-center">CGPA</th>
                    <th className="px-4 py-3 text-center">Grade</th>
                    <th className="px-4 py-3">Division</th>
                    <th className="px-4 py-3 text-center">Status</th>
                    <th className="px-4 py-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                  {filteredStudents.map((student) => (
                    <tr
                      key={student.id}
                      className="hover:bg-gray-50 dark:hover:bg-gray-750 transition-colors cursor-pointer"
                      onClick={() => {
                        setSelectedStudent(student);
                        setActiveTab("transcript");
                      }}
                    >
                      <td className="px-4 py-3 font-semibold">
                        <div className="flex items-center gap-1.5">
                          {student.classRank === 1 && <Trophy className="w-4 h-4 text-amber-500" />}
                          {student.classRank === 2 && <Trophy className="w-4 h-4 text-slate-400" />}
                          {student.classRank === 3 && <Trophy className="w-4 h-4 text-amber-700" />}
                          #{student.classRank}
                        </div>
                      </td>
                      <td className="px-4 py-3">
                        <div className="font-medium text-gray-900 dark:text-white">{student.rollNumber}</div>
                        <div className="text-xs text-gray-500 dark:text-gray-400">{student.enrollmentNo}</div>
                      </td>
                      <td className="px-4 py-3 font-medium text-gray-900 dark:text-white">
                        {student.candidateName}
                      </td>
                      <td className="px-4 py-3 text-center font-semibold text-gray-900 dark:text-white">
                        {student.totalMarksObtained}
                      </td>
                      <td className="px-4 py-3 text-center font-medium text-indigo-600 dark:text-indigo-400">
                        {student.percentage}%
                      </td>
                      <td className="px-4 py-3 text-center font-bold text-gray-900 dark:text-white">
                        {student.sgpa.toFixed(2)}
                      </td>
                      <td className="px-4 py-3 text-center font-bold text-purple-600 dark:text-purple-400">
                        {student.cgpa.toFixed(2)}
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span className="inline-block px-2.5 py-0.5 rounded text-xs font-bold bg-indigo-100 text-indigo-800 dark:bg-indigo-900/50 dark:text-indigo-300">
                          {student.overallGrade}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-xs">
                        {student.division === "FIRST_CLASS_DISTINCTION" && (
                          <span className="text-emerald-700 dark:text-emerald-400 font-medium">1st Distinction</span>
                        )}
                        {student.division === "FIRST_CLASS" && (
                          <span className="text-blue-700 dark:text-blue-400 font-medium">1st Class</span>
                        )}
                        {student.division === "SECOND_CLASS" && (
                          <span className="text-amber-700 dark:text-amber-400 font-medium">2nd Class</span>
                        )}
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span className="inline-flex items-center gap-1 text-xs font-medium text-emerald-600 dark:text-emerald-400">
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          Passed
                        </span>
                      </td>
                      <td className="px-4 py-3 text-right">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            setSelectedStudent(student);
                            setActiveTab("transcript");
                          }}
                          className="px-2.5 py-1 text-xs font-medium text-indigo-600 dark:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-indigo-950/50 rounded transition-colors"
                        >
                          View Transcript
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Merit List Tab */}
      {activeTab === "merit" && (
        <div className="space-y-6">
          <div className="p-4 rounded-xl border border-amber-200 dark:border-amber-800 bg-amber-50/50 dark:bg-amber-950/20 flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <Trophy className="w-8 h-8 text-amber-500 flex-shrink-0" />
              <div>
                <h3 className="font-bold text-gray-900 dark:text-white text-base">
                  Autonomous Campus Academic Honours & Merit Roll 2026-27
                </h3>
                <p className="text-xs text-gray-600 dark:text-gray-300">
                  Department of Computer Science & Engineering • 5th Semester Comprehensive Evaluation
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium bg-amber-600 hover:bg-amber-700 text-white rounded-lg shadow-sm">
                <Download className="w-3.5 h-3.5" />
                Export Merit Circular (PDF)
              </button>
            </div>
          </div>

          {/* Top 3 Podium Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Rank 1: Gold */}
            <div className="p-6 rounded-2xl border-2 border-amber-400 dark:border-amber-500 bg-gradient-to-b from-amber-50 to-white dark:from-amber-950/30 dark:to-gray-800 shadow-md relative overflow-hidden">
              <div className="absolute -right-4 -top-4 w-20 h-20 bg-amber-200 dark:bg-amber-800/40 rounded-full flex items-center justify-center">
                <Trophy className="w-10 h-10 text-amber-600 dark:text-amber-400" />
              </div>
              <span className="px-3 py-1 rounded-full text-xs font-extrabold bg-amber-500 text-white tracking-wider">
                GOLD MEDALIST
              </span>
              <div className="mt-4">
                <div className="text-xs text-gray-500 dark:text-gray-400">Class Rank #1</div>
                <h4 className="text-xl font-bold text-gray-900 dark:text-white mt-0.5">
                  {cohortResults[0]?.candidateName}
                </h4>
                <div className="text-xs font-mono text-gray-600 dark:text-gray-300 mt-0.5">
                  {cohortResults[0]?.rollNumber} • {cohortResults[0]?.enrollmentNo}
                </div>
              </div>
              <div className="mt-5 grid grid-cols-3 gap-2 pt-4 border-t border-amber-200 dark:border-amber-800 text-center">
                <div>
                  <div className="text-[11px] text-gray-500 dark:text-gray-400">SGPA</div>
                  <div className="text-lg font-bold text-gray-900 dark:text-white">{cohortResults[0]?.sgpa.toFixed(2)}</div>
                </div>
                <div>
                  <div className="text-[11px] text-gray-500 dark:text-gray-400">CGPA</div>
                  <div className="text-lg font-bold text-amber-600 dark:text-amber-400">{cohortResults[0]?.cgpa.toFixed(2)}</div>
                </div>
                <div>
                  <div className="text-[11px] text-gray-500 dark:text-gray-400">Score</div>
                  <div className="text-lg font-bold text-gray-900 dark:text-white">{cohortResults[0]?.percentage}%</div>
                </div>
              </div>
            </div>

            {/* Rank 2: Silver */}
            <div className="p-6 rounded-2xl border-2 border-slate-300 dark:border-slate-600 bg-gradient-to-b from-slate-50 to-white dark:from-slate-900/30 dark:to-gray-800 shadow-sm relative overflow-hidden">
              <div className="absolute -right-4 -top-4 w-20 h-20 bg-slate-200 dark:bg-slate-700/40 rounded-full flex items-center justify-center">
                <Trophy className="w-10 h-10 text-slate-500 dark:text-slate-400" />
              </div>
              <span className="px-3 py-1 rounded-full text-xs font-extrabold bg-slate-500 text-white tracking-wider">
                SILVER MEDALIST
              </span>
              <div className="mt-4">
                <div className="text-xs text-gray-500 dark:text-gray-400">Class Rank #2</div>
                <h4 className="text-xl font-bold text-gray-900 dark:text-white mt-0.5">
                  {cohortResults[1]?.candidateName}
                </h4>
                <div className="text-xs font-mono text-gray-600 dark:text-gray-300 mt-0.5">
                  {cohortResults[1]?.rollNumber} • {cohortResults[1]?.enrollmentNo}
                </div>
              </div>
              <div className="mt-5 grid grid-cols-3 gap-2 pt-4 border-t border-slate-200 dark:border-slate-700 text-center">
                <div>
                  <div className="text-[11px] text-gray-500 dark:text-gray-400">SGPA</div>
                  <div className="text-lg font-bold text-gray-900 dark:text-white">{cohortResults[1]?.sgpa.toFixed(2)}</div>
                </div>
                <div>
                  <div className="text-[11px] text-gray-500 dark:text-gray-400">CGPA</div>
                  <div className="text-lg font-bold text-slate-600 dark:text-slate-300">{cohortResults[1]?.cgpa.toFixed(2)}</div>
                </div>
                <div>
                  <div className="text-[11px] text-gray-500 dark:text-gray-400">Score</div>
                  <div className="text-lg font-bold text-gray-900 dark:text-white">{cohortResults[1]?.percentage}%</div>
                </div>
              </div>
            </div>

            {/* Rank 3: Bronze */}
            <div className="p-6 rounded-2xl border-2 border-amber-600/60 dark:border-amber-700/60 bg-gradient-to-b from-amber-50/50 to-white dark:from-amber-950/20 dark:to-gray-800 shadow-sm relative overflow-hidden">
              <div className="absolute -right-4 -top-4 w-20 h-20 bg-amber-200/50 dark:bg-amber-900/30 rounded-full flex items-center justify-center">
                <Trophy className="w-10 h-10 text-amber-700 dark:text-amber-500" />
              </div>
              <span className="px-3 py-1 rounded-full text-xs font-extrabold bg-amber-700 text-white tracking-wider">
                BRONZE MEDALIST
              </span>
              <div className="mt-4">
                <div className="text-xs text-gray-500 dark:text-gray-400">Class Rank #3</div>
                <h4 className="text-xl font-bold text-gray-900 dark:text-white mt-0.5">
                  {cohortResults[2]?.candidateName}
                </h4>
                <div className="text-xs font-mono text-gray-600 dark:text-gray-300 mt-0.5">
                  {cohortResults[2]?.rollNumber} • {cohortResults[2]?.enrollmentNo}
                </div>
              </div>
              <div className="mt-5 grid grid-cols-3 gap-2 pt-4 border-t border-amber-200 dark:border-amber-800 text-center">
                <div>
                  <div className="text-[11px] text-gray-500 dark:text-gray-400">SGPA</div>
                  <div className="text-lg font-bold text-gray-900 dark:text-white">{cohortResults[2]?.sgpa.toFixed(2)}</div>
                </div>
                <div>
                  <div className="text-[11px] text-gray-500 dark:text-gray-400">CGPA</div>
                  <div className="text-lg font-bold text-amber-700 dark:text-amber-500">{cohortResults[2]?.cgpa.toFixed(2)}</div>
                </div>
                <div>
                  <div className="text-[11px] text-gray-500 dark:text-gray-400">Score</div>
                  <div className="text-lg font-bold text-gray-900 dark:text-white">{cohortResults[2]?.percentage}%</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Transcript Card Tab */}
      {activeTab === "transcript" && selectedStudent && (
        <div className="space-y-6">
          {/* Header of Transcript */}
          <div className="p-6 rounded-2xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-gray-200 dark:border-gray-700 pb-5">
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 rounded-full bg-indigo-100 dark:bg-indigo-900/60 flex items-center justify-center font-bold text-indigo-700 dark:text-indigo-300 text-xl">
                  {selectedStudent.candidateName.charAt(0)}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                      {selectedStudent.candidateName}
                    </h2>
                    <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-900/50 dark:text-emerald-300">
                      PASSED • DISTINCTION
                    </span>
                  </div>
                  <div className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">
                    Roll: <span className="font-mono font-medium text-gray-700 dark:text-gray-200">{selectedStudent.rollNumber}</span> • Enrollment: <span className="font-mono font-medium text-gray-700 dark:text-gray-200">{selectedStudent.enrollmentNo}</span>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <div className="text-right">
                  <div className="text-xs text-gray-500 dark:text-gray-400">Semester SGPA</div>
                  <div className="text-2xl font-black text-indigo-600 dark:text-indigo-400">
                    {selectedStudent.sgpa.toFixed(2)}
                  </div>
                </div>
                <div className="h-8 w-px bg-gray-200 dark:border-gray-700" />
                <div className="text-right">
                  <div className="text-xs text-gray-500 dark:text-gray-400">Overall CGPA</div>
                  <div className="text-2xl font-black text-purple-600 dark:text-purple-400">
                    {selectedStudent.cgpa.toFixed(2)}
                  </div>
                </div>
                <div className="h-8 w-px bg-gray-200 dark:border-gray-700" />
                <div className="text-right">
                  <div className="text-xs text-gray-500 dark:text-gray-400">Class Rank</div>
                  <div className="text-2xl font-black text-amber-600 dark:text-amber-400">
                    #{selectedStudent.classRank}
                  </div>
                </div>
              </div>
            </div>

            {/* Course-by-Course Breakdown Table */}
            <div className="mt-6">
              <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
                <BookOpen className="w-4 h-4 text-indigo-500" />
                Course Performance & Grade Breakdown
              </h4>
              <div className="border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden">
                <table className="w-full text-left text-sm">
                  <thead className="bg-gray-50 dark:bg-gray-900/60 text-gray-500 dark:text-gray-400 text-xs uppercase font-semibold">
                    <tr>
                      <th className="px-4 py-3">Course Code</th>
                      <th className="px-4 py-3">Course Title</th>
                      <th className="px-4 py-3 text-center">Credits</th>
                      <th className="px-4 py-3 text-center">Max Marks</th>
                      <th className="px-4 py-3 text-center">Marks Obtained</th>
                      <th className="px-4 py-3 text-center">Grade Letter</th>
                      <th className="px-4 py-3 text-center">Grade Points</th>
                      <th className="px-4 py-3 text-center">Credits × GP</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                    {selectedStudent.courses.map((c) => (
                      <tr key={c.courseCode} className="hover:bg-gray-50 dark:hover:bg-gray-750">
                        <td className="px-4 py-3 font-mono font-medium text-gray-900 dark:text-white">
                          {c.courseCode}
                        </td>
                        <td className="px-4 py-3 text-gray-900 dark:text-white font-medium">
                          {c.courseName}
                        </td>
                        <td className="px-4 py-3 text-center">{c.credits.toFixed(1)}</td>
                        <td className="px-4 py-3 text-center">{c.maxMarks.toFixed(1)}</td>
                        <td className="px-4 py-3 text-center font-semibold text-gray-900 dark:text-white">
                          {c.marksObtained.toFixed(1)}
                        </td>
                        <td className="px-4 py-3 text-center">
                          <span className="px-2 py-0.5 rounded text-xs font-bold bg-indigo-100 text-indigo-800 dark:bg-indigo-900/50 dark:text-indigo-300">
                            {c.gradeLetter}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-center font-bold">{c.gradePoints.toFixed(1)}</td>
                        <td className="px-4 py-3 text-center font-bold text-indigo-600 dark:text-indigo-400">
                          {(c.credits * c.gradePoints).toFixed(1)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                  <tfoot className="bg-gray-50 dark:bg-gray-900/60 font-semibold border-t border-gray-200 dark:border-gray-700">
                    <tr>
                      <td colSpan={2} className="px-4 py-3 text-right">Total:</td>
                      <td className="px-4 py-3 text-center font-bold">{selectedStudent.totalCreditsRegistered.toFixed(1)}</td>
                      <td className="px-4 py-3 text-center">{selectedStudent.totalMaxMarks.toFixed(1)}</td>
                      <td className="px-4 py-3 text-center font-bold text-gray-900 dark:text-white">
                        {selectedStudent.totalMarksObtained.toFixed(1)}
                      </td>
                      <td colSpan={2} className="px-4 py-3 text-right">Computed SGPA:</td>
                      <td className="px-4 py-3 text-center font-extrabold text-indigo-600 dark:text-indigo-400">
                        {selectedStudent.sgpa.toFixed(2)}
                      </td>
                    </tr>
                  </tfoot>
                </table>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Distribution Analytics Tab */}
      {activeTab === "statistics" && (
        <div className="space-y-6">
          <div className="p-6 rounded-2xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm space-y-6">
            <h3 className="font-bold text-gray-900 dark:text-white text-base flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-indigo-500" />
              Grade Frequency & Bell Curve Dispersion
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="p-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/40">
                <div className="text-xs text-gray-500 dark:text-gray-400">Grade 'O' (Outstanding)</div>
                <div className="text-2xl font-bold text-indigo-600 dark:text-indigo-400 mt-1">2 Candidates</div>
                <div className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">40.0% of cohort</div>
              </div>
              <div className="p-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/40">
                <div className="text-xs text-gray-500 dark:text-gray-400">Grade 'A+' (Excellent)</div>
                <div className="text-2xl font-bold text-blue-600 dark:text-blue-400 mt-1">2 Candidates</div>
                <div className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">40.0% of cohort</div>
              </div>
              <div className="p-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/40">
                <div className="text-xs text-gray-500 dark:text-gray-400">Grade 'A' (Very Good)</div>
                <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1">1 Candidate</div>
                <div className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">20.0% of cohort</div>
              </div>
              <div className="p-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/40">
                <div className="text-xs text-gray-500 dark:text-gray-400">Backlogs / Failures</div>
                <div className="text-2xl font-bold text-gray-400 mt-1">0 Candidates</div>
                <div className="text-xs text-emerald-600 dark:text-emerald-400 mt-0.5">0.0% Fail rate</div>
              </div>
            </div>

            <div className="p-4 rounded-xl border border-indigo-100 dark:border-indigo-900 bg-indigo-50/40 dark:bg-indigo-950/20 text-xs text-indigo-900 dark:text-indigo-300">
              <span className="font-semibold">Autonomous Evaluation Engine Formula:</span> SGPA is calculated as $\sum (\text{Course Credits} \times \text{Grade Points}) / \sum (\text{Course Credits})$, conforming strictly to UGC & AICTE autonomous institute regulations.
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultProcessingStudioPage;
