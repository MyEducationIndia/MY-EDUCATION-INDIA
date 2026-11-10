import React from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useQuery } from "@tanstack/react-query";
import { ShieldCheck, UserCheck, GraduationCap } from "lucide-react";
import { admissionService } from "../services/admissionService";
import { systemApi } from "@/modules/system/api/systemApi";

const admissionSchema = z.object({
  first_name: z.string().min(2),
  last_name: z.string().min(2),
  email: z.string().email(),
  phone_number: z.string().min(8),
  date_of_birth: z.string(),
  gender: z.string(),
  course_name: z.string(),
  batch_preference: z.string(),
  guardian_name: z.string().min(2),
  guardian_phone: z.string().min(8),
  address_line1: z.string().min(3),
  city: z.string().min(2),
  state: z.string().min(2),
  postal_code: z.string().min(4),
});

type AdmissionFormValues = z.infer<typeof admissionSchema>;

export const OnlineAdmissionFormPage: React.FC = () => {
  const navigate = useNavigate();

  const { data: institutes = [] } = useQuery({ queryKey: ["systemInstitutes"], queryFn: systemApi.listInstitutes });
  const instId = institutes[0]?.id;

  const { data: branches = [] } = useQuery({
    queryKey: ["systemBranches", instId],
    queryFn: () => (instId ? systemApi.listBranches(instId) : Promise.resolve([])),
    enabled: Boolean(instId),
  });
  const branchId = branches[0]?.id;

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<AdmissionFormValues>({
    resolver: zodResolver(admissionSchema),
    defaultValues: {
      first_name: "",
      last_name: "",
      email: "",
      phone_number: "",
      date_of_birth: "2006-05-12",
      gender: "MALE",
      course_name: "B.Tech Computer Science & AI",
      batch_preference: "2026-Batch-A",
      guardian_name: "",
      guardian_phone: "",
      address_line1: "",
      city: "Bhopal",
      state: "Madhya Pradesh",
      postal_code: "462011",
    },
  });

  const onSubmit = async (values: AdmissionFormValues) => {
    if (!instId || !branchId) {
      alert("Institute & Branch configuration required.");
      return;
    }
    const app = await admissionService.submitApplication({
      ...values,
      institute_id: instId,
      branch_id: branchId,
      academic_year_code: "2026-2027",
      application_mode: "ONLINE",
    });
    alert(`Application Submitted Successfully! Application No: ${app.application_number}`);
    navigate("/admin/admissions/applications");
  };

  return (
    <div className="mx-auto max-w-3xl rounded-2xl border border-slate-200 bg-white p-6 shadow-md dark:border-slate-800 dark:bg-slate-900 sm:p-8">
      <div className="flex items-center gap-3 border-b border-slate-200 pb-4 dark:border-slate-800">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-600 text-white">
          <GraduationCap className="h-6 w-6" />
        </div>
        <div>
          <h1 className="text-base font-bold text-slate-900 dark:text-white">Online Admission Application Form</h1>
          <p className="text-xs text-slate-500">Session 2026-2027 • Unified Academic Admission Intake</p>
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="mt-6 space-y-4">
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">First Name</label>
            <input type="text" {...register("first_name")} className="mt-1 block w-full rounded-xl border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
            {errors.first_name && <p className="text-[10px] text-rose-600">{errors.first_name.message}</p>}
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Last Name</label>
            <input type="text" {...register("last_name")} className="mt-1 block w-full rounded-xl border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
            {errors.last_name && <p className="text-[10px] text-rose-600">{errors.last_name.message}</p>}
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Email Address</label>
            <input type="email" {...register("email")} className="mt-1 block w-full rounded-xl border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Phone Number</label>
            <input type="tel" {...register("phone_number")} className="mt-1 block w-full rounded-xl border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Date of Birth</label>
            <input type="date" {...register("date_of_birth")} className="mt-1 block w-full rounded-xl border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Gender</label>
            <select {...register("gender")} className="mt-1 block w-full rounded-xl border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white">
              <option value="MALE">Male</option>
              <option value="FEMALE">Female</option>
              <option value="OTHER">Other</option>
            </select>
          </div>
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Academic Program</label>
          <select {...register("course_name")} className="mt-1 block w-full rounded-xl border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white">
            <option value="B.Tech Computer Science & AI">B.Tech Computer Science & AI (4 Years)</option>
            <option value="MBA in Enterprise Analytics">MBA in Enterprise Analytics (2 Years)</option>
            <option value="B.Pharmacy & Clinical Research">B.Pharmacy & Clinical Research (4 Years)</option>
          </select>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Parent / Guardian Name</label>
            <input type="text" {...register("guardian_name")} className="mt-1 block w-full rounded-xl border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Guardian Phone</label>
            <input type="tel" {...register("guardian_phone")} className="mt-1 block w-full rounded-xl border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
          </div>
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Address Line</label>
          <input type="text" {...register("address_line1")} className="mt-1 block w-full rounded-xl border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
        </div>

        <div className="grid grid-cols-3 gap-3">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">City</label>
            <input type="text" {...register("city")} className="mt-1 block w-full rounded-xl border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">State</label>
            <input type="text" {...register("state")} className="mt-1 block w-full rounded-xl border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">PIN Code</label>
            <input type="text" {...register("postal_code")} className="mt-1 block w-full rounded-xl border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
          </div>
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full rounded-xl bg-brand-600 py-3 text-xs font-bold text-white shadow-lg hover:bg-brand-500 disabled:opacity-50"
        >
          {isSubmitting ? "Submitting Application..." : "Submit Admission Application"}
        </button>
      </form>
    </div>
  );
};
