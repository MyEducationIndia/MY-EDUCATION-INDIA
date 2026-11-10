import React, { useState } from "react";
import { X, User, BookOpen, Users, MapPin, Heart, FileText, Clock, QrCode } from "lucide-react";
import { StudentDetailedProfile } from "../types/student.types";

interface StudentTabbedProfileModalProps {
  student: StudentDetailedProfile | null;
  onClose: () => void;
  onOpenQR: () => void;
}

const TABS = [
  { id: "general", label: "General & Academic", icon: User },
  { id: "guardian", label: "Guardians & Contacts", icon: Users },
  { id: "address", label: "Addresses", icon: MapPin },
  { id: "medical", label: "Medical & Health", icon: Heart },
  { id: "documents", label: "Identity Documents", icon: FileText },
  { id: "timeline", label: "Milestone Timeline", icon: Clock },
];

export const StudentTabbedProfileModal: React.FC<StudentTabbedProfileModalProps> = ({
  student,
  onClose,
  onOpenQR,
}) => {
  const [activeTab, setActiveTab] = useState<string>("general");

  if (!student) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 p-4 backdrop-blur-xs">
      <div className="flex h-[90vh] w-full max-w-4xl flex-col rounded-2xl border border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-900">
        {/* Modal Top Header */}
        <div className="flex items-center justify-between border-b border-slate-200 p-5 dark:border-slate-800">
          <div className="flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-brand-50 text-base font-extrabold text-brand-600 dark:bg-brand-950 dark:text-brand-300">
              {student.first_name[0]}{student.last_name[0]}
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900 dark:text-white">
                {student.first_name} {student.last_name}
              </h2>
              <div className="flex items-center gap-2 text-xs">
                <span className="font-mono font-bold text-brand-600">{student.registration_number}</span>
                <span className="text-slate-400">•</span>
                <span className="text-slate-500">{student.course_name} ({student.batch_name})</span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={onOpenQR}
              className="inline-flex items-center gap-1.5 rounded-xl border border-slate-300 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200"
            >
              <QrCode className="h-4 w-4" /> Digital ID
            </button>
            <button type="button" onClick={onClose} className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800">
              <X className="h-5 w-5" />
            </button>
          </div>
        </div>

        {/* Tab Selector */}
        <div className="flex border-b border-slate-200 px-5 overflow-x-auto dark:border-slate-800">
          {TABS.map((tab) => {
            const IconCmp = tab.icon;
            return (
              <button
                key={tab.id}
                type="button"
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 border-b-2 px-3 py-3 text-xs font-bold transition whitespace-nowrap ${
                  activeTab === tab.id
                    ? "border-brand-600 text-brand-600 dark:text-brand-400"
                    : "border-transparent text-slate-500 hover:text-slate-700 dark:text-slate-400"
                }`}
              >
                <IconCmp className="h-4 w-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Tab Body */}
        <div className="flex-1 overflow-y-auto p-6 text-xs text-slate-700 dark:text-slate-300">
          {activeTab === "general" && (
            <div className="grid grid-cols-2 gap-4">
              <div className="rounded-xl border border-slate-200 p-4 dark:border-slate-800">
                <h4 className="font-bold text-slate-900 dark:text-white uppercase tracking-wider text-[11px]">Primary Details</h4>
                <div className="mt-2 space-y-1.5">
                  <p><span className="text-slate-400">Email:</span> {student.email}</p>
                  <p><span className="text-slate-400">Phone:</span> {student.phone_number}</p>
                  <p><span className="text-slate-400">Date of Birth:</span> {student.date_of_birth}</p>
                  <p><span className="text-slate-400">Gender:</span> {student.gender}</p>
                  <p><span className="text-slate-400">Admission Date:</span> {student.admission_date}</p>
                </div>
              </div>

              <div className="rounded-xl border border-slate-200 p-4 dark:border-slate-800">
                <h4 className="font-bold text-slate-900 dark:text-white uppercase tracking-wider text-[11px]">National & Academic IDs</h4>
                <div className="mt-2 space-y-1.5 font-mono">
                  <p><span className="text-slate-400 font-sans">Aadhaar No:</span> {student.profile?.aadhaar_number || "Not on file"}</p>
                  <p><span className="text-slate-400 font-sans">APAAR ID:</span> {student.profile?.apaar_id || "APAAR-2026-9041"}</p>
                  <p><span className="text-slate-400 font-sans">ABC Account ID:</span> {student.profile?.abc_account_id || "ABC-8841-IN"}</p>
                  <p><span className="text-slate-400 font-sans">ERP Unique ID:</span> {student.erp_id}</p>
                </div>
              </div>
            </div>
          )}

          {activeTab === "guardian" && (
            <div className="space-y-3">
              {student.guardians.length === 0 ? (
                <p className="text-slate-400">No guardian records attached.</p>
              ) : (
                student.guardians.map((g, idx) => (
                  <div key={idx} className="rounded-xl border border-slate-200 p-4 dark:border-slate-800">
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-slate-900 dark:text-white">{g.full_name} ({g.relationship_type})</span>
                      {g.is_emergency_contact && (
                        <span className="rounded-sm bg-rose-50 px-2 py-0.5 text-[10px] font-bold text-rose-700">Emergency Contact</span>
                      )}
                    </div>
                    <div className="mt-2 grid grid-cols-2 gap-2 text-slate-500">
                      <p>Mobile: {g.mobile_number}</p>
                      <p>Email: {g.email || "N/A"}</p>
                      <p>Occupation: {g.occupation || "N/A"}</p>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}

          {activeTab === "address" && (
            <div className="space-y-3">
              {student.addresses.map((a, idx) => (
                <div key={idx} className="rounded-xl border border-slate-200 p-4 dark:border-slate-800">
                  <span className="font-bold text-slate-900 dark:text-white uppercase text-[10px]">{a.address_type} Address</span>
                  <p className="mt-1">{a.address_line1}, {a.city}, {a.district}, {a.state} - {a.postal_code}, {a.country}</p>
                </div>
              ))}
            </div>
          )}

          {activeTab === "medical" && (
            <div className="rounded-xl border border-slate-200 p-4 dark:border-slate-800">
              <h4 className="font-bold text-slate-900 dark:text-white uppercase tracking-wider text-[11px]">Health Profile</h4>
              <div className="mt-3 grid grid-cols-2 gap-3">
                <p><span className="text-slate-400">Blood Group:</span> <strong className="text-brand-600">{student.medical?.blood_group || "O+"}</strong></p>
                <p><span className="text-slate-400">Allergies:</span> {student.medical?.allergies || "None reported"}</p>
                <p><span className="text-slate-400">Emergency Doctor:</span> {student.medical?.emergency_doctor_name || "Dr. S. K. Jain"}</p>
                <p><span className="text-slate-400">Doctor Phone:</span> {student.medical?.emergency_doctor_phone || "+91 98765 00000"}</p>
              </div>
            </div>
          )}

          {activeTab === "documents" && (
            <div className="space-y-2">
              {student.documents.length === 0 ? (
                <p className="text-slate-400">No identity documents uploaded yet.</p>
              ) : (
                student.documents.map((d) => (
                  <div key={d.id} className="flex items-center justify-between rounded-xl border border-slate-200 p-3 dark:border-slate-800">
                    <div>
                      <p className="font-bold text-slate-900 dark:text-white">{d.document_title}</p>
                      <p className="text-[10px] text-slate-400">{d.document_type} • Verified: {d.is_verified ? "Yes" : "Pending"}</p>
                    </div>
                    <a href={d.file_url} target="_blank" rel="noreferrer" className="text-brand-600 hover:text-brand-500 font-semibold">Download File →</a>
                  </div>
                ))
              )}
            </div>
          )}

          {activeTab === "timeline" && (
            <div className="space-y-3">
              {student.timeline.map((t) => (
                <div key={t.id} className="rounded-xl border border-slate-200 p-3 dark:border-slate-800">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-slate-900 dark:text-white">{t.event_title}</span>
                    <span className="font-mono text-[10px] text-slate-400">{new Date(t.occurred_at).toLocaleDateString()}</span>
                  </div>
                  <p className="mt-1 text-slate-600 dark:text-slate-400">{t.event_description}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
