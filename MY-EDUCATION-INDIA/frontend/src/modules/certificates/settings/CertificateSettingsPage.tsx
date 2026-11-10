import React, { useState } from "react";
import { Sliders, Save, ShieldCheck } from "lucide-react";

export const CertificateSettingsPage: React.FC = () => {
  const [enableDSC, setEnableDSC] = useState(true);
  const [qrSize, setQrSize] = useState(128);

  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-5 dark:border-slate-800">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
          <Sliders className="h-7 w-7 text-teal-600 dark:text-teal-400" />
          Digital Signature (DSC) & Credential Policies
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Configure cryptographic PKI signature keys, public verification URL routing, and security policies.
        </p>
      </div>

      <div className="max-w-2xl rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs space-y-4">
        <label className="flex items-center gap-3 text-sm font-semibold text-slate-800 dark:text-slate-200">
          <input
            type="checkbox"
            checked={enableDSC}
            onChange={(e) => setEnableDSC(e.target.checked)}
            className="h-4 w-4 rounded-sm text-teal-600 focus:ring-teal-500"
          />
          <span>Enable Cryptographic HMAC-SHA256 Digital Signature Stamp</span>
        </label>

        <div>
          <label className="block text-xs font-bold uppercase text-slate-400 mb-1">Standard QR Code Dimension (Pixels)</label>
          <input
            type="number"
            value={qrSize}
            onChange={(e) => setQrSize(Number(e.target.value))}
            className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 py-2 px-3 text-sm font-bold"
          />
        </div>

        <button
          type="button"
          onClick={() => alert("Credential security policies saved!")}
          className="flex items-center gap-2 rounded-lg bg-teal-600 px-4 py-2 text-xs font-bold text-white shadow-xs hover:bg-teal-700 transition"
        >
          <Save className="h-4 w-4" />
          <span>Save Security Policies</span>
        </button>
      </div>
    </div>
  );
};
