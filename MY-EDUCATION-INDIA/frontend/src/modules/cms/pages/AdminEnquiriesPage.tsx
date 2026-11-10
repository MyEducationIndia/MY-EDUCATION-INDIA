import React from "react";
import { useQuery } from "@tanstack/react-query";
import { cmsApi } from "../api/cmsApi";

export const AdminEnquiriesPage: React.FC = () => {
  const { data: enquiries = [], isLoading } = useQuery({
    queryKey: ["adminEnquiries"],
    queryFn: cmsApi.listAdminEnquiries,
  });

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900">
      <h1 className="text-base font-bold text-slate-900 dark:text-white">Website Admission & Counseling Enquiries</h1>
      <p className="text-xs text-slate-500">Live leads and student contact submissions from the public portal.</p>

      <div className="mt-5 overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200 text-left text-xs dark:divide-slate-800">
          <thead>
            <tr className="bg-slate-50 uppercase text-slate-500 dark:bg-slate-950">
              <th className="px-4 py-3">Candidate</th>
              <th className="px-4 py-3">Phone</th>
              <th className="px-4 py-3">Email</th>
              <th className="px-4 py-3">Type</th>
              <th className="px-4 py-3">Course</th>
              <th className="px-4 py-3">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
            {isLoading ? (
              <tr><td colSpan={6} className="p-6 text-center text-slate-500">Loading enquiries...</td></tr>
            ) : enquiries.length === 0 ? (
              <tr><td colSpan={6} className="p-6 text-center text-slate-500">No active enquiries yet.</td></tr>
            ) : (
              enquiries.map((e) => (
                <tr key={e.id}>
                  <td className="px-4 py-3 font-bold text-slate-900 dark:text-white">{e.full_name}</td>
                  <td className="px-4 py-3 font-mono">{e.phone_number}</td>
                  <td className="px-4 py-3">{e.email}</td>
                  <td className="px-4 py-3 font-semibold text-brand-600">{e.enquiry_type}</td>
                  <td className="px-4 py-3">{e.course_interested || "General"}</td>
                  <td className="px-4 py-3">
                    <span className="rounded-sm bg-blue-50 px-2 py-0.5 font-bold text-blue-700">{e.status}</span>
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
