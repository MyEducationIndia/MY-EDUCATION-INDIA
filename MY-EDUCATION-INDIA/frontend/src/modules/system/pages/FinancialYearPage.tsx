import React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Coins, CheckCircle2 } from "lucide-react";
import { systemApi } from "../api/systemApi";

const fySchema = z.object({
  code: z.string().min(4).max(32),
  name: z.string().min(2).max(120),
  start_date: z.string(),
  end_date: z.string(),
  gstin: z.string().optional(),
  is_current: z.boolean().default(false),
});

type FyFormValues = z.infer<typeof fySchema>;

export const FinancialYearPage: React.FC = () => {
  const queryClient = useQueryClient();

  const { data: institutes = [] } = useQuery({ queryKey: ["systemInstitutes"], queryFn: systemApi.listInstitutes });
  const instId = institutes[0]?.id;

  const { data: years = [], isLoading } = useQuery({
    queryKey: ["systemFinancialYears", instId],
    queryFn: () => (instId ? systemApi.listFinancialYears(instId) : Promise.resolve([])),
    enabled: Boolean(instId),
  });

  const createMutation = useMutation({
    mutationFn: (values: FyFormValues) => {
      if (!instId) throw new Error("Institute required");
      return systemApi.createFinancialYear({ ...values, institute_id: instId });
    },
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["systemFinancialYears"] });
      reset();
    },
  });

  const setCurrentMutation = useMutation({
    mutationFn: (fyId: string) => systemApi.setCurrentFinancialYear(fyId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["systemFinancialYears"] });
    },
  });

  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm<FyFormValues>({
    resolver: zodResolver(fySchema),
    defaultValues: {
      code: "FY2026-27",
      name: "Financial Year 2026-2027",
      start_date: "2026-04-01",
      end_date: "2027-03-31",
      gstin: "23AABCU9603R1ZX",
      is_current: false,
    },
  });

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900 lg:col-span-1">
        <h2 className="text-sm font-bold text-slate-900 dark:text-white">Create Financial Year (GST Ready)</h2>
        <form onSubmit={handleSubmit((d) => createMutation.mutate(d))} className="mt-4 space-y-3">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Fiscal Code</label>
            <input type="text" {...register("code")} placeholder="FY2026-27" className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
            {errors.code && <p className="mt-1 text-xs text-rose-600">{errors.code.message}</p>}
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Fiscal Name</label>
            <input type="text" {...register("name")} placeholder="Financial Year 2026-2027" className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
          </div>

          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Start Date</label>
              <input type="date" {...register("start_date")} className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">End Date</label>
              <input type="date" {...register("end_date")} className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Institutional GSTIN</label>
            <input type="text" {...register("gstin")} placeholder="23AABCU9603R1ZX" className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
          </div>

          <label className="flex items-center gap-2 pt-1 text-xs text-slate-700 dark:text-slate-300 cursor-pointer">
            <input type="checkbox" {...register("is_current")} className="rounded-sm border-slate-300 text-brand-600" />
            <span>Set as Current Financial Year</span>
          </label>

          <button type="submit" disabled={isSubmitting} className="w-full rounded-lg bg-brand-600 py-2.5 text-xs font-semibold text-white hover:bg-brand-500 disabled:opacity-50">
            {isSubmitting ? "Creating..." : "Save Financial Year"}
          </button>
        </form>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900 lg:col-span-2">
        <h2 className="text-sm font-bold text-slate-900 dark:text-white">Active Financial Years ({years.length})</h2>
        <div className="mt-4 space-y-3">
          {isLoading ? (
            <p className="text-xs text-slate-500">Loading fiscal records...</p>
          ) : (
            years.map((y) => (
              <div key={y.id} className="flex items-center justify-between rounded-xl border border-slate-200 p-4 dark:border-slate-800 dark:bg-slate-950/40">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-bold text-slate-900 dark:text-white">{y.name}</span>
                    <span className="rounded-sm bg-slate-100 px-2 py-0.5 font-mono text-[11px] text-slate-700 dark:bg-slate-800 dark:text-slate-300">{y.code}</span>
                    {y.is_current && (
                      <span className="inline-flex items-center gap-1 rounded-sm bg-emerald-50 px-2 py-0.5 text-[10px] font-bold text-emerald-700 dark:bg-emerald-950 dark:text-emerald-400">
                        <CheckCircle2 className="h-3 w-3" /> Active Fiscal Year
                      </span>
                    )}
                  </div>
                  <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                    Period: {y.start_date} to {y.end_date} {y.gstin ? `• GSTIN: ${y.gstin}` : ""}
                  </p>
                </div>

                {!y.is_current && (
                  <button
                    type="button"
                    onClick={() => setCurrentMutation.mutate(y.id)}
                    className="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200"
                  >
                    Set Active
                  </button>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
