import React, { useState } from "react";
import { FileText, Download, Calendar, Filter, IndianRupee } from "lucide-react";

export const FinancialReportsPage: React.FC = () => {
  const [reportType, setReportType] = useState("DAILY_COLLECTION");
  const [selectedDate, setSelectedDate] = useState("2026-11-06");

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <FileText className="h-7 w-7 text-emerald-600 dark:text-emerald-400" />
            Financial Ledgers & Regulatory Audit Reports
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Export daily cashier sheets, monthly reconciliations, outstanding fee dues, and refund summaries.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => alert("Exporting report as Excel...")}
            className="flex items-center gap-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-2 text-xs font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 transition"
          >
            <Download className="h-4 w-4" />
            <span>Excel Export</span>
          </button>
          <button
            type="button"
            onClick={() => alert("Exporting report as PDF...")}
            className="flex items-center gap-2 rounded-lg bg-emerald-600 px-3 py-2 text-xs font-semibold text-white hover:bg-emerald-700 transition"
          >
            <Download className="h-4 w-4" />
            <span>PDF Print</span>
          </button>
        </div>
      </div>

      {/* Filter Controls */}
      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-4 shadow-xs flex flex-wrap items-center gap-4">
        <div>
          <label className="block text-[11px] font-bold uppercase text-slate-400 mb-1">Report Type</label>
          <select
            value={reportType}
            onChange={(e) => setReportType(e.target.value)}
            className="rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/50 py-1.5 px-3 text-xs text-slate-800 dark:text-slate-200"
          >
            <option value="DAILY_COLLECTION">Daily Cashier Collection</option>
            <option value="MONTHLY_COLLECTION">Monthly Reconciled Summary</option>
            <option value="OUTSTANDING">Outstanding Dues Ledger</option>
            <option value="SCHOLARSHIP">Scholarship Grant Utilization</option>
            <option value="REFUND">Refunds & Cancellations Ledger</option>
          </select>
        </div>
        <div>
          <label className="block text-[11px] font-bold uppercase text-slate-400 mb-1">Target Date</label>
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/50 py-1.5 px-3 text-xs text-slate-800 dark:text-slate-200"
          />
        </div>
      </div>

      {/* Sample Daily Report Summary */}
      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs">
        <div className="flex justify-between items-center border-b border-slate-100 dark:border-slate-700 pb-4 mb-4">
          <div>
            <h3 className="text-base font-bold text-slate-900 dark:text-white">Daily Cashier Summary: {selectedDate}</h3>
            <p className="text-xs text-slate-500">Institute Head Office Counter & Online Gateways</p>
          </div>
          <div className="text-right">
            <span className="text-xs text-slate-400 uppercase font-semibold">Total Collections</span>
            <p className="text-xl font-black text-emerald-600 dark:text-emerald-400">₹1,85,000.00</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="rounded-lg bg-slate-50 dark:bg-slate-700/40 p-3 border border-slate-200/60 dark:border-slate-700">
            <span className="text-xs text-slate-500">UPI Payments (12 tx)</span>
            <p className="text-base font-bold text-slate-900 dark:text-white mt-1">₹1,10,000.00</p>
          </div>
          <div className="rounded-lg bg-slate-50 dark:bg-slate-700/40 p-3 border border-slate-200/60 dark:border-slate-700">
            <span className="text-xs text-slate-500">Cash Register (4 tx)</span>
            <p className="text-base font-bold text-slate-900 dark:text-white mt-1">₹45,000.00</p>
          </div>
          <div className="rounded-lg bg-slate-50 dark:bg-slate-700/40 p-3 border border-slate-200/60 dark:border-slate-700">
            <span className="text-xs text-slate-500">Debit / Credit Cards (3 tx)</span>
            <p className="text-base font-bold text-slate-900 dark:text-white mt-1">₹30,000.00</p>
          </div>
          <div className="rounded-lg bg-slate-50 dark:bg-slate-700/40 p-3 border border-slate-200/60 dark:border-slate-700">
            <span className="text-xs text-slate-500">Cheques / DD (0 tx)</span>
            <p className="text-base font-bold text-slate-900 dark:text-white mt-1">₹0.00</p>
          </div>
        </div>
      </div>
    </div>
  );
};
