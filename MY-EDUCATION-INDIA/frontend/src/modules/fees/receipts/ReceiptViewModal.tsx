import React from "react";
import { X, Printer, Download, ShieldCheck, QrCode } from "lucide-react";

interface ReceiptViewModalProps {
  receipt: {
    receipt_number: string;
    student_name: string;
    enrollment_number: string;
    amount: number;
    amount_in_words: string;
    payment_mode: string;
    date: string;
  };
  onClose: () => void;
}

export const ReceiptViewModal: React.FC<ReceiptViewModalProps> = ({ receipt, onClose }) => {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4">
      <div className="w-full max-w-xl rounded-2xl bg-white dark:bg-slate-800 shadow-2xl border border-slate-200 dark:border-slate-700 overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-700 px-6 py-4 bg-slate-50 dark:bg-slate-800/80">
          <div className="flex items-center gap-2.5">
            <ShieldCheck className="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
            <h3 className="text-base font-bold text-slate-900 dark:text-white">Official Institutional Fee Receipt</h3>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Receipt Content */}
        <div className="p-6 space-y-4">
          <div className="text-center pb-4 border-b border-slate-100 dark:border-slate-700">
            <h2 className="text-lg font-extrabold text-slate-900 dark:text-white">MY EDUCATION INDIA</h2>
            <p className="text-xs text-slate-500">Universal Educational ERP & Campus Administration</p>
            <span className="mt-2 inline-block font-mono text-xs font-bold text-emerald-600 bg-emerald-50 dark:bg-emerald-950 px-2.5 py-0.5 rounded-sm">
              {receipt.receipt_number}
            </span>
          </div>

          <div className="grid grid-cols-2 gap-3 text-xs">
            <div>
              <span className="text-slate-400 uppercase font-semibold">Student Name:</span>
              <p className="font-bold text-slate-900 dark:text-white">{receipt.student_name}</p>
            </div>
            <div>
              <span className="text-slate-400 uppercase font-semibold">Enrollment ID:</span>
              <p className="font-mono font-bold text-slate-900 dark:text-white">{receipt.enrollment_number}</p>
            </div>
            <div>
              <span className="text-slate-400 uppercase font-semibold">Payment Mode:</span>
              <p className="font-semibold text-slate-700 dark:text-slate-300">{receipt.payment_mode}</p>
            </div>
            <div>
              <span className="text-slate-400 uppercase font-semibold">Date of Receipt:</span>
              <p className="font-semibold text-slate-700 dark:text-slate-300">{receipt.date}</p>
            </div>
          </div>

          <div className="rounded-lg bg-emerald-50 dark:bg-emerald-950/40 p-4 border border-emerald-200/60 dark:border-emerald-800">
            <span className="text-xs font-semibold text-emerald-700 dark:text-emerald-400 uppercase">Amount Received</span>
            <p className="text-2xl font-black text-emerald-700 dark:text-emerald-300">
              ₹{receipt.amount.toLocaleString("en-IN")}
            </p>
            <p className="text-xs italic text-emerald-800 dark:text-emerald-400 mt-1">
              "{receipt.amount_in_words}"
            </p>
          </div>

          <div className="flex items-center justify-between pt-2">
            <div className="flex items-center gap-2 text-xs text-slate-500">
              <QrCode className="h-8 w-8 text-slate-700 dark:text-slate-300" />
              <span>Digitally Verified & Validated</span>
            </div>
            <div className="text-right text-xs text-slate-400">
              <p>Authorized Signatory</p>
              <p className="font-semibold text-slate-700 dark:text-slate-300">Finance & Accounts Office</p>
            </div>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="flex items-center justify-end gap-3 border-t border-slate-100 dark:border-slate-700 px-6 py-4 bg-slate-50 dark:bg-slate-800/80">
          <button
            type="button"
            onClick={() => window.print()}
            className="flex items-center gap-2 rounded-lg bg-emerald-600 px-4 py-2 text-xs font-bold text-white hover:bg-emerald-700 transition"
          >
            <Printer className="h-4 w-4" />
            <span>Print Receipt</span>
          </button>
        </div>
      </div>
    </div>
  );
};
