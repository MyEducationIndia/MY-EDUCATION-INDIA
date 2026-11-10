import React from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  BookOpen,
  GraduationCap,
  Layers,
  Calendar,
  Building,
  Clock,
  Plus,
  CheckCircle2,
} from "lucide-react";
import { academicService } from "../services/academicService";

export const AcademicDashboardPage: React.FC = () => {
  const { data: courses = [] } = useQuery({ queryKey: ["academicCourses"], queryFn: academicService.listCourses });
  const { data: depts = [] } = useQuery({ queryKey: ["academicDepts"], queryFn: academicService.listDepartments });
  const { data: batches = [] } = useQuery({ queryKey: ["academicBatches"], queryFn: academicService.listBatches });
  const { data: subjects = [] } = useQuery({ queryKey: ["academicSubjects"], queryFn: academicService.listSubjects });

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs dark:border-slate-800 dark:bg-slate-900 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-base font-bold text-slate-900 dark:text-white">
            Enterprise Academic Management System
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Academic structure, courses, CBCS curriculums, cohorts, conflict-free timetables, and teacher assignments.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Link
            to="/admin/academics/courses"
            className="inline-flex items-center gap-1.5 rounded-xl bg-brand-600 px-4 py-2 text-xs font-bold text-white shadow-md hover:bg-brand-500"
          >
            <Plus className="h-4 w-4" /> Manage Courses
          </Link>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase text-slate-500">Departments</span>
            <Building className="h-5 w-5 text-blue-600" />
          </div>
          <p className="mt-2 text-2xl font-extrabold text-slate-900 dark:text-white">{depts.length}</p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase text-slate-500">Courses / Degrees</span>
            <BookOpen className="h-5 w-5 text-emerald-600" />
          </div>
          <p className="mt-2 text-2xl font-extrabold text-slate-900 dark:text-white">{courses.length}</p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase text-slate-500">Active Batches</span>
            <Layers className="h-5 w-5 text-indigo-600" />
          </div>
          <p className="mt-2 text-2xl font-extrabold text-slate-900 dark:text-white">{batches.length}</p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase text-slate-500">Total Subjects</span>
            <GraduationCap className="h-5 w-5 text-purple-600" />
          </div>
          <p className="mt-2 text-2xl font-extrabold text-slate-900 dark:text-white">{subjects.length}</p>
        </div>
      </div>

      {/* Sections Hub */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <Link to="/admin/academics/departments" className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs hover:border-brand-500 dark:border-slate-800 dark:bg-slate-900">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white">Academic Departments</h3>
          <p className="mt-1 text-xs text-slate-500">Manage academic departments, faculty HODs, and branch linkages.</p>
          <span className="mt-3 inline-block text-xs font-bold text-brand-600">Open Departments →</span>
        </Link>

        <Link to="/admin/academics/batches" className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs hover:border-brand-500 dark:border-slate-800 dark:bg-slate-900">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white">Batches & Sections</h3>
          <p className="mt-1 text-xs text-slate-500">Manage cohorts, intake capacity, and classroom sections (A, B, Evening).</p>
          <span className="mt-3 inline-block text-xs font-bold text-brand-600">Open Batches →</span>
        </Link>

        <Link to="/admin/academics/timetable" className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs hover:border-brand-500 dark:border-slate-800 dark:bg-slate-900">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white">Conflict-Free Timetable</h3>
          <p className="mt-1 text-xs text-slate-500">Weekly schedule matrix with automatic classroom and faculty overlap prevention.</p>
          <span className="mt-3 inline-block text-xs font-bold text-brand-600">Open Timetable Engine →</span>
        </Link>
      </div>
    </div>
  );
};
