import { httpClient } from "@/api/httpClient";
import { authMemoryStore } from "@/store/authMemoryStore";
import {
  AuthenticatedUser,
  LoginCredentials,
  TokenSessionResponse,
} from "@/types/auth.types";

export const authService = {
  async login(credentials: LoginCredentials): Promise<TokenSessionResponse> {
    const response = await httpClient.post<TokenSessionResponse>(
      "/auth/login",
      credentials
    );
    const { access_token, csrf_token, user } = response.data;
    authMemoryStore.setSession(access_token, csrf_token, user);
    return response.data;
  },

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
