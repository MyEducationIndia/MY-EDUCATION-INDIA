import { httpClient } from "@/api/httpClient";
import { authMemoryStore } from "@/store/authMemoryStore";
import {
  AuthenticatedUser,
  LoginCredentials,
  TokenSessionResponse,
  ActiveSessionItem,
  LoginHistoryItem,
  SecurityPolicy,
  MfaSetupResponse,
} from "@/types/auth.types";

export const authService = {
  // Unified Password Authentication
  async login(credentials: LoginCredentials): Promise<TokenSessionResponse> {
    const response = await httpClient.post<TokenSessionResponse>(
      "/auth/login",
      credentials
    );
    const { access_token, csrf_token, user } = response.data;
    authMemoryStore.setSession(access_token, csrf_token, user);
    return response.data;
  },

  // OTP Login & Verification
  async requestOtp(
    identifier: string,
    channel: string = "EMAIL",
    otp_type: string = "LOGIN"
  ): Promise<any> {
    const response = await httpClient.post("/auth/login/otp/request", {
      identifier,
      channel,
      otp_type,
    });
    return response.data;
  },

  async loginWithOtp(
    identifier: string,
    otp_code: string
  ): Promise<TokenSessionResponse> {
    const response = await httpClient.post<TokenSessionResponse>(
      "/auth/login/otp/verify",
      {
        identifier,
        otp_code,
        otp_type: "LOGIN",
      }
    );
    const { access_token, csrf_token, user } = response.data;
    authMemoryStore.setSession(access_token, csrf_token, user);
    return response.data;
  },

  // Password Reset Flows
  async requestPasswordReset(email: string): Promise<any> {
    const response = await httpClient.post("/auth/password-reset/request", {
      email,
    });
    return response.data;
  },

  async confirmPasswordReset(
    email: string,
    otp_code: string,
    new_password: string
  ): Promise<any> {
    const response = await httpClient.post("/auth/password-reset/confirm", {
      email,
      otp_code,
      new_password,
    });
    return response.data;
  },

  // Multi-Factor Authentication (MFA / 2FA)
  async setupMfa(): Promise<MfaSetupResponse> {
    const response = await httpClient.post<MfaSetupResponse>("/auth/mfa/setup", {});
    return response.data;
  },

  async verifyMfa(code: string): Promise<any> {
    const response = await httpClient.post("/auth/mfa/verify", { code });
    return response.data;
  },

  // Active Sessions & Device Management
  async listActiveSessions(): Promise<ActiveSessionItem[]> {
    const response = await httpClient.get<ActiveSessionItem[]>("/auth/sessions/active");
    return response.data;
  },

  async revokeSession(sessionId: string): Promise<any> {
    const response = await httpClient.delete(`/auth/sessions/${sessionId}`);
    return response.data;
  },

  async revokeAllSessions(): Promise<any> {
    const response = await httpClient.post("/auth/sessions/revoke-all", {});
    return response.data;
  },

  // Login History Audit
  async listLoginHistory(limit: number = 50): Promise<LoginHistoryItem[]> {
    const response = await httpClient.get<LoginHistoryItem[]>("/auth/login-history", {
      params: { limit },
    });
    return response.data;
  },

  // Security Policies
  async getSecurityPolicy(): Promise<SecurityPolicy> {
    const response = await httpClient.get<SecurityPolicy>("/auth/security-policy");
    return response.data;
  },

  async updateSecurityPolicy(payload: Partial<SecurityPolicy>): Promise<SecurityPolicy> {
    const response = await httpClient.patch<SecurityPolicy>("/auth/security-policy", payload);
    return response.data;
  },

  // Session Lifecycle
  async restoreSession(): Promise<AuthenticatedUser | null> {
    try {
      const response = await httpClient.post<TokenSessionResponse>(
        "/auth/refresh",
        {}
      );
      const { access_token, csrf_token, user } = response.data;
      authMemoryStore.setSession(access_token, csrf_token, user);
      return user;
    } catch {
      authMemoryStore.clearSession();
      return null;
    }
  },

  async logout(): Promise<void> {
    try {
      await httpClient.post("/auth/logout", {});
    } finally {
      authMemoryStore.clearSession();
    }
  },
};
