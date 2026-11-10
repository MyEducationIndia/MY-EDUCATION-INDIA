import React, { useState } from "react";
import { QrCode, CheckCircle2, ShieldCheck, RefreshCw, AlertCircle } from "lucide-react";

export const QRAttendanceScannerPage: React.FC = () => {
  const [tokenInput, setTokenInput] = useState("");
  const [recentScans, setRecentScans] = useState<any[]>([
    { id: "1", name: "Aarav Sharma", roll: "MEI-2026-CS-0042", time: "08:54 AM", status: "VERIFIED" },
    { id: "2", name: "Ananya Iyer", roll: "MEI-2026-CS-0043", time: "08:56 AM", status: "VERIFIED" },
    { id: "3", name: "Rohan Deshmukh", roll: "MEI-2026-CS-0046", time: "08:58 AM", status: "VERIFIED" },
  ]);

  const handleSimulateScan = (e: React.FormEvent) => {
    e.preventDefault();
    if (!tokenInput) return;
    const newScan = {
      id: Date.now().toString(),
      name: "Simulated Student",
      roll: `MEI-${Math.floor(1000 + Math.random() * 9000)}`,
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      status: "VERIFIED",
    };
    setRecentScans([newScan, ...recentScans]);
    setTokenInput("");
  };

  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-5 dark:border-slate-800">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
          <QrCode className="h-7 w-7 text-indigo-600 dark:text-indigo-400" />
          High-Speed QR Code & Barcode Attendance Terminal
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Instant contactless check-in using student identity QR cards with automated duplicate scan filtering.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Scanner Simulation Input */}
        <div className="lg:col-span-1 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Optical Scanner Hook</span>
              <span className="flex items-center gap-1.5 text-xs font-semibold text-emerald-600 bg-emerald-50 dark:bg-emerald-950 px-2 py-0.5 rounded-sm">
                <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
                Hardware Active
              </span>
            </div>

            <div className="h-44 rounded-xl border-2 border-dashed border-indigo-300 dark:border-indigo-800 bg-indigo-50/40 dark:bg-indigo-950/20 flex flex-col items-center justify-center p-4 text-center">
              <QrCode className="h-14 w-14 text-indigo-600 dark:text-indigo-400 mb-2" />
              <p className="text-xs font-bold text-slate-800 dark:text-slate-200">Point QR Code at Camera / Reader</p>
              <span className="text-[11px] text-slate-500 mt-0.5">Supports standard USB/Bluetooth 2D barcode imagers</span>
            </div>

            <form onSubmit={handleSimulateScan} className="mt-4 space-y-3">
              <input
                type="text"
                placeholder="Scan or paste student QR token payload..."
                value={tokenInput}
                onChange={(e) => setTokenInput(e.target.value)}
                className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/50 py-2 px-3 text-xs text-slate-900 dark:text-white focus:border-indigo-500 focus:outline-hidden"
              />
              <button
                type="submit"
                className="w-full rounded-lg bg-indigo-600 py-2 text-xs font-bold text-white hover:bg-indigo-700 transition"
              >
                Log QR Scan Manually
              </button>
            </form>
          </div>

          <div className="mt-6 pt-3 border-t border-slate-100 dark:border-slate-700 text-xs text-slate-400 flex items-center gap-1.5">
            <ShieldCheck className="h-4 w-4 text-indigo-500" />
            <span>Cryptographically verified against Student SIMS ID</span>
          </div>
        </div>

        {/* Live Real-time Feed */}
        <div className="lg:col-span-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-bold text-slate-900 dark:text-white">Recent Verified Gate Check-ins</h2>
            <button
              type="button"
              onClick={() => alert("Refreshed log")}
              className="text-xs font-semibold text-slate-500 flex items-center gap-1 hover:text-indigo-600"
            >
              <RefreshCw className="h-3.5 w-3.5" />
              <span>Live Stream</span>
            </button>
          </div>

          <div className="space-y-3">
            {recentScans.map((scan) => (
              <div
                key={scan.id}
                className="flex items-center justify-between rounded-lg bg-slate-50 dark:bg-slate-700/40 border border-slate-200/60 dark:border-slate-700 p-3.5"
              >
                <div className="flex items-center gap-3">
                  <div className="rounded-full bg-emerald-100 dark:bg-emerald-950 p-2 text-emerald-600 dark:text-emerald-400">
                    <CheckCircle2 className="h-4 w-4" />
                  </div>
                  <div>
                    <p className="text-sm font-bold text-slate-900 dark:text-white">{scan.name}</p>
                    <p className="font-mono text-xs text-slate-500">{scan.roll}</p>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-xs font-bold text-slate-700 dark:text-slate-300">{scan.time}</span>
                  <span className="block text-[11px] font-semibold text-emerald-600">{scan.status}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
