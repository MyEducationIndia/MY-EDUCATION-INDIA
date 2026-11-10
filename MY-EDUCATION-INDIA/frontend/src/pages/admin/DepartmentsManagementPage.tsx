import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Building2,
  FolderTree,
  UserCheck,
  Workflow,
  Plus,
  GitBranch,
  ShieldCheck,
  Mail,
  Phone,
  MapPin,
  Edit2,
  Trash2,
  CheckCircle2,
  Layers,
  Award,
  ChevronRight,
  ChevronDown,
  Settings2,
} from "lucide-react";
import { departmentService } from "@/services/departmentService";
import {
  CreateDepartmentPayload,
  CreateDesignationPayload,
  DepartmentDetail,
  DepartmentSummary,
  DesignationItem,
} from "@/types/department.types";

const ALL_WORKFLOWS = [
  { code: "LEAVE_APPROVAL", label: "Faculty & Staff Leave Approval" },
  { code: "PURCHASE_REQUISITION", label: "Procurement & Purchase Requisition" },
  { code: "CURRICULUM_SIGN_OFF", label: "Academic Syllabus & Curriculum Review" },
  { code: "EXAM_PAPER_AUDIT", label: "Confidential Exam Paper Audit" },
  { code: "GRADE_MODERATION", label: "Semester Grade Moderation & Approval" },
  { code: "FEE_RECONCILIATION", label: "Student Fee Concession & Waiver" },
  { code: "LAB_REQUISITION", label: "Lab Equipment & Consumables Requisition" },
  { code: "HOSTEL_ALLOTMENT", label: "Hostel & Room Allotment Approval" },
];

