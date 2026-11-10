import { httpClient } from "@/api/httpClient";
import { PaginatedResponse } from "@/types/common.types";
import {
  CreateUserPayload,
  UpdateUserPayload,
  UserBulkActionPayload,
  UserBulkImportPayload,
  UserDetail,
  UserDocument,
  UserSummary,
} from "@/types/user.types";

export const userService = {
  async listUsers(params: {
    institute_id?: string;
    search?: string;
    user_category?: string;
    is_archived?: boolean;
    department?: string;
    verification_status?: string;
    page: number;
    page_size: number;
  }): Promise<PaginatedResponse<UserSummary>> {
    const response = await httpClient.get<PaginatedResponse<UserSummary>>(
      "/users",
      { params }
    );
    return response.data;
  },

  async getUserDetail(userId: string): Promise<UserDetail> {
    const response = await httpClient.get<UserDetail>(`/users/${userId}`);
    return response.data;
  },

  async createUser(payload: CreateUserPayload): Promise<UserDetail> {
    const response = await httpClient.post<UserDetail>("/users", payload);
    return response.data;
  },

  async updateUser(userId: string, payload: UpdateUserPayload): Promise<UserDetail> {
    const response = await httpClient.patch<UserDetail>(`/users/${userId}`, payload);
    return response.data;
  },

  async toggleUserActive(
    userId: string,
    isActive: boolean
  ): Promise<UserDetail> {
    const response = await httpClient.patch<UserDetail>(`/users/${userId}`, {
      is_active: isActive,
    });
    return response.data;
  },

  async archiveUser(userId: string): Promise<{ status: string; message: string }> {
    const response = await httpClient.post<{ status: string; message: string }>(
      `/users/${userId}/archive`
    );
    return response.data;
  },

  async restoreUser(userId: string): Promise<{ status: string; message: string }> {
    const response = await httpClient.post<{ status: string; message: string }>(
      `/users/${userId}/restore`
    );
    return response.data;
  },

  async executeBulkAction(
    payload: UserBulkActionPayload
  ): Promise<{ status: string; message: string; processed_count: number }> {
    const response = await httpClient.post<{
      status: string;
      message: string;
      processed_count: number;
    }>("/users/bulk-action", payload);
    return response.data;
  },

  async bulkImport(
    payload: UserBulkImportPayload
  ): Promise<{
    status: string;
    message: string;
    created_count: number;
    skipped_count: number;
  }> {
    const response = await httpClient.post<{
      status: string;
      message: string;
      created_count: number;
      skipped_count: number;
    }>("/users/import", payload);
    return response.data;
  },

  async addUserDocument(
    userId: string,
    payload: {
      document_type: string;
      document_title: string;
      document_url: string;
      file_size_bytes?: number;
      mime_type?: string;
      remarks?: string;
    }
  ): Promise<UserDocument> {
    const response = await httpClient.post<UserDocument>(
      `/users/${userId}/documents`,
      payload
    );
    return response.data;
  },

  async verifyUserDocument(
    userId: string,
    documentId: string,
    payload: { verification_status: string; remarks?: string }
  ): Promise<UserDocument> {
    const response = await httpClient.patch<UserDocument>(
      `/users/${userId}/documents/${documentId}/verify`,
      payload
    );
    return response.data;
  },

  async deleteUserDocument(
    userId: string,
    documentId: string
  ): Promise<{ status: string; message: string }> {
    const response = await httpClient.delete<{ status: string; message: string }>(
      `/users/${userId}/documents/${documentId}`
    );
    return response.data;
  },
};
