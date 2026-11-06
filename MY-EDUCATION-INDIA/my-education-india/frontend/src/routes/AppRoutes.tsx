import { PublicHomePage } from "@/pages/PublicHomePage";
export const AppRoutes: React.FC = () => {
  return (
    <Routes>
      {/* 1. Public Facing Institute Website (Default Root '/') */}
      <Route path="/" element={<PublicHomePage />} />

      {/* 2. Public Authentication Route ('/login') */}
      <Route path="/login" element={<LoginPage />} />

      {/* 3. Protected Enterprise Command Center Routes ('/admin/*') */}
      <Route element={<ProtectedRoute />}>
        <Route path="/admin" element={<SuperAdminLayout />}>
          <Route index element={<Navigate to="dashboard" replace />} />
          <Route path="dashboard" element={<DashboardOverviewPage />} />
          <Route path="modules" element={<SuperAdminDashboardPage />} />
          {/* ... all other subsystem routes ... */}
        </Route>
      </Route>

      {/* Fallback to homepage */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

import React from "react";
import { Routes, Route, Navigate, Outlet } from "react-router-dom";
import { LoginPage } from "@/pages/auth/LoginPage";
import { SuperAdminLayout } from "@/layouts/SuperAdminLayout";
import { SuperAdminDashboardPage } from "@/pages/admin/SuperAdminDashboardPage";
import { RolesPermissionsPage } from "@/pages/admin/RolesPermissionsPage";
import { UsersManagementPage } from "@/pages/admin/UsersManagementPage";
import { AuditLogsPage } from "@/pages/admin/AuditLogsPage";
import { useAuthSession } from "@/hooks/useAuthSession";

/**
 * Enterprise Protected Route wrapper
 * Protects administrative paths using volatile in-memory authentication state.
 */
const ProtectedRoute: React.FC = () => {
  const { isAuthenticated, isInitializing } = useAuthSession();

  if (isInitializing) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50">
        <div className="flex flex-col items-center gap-3">
          <div className="h-10 w-10 animate-spin rounded-full border-4 border-brand-600 border-t-transparent" />
          <p className="text-sm font-medium text-slate-600">
            Verifying secure session...
          </p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
};

export const AppRoutes: React.FC = () => {
  return (
    <Routes>
      {/* Public Authentication Route */}
      <Route path="/login" element={<LoginPage />} />

      {/* Protected Admin Routes */}
      <Route element={<ProtectedRoute />}>
        <Route path="/admin" element={<SuperAdminLayout />}>
          <Route index element={<Navigate to="dashboard" replace />} />
          <Route path="dashboard" element={<SuperAdminDashboardPage />} />
          <Route path="modules" element={<SuperAdminDashboardPage />} />
          <Route path="roles" element={<RolesPermissionsPage />} />
          <Route path="users" element={<UsersManagementPage />} />
          <Route path="audit-logs" element={<AuditLogsPage />} />
        </Route>
      </Route>

      {/* Fallbacks */}
      <Route path="/" element={<Navigate to="/admin/dashboard" replace />} />
      <Route path="*" element={<Navigate to="/admin/dashboard" replace />} />
    </Routes>
  );
};
