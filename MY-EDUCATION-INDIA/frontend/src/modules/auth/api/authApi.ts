import { httpClient } from "@/api/httpClient";
import {
  ActiveSession,
  AuthSessionResponse,
  ConfigurableLoginPayload,
  LoginHistoryRecord,
  SystemAuthSettings,
  UserProfile,
} from "../types/auth.types";

export const authApi = {
  async getAuthSettings(): Promise<SystemAuthSettings> {
    const response = await httpClient.get<SystemAuthSettings>("/auth/config");
    return response.data;
  },

  async login(payload: ConfigurableLoginPayload): Promise<AuthSessionResponse> {
    const response = await httpClient.post<AuthSessionResponse>("/auth/login", payload);
    return response.data;
  },

  async refreshSession(): Promise<AuthSessionResponse> {
    const response = await httpClient.post<AuthSessionResponse>("/auth/refresh", {});
    return response.data;
  },

  async logout(): Promise<void> {
    await httpClient.post("/auth/logout", {});
  },

  async getCurrentProfile(): Promise<UserProfile> {
    const response = await httpClient.get<UserProfile>("/auth/me");
    return response.data;
  },

  async getMyPermissions(): Promise<string[]> {
    const response = await httpClient.get<string[]>("/auth/permissions");
    return response.data;
  },

  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    await httpClient.post("/auth/change-password", {
      current_password: currentPassword,
      new_password: newPassword,
    });
  },

  async initiateForgotPassword(identifier: string): Promise<{ message: string; reset_token?: string }> {
    const response = await httpClient.post<{ message: string; reset_token?: string }>("/auth/forgot-password", {
      identifier,
    });
    return response.data;
  },

  async resetPasswordWithToken(token: string, newPassword: string): Promise<void> {
    await httpClient.post("/auth/reset-password", {
      token,
      new_password: newPassword,
    });
  },

  // Admin APIs
  async getActiveSessions(userId: string): Promise<ActiveSession[]> {
    const response = await httpClient.get<ActiveSession[]>(`/auth/admin/users/${userId}/sessions`);
    return response.data;
  },

  async forceLogoutSession(sessionId: string): Promise<void> {
    await httpClient.post(`/auth/admin/sessions/${sessionId}/revoke`, {});
  },

  async getLoginHistory(params: { page: number; pageSize: number; userId?: string }): Promise<{ items: LoginHistoryRecord[]; total: number }> {
    const response = await httpClient.get<{ items: LoginHistoryRecord[]; total: number }>("/auth/admin/login-history", {
      params: { page: params.page, page_size: params.pageSize, user_id: params.userId },
    });
    return response.data;
  },
};
