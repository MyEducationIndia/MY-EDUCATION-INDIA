import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { motion } from "framer-motion";
import { ShieldCheck, Lock, UserCheck, AlertCircle } from "lucide-react";
import { authService } from "@/services/authService";
import { AxiosError } from "axios";
import { ApiErrorPayload } from "@/types/common.types";

const loginSchema = z.object({
  identifier: z
    .string()
    .min(3, "Enter a valid institutional email or username")
    .max(255),
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .max(128),
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
    },
  });

  const onSubmit = async (values: LoginFormValues): Promise<void> => {
    setServerError(null);
    try {
      await authService.login(values);
      navigate("/admin/dashboard", { replace: true });
    } catch (err) {
      const axiosErr = err as AxiosError<ApiErrorPayload>;
      const message =
        axiosErr.response?.data?.error?.message ||
        "Authentication failed. Verify your credentials and network connection.";
      setServerError(message);
    }
  };

  return (
    <div className="flex min-h-screen flex-col justify-center bg-slate-900 px-4 py-12 sm:px-6 lg:px-8">
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35 }}
        className="mx-auto w-full max-w-md"
      >
        <div className="flex flex-col items-center text-center">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-brand-600 text-white shadow-lg">
            <ShieldCheck className="h-8 w-8" />
          </div>
          <h1 className="mt-4 text-2xl font-extrabold tracking-tight text-white sm:text-3xl">
            MY EDUCATION INDIA
          </h1>
          <p className="mt-1.5 text-sm text-slate-400">
            Enterprise Unified ERP, LMS & CBT Identity Gateway
          </p>
        </div>

        <div className="mt-8 rounded-2xl border border-slate-800 bg-slate-950/90 p-6 shadow-2xl sm:p-8">
          {serverError && (
            <div
              role="alert"
              className="mb-6 flex items-start gap-3 rounded-xl border border-rose-500/30 bg-rose-950/50 p-4 text-xs text-rose-200"
            >
              <AlertCircle className="h-4 w-4 shrink-0 text-rose-400 mt-0.5" />
              <span>{serverError}</span>
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5" noValidate>
            <div>
              <label
                htmlFor="identifier"
                className="block text-xs font-semibold uppercase tracking-wider text-slate-300"
              >
                Institutional Email or Username
              </label>
              <div className="relative mt-1.5">
                <UserCheck className="pointer-events-none absolute left-3.5 top-3 h-4 w-4 text-slate-500" />
                <input
                  id="identifier"
                  type="text"
                  autoComplete="username"
                  {...register("identifier")}
                  className="block w-full rounded-xl border border-slate-700 bg-slate-900 py-2.5 pl-10 pr-3.5 text-sm text-white placeholder-slate-500 focus:border-brand-500 focus:outline-hidden focus:ring-2 focus:ring-brand-500/30"
                  placeholder="admin@myeducationindia.edu.in"
                />
              </div>
              {errors.identifier && (
                <p className="mt-1.5 text-xs text-rose-400">
                  {errors.identifier.message}
                </p>
              )}
            </div>

            <div>
              <label
                htmlFor="password"
                className="block text-xs font-semibold uppercase tracking-wider text-slate-300"
              >
                Password
              </label>
              <div className="relative mt-1.5">
                <Lock className="pointer-events-none absolute left-3.5 top-3 h-4 w-4 text-slate-500" />
                <input
                  id="password"
                  type="password"
                  autoComplete="current-password"
                  {...register("password")}
                  className="block w-full rounded-xl border border-slate-700 bg-slate-900 py-2.5 pl-10 pr-3.5 text-sm text-white placeholder-slate-500 focus:border-brand-500 focus:outline-hidden focus:ring-2 focus:ring-brand-500/30"
                  placeholder="••••••••••••"
                />
              </div>
              {errors.password && (
                <p className="mt-1.5 text-xs text-rose-400">
                  {errors.password.message}
                </p>
              )}
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="flex w-full items-center justify-center rounded-xl bg-brand-600 px-4 py-3 text-sm font-semibold text-white shadow-md transition hover:bg-brand-500 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isSubmitting
                ? "Establishing Encrypted Session..."
                : "Sign In to Enterprise Portal"}
            </button>
          </form>

          <div className="mt-6 border-t border-slate-800 pt-4 text-center">
            <p className="text-[11px] text-slate-500">
              Protected by Argon2id Password Hashing, HttpOnly Refresh Token Rotation,
              and Strict Zero-LocalStorage Session Architecture.
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};
