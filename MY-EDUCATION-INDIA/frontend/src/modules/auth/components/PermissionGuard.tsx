import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

interface PermissionGuardProps {
  requiredPermissions: string[];
  requireAll?: boolean;
  fallbackPath?: string;
}

export const PermissionGuard: React.FC<PermissionGuardProps> = ({
  requiredPermissions,
  requireAll = true,
  fallbackPath = "/403",
}) => {
  const { user, hasPermission } = useAuth();

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (user.is_super_admin) {
    return <Outlet />;
  }

  const authorized = requireAll
    ? requiredPermissions.every((p) => hasPermission(p))
    : requiredPermissions.some((p) => hasPermission(p));

  if (!authorized) {
    return <Navigate to={fallbackPath} replace />;
  }

  return <Outlet />;
};
