import React from "react";
import { Link } from "react-router-dom";
import { Lock, ArrowLeft } from "lucide-react";

export const UnauthorizedPage: React.FC = () => {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-slate-50 px-4 text-center dark:bg-slate-900">
      <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-amber-500/10 text-amber-600 dark:bg-amber-500/20 dark:text-amber-400">
        <Lock className="h-8 w-8" />
      </div>
      <h1 className="mt-4 text-2xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-3xl">
        401 - Authentication Required
      </h1>
      <p className="mt-2 max-w-md text-sm text-slate-600 dark:text-slate-400">
        Your session has expired or you have not provided valid authentication credentials.
      </p>
      <Link
        to="/login"
        className="mt-6 inline-flex items-center gap-2 rounded-xl bg-brand-600 px-5 py-2.5 text-xs font-semibold text-white shadow-xs transition hover:bg-brand-500"
      >
        <ArrowLeft className="h-4 w-4" /> Return to Login
      </Link>
    </div>
  );
};
