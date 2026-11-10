import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Users,
  UserPlus,
  Search,
  Filter,
  ShieldCheck,
  ShieldAlert,
  FileText,
  Upload,
  Download,
  Archive,
  RefreshCw,
  CheckCircle2,
  XCircle,
  Eye,
  Trash2,
  FileCheck,
  UserCheck,
  Tag,
  Mail,
  Phone,
  Building,
} from "lucide-react";
import { userService } from "@/services/userService";
import { roleService } from "@/services/roleService";
import {
  CreateUserPayload,
  UserCategory,
  UserDetail,
  UserSummary,
} from "@/types/user.types";

const CATEGORY_TABS: { key: UserCategory; label: string }[] = [
  { key: "ALL", label: "All Users" },
  { key: "STUDENT", label: "Students" },
  { key: "FACULTY", label: "Faculty" },
  { key: "STAFF", label: "Staff" },
  { key: "PARENT", label: "Parents" },
  { key: "RECEPTION", label: "Reception" },
  { key: "LIBRARIAN", label: "Librarian" },
  { key: "ACCOUNTANT", label: "Accountant" },
  { key: "EXAM_CELL", label: "Exam Cell" },
  { key: "CBT_STAFF", label: "CBT Staff" },
  { key: "LMS_STAFF", label: "LMS Staff" },
  { key: "SUPER_ADMIN", label: "Super Admin" },
];

