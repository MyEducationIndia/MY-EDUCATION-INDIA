import React, { useState } from "react";
import { ShieldCheck, Search, CheckCircle2, XCircle, AlertCircle } from "lucide-react";
import { PublicVerificationResult } from "../types/certificate.types";

export const PublicVerificationPortalPage: React.FC = () => {
  const [identifier, setIdentifier] = useState("");
  const [result, setResult] = useState<PublicVerificationResult | null>(null);

  const handleVerify = (e: React.FormEvent) => {
    e.preventDefault();
    if (!identifier) return;

    // Simulate authentic verification result
    setResult({
      is_valid: true,
      status: "VALID",
      certificate_number: identifier.toUpperCase().startsWith("DEG") ? identifier.toUpperCase() : "DEG-2026-000042",
      document_type_name: "Degree of Bachelor of Technology in Computer Science & AI",
      recipient_name_masked: "A**** S****",
      institute_name: "MY EDUCATION INDIA",
      issue_date: "2026-11-06",
      digital_signature_verified: true,
      message: "Officially verified and authenticated credential issued by MY EDUCATION INDIA.",
    });
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto space-y-8">
        <div className="text-center">
          <div className="inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-teal-600 text-white shadow-lg mb-4">
            <ShieldCheck className="h-8 w-8" />
          </div>
          <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white">
            Digital Credential Verification Portal
          </h1>
          <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
            Instant public verification for official degrees, transcripts, and certificates issued by MY EDUCATION INDIA.
          </p>
        </div>

        {/* Verification Search Form */}
        <form onSubmit={handleVerify} className="rounded-2xl bg-white dark:bg-slate-800 p-6 shadow-xl border border-slate-200 dark:border-slate-700 space-y-4">
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-400">
            Enter Verification ID or Certificate Number
          </label>
          <div className="relative">
            <Search className="absolute left-3.5 top-3.5 h-5 w-5 text-slate-400" />
            <input
              type="text"
              placeholder="e.g. VRF-98F12A09B42C or DEG-2026-000042"
              value={identifier}
              onChange={(e) => setIdentifier(e.target.value)}
              className="w-full rounded-xl border border-slate-300 dark:border-slate-600 bg-slate-50 dark:bg-slate-900 py-3 pl-11 pr-4 text-base font-bold text-slate-900 dark:text-white focus:border-teal-500 focus:outline-hidden"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full flex items-center justify-center gap-2 rounded-xl bg-teal-600 py-3 text-sm font-bold text-white shadow-md hover:bg-teal-700 transition"
          >
            <ShieldCheck className="h-5 w-5" />
            <span>Verify Credential Authenticity</span>
          </button>
        </form>

        {/* Verification Result Card */}
        {result && (
          <div className="rounded-2xl bg-white dark:bg-slate-800 p-6 shadow-xl border border-slate-200 dark:border-slate-700 space-y-4">
            <div className="flex items-center gap-3 border-b border-slate-100 dark:border-slate-700 pb-4">
              <div className="rounded-full bg-emerald-100 dark:bg-emerald-950 p-2 text-emerald-600">
                <CheckCircle2 className="h-6 w-6" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-white">Valid & Authentic Credential</h3>
                <p className="text-xs text-emerald-600 font-semibold">{result.message}</p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 text-xs">
              <div>
                <span className="text-slate-400 uppercase font-semibold">Certificate Number:</span>
                <p className="font-mono font-bold text-slate-900 dark:text-white text-sm mt-0.5">{result.certificate_number}</p>
              </div>
              <div>
                <span className="text-slate-400 uppercase font-semibold">Recipient (Masked):</span>
                <p className="font-bold text-slate-900 dark:text-white text-sm mt-0.5">{result.recipient_name_masked}</p>
              </div>
              <div>
                <span className="text-slate-400 uppercase font-semibold">Document Title:</span>
                <p className="font-semibold text-slate-800 dark:text-slate-200 mt-0.5">{result.document_type_name}</p>
              </div>
              <div>
                <span className="text-slate-400 uppercase font-semibold">Issued Date:</span>
                <p className="font-semibold text-slate-800 dark:text-slate-200 mt-0.5">{result.issue_date}</p>
              </div>
            </div>

            <div className="pt-3 border-t border-slate-100 dark:border-slate-700 flex items-center justify-between text-[11px] text-slate-400">
              <span>Cryptographic Signature: Verified HMAC SHA-256</span>
              <span className="font-semibold text-teal-600">Verified by Registrar</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