export const DepartmentsManagementPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<"departments" | "designations" | "workflows">(
    "departments"
  );
  const [selectedType, setSelectedType] = useState<string>("ALL");
  const [selectedCadre, setSelectedCadre] = useState<string>("ALL");
  const [expandedDeptIds, setExpandedDeptIds] = useState<string[]>([]);

  // Modals state
  const [deptModalOpen, setDeptModalOpen] = useState(false);
  const [parentDeptForSub, setParentDeptForSub] = useState<DepartmentSummary | null>(null);
  const [editingDept, setEditingDept] = useState<DepartmentSummary | null>(null);
  const [desigModalOpen, setDesigModalOpen] = useState(false);
  const [editingDesig, setEditingDesig] = useState<DesignationItem | null>(null);
  const [workflowModalOpen, setWorkflowModalOpen] = useState(false);
  const [selectedDeptForWorkflow, setSelectedDeptForWorkflow] = useState<DepartmentSummary | null>(
    null
  );
  const [selectedWorkflows, setSelectedWorkflows] = useState<string[]>([]);

  // Department Form State
  const [deptCode, setDeptCode] = useState("");
  const [deptName, setDeptName] = useState("");
  const [deptType, setDeptType] = useState("ACADEMIC");
  const [deptLocation, setDeptLocation] = useState("");
  const [deptEmail, setDeptEmail] = useState("");
  const [deptPhone, setDeptPhone] = useState("");
  const [deptHeadName, setDeptHeadName] = useState("");
  const [deptHeadDesignation, setDeptHeadDesignation] = useState("Head of Department");

  // Designation Form State
  const [desigCode, setDesigCode] = useState("");
  const [desigTitle, setDesigTitle] = useState("");
  const [desigCadre, setDesigCadre] = useState("TEACHING");
  const [desigLevel, setDesigLevel] = useState(3);
  const [desigDeptId, setDesigDeptId] = useState<string>("");
  const [desigDesc, setDesigDesc] = useState("");

  // Queries
  const { data: departments = [], isLoading: deptsLoading } = useQuery({
    queryKey: ["departments", selectedType],
    queryFn: () =>
      departmentService.listDepartments({
        department_type: selectedType === "ALL" ? undefined : selectedType,
      }),
  });

  const { data: designations = [], isLoading: desigsLoading } = useQuery({
    queryKey: ["designations", selectedCadre],
    queryFn: () =>
      departmentService.listDesignations({
        cadre: selectedCadre === "ALL" ? undefined : selectedCadre,
      }),
  });

  // Filter parents vs sub-departments
  const parentDepartments = departments.filter((d) => !d.parent_department_id);
  const getSubDepartments = (parentId: string) =>
    departments.filter((d) => d.parent_department_id === parentId);

  // Mutations
  const createDeptMutation = useMutation({
    mutationFn: (payload: CreateDepartmentPayload) => departmentService.createDepartment(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["departments"] });
      setDeptModalOpen(false);
      resetDeptForm();
      alert("Department successfully registered!");
    },
  });

  const updateDeptMutation = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: any }) =>
      departmentService.updateDepartment(id, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["departments"] });
      setDeptModalOpen(false);
      resetDeptForm();
      alert("Department successfully updated!");
    },
  });

  const deleteDeptMutation = useMutation({
    mutationFn: (id: string) => departmentService.deleteDepartment(id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["departments"] });
    },
  });

  const createDesigMutation = useMutation({
    mutationFn: (payload: CreateDesignationPayload) => departmentService.createDesignation(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["designations"] });
      setDesigModalOpen(false);
      resetDesigForm();
      alert("Designation successfully added!");
    },
  });

  const deleteDesigMutation = useMutation({
    mutationFn: (id: string) => departmentService.deleteDesignation(id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["designations"] });
    },
  });

  const assignWorkflowsMutation = useMutation({
    mutationFn: ({ id, workflows }: { id: string; workflows: string[] }) =>
      departmentService.assignWorkflows(id, workflows),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["departments"] });
      setWorkflowModalOpen(false);
      alert("Department workflow assignments updated!");
    },
  });

  const toggleExpand = (id: string) => {
    setExpandedDeptIds((prev) =>
      prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id]
    );
  };

  const resetDeptForm = () => {
    setDeptCode("");
    setDeptName("");
    setDeptType("ACADEMIC");
    setDeptLocation("");
    setDeptEmail("");
    setDeptPhone("");
    setDeptHeadName("");
    setDeptHeadDesignation("Head of Department");
    setParentDeptForSub(null);
    setEditingDept(null);
  };

  const resetDesigForm = () => {
    setDesigCode("");
    setDesigTitle("");
    setDesigCadre("TEACHING");
    setDesigLevel(3);
    setDesigDeptId("");
    setDesigDesc("");
    setEditingDesig(null);
  };

  const handleOpenCreateSub = (parent: DepartmentSummary) => {
    resetDeptForm();
    setParentDeptForSub(parent);
    setDeptType(parent.department_type);
    setDeptCode(`${parent.code}-`);
    setDeptModalOpen(true);
  };

  const handleOpenEditDept = (dept: DepartmentSummary) => {
    setEditingDept(dept);
    setDeptCode(dept.code);
    setDeptName(dept.name);
    setDeptType(dept.department_type);
    setDeptLocation(dept.location_room || "");
    setDeptEmail(dept.contact_email || "");
    setDeptPhone(dept.contact_phone || "");
    setDeptHeadName(dept.head_name || "");
    setDeptHeadDesignation(dept.head_designation || "Head of Department");
    setParentDeptForSub(null);
    setDeptModalOpen(true);
  };

  const handleOpenWorkflowModal = (dept: DepartmentSummary) => {
    setSelectedDeptForWorkflow(dept);
    setSelectedWorkflows(dept.workflow_assignments || []);
    setWorkflowModalOpen(true);
  };

  const handleSaveDept = (e: React.FormEvent) => {
    e.preventDefault();
    if (editingDept) {
      void updateDeptMutation.mutate({
        id: editingDept.id,
        payload: {
          name: deptName,
          department_type: deptType,
          location_room: deptLocation,
          contact_email: deptEmail || null,
          contact_phone: deptPhone || null,
          head_designation: deptHeadDesignation,
        },
      });
    } else {
      void createDeptMutation.mutate({
        code: deptCode.toUpperCase(),
        name: deptName,
        department_type: deptType,
        parent_department_id: parentDeptForSub ? parentDeptForSub.id : null,
        location_room: deptLocation,
        contact_email: deptEmail || null,
        contact_phone: deptPhone || null,
        head_designation: deptHeadDesignation,
        workflow_assignments: [],
      });
    }
  };

  const handleSaveDesig = (e: React.FormEvent) => {
    e.preventDefault();
    void createDesigMutation.mutate({
      code: desigCode.toUpperCase(),
      title: desigTitle,
      cadre: desigCadre,
      level: Number(desigLevel),
      department_id: desigDeptId ? desigDeptId : null,
      description: desigDesc,
    });
  };

  const handleToggleWorkflow = (wfCode: string) => {
    setSelectedWorkflows((prev) =>
      prev.includes(wfCode) ? prev.filter((c) => c !== wfCode) : [...prev, wfCode]
    );
  };

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
        <div>
          <div className="flex items-center gap-2">
            <span className="rounded-md bg-indigo-100 px-2 py-0.5 text-xs font-bold text-indigo-800">
              Module 5
            </span>
            <span className="rounded-md bg-emerald-100 px-2 py-0.5 text-xs font-semibold text-emerald-800">
              Department Governance
            </span>
          </div>
          <h1 className="mt-2 text-xl font-bold text-slate-900">
            Departments, Hierarchy & Designations
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            Configure primary academic departments, sub-departments, institutional designations, and approval workflows.
          </p>
        </div>

        {/* Tab Controls */}
        <div className="flex flex-wrap items-center gap-1 rounded-xl bg-slate-100 p-1">
          <button
            type="button"
            onClick={() => setActiveTab("departments")}
            className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
              activeTab === "departments"
                ? "bg-white text-indigo-700 shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Departments & Hierarchy ({parentDepartments.length})
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("designations")}
            className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
              activeTab === "designations"
                ? "bg-white text-indigo-700 shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Designations & Cadres ({designations.length})
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("workflows")}
            className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
              activeTab === "workflows"
                ? "bg-white text-indigo-700 shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Workflow Matrix
          </button>
        </div>
      </div>

      {/* Departments & Hierarchy Tab */}
      {activeTab === "departments" && (
        <div className="space-y-4">
          {/* Controls Bar */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-slate-700 uppercase">Department Type:</span>
              <div className="flex flex-wrap gap-1">
                {["ALL", "ACADEMIC", "ADMINISTRATIVE", "OPERATIONAL", "EXAMINATION", "FINANCE"].map(
                  (t) => (
                    <button
                      key={t}
                      type="button"
                      onClick={() => setSelectedType(t)}
                      className={`rounded-lg px-2.5 py-1 text-xs font-semibold transition-colors ${
                        selectedType === t
                          ? "bg-indigo-600 text-white shadow-xs"
                          : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                      }`}
                    >
                      {t}
                    </button>
                  )
                )}
              </div>
            </div>

            <button
              type="button"
              onClick={() => {
                resetDeptForm();
                setDeptModalOpen(true);
              }}
              className="flex items-center gap-1.5 rounded-lg bg-indigo-600 px-4 py-2 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700"
            >
              <Plus className="h-4 w-4" />
              New Department
            </button>
          </div>

          {/* Departments Hierarchy Tree */}
          <div className="space-y-3">
            {deptsLoading ? (
              <div className="rounded-2xl border border-slate-200 bg-white p-12 text-center text-xs text-slate-500">
                Loading departments from PostgreSQL database...
              </div>
            ) : !parentDepartments.length ? (
              <div className="rounded-2xl border border-slate-200 bg-white p-12 text-center text-xs text-slate-500">
                No departments found for the selected category.
              </div>
            ) : (
              parentDepartments.map((dept) => {
                const subDepts = getSubDepartments(dept.id);
                const isExpanded = expandedDeptIds.includes(dept.id);

                return (
                  <div
                    key={dept.id}
                    className="rounded-2xl border border-slate-200 bg-white shadow-2xs overflow-hidden transition-all"
                  >
                    {/* Primary Department Header */}
                    <div className="flex flex-col md:flex-row md:items-center md:justify-between p-5 gap-4 bg-white hover:bg-slate-50/50">
                      <div className="flex items-start gap-3">
                        {subDepts.length > 0 ? (
                          <button
                            type="button"
                            onClick={() => toggleExpand(dept.id)}
                            className="mt-0.5 rounded p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-700"
                          >
                            {isExpanded ? (
                              <ChevronDown className="h-4 w-4" />
                            ) : (
                              <ChevronRight className="h-4 w-4" />
                            )}
                          </button>
                        ) : (
                          <div className="mt-0.5 h-6 w-6 flex items-center justify-center text-slate-300">
                            &bull;
                          </div>
                        )}

                        <div>
                          <div className="flex items-center gap-2">
                            <h3 className="text-base font-bold text-slate-900">{dept.name}</h3>
                            <span className="font-mono text-xs font-bold rounded bg-indigo-50 px-2 py-0.5 text-indigo-700 border border-indigo-200">
                              {dept.code}
                            </span>
                            <span
                              className={`rounded px-2 py-0.5 text-[10px] font-bold ${
                                dept.department_type === "ACADEMIC"
                                  ? "bg-purple-100 text-purple-800"
                                  : dept.department_type === "EXAMINATION"
                                  ? "bg-amber-100 text-amber-800"
                                  : dept.department_type === "FINANCE"
                                  ? "bg-emerald-100 text-emerald-800"
                                  : "bg-slate-100 text-slate-700"
                              }`}
                            >
                              {dept.department_type}
                            </span>
                          </div>

                          <div className="mt-2 flex flex-wrap items-center gap-4 text-xs text-slate-500">
                            {dept.location_room && (
                              <div className="flex items-center gap-1">
                                <MapPin className="h-3.5 w-3.5 text-slate-400" />
                                <span>{dept.location_room}</span>
                              </div>
                            )}
                            <div className="flex items-center gap-1">
                              <UserCheck className="h-3.5 w-3.5 text-indigo-500" />
                              <span className="font-semibold text-slate-700">
                                {dept.head_name || "HOD Office"}
                              </span>
                              <span className="text-slate-400 font-mono text-[11px]">
                                ({dept.head_designation || "Head"})
                              </span>
                            </div>
                            {subDepts.length > 0 && (
                              <div className="flex items-center gap-1 text-indigo-700 font-semibold">
                                <GitBranch className="h-3.5 w-3.5" />
                                <span>{subDepts.length} Specialized Sub-Departments</span>
                              </div>
                            )}
                          </div>

                          {/* Workflows Assigned */}
                          {dept.workflow_assignments.length > 0 && (
                            <div className="mt-3 flex flex-wrap gap-1.5">
                              {dept.workflow_assignments.map((wf) => (
                                <span
                                  key={wf}
                                  className="inline-flex items-center gap-1 rounded bg-slate-100 px-2 py-0.5 text-[10px] font-mono text-slate-700"
                                >
                                  <Workflow className="h-2.5 w-2.5 text-indigo-500" />
                                  {wf}
                                </span>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>

                      {/* Department Actions */}
                      <div className="flex items-center gap-1.5 self-end md:self-center">
                        <button
                          type="button"
                          onClick={() => handleOpenCreateSub(dept)}
                          className="flex items-center gap-1 rounded-lg bg-indigo-50 px-2.5 py-1.5 text-xs font-semibold text-indigo-700 hover:bg-indigo-100"
                        >
                          <Plus className="h-3.5 w-3.5" />
                          Sub-Dept
                        </button>
                        <button
                          type="button"
                          onClick={() => handleOpenWorkflowModal(dept)}
                          className="flex items-center gap-1 rounded-lg bg-slate-100 px-2.5 py-1.5 text-xs font-semibold text-slate-700 hover:bg-slate-200"
                          title="Assign Approval Workflows"
                        >
                          <Settings2 className="h-3.5 w-3.5" />
                          Workflows
                        </button>
                        <button
                          type="button"
                          onClick={() => handleOpenEditDept(dept)}
                          className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-700"
                          title="Edit Department"
                        >
                          <Edit2 className="h-3.5 w-3.5" />
                        </button>
                        <button
                          type="button"
                          onClick={() => {
                            if (confirm(`Delete department ${dept.name}?`)) {
                              void deleteDeptMutation.mutate(dept.id);
                            }
                          }}
                          className="rounded-lg p-1.5 text-rose-400 hover:bg-rose-50 hover:text-rose-600"
                          title="Delete Department"
                        >
                          <Trash2 className="h-3.5 w-3.5" />
                        </button>
                      </div>
                    </div>

                    {/* Sub-departments Dropdown Accordion */}
                    {isExpanded && subDepts.length > 0 && (
                      <div className="bg-slate-50/70 border-t border-slate-100 p-4 space-y-2">
                        <div className="text-[11px] font-bold text-slate-500 uppercase tracking-wide px-3">
                          Child Sub-Departments & Centers of Excellence
                        </div>
                        {subDepts.map((sub) => (
                          <div
                            key={sub.id}
                            className="flex items-center justify-between rounded-xl border border-slate-200 bg-white p-3 shadow-2xs ml-6"
                          >
                            <div className="flex items-center gap-2.5">
                              <GitBranch className="h-4 w-4 text-indigo-500 shrink-0" />
                              <div>
                                <div className="flex items-center gap-2">
                                  <span className="font-bold text-xs text-slate-900">{sub.name}</span>
                                  <span className="font-mono text-[10px] font-bold rounded bg-slate-100 px-1.5 py-0.2 text-slate-700">
                                    {sub.code}
                                  </span>
                                </div>
                                <div className="text-[11px] text-slate-500 mt-0.5">
                                  Location: {sub.location_room || "Assigned in Lab Wing"}
                                </div>
                              </div>
                            </div>

                            <div className="flex items-center gap-1.5">
                              <button
                                type="button"
                                onClick={() => handleOpenWorkflowModal(sub)}
                                className="rounded p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-700"
                                title="Assign Workflows"
                              >
                                <Settings2 className="h-3.5 w-3.5" />
                              </button>
                              <button
                                type="button"
                                onClick={() => {
                                  if (confirm(`Remove sub-department ${sub.name}?`)) {
                                    void deleteDeptMutation.mutate(sub.id);
                                  }
                                }}
                                className="rounded p-1 text-rose-400 hover:bg-rose-50 hover:text-rose-600"
                              >
                                <Trash2 className="h-3.5 w-3.5" />
                              </button>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })
            )}
          </div>
        </div>
      )}

      {/* Designations & Cadres Tab */}
      {activeTab === "designations" && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-slate-700 uppercase">Cadre Filter:</span>
              <div className="flex flex-wrap gap-1">
                {["ALL", "TEACHING", "NON_TEACHING", "ADMINISTRATIVE", "EXECUTIVE", "SUPPORT"].map(
                  (c) => (
                    <button
                      key={c}
                      type="button"
                      onClick={() => setSelectedCadre(c)}
                      className={`rounded-lg px-2.5 py-1 text-xs font-semibold transition-colors ${
                        selectedCadre === c
                          ? "bg-indigo-600 text-white shadow-xs"
                          : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                      }`}
                    >
                      {c}
                    </button>
                  )
                )}
              </div>
            </div>

            <button
              type="button"
              onClick={() => {
                resetDesigForm();
                setDesigModalOpen(true);
              }}
              className="flex items-center gap-1.5 rounded-lg bg-indigo-600 px-4 py-2 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700"
            >
              <Plus className="h-4 w-4" />
              New Designation
            </button>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead className="border-b border-slate-100 bg-slate-50 text-xs font-semibold text-slate-600">
                <tr>
                  <th className="px-3 py-3">Code</th>
                  <th className="px-3 py-3">Designation Title</th>
                  <th className="px-3 py-3">Cadre</th>
                  <th className="px-3 py-3">Hierarchy Level</th>
                  <th className="px-3 py-3">Department</th>
                  <th className="px-3 py-3">Status</th>
                  <th className="px-3 py-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-xs">
                {desigsLoading ? (
                  <tr>
                    <td colSpan={7} className="py-12 text-center text-slate-500">
                      Loading designations...
                    </td>
                  </tr>
                ) : (
                  designations.map((ds) => (
                    <tr key={ds.id} className="hover:bg-slate-50/70">
                      <td className="px-3 py-3 font-mono font-bold text-indigo-700">{ds.code}</td>
                      <td className="px-3 py-3 font-semibold text-slate-900">
                        <div>{ds.title}</div>
                        {ds.description && (
                          <div className="text-[11px] text-slate-400 line-clamp-1">
                            {ds.description}
                          </div>
                        )}
                      </td>
                      <td className="px-3 py-3">
                        <span className="rounded bg-slate-100 px-2 py-0.5 font-medium text-slate-700">
                          {ds.cadre}
                        </span>
                      </td>
                      <td className="px-3 py-3 font-bold text-slate-700">Level {ds.level}</td>
                      <td className="px-3 py-3 text-slate-600">
                        {ds.department_id ? "Department Specific" : "Campus Wide"}
                      </td>
                      <td className="px-3 py-3">
                        <span className="rounded bg-emerald-100 px-2 py-0.5 text-[10px] font-bold text-emerald-800">
                          ACTIVE
                        </span>
                      </td>
                      <td className="px-3 py-3 text-right">
                        <button
                          type="button"
                          onClick={() => {
                            if (confirm(`Delete designation ${ds.title}?`)) {
                              void deleteDesigMutation.mutate(ds.id);
                            }
                          }}
                          className="rounded p-1 text-rose-500 hover:bg-rose-50"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Workflow Assignment Matrix Tab */}
      {activeTab === "workflows" && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
          <div>
            <h2 className="text-base font-bold text-slate-900">
              Department Approval & Workflow Assignment Matrix
            </h2>
            <p className="text-xs text-slate-500">
              Cross-cutting organizational approval workflows mapped to responsible operational departments.
            </p>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-xs">
              <thead className="border-b border-slate-100 bg-slate-50 font-semibold text-slate-600">
                <tr>
                  <th className="px-3 py-3">Workflow Definition</th>
                  <th className="px-3 py-3">Workflow Code</th>
                  <th className="px-3 py-3">Assigned Departments</th>
                  <th className="px-3 py-3 text-right">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {ALL_WORKFLOWS.map((wf) => {
                  const assignedDepts = departments.filter((d) =>
                    d.workflow_assignments.includes(wf.code)
                  );

                  return (
                    <tr key={wf.code} className="hover:bg-slate-50/70">
                      <td className="px-3 py-3 font-semibold text-slate-900">{wf.label}</td>
                      <td className="px-3 py-3 font-mono text-indigo-700">{wf.code}</td>
                      <td className="px-3 py-3">
                        <div className="flex flex-wrap gap-1">
                          {assignedDepts.length > 0 ? (
                            assignedDepts.map((d) => (
                              <span
                                key={d.id}
                                className="rounded bg-indigo-50 px-2 py-0.5 text-[10px] font-bold text-indigo-700 border border-indigo-200"
                              >
                                {d.code}
                              </span>
                            ))
                          ) : (
                            <span className="text-slate-400 italic">No departments assigned</span>
                          )}
                        </div>
                      </td>
                      <td className="px-3 py-3 text-right">
                        <span className="rounded bg-emerald-100 px-2 py-0.5 text-[10px] font-bold text-emerald-800">
                          GOVERNED
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Create / Edit Department Modal */}
      {deptModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-xs overflow-y-auto">
          <div className="relative w-full max-w-lg rounded-2xl bg-white p-6 shadow-2xl">
            <h3 className="text-base font-bold text-slate-900">
              {editingDept
                ? `Edit Department: ${editingDept.name}`
                : parentDeptForSub
                ? `Create Sub-Department under ${parentDeptForSub.name}`
                : "Create Primary Department"}
            </h3>
            <p className="mt-1 text-xs text-slate-500">
              Define departmental metadata, official location, and leadership contact channels.
            </p>

            <form onSubmit={handleSaveDept} className="mt-4 space-y-3 text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-semibold text-slate-700">Department Code</label>
                  <input
                    type="text"
                    required
                    disabled={Boolean(editingDept)}
                    placeholder="CSE"
                    value={deptCode}
                    onChange={(e) => setDeptCode(e.target.value.toUpperCase())}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 font-mono uppercase"
                  />
                </div>
                <div>
                  <label className="font-semibold text-slate-700">Department Type</label>
                  <select
                    value={deptType}
                    onChange={(e) => setDeptType(e.target.value)}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                  >
                    <option value="ACADEMIC">ACADEMIC</option>
                    <option value="ADMINISTRATIVE">ADMINISTRATIVE</option>
                    <option value="OPERATIONAL">OPERATIONAL</option>
                    <option value="EXAMINATION">EXAMINATION</option>
                    <option value="FINANCE">FINANCE</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="font-semibold text-slate-700">Department Display Name</label>
                <input
                  type="text"
                  required
                  placeholder="Computer Science & Engineering"
                  value={deptName}
                  onChange={(e) => setDeptName(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 text-sm"
                />
              </div>

              <div>
                <label className="font-semibold text-slate-700">Campus Location / Room</label>
                <input
                  type="text"
                  placeholder="Block A, 3rd Floor, Room 301"
                  value={deptLocation}
                  onChange={(e) => setDeptLocation(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-semibold text-slate-700">Official Email</label>
                  <input
                    type="email"
                    placeholder="cse.dept@myeducationindia.com"
                    value={deptEmail}
                    onChange={(e) => setDeptEmail(e.target.value)}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                  />
                </div>
                <div>
                  <label className="font-semibold text-slate-700">Official Phone</label>
                  <input
                    type="text"
                    placeholder="+91-731-400100"
                    value={deptPhone}
                    onChange={(e) => setDeptPhone(e.target.value)}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                  />
                </div>
              </div>

              <div>
                <label className="font-semibold text-slate-700">Head of Department Designation</label>
                <input
                  type="text"
                  placeholder="Head of Department (HOD)"
                  value={deptHeadDesignation}
                  onChange={(e) => setDeptHeadDesignation(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                />
              </div>

              <div className="mt-5 flex justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setDeptModalOpen(false)}
                  className="rounded border border-slate-200 px-3 py-1.5 font-semibold text-slate-600 hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createDeptMutation.isPending || updateDeptMutation.isPending}
                  className="rounded bg-indigo-600 px-4 py-1.5 font-semibold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
                >
                  {createDeptMutation.isPending || updateDeptMutation.isPending
                    ? "Saving..."
                    : "Save Department"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Create Designation Modal */}
      {desigModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-xs">
          <div className="relative w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl">
            <h3 className="text-base font-bold text-slate-900">Create Campus Designation</h3>
            <p className="mt-1 text-xs text-slate-500">
              Define official cadre titles, reporting hierarchies, and seniority levels.
            </p>

            <form onSubmit={handleSaveDesig} className="mt-4 space-y-3 text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-semibold text-slate-700">Designation Code</label>
                  <input
                    type="text"
                    required
                    placeholder="ASSOC_PROF"
                    value={desigCode}
                    onChange={(e) => setDesigCode(e.target.value.toUpperCase())}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 font-mono uppercase"
                  />
                </div>
                <div>
                  <label className="font-semibold text-slate-700">Seniority Level</label>
                  <select
                    value={desigLevel}
                    onChange={(e) => setDesigLevel(Number(e.target.value))}
                    className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                  >
                    <option value={1}>Level 1 (Dean / Director)</option>
                    <option value={2}>Level 2 (HOD / Controller)</option>
                    <option value={3}>Level 3 (Professor / Chief)</option>
                    <option value={4}>Level 4 (Associate Professor)</option>
                    <option value={5}>Level 5 (Assistant Professor)</option>
                    <option value={6}>Level 6 (Officer / Lab Incharge)</option>
                    <option value={7}>Level 7 (Executive / Staff)</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="font-semibold text-slate-700">Title</label>
                <input
                  type="text"
                  required
                  placeholder="Associate Professor"
                  value={desigTitle}
                  onChange={(e) => setDesigTitle(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5 text-sm"
                />
              </div>

              <div>
                <label className="font-semibold text-slate-700">Cadre</label>
                <select
                  value={desigCadre}
                  onChange={(e) => setDesigCadre(e.target.value)}
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                >
                  <option value="TEACHING">TEACHING</option>
                  <option value="NON_TEACHING">NON_TEACHING</option>
                  <option value="ADMINISTRATIVE">ADMINISTRATIVE</option>
                  <option value="EXECUTIVE">EXECUTIVE</option>
                  <option value="SUPPORT">SUPPORT</option>
                </select>
              </div>

              <div>
                <label className="font-semibold text-slate-700">Description</label>
                <textarea
                  rows={2}
                  value={desigDesc}
                  onChange={(e) => setDesigDesc(e.target.value)}
                  placeholder="Primary roles, course loads, and supervisory duties..."
                  className="mt-1 block w-full rounded border border-slate-300 px-2.5 py-1.5"
                />
              </div>

              <div className="mt-5 flex justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setDesigModalOpen(false)}
                  className="rounded border border-slate-200 px-3 py-1.5 font-semibold text-slate-600 hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createDesigMutation.isPending}
                  className="rounded bg-indigo-600 px-4 py-1.5 font-semibold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
                >
                  {createDesigMutation.isPending ? "Saving..." : "Create Designation"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Assign Workflow Modal */}
      {workflowModalOpen && selectedDeptForWorkflow && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-xs">
          <div className="relative w-full max-w-lg rounded-2xl bg-white p-6 shadow-2xl">
            <h3 className="text-base font-bold text-slate-900">
              Assign Workflows: {selectedDeptForWorkflow.name}
            </h3>
            <p className="mt-1 text-xs text-slate-500">
              Select which organizational workflows require review or sign-off by this department.
            </p>

            <div className="mt-4 space-y-2 max-h-64 overflow-y-auto pr-1">
              {ALL_WORKFLOWS.map((wf) => {
                const isAssigned = selectedWorkflows.includes(wf.code);

                return (
                  <label
                    key={wf.code}
                    className={`flex items-center justify-between rounded-xl border p-3 text-xs cursor-pointer transition-colors ${
                      isAssigned
                        ? "bg-indigo-50/70 border-indigo-200 text-indigo-900"
                        : "bg-slate-50/50 border-slate-200 text-slate-600 hover:bg-slate-100"
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={isAssigned}
                        onChange={() => handleToggleWorkflow(wf.code)}
                        className="rounded border-slate-300 text-indigo-600"
                      />
                      <div>
                        <div className="font-bold">{wf.label}</div>
                        <div className="font-mono text-[10px] text-slate-400">{wf.code}</div>
                      </div>
                    </div>
                  </label>
                );
              })}
            </div>

            <div className="mt-5 flex justify-end gap-2 pt-3 border-t border-slate-100">
              <button
                type="button"
                onClick={() => setWorkflowModalOpen(false)}
                className="rounded border border-slate-200 px-3 py-1.5 text-xs font-semibold text-slate-600 hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={() =>
                  assignWorkflowsMutation.mutate({
                    id: selectedDeptForWorkflow.id,
                    workflows: selectedWorkflows,
                  })
                }
                disabled={assignWorkflowsMutation.isPending}
                className="rounded bg-indigo-600 px-4 py-1.5 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
              >
                {assignWorkflowsMutation.isPending ? "Saving..." : "Save Workflow Assignments"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
