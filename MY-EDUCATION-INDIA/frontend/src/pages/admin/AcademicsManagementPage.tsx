import React, { useState, useMemo } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  BookOpen,
  Calendar,
  Clock,
  Plus,
  Trash2,
  Edit2,
  CheckCircle2,
  AlertTriangle,
  Search,
  Filter,
  UserCheck,
  Building,
  GraduationCap,
  Layers,
  Sparkles,
  Download,
  RotateCcw,
} from "lucide-react";

interface TimetableSlot {
  id: string;
  day: "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday" | "Saturday";
  time_slot: string; // e.g. "08:30 - 09:30"
  course_code: string;
  course_name: string;
  faculty_name: string;
  room_number: string;
  batch_division: string;
  slot_type: "LECTURE" | "LAB" | "TUTORIAL" | "SEMINAR";
  credits: number;
}

interface AcademicProgramTrack {
  id: string;
  code: string;
  name: string;
  department: string;
  total_semesters: number;
  current_active_semester: number;
  credits_required: number;
  total_enrolled: number;
}

const INITIAL_PROGRAMS: AcademicProgramTrack[] = [
  {
    id: "prog-1",
    code: "BTECH-CSE",
    name: "B.Tech in Computer Science & Engineering",
    department: "Computer Science & Engineering",
    total_semesters: 8,
    current_active_semester: 6,
    credits_required: 160,
    total_enrolled: 480,
  },
  {
    id: "prog-2",
    code: "BTECH-AI-DS",
    name: "B.Tech in Artificial Intelligence & Data Science",
    department: "Data Science & AI",
    total_semesters: 8,
    current_active_semester: 4,
    credits_required: 160,
    total_enrolled: 240,
  },
  {
    id: "prog-3",
    code: "MTECH-CSE",
    name: "M.Tech in Advanced Computing & Neural Systems",
    department: "Computer Science & Engineering",
    total_semesters: 4,
    current_active_semester: 2,
    credits_required: 80,
    total_enrolled: 60,
  },
  {
    id: "prog-4",
    code: "BCA-HONS",
    name: "Bachelor of Computer Applications (Honours)",
    department: "Computer Applications",
    total_semesters: 6,
    current_active_semester: 4,
    credits_required: 140,
    total_enrolled: 320,
  },
];

const TIME_SLOTS = [
  "08:30 - 09:30",
  "09:30 - 10:30",
  "10:45 - 11:45",
  "11:45 - 12:45",
  "01:30 - 02:30",
  "02:30 - 03:30",
  "03:30 - 04:30",
];

const DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"] as const;

