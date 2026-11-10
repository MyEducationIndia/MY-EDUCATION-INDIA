import React from "react";
import { Link } from "react-router-dom";
import { ArrowRight, CheckCircle2, Phone, Mail, Award, Users, BookOpen } from "lucide-react";
import { PageSectionItem } from "../types/cms.types";

interface DynamicSectionRendererProps {
  section: PageSectionItem;
  onEnquirySubmit?: (data: any) => Promise<void>;
}

export const DynamicSectionRenderer: React.FC<DynamicSectionRendererProps> = ({
  section,
  onEnquirySubmit,
}) => {
  const p = section.content_payload || {};

  switch (section.block_type) {
    case "HERO":
      return (
        <section className="relative overflow-hidden bg-slate-900 py-20 text-white sm:py-28">
          <div className="absolute inset-0 bg-radial-gradient from-brand-600/20 via-transparent to-transparent opacity-60" />
          <div className="relative mx-auto max-w-5xl px-4 text-center sm:px-6">
            {p.badge_text && (
              <span className="inline-block rounded-full bg-brand-500/20 px-3.5 py-1 text-xs font-bold uppercase tracking-wider text-brand-300 ring-1 ring-inset ring-brand-500/30">
                {p.badge_text}
              </span>
            )}
            <h1 className="mt-4 text-3xl font-extrabold tracking-tight sm:text-5xl lg:text-6xl">
              {p.heading || "Empowering India's Digital Education"}
            </h1>
            <p className="mx-auto mt-4 max-w-2xl text-sm leading-relaxed text-slate-300 sm:text-base">
              {p.subheading || "Explore industry-aligned curricula, world-class labs, and autonomous CBT testing."}
            </p>
            <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
              {p.primary_cta_text && (
                <Link
                  to={p.primary_cta_url || "/admissions"}
                  className="rounded-xl bg-brand-600 px-6 py-3 text-xs font-bold text-white shadow-lg transition hover:bg-brand-500"
                >
                  {p.primary_cta_text}
                </Link>
              )}
              {p.secondary_cta_text && (
                <Link
                  to={p.secondary_cta_url || "/courses"}
                  className="rounded-xl border border-slate-700 bg-slate-800/80 px-6 py-3 text-xs font-bold text-slate-200 transition hover:bg-slate-700"
                >
                  {p.secondary_cta_text}
                </Link>
              )}
            </div>
          </div>
        </section>
      );

    case "COUNTER":
      const counters = p.counters || [
        { label: "Students", value: "15,000+" },
        { label: "Placement", value: "98.4%" },
        { label: "Recruiters", value: "350+" },
      ];
      return (
        <section className="border-y border-slate-200 bg-white py-10 dark:border-slate-800 dark:bg-slate-900">
          <div className="mx-auto max-w-7xl px-4 sm:px-6">
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
              {counters.map((cnt: any, idx: number) => (
                <div key={idx} className="text-center">
                  <p className="text-2xl font-extrabold text-brand-600 dark:text-brand-400 sm:text-4xl">{cnt.value}</p>
                  <p className="mt-1 text-xs font-semibold uppercase tracking-wider text-slate-500">{cnt.label}</p>
                </div>
              ))}
            </div>
          </div>
        </section>
      );

    case "COURSE_LIST":
      return (
        <section className="bg-slate-50 py-16 dark:bg-slate-950">
          <div className="mx-auto max-w-7xl px-4 sm:px-6">
            <div className="text-center">
              <h2 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-3xl">
                {p.title || "Featured Academic Courses"}
              </h2>
              <p className="mt-2 text-xs text-slate-500">{p.subtitle || "Undergraduate, Postgraduate and Autonomous Diploma Disciplines"}</p>
            </div>

            <div className="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {[
                { name: "B.Tech Computer Science & AI", duration: "4 Years", seats: "120 Seats", fee: "₹95,000 / Sem" },
                { name: "MBA in Enterprise Analytics", duration: "2 Years", seats: "60 Seats", fee: "₹1,20,000 / Sem" },
                { name: "B.Pharmacy & Clinical Research", duration: "4 Years", seats: "100 Seats", fee: "₹85,000 / Sem" },
              ].map((crs, i) => (
                <div key={i} className="flex flex-col justify-between rounded-2xl border border-slate-200 bg-white p-6 shadow-xs dark:border-slate-800 dark:bg-slate-900">
                  <div>
                    <span className="rounded-sm bg-brand-50 px-2 py-0.5 text-[10px] font-bold text-brand-700 dark:bg-brand-950 dark:text-brand-300">
                      Accredited
                    </span>
                    <h3 className="mt-2 text-base font-bold text-slate-900 dark:text-white">{crs.name}</h3>
                    <p className="mt-2 text-xs text-slate-500">Duration: {crs.duration} • Intake: {crs.seats}</p>
                  </div>
                  <div className="mt-6 flex items-center justify-between border-t border-slate-100 pt-4 dark:border-slate-800">
                    <span className="text-xs font-extrabold text-slate-900 dark:text-white">{crs.fee}</span>
                    <Link to="/admissions" className="text-xs font-bold text-brand-600 hover:text-brand-500">Apply Now →</Link>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      );

    case "ADMISSION_FORM":
    case "CONTACT_FORM":
      return (
        <section className="bg-white py-16 dark:bg-slate-900">
          <div className="mx-auto max-w-2xl px-4 sm:px-6">
            <div className="rounded-2xl border border-slate-200 bg-slate-50/70 p-6 shadow-md dark:border-slate-800 dark:bg-slate-950 sm:p-8">
              <h2 className="text-center text-lg font-bold text-slate-900 dark:text-white">
                {p.form_title || "Direct Online Admission & Enquiry Form"}
              </h2>
              <p className="mt-1 text-center text-xs text-slate-500">Submit your academic details to receive instant counseling support.</p>
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  alert("Enquiry submitted successfully! Our counseling desk will contact you.");
                }}
                className="mt-6 space-y-3"
              >
                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Full Name</label>
                  <input type="text" required placeholder="Aarav Sharma" className="mt-1 block w-full rounded-xl border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-900 dark:text-white" />
                </div>
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Email</label>
                    <input type="email" required placeholder="aarav@gmail.com" className="mt-1 block w-full rounded-xl border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-900 dark:text-white" />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Phone</label>
                    <input type="tel" required placeholder="+91 9876543210" className="mt-1 block w-full rounded-xl border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-900 dark:text-white" />
                  </div>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Course Interested</label>
                  <input type="text" placeholder="B.Tech Computer Science" className="mt-1 block w-full rounded-xl border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-900 dark:text-white" />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Message / Query</label>
                  <textarea rows={3} placeholder="Please provide fee schedule and hostel details." className="mt-1 block w-full rounded-xl border border-slate-300 px-3 py-2 text-xs dark:border-slate-700 dark:bg-slate-900 dark:text-white" />
                </div>
                <button type="submit" className="w-full rounded-xl bg-brand-600 py-3 text-xs font-bold text-white shadow-md hover:bg-brand-500">
                  Submit Online Application
                </button>
              </form>
            </div>
          </div>
        </section>
      );

    default:
      return null;
  }
};
