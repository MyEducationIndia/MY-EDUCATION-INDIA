import { authMemoryStore } from "@/store/authMemoryStore";
import { authApi } from "../api/authApi";
import { ConfigurableLoginPayload, UserProfile } from "../types/auth.types";

export const authService = {
  async login(payload: ConfigurableLoginPayload): Promise<UserProfile> {
    const session = await authApi.login(payload);
    // Transform roles into string array for memory store backward compatibility
    const compatUser = {
      ...session.user,
      roles: session.user.roles.map((r) => r.code),
    };
    authMemoryStore.setSession(session.access_token, session.csrf_token, compatUser);
    return session.user;
  },

  async restoreSession(): Promise<UserProfile | null> {
    try {
      const session = await authApi.refreshSession();
      const compatUser = {
        ...session.user,
        roles: session.user.roles.map((r) => r.code),
      };
      authMemoryStore.setSession(session.access_token, session.csrf_token, compatUser);
      return session.user;
    } catch {
      authMemoryStore.clearSession();
      return null;
    }
  },

  async logout(): Promise<void> {
    try {
      await authApi.logout();
    } finally {
      authMemoryStore.clearSession();
    }
  },
};
