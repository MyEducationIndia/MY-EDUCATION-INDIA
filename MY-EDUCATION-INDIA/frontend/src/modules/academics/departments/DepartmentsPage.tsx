import React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Building, Plus } from "lucide-react";
import { academicService } from "../services/academicService";
import { systemApi } from "@/modules/system/api/systemApi";

const deptSchema = z.object({
  code: z.string().min(2).max(32).regex(/^[A-Z0-9_-]+$/),
  name: z.string().min(2).max(150),
  hod_name: z.string().optional(),
});

type DeptFormValues = z.infer<typeof deptSchema>;

export const DepartmentsPage: React.FC = () => {
  const queryClient = useQueryClient();

  const { data: institutes = [] } = useQuery({ queryKey: ["systemInstitutes"], queryFn: systemApi.listInstitutes });
  const instId = institutes[0]?.id;

  const { data: depts = [], isLoading } = useQuery({
    queryKey: ["academicDepts"],
    queryFn: academicService.listDepartments,
  });

  const createMutation = useMutation({
    mutationFn: (values: DeptFormValues) => {
      if (!instId) throw new Error("Institute required");
      return academicService.createDepartment({ ...values, institute_id: instId });
    },
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["academicDepts"] });
      reset();
    },
  });

  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm<DeptFormValues>({
    resolver: zodResolver(deptSchema),
    defaultValues: { code: "", name: "", hod_name: "" },
  });

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900 lg:col-span-1">
        <h2 className="text-sm font-bold text-slate-900 dark:text-white">Create Department</h2>
        <form onSubmit={handleSubmit((d) => createMutation.mutate(d))} className="mt-4 space-y-3">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Department Code</label>
            <input type="text" {...register("code")} placeholder="CSE" className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
            {errors.code && <p className="mt-1 text-xs text-rose-600">{errors.code.message}</p>}
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Department Name</label>
            <input type="text" {...register("name")} placeholder="Computer Science & Engineering" className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Head of Department (HOD)</label>
            <input type="text" {...register("hod_name")} placeholder="Prof. R. K. Sharma" className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
          </div>

          <button type="submit" disabled={isSubmitting} className="w-full rounded-lg bg-brand-600 py-2.5 text-xs font-semibold text-white hover:bg-brand-500 disabled:opacity-50">
            {isSubmitting ? "Creating..." : "Save Department"}
          </button>
        </form>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900 lg:col-span-2">
        <h2 className="text-sm font-bold text-slate-900 dark:text-white">Active Departments ({depts.length})</h2>
        <div className="mt-4 space-y-3">
          {isLoading ? (
            <p className="text-xs text-slate-500">Loading departments...</p>
          ) : depts.length === 0 ? (
            <p className="text-xs text-slate-500">No departments added yet.</p>
          ) : (
            depts.map((d) => (
              <div key={d.id} className="flex items-center justify-between rounded-xl border border-slate-200 p-4 dark:border-slate-800 dark:bg-slate-950/40">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-bold text-slate-900 dark:text-white">{d.name}</span>
                    <span className="rounded-sm bg-brand-50 px-2 py-0.5 font-mono text-[11px] font-bold text-brand-700 dark:bg-brand-950 dark:text-brand-300">{d.code}</span>
                  </div>
                  {d.hod_name && <p className="mt-1 text-xs text-slate-500">HOD: {d.hod_name}</p>}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
