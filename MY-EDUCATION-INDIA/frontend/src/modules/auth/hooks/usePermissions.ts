import { useAuth } from "../context/AuthContext";

export function usePermissions() {
  const { user, hasPermission, hasRole } = useAuth();

  return {
    permissions: user?.permissions || [],
    hasPermission,
    hasRole,
    isSuperAdmin: Boolean(user?.is_super_admin),
  };
}
