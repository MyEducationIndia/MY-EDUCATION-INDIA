import React, { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Binary, Sparkles, CheckCircle2 } from "lucide-react";
import { systemApi } from "../api/systemApi";

const numGenSchema = z.object({
  entity_type: z.string().min(2).max(64),
  name: z.string().min(2).max(150),
  prefix: z.string().optional(),
  suffix: z.string().optional(),
  format_template: z.string().min(5).max(150),
  separator: z.string().min(1).max(4),
  padding_length: z.coerce.number().min(3).max(12),
  reset_rule: z.enum(["NEVER", "YEARLY", "ACADEMIC_YEAR", "FINANCIAL_YEAR", "MONTHLY", "BRANCH"]),
});

type NumGenFormValues = z.infer<typeof numGenSchema>;

export const NumberGeneratorPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [livePreview, setLivePreview] = useState<string>("");

  const { data: institutes = [] } = useQuery({ queryKey: ["systemInstitutes"], queryFn: systemApi.listInstitutes });
  const instId = institutes[0]?.id;

  const { data: generators = [], isLoading } = useQuery({
    queryKey: ["systemNumberGenerators", instId],
    queryFn: () => (instId ? systemApi.listNumberGenerators(instId) : Promise.resolve([])),
    enabled: Boolean(instId),
  });

  const {
    register,
    handleSubmit,
    watch,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<NumGenFormValues>({
    resolver: zodResolver(numGenSchema),
    defaultValues: {
      entity_type: "student_registration",
      name: "Student Registration Number",
      prefix: "MEI",
      suffix: "",
      format_template: "{PREFIX}-{BRANCH}-{YEAR}-{NUMBER}",
      separator: "-",
      padding_length: 6,
      reset_rule: "YEARLY",
    },
  });

  const watchedValues = watch();

  useEffect(() => {
    // Dynamic real-time preview computation
    systemApi
      .previewNumber({
        prefix: watchedValues.prefix || "MEI",
        suffix: watchedValues.suffix || undefined,
        format_template: watchedValues.format_template || "{PREFIX}-{YEAR}-{NUMBER}",
        separator: watchedValues.separator || "-",
        padding_length: Number(watchedValues.padding_length) || 6,
        sample_number: 124,
        branch_code: "BPL",
        year: 2027,
      })
      .then((res) => setLivePreview(res.preview))
      .catch(() => setLivePreview("Invalid Format Template"));
  }, [
    watchedValues.prefix,
    watchedValues.suffix,
    watchedValues.format_template,
    watchedValues.separator,
    watchedValues.padding_length,
  ]);

  const createMutation = useMutation({
    mutationFn: (values: NumGenFormValues) => {
      if (!instId) throw new Error("Institute required");
      return systemApi.createNumberGenerator({ ...values, institute_id: instId });
    },
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["systemNumberGenerators"] });
      reset();
    },
  });

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
      {/* Configuration Form */}
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900 lg:col-span-1">
        <div className="flex items-center gap-2">
          <Binary className="h-5 w-5 text-brand-600 dark:text-brand-400" />
          <h2 className="text-sm font-bold text-slate-900 dark:text-white">Configure Number Generator</h2>
        </div>

        {/* Live Preview Banner */}
        <div className="mt-4 rounded-xl border border-brand-500/30 bg-brand-50/60 p-4 dark:border-brand-500/40 dark:bg-brand-950/40">
          <div className="flex items-center gap-2 text-xs font-semibold text-brand-700 dark:text-brand-300">
            <Sparkles className="h-4 w-4" />
            <span>Real-Time Live Number Preview</span>
          </div>
          <p className="mt-2 font-mono text-base font-bold tracking-wide text-brand-900 dark:text-brand-100 select-all">
            {livePreview || "Calculating..."}
          </p>
        </div>

        <form onSubmit={handleSubmit((d) => createMutation.mutate(d))} className="mt-4 space-y-3">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Entity Type</label>
            <select
              {...register("entity_type")}
              className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white"
            >
              <option value="student_registration">Student Registration Number</option>
              <option value="admission_number">Admission Number</option>
              <option value="enrollment_number">Enrollment Number</option>
              <option value="roll_number">Student Roll Number</option>
              <option value="employee_id">Employee / Faculty ID</option>
              <option value="certificate_number">Certificate Number</option>
              <option value="receipt_number">Fee Receipt Number</option>
              <option value="invoice_number">Invoice / Bill Number</option>
              <option value="library_card">Library Card Barcode</option>
              <option value="visitor_pass">Visitor Pass ID</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Display Label</label>
            <input type="text" {...register("name")} placeholder="Student Registration Number" className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
          </div>

          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Prefix</label>
              <input type="text" {...register("prefix")} placeholder="MEI" className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Suffix</label>
              <input type="text" {...register("suffix")} placeholder="REG" className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Format Template</label>
            <input
              type="text"
              {...register("format_template")}
              placeholder="{PREFIX}-{BRANCH}-{YEAR}-{NUMBER}"
              className="mt-1 block w-full font-mono rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white"
            />
            <p className="mt-1 text-[10px] text-slate-500">
              Tokens: {"{PREFIX}"}, {"{BRANCH}"}, {"{COURSE}"}, {"{DEPT}"}, {"{YEAR}"}, {"{MONTH}"}, {"{NUMBER}"}, {"{SUFFIX}"}
            </p>
          </div>

          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Separator</label>
              <input type="text" {...register("separator")} placeholder="-" className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Padding Length</label>
              <input type="number" {...register("padding_length")} min={3} max={10} className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Reset Rule</label>
            <select
              {...register("reset_rule")}
              className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white"
            >
              <option value="YEARLY">Every Calendar Year (Jan 1)</option>
              <option value="ACADEMIC_YEAR">Every Academic Session (June)</option>
              <option value="FINANCIAL_YEAR">Every Financial Year (April 1)</option>
              <option value="MONTHLY">Every Month</option>
              <option value="BRANCH">Per Branch Partition</option>
              <option value="NEVER">Never Reset (Continuous)</option>
            </select>
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full rounded-lg bg-brand-600 py-2.5 text-xs font-semibold text-white hover:bg-brand-500 disabled:opacity-50"
          >
            {isSubmitting ? "Saving Format..." : "Save Number Format"}
          </button>
        </form>
      </div>

      {/* Existing Generators */}
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900 lg:col-span-2">
        <h2 className="text-sm font-bold text-slate-900 dark:text-white">
          Active Universal Numbering Generators ({generators.length})
        </h2>
        <div className="mt-4 space-y-3">
          {isLoading ? (
            <p className="text-xs text-slate-500">Loading number formats...</p>
          ) : (
            generators.map((g) => (
              <div key={g.id} className="rounded-xl border border-slate-200 p-4 dark:border-slate-800 dark:bg-slate-950/40">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-bold text-slate-900 dark:text-white">{g.name}</span>
                  <span className="rounded-sm bg-purple-50 px-2 py-0.5 font-mono text-[11px] font-bold text-purple-700 dark:bg-purple-950 dark:text-purple-300">
                    Reset: {g.reset_rule}
                  </span>
                </div>
                <div className="mt-2 flex items-center gap-2">
                  <span className="text-xs text-slate-500">Template:</span>
                  <code className="rounded-sm bg-slate-100 px-2 py-0.5 font-mono text-xs text-slate-800 dark:bg-slate-800 dark:text-slate-200">
                    {g.format_template}
                  </code>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
