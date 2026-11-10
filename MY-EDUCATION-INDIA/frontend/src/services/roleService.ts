import { httpClient } from "@/api/httpClient";
import {
  CreateRolePayload,
  InstantiateTemplatePayload,
  PermissionGroupItem,
  PermissionItem,
  RoleItem,
  RoleTemplateItem,
  UpdateRolePayload,
} from "@/types/role.types";

export const roleService = {
  async listRoles(instituteId?: string): Promise<RoleItem[]> {
    const response = await httpClient.get<RoleItem[]>("/roles", {
      params: instituteId ? { institute_id: instituteId } : undefined,
    });
    return response.data;
  },

  async listPermissions(moduleKey?: string): Promise<PermissionItem[]> {
    const response = await httpClient.get<PermissionItem[]>("/roles/permissions", {
      params: moduleKey ? { module_key: moduleKey } : undefined,
    });
    return response.data;
  },

  async listPermissionGroups(): Promise<PermissionGroupItem[]> {
    const response = await httpClient.get<PermissionGroupItem[]>("/roles/groups");
    return response.data;
  },

  async listRoleTemplates(): Promise<RoleTemplateItem[]> {
    const response = await httpClient.get<RoleTemplateItem[]>("/roles/templates");
    return response.data;
  },

  async createRole(payload: CreateRolePayload): Promise<RoleItem> {
    const response = await httpClient.post<RoleItem>("/roles", payload);
    return response.data;
  },

  async instantiateRoleTemplate(
    templateKey: string,
    payload: InstantiateTemplatePayload
  ): Promise<RoleItem> {
    const response = await httpClient.post<RoleItem>(
      `/roles/templates/${templateKey}/instantiate`,
      payload
    );
    return response.data;
  },

  async updateRole(
    roleId: string,
    payload: UpdateRolePayload
  ): Promise<RoleItem> {
    const response = await httpClient.patch<RoleItem>(`/roles/${roleId}`, payload);
    return response.data;
  },

  async updateRolePermissions(
    roleId: string,
    permissionCodes: string[]
  ): Promise<RoleItem> {
    const response = await httpClient.put<RoleItem>(
      `/roles/${roleId}/permissions`,
      { permission_codes: permissionCodes }
    );
    return response.data;
  },

  async deleteRole(roleId: string): Promise<{ status: string; message: string }> {
    const response = await httpClient.delete<{ status: string; message: string }>(
      `/roles/${roleId}`
    );
    return response.data;
  },
};
