import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { roleService } from "@/services/roleService";
import {
  PermissionGroupItem,
  PermissionItem,
  RoleItem,
  RoleTemplateItem,
} from "@/types/role.types";

const createRoleSchema = z.object({
  code: z
    .string()
    .min(2)
    .max(64)
    .regex(/^[A-Z0-9_]+$/, "Use uppercase letters, digits, and underscores only"),
  name: z.string().min(2).max(120),
  description: z.string().max(500).optional(),
  portal_subdomain: z.string().min(2).max(32),
  department_name: z.string().min(2).max(100),
  data_scope: z.enum(["ALL_INSTITUTE", "OWN_DEPARTMENT", "OWN_RECORDS"]),
});

type CreateRoleFormValues = z.infer<typeof createRoleSchema>;

export const RolesPermissionsPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<"roles" | "templates" | "permissions">("roles");
  const [selectedRole, setSelectedRole] = useState<RoleItem | null>(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState<RoleTemplateItem | null>(null);
  const [templateModalOpen, setTemplateModalOpen] = useState(false);
  const [templateRoleCode, setTemplateRoleCode] = useState("");
  const [templateRoleName, setTemplateRoleName] = useState("");
  const [templateDept, setTemplateDept] = useState("");

  // Edit role states
  const [editName, setEditName] = useState("");
  const [editDept, setEditDept] = useState("");
  const [editScope, setEditScope] = useState<string>("ALL_INSTITUTE");
  const [editPermCodes, setEditPermCodes] = useState<string[]>([]);
  const [fieldMasks, setFieldMasks] = useState<Record<string, boolean>>({
    mask_student_phone: false,
    mask_employee_salary: true,
    mask_government_id: true,
    mask_exam_answer_keys: true,
  });
  const [allowedMenus, setAllowedMenus] = useState<string[]>([
    "DASHBOARD",
    "ACADEMICS",
    "ADMISSIONS",
    "EXAMS_CBT",
    "FINANCE",
  ]);

  const { data: roles = [], isLoading: rolesLoading } = useQuery({
    queryKey: ["roles"],
    queryFn: () => roleService.listRoles(),
  });

  const { data: permissions = [] } = useQuery({
    queryKey: ["permissions"],
    queryFn: () => roleService.listPermissions(),
  });

  const { data: permissionGroups = [] } = useQuery({
    queryKey: ["permission-groups"],
    queryFn: () => roleService.listPermissionGroups(),
  });

  const { data: roleTemplates = [] } = useQuery({
    queryKey: ["role-templates"],
    queryFn: () => roleService.listRoleTemplates(),
  });

  const createMutation = useMutation({
    mutationFn: roleService.createRole,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["roles"] });
      reset();
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: any }) =>
      roleService.updateRole(id, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["roles"] });
      setIsEditModalOpen(false);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (roleId: string) => roleService.deleteRole(roleId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["roles"] });
    },
  });

  const instantiateMutation = useMutation({
    mutationFn: ({
      key,
      payload,
    }: {
      key: string;
      payload: { role_code: string; role_name: string; department_name?: string };
    }) => roleService.instantiateRoleTemplate(key, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["roles"] });
      setTemplateModalOpen(false);
    },
  });

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<CreateRoleFormValues>({
    resolver: zodResolver(createRoleSchema),
    defaultValues: {
      code: "",
      name: "",
      description: "",
      portal_subdomain: "admin",
      department_name: "General Administration",
      data_scope: "ALL_INSTITUTE",
    },
  });

  const onSubmit = async (values: CreateRoleFormValues): Promise<void> => {
    await createMutation.mutateAsync({
      ...values,
      is_custom_role: true,
      permission_codes: [],
      data_scope: values.data_scope,
      department_name: values.department_name,
    });
  };

  const handleOpenEdit = (role: RoleItem) => {
    setSelectedRole(role);
    setEditName(role.name);
    setEditDept(role.department_name || "General");
    setEditScope(role.data_scope || "ALL_INSTITUTE");
    setEditPermCodes(role.permissions.map((p) => p.code));
    if (role.field_permissions_json) {
      setFieldMasks({
        mask_student_phone: Boolean(role.field_permissions_json.mask_student_phone),
        mask_employee_salary: Boolean(role.field_permissions_json.mask_employee_salary),
        mask_government_id: Boolean(role.field_permissions_json.mask_government_id),
        mask_exam_answer_keys: Boolean(role.field_permissions_json.mask_exam_answer_keys),
      });
    } else {
      setFieldMasks({
        mask_student_phone: false,
        mask_employee_salary: true,
        mask_government_id: true,
        mask_exam_answer_keys: true,
      });
    }
    if (role.menu_permissions_json && role.menu_permissions_json.length > 0) {
      setAllowedMenus(role.menu_permissions_json);
    } else {
      setAllowedMenus(["DASHBOARD", "ACADEMICS", "ADMISSIONS", "EXAMS_CBT", "FINANCE"]);
    }
    setIsEditModalOpen(true);
  };

  const handleSaveRole = async () => {
    if (!selectedRole) return;
    await updateMutation.mutateAsync({
      id: selectedRole.id,
      payload: {
        name: editName,
        department_name: editDept,
        data_scope: editScope,
        permission_codes: editPermCodes,
        field_permissions_json: fieldMasks,
        menu_permissions_json: allowedMenus,
      },
    });
  };

  const togglePermission = (code: string) => {
    setEditPermCodes((prev) =>
      prev.includes(code) ? prev.filter((c) => c !== code) : [...prev, code]
    );
  };

  const toggleAllInGroup = (groupPerms: PermissionItem[]) => {
    const groupCodes = groupPerms.map((p) => p.code);
    const allSelected = groupCodes.every((c) => editPermCodes.includes(c));
    if (allSelected) {
      setEditPermCodes((prev) => prev.filter((c) => !groupCodes.includes(c)));
    } else {
      setEditPermCodes((prev) => Array.from(new Set([...prev, ...groupCodes])));
    }
  };

  const handleOpenTemplateModal = (tpl: RoleTemplateItem) => {
    setSelectedTemplate(tpl);
    setTemplateRoleCode(`${tpl.template_key}_01`);
    setTemplateRoleName(tpl.name);
    setTemplateDept(tpl.department);
    setTemplateModalOpen(true);
  };

  const handleInstantiate = async () => {
    if (!selectedTemplate) return;
    await instantiateMutation.mutateAsync({
      key: selectedTemplate.template_key,
      payload: {
        role_code: templateRoleCode.toUpperCase(),
        role_name: templateRoleName,
        department_name: templateDept,
      },
    });
  };

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
        <div>
          <div className="flex items-center gap-2">
            <span className="rounded-md bg-indigo-100 px-2 py-0.5 text-xs font-bold text-indigo-800">
              Module 2
            </span>
            <span className="rounded-md bg-emerald-100 px-2 py-0.5 text-xs font-semibold text-emerald-800">
              Enterprise RBAC Engine
            </span>
          </div>
          <h1 className="mt-2 text-xl font-bold text-slate-900">
            Role-Based Access Control (RBAC) & Governance
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            Configure institutional roles, hierarchical data scopes, granular permission matrices, and field-level masking.
          </p>
        </div>

        {/* Tab Controls */}
        <div className="flex items-center rounded-xl bg-slate-100 p-1">
          <button
            type="button"
            onClick={() => setActiveTab("roles")}
            className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
              activeTab === "roles"
                ? "bg-white text-indigo-700 shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Roles & Matrix ({roles.length})
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("templates")}
            className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
              activeTab === "templates"
                ? "bg-white text-indigo-700 shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Role Templates ({roleTemplates.length})
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("permissions")}
            className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
              activeTab === "permissions"
                ? "bg-white text-indigo-700 shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Permission Groups ({permissionGroups.length})
          </button>
        </div>
      </div>

      {/* Main Content Area */}
      {activeTab === "roles" && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          {/* Create Custom Role Card */}
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs lg:col-span-1">
            <h2 className="text-base font-bold text-slate-900">Create Custom Role</h2>
            <p className="mt-1 text-xs text-slate-500">
              Define a tailored institutional role with custom data scopes and subdomain routing.
            </p>

            <form onSubmit={handleSubmit(onSubmit)} className="mt-4 space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Role Code</label>
                <input
                  type="text"
                  placeholder="EXAM_INVIGILATOR"
                  {...register("code")}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                />
                {errors.code && <p className="mt-1 text-xs text-rose-600">{errors.code.message}</p>}
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Display Name</label>
                <input
                  type="text"
                  placeholder="Senior Exam Invigilator"
                  {...register("name")}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                />
                {errors.name && <p className="mt-1 text-xs text-rose-600">{errors.name.message}</p>}
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Department</label>
                <input
                  type="text"
                  placeholder="Examination Cell"
                  {...register("department_name")}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                />
                {errors.department_name && (
                  <p className="mt-1 text-xs text-rose-600">{errors.department_name.message}</p>
                )}
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Portal Subdomain</label>
                  <select
                    {...register("portal_subdomain")}
                    className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                  >
                    <option value="admin">admin</option>
                    <option value="faculty">faculty</option>
                    <option value="student">student</option>
                    <option value="parent">parent</option>
                    <option value="exam">exam</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700">Data Scope</label>
                  <select
                    {...register("data_scope")}
                    className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                  >
                    <option value="ALL_INSTITUTE">All Institute</option>
                    <option value="OWN_DEPARTMENT">Own Department</option>
                    <option value="OWN_RECORDS">Own Records Only</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Description</label>
                <textarea
                  rows={2}
                  placeholder="Institutional duties and access mandate..."
                  {...register("description")}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                />
              </div>

              <button
                type="submit"
                disabled={isSubmitting || createMutation.isPending}
                className="w-full rounded-lg bg-indigo-600 px-4 py-2.5 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
              >
                {createMutation.isPending ? "Creating Role..." : "Create Custom Role"}
              </button>
            </form>
          </div>

          {/* Role Matrix Table */}
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs lg:col-span-2">
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <h2 className="text-base font-bold text-slate-900">Institutional Roles Matrix</h2>
              <span className="text-xs text-slate-500">{roles.length} roles active</span>
            </div>

            {rolesLoading ? (
              <div className="py-12 text-center text-sm text-slate-500">Loading roles...</div>
            ) : (
              <div className="mt-4 overflow-x-auto">
                <table className="min-w-full text-left text-sm">
                  <thead className="border-b border-slate-100 bg-slate-50 text-xs font-semibold text-slate-600">
                    <tr>
                      <th className="px-3 py-2.5">Role & Code</th>
                      <th className="px-3 py-2.5">Department</th>
                      <th className="px-3 py-2.5">Subdomain</th>
                      <th className="px-3 py-2.5">Scope</th>
                      <th className="px-3 py-2.5">Permissions</th>
                      <th className="px-3 py-2.5 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 text-xs">
                    {roles.map((role) => (
                      <tr key={role.id} className="hover:bg-slate-50/60">
                        <td className="px-3 py-3">
                          <div className="font-semibold text-slate-900">{role.name}</div>
                          <div className="font-mono text-[11px] text-slate-500">{role.code}</div>
                          {role.is_system_role ? (
                            <span className="inline-block mt-0.5 rounded bg-amber-50 px-1.5 py-0.2 text-[10px] font-medium text-amber-700 border border-amber-200">
                              Core System Role
                            </span>
                          ) : (
                            <span className="inline-block mt-0.5 rounded bg-blue-50 px-1.5 py-0.2 text-[10px] font-medium text-blue-700 border border-blue-200">
                              Custom Role
                            </span>
                          )}
                        </td>
                        <td className="px-3 py-3 text-slate-600">
                          {role.department_name || "General"}
                        </td>
                        <td className="px-3 py-3">
                          <span className="font-mono rounded bg-slate-100 px-1.5 py-0.5 text-slate-700">
                            {role.portal_subdomain}
                          </span>
                        </td>
                        <td className="px-3 py-3">
                          <span
                            className={`rounded px-1.5 py-0.5 font-medium ${
                              role.data_scope === "ALL_INSTITUTE"
                                ? "bg-purple-100 text-purple-800"
                                : role.data_scope === "OWN_DEPARTMENT"
                                ? "bg-indigo-100 text-indigo-800"
                                : "bg-emerald-100 text-emerald-800"
                            }`}
                          >
                            {role.data_scope || "ALL_INSTITUTE"}
                          </span>
                        </td>
                        <td className="px-3 py-3">
                          <span className="font-semibold text-slate-700">
                            {role.permissions.length}
                          </span>{" "}
                          granted
                        </td>
                        <td className="px-3 py-3 text-right space-x-2">
                          <button
                            type="button"
                            onClick={() => handleOpenEdit(role)}
                            className="rounded-md bg-indigo-50 px-2.5 py-1 text-xs font-semibold text-indigo-700 hover:bg-indigo-100"
                          >
                            Configure
                          </button>
                          {!role.is_system_role && (
                            <button
                              type="button"
                              onClick={() => {
                                if (confirm(`Delete custom role '${role.name}'?`)) {
                                  void deleteMutation.mutate(role.id);
                                }
                              }}
                              className="rounded-md bg-rose-50 px-2 py-1 text-xs font-semibold text-rose-600 hover:bg-rose-100"
                            >
                              Delete
                            </button>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Role Templates Tab */}
      {activeTab === "templates" && (
        <div className="space-y-4">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
            <h2 className="text-base font-bold text-slate-900">Pre-Configured Enterprise Role Templates</h2>
            <p className="mt-1 text-xs text-slate-500">
              Standardized campus templates designed for instant onboarding across departments.
            </p>
          </div>

          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
            {roleTemplates.map((tpl) => (
              <div
                key={tpl.id}
                className="flex flex-col justify-between rounded-2xl border border-slate-200 bg-white p-5 shadow-xs hover:border-indigo-300 transition-all"
              >
                <div>
                  <div className="flex items-center justify-between">
                    <span className="rounded bg-indigo-100 px-2 py-0.5 text-[11px] font-bold text-indigo-800">
                      {tpl.department}
                    </span>
                    <span className="font-mono text-xs text-slate-400">
                      subdomain: {tpl.default_subdomain}
                    </span>
                  </div>
                  <h3 className="mt-3 text-base font-bold text-slate-900">{tpl.name}</h3>
                  <p className="mt-1 text-xs text-slate-600 line-clamp-2">{tpl.description}</p>

                  <div className="mt-4 space-y-1.5 text-xs text-slate-600">
                    <div>
                      <span className="font-semibold text-slate-700">Data Scope:</span>{" "}
                      <span className="font-mono text-indigo-700">{tpl.default_data_scope}</span>
                    </div>
                    <div>
                      <span className="font-semibold text-slate-700">Default Permissions:</span>{" "}
                      <span className="font-semibold text-slate-900">{tpl.default_permissions.length} items</span>
                    </div>
                  </div>
                </div>

                <div className="mt-5 pt-4 border-t border-slate-100">
                  <button
                    type="button"
                    onClick={() => handleOpenTemplateModal(tpl)}
                    className="w-full rounded-lg bg-indigo-600 px-3 py-2 text-xs font-semibold text-white hover:bg-indigo-700 shadow-xs"
                  >
                    Instantiate Role
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Permission Groups Catalog Tab */}
      {activeTab === "permissions" && (
        <div className="space-y-4">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
            <h2 className="text-base font-bold text-slate-900">Permission Groups & Capability Tree</h2>
            <p className="mt-1 text-xs text-slate-500">
              System capabilities partitioned into enterprise operational groups.
            </p>
          </div>

          <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
            {permissionGroups.map((grp) => {
              const groupPerms = permissions.filter(
                (p) => p.group_key === grp.group_key || p.module_key.toUpperCase() === grp.group_key
              );

              return (
                <div key={grp.id} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="rounded bg-slate-100 px-2 py-0.5 text-[10px] font-bold text-slate-700">
                        {grp.category}
                      </span>
                      <h3 className="mt-1 text-sm font-bold text-slate-900">{grp.group_name}</h3>
                    </div>
                    <span className="font-mono text-xs font-bold text-indigo-600">
                      {grp.group_key}
                    </span>
                  </div>
                  <p className="mt-1 text-xs text-slate-500">{grp.description}</p>

                  <div className="mt-3 rounded-xl bg-slate-50 p-3">
                    <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-wide mb-2">
                      Associated System Capabilities ({groupPerms.length})
                    </div>
                    <div className="flex flex-wrap gap-1.5">
                      {groupPerms.length > 0 ? (
                        groupPerms.map((perm) => (
                          <span
                            key={perm.id}
                            className="inline-flex items-center gap-1 rounded bg-white px-2 py-1 text-[11px] font-mono text-slate-700 border border-slate-200"
                          >
                            <span className="h-1.5 w-1.5 rounded-full bg-emerald-500"></span>
                            {perm.code}
                          </span>
                        ))
                      ) : (
                        <span className="text-xs text-slate-400 italic">
                          No direct granular permissions attached yet
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Role Configuration & Permission Matrix Modal */}
      {isEditModalOpen && selectedRole && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-xs overflow-y-auto">
          <div className="relative w-full max-w-4xl max-h-[90vh] flex flex-col rounded-2xl bg-white shadow-2xl">
            {/* Modal Header */}
            <div className="flex items-center justify-between border-b border-slate-100 px-6 py-4">
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-base font-bold text-slate-900">
                    Configure Role: {selectedRole.name}
                  </h3>
                  <span className="font-mono text-xs text-slate-500">({selectedRole.code})</span>
                </div>
                <p className="text-xs text-slate-500">
                  Update departmental alignment, data scopes, field-level masks, and granular permissions.
                </p>
              </div>
              <button
                type="button"
                onClick={() => setIsEditModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 font-bold text-lg"
              >
                &times;
              </button>
            </div>

            {/* Modal Body */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
              {/* Scope & Department Row */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Display Name</label>
                  <input
                    type="text"
                    value={editName}
                    onChange={(e) => setEditName(e.target.value)}
                    className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Department</label>
                  <input
                    type="text"
                    value={editDept}
                    onChange={(e) => setEditDept(e.target.value)}
                    className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Data Scope</label>
                  <select
                    value={editScope}
                    onChange={(e) => setEditScope(e.target.value)}
                    className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                  >
                    <option value="ALL_INSTITUTE">ALL_INSTITUTE (Full Campus Access)</option>
                    <option value="OWN_DEPARTMENT">OWN_DEPARTMENT (Department Scoped)</option>
                    <option value="OWN_RECORDS">OWN_RECORDS (Self Records Only)</option>
                  </select>
                </div>
              </div>

              {/* Field-Level Security Masks */}
              <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
                <h4 className="text-xs font-bold text-slate-900 uppercase tracking-wide">
                  Field-Level Security & Data Masking
                </h4>
                <p className="mt-0.5 text-xs text-slate-500">
                  Protect sensitive student, staff, and examination records from unauthorized view.
                </p>

                <div className="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                  <label className="flex items-center gap-2 cursor-pointer bg-white p-2.5 rounded-lg border border-slate-200">
                    <input
                      type="checkbox"
                      checked={fieldMasks.mask_student_phone}
                      onChange={(e) =>
                        setFieldMasks((prev) => ({ ...prev, mask_student_phone: e.target.checked }))
                      }
                      className="rounded border-slate-300 text-indigo-600"
                    />
                    <div>
                      <div className="font-semibold text-slate-800">Mask Student Phone & Email</div>
                      <div className="text-[11px] text-slate-500">Redact phone and personal emails</div>
                    </div>
                  </label>

                  <label className="flex items-center gap-2 cursor-pointer bg-white p-2.5 rounded-lg border border-slate-200">
                    <input
                      type="checkbox"
                      checked={fieldMasks.mask_employee_salary}
                      onChange={(e) =>
                        setFieldMasks((prev) => ({ ...prev, mask_employee_salary: e.target.checked }))
                      }
                      className="rounded border-slate-300 text-indigo-600"
                    />
                    <div>
                      <div className="font-semibold text-slate-800">Mask Faculty & Staff Salary</div>
                      <div className="text-[11px] text-slate-500">Redact payroll, bank accounts & CTC</div>
                    </div>
                  </label>

                  <label className="flex items-center gap-2 cursor-pointer bg-white p-2.5 rounded-lg border border-slate-200">
                    <input
                      type="checkbox"
                      checked={fieldMasks.mask_government_id}
                      onChange={(e) =>
                        setFieldMasks((prev) => ({ ...prev, mask_government_id: e.target.checked }))
                      }
                      className="rounded border-slate-300 text-indigo-600"
                    />
                    <div>
                      <div className="font-semibold text-slate-800">Mask Aadhaar / PAN / Passport</div>
                      <div className="text-[11px] text-slate-500">Show only last 4 digits (XXXX-XXXX-1234)</div>
                    </div>
                  </label>

                  <label className="flex items-center gap-2 cursor-pointer bg-white p-2.5 rounded-lg border border-slate-200">
                    <input
                      type="checkbox"
                      checked={fieldMasks.mask_exam_answer_keys}
                      onChange={(e) =>
                        setFieldMasks((prev) => ({ ...prev, mask_exam_answer_keys: e.target.checked }))
                      }
                      className="rounded border-slate-300 text-indigo-600"
                    />
                    <div>
                      <div className="font-semibold text-slate-800">Mask Exam Answer Keys & Rubrics</div>
                      <div className="text-[11px] text-slate-500">Hide evaluation keys until results release</div>
                    </div>
                  </label>
                </div>
              </div>

              {/* Granular Permission Groups Accordion */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <h4 className="text-xs font-bold text-slate-900 uppercase tracking-wide">
                    Granular Permission Matrix ({editPermCodes.length} active)
                  </h4>
                  <div className="text-xs text-indigo-600 font-semibold cursor-pointer">
                    Click group header to toggle group permissions
                  </div>
                </div>

                <div className="space-y-3">
                  {permissionGroups.map((grp) => {
                    const groupPerms = permissions.filter(
                      (p) => p.group_key === grp.group_key || p.module_key.toUpperCase() === grp.group_key
                    );
                    const selectedInGroup = groupPerms.filter((p) => editPermCodes.includes(p.code)).length;

                    return (
                      <div key={grp.id} className="rounded-xl border border-slate-200 bg-white p-3">
                        <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                          <div className="flex items-center gap-2">
                            <span className="font-semibold text-xs text-slate-900">
                              {grp.group_name}
                            </span>
                            <span className="font-mono text-[10px] text-slate-400">
                              ({selectedInGroup}/{groupPerms.length} granted)
                            </span>
                          </div>
                          {groupPerms.length > 0 && (
                            <button
                              type="button"
                              onClick={() => toggleAllInGroup(groupPerms)}
                              className="text-[11px] font-semibold text-indigo-600 hover:text-indigo-800"
                            >
                              {selectedInGroup === groupPerms.length ? "Deselect All" : "Select All"}
                            </button>
                          )}
                        </div>

                        <div className="mt-2.5 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
                          {groupPerms.map((perm) => {
                            const isChecked = editPermCodes.includes(perm.code);
                            return (
                              <label
                                key={perm.id}
                                className={`flex items-start gap-2 rounded-lg p-2 border text-xs cursor-pointer transition-colors ${
                                  isChecked
                                    ? "bg-indigo-50/70 border-indigo-200 text-indigo-950"
                                    : "bg-slate-50/60 border-slate-100 text-slate-600 hover:bg-slate-100"
                                }`}
                              >
                                <input
                                  type="checkbox"
                                  checked={isChecked}
                                  onChange={() => togglePermission(perm.code)}
                                  className="mt-0.5 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
                                />
                                <div>
                                  <div className="font-mono text-[11px] font-bold">{perm.code}</div>
                                  <div className="text-[10px] text-slate-500">{perm.name}</div>
                                </div>
                              </label>
                            );
                          })}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* Modal Footer */}
            <div className="flex items-center justify-end gap-3 border-t border-slate-100 px-6 py-4">
              <button
                type="button"
                onClick={() => setIsEditModalOpen(false)}
                className="rounded-lg border border-slate-200 px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleSaveRole}
                disabled={updateMutation.isPending}
                className="rounded-lg bg-indigo-600 px-4 py-2 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
              >
                {updateMutation.isPending ? "Saving..." : "Save Role Configuration"}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Instantiate Role Template Modal */}
      {templateModalOpen && selectedTemplate && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-xs">
          <div className="relative w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl">
            <h3 className="text-base font-bold text-slate-900">
              Instantiate Role: {selectedTemplate.name}
            </h3>
            <p className="mt-1 text-xs text-slate-500">
              Create an institutional role based on the {selectedTemplate.department} template.
            </p>

            <div className="mt-4 space-y-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Role Code</label>
                <input
                  type="text"
                  value={templateRoleCode}
                  onChange={(e) => setTemplateRoleCode(e.target.value.toUpperCase())}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden font-mono"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Display Name</label>
                <input
                  type="text"
                  value={templateRoleName}
                  onChange={(e) => setTemplateRoleName(e.target.value)}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Department</label>
                <input
                  type="text"
                  value={templateDept}
                  onChange={(e) => setTemplateDept(e.target.value)}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                />
              </div>
            </div>

            <div className="mt-6 flex justify-end gap-2">
              <button
                type="button"
                onClick={() => setTemplateModalOpen(false)}
                className="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-semibold text-slate-600 hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleInstantiate}
                disabled={instantiateMutation.isPending}
                className="rounded-lg bg-indigo-600 px-4 py-1.5 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
              >
                {instantiateMutation.isPending ? "Instantiating..." : "Confirm & Instantiate"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
