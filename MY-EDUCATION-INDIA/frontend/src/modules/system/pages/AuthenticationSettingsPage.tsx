import React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { KeyRound, ShieldAlert } from "lucide-react";
import { authApi } from "@/modules/auth/api/authApi";

export const AuthenticationSettingsPage: React.FC = () => {
  const queryClient = useQueryClient();

  const { data: config, isLoading } = useQuery({
    queryKey: ["authSettings"],
    queryFn: authApi.getAuthSettings,
  });

  const { register, handleSubmit } = useForm({
    defaultValues: {
      password_min_length: 10,
      session_timeout_minutes: 60,
      allow_remember_me: true,
      password_require_uppercase: true,
      password_require_special: true,
    },
  });

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs dark:border-slate-800 dark:bg-slate-900">
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-50 text-amber-600 dark:bg-amber-950 dark:text-amber-400">
          <KeyRound className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-base font-bold text-slate-900 dark:text-white">
            Authentication & Security Policies
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Stored in PostgreSQL `system_settings` table. Configures dynamic login criteria, password policy, and lockout parameters.
          </p>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div className="rounded-xl border border-slate-200 p-4 dark:border-slate-800">
          <h3 className="text-xs font-bold uppercase text-slate-700 dark:text-slate-300">
            Active Multi-Login Criteria
          </h3>
          <p className="mt-1 text-xs text-slate-500">
            Users across portals can authenticate with any of these database-configured criteria:
          </p>
          <div className="mt-3 flex flex-wrap gap-1.5">
            {(config?.login_criteria || ["email", "username", "roll_number", "erp_id", "mobile_number"]).map((c) => (
              <span key={c} className="rounded-md bg-brand-50 px-2.5 py-1 text-xs font-semibold capitalize text-brand-700 dark:bg-brand-950 dark:text-brand-300">
                {c.replace("_", " ")}
              </span>
            ))}
          </div>
        </div>

        <div className="rounded-xl border border-slate-200 p-4 dark:border-slate-800">
          <h3 className="text-xs font-bold uppercase text-slate-700 dark:text-slate-300">
            Security & Lockout Thresholds
          </h3>
          <div className="mt-3 space-y-2 text-xs text-slate-600 dark:text-slate-400">
            <div className="flex justify-between">
              <span>Max Failed Attempts:</span>
              <strong className="text-slate-900 dark:text-white">5 Attempts (15-min lockout)</strong>
            </div>
            <div className="flex justify-between">
              <span>Password History Buffer:</span>
              <strong className="text-slate-900 dark:text-white">Last 5 Passwords Locked</strong>
            </div>
            <div className="flex justify-between">
              <span>Session Inactivity Timeout:</span>
              <strong className="text-slate-900 dark:text-white">{config?.session_timeout_minutes || 60} Minutes</strong>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
