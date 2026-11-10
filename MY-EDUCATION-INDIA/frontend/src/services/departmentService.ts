import { httpClient } from "@/api/httpClient";
import {
  CreateDepartmentPayload,
  CreateDesignationPayload,
  DepartmentDetail,
  DepartmentSummary,
  DesignationItem,
  UpdateDepartmentPayload,
  UpdateDesignationPayload,
} from "@/types/department.types";

export const departmentService = {
  async listDepartments(params?: {
    parent_only?: boolean;
    department_type?: string;
  }): Promise<DepartmentSummary[]> {
    const response = await httpClient.get<DepartmentSummary[]>("/departments", {
      params,
    });
    return response.data;
  },

  async getDepartment(departmentId: string): Promise<DepartmentDetail> {
    const response = await httpClient.get<DepartmentDetail>(
      `/departments/${departmentId}`
    );
    return response.data;
  },

  async createDepartment(
    payload: CreateDepartmentPayload
  ): Promise<DepartmentDetail> {
    const response = await httpClient.post<DepartmentDetail>(
      "/departments",
      payload
    );
    return response.data;
  },

  async updateDepartment(
    departmentId: string,
    payload: UpdateDepartmentPayload
  ): Promise<DepartmentDetail> {
    const response = await httpClient.patch<DepartmentDetail>(
      `/departments/${departmentId}`,
      payload
    );
    return response.data;
  },

  async deleteDepartment(
    departmentId: string
  ): Promise<{ status: string; message: string }> {
    const response = await httpClient.delete<{ status: string; message: string }>(
      `/departments/${departmentId}`
    );
    return response.data;
  },

  async assignWorkflows(
    departmentId: string,
    workflowAssignments: string[]
  ): Promise<DepartmentDetail> {
    const response = await httpClient.patch<DepartmentDetail>(
      `/departments/${departmentId}/workflows`,
      { workflow_assignments: workflowAssignments }
    );
    return response.data;
  },

  async listDesignations(params?: {
    department_id?: string;
    cadre?: string;
  }): Promise<DesignationItem[]> {
    const response = await httpClient.get<DesignationItem[]>(
      "/departments/designations",
      { params }
    );
    return response.data;
  },

  async createDesignation(
    payload: CreateDesignationPayload
  ): Promise<DesignationItem> {
    const response = await httpClient.post<DesignationItem>(
      "/departments/designations",
      payload
    );
    return response.data;
  },

  async updateDesignation(
    designationId: string,
    payload: UpdateDesignationPayload
  ): Promise<DesignationItem> {
    const response = await httpClient.patch<DesignationItem>(
      `/departments/designations/${designationId}`,
      payload
    );
    return response.data;
  },

  async deleteDesignation(
    designationId: string
  ): Promise<{ status: string; message: string }> {
    const response = await httpClient.delete<{ status: string; message: string }>(
      `/departments/designations/${designationId}`
    );
    return response.data;
  },
};