export const UsersManagementPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [search, setSearch] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<UserCategory>("ALL");
  const [isArchivedView, setIsArchivedView] = useState(false);
  const [page, setPage] = useState(1);
  const [selectedUserIds, setSelectedUserIds] = useState<string[]>([]);

  // Modals state
  const [createModalOpen, setCreateModalOpen] = useState(false);
  const [detailUser, setDetailUser] = useState<UserDetail | null>(null);
  const [detailModalOpen, setDetailModalOpen] = useState(false);
  const [documentModalOpen, setDocumentModalOpen] = useState(false);
  const [importModalOpen, setImportModalOpen] = useState(false);

  // New User Form State
  const [newUser, setNewUser] = useState<CreateUserPayload>({
    email: "",
    username: "",
    phone_number: "",
    first_name: "",
    last_name: "",
    password: "",
    user_category: "STUDENT",
    department: "Computer Science & Engineering",
    designation: "Undergraduate Student",
    admission_or_emp_id: "",
    dob: "2004-05-15",
    gender: "Male",
    blood_group: "O+",
    photo_url: "",
    digital_signature_url: "",
    verification_id_type: "AADHAAR",
    verification_id_number: "",
    role_ids: [],
    is_super_admin: false,
  });

  // New Document State
  const [docType, setDocType] = useState("AADHAAR_CARD");
  const [docTitle, setDocTitle] = useState("Aadhaar Card Front & Back");
  const [docUrl, setDocUrl] = useState("https://res.cloudinary.com/my-education-india/doc1.pdf");
  const [docRemarks, setDocRemarks] = useState("Government UIDAI Verified Copy");

  // Import State
  const [importJson, setImportJson] = useState(
    JSON.stringify(
      [
        {
          email: "rajesh.sharma@myeducationindia.com",
          username: "rsharma",
          phone_number: "+919826011122",
          first_name: "Rajesh",
          last_name: "Sharma",
          user_category: "FACULTY",
          department: "Computer Science",
          designation: "Assistant Professor",
          admission_or_emp_id: "EMP-2026-089",
          gender: "Male",
        },
        {
          email: "priya.verma@myeducationindia.com",
          username: "pverma",
          phone_number: "+919826033344",
          first_name: "Priya",
          last_name: "Verma",
          user_category: "STUDENT",
          department: "Artificial Intelligence",
          designation: "B.Tech Student",
          admission_or_emp_id: "STU-2026-104",
          gender: "Female",
        },
      ],
      null,
      2
    )
  );

  // Queries
  const { data, isLoading } = useQuery({
    queryKey: ["users", search, selectedCategory, isArchivedView, page],
    queryFn: () =>
      userService.listUsers({
        search: search || undefined,
        user_category: selectedCategory === "ALL" ? undefined : selectedCategory,
        is_archived: isArchivedView,
        page,
        page_size: 20,
      }),
  });

  const { data: roles = [] } = useQuery({
    queryKey: ["roles"],
    queryFn: () => roleService.listRoles(),
  });

  // Mutations
  const createMutation = useMutation({
    mutationFn: (payload: CreateUserPayload) => userService.createUser(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["users"] });
      setCreateModalOpen(false);
      alert("User account successfully provisioned!");
    },
  });

  const statusMutation = useMutation({
    mutationFn: (params: { userId: string; isActive: boolean }) =>
      userService.toggleUserActive(params.userId, params.isActive),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });

  const archiveMutation = useMutation({
    mutationFn: (userId: string) => userService.archiveUser(userId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });

  const restoreMutation = useMutation({
    mutationFn: (userId: string) => userService.restoreUser(userId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });

  const bulkMutation = useMutation({
    mutationFn: (payload: { action: any }) =>
      userService.executeBulkAction({
        user_ids: selectedUserIds,
        action: payload.action,
      }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["users"] });
      setSelectedUserIds([]);
      alert("Bulk operation successfully applied!");
    },
  });

  const importMutation = useMutation({
    mutationFn: (users: any[]) =>
      userService.bulkImport({
        users,
        default_password: "Welcome@MEI2026",
      }),
    onSuccess: (res) => {
      void queryClient.invalidateQueries({ queryKey: ["users"] });
      setImportModalOpen(false);
      alert(res.message);
    },
  });

  const addDocMutation = useMutation({
    mutationFn: () =>
      userService.addUserDocument(detailUser!.id, {
        document_type: docType,
        document_title: docTitle,
        document_url: docUrl,
        remarks: docRemarks,
      }),
    onSuccess: async () => {
      const refreshed = await userService.getUserDetail(detailUser!.id);
      setDetailUser(refreshed);
      setDocumentModalOpen(false);
      void queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });

  const verifyDocMutation = useMutation({
    mutationFn: (params: { docId: string; status: string }) =>
      userService.verifyUserDocument(detailUser!.id, params.docId, {
        verification_status: params.status,
        remarks: "Audited and verified by institutional registrar",
      }),
    onSuccess: async () => {
      const refreshed = await userService.getUserDetail(detailUser!.id);
      setDetailUser(refreshed);
      void queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });

  // Handlers
  const handleSelectAll = (checked: boolean) => {
    if (checked && data?.items) {
      setSelectedUserIds(data.items.map((u) => u.id));
    } else {
      setSelectedUserIds([]);
    }
  };

  const handleToggleSelect = (userId: string) => {
    setSelectedUserIds((prev) =>
      prev.includes(userId) ? prev.filter((id) => id !== userId) : [...prev, userId]
    );
  };

  const handleOpenDetail = async (userSummary: UserSummary) => {
    const detail = await userService.getUserDetail(userSummary.id);
    setDetailUser(detail);
    setDetailModalOpen(true);
  };

  const handleExport = () => {
    if (!data?.items) return;
    const jsonStr = JSON.stringify(data.items, null, 2);
    const blob = new Blob([jsonStr], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `mei-users-export-${new Date().toISOString().split("T")[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
        <div>
          <div className="flex items-center gap-2">
            <span className="rounded-md bg-indigo-100 px-2 py-0.5 text-xs font-bold text-indigo-800">
              Module 4
            </span>
            <span className="rounded-md bg-emerald-100 px-2 py-0.5 text-xs font-semibold text-emerald-800">
              Enterprise User Directory
            </span>
          </div>
          <h1 className="mt-2 text-xl font-bold text-slate-900">
            Institutional User & Identity Management
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            Provision, manage, audit, and verify accounts across Students, Faculty, Staff, Parents, and Operations.
          </p>
        </div>

        {/* Global Action Buttons */}
        <div className="flex flex-wrap items-center gap-2">
          <button
            type="button"
            onClick={() => setIsArchivedView(!isArchivedView)}
            className={`flex items-center gap-1.5 rounded-lg border px-3 py-2 text-xs font-semibold transition-colors ${
              isArchivedView
                ? "bg-amber-50 border-amber-300 text-amber-800"
                : "border-slate-200 text-slate-600 hover:bg-slate-50"
            }`}
          >
            <Archive className="h-4 w-4" />
            {isArchivedView ? "Archived View (Active)" : "View Archived"}
          </button>
          <button
            type="button"
            onClick={handleExport}
            className="flex items-center gap-1.5 rounded-lg border border-slate-200 px-3 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-50"
          >
            <Download className="h-4 w-4" />
            Export Directory
          </button>
          <button
            type="button"
            onClick={() => setImportModalOpen(true)}
            className="flex items-center gap-1.5 rounded-lg border border-slate-200 px-3 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-50"
          >
            <Upload className="h-4 w-4" />
            Bulk Import
          </button>
          <button
            type="button"
            onClick={() => setCreateModalOpen(true)}
            className="flex items-center gap-1.5 rounded-lg bg-indigo-600 px-4 py-2 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700"
          >
            <UserPlus className="h-4 w-4" />
            Provision User
          </button>
        </div>
      </div>

      {/* Category Pills Bar */}
      <div className="flex overflow-x-auto gap-1 rounded-2xl border border-slate-200 bg-white p-2 shadow-xs">
        {CATEGORY_TABS.map((cat) => (
          <button
            key={cat.key}
            type="button"
            onClick={() => {
              setSelectedCategory(cat.key);
              setPage(1);
            }}
            className={`rounded-xl px-3.5 py-1.5 text-xs font-semibold whitespace-nowrap transition-colors ${
              selectedCategory === cat.key
                ? "bg-indigo-600 text-white shadow-xs"
                : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Bulk Actions Banner (Visible when rows selected) */}
      {selectedUserIds.length > 0 && (
        <div className="flex items-center justify-between rounded-xl bg-indigo-50 border border-indigo-200 px-4 py-3 text-xs text-indigo-900">
          <div className="font-semibold">
            {selectedUserIds.length} users selected across directory
          </div>
          <div className="flex items-center gap-2">
            {!isArchivedView ? (
              <>
                <button
                  type="button"
                  onClick={() => bulkMutation.mutate({ action: "ACTIVATE" })}
                  className="rounded bg-white border border-indigo-300 px-3 py-1 font-semibold text-emerald-700 hover:bg-emerald-50"
                >
                  Activate Selected
                </button>
                <button
                  type="button"
                  onClick={() => bulkMutation.mutate({ action: "DEACTIVATE" })}
                  className="rounded bg-white border border-indigo-300 px-3 py-1 font-semibold text-slate-700 hover:bg-slate-100"
                >
                  Suspend Selected
                </button>
                <button
                  type="button"
                  onClick={() => bulkMutation.mutate({ action: "ARCHIVE" })}
                  className="rounded bg-rose-600 px-3 py-1 font-semibold text-white hover:bg-rose-700 shadow-xs"
                >
                  Archive Selected
                </button>
              </>
            ) : (
              <button
                type="button"
                onClick={() => bulkMutation.mutate({ action: "RESTORE" })}
                className="rounded bg-emerald-600 px-3 py-1 font-semibold text-white hover:bg-emerald-700 shadow-xs"
              >
                Restore Selected Users
              </button>
            )}
          </div>
        </div>
      )}

      {/* Directory Table Card */}
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 pb-4 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <h2 className="text-base font-bold text-slate-900">
              {isArchivedView ? "Archived User Repository" : "Active Campus Directory"}
            </h2>
            <span className="rounded-full bg-slate-100 px-2.5 py-0.5 text-xs text-slate-600 font-semibold">
              {data?.total || 0} registered
            </span>
          </div>

          <div className="relative w-full sm:w-80">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
            <input
              type="search"
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setPage(1);
              }}
              placeholder="Search by name, ID, email, username..."
              className="w-full rounded-lg border border-slate-300 pl-9 pr-3 py-2 text-xs focus:border-indigo-600 focus:outline-hidden"
            />
          </div>
        </div>

        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="border-b border-slate-100 bg-slate-50 text-xs font-semibold text-slate-600">
              <tr>
                <th className="px-3 py-3 w-8">
                  <input
                    type="checkbox"
                    checked={
                      Boolean(data?.items?.length) &&
                      selectedUserIds.length === data?.items?.length
                    }
                    onChange={(e) => handleSelectAll(e.target.checked)}
                    className="rounded border-slate-300 text-indigo-600"
                  />
                </th>
                <th className="px-3 py-3">User & Category</th>
                <th className="px-3 py-3">ID / Department</th>
                <th className="px-3 py-3">Contact</th>
                <th className="px-3 py-3">Verification</th>
                <th className="px-3 py-3">Status</th>
                <th className="px-3 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-xs">
              {isLoading ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-slate-500">
                    Loading users from PostgreSQL database...
                  </td>
                </tr>
              ) : !data?.items?.length ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-slate-500">
                    No users matching criteria.
                  </td>
                </tr>
              ) : (
                data.items.map((u) => {
                  const isSelected = selectedUserIds.includes(u.id);

                  return (
                    <tr
                      key={u.id}
                      className={`hover:bg-slate-50/70 ${isSelected ? "bg-indigo-50/40" : ""}`}
                    >
                      <td className="px-3 py-3">
                        <input
                          type="checkbox"
                          checked={isSelected}
                          onChange={() => handleToggleSelect(u.id)}
                          className="rounded border-slate-300 text-indigo-600"
                        />
                      </td>
                      <td className="px-3 py-3">
                        <div className="flex items-center gap-2.5">
                          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-indigo-100 text-xs font-bold text-indigo-700">
                            {u.first_name[0]}
                            {u.last_name[0]}
                          </div>
                          <div>
                            <div className="font-bold text-slate-900">
                              {u.first_name} {u.last_name}
                            </div>
                            <div className="flex items-center gap-1.5 mt-0.5">
                              <span className="rounded bg-slate-100 px-1.5 py-0.2 text-[10px] font-bold text-slate-700 font-mono">
                                {u.user_category}
                              </span>
                              <span className="font-mono text-slate-400 text-[10px]">
                                @{u.username}
                              </span>
                            </div>
                          </div>
                        </div>
                      </td>
                      <td className="px-3 py-3">
                        <div className="font-semibold text-slate-800">
                          {u.admission_or_emp_id || "ID-Pending"}
                        </div>
                        <div className="text-[11px] text-slate-500">
                          {u.department || "General"}
                        </div>
                      </td>
                      <td className="px-3 py-3 text-slate-600">
                        <div>{u.email}</div>
                        <div className="text-[11px] text-slate-500">{u.phone_number}</div>
                      </td>
                      <td className="px-3 py-3">
                        {u.identity_verification_status === "VERIFIED" ? (
                          <span className="inline-flex items-center gap-1 rounded-full bg-emerald-100 px-2 py-0.5 text-[11px] font-semibold text-emerald-800">
                            <ShieldCheck className="h-3 w-3" />
                            Verified
                          </span>
                        ) : u.identity_verification_status === "REJECTED" ? (
                          <span className="inline-flex items-center gap-1 rounded-full bg-rose-100 px-2 py-0.5 text-[11px] font-semibold text-rose-800">
                            <ShieldAlert className="h-3 w-3" />
                            Rejected
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 rounded-full bg-amber-100 px-2 py-0.5 text-[11px] font-semibold text-amber-800">
                            <ShieldAlert className="h-3 w-3" />
                            Pending
                          </span>
                        )}
                      </td>
                      <td className="px-3 py-3">
                        {u.is_archived ? (
                          <span className="rounded bg-rose-100 px-2 py-0.5 text-[10px] font-bold text-rose-800">
                            Archived
                          </span>
                        ) : u.is_active ? (
                          <span className="rounded bg-emerald-100 px-2 py-0.5 text-[10px] font-bold text-emerald-800">
                            Active
                          </span>
                        ) : (
                          <span className="rounded bg-slate-100 px-2 py-0.5 text-[10px] font-bold text-slate-600">
                            Suspended
                          </span>
                        )}
                      </td>
                      <td className="px-3 py-3 text-right space-x-1.5">
                        <button
                          type="button"
                          onClick={() => void handleOpenDetail(u)}
                          className="rounded-md bg-indigo-50 p-1.5 text-indigo-700 hover:bg-indigo-100"
                          title="View Profile & Documents"
                        >
                          <Eye className="h-3.5 w-3.5" />
                        </button>
                        {!u.is_archived ? (
                          <button
                            type="button"
                            onClick={() => {
                              if (confirm(`Archive user ${u.username}?`)) {
                                void archiveMutation.mutate(u.id);
                              }
                            }}
                            className="rounded-md bg-rose-50 p-1.5 text-rose-600 hover:bg-rose-100"
                            title="Archive User"
                          >
                            <Archive className="h-3.5 w-3.5" />
                          </button>
                        ) : (
                          <button
                            type="button"
                            onClick={() => void restoreMutation.mutate(u.id)}
                            className="rounded-md bg-emerald-50 p-1.5 text-emerald-700 hover:bg-emerald-100"
                            title="Restore User"
                          >
                            <RefreshCw className="h-3.5 w-3.5" />
                          </button>
                        )}
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* User Profile & Document Management Drawer Modal */}
      {detailModalOpen && detailUser && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-xs overflow-y-auto">
          <div className="relative w-full max-w-3xl max-h-[90vh] flex flex-col rounded-2xl bg-white shadow-2xl">
            {/* Drawer Header */}
            <div className="flex items-center justify-between border-b border-slate-100 px-6 py-4">
              <div className="flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-indigo-600 text-base font-bold text-white shadow-xs">
                  {detailUser.first_name[0]}
                  {detailUser.last_name[0]}
                </div>
                <div>
                  <h3 className="text-base font-bold text-slate-900">
                    {detailUser.first_name} {detailUser.last_name}
                  </h3>
                  <div className="flex items-center gap-2 text-xs text-slate-500">
                    <span className="font-mono text-indigo-700 font-bold">
                      {detailUser.user_category}
                    </span>
                    <span>&bull;</span>
                    <span>{detailUser.department || "General Department"}</span>
                    <span>&bull;</span>
                    <span className="font-mono">{detailUser.admission_or_emp_id}</span>
                  </div>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setDetailModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 font-bold text-xl"
              >
                &times;
              </button>
            </div>

            {/* Drawer Body */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
              {/* Demographics Card */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 rounded-xl border border-slate-200 bg-slate-50 p-4 text-xs">
                <div>
                  <span className="text-slate-500 font-medium">Date of Birth</span>
                  <div className="font-semibold text-slate-900 mt-0.5">
                    {detailUser.dob || "Not Provided"}
                  </div>
                </div>
                <div>
                  <span className="text-slate-500 font-medium">Gender</span>
                  <div className="font-semibold text-slate-900 mt-0.5">
                    {detailUser.gender || "Not Specified"}
                  </div>
                </div>
                <div>
                  <span className="text-slate-500 font-medium">Blood Group</span>
                  <div className="font-semibold text-slate-900 mt-0.5">
                    {detailUser.blood_group || "Not Recorded"}
                  </div>
                </div>
                <div>
                  <span className="text-slate-500 font-medium">Identity Status</span>
                  <div className="font-bold text-indigo-700 mt-0.5">
                    {detailUser.identity_verification_status}
                  </div>
                </div>
              </div>

              {/* Digital Signature & Photos */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="rounded-xl border border-slate-200 p-4">
                  <span className="text-xs font-bold text-slate-900 uppercase">
                    Profile Photo Asset
                  </span>
                  <div className="mt-2 h-28 flex items-center justify-center rounded-lg bg-slate-100 border border-dashed border-slate-300 text-xs text-slate-500">
                    {detailUser.photo_url ? (
                      <img
                        src={detailUser.photo_url}
                        alt="Profile"
                        className="h-full object-contain"
                      />
                    ) : (
                      "Default Cloudinary Avatar"
                    )}
                  </div>
                </div>

                <div className="rounded-xl border border-slate-200 p-4">
                  <span className="text-xs font-bold text-slate-900 uppercase">
                    Verified Digital Signature
                  </span>
                  <div className="mt-2 h-28 flex items-center justify-center rounded-lg bg-slate-100 border border-dashed border-slate-300 text-xs text-slate-500">
                    {detailUser.digital_signature_url ? (
                      <img
                        src={detailUser.digital_signature_url}
                        alt="Signature"
                        className="h-full object-contain"
                      />
                    ) : (
                      "Digital Signature on File (e-Sign)"
                    )}
                  </div>
                </div>
              </div>

              {/* Uploaded Documents List */}
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <FileText className="h-4 w-4 text-indigo-600" />
                    <h4 className="text-xs font-bold text-slate-900 uppercase tracking-wide">
                      Verification Documents ({detailUser.documents.length})
                    </h4>
                  </div>
                  <button
                    type="button"
                    onClick={() => setDocumentModalOpen(true)}
                    className="flex items-center gap-1 rounded bg-indigo-600 px-2.5 py-1 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700"
                  >
                    <Upload className="h-3.5 w-3.5" />
                    Upload Document
                  </button>
                </div>

                <div className="space-y-2">
                  {!detailUser.documents.length ? (
                    <div className="rounded-xl border border-dashed border-slate-300 p-6 text-center text-xs text-slate-500">
                      No documents uploaded yet. Add government IDs, degrees, or joining letters.
                    </div>
                  ) : (
                    detailUser.documents.map((doc) => (
                      <div
                        key={doc.id}
                        className="flex items-center justify-between rounded-xl border border-slate-200 bg-white p-3 shadow-2xs"
                      >
                        <div>
                          <div className="font-semibold text-slate-900 text-xs">
                            {doc.document_title}
                          </div>
                          <div className="flex items-center gap-2 text-[11px] text-slate-500 mt-0.5">
                            <span className="font-mono">{doc.document_type}</span>
                            <span>&bull;</span>
                            <span>{doc.mime_type}</span>
                            {doc.remarks && (
                              <>
                                <span>&bull;</span>
                                <span className="italic">{doc.remarks}</span>
                              </>
                            )}
                          </div>
                        </div>

                        <div className="flex items-center gap-2">
                          {doc.verification_status === "VERIFIED" ? (
                            <span className="rounded bg-emerald-100 px-2 py-0.5 text-[10px] font-bold text-emerald-800">
                              VERIFIED
                            </span>
                          ) : (
                            <div className="flex items-center gap-1">
                              <button
                                type="button"
                                onClick={() =>
                                  verifyDocMutation.mutate({
                                    docId: doc.id,
                                    status: "VERIFIED",
                                  })
                                }
                                className="rounded bg-emerald-50 px-2 py-1 text-[11px] font-semibold text-emerald-700 hover:bg-emerald-100"
                              >
                                Approve
                              </button>
                              <button
                                type="button"
                                onClick={() =>
                                  verifyDocMutation.mutate({
                                    docId: doc.id,
                                    status: "REJECTED",
                                  })
                                }
                                className="rounded bg-rose-50 px-2 py-1 text-[11px] font-semibold text-rose-700 hover:bg-rose-100"
                              >
                                Reject
                              </button>
                            </div>
                          )}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>

            {/* Drawer Footer */}
            <div className="flex justify-end border-t border-slate-100 px-6 py-4">
              <button
                type="button"
                onClick={() => setDetailModalOpen(false)}
                className="rounded-lg border border-slate-200 px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-50"
              >
                Close Profile
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Provision User Modal */}
      {createModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-xs overflow-y-auto">
          <div className="relative w-full max-w-2xl rounded-2xl bg-white p-6 shadow-2xl">
            <h3 className="text-base font-bold text-slate-900">
              Provision Institutional User Account
            </h3>
            <p className="mt-1 text-xs text-slate-500">
              Create an account with role assignments, department linkage, and demographic baseline.
            </p>

            <form
              onSubmit={(e) => {
                e.preventDefault();
                createMutation.mutate(newUser);
              }}
              className="mt-4 space-y-3"
            >
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">First Name</label>
                  <input
                    type="text"
                    required
                    value={newUser.first_name}
                    onChange={(e) => setNewUser({ ...newUser, first_name: e.target.value })}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 text-xs"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Last Name</label>
                  <input
                    type="text"
                    required
                    value={newUser.last_name}
                    onChange={(e) => setNewUser({ ...newUser, last_name: e.target.value })}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 text-xs"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Email Address</label>
                  <input
                    type="email"
                    required
                    value={newUser.email}
                    onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 text-xs"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Username</label>
                  <input
                    type="text"
                    required
                    value={newUser.username}
                    onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 text-xs font-mono"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Phone Number</label>
                  <input
                    type="text"
                    required
                    placeholder="+919826012345"
                    value={newUser.phone_number}
                    onChange={(e) => setNewUser({ ...newUser, phone_number: e.target.value })}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 text-xs font-mono"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Password</label>
                  <input
                    type="password"
                    required
                    placeholder="Must meet policy"
                    value={newUser.password}
                    onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 text-xs"
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">User Category</label>
                  <select
                    value={newUser.user_category}
                    onChange={(e) => setNewUser({ ...newUser, user_category: e.target.value })}
                    className="mt-1 block w-full rounded border border-slate-300 px-2 py-1.5 text-xs font-semibold"
                  >
                    <option value="STUDENT">STUDENT</option>
                    <option value="FACULTY">FACULTY</option>
                    <option value="STAFF">STAFF</option>
                    <option value="PARENT">PARENT</option>
                    <option value="RECEPTION">RECEPTION</option>
                    <option value="LIBRARIAN">LIBRARIAN</option>
                    <option value="ACCOUNTANT">ACCOUNTANT</option>
                    <option value="EXAM_CELL">EXAM_CELL</option>
                    <option value="CBT_STAFF">CBT_STAFF</option>
                    <option value="LMS_STAFF">LMS_STAFF</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700">Department</label>
                  <input
                    type="text"
                    value={newUser.department || ""}
                    onChange={(e) => setNewUser({ ...newUser, department: e.target.value })}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 text-xs"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700">Roll / Emp ID</label>
                  <input
                    type="text"
                    placeholder="MEI-2026-X"
                    value={newUser.admission_or_emp_id || ""}
                    onChange={(e) => setNewUser({ ...newUser, admission_or_emp_id: e.target.value })}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 text-xs font-mono"
                  />
                </div>
              </div>

              <div className="mt-5 flex justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setCreateModalOpen(false)}
                  className="rounded border border-slate-200 px-3 py-1.5 text-xs font-semibold text-slate-600 hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createMutation.isPending}
                  className="rounded bg-indigo-600 px-4 py-1.5 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
                >
                  {createMutation.isPending ? "Provisioning..." : "Provision User"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Upload Document Modal */}
      {documentModalOpen && detailUser && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-xs">
          <div className="relative w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl">
            <h3 className="text-base font-bold text-slate-900">Upload Verification Document</h3>
            <p className="mt-1 text-xs text-slate-500">
              Attach official identity proofs or educational certificates for {detailUser.first_name}.
            </p>

            <div className="mt-4 space-y-3 text-xs">
              <div>
                <label className="font-semibold text-slate-700">Document Type</label>
                <select
                  value={docType}
                  onChange={(e) => setDocType(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                >
                  <option value="AADHAAR_CARD">Aadhaar Card</option>
                  <option value="PAN_CARD">PAN Card</option>
                  <option value="10TH_MARKSHEET">10th Marksheet</option>
                  <option value="12TH_MARKSHEET">12th Marksheet</option>
                  <option value="DEGREE_CERTIFICATE">Degree Certificate</option>
                  <option value="JOINING_LETTER">Appointment / Joining Letter</option>
                </select>
              </div>

              <div>
                <label className="font-semibold text-slate-700">Document Title</label>
                <input
                  type="text"
                  value={docTitle}
                  onChange={(e) => setDocTitle(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                />
              </div>

              <div>
                <label className="font-semibold text-slate-700">Cloudinary Document URL</label>
                <input
                  type="text"
                  value={docUrl}
                  onChange={(e) => setDocUrl(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 font-mono"
                />
              </div>

              <div>
                <label className="font-semibold text-slate-700">Verification Notes</label>
                <input
                  type="text"
                  value={docRemarks}
                  onChange={(e) => setDocRemarks(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                />
              </div>
            </div>

            <div className="mt-5 flex justify-end gap-2 pt-3 border-t border-slate-100">
              <button
                type="button"
                onClick={() => setDocumentModalOpen(false)}
                className="rounded border border-slate-200 px-3 py-1.5 text-xs font-semibold text-slate-600 hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={() => addDocMutation.mutate()}
                disabled={addDocMutation.isPending}
                className="rounded bg-indigo-600 px-4 py-1.5 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
              >
                {addDocMutation.isPending ? "Uploading..." : "Save Document"}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Bulk Import Modal */}
      {importModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-xs">
          <div className="relative w-full max-w-lg rounded-2xl bg-white p-6 shadow-2xl">
            <h3 className="text-base font-bold text-slate-900">Bulk Import User Records</h3>
            <p className="mt-1 text-xs text-slate-500">
              Paste user JSON records to provision accounts in bulk with default password.
            </p>

            <div className="mt-4">
              <textarea
                rows={8}
                value={importJson}
                onChange={(e) => setImportJson(e.target.value)}
                className="w-full rounded-lg border border-slate-300 p-2.5 font-mono text-xs focus:border-indigo-600 focus:outline-hidden"
              />
            </div>

            <div className="mt-4 flex justify-end gap-2">
              <button
                type="button"
                onClick={() => setImportModalOpen(false)}
                className="rounded border border-slate-200 px-3 py-1.5 text-xs font-semibold text-slate-600 hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={() => {
                  try {
                    const parsed = JSON.parse(importJson);
                    importMutation.mutate(parsed);
                  } catch (err) {
                    alert("Invalid JSON format. Please verify records.");
                  }
                }}
                disabled={importMutation.isPending}
                className="rounded bg-indigo-600 px-4 py-1.5 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
              >
                {importMutation.isPending ? "Importing..." : "Execute Bulk Import"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
