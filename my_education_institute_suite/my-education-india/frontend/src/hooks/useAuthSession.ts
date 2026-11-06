import { useEffect, useState } from "react";
import { authMemoryStore } from "@/store/authMemoryStore";
import { AuthenticatedUser } from "@/types/auth.types";
import { authService } from "@/services/authService";

export function useAuthSession() {
  const [user, setUser] = useState<AuthenticatedUser | null>(
    authMemoryStore.getState().user
  );
  const [isInitializing, setIsInitializing] = useState<boolean>(
    authMemoryStore.getState().user === null
  );

  useEffect(() => {
    const unsubscribe = authMemoryStore.subscribe((snapshot) => {
      setUser(snapshot.user);
    });

    if (!authMemoryStore.getState().accessToken) {
      authService
        .restoreSession()
        .finally(() => setIsInitializing(false));
    } else {
      setIsInitializing(false);
    }

    return unsubscribe;
  }, []);

  const hasPermission = (permissionCode: string): boolean => {
    if (!user) return false;
    if (user.is_super_admin || user.permissions.includes("*")) return true;
    return user.permissions.includes(permissionCode);
  };

  return {
    user,
    isAuthenticated: Boolean(user),
    isInitializing,
    hasPermission,
    logout: authService.logout,
  };
}
