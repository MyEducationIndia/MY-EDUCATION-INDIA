import React from "react";
import { Link } from "react-router-dom";
import {
  IndianRupee,
  CreditCard,
  Layers,
  Award,
  RotateCcw,
  TrendingUp,
  FileText,
  AlertCircle,
  PlusCircle,
  Receipt as ReceiptIcon,
} from "lucide-react";
import { FeeAnalyticsSummary } from "../types/fee.types";

export const FeeDashboardPage: React.FC = () => {
  // Real-time state mock/default for immediate reactive render
  const summary: FeeAnalyticsSummary = {
    total_projected_revenue: 12500000.0,
    total_collected_revenue: 9850000.0,
    total_outstanding_dues: 2650000.0,
    collection_percentage: 78.8,
    total_scholarships_granted: 450000.0,
    total_discounts_granted: 180000.0,
    total_refunds_processed: 65000.0,
    today_collection: 185000.0,
    month_collection: 2950000.0,
    payment_mode_distribution: {
      UPI: 5400000.0,
      NET_BANKING: 2450000.0,
      CREDIT_CARD: 1200000.0,
      CASH: 800000.0,
    },
    monthly_trend: [
      { month: "Nov 2026", projected: 3000000, collected: 2950000 },
      { month: "Dec 2026", projected: 2500000, collected: 2100000 },
      { month: "Jan 2027", projected: 2500000, collected: 1900000 },
      { month: "Feb 2027", projected: 2000000, collected: 1600000 },
    ],
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <IndianRupee className="h-7 w-7 text-emerald-600 dark:text-emerald-400" />
            Enterprise Fee & Finance Management
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Real-time financial dashboard, fee structures, collections, installment tracking & reports.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Link
            to="/admin/fees/collect"
            className="flex items-center gap-2 rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold text-white shadow-xs hover:bg-emerald-700 transition"
          >
            <CreditCard className="h-4 w-4" />
            <span>Collect Fee</span>
          </Link>
          <Link
            to="/admin/fees/structures"
            className="flex items-center gap-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2 text-sm font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700 transition"
          >
            <Layers className="h-4 w-4" />
            <span>Fee Structures</span>
          </Link>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {/* Total Projected */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/80 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              Projected Revenue
            </span>
            <div className="rounded-lg bg-blue-50 dark:bg-blue-900/40 p-2 text-blue-600 dark:text-blue-400">
              <TrendingUp className="h-5 w-5" />
            </div>
          </div>
          <p className="mt-3 text-2xl font-bold text-slate-900 dark:text-white">
            ₹{(summary.total_projected_revenue / 100000).toFixed(2)} Lakhs
          </p>
          <p className="mt-1 text-xs text-slate-500">Total assigned institutional fees</p>
        </div>

        {/* Total Collected */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/80 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">
              Total Realized
            </span>
            <div className="rounded-lg bg-emerald-50 dark:bg-emerald-900/40 p-2 text-emerald-600 dark:text-emerald-400">
              <IndianRupee className="h-5 w-5" />
            </div>
          </div>
          <p className="mt-3 text-2xl font-bold text-emerald-600 dark:text-emerald-400">
            ₹{(summary.total_collected_revenue / 100000).toFixed(2)} Lakhs
          </p>
          <div className="mt-1 flex items-center gap-2">
            <span className="text-xs font-semibold text-emerald-600 bg-emerald-100 dark:bg-emerald-950 px-1.5 py-0.5 rounded-sm">
              {summary.collection_percentage}%
            </span>
            <span className="text-xs text-slate-500">realization rate</span>
          </div>
        </div>

        {/* Outstanding Dues */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/80 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-rose-500 dark:text-rose-400">
              Outstanding Dues
            </span>
            <div className="rounded-lg bg-rose-50 dark:bg-rose-900/40 p-2 text-rose-600 dark:text-rose-400">
              <AlertCircle className="h-5 w-5" />
            </div>
          </div>
          <p className="mt-3 text-2xl font-bold text-rose-600 dark:text-rose-400">
            ₹{(summary.total_outstanding_dues / 100000).toFixed(2)} Lakhs
          </p>
          <p className="mt-1 text-xs text-slate-500">Pending student balances</p>
        </div>

        {/* Today's Counter Collection */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/80 p-5 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-purple-600 dark:text-purple-400">
              Today's Collections
            </span>
            <div className="rounded-lg bg-purple-50 dark:bg-purple-900/40 p-2 text-purple-600 dark:text-purple-400">
              <ReceiptIcon className="h-5 w-5" />
            </div>
          </div>
          <p className="mt-3 text-2xl font-bold text-purple-600 dark:text-purple-400">
            ₹{summary.today_collection.toLocaleString("en-IN")}
          </p>
          <p className="mt-1 text-xs text-slate-500">Live cashier collection tally</p>
        </div>
      </div>

      {/* Operational Hub & Fast Navigation */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
        <Link
          to="/admin/fees/structures"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-emerald-500 dark:hover:border-emerald-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-emerald-600 group-hover:text-white transition">
            <Layers className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Fee Structures</span>
        </Link>

        <Link
          to="/admin/fees/categories"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-emerald-500 dark:hover:border-emerald-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-emerald-600 group-hover:text-white transition">
            <PlusCircle className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Categories & Heads</span>
        </Link>

        <Link
          to="/admin/fees/collect"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-emerald-500 dark:hover:border-emerald-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-emerald-600 group-hover:text-white transition">
            <CreditCard className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Fee Collection</span>
        </Link>

        <Link
          to="/admin/fees/scholarships"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-emerald-500 dark:hover:border-emerald-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-emerald-600 group-hover:text-white transition">
            <Award className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Scholarships</span>
        </Link>

        <Link
          to="/admin/fees/refunds"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-emerald-500 dark:hover:border-emerald-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-emerald-600 group-hover:text-white transition">
            <RotateCcw className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Refunds</span>
        </Link>

        <Link
          to="/admin/fees/reports"
          className="flex flex-col items-center justify-center rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60 p-4 text-center hover:border-emerald-500 dark:hover:border-emerald-500 transition group shadow-xs"
        >
          <div className="mb-2 rounded-full bg-slate-100 dark:bg-slate-700/80 p-3 text-slate-700 dark:text-slate-300 group-hover:bg-emerald-600 group-hover:text-white transition">
            <FileText className="h-5 w-5" />
          </div>
          <span className="text-xs font-semibold text-slate-800 dark:text-slate-200">Ledgers & Reports</span>
        </Link>
      </div>

      {/* Payment Modes Breakdown & Monthly Trend */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <h2 className="text-base font-bold text-slate-900 dark:text-white mb-4">
            Payment Mode Distribution
          </h2>
          <div className="space-y-3">
            {Object.entries(summary.payment_mode_distribution).map(([mode, amt]) => {
              const pct = ((amt / summary.total_collected_revenue) * 100).toFixed(1);
              return (
                <div key={mode} className="space-y-1">
                  <div className="flex justify-between text-xs font-medium text-slate-700 dark:text-slate-300">
                    <span>{mode.replace("_", " ")}</span>
                    <span>₹{amt.toLocaleString("en-IN")} ({pct}%)</span>
                  </div>
                  <div className="h-2 w-full rounded-full bg-slate-100 dark:bg-slate-700 overflow-hidden">
                    <div
                      className="h-full bg-emerald-600 rounded-full"
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs">
          <h2 className="text-base font-bold text-slate-900 dark:text-white mb-4">
            Financial Concessions & Relief Granted
          </h2>
          <div className="grid grid-cols-2 gap-4">
            <div className="rounded-lg bg-slate-50 dark:bg-slate-700/50 p-4 border border-slate-200/60 dark:border-slate-700">
              <span className="text-xs font-semibold uppercase text-slate-500 dark:text-slate-400">Merit & Need Scholarships</span>
              <p className="mt-2 text-xl font-bold text-purple-600 dark:text-purple-400">
                ₹{summary.total_scholarships_granted.toLocaleString("en-IN")}
              </p>
              <span className="text-[11px] text-slate-500">Government & Institutional</span>
            </div>
            <div className="rounded-lg bg-slate-50 dark:bg-slate-700/50 p-4 border border-slate-200/60 dark:border-slate-700">
              <span className="text-xs font-semibold uppercase text-slate-500 dark:text-slate-400">Sibling & Early Discounts</span>
              <p className="mt-2 text-xl font-bold text-blue-600 dark:text-blue-400">
                ₹{summary.total_discounts_granted.toLocaleString("en-IN")}
              </p>
              <span className="text-[11px] text-slate-500">Fee structure concessions</span>
            </div>
            <div className="rounded-lg bg-slate-50 dark:bg-slate-700/50 p-4 border border-slate-200/60 dark:border-slate-700 col-span-2">
              <span className="text-xs font-semibold uppercase text-slate-500 dark:text-slate-400">Audited Refunds Processed</span>
              <p className="mt-2 text-xl font-bold text-slate-700 dark:text-slate-200">
                ₹{summary.total_refunds_processed.toLocaleString("en-IN")}
              </p>
              <span className="text-[11px] text-slate-500">Withdrawals, excess payments & security deposits</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
