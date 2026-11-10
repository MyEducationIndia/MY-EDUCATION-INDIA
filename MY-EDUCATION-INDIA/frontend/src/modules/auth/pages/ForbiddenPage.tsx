import React from "react";
import { Link } from "react-router-dom";
import { ShieldAlert, ArrowLeft } from "lucide-react";

export const ForbiddenPage: React.FC = () => {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-slate-50 px-4 text-center dark:bg-slate-900">
      <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-rose-500/10 text-rose-600 dark:bg-rose-500/20 dark:text-rose-400">
        <ShieldAlert className="h-8 w-8" />
      </div>
      <h1 className="mt-4 text-2xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-3xl">
        403 - Access Forbidden
      </h1>
      <p className="mt-2 max-w-md text-sm text-slate-600 dark:text-slate-400">
        You do not have the required institutional permissions or role clearance to access this resource.
      </p>
      <Link
        to="/admin/dashboard"
        className="mt-6 inline-flex items-center gap-2 rounded-xl bg-slate-900 px-5 py-2.5 text-xs font-semibold text-white shadow-xs transition hover:bg-slate-800 dark:bg-slate-800 dark:hover:bg-slate-700"
      >
        <ArrowLeft className="h-4 w-4" /> Go to Authorized Dashboard
      </Link>
    </div>
  );
};
