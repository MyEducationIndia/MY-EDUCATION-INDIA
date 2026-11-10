import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

interface RoleGuardProps {
  allowedRoles: string[];
  fallbackPath?: string;
}

export const RoleGuard: React.FC<RoleGuardProps> = ({
  allowedRoles,
  fallbackPath = "/403",
}) => {
  const { user, hasRole } = useAuth();

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (user.is_super_admin) {
    return <Outlet />;
  }

  const allowed = allowedRoles.some((r) => hasRole(r));
  if (!allowed) {
    return <Navigate to={fallbackPath} replace />;
  }

  return <Outlet />;
};
