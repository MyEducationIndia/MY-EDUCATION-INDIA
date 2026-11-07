import React from "react";
import { Link } from "react-router-dom";
import {
  ShieldCheck,
  BookOpen,
  Award,
  GraduationCap,
  ArrowRight,
  Phone,
  MapPin,
} from "lucide-react";

export const PublicHomePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans">
      <div className="bg-slate-900 px-4 py-2 text-xs text-slate-300">
        <div className="mx-auto flex max-w-7xl items-center justify-between">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1.5">
              <MapPin className="h-3.5 w-3.5 text-brand-400" />
              Indore, Madhya Pradesh, India
            </span>
            <span className="hidden sm:flex items-center gap-1.5">
              <Phone className="h-3.5 w-3.5 text-brand-400" />
              +91 731 245 6789
            </span>
          </div>
          <div className="flex items-center gap-3">
            <span className="hidden md:inline text-slate-400">Admissions Open 2026-27</span>
            <Link
              to="/login"
              className="inline-flex items-center gap-1 rounded bg-brand-600 px-2.5 py-1 text-xs font-semibold text-white transition hover:bg-brand-500"
            >
              <span>Portal Login</span>
              <ArrowRight className="h-3 w-3" />
            </Link>
          </div>
        </div>
      </div>

      <header className="sticky top-0 z-40 border-b border-slate-200 bg-white/95 backdrop-blur-md">
        <div className="mx-auto flex h-20 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <Link to="/" className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-brand-600 text-white shadow-md shadow-brand-500/20">
              <ShieldCheck className="h-7 w-7" />
            </div>
            <div>
              <p className="text-lg font-black tracking-tight text-slate-900">MY EDUCATION INDIA</p>
              <p className="text-[11px] font-semibold tracking-wider text-brand-700 uppercase">National Flagship Institution</p>
            </div>
          </Link>

          <nav className="hidden md:flex items-center gap-8 text-sm font-semibold text-slate-700">
            <a href="#about" className="transition hover:text-brand-600">About</a>
            <a href="#programs" className="transition hover:text-brand-600">Academics</a>
            <a href="#contact" className="transition hover:text-brand-600">Contact</a>
          </nav>

          <div className="flex items-center gap-3">
            <Link
              to="/login"
              className="inline-flex items-center gap-2 rounded-xl border border-slate-300 bg-white px-4 py-2 text-xs font-bold text-slate-800 shadow-2xs transition hover:border-brand-600 hover:text-brand-600"
            >
              <span>Sign In</span>
            </Link>
            <Link
              to="/login"
              className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2 text-xs font-bold text-white shadow-xs transition hover:bg-brand-700"
            >
              <span>ERP Command Center</span>
            </Link>
          </div>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-brand-50/50 via-white to-slate-50 py-20 sm:py-28">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-3xl text-center">
            <div className="inline-flex items-center gap-2 rounded-full border border-brand-200 bg-white px-3.5 py-1 text-xs font-semibold text-brand-700 shadow-2xs mb-6">
              <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
              Autonomous Higher Education & Research Campus
            </div>
            <h1 className="text-4xl font-extrabold tracking-tight text-slate-900 sm:text-5xl lg:text-6xl">
              Empowering Next-Generation Scholars Across India
            </h1>
            <p className="mt-6 text-base leading-relaxed text-slate-600 sm:text-lg">
              MY EDUCATION INDIA is a premier institution offering accredited degree programs, 
              computer-based national examinations, and digital tamper-proof credentials powered by enterprise technology.
            </p>
            <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
              <Link
                to="/login"
                className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-6 py-3 text-sm font-bold text-white shadow-md shadow-brand-500/25 transition hover:bg-brand-700"
              >
                <span>Access Student & Staff Portal</span>
                <ArrowRight className="h-4 w-4" />
              </Link>
              <a
                href="#about"
                className="inline-flex items-center gap-2 rounded-xl border border-slate-300 bg-white px-6 py-3 text-sm font-bold text-slate-700 transition hover:bg-slate-50"
              >
                <span>Campus Overview</span>
              </a>
            </div>
          </div>
        </div>
      </section>

      <section className="border-y border-slate-200 bg-white py-10">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 gap-6 md:grid-cols-4 text-center">
            <div>
              <p className="text-3xl font-extrabold text-brand-600">37+</p>
              <p className="mt-1 text-xs font-semibold uppercase tracking-wider text-slate-500">Integrated Subsystems</p>
            </div>
            <div>
              <p className="text-3xl font-extrabold text-slate-900">100%</p>
              <p className="mt-1 text-xs font-semibold uppercase tracking-wider text-slate-500">Digital Credentials</p>
            </div>
            <div>
              <p className="text-3xl font-extrabold text-slate-900">MEI-HQ</p>
              <p className="mt-1 text-xs font-semibold uppercase tracking-wider text-slate-500">Flagship Campus Indore</p>
            </div>
            <div>
              <p className="text-3xl font-extrabold text-emerald-600">A+</p>
              <p className="mt-1 text-xs font-semibold uppercase tracking-wider text-slate-500">Institutional Governance</p>
            </div>
          </div>
        </div>
      </section>

      <section id="programs" className="py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-14">
            <h2 className="text-xs font-bold uppercase tracking-wider text-brand-600">Comprehensive Academic Model</h2>
            <p className="mt-2 text-3xl font-extrabold text-slate-900">Institutional Excellence & Programs</p>
          </div>

          <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
            <div className="rounded-2xl border border-slate-200 bg-white p-7 shadow-xs">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-50 text-brand-600 mb-5">
                <BookOpen className="h-6 w-6" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">Academics & Curricula</h3>
              <p className="mt-2 text-xs leading-relaxed text-slate-600">
                Semester-wise credit systems, interactive timetables, and lecture delivery tracked dynamically in Neon PostgreSQL.
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-7 shadow-xs">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600 mb-5">
                <Award className="h-6 w-6" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">CBT & Examinations</h3>
              <p className="mt-2 text-xs leading-relaxed text-slate-600">
                Online Computer-Based Testing engine with proctoring safeguards, anti-cheat detection, and instant SGPA/CGPA generation.
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-7 shadow-xs">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-purple-50 text-purple-600 mb-5">
                <GraduationCap className="h-6 w-6" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">Verified Credentials</h3>
              <p className="mt-2 text-xs leading-relaxed text-slate-600">
                Cryptographically signed digital marksheets and certificates with instantaneous public QR code verification.
              </p>
            </div>
          </div>
        </div>
      </section>

      <footer id="contact" className="border-t border-slate-200 bg-white pt-14 pb-8 text-xs text-slate-500">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 gap-8 md:grid-cols-4 pb-10 border-b border-slate-200">
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-slate-900 font-bold text-base">
                <ShieldCheck className="h-5 w-5 text-brand-600" />
                <span>MY EDUCATION INDIA</span>
              </div>
              <p className="text-xs text-slate-500 leading-relaxed">
                National Flagship Institution for Higher Education & Research.
                Campus in Indore, Madhya Pradesh.
              </p>
            </div>

            <div>
              <h4 className="font-bold text-slate-900 mb-3 uppercase tracking-wider text-[11px]">Quick Links</h4>
              <ul className="space-y-2">
                <li><Link to="/login" className="hover:text-brand-600">Staff & Faculty Portal</Link></li>
                <li><Link to="/login" className="hover:text-brand-600">Student Portal</Link></li>
                <li><Link to="/login" className="hover:text-brand-600">Admin Control Center</Link></li>
              </ul>
            </div>

            <div>
              <h4 className="font-bold text-slate-900 mb-3 uppercase tracking-wider text-[11px]">Campus Details</h4>
              <p>Campus Square, Institutional Sector</p>
              <p className="mt-1">Indore, Madhya Pradesh — 452001</p>
              <p className="mt-1 font-semibold text-slate-700">Affiliation Code: MEI-HQ</p>
            </div>

            <div>
              <h4 className="font-bold text-slate-900 mb-3 uppercase tracking-wider text-[11px]">Administration</h4>
              <Link
                to="/login"
                className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-slate-900 px-4 py-2.5 font-bold text-white transition hover:bg-brand-600"
              >
                <span>Institutional Login</span>
                <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </div>

          <div className="pt-6 flex flex-col sm:flex-row items-center justify-between gap-4">
            <p>© {new Date().getFullYear()} MY EDUCATION INDIA. All rights reserved.</p>
            <p className="text-slate-400">Enterprise Modular Monolith ERP V2 • Production Release</p>
          </div>
        </div>
      </footer>
    </div>
  );
};
