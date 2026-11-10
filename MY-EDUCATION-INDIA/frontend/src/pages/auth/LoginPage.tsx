import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { motion } from "framer-motion";
import {
  ShieldCheck,
  Lock,
  UserCheck,
  AlertCircle,
  ArrowLeft,
  RefreshCw,
  Fingerprint,
  ShieldAlert,
} from "lucide-react";
import { authService } from "@/services/authService";
import { AxiosError } from "axios";
import { ApiErrorPayload } from "@/types/common.types";

const loginSchema = z.object({
  identifier: z
    .string()
    .min(3, "Enter a valid Institutional User ID (e.g. STU240001, FAC240001)")
    .max(64),
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .max(128),
  remember_me: z.boolean().default(false),
});

type LoginFormValues = z.infer<typeof loginSchema>;

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const [serverError, setServerError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      identifier: "",
      password: "",
      remember_me: false,
    },
  });

  const handleRouteByRoles = (roles: string[], isSuperAdmin: boolean) => {
    if (isSuperAdmin || roles.includes("ROOT_OWNER") || roles.includes("SUPER_ADMIN")) {
      navigate("/admin/dashboard", { replace: true });
    } else if (roles.includes("ACCOUNTANT")) {
      navigate("/admin/fees", { replace: true });
    } else if (roles.includes("COUNSELLOR")) {
      navigate("/admin/crm", { replace: true });
    } else if (roles.includes("EXAM_CONTROLLER")) {
      navigate("/admin/exams", { replace: true });
    } else if (roles.includes("FACULTY") || roles.includes("INSTITUTE_ADMIN")) {
      navigate("/admin/academics", { replace: true });
    } else if (roles.includes("STUDENT")) {
      navigate("/admin/cbt", { replace: true });
    } else {
      navigate("/admin/dashboard", { replace: true });
    }
  };

  const onPasswordSubmit = async (values: LoginFormValues): Promise<void> => {
    setServerError(null);
    try {
      const session = await authService.login(values);
      const user = session.user;
      handleRouteByRoles(user.roles || [], user.is_super_admin);
    } catch (err) {
      const axiosErr = err as AxiosError<ApiErrorPayload>;
      const errorMsg =
        axiosErr.response?.data?.error?.message ||
        "Invalid User ID or Password. Identity verification failed.";
      setServerError(errorMsg);
    }
  };

  return (
    <div className="relative min-h-screen bg-slate-950 font-sans text-slate-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8 selection:bg-brand-500 selection:text-white">
      {/* Background Aesthetic */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 left-1/2 -translate-x-1/2 w-[700px] h-[350px] bg-brand-600/15 blur-[120px] rounded-full" />
        <div className="absolute bottom-0 right-10 w-[400px] h-[300px] bg-amber-500/10 blur-[100px] rounded-full" />
      </div>

      <div className="relative z-10 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-start mb-6">
          <Link
            to="/"
            className="inline-flex items-center gap-2 text-xs font-semibold text-slate-400 hover:text-white transition group"
          >
            <ArrowLeft className="h-3.5 w-3.5 transition group-hover:-translate-x-0.5" />
            <span>Back to Public Website</span>
          </Link>
        </div>

        <div className="flex flex-col items-center text-center">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-brand-600 text-white shadow-xl shadow-brand-600/30">
            <ShieldCheck className="h-8 w-8" />
          </div>
          <h1 className="mt-4 text-2xl font-extrabold tracking-tight text-white sm:text-3xl">
            MY EDUCATION INDIA
          </h1>
          <p className="mt-1.5 text-xs text-slate-400">
            Autonomous Campus ERP & Unified Portals • Sovereign Access Control
          </p>
          <div className="mt-2 inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-mono font-medium bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
            <Fingerprint className="w-3.5 h-3.5" />
            STRICT SECURITY: USER ID + PASSWORD ONLY
          </div>
        </div>

        {/* Authentication Card */}
        <div className="mt-6 rounded-3xl bg-slate-900/90 p-8 shadow-2xl border border-slate-800 backdrop-blur-md space-y-5">
          {serverError && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              className="rounded-xl border border-rose-500/40 bg-rose-500/10 p-4 text-xs font-medium text-rose-300 flex items-start gap-2.5"
            >
              <AlertCircle className="h-4 w-4 shrink-0 text-rose-400 mt-0.5" />
              <div className="space-y-1">
                <span className="font-bold block">Access Restricted</span>
                <span>{serverError}</span>
              </div>
            </motion.div>
          )}

          <form onSubmit={handleSubmit(onPasswordSubmit)} className="space-y-4">
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-300">
                Institutional User ID *
              </label>
              <div className="mt-1.5 relative">
                <input
                  {...register("identifier")}
                  type="text"
                  autoComplete="username"
                  placeholder="e.g. STU240001, FAC240001, ADM000001"
                  className="block w-full rounded-xl border border-slate-700 bg-slate-950/70 px-4 py-2.5 text-sm font-mono text-white placeholder-slate-500 transition focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
                />
                {errors.identifier && (
                  <p className="mt-1 text-xs text-rose-400">
                    {errors.identifier.message}
                  </p>
                )}
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-300">
                Password *
              </label>
              <div className="mt-1.5 relative">
                <input
                  {...register("password")}
                  type="password"
                  autoComplete="current-password"
                  placeholder="••••••••••••"
                  className="block w-full rounded-xl border border-slate-700 bg-slate-950/70 px-4 py-2.5 text-sm text-white placeholder-slate-500 transition focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
                />
                {errors.password && (
                  <p className="mt-1 text-xs text-rose-400">
                    {errors.password.message}
                  </p>
                )}
              </div>
            </div>

            <div className="flex items-center justify-between pt-1">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  {...register("remember_me")}
                  type="checkbox"
                  className="h-4 w-4 rounded border-slate-700 bg-slate-950 text-brand-600 focus:ring-brand-500"
                />
                <span className="text-xs text-slate-400">Remember session</span>
              </label>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 px-4 py-3 text-sm font-bold text-white shadow-lg shadow-brand-600/30 transition hover:bg-brand-500 focus:outline-none disabled:opacity-50"
            >
              {isSubmitting ? (
                <RefreshCw className="h-4 w-4 animate-spin" />
              ) : (
                <UserCheck className="h-4 w-4" />
              )}
              <span>Sign In with User ID & Password</span>
            </button>
          </form>

          {/* Institutional Password Policy Notice */}
          <div className="mt-5 rounded-xl bg-slate-950/60 border border-slate-800 p-3.5 space-y-1 text-center">
            <div className="flex items-center justify-center gap-1.5 text-xs font-bold text-amber-400">
              <Lock className="w-3.5 h-3.5" />
              Security Notice
            </div>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              Public self-service password recovery is disabled. Password resets are administered strictly by Campus Administration upon verified identity presentation.
            </p>
          </div>
        </div>

        <div className="mt-6 text-center text-xs text-slate-500 font-mono">
          MY EDUCATION INDIA • Phase 1–5 Unified Autonomous Campus Platform
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