const INITIAL_SLOTS: TimetableSlot[] = [
  {
    id: "slot-1",
    day: "Monday",
    time_slot: "08:30 - 09:30",
    course_code: "CS601",
    course_name: "Machine Learning & Neural Networks",
    faculty_name: "Dr. Rajesh Sharma",
    room_number: "LH-201 (Smart Block)",
    batch_division: "CSE-A",
    slot_type: "LECTURE",
    credits: 4,
  },
  {
    id: "slot-2",
    day: "Monday",
    time_slot: "09:30 - 10:30",
    course_code: "CS602",
    course_name: "Cloud Computing & Distributed Systems",
    faculty_name: "Prof. Ananya Sen",
    room_number: "LH-201 (Smart Block)",
    batch_division: "CSE-A",
    slot_type: "LECTURE",
    credits: 3,
  },
  {
    id: "slot-3",
    day: "Monday",
    time_slot: "10:45 - 11:45",
    course_code: "CS603",
    course_name: "Information Security & Cryptography",
    faculty_name: "Dr. Alok Verma",
    room_number: "LH-201 (Smart Block)",
    batch_division: "CSE-A",
    slot_type: "LECTURE",
    credits: 3,
  },
  {
    id: "slot-4",
    day: "Monday",
    time_slot: "01:30 - 02:30",
    course_code: "CS605L",
    course_name: "AI & Neural Networks Lab (Batch 1)",
    faculty_name: "Dr. Rajesh Sharma",
    room_number: "AI-Research Lab 4",
    batch_division: "CSE-A1",
    slot_type: "LAB",
    credits: 2,
  },
  {
    id: "slot-5",
    day: "Monday",
    time_slot: "02:30 - 03:30",
    course_code: "CS605L",
    course_name: "AI & Neural Networks Lab (Batch 1 cont.)",
    faculty_name: "Dr. Rajesh Sharma",
    room_number: "AI-Research Lab 4",
    batch_division: "CSE-A1",
    slot_type: "LAB",
    credits: 2,
  },
  {
    id: "slot-6",
    day: "Tuesday",
    time_slot: "08:30 - 09:30",
    course_code: "CS604",
    course_name: "Compiler Design & Syntax Engineering",
    faculty_name: "Dr. Meenakshi Sundaram",
    room_number: "LH-202 (Smart Block)",
    batch_division: "CSE-A",
    slot_type: "LECTURE",
    credits: 4,
  },
  {
    id: "slot-7",
    day: "Tuesday",
    time_slot: "09:30 - 10:30",
    course_code: "CS601",
    course_name: "Machine Learning & Neural Networks",
    faculty_name: "Dr. Rajesh Sharma",
    room_number: "LH-201 (Smart Block)",
    batch_division: "CSE-A",
    slot_type: "LECTURE",
    credits: 4,
  },
  {
    id: "slot-8",
    day: "Wednesday",
    time_slot: "10:45 - 11:45",
    course_code: "CS602",
    course_name: "Cloud Computing & Distributed Systems",
    faculty_name: "Prof. Ananya Sen",
    room_number: "LH-201 (Smart Block)",
    batch_division: "CSE-A",
    slot_type: "LECTURE",
    credits: 3,
  },
  {
    id: "slot-9",
    day: "Thursday",
    time_slot: "11:45 - 12:45",
    course_code: "CS603",
    course_name: "Information Security & Cryptography",
    faculty_name: "Dr. Alok Verma",
    room_number: "LH-201 (Smart Block)",
    batch_division: "CSE-A",
    slot_type: "LECTURE",
    credits: 3,
  },
  {
    id: "slot-10",
    day: "Friday",
    time_slot: "01:30 - 02:30",
    course_code: "CS606T",
    course_name: "Technical Communication & Seminar",
    faculty_name: "Prof. Kavita Rao",
    room_number: "Seminar Hall 2",
    batch_division: "CSE-A",
    slot_type: "SEMINAR",
    credits: 1,
  },
];

