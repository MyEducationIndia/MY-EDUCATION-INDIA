import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { userService } from "@/services/userService";
import { StatusBadge } from "@/components/ui/StatusBadge";

export const UsersManagementPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);

  const { data, isLoading } = useQuery({
    queryKey: ["users", search, page],
    queryFn: () =>
      userService.listUsers({
        search: search || undefined,
        page,
        page_size: 20,
      }),
  });

  const statusMutation = useMutation({
    mutationFn: (params: { userId: string; isActive: boolean }) =>
      userService.toggleUserActive(params.userId, params.isActive),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs sm:p-6">
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <h2 className="text-base font-bold text-slate-900">
            Enterprise Identity & User Directory
          </h2>
          <p className="text-xs text-slate-500">
            Search, audit, and control active status across staff, faculty, students, and parents.
          </p>
        </div>
        <input
          type="search"
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
            setPage(1);
          }}
          placeholder="Search name, username, or email..."
          className="w-full rounded-lg border border-slate-300 px-3.5 py-2 text-sm sm:w-72 focus:border-brand-600 focus:outline-hidden"
        />
      </div>

      <div className="mt-5 overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200 text-left text-sm">
          <thead>
            <tr className="bg-slate-50 text-xs font-semibold uppercase tracking-wider text-slate-500">
              <th className="px-4 py-3">Full Name</th>
              <th className="px-4 py-3">Username / Email</th>
              <th className="px-4 py-3">Phone</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {isLoading ? (
              <tr>
                <td colSpan={5} className="px-4 py-6 text-center text-slate-500">
                  Loading users from PostgreSQL...
                </td>
              </tr>
            ) : (
              (data?.items || []).map((u) => (
                <tr key={u.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-semibold text-slate-900">
                    {u.first_name} {u.last_name}
                  </td>
                  <td className="px-4 py-3 text-xs text-slate-600">
                    <div>{u.email}</div>
                    <div className="font-mono text-slate-400">@{u.username}</div>
                  </td>
                  <td className="px-4 py-3 text-xs text-slate-600">
                    {u.phone_number}
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge active={u.is_active} />
                  </td>
                  <td className="px-4 py-3 text-right">
                    <button
                      type="button"
                      disabled={u.is_super_admin || statusMutation.isPending}
                      onClick={() =>
                        statusMutation.mutate({
                          userId: u.id,
                          isActive: !u.is_active,
                        })
                      }
                      className="rounded-lg border border-slate-300 px-3 py-1 text-xs font-semibold text-slate-700 hover:bg-slate-100 disabled:opacity-40"
                    >
                      {u.is_active ? "Suspend" : "Activate"}
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
