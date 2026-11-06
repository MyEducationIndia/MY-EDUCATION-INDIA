import { httpClient } from "@/api/httpClient";
import {
  CreateRolePayload,
  PermissionItem,
  RoleItem,
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

  async createRole(payload: CreateRolePayload): Promise<RoleItem> {
    const response = await httpClient.post<RoleItem>("/roles", payload);
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
};
