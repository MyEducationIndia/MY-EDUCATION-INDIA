import React from "react";

export const PublicTestimonialsPage: React.FC = () => {
  return (
    <div className="mx-auto max-w-6xl p-6 space-y-4">
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs dark:border-slate-800 dark:bg-slate-900">
        <span className="inline-block rounded-full bg-indigo-100 px-3 py-1 text-xs font-semibold text-indigo-800 dark:bg-indigo-900/40 dark:text-indigo-300">
          MY EDUCATION INDIA
        </span>
        <h1 className="mt-3 text-2xl font-bold text-slate-900 dark:text-white">Testimonials & Reviews</h1>
        <p className="mt-1 text-sm text-slate-600 dark:text-slate-300">Feedback from students, alumni, and parents.</p>
      </div>
    </div>
  );
};

export default PublicTestimonialsPage;
