import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { motion } from "framer-motion";
import { useQuery } from "@tanstack/react-query";
import {
  ShieldCheck,
  Lock,
  UserCheck,
  Eye,
  EyeOff,
  AlertCircle,
  Moon,
  Sun,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { authApi } from "../api/authApi";
import { AxiosError } from "axios";

const loginSchema = z.object({
  identifier: z.string().min(2, "Identifier is required").max(255),
  password: z.string().min(1, "Password is required").max(128),
  remember_me: z.boolean().default(false),
  login_criterion: z.string().optional(),
});

type LoginFormValues = z.infer<typeof loginSchema>;

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, isDarkMode, toggleDarkMode } = useAuth();

  const [showPassword, setShowPassword] = useState<boolean>(false);
  const [serverError, setServerError] = useState<string | null>(null);
  const [selectedCriterion, setSelectedCriterion] = useState<string>("identifier");

  // Fetch dynamic institutional auth settings from PostgreSQL
  const { data: settings } = useQuery({
    queryKey: ["authSettings"],
    queryFn: authApi.getAuthSettings,
  });

  const availableCriteria = settings?.login_criteria || [
    "email",
    "username",
    "mobile_number",
    "roll_number",
    "erp_id",
    "student_id",
  ];

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      identifier: "",
      password: "",
      remember_me: false,
      login_criterion: "identifier",
    },
  });

  const onSelectCriterion = (crit: string) => {
    setSelectedCriterion(crit);
    setValue("login_criterion", crit);
  };

  const getCriterionPlaceholder = (crit: string): string => {
    switch (crit) {
      case "email":
        return "admin@myeducationindia.edu.in";
      case "username":
        return "superadmin";
      case "roll_number":
        return "e.g. 2026-CS-042";
      case "erp_id":
        return "e.g. ERP-99014";
      case "student_id":
        return "e.g. STU-2026-001";
      case "mobile_number":
        return "+91 98765 43210";
      default:
        return "Email, Username, Roll No, or ERP ID";
    }
  };

  const onSubmit = async (values: LoginFormValues): Promise<void> => {
    setServerError(null);
    try {
      await login({
        ...values,
        login_criterion: selectedCriterion,
      });
      const origin =
        (location.state as { from?: { pathname: string } })?.from?.pathname ||
        "/admin/dashboard";
      navigate(origin, { replace: true });
    } catch (err) {
      const axiosErr = err as AxiosError<{ error?: { message?: string } }>;
      const msg =
        axiosErr.response?.data?.error?.message ||
        "Invalid credentials. Please verify your details.";
      setServerError(msg);
    }
  };

  return (
    <div className="relative flex min-h-screen flex-col justify-center bg-slate-900 px-4 py-12 transition-colors duration-200 dark:bg-slate-950 sm:px-6 lg:px-8">
      {/* Top Controls: Dark Mode Toggle */}
      <div className="absolute right-4 top-4 sm:right-6 sm:top-6">
        <button
          type="button"
          onClick={toggleDarkMode}
          className="flex h-10 w-10 items-center justify-center rounded-xl border border-slate-700 bg-slate-800 text-slate-300 transition hover:bg-slate-700 hover:text-white"
          aria-label="Toggle visual theme"
        >
          {isDarkMode ? (
            <Sun className="h-5 w-5 text-amber-400" />
          ) : (
            <Moon className="h-5 w-5 text-slate-300" />
          )}
        </button>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35 }}
        className="mx-auto w-full max-w-md"
      >
        {/* Header */}
        <div className="flex flex-col items-center text-center">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-brand-600 text-white shadow-xl">
            <ShieldCheck className="h-8 w-8" />
          </div>
          <h1 className="mt-4 text-2xl font-extrabold tracking-tight text-white sm:text-3xl">
            MY EDUCATION INDIA
          </h1>
          <p className="mt-1 text-xs font-semibold uppercase tracking-widest text-brand-400">
            Enterprise Unified Authentication & Security Gateway
          </p>
        </div>

        {/* Card */}
        <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-950/90 p-6 shadow-2xl backdrop-blur-md sm:p-8">
          {serverError && (
            <div
              role="alert"
              className="mb-5 flex items-start gap-3 rounded-xl border border-rose-500/30 bg-rose-950/50 p-4 text-xs text-rose-200"
            >
              <AlertCircle className="h-4 w-4 shrink-0 text-rose-400 mt-0.5" />
              <span>{serverError}</span>
            </div>
          )}

          {/* Configurable Identifier Criterion Switcher */}
          <div className="mb-5">
            <label className="block text-[11px] font-semibold uppercase tracking-wider text-slate-400">
              Sign In Using
            </label>
            <div className="mt-2 flex flex-wrap gap-1.5">
              <button
                type="button"
                onClick={() => onSelectCriterion("identifier")}
                className={`rounded-lg px-2.5 py-1 text-xs font-semibold transition ${
                  selectedCriterion === "identifier"
                    ? "bg-brand-600 text-white"
                    : "bg-slate-800 text-slate-300 hover:bg-slate-700"
                }`}
              >
                Auto-Detect
              </button>
              {availableCriteria.map((crit) => (
                <button
                  key={crit}
                  type="button"
                  onClick={() => onSelectCriterion(crit)}
                  className={`rounded-lg px-2.5 py-1 text-xs font-semibold capitalize transition ${
                    selectedCriterion === crit
                      ? "bg-brand-600 text-white"
                      : "bg-slate-800 text-slate-300 hover:bg-slate-700"
                  }`}
                >
                  {crit.replace("_", " ")}
                </button>
              ))}
            </div>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" noValidate>
            <div>
              <label
                htmlFor="identifier"
                className="block text-xs font-semibold uppercase tracking-wider text-slate-300"
              >
                {selectedCriterion === "identifier"
                  ? "Institutional Identifier"
                  : selectedCriterion.replace("_", " ")}
              </label>
              <div className="relative mt-1.5">
                <UserCheck className="pointer-events-none absolute left-3.5 top-3 h-4 w-4 text-slate-500" />
                <input
                  id="identifier"
                  type="text"
                  autoComplete="username"
                  {...register("identifier")}
                  className="block w-full rounded-xl border border-slate-700 bg-slate-900 py-2.5 pl-10 pr-3.5 text-sm text-white placeholder-slate-500 focus:border-brand-500 focus:outline-hidden focus:ring-2 focus:ring-brand-500/30"
                  placeholder={getCriterionPlaceholder(selectedCriterion)}
                />
              </div>
              {errors.identifier && (
                <p className="mt-1 text-xs text-rose-400">
                  {errors.identifier.message}
                </p>
              )}
            </div>

            <div>
              <div className="flex items-center justify-between">
                <label
                  htmlFor="password"
                  className="block text-xs font-semibold uppercase tracking-wider text-slate-300"
                >
                  Password
                </label>
              </div>
              <div className="relative mt-1.5">
                <Lock className="pointer-events-none absolute left-3.5 top-3 h-4 w-4 text-slate-500" />
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  autoComplete="current-password"
                  {...register("password")}
                  className="block w-full rounded-xl border border-slate-700 bg-slate-900 py-2.5 pl-10 pr-10 text-sm text-white placeholder-slate-500 focus:border-brand-500 focus:outline-hidden focus:ring-2 focus:ring-brand-500/30"
                  placeholder="••••••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((prev) => !prev)}
                  className="absolute right-3 top-2.5 text-slate-400 hover:text-white"
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? (
                    <EyeOff className="h-4 w-4" />
                  ) : (
                    <Eye className="h-4 w-4" />
                  )}
                </button>
              </div>
              {errors.password && (
                <p className="mt-1 text-xs text-rose-400">
                  {errors.password.message}
                </p>
              )}
            </div>

            {/* Remember Me Checkbox */}
            <div className="flex items-center justify-between pt-1">
              <label className="flex items-center gap-2 text-xs font-medium text-slate-300 cursor-pointer">
                <input
                  type="checkbox"
                  {...register("remember_me")}
                  className="h-4 w-4 rounded-sm border-slate-700 bg-slate-900 text-brand-600 focus:ring-brand-500"
                />
                <span>Remember me on this trusted device</span>
              </label>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="mt-2 flex w-full items-center justify-center rounded-xl bg-brand-600 px-4 py-3 text-sm font-semibold text-white shadow-lg transition hover:bg-brand-500 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isSubmitting
                ? "Establishing Authenticated Session..."
                : "Sign In to Enterprise Gateway"}
            </button>
          </form>

          <div className="mt-5 border-t border-slate-800 pt-3 text-center">
            <p className="text-[11px] text-slate-500">
              Protected by Argon2id Password Hashing, Automatic Session Rotation,
              and Zero-LocalStorage In-Memory Token Architecture.
            </p>
          </div>

          <div className="mt-4 rounded-xl bg-slate-950/60 border border-slate-800 p-3 text-center">
            <p className="text-[11px] text-amber-400 font-semibold">
              Single Auth Policy: Institutional User ID + Password Only
            </p>
            <p className="text-[10px] text-slate-500 mt-0.5">
              Self-service password recovery is disabled. Password resets are handled by campus administrators upon physical verification.
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};
