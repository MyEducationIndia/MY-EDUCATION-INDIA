import React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { roleService } from "@/services/roleService";

const createRoleSchema = z.object({
  code: z
    .string()
    .min(2)
    .max(64)
    .regex(/^[A-Z0-9_]+$/, "Use uppercase letters, digits, and underscores only"),
  name: z.string().min(2).max(120),
  description: z.string().max(500).optional(),
  portal_subdomain: z.string().min(2).max(32),
});

type CreateRoleFormValues = z.infer<typeof createRoleSchema>;

export const RolesPermissionsPage: React.FC = () => {
  const queryClient = useQueryClient();

  const { data: roles = [], isLoading } = useQuery({
    queryKey: ["roles"],
    queryFn: () => roleService.listRoles(),
  });

  const createMutation = useMutation({
    mutationFn: roleService.createRole,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["roles"] });
      reset();
    },
  });

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<CreateRoleFormValues>({
    resolver: zodResolver(createRoleSchema),
    defaultValues: {
      code: "",
      name: "",
      description: "",
      portal_subdomain: "admin",
    },
  });

  const onSubmit = async (values: CreateRoleFormValues): Promise<void> => {
    await createMutation.mutateAsync({
      ...values,
      permission_codes: [],
    });
  };

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs lg:col-span-1">
        <h2 className="text-base font-bold text-slate-900">
          Create RBAC Role
        </h2>
        <p className="mt-1 text-xs text-slate-500">
          Define a new institutional role scoped to a target portal subdomain.
        </p>

        <form onSubmit={handleSubmit(onSubmit)} className="mt-4 space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700">
              Role Code
            </label>
            <input
              type="text"
              placeholder="EXAM_CONTROLLER"
              {...register("code")}
              className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand-600 focus:outline-hidden"
            />
            {errors.code && (
              <p className="mt-1 text-xs text-rose-600">{errors.code.message}</p>
            )}
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700">
              Display Name
            </label>
            <input
              type="text"
              placeholder="Chief Examination Controller"
              {...register("name")}
              className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand-600 focus:outline-hidden"
            />
            {errors.name && (
              <p className="mt-1 text-xs text-rose-600">{errors.name.message}</p>
            )}
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700">
              Target Portal Subdomain
            </label>
            <select
              {...register("portal_subdomain")}
              className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand-600 focus:outline-hidden"
            >
              <option value="admin">admin.myeducationindia.edu.in</option>
              <option value="student">student.myeducationindia.edu.in</option>
              <option value="teacher">teacher.myeducationindia.edu.in</option>
              <option value="parent">parent.myeducationindia.edu.in</option>
              <option value="exam">exam.myeducationindia.edu.in</option>
              <option value="cbt">cbt.myeducationindia.edu.in</option>
              <option value="fees">fees.myeducationindia.edu.in</option>
              <option value="library">library.myeducationindia.edu.in</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700">
              Description
            </label>
            <textarea
              rows={3}
              {...register("description")}
              className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand-600 focus:outline-hidden"
            />
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full rounded-lg bg-brand-600 px-4 py-2.5 text-xs font-semibold text-white hover:bg-brand-500 disabled:opacity-50"
          >
            {isSubmitting ? "Saving Role..." : "Create Role"}
          </button>
        </form>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs lg:col-span-2">
        <h2 className="text-base font-bold text-slate-900">
          Configured Roles ({roles.length})
        </h2>
        {isLoading ? (
          <p className="mt-4 text-sm text-slate-500">Loading roles...</p>
        ) : (
          <div className="mt-4 space-y-3">
            {roles.map((role) => (
              <div
                key={role.id}
                className="rounded-xl border border-slate-200 p-4"
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div>
                    <span className="text-sm font-bold text-slate-900">
                      {role.name}
                    </span>
                    <span className="ml-2 rounded-sm bg-slate-100 px-2 py-0.5 font-mono text-xs text-slate-700">
                      {role.code}
                    </span>
                  </div>
                  <span className="rounded-md bg-brand-50 px-2.5 py-0.5 text-xs font-semibold text-brand-700">
                    Subdomain: {role.portal_subdomain}
                  </span>
                </div>
                {role.description && (
                  <p className="mt-1.5 text-xs text-slate-600">
                    {role.description}
                  </p>
                )}
                <div className="mt-3 flex flex-wrap gap-1.5">
                  {role.permissions.map((perm) => (
                    <span
                      key={perm.id}
                      className="rounded-sm bg-emerald-50 px-2 py-0.5 font-mono text-[11px] text-emerald-700"
                    >
                      {perm.code}
                    </span>
                  ))}
                  {role.permissions.length === 0 && (
                    <span className="text-xs italic text-slate-400">
                      No granular permissions attached yet
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
