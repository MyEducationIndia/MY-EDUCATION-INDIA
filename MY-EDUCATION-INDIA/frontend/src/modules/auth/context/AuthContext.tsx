import React, { createContext, useContext, useEffect, useState, useMemo } from "react";
import { authMemoryStore } from "@/store/authMemoryStore";
import { authService } from "../services/authService";
import { ConfigurableLoginPayload, UserProfile } from "../types/auth.types";

interface AuthContextType {
  user: UserProfile | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  isDarkMode: boolean;
  toggleDarkMode: () => void;
  login: (payload: ConfigurableLoginPayload) => Promise<void>;
  logout: () => Promise<void>;
  hasPermission: (permissionCode: string) => boolean;
  hasRole: (roleCode: string) => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isDarkMode, setIsDarkMode] = useState<boolean>(false);

  useEffect(() => {
    // Check initial session via HttpOnly refresh cookie
    authService
      .restoreSession()
      .then((restoredUser) => {
        if (restoredUser) {
          setUser(restoredUser);
        }
      })
      .finally(() => {
        setIsLoading(false);
      });

    // Subscribe to volatile auth memory store updates
    const unsubscribe = authMemoryStore.subscribe((snapshot) => {
      if (snapshot.user) {
        // Map roles safely
        const fullUser: UserProfile = {
          ...snapshot.user,
          roles: snapshot.user.roles.map((code) => ({
            id: code,
            code,
            name: code,
            portal_subdomain: "admin",
            is_system_role: true,
          })),
        };
        setUser(fullUser);
      } else {
        setUser(null);
      }
    });

    return unsubscribe;
  }, []);

  const toggleDarkMode = () => {
    setIsDarkMode((prev) => {
      const next = !prev;
      if (next) {
        document.documentElement.classList.add("dark");
      } else {
        document.documentElement.classList.remove("dark");
      }
      return next;
    });
  };

  const login = async (payload: ConfigurableLoginPayload): Promise<void> => {
    const profile = await authService.login(payload);
    setUser(profile);
  };

  const logout = async (): Promise<void> => {
    await authService.logout();
    setUser(null);
  };

  const hasPermission = (permissionCode: string): boolean => {
    if (!user) return false;
    if (user.is_super_admin) return true;
    if (user.permissions.includes("*")) return true;
    if (user.permissions.includes(permissionCode)) return true;
    if (permissionCode.includes(".")) {
      const wildcard = `${permissionCode.split(".")[0]}.*`;
      if (user.permissions.includes(wildcard)) return true;
    }
    return false;
  };

  const hasRole = (roleCode: string): boolean => {
    if (!user) return false;
    if (user.is_super_admin) return true;
    return user.roles.some((r) => r.code.toUpperCase() === roleCode.toUpperCase());
  };

  const value = useMemo(
    () => ({
      user,
      isAuthenticated: Boolean(user),
      isLoading,
      isDarkMode,
      toggleDarkMode,
      login,
      logout,
      hasPermission,
      hasRole,
    }),
    [user, isLoading, isDarkMode]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