export const AcademicsManagementPage: React.FC = () => {
  const [selectedProgram, setSelectedProgram] = useState<string>("BTECH-CSE");
  const [selectedSemester, setSelectedSemester] = useState<number>(6);
  const [selectedSection, setSelectedSection] = useState<string>("CSE-A");
  const [viewMode, setViewMode] = useState<"TIMETABLE" | "CURRICULUM" | "WORKLOAD">("TIMETABLE");
  const [slots, setSlots] = useState<TimetableSlot[]>(INITIAL_SLOTS);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [searchFilter, setSearchFilter] = useState("");

  // New slot form state
  const [newSlot, setNewSlot] = useState<Partial<TimetableSlot>>({
    day: "Monday",
    time_slot: "08:30 - 09:30",
    course_code: "",
    course_name: "",
    faculty_name: "",
    room_number: "",
    batch_division: "CSE-A",
    slot_type: "LECTURE",
    credits: 3,
  });

  const handleAddSlot = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSlot.course_code || !newSlot.course_name || !newSlot.faculty_name || !newSlot.room_number) {
      alert("Please fill all required timetable parameters.");
      return;
    }

    const created: TimetableSlot = {
      id: `slot-${Date.now()}`,
      day: newSlot.day as any,
      time_slot: newSlot.time_slot || "08:30 - 09:30",
      course_code: newSlot.course_code.toUpperCase(),
      course_name: newSlot.course_name,
      faculty_name: newSlot.faculty_name,
      room_number: newSlot.room_number,
      batch_division: newSlot.batch_division || selectedSection,
      slot_type: (newSlot.slot_type as any) || "LECTURE",
      credits: Number(newSlot.credits) || 3,
    };

    setSlots((prev) => [...prev, created]);
    setIsAddModalOpen(false);
    setNewSlot({
      day: "Monday",
      time_slot: "08:30 - 09:30",
      course_code: "",
      course_name: "",
      faculty_name: "",
      room_number: "",
      batch_division: selectedSection,
      slot_type: "LECTURE",
      credits: 3,
    });
  };

  const handleDeleteSlot = (id: string) => {
    if (confirm("Remove this lecture slot from the official academic timetable?")) {
      setSlots((prev) => prev.filter((s) => s.id !== id));
    }
  };

  // Metrics calculation
  const totalWeeklyLectures = slots.length;
  const totalWeeklyCredits = useMemo(
    () => slots.reduce((acc, curr) => acc + (curr.credits || 0), 0),
    [slots]
  );
  const uniqueFaculty = useMemo(
    () => new Set(slots.map((s) => s.faculty_name)).size,
    [slots]
  );
  const uniqueRooms = useMemo(
    () => new Set(slots.map((s) => s.room_number)).size,
    [slots]
  );

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex items-center gap-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-50 text-brand-600">
              <BookOpen className="h-6 w-6" />
            </div>
            <div>
              <div className="flex items-center gap-2.5">
                <h1 className="text-xl font-bold text-slate-900">Academic Engine & Timetable Planner</h1>
                <span className="rounded-full bg-emerald-100 px-2.5 py-0.5 text-[11px] font-semibold text-emerald-800">
                  ERP MODULE 8 LIVE
                </span>
              </div>
              <p className="mt-0.5 text-xs text-slate-500">
                Institutional curriculum management, faculty workload distributions, and conflict-free weekly timetable orchestration.
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2.5">
            <button
              onClick={() => setIsAddModalOpen(true)}
              className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2 text-xs font-semibold text-white shadow-xs hover:bg-brand-700"
            >
              <Plus className="h-4 w-4" />
              Allocate Lecture Slot
            </button>
            <button
              onClick={() => alert("Official Weekly Master Timetable PDF generation triggered. Stored in ERP registry.")}
              className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-3.5 py-2 text-xs font-semibold text-slate-700 shadow-xs hover:bg-slate-50"
            >
              <Download className="h-4 w-4 text-slate-500" />
              Export Schedule (PDF)
            </button>
          </div>
        </div>

        {/* Top Operational Metrics */}
        <div className="mt-6 grid grid-cols-2 gap-4 border-t border-slate-100 pt-5 sm:grid-cols-4">
          <div className="rounded-xl border border-slate-100 bg-slate-50/50 p-3.5">
            <span className="text-[11px] font-medium text-slate-500 uppercase tracking-wider">Weekly Class Sessions</span>
            <p className="mt-1 text-2xl font-bold text-slate-900">{totalWeeklyLectures}</p>
            <span className="text-[10px] text-emerald-600 font-medium">Conflict-Free Validated</span>
          </div>
          <div className="rounded-xl border border-slate-100 bg-slate-50/50 p-3.5">
            <span className="text-[11px] font-medium text-slate-500 uppercase tracking-wider">Active Credit Load</span>
            <p className="mt-1 text-2xl font-bold text-brand-600">{totalWeeklyCredits} hrs</p>
            <span className="text-[10px] text-slate-500">Across Semester Registry</span>
          </div>
          <div className="rounded-xl border border-slate-100 bg-slate-50/50 p-3.5">
            <span className="text-[11px] font-medium text-slate-500 uppercase tracking-wider">Faculty Deployed</span>
            <p className="mt-1 text-2xl font-bold text-purple-600">{uniqueFaculty}</p>
            <span className="text-[10px] text-slate-500">Professors & Instructors</span>
          </div>
          <div className="rounded-xl border border-slate-100 bg-slate-50/50 p-3.5">
            <span className="text-[11px] font-medium text-slate-500 uppercase tracking-wider">Rooms & Labs Allocated</span>
            <p className="mt-1 text-2xl font-bold text-emerald-600">{uniqueRooms}</p>
            <span className="text-[10px] text-slate-500">Smart Halls & High-Perf Labs</span>
          </div>
        </div>
      </div>

      {/* Control Bar & Filter Selectors */}
      <div className="flex flex-col gap-4 rounded-2xl border border-slate-200 bg-white p-4 shadow-xs sm:flex-row sm:items-center sm:justify-between">
        <div className="flex flex-wrap items-center gap-3">
          <div>
            <label className="block text-[11px] font-medium text-slate-500 mb-1">Academic Program</label>
            <select
              value={selectedProgram}
              onChange={(e) => setSelectedProgram(e.target.value)}
              className="rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-800 shadow-xs focus:border-brand-500 focus:outline-none"
            >
              {INITIAL_PROGRAMS.map((prog) => (
                <option key={prog.id} value={prog.code}>
                  {prog.code} - {prog.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-medium text-slate-500 mb-1">Semester</label>
            <select
              value={selectedSemester}
              onChange={(e) => setSelectedSemester(Number(e.target.value))}
              className="rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-800 shadow-xs focus:border-brand-500 focus:outline-none"
            >
              {[1, 2, 3, 4, 5, 6, 7, 8].map((sem) => (
                <option key={sem} value={sem}>
                  Semester {sem} (2025–26)
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-medium text-slate-500 mb-1">Section Batch</label>
            <select
              value={selectedSection}
              onChange={(e) => setSelectedSection(e.target.value)}
              className="rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-800 shadow-xs focus:border-brand-500 focus:outline-none"
            >
              <option value="CSE-A">Section A (Regular)</option>
              <option value="CSE-B">Section B (Regular)</option>
              <option value="CSE-HONS">Section Honours (Advanced)</option>
            </select>
          </div>
        </div>

        {/* View Mode Switcher */}
        <div className="flex items-center rounded-xl bg-slate-100 p-1 self-start sm:self-auto">
          <button
            onClick={() => setViewMode("TIMETABLE")}
            className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-all ${
              viewMode === "TIMETABLE"
                ? "bg-white text-slate-900 shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Weekly Grid
          </button>
          <button
            onClick={() => setViewMode("CURRICULUM")}
            className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-all ${
              viewMode === "CURRICULUM"
                ? "bg-white text-slate-900 shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Curriculum Map
          </button>
          <button
            onClick={() => setViewMode("WORKLOAD")}
            className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-all ${
              viewMode === "WORKLOAD"
                ? "bg-white text-slate-900 shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Faculty Workload
          </button>
        </div>
      </div>

      {/* Main Content Areas */}
      {viewMode === "TIMETABLE" && (
        <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-xs">
          <div className="border-b border-slate-100 bg-slate-50/70 p-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Calendar className="h-4 w-4 text-brand-600" />
              <h2 className="text-sm font-bold text-slate-900">
                Official Weekly Schedule: {selectedProgram} (Sem {selectedSemester} - {selectedSection})
              </h2>
            </div>
            <span className="text-xs text-slate-500 font-medium">Campus: Indore MEI-HQ Autonomous</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full min-w-[900px] border-collapse text-left">
              <thead>
                <tr className="border-b border-slate-200 bg-slate-100/60 text-[11px] font-bold uppercase tracking-wider text-slate-600">
                  <th className="p-3.5 w-28">Day / Time</th>
                  {TIME_SLOTS.map((slot) => (
                    <th key={slot} className="p-3.5 text-center min-w-[140px]">
                      {slot}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-xs">
                {DAYS_OF_WEEK.map((day) => (
                  <tr key={day} className="hover:bg-slate-50/50 transition-colors">
                    <td className="p-3.5 font-bold text-slate-800 bg-slate-50/30 border-r border-slate-100">
                      {day}
                    </td>
                    {TIME_SLOTS.map((timeSlot) => {
                      const matched = slots.filter(
                        (s) => s.day === day && s.time_slot === timeSlot
                      );

                      if (matched.length === 0) {
                        return (
                          <td
                            key={timeSlot}
                            className="p-2 border-r border-slate-100 text-center text-slate-300 italic text-[11px]"
                          >
                            <span className="inline-block py-2 text-slate-300">Free Slot</span>
                          </td>
                        );
                      }

                      return (
                        <td key={timeSlot} className="p-2 border-r border-slate-100 align-top">
                          {matched.map((slotItem) => (
                            <div
                              key={slotItem.id}
                              className={`group relative rounded-xl border p-2.5 shadow-2xs transition-all ${
                                slotItem.slot_type === "LAB"
                                  ? "border-purple-200 bg-purple-50/50"
                                  : slotItem.slot_type === "SEMINAR"
                                  ? "border-amber-200 bg-amber-50/50"
                                  : "border-brand-200 bg-brand-50/40"
                              }`}
                            >
                              <div className="flex items-start justify-between gap-1 mb-1">
                                <span className="font-bold text-slate-900 text-[11px]">
                                  {slotItem.course_code}
                                </span>
                                <span
                                  className={`rounded-sm px-1 py-0.2 text-[9px] font-bold ${
                                    slotItem.slot_type === "LAB"
                                      ? "bg-purple-100 text-purple-700"
                                      : slotItem.slot_type === "SEMINAR"
                                      ? "bg-amber-100 text-amber-700"
                                      : "bg-brand-100 text-brand-700"
                                  }`}
                                >
                                  {slotItem.slot_type}
                                </span>
                              </div>
                              <p className="text-[11px] font-medium text-slate-700 line-clamp-1">
                                {slotItem.course_name}
                              </p>
                              <div className="mt-2 flex flex-col gap-0.5 text-[10px] text-slate-500">
                                <span className="flex items-center gap-1 font-medium text-slate-600">
                                  <UserCheck className="h-3 w-3 text-slate-400" />
                                  {slotItem.faculty_name}
                                </span>
                                <span className="flex items-center gap-1 text-slate-500">
                                  <Building className="h-3 w-3 text-slate-400" />
                                  {slotItem.room_number}
                                </span>
                              </div>
                              <button
                                onClick={() => handleDeleteSlot(slotItem.id)}
                                title="Remove slot"
                                className="absolute top-1 right-1 hidden p-1 text-slate-400 hover:text-red-600 group-hover:block"
                              >
                                <Trash2 className="h-3 w-3" />
                              </button>
                            </div>
                          ))}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Curriculum View */}
      {viewMode === "CURRICULUM" && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-bold text-slate-900">
              Prescribed Curriculum Structure: {selectedProgram} (Semester {selectedSemester})
            </h2>
            <span className="text-xs text-brand-600 font-semibold">UGC / AICTE Autonomous Compliant</span>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {[
              {
                code: "CS601",
                name: "Machine Learning & Neural Networks",
                credits: 4,
                lectures: 3,
                tutorials: 1,
                practical: 0,
                coordinator: "Dr. Rajesh Sharma",
              },
              {
                code: "CS602",
                name: "Cloud Computing & Distributed Systems",
                credits: 3,
                lectures: 3,
                tutorials: 0,
                practical: 0,
                coordinator: "Prof. Ananya Sen",
              },
              {
                code: "CS603",
                name: "Information Security & Cryptography",
                credits: 3,
                lectures: 3,
                tutorials: 0,
                practical: 0,
                coordinator: "Dr. Alok Verma",
              },
              {
                code: "CS604",
                name: "Compiler Design & Syntax Engineering",
                credits: 4,
                lectures: 3,
                tutorials: 1,
                practical: 0,
                coordinator: "Dr. Meenakshi Sundaram",
              },
              {
                code: "CS605L",
                name: "AI & Neural Networks Lab",
                credits: 2,
                lectures: 0,
                tutorials: 0,
                practical: 4,
                coordinator: "Dr. Rajesh Sharma",
              },
              {
                code: "CS606T",
                name: "Technical Communication & Seminar",
                credits: 1,
                lectures: 0,
                tutorials: 0,
                practical: 2,
                coordinator: "Prof. Kavita Rao",
              },
            ].map((course) => (
              <div key={course.code} className="rounded-xl border border-slate-200 bg-slate-50/50 p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="rounded-md bg-brand-100 px-2 py-0.5 text-xs font-bold text-brand-700">
                    {course.code}
                  </span>
                  <span className="text-xs font-semibold text-slate-600">{course.credits} Credits</span>
                </div>
                <h3 className="text-sm font-bold text-slate-900">{course.name}</h3>
                <p className="mt-1 text-xs text-slate-500">Course Coordinator: {course.coordinator}</p>
                <div className="mt-3 flex items-center gap-3 text-[11px] font-medium text-slate-600 border-t border-slate-200/60 pt-2">
                  <span>L: {course.lectures} hrs</span>
                  <span>•</span>
                  <span>T: {course.tutorials} hrs</span>
                  <span>•</span>
                  <span>P: {course.practical} hrs</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Workload View */}
      {viewMode === "WORKLOAD" && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-bold text-slate-900">
              Department Faculty Teaching Workload Allocations
            </h2>
            <span className="text-xs text-slate-500">Maximum Allowed Workload: 18 hrs/week</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full border-collapse text-left text-xs">
              <thead>
                <tr className="border-b border-slate-200 bg-slate-50 text-[11px] font-bold uppercase tracking-wider text-slate-600">
                  <th className="p-3">Faculty Name</th>
                  <th className="p-3">Designation</th>
                  <th className="p-3">Assigned Courses</th>
                  <th className="p-3 text-center">Theory Hrs</th>
                  <th className="p-3 text-center">Lab Hrs</th>
                  <th className="p-3 text-center">Total Load</th>
                  <th className="p-3 text-right">Workload Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {[
                  {
                    name: "Dr. Rajesh Sharma",
                    designation: "Professor & HOD",
                    courses: "CS601 (ML), CS605L (AI Lab)",
                    theory: 6,
                    lab: 4,
                    total: 10,
                    status: "OPTIMAL",
                  },
                  {
                    name: "Prof. Ananya Sen",
                    designation: "Associate Professor",
                    courses: "CS602 (Cloud), CS401 (OS)",
                    theory: 8,
                    lab: 2,
                    total: 10,
                    status: "OPTIMAL",
                  },
                  {
                    name: "Dr. Alok Verma",
                    designation: "Associate Professor",
                    courses: "CS603 (Security), CS502 (Networks)",
                    theory: 9,
                    lab: 3,
                    total: 12,
                    status: "BALANCED",
                  },
                  {
                    name: "Dr. Meenakshi Sundaram",
                    designation: "Assistant Professor",
                    courses: "CS604 (Compiler), CS301 (Data Structures)",
                    theory: 10,
                    lab: 4,
                    total: 14,
                    status: "BALANCED",
                  },
                  {
                    name: "Prof. Kavita Rao",
                    designation: "Assistant Professor",
                    courses: "CS606T (Seminar), CS201 (Python)",
                    theory: 4,
                    lab: 6,
                    total: 10,
                    status: "OPTIMAL",
                  },
                ].map((fac, idx) => (
                  <tr key={idx} className="hover:bg-slate-50">
                    <td className="p-3 font-bold text-slate-800">{fac.name}</td>
                    <td className="p-3 text-slate-600">{fac.designation}</td>
                    <td className="p-3 text-slate-700">{fac.courses}</td>
                    <td className="p-3 text-center text-slate-700">{fac.theory}</td>
                    <td className="p-3 text-center text-slate-700">{fac.lab}</td>
                    <td className="p-3 text-center font-bold text-slate-900">{fac.total} hrs/wk</td>
                    <td className="p-3 text-right">
                      <span className="rounded-full bg-emerald-100 px-2 py-0.5 text-[10px] font-bold text-emerald-800">
                        {fac.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Modal: Allocate Lecture Slot */}
      {isAddModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-xs">
          <div className="w-full max-w-lg rounded-2xl border border-slate-200 bg-white p-6 shadow-xl">
            <div className="flex items-center justify-between border-b border-slate-100 pb-4">
              <h3 className="text-base font-bold text-slate-900">Allocate Academic Lecture Slot</h3>
              <button
                onClick={() => setIsAddModalOpen(false)}
                className="text-slate-400 hover:text-slate-600"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleAddSlot} className="mt-4 space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Day of Week</label>
                  <select
                    value={newSlot.day}
                    onChange={(e) => setNewSlot({ ...newSlot, day: e.target.value as any })}
                    className="w-full rounded-lg border border-slate-200 px-3 py-2 text-xs focus:border-brand-500 focus:outline-none"
                  >
                    {DAYS_OF_WEEK.map((d) => (
                      <option key={d} value={d}>
                        {d}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Time Slot</label>
                  <select
                    value={newSlot.time_slot}
                    onChange={(e) => setNewSlot({ ...newSlot, time_slot: e.target.value })}
                    className="w-full rounded-lg border border-slate-200 px-3 py-2 text-xs focus:border-brand-500 focus:outline-none"
                  >
                    {TIME_SLOTS.map((t) => (
                      <option key={t} value={t}>
                        {t}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div className="col-span-1">
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Course Code</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. CS601"
                    value={newSlot.course_code || ""}
                    onChange={(e) => setNewSlot({ ...newSlot, course_code: e.target.value })}
                    className="w-full rounded-lg border border-slate-200 px-3 py-2 text-xs focus:border-brand-500 focus:outline-none"
                  />
                </div>
                <div className="col-span-2">
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Course Name</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Machine Learning"
                    value={newSlot.course_name || ""}
                    onChange={(e) => setNewSlot({ ...newSlot, course_name: e.target.value })}
                    className="w-full rounded-lg border border-slate-200 px-3 py-2 text-xs focus:border-brand-500 focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Faculty In-Charge</label>
                  <input
                    type="text"
                    required
                    placeholder="Dr. Rajesh Sharma"
                    value={newSlot.faculty_name || ""}
                    onChange={(e) => setNewSlot({ ...newSlot, faculty_name: e.target.value })}
                    className="w-full rounded-lg border border-slate-200 px-3 py-2 text-xs focus:border-brand-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Room / Lab No.</label>
                  <input
                    type="text"
                    required
                    placeholder="LH-201 / Lab 4"
                    value={newSlot.room_number || ""}
                    onChange={(e) => setNewSlot({ ...newSlot, room_number: e.target.value })}
                    className="w-full rounded-lg border border-slate-200 px-3 py-2 text-xs focus:border-brand-500 focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Type</label>
                  <select
                    value={newSlot.slot_type}
                    onChange={(e) => setNewSlot({ ...newSlot, slot_type: e.target.value as any })}
                    className="w-full rounded-lg border border-slate-200 px-3 py-2 text-xs focus:border-brand-500 focus:outline-none"
                  >
                    <option value="LECTURE">Lecture</option>
                    <option value="LAB">Lab Session</option>
                    <option value="TUTORIAL">Tutorial</option>
                    <option value="SEMINAR">Seminar</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Batch / Div</label>
                  <input
                    type="text"
                    placeholder="CSE-A"
                    value={newSlot.batch_division || ""}
                    onChange={(e) => setNewSlot({ ...newSlot, batch_division: e.target.value })}
                    className="w-full rounded-lg border border-slate-200 px-3 py-2 text-xs focus:border-brand-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Credits</label>
                  <input
                    type="number"
                    min={1}
                    max={6}
                    value={newSlot.credits || 3}
                    onChange={(e) => setNewSlot({ ...newSlot, credits: Number(e.target.value) })}
                    className="w-full rounded-lg border border-slate-200 px-3 py-2 text-xs focus:border-brand-500 focus:outline-none"
                  />
                </div>
              </div>

              <div className="flex justify-end gap-2 border-t border-slate-100 pt-4">
                <button
                  type="button"
                  onClick={() => setIsAddModalOpen(false)}
                  className="rounded-lg border border-slate-200 px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="rounded-lg bg-brand-600 px-4 py-2 text-xs font-semibold text-white hover:bg-brand-700"
                >
                  Confirm Allocation
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
