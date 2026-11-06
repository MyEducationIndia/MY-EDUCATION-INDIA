import { httpClient } from "@/api/httpClient";
import { PaginatedResponse } from "@/types/common.types";
import { CreateUserPayload, UserSummary } from "@/types/user.types";

export const userService = {
  async listUsers(params: {
    institute_id?: string;
    search?: string;
    page: number;
    page_size: number;
  }): Promise<PaginatedResponse<UserSummary>> {
    const response = await httpClient.get<PaginatedResponse<UserSummary>>(
      "/users",
      { params }
    );
    return response.data;
  },

  async createUser(payload: CreateUserPayload): Promise<UserSummary> {
    const response = await httpClient.post<UserSummary>("/users", payload);
    return response.data;
  },

  async toggleUserActive(
    userId: string,
    isActive: boolean
  ): Promise<UserSummary> {
    const response = await httpClient.patch<UserSummary>(`/users/${userId}`, {
      is_active: isActive,
    });
    return response.data;
  },
};
