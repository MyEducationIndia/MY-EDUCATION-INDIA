import React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { GitBranch, Plus, Clock, MapPin, Phone, Mail } from "lucide-react";
import { systemApi } from "../api/systemApi";

const branchSchema = z.object({
  code: z.string().min(2).max(32).regex(/^[A-Z0-9_-]+$/, "Use uppercase, digits, and hyphen/underscore"),
  name: z.string().min(2).max(255),
  address_line1: z.string().min(3).max(255),
  city: z.string().min(2).max(100),
  state: z.string().min(2).max(100),
  postal_code: z.string().min(4).max(20),
  phone: z.string().min(8).max(32),
  email: z.string().email(),
  principal_name: z.string().optional(),
  is_main_branch: z.boolean().default(false),
});

type BranchFormValues = z.infer<typeof branchSchema>;

export const BranchManagementPage: React.FC = () => {
  const queryClient = useQueryClient();

  const { data: institutes = [] } = useQuery({
    queryKey: ["systemInstitutes"],
    queryFn: systemApi.listInstitutes,
  });
  const currentInstitute = institutes[0];

  const { data: branches = [], isLoading } = useQuery({
    queryKey: ["systemBranches", currentInstitute?.id],
    queryFn: () => (currentInstitute?.id ? systemApi.listBranches(currentInstitute.id) : Promise.resolve([])),
    enabled: Boolean(currentInstitute?.id),
  });

  const createMutation = useMutation({
    mutationFn: (values: BranchFormValues) => {
      if (!currentInstitute) throw new Error("Institute required");
      return systemApi.createBranch({ ...values, institute_id: currentInstitute.id });
    },
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["systemBranches"] });
      reset();
    },
  });

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<BranchFormValues>({
    resolver: zodResolver(branchSchema),
    defaultValues: {
      code: "",
      name: "",
      address_line1: "",
      city: "",
      state: "",
      postal_code: "",
      phone: "",
      email: "",
      is_main_branch: false,
    },
  });

  const onSubmit = async (values: BranchFormValues) => {
    await createMutation.mutateAsync(values);
  };

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
      {/* Create Branch Card */}
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900 lg:col-span-1">
        <div className="flex items-center gap-2">
          <Plus className="h-5 w-5 text-brand-600 dark:text-brand-400" />
          <h2 className="text-sm font-bold text-slate-900 dark:text-white">
            Create Regional Branch
          </h2>
        </div>
        <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
          Provision an independent campus or branch under {currentInstitute?.name || "your Institute"}.
        </p>

        <form onSubmit={handleSubmit(onSubmit)} className="mt-4 space-y-3">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">
              Branch Code (e.g. BPL, IND, DEL)
            </label>
            <input
              type="text"
              {...register("code")}
              placeholder="BPL-CAMPUS"
              className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white"
            />
            {errors.code && <p className="mt-1 text-xs text-rose-600">{errors.code.message}</p>}
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">
              Branch Name
            </label>
            <input
              type="text"
              {...register("name")}
              placeholder="Bhopal City Main Campus"
              className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white"
            />
            {errors.name && <p className="mt-1 text-xs text-rose-600">{errors.name.message}</p>}
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">
              Address
            </label>
            <input
              type="text"
              {...register("address_line1")}
              placeholder="Plot 42, Knowledge Park"
              className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white"
            />
          </div>

          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">City</label>
              <input type="text" {...register("city")} placeholder="Bhopal" className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">State</label>
              <input type="text" {...register("state")} placeholder="Madhya Pradesh" className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">PIN Code</label>
              <input type="text" {...register("postal_code")} placeholder="462001" className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Phone</label>
              <input type="text" {...register("phone")} placeholder="+91 755 2400000" className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Branch Email</label>
            <input type="email" {...register("email")} placeholder="bhopal@myeducationindia.edu.in" className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Principal / Director</label>
            <input type="text" {...register("principal_name")} placeholder="Dr. S. K. Verma" className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
          </div>

          <label className="flex items-center gap-2 pt-1 text-xs text-slate-700 dark:text-slate-300 cursor-pointer">
            <input type="checkbox" {...register("is_main_branch")} className="rounded-sm border-slate-300 text-brand-600" />
            <span>Mark as Main Campus / Headquarter</span>
          </label>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full rounded-lg bg-brand-600 py-2.5 text-xs font-semibold text-white hover:bg-brand-500 disabled:opacity-50"
          >
            {isSubmitting ? "Provisioning..." : "Provision Branch"}
          </button>
        </form>
      </div>

      {/* Branch List */}
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900 lg:col-span-2">
        <h2 className="text-sm font-bold text-slate-900 dark:text-white">
          Active Branches ({branches.length})
        </h2>
        <div className="mt-4 space-y-3">
          {isLoading ? (
            <p className="text-xs text-slate-500">Loading branch network...</p>
          ) : branches.length === 0 ? (
            <p className="text-xs text-slate-500">No branches added yet.</p>
          ) : (
            branches.map((b) => (
              <div key={b.id} className="rounded-xl border border-slate-200 p-4 dark:border-slate-800 dark:bg-slate-950/40">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-bold text-slate-900 dark:text-white">{b.name}</span>
                    <span className="rounded-sm bg-brand-50 px-2 py-0.5 font-mono text-[11px] font-bold text-brand-700 dark:bg-brand-950 dark:text-brand-300">
                      {b.code}
                    </span>
                    {b.is_main_branch && (
                      <span className="rounded-sm bg-emerald-50 px-2 py-0.5 text-[10px] font-bold text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300">
                        Main Campus
                      </span>
                    )}
                  </div>
                </div>

                <div className="mt-2 grid grid-cols-1 gap-2 text-xs text-slate-600 dark:text-slate-400 sm:grid-cols-2">
                  <div className="flex items-center gap-1.5">
                    <MapPin className="h-3.5 w-3.5 text-slate-400" />
                    <span>{b.address_line1}, {b.city}, {b.state}</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <Phone className="h-3.5 w-3.5 text-slate-400" />
                    <span>{b.phone}</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <Mail className="h-3.5 w-3.5 text-slate-400" />
                    <span>{b.email}</span>
                  </div>
                  {b.principal_name && (
                    <div className="flex items-center gap-1.5">
                      <Clock className="h-3.5 w-3.5 text-slate-400" />
                      <span>Principal: {b.principal_name}</span>
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
