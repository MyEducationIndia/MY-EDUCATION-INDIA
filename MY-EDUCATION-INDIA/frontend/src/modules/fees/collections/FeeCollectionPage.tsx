import React, { useState } from "react";
import { CreditCard, IndianRupee, Search, CheckCircle, Receipt, ArrowRight } from "lucide-react";
import { ReceiptViewModal } from "../receipts/ReceiptViewModal";

export const FeeCollectionPage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedStudent, setSelectedStudent] = useState<any>({
    name: "Aarav Sharma",
    enrollment_number: "MEI-2026-CS-0042",
    course: "B.Tech Computer Science (2026-2030)",
    total_fee: 145000.0,
    paid: 72500.0,
    due: 72500.0,
    installment: "2nd Semester Fee (Due Jan 15, 2027)",
  });
  const [amountToPay, setAmountToPay] = useState("72500");
  const [paymentMode, setPaymentMode] = useState("UPI");
  const [showReceiptModal, setShowReceiptModal] = useState(false);
  const [generatedReceipt, setGeneratedReceipt] = useState<any>(null);

  const handleCollect = (e: React.FormEvent) => {
    e.preventDefault();
    const receiptData = {
      receipt_number: `REC-MEI-20261106-${Math.floor(1000 + Math.random() * 9000)}`,
      student_name: selectedStudent.name,
      enrollment_number: selectedStudent.enrollment_number,
      amount: parseFloat(amountToPay),
      amount_in_words: "Seventy Two Thousand Five Hundred Rupees Only",
      payment_mode: paymentMode,
      date: new Date().toISOString().split("T")[0],
    };
    setGeneratedReceipt(receiptData);
    setShowReceiptModal(true);
  };

  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-5 dark:border-slate-800">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
          <CreditCard className="h-7 w-7 text-emerald-600 dark:text-emerald-400" />
          Counter Fee Collection & Payment Terminal
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Process student counter payments across Cash, UPI, Cards, Net Banking & DD with instant receipts.
        </p>
      </div>

      {/* Student Search Bar */}
      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-4 shadow-xs">
        <div className="relative">
          <Search className="absolute left-3.5 top-3 h-5 w-5 text-slate-400" />
          <input
            type="text"
            placeholder="Search by student enrollment number, name, or phone..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/50 py-2.5 pl-11 pr-4 text-sm text-slate-900 dark:text-white focus:border-emerald-500 focus:outline-hidden"
          />
        </div>
      </div>

      {/* Collection Form & Account Ledger */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs">
          <h2 className="text-base font-bold text-slate-900 dark:text-white mb-4">Student Account Summary</h2>
          <div className="space-y-3 text-sm">
            <div>
              <span className="text-xs text-slate-400 uppercase font-semibold">Student Name</span>
              <p className="font-bold text-slate-900 dark:text-white">{selectedStudent.name}</p>
            </div>
            <div>
              <span className="text-xs text-slate-400 uppercase font-semibold">Enrollment ID</span>
              <p className="font-mono text-emerald-600 dark:text-emerald-400 font-bold">{selectedStudent.enrollment_number}</p>
            </div>
            <div>
              <span className="text-xs text-slate-400 uppercase font-semibold">Course & Batch</span>
              <p className="text-slate-700 dark:text-slate-300">{selectedStudent.course}</p>
            </div>
            <div className="pt-3 border-t border-slate-100 dark:border-slate-700 space-y-2">
              <div className="flex justify-between text-xs">
                <span className="text-slate-500">Total Program Fee:</span>
                <span className="font-semibold text-slate-900 dark:text-white">₹{selectedStudent.total_fee.toLocaleString("en-IN")}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-slate-500">Paid So Far:</span>
                <span className="font-semibold text-emerald-600">₹{selectedStudent.paid.toLocaleString("en-IN")}</span>
              </div>
              <div className="flex justify-between text-xs font-bold text-rose-600 pt-1 border-t border-dashed border-slate-200 dark:border-slate-700">
                <span>Remaining Due:</span>
                <span>₹{selectedStudent.due.toLocaleString("en-IN")}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="lg:col-span-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs">
          <h2 className="text-base font-bold text-slate-900 dark:text-white mb-4">Record Payment & Issue Receipt</h2>
          <form onSubmit={handleCollect} className="space-y-4">
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1.5">
                Amount to Collect (₹)
              </label>
              <div className="relative">
                <IndianRupee className="absolute left-3.5 top-3 h-4 w-4 text-slate-400" />
                <input
                  type="number"
                  value={amountToPay}
                  onChange={(e) => setAmountToPay(e.target.value)}
                  className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/50 py-2 pl-10 pr-4 text-base font-bold text-slate-900 dark:text-white focus:border-emerald-500 focus:outline-hidden"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1.5">
                Payment Mode
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                {["UPI", "CASH", "NET_BANKING", "CREDIT_CARD", "DEBIT_CARD", "CHEQUE", "DEMAND_DRAFT", "BANK_TRANSFER"].map((mode) => (
                  <button
                    key={mode}
                    type="button"
                    onClick={() => setPaymentMode(mode)}
                    className={`rounded-lg py-2 px-3 text-xs font-semibold border transition ${
                      paymentMode === mode
                        ? "border-emerald-600 bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400"
                        : "border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700"
                    }`}
                  >
                    {mode.replace("_", " ")}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1.5">
                Transaction / Cheque / UTR Reference
              </label>
              <input
                type="text"
                placeholder="e.g. UPI-984210948190 or CHQ-002148"
                className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/50 py-2 px-3.5 text-sm text-slate-900 dark:text-white focus:border-emerald-500 focus:outline-hidden"
              />
            </div>

            <button
              type="submit"
              className="w-full flex items-center justify-center gap-2 rounded-lg bg-emerald-600 py-3 text-sm font-bold text-white shadow-xs hover:bg-emerald-700 transition"
            >
              <CheckCircle className="h-5 w-5" />
              <span>Confirm Payment & Print Universal Receipt</span>
            </button>
          </form>
        </div>
      </div>

      {showReceiptModal && generatedReceipt && (
        <ReceiptViewModal
          receipt={generatedReceipt}
          onClose={() => setShowReceiptModal(false)}
        />
      )}
    </div>
  );
};
