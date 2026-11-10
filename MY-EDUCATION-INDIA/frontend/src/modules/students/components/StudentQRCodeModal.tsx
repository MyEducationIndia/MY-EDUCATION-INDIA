import React from "react";
import { X, Printer, ShieldCheck, Download } from "lucide-react";
import { StudentDetailedProfile } from "../types/student.types";

interface StudentQRCodeModalProps {
  student: StudentDetailedProfile | null;
  onClose: () => void;
}

export const StudentQRCodeModal: React.FC<StudentQRCodeModalProps> = ({ student, onClose }) => {
  if (!student) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 p-4 backdrop-blur-xs">
      <div className="w-full max-w-md rounded-2xl border border-slate-200 bg-white p-6 shadow-2xl dark:border-slate-800 dark:bg-slate-900">
        <div className="flex items-center justify-between border-b border-slate-200 pb-3 dark:border-slate-800">
          <div className="flex items-center gap-2">
            <ShieldCheck className="h-5 w-5 text-brand-600" />
            <h3 className="text-sm font-bold text-slate-900 dark:text-white">Student Digital ID & QR Verification</h3>
          </div>
          <button type="button" onClick={onClose} className="text-slate-400 hover:text-slate-600 dark:hover:text-white">
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Printable ID Card Mockup */}
        <div id="printable-id-card" className="mt-5 rounded-2xl border-2 border-brand-600 bg-linear-to-b from-brand-50/50 to-white p-5 text-center shadow-lg dark:from-slate-950 dark:to-slate-900">
          <p className="text-[11px] font-extrabold uppercase tracking-widest text-brand-700 dark:text-brand-300">
            MY EDUCATION INDIA
          </p>
          <p className="text-[10px] text-slate-500">Autonomous University & Assessment Center</p>

          <div className="mt-4 flex flex-col items-center">
            <div className="flex h-16 w-16 items-center justify-center rounded-full border-2 border-brand-600 bg-slate-100 font-bold text-slate-700 dark:bg-slate-800 dark:text-slate-200">
              {student.first_name[0]}{student.last_name[0]}
            </div>
            <h4 className="mt-2 text-base font-extrabold text-slate-900 dark:text-white">
              {student.first_name} {student.middle_name ? `${student.middle_name} ` : ""}{student.last_name}
            </h4>
            <p className="font-mono text-xs font-bold text-brand-600 dark:text-brand-400">
              {student.registration_number}
            </p>
            <p className="mt-1 text-xs text-slate-600 dark:text-slate-400">
              {student.course_name} ({student.batch_name})
            </p>
            <span className="mt-1 inline-block rounded-sm bg-emerald-50 px-2 py-0.5 text-[10px] font-bold text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300">
              Status: {student.status}
            </span>
          </div>

          {/* Inline SVG QR Code */}
          <div className="mt-5 flex justify-center">
            {student.qr_svg ? (
              <div
                className="overflow-hidden rounded-xl border border-slate-200 p-2 shadow-xs bg-white"
                dangerouslySetInnerHTML={{ __html: student.qr_svg }}
              />
            ) : (
              <div className="h-32 w-32 flex items-center justify-center bg-slate-100 rounded-xl text-xs text-slate-400">
                QR Not Generated
              </div>
            )}
          </div>
          <p className="mt-2 text-[10px] text-slate-400">Scan for instantaneous CBT, Library & Gate attendance check</p>
        </div>

        <div className="mt-5 flex justify-end gap-2">
          <button
            type="button"
            onClick={() => window.print()}
            className="inline-flex items-center gap-1.5 rounded-xl bg-brand-600 px-4 py-2 text-xs font-bold text-white shadow-md hover:bg-brand-500"
          >
            <Printer className="h-4 w-4" /> Print ID Card
          </button>
        </div>
      </div>
    </div>
  );
};
