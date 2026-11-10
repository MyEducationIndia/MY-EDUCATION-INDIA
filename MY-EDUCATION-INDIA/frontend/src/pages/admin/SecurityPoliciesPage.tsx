import React, { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  ShieldCheck,
  Lock,
  Key,
  Clock,
  AlertTriangle,
  CheckCircle2,
  Save,
  RefreshCw,
  Sliders,
  UserCheck,
} from "lucide-react";
import { authService } from "@/services/authService";
import { SecurityPolicy } from "@/types/auth.types";

export const SecurityPoliciesPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const {
    data: policy,
    isLoading,
    refetch,
  } = useQuery<SecurityPolicy>({
    queryKey: ["security_policy"],
    queryFn: authService.getSecurityPolicy,
  });

  const [formState, setFormState] = useState<Partial<SecurityPolicy>>({
    min_password_length: 10,
    require_uppercase: true,
    require_numbers: true,
    require_special_chars: true,
    password_expiry_days: 90,
    max_failed_attempts: 5,
    lockout_duration_minutes: 30,
    session_timeout_minutes: 60,
    enforce_2fa: false,
    allow_remember_me: true,
    remember_me_days: 30,
  });

  useEffect(() => {
    if (policy) {
      setFormState({
        min_password_length: policy.min_password_length,
        require_uppercase: policy.require_uppercase,
        require_numbers: policy.require_numbers,
        require_special_chars: policy.require_special_chars,
        password_expiry_days: policy.password_expiry_days,
        max_failed_attempts: policy.max_failed_attempts,
        lockout_duration_minutes: policy.lockout_duration_minutes,
        session_timeout_minutes: policy.session_timeout_minutes,
        enforce_2fa: policy.enforce_2fa,
        allow_remember_me: policy.allow_remember_me,
        remember_me_days: policy.remember_me_days,
      });
    }
  }, [policy]);

  const updateMutation = useMutation({
    mutationFn: async (payload: Partial<SecurityPolicy>) => {
      return await authService.updateSecurityPolicy(payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["security_policy"] });
      setSuccessMessage("Security policy matrix updated and propagated across all auth gates.");
      setTimeout(() => setSuccessMessage(null), 3500);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    updateMutation.mutate(formState);
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-xl border border-slate-800">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="space-y-1.5">
            <div className="flex items-center gap-2 text-indigo-400 font-semibold text-xs tracking-wider uppercase">
              <ShieldCheck className="w-4 h-4" /> Phase 2 Module 1 Security Governance
            </div>
            <h1 className="text-2xl sm:text-3xl font-black text-white">
              Institutional Security Policies
            </h1>
            <p className="text-slate-300 text-xs sm:text-sm max-w-2xl leading-relaxed">
              Configure password complexity thresholds, account lockout limits,
              session timeout durations, and multi-factor authentication (2FA) rules
              for all scholars, faculty, and administrators.
            </p>
          </div>

          <button
            onClick={() => refetch()}
            className="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-bold transition border border-slate-700 flex items-center gap-1.5"
          >
            <RefreshCw className="w-3.5 h-3.5" /> Reload Policies
          </button>
        </div>
      </div>

      {successMessage && (
        <div className="p-4 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-2xl text-xs font-semibold flex items-center gap-2 animate-in fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
          <span>{successMessage}</span>
        </div>
      )}

      {/* Policies Form Container */}
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Section 1: Password Complexity Rules */}
          <div className="bg-white rounded-3xl p-6 border border-slate-200/90 shadow-sm space-y-4">
            <div className="flex items-center gap-2.5 pb-2 border-b border-slate-100">
              <Key className="w-5 h-5 text-indigo-600" />
              <div>
                <h3 className="font-bold text-slate-900 text-sm">
                  Password Complexity & Lifecycle
                </h3>
                <p className="text-xs text-slate-500">
                  Enforces OWASP-compliant Argon2 password strength.
                </p>
              </div>
            </div>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Minimum Password Length (Characters)
                </label>
                <input
                  type="number"
                  min={8}
                  max={32}
                  value={formState.min_password_length || 10}
                  onChange={(e) =>
                    setFormState({
                      ...formState,
                      min_password_length: parseInt(e.target.value) || 10,
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl px-3 py-2 text-xs font-bold outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Password Validity Window (Days)
                </label>
                <input
                  type="number"
                  min={30}
                  max={365}
                  value={formState.password_expiry_days || 90}
                  onChange={(e) =>
                    setFormState({
                      ...formState,
                      password_expiry_days: parseInt(e.target.value) || 90,
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl px-3 py-2 text-xs font-bold outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div className="space-y-2 pt-2">
                <label className="flex items-center gap-2 text-xs text-slate-700 font-semibold cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formState.require_uppercase}
                    onChange={(e) =>
                      setFormState({
                        ...formState,
                        require_uppercase: e.target.checked,
                      })
                    }
                    className="w-4 h-4 text-indigo-600 rounded"
                  />
                  <span>Require at least one uppercase letter (A-Z)</span>
                </label>

                <label className="flex items-center gap-2 text-xs text-slate-700 font-semibold cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formState.require_numbers}
                    onChange={(e) =>
                      setFormState({
                        ...formState,
                        require_numbers: e.target.checked,
                      })
                    }
                    className="w-4 h-4 text-indigo-600 rounded"
                  />
                  <span>Require at least one numerical digit (0-9)</span>
                </label>

                <label className="flex items-center gap-2 text-xs text-slate-700 font-semibold cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formState.require_special_chars}
                    onChange={(e) =>
                      setFormState({
                        ...formState,
                        require_special_chars: e.target.checked,
                      })
                    }
                    className="w-4 h-4 text-indigo-600 rounded"
                  />
                  <span>Require at least one special character (!@#$%^&*)</span>
                </label>
              </div>
            </div>
          </div>

          {/* Section 2: Account Lockout & Brute-Force Safeguards */}
          <div className="bg-white rounded-3xl p-6 border border-slate-200/90 shadow-sm space-y-4">
            <div className="flex items-center gap-2.5 pb-2 border-b border-slate-100">
              <Lock className="w-5 h-5 text-rose-600" />
              <div>
                <h3 className="font-bold text-slate-900 text-sm">
                  Account Lockout & Brute-Force Safeguards
                </h3>
                <p className="text-xs text-slate-500">
                  Automated lockout mitigation against credential stuffing attacks.
                </p>
              </div>
            </div>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Maximum Failed Attempts Before Lockout
                </label>
                <input
                  type="number"
                  min={3}
                  max={10}
                  value={formState.max_failed_attempts || 5}
                  onChange={(e) =>
                    setFormState({
                      ...formState,
                      max_failed_attempts: parseInt(e.target.value) || 5,
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl px-3 py-2 text-xs font-bold outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Temporary Lockout Duration (Minutes)
                </label>
                <input
                  type="number"
                  min={5}
                  max={1440}
                  value={formState.lockout_duration_minutes || 30}
                  onChange={(e) =>
                    setFormState({
                      ...formState,
                      lockout_duration_minutes: parseInt(e.target.value) || 30,
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl px-3 py-2 text-xs font-bold outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div className="p-3.5 bg-slate-50 rounded-2xl border border-slate-100 text-xs text-slate-600 space-y-1">
                <p className="font-bold text-slate-800">Lockout Mechanism:</p>
                <p>
                  Upon 5 consecutive failed passwords, the account is locked in
                  PostgreSQL. Self-service reset via OTP instantly lifts the restriction.
                </p>
              </div>
            </div>
          </div>

          {/* Section 3: Session Lifecycles */}
          <div className="bg-white rounded-3xl p-6 border border-slate-200/90 shadow-sm space-y-4">
            <div className="flex items-center gap-2.5 pb-2 border-b border-slate-100">
              <Clock className="w-5 h-5 text-indigo-600" />
              <div>
                <h3 className="font-bold text-slate-900 text-sm">
                  Session Lifecycles & Remember Me
                </h3>
                <p className="text-xs text-slate-500">
                  Idle timeout rules and long-lived trusted device parameters.
                </p>
              </div>
            </div>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Idle Session Timeout (Minutes)
                </label>
                <input
                  type="number"
                  min={15}
                  max={480}
                  value={formState.session_timeout_minutes || 60}
                  onChange={(e) =>
                    setFormState({
                      ...formState,
                      session_timeout_minutes: parseInt(e.target.value) || 60,
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl px-3 py-2 text-xs font-bold outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Remember Me Validity (Days)
                </label>
                <input
                  type="number"
                  min={1}
                  max={90}
                  value={formState.remember_me_days || 30}
                  onChange={(e) =>
                    setFormState({
                      ...formState,
                      remember_me_days: parseInt(e.target.value) || 30,
                    })
                  }
                  className="w-full border border-slate-300 rounded-xl px-3 py-2 text-xs font-bold outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <label className="flex items-center gap-2 text-xs text-slate-700 font-semibold cursor-pointer pt-1">
                <input
                  type="checkbox"
                  checked={formState.allow_remember_me}
                  onChange={(e) =>
                    setFormState({
                      ...formState,
                      allow_remember_me: e.target.checked,
                    })
                  }
                  className="w-4 h-4 text-indigo-600 rounded"
                />
                <span>Allow "Remember this device" on student and faculty login</span>
              </label>
            </div>
          </div>

          {/* Section 4: Multi-Factor Authentication */}
          <div className="bg-white rounded-3xl p-6 border border-slate-200/90 shadow-sm space-y-4">
            <div className="flex items-center gap-2.5 pb-2 border-b border-slate-100">
              <UserCheck className="w-5 h-5 text-emerald-600" />
              <div>
                <h3 className="font-bold text-slate-900 text-sm">
                  Two-Factor Authentication (2FA / MFA)
                </h3>
                <p className="text-xs text-slate-500">
                  TOTP authenticator app and SMS OTP second factor.
                </p>
              </div>
            </div>

            <div className="space-y-3">
              <label className="flex items-start gap-2.5 text-xs text-slate-700 font-semibold cursor-pointer p-3 bg-slate-50 rounded-2xl border border-slate-100">
                <input
                  type="checkbox"
                  checked={formState.enforce_2fa}
                  onChange={(e) =>
                    setFormState({
                      ...formState,
                      enforce_2fa: e.target.checked,
                    })
                  }
                  className="w-4 h-4 text-indigo-600 rounded mt-0.5"
                />
                <div>
                  <span className="block text-slate-900 font-bold">
                    Enforce Mandatory 2FA for Administrative Roles
                  </span>
                  <span className="text-[11px] text-slate-500 font-normal block mt-0.5">
                    Requires Super Admins, Accountants, and Exam Controllers to enter a 6-digit TOTP code on login.
                  </span>
                </div>
              </label>
            </div>
          </div>
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={updateMutation.isPending}
            className="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl text-xs font-bold transition flex items-center gap-2 shadow-lg disabled:opacity-50"
          >
            {updateMutation.isPending ? (
              <RefreshCw className="w-4 h-4 animate-spin" />
            ) : (
              <Save className="w-4 h-4" />
            )}
            <span>Save Security Policies</span>
          </button>
        </div>
      </form>
    </div>
  );
};
