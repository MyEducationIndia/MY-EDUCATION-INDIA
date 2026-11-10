import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Users,
  Search,
  Filter,
  UserPlus,
  Upload,
  Download,
  Trash2,
  TrendingUp,
  Eye,
  QrCode,
} from "lucide-react";
import { studentApi } from "../api/studentApi";
import { StudentDetailedProfile, StudentSummary } from "../types/student.types";
import { StudentTabbedProfileModal } from "../profile/StudentTabbedProfileModal";
import { StudentQRCodeModal } from "../components/StudentQRCodeModal";

export const StudentDirectoryPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCourse, setSelectedCourse] = useState("");
  const [selectedStatus, setSelectedStatus] = useState("");
  const [page, setPage] = useState(1);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);

  // Modals state
  const [activeProfile, setActiveProfile] = useState<StudentDetailedProfile | null>(null);
  const [qrModalStudent, setQrModalStudent] = useState<StudentDetailedProfile | null>(null);

  const { data, isLoading } = useQuery({
    queryKey: ["studentsDirectory", searchTerm, selectedCourse, selectedStatus, page],
    queryFn: () =>
      studentApi.searchStudents({
        query: searchTerm || undefined,
        course_name: selectedCourse || undefined,
        status: selectedStatus || undefined,
        page,
        page_size: 20,
      }),
  });

  const bulkDeleteMutation = useMutation({
    mutationFn: (ids: string[]) => studentApi.bulkDeleteStudents(ids),
    onSuccess: () => {
      setSelectedIds([]);
      void queryClient.invalidateQueries({ queryKey: ["studentsDirectory"] });
    },
  });

  const openProfileModal = async (id: string) => {
    const prof = await studentApi.getStudentProfile(id);
    setActiveProfile(prof);
  };

  const handleSelectAll = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.checked && data?.items) {
      setSelectedIds(data.items.map((s) => s.id));
    } else {
      setSelectedIds([]);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner & Quick Controls */}
      <div className="flex flex-col justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs dark:border-slate-800 dark:bg-slate-900 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-base font-bold text-slate-900 dark:text-white">
            Student Information Management System (SIMS)
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Enterprise master repository for student profiles, academic allocations, digital ID cards, and lifecycle tracking.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <a
            href="/api/v1/students/template/csv"
            className="inline-flex items-center gap-1.5 rounded-xl border border-slate-300 bg-white px-3 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200"
          >
            <Download className="h-4 w-4" /> CSV Template
          </a>
          <button
            type="button"
            onClick={() => alert("Please use the Student Registration form.")}
            className="inline-flex items-center gap-1.5 rounded-xl bg-brand-600 px-4 py-2 text-xs font-bold text-white shadow-md hover:bg-brand-500"
          >
            <UserPlus className="h-4 w-4" /> Register Student
          </button>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs dark:border-slate-800 dark:bg-slate-900">
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-4">
          <div className="relative sm:col-span-2">
            <Search className="pointer-events-none absolute left-3.5 top-3 h-4 w-4 text-slate-400" />
            <input
              type="search"
              value={searchTerm}
              onChange={(e) => { setSearchTerm(e.target.value); setPage(1); }}
              placeholder="Search Reg No, Name, Roll No, Email, Mobile, ERP ID..."
              className="w-full rounded-xl border border-slate-200 bg-slate-50 py-2 pl-10 pr-3.5 text-xs text-slate-900 focus:outline-hidden dark:border-slate-800 dark:bg-slate-950 dark:text-white"
            />
          </div>

          <div>
            <select
              value={selectedCourse}
              onChange={(e) => { setSelectedCourse(e.target.value); setPage(1); }}
              className="w-full rounded-xl border border-slate-200 bg-slate-50 py-2 px-3 text-xs text-slate-900 dark:border-slate-800 dark:bg-slate-950 dark:text-white"
            >
              <option value="">All Academic Disciplines</option>
              <option value="B.Tech Computer Science">B.Tech Computer Science</option>
              <option value="MBA in Enterprise Analytics">MBA Analytics</option>
              <option value="B.Pharmacy">B.Pharmacy</option>
            </select>
          </div>

          <div>
            <select
              value={selectedStatus}
              onChange={(e) => { setSelectedStatus(e.target.value); setPage(1); }}
              className="w-full rounded-xl border border-slate-200 bg-slate-50 py-2 px-3 text-xs text-slate-900 dark:border-slate-800 dark:bg-slate-950 dark:text-white"
            >
              <option value="">All Statuses</option>
              <option value="ACTIVE">Active</option>
              <option value="INACTIVE">Inactive</option>
              <option value="TRANSFERRED">Transferred</option>
              <option value="ALUMNI">Alumni</option>
            </select>
          </div>
        </div>

        {/* Bulk Action Controls */}
        {selectedIds.length > 0 && (
          <div className="mt-4 flex items-center justify-between border-t border-slate-100 pt-3 dark:border-slate-800">
            <span className="text-xs font-semibold text-brand-600">
              {selectedIds.length} students selected
            </span>
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => bulkDeleteMutation.mutate(selectedIds)}
                className="inline-flex items-center gap-1 rounded-lg border border-rose-300 bg-rose-50 px-3 py-1.5 text-xs font-semibold text-rose-700 hover:bg-rose-100"
              >
                <Trash2 className="h-3.5 w-3.5" /> Bulk Soft Delete
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Student List Table */}
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200 text-left text-xs dark:divide-slate-800">
            <thead>
              <tr className="bg-slate-50 font-semibold uppercase text-slate-500 dark:bg-slate-950">
                <th className="px-3 py-3 w-8">
                  <input type="checkbox" onChange={handleSelectAll} className="rounded-sm border-slate-300 text-brand-600" />
                </th>
                <th className="px-4 py-3">Registration & Roll No</th>
                <th className="px-4 py-3">Student Full Name</th>
                <th className="px-4 py-3">Contact</th>
                <th className="px-4 py-3">Course & Batch</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
              {isLoading ? (
                <tr><td colSpan={7} className="p-8 text-center text-slate-500">Querying PostgreSQL SIMS records...</td></tr>
              ) : (data?.items || []).length === 0 ? (
                <tr><td colSpan={7} className="p-8 text-center text-slate-500">No matching student records found.</td></tr>
              ) : (
                data?.items.map((s) => (
                  <tr key={s.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                    <td className="px-3 py-3">
                      <input
                        type="checkbox"
                        checked={selectedIds.includes(s.id)}
                        onChange={(e) => {
                          if (e.target.checked) setSelectedIds([...selectedIds, s.id]);
                          else setSelectedIds(selectedIds.filter((id) => id !== s.id));
                        }}
                        className="rounded-sm border-slate-300 text-brand-600"
                      />
                    </td>
                    <td className="px-4 py-3">
                      <div className="font-mono font-bold text-brand-600 dark:text-brand-400">{s.registration_number}</div>
                      <div className="font-mono text-[11px] text-slate-400">{s.roll_number || s.erp_id}</div>
                    </td>
                    <td className="px-4 py-3">
                      <div className="font-bold text-slate-900 dark:text-white">{s.first_name} {s.last_name}</div>
                      <div className="text-[11px] text-slate-500">{s.gender} • DOB: {s.date_of_birth}</div>
                    </td>
                    <td className="px-4 py-3 text-slate-600 dark:text-slate-400">
                      <div>{s.email}</div>
                      <div className="font-mono">{s.phone_number}</div>
                    </td>
                    <td className="px-4 py-3">
                      <div className="font-semibold text-slate-900 dark:text-white">{s.course_name}</div>
                      <div className="text-[11px] text-slate-500">{s.batch_name} ({s.academic_year_code})</div>
                    </td>
                    <td className="px-4 py-3">
                      <span className="rounded-sm bg-emerald-50 px-2 py-0.5 font-bold text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300">
                        {s.status}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-right">
                      <div className="flex items-center justify-end gap-1.5">
                        <button
                          type="button"
                          onClick={() => openProfileModal(s.id)}
                          className="rounded-lg border border-slate-300 bg-white px-2.5 py-1 font-semibold text-slate-700 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200"
                        >
                          Profile
                        </button>
                        <button
                          type="button"
                          onClick={async () => {
                            const p = await studentApi.getStudentProfile(s.id);
                            setQrModalStudent(p);
                          }}
                          className="p-1 text-slate-400 hover:text-brand-600"
                          title="Generate QR ID Card"
                        >
                          <QrCode className="h-4 w-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Tabbed Profile Modal */}
      <StudentTabbedProfileModal
        student={activeProfile}
        onClose={() => setActiveProfile(null)}
        onOpenQR={() => {
          setQrModalStudent(activeProfile);
          setActiveProfile(null);
        }}
      />

      {/* Digital QR Code ID Card Modal */}
      <StudentQRCodeModal
        student={qrModalStudent}
        onClose={() => setQrModalStudent(null)}
      />
    </div>
  );
};
