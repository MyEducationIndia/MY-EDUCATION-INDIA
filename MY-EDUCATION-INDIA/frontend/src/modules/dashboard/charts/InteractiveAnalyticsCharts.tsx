import React from "react";
import { MultiChartData, TimeSeriesPoint } from "../types/dashboard.types";

interface InteractiveAnalyticsChartsProps {
  data: MultiChartData;
  granularity: string;
  onGranularityChange: (g: string) => void;
}

export const InteractiveAnalyticsCharts: React.FC<InteractiveAnalyticsChartsProps> = ({
  data,
  granularity,
  onGranularityChange,
}) => {
  const maxAdmission = Math.max(...data.admission_trends.map((p) => p.value), 50);
  const maxFees = Math.max(...data.fee_collection.map((p) => p.value), 1000);

  return (
    <div className="space-y-6">
      {/* Chart Granularity Filter */}
      <div className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-xs dark:border-slate-800 dark:bg-slate-900">
        <div>
          <h2 className="text-sm font-bold text-slate-900 dark:text-white">Enterprise Visual Analytics</h2>
          <p className="text-xs text-slate-500 dark:text-slate-400">Time-series and distribution metrics queried from Neon PostgreSQL.</p>
        </div>
        <div className="flex gap-1.5">
          {["DAILY", "WEEKLY", "MONTHLY", "YEARLY"].map((g) => (
            <button
              key={g}
              type="button"
              onClick={() => onGranularityChange(g)}
              className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition ${
                granularity === g
                  ? "bg-brand-600 text-white"
                  : "bg-slate-100 text-slate-700 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-300"
              }`}
            >
              {g}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Admission Trends Bar Chart */}
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300">
              Admission Trends ({granularity})
            </h3>
            <span className="text-xs font-semibold text-brand-600 dark:text-brand-400">Total: {data.admission_trends.reduce((a, b) => a + b.value, 0)} Admissions</span>
          </div>

          <div className="mt-6 flex h-48 items-end gap-2 border-b border-slate-200 pb-2 dark:border-slate-800">
            {data.admission_trends.map((pt, i) => {
              const heightPct = (pt.value / maxAdmission) * 100;
              return (
                <div key={i} className="group relative flex flex-1 flex-col items-center">
                  <div
                    style={{ height: `${Math.max(heightPct, 8)}%` }}
                    className="w-full rounded-t-md bg-blue-600 transition-all hover:bg-blue-500"
                  />
                  <span className="mt-2 text-[10px] text-slate-500 truncate w-full text-center">{pt.label}</span>
                  {/* Tooltip */}
                  <div className="absolute -top-7 hidden rounded-md bg-slate-900 px-2 py-0.5 text-[10px] text-white shadow-md group-hover:block dark:bg-slate-800">
                    {pt.value}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Fee Collection Trends Chart */}
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300">
              Fee Collections (₹ Thousands)
            </h3>
            <span className="text-xs font-semibold text-teal-600 dark:text-teal-400">Growth: +14.2%</span>
          </div>

          <div className="mt-6 flex h-48 items-end gap-2 border-b border-slate-200 pb-2 dark:border-slate-800">
            {data.fee_collection.map((pt, i) => {
              const heightPct = (pt.value / maxFees) * 100;
              return (
                <div key={i} className="group relative flex flex-1 flex-col items-center">
                  <div
                    style={{ height: `${Math.max(heightPct, 8)}%` }}
                    className="w-full rounded-t-md bg-teal-600 transition-all hover:bg-teal-500"
                  />
                  <span className="mt-2 text-[10px] text-slate-500 truncate w-full text-center">{pt.label}</span>
                  <div className="absolute -top-7 hidden rounded-md bg-slate-900 px-2 py-0.5 text-[10px] text-white shadow-md group-hover:block dark:bg-slate-800">
                    ₹{pt.value}k
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Course Popularity Breakdown */}
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300">
            Course Enrollment Popularity
          </h3>
          <div className="mt-4 space-y-3">
            {data.course_popularity.map((c) => (
              <div key={c.name}>
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-slate-900 dark:text-white truncate max-w-[200px]">{c.name}</span>
                  <span className="text-slate-500">{c.count} ({c.percentage}%)</span>
                </div>
                <div className="mt-1 h-2 w-full rounded-full bg-slate-100 dark:bg-slate-800">
                  <div
                    style={{ width: `${c.percentage}%`, backgroundColor: c.color_hex || "#1D4ED8" }}
                    className="h-2 rounded-full"
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Branch Student Comparison */}
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300">
            Regional Branch Distribution
          </h3>
          <div className="mt-4 space-y-3">
            {data.branch_comparison.map((b) => (
              <div key={b.name}>
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-slate-900 dark:text-white truncate">{b.name}</span>
                  <span className="text-slate-500">{b.count} Students</span>
                </div>
                <div className="mt-1 h-2 w-full rounded-full bg-slate-100 dark:bg-slate-800">
                  <div
                    style={{ width: `${b.percentage}%`, backgroundColor: b.color_hex || "#0D9488" }}
                    className="h-2 rounded-full"
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Omnichannel Broadcast Delivery */}
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300">
            Omnichannel Communication Hub
          </h3>
          <div className="mt-4 space-y-3 text-xs">
            <div className="flex items-center justify-between rounded-xl bg-slate-50 p-3 dark:bg-slate-950">
              <span className="font-semibold text-slate-700 dark:text-slate-300">DLT SMS Sent</span>
              <strong className="font-mono text-slate-900 dark:text-white">{data.channel_statistics.sms?.toLocaleString()}</strong>
            </div>
            <div className="flex items-center justify-between rounded-xl bg-slate-50 p-3 dark:bg-slate-950">
              <span className="font-semibold text-slate-700 dark:text-slate-300">WhatsApp Alerts</span>
              <strong className="font-mono text-slate-900 dark:text-white">{data.channel_statistics.whatsapp?.toLocaleString()}</strong>
            </div>
            <div className="flex items-center justify-between rounded-xl bg-slate-50 p-3 dark:bg-slate-950">
              <span className="font-semibold text-slate-700 dark:text-slate-300">Transactional Emails</span>
              <strong className="font-mono text-slate-900 dark:text-white">{data.channel_statistics.email?.toLocaleString()}</strong>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
