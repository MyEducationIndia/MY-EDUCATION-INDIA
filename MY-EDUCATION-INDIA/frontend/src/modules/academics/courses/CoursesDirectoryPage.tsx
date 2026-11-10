import React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { BookOpen, Plus } from "lucide-react";
import { academicService } from "../services/academicService";
import { systemApi } from "@/modules/system/api/systemApi";

const courseSchema = z.object({
  code: z.string().min(2).max(32).regex(/^[A-Z0-9_-]+$/),
  name: z.string().min(2).max(150),
  academic_pattern: z.string(),
  total_semesters_or_years: z.coerce.number().min(1).max(12),
  max_intake_capacity: z.coerce.number().min(10).max(500),
  department_id: z.string().uuid(),
});

type CourseFormValues = z.infer<typeof courseSchema>;

export const CoursesDirectoryPage: React.FC = () => {
  const queryClient = useQueryClient();

  const { data: institutes = [] } = useQuery({ queryKey: ["systemInstitutes"], queryFn: systemApi.listInstitutes });
  const instId = institutes[0]?.id;

  const { data: depts = [] } = useQuery({ queryKey: ["academicDepts"], queryFn: academicService.listDepartments });
  const { data: programs = [] } = useQuery({ queryKey: ["academicPrograms"], queryFn: academicService.listPrograms });
  const { data: courses = [], isLoading } = useQuery({ queryKey: ["academicCourses"], queryFn: academicService.listCourses });

  const createMutation = useMutation({
    mutationFn: (values: CourseFormValues) => {
      if (!instId || programs.length === 0) throw new Error("Institute and Program required");
      return academicService.createCourse({
        ...values,
        institute_id: instId,
        program_id: programs[0].id,
      });
    },
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["academicCourses"] });
      reset();
    },
  });

  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm<CourseFormValues>({
    resolver: zodResolver(courseSchema),
    defaultValues: {
      code: "BTECH_CSE",
      name: "B.Tech Computer Science & AI",
      academic_pattern: "SEMESTER",
      total_semesters_or_years: 8,
      max_intake_capacity: 120,
    },
  });

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900 lg:col-span-1">
        <h2 className="text-sm font-bold text-slate-900 dark:text-white">Create Academic Course</h2>
        <form onSubmit={handleSubmit((d) => createMutation.mutate(d))} className="mt-4 space-y-3">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Course Code</label>
            <input type="text" {...register("code")} placeholder="BTECH_CSE" className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
            {errors.code && <p className="mt-1 text-xs text-rose-600">{errors.code.message}</p>}
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Course Name</label>
            <input type="text" {...register("name")} placeholder="B.Tech Computer Science" className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Parent Department</label>
            <select {...register("department_id")} className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white">
              {depts.map((d) => (
                <option key={d.id} value={d.id}>{d.name} ({d.code})</option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Pattern</label>
              <select {...register("academic_pattern")} className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white">
                <option value="SEMESTER">Semester</option>
                <option value="YEARLY">Yearly</option>
                <option value="TRIMESTER">Trimester</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Total Terms</label>
              <input type="number" {...register("total_semesters_or_years")} min={1} max={12} className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-white" />
            </div>
          </div>

          <button type="submit" disabled={isSubmitting} className="w-full rounded-lg bg-brand-600 py-2.5 text-xs font-semibold text-white hover:bg-brand-500 disabled:opacity-50">
            {isSubmitting ? "Saving..." : "Save Course"}
          </button>
        </form>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900 lg:col-span-2">
        <h2 className="text-sm font-bold text-slate-900 dark:text-white">Configured Courses ({courses.length})</h2>
        <div className="mt-4 space-y-3">
          {isLoading ? (
            <p className="text-xs text-slate-500">Loading courses...</p>
          ) : (
            courses.map((c) => (
              <div key={c.id} className="flex items-center justify-between rounded-xl border border-slate-200 p-4 dark:border-slate-800 dark:bg-slate-950/40">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-bold text-slate-900 dark:text-white">{c.name}</span>
                    <span className="rounded-sm bg-brand-50 px-2 py-0.5 font-mono text-[11px] font-bold text-brand-700 dark:bg-brand-950 dark:text-brand-300">{c.code}</span>
                  </div>
                  <p className="mt-1 text-xs text-slate-500">
                    Pattern: {c.academic_pattern} • Terms: {c.total_semesters_or_years} • Intake: {c.max_intake_capacity}
                  </p>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
