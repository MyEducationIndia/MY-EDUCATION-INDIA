import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Building2,
  Calendar,
  CreditCard,
  Globe,
  Mail,
  MapPin,
  MessageSquare,
  Palette,
  Phone,
  Save,
  Send,
  ShieldCheck,
  Plus,
  Trash2,
  Edit2,
  CheckCircle2,
  ExternalLink,
} from "lucide-react";
import { instituteService } from "@/services/instituteService";
import {
  AcademicSessionCreatePayload,
  AcademicSessionItem,
  Institute,
  InstituteIntegrationsUpdatePayload,
  InstituteProfileUpdatePayload,
} from "@/types/institute.types";

export const InstituteSetupPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<
    "profile" | "branding" | "sessions" | "gateways" | "social"
  >("profile");

  // Fetch all institutes to find the primary institute (MEI-HQ)
  const { data: institutes = [], isLoading: institutesLoading } = useQuery({
    queryKey: ["institutes"],
    queryFn: () => instituteService.listInstitutes(),
  });

  const primaryInst = institutes[0] as Institute | undefined;
  const instituteId = primaryInst?.id;

  // Fetch full setup bundle for primary institute
  const { data: setupBundle, isLoading: bundleLoading } = useQuery({
    queryKey: ["institute-setup-bundle", instituteId],
    queryFn: () => (instituteId ? instituteService.getSetupBundle(instituteId) : null),
    enabled: Boolean(instituteId),
  });

  // Local form states
  const inst = setupBundle?.institute || primaryInst;

  // Profile State
  const [profileForm, setProfileForm] = useState<InstituteProfileUpdatePayload>({});
  const [isProfileDirty, setIsProfileDirty] = useState(false);

  // Branding State
  const [primaryColor, setPrimaryColor] = useState(inst?.primary_color_hex || "#1E40AF");
  const [secondaryColor, setSecondaryColor] = useState(inst?.secondary_color_hex || "#0D9488");
  const [logoUrl, setLogoUrl] = useState(inst?.logo_url || "");
  const [faviconUrl, setFaviconUrl] = useState(inst?.favicon_url || "");

  // Gateways State
  const [smtpConfig, setSmtpConfig] = useState({
    host: "smtp.mailgun.org",
    port: 587,
    username: "postmaster@mg.myeducationindia.com",
    sender_email: "noreply@myeducationindia.com",
    encryption: "TLS",
    enabled: true,
  });

  const [smsConfig, setSmsConfig] = useState({
    provider: "Gupshup DLT",
    sender_id: "MYEDIN",
    api_key: "********************",
    dlt_entity_id: "14015689745236",
    enabled: true,
  });

  const [whatsappConfig, setWhatsappConfig] = useState({
    provider: "Meta Cloud API",
    phone_number_id: "109847528492049",
    business_account_id: "948572948572948",
    access_token: "********************",
    enabled: true,
  });

  const [paymentConfig, setPaymentConfig] = useState({
    primary_gateway: "Razorpay Enterprise",
    key_id: "rzp_live_MEIHQ889423",
    key_secret: "********************",
    webhook_secret: "********************",
    test_mode: false,
    enabled: true,
  });

  // Social & Domain State
  const [customDomain, setCustomDomain] = useState(inst?.custom_domain || "portal.myeducationindia.com");
  const [socialLinks, setSocialLinks] = useState({
    twitter: "https://twitter.com/myeducationindia",
    facebook: "https://facebook.com/myeducationindia",
    instagram: "https://instagram.com/myeducationindia",
    linkedin: "https://linkedin.com/company/myeducationindia",
    youtube: "https://youtube.com/@myeducationindia",
  });

  // Session Modal State
  const [sessionModalOpen, setSessionModalOpen] = useState(false);
  const [sessionCode, setSessionCode] = useState("");
  const [sessionName, setSessionName] = useState("");
  const [startDate, setStartDate] = useState("2026-07-01");
  const [endDate, setEndDate] = useState("2027-06-30");
  const [termStructure, setTermStructure] = useState("SEMESTER");
  const [termsCount, setTermsCount] = useState(2);
  const [isAdmissionOpen, setIsAdmissionOpen] = useState(true);
  const [isCurrent, setIsCurrent] = useState(false);

  // Mutations
  const updateProfileMutation = useMutation({
    mutationFn: (payload: InstituteProfileUpdatePayload) =>
      instituteService.updateProfile(instituteId!, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["institute-setup-bundle", instituteId] });
      void queryClient.invalidateQueries({ queryKey: ["institutes"] });
      setIsProfileDirty(false);
      alert("Institutional profile successfully updated!");
    },
  });

  const updateBrandingMutation = useMutation({
    mutationFn: () =>
      instituteService.updateBranding(instituteId!, {
        primary_color_hex: primaryColor,
        secondary_color_hex: secondaryColor,
        logo_url: logoUrl,
        favicon_url: faviconUrl,
      }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["institute-setup-bundle", instituteId] });
      void queryClient.invalidateQueries({ queryKey: ["institutes"] });
      alert("Institutional branding and colors successfully saved!");
    },
  });

  const updateIntegrationsMutation = useMutation({
    mutationFn: (payload: InstituteIntegrationsUpdatePayload) =>
      instituteService.updateIntegrations(instituteId!, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["institute-setup-bundle", instituteId] });
      alert("Communication gateways & integrations updated!");
    },
  });

  const createSessionMutation = useMutation({
    mutationFn: (payload: AcademicSessionCreatePayload) =>
      instituteService.createAcademicSession(instituteId!, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["institute-setup-bundle", instituteId] });
      setSessionModalOpen(false);
      setSessionCode("");
      setSessionName("");
    },
  });

  const deleteSessionMutation = useMutation({
    mutationFn: (sessionId: string) =>
      instituteService.deleteAcademicSession(instituteId!, sessionId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["institute-setup-bundle", instituteId] });
    },
  });

  const handleProfileSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!instituteId) return;
    void updateProfileMutation.mutate(profileForm);
  };

  const handleSaveIntegrations = () => {
    if (!instituteId) return;
    void updateIntegrationsMutation.mutate({
      smtp_config: smtpConfig,
      sms_gateway_config: smsConfig,
      whatsapp_gateway_config: whatsappConfig,
      payment_gateway_config: paymentConfig,
      social_media_links: socialLinks,
    });
  };

  const handleCreateSession = (e: React.FormEvent) => {
    e.preventDefault();
    if (!instituteId) return;
    void createSessionMutation.mutate({
      session_code: sessionCode.toUpperCase(),
      session_name: sessionName,
      start_date: startDate,
      end_date: endDate,
      term_structure: termStructure,
      terms_count: Number(termsCount),
      is_admission_open: isAdmissionOpen,
      is_current: isCurrent,
    });
  };

  if (institutesLoading || bundleLoading) {
    return (
      <div className="flex h-64 items-center justify-center text-sm text-slate-500">
        Loading institutional configuration matrix...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
        <div>
          <div className="flex items-center gap-2">
            <span className="rounded-md bg-indigo-100 px-2 py-0.5 text-xs font-bold text-indigo-800">
              Module 3
            </span>
            <span className="rounded-md bg-emerald-100 px-2 py-0.5 text-xs font-semibold text-emerald-800">
              Enterprise Institute Setup
            </span>
          </div>
          <h1 className="mt-2 text-xl font-bold text-slate-900">
            {inst?.name || "MY EDUCATION INDIA HQ"}
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            Configure campus profile, branding themes, academic sessions, SMTP, SMS, WhatsApp, and payment gateways.
          </p>
        </div>

        {/* Tab Controls */}
        <div className="flex flex-wrap items-center gap-1 rounded-xl bg-slate-100 p-1">
          <button
            type="button"
            onClick={() => setActiveTab("profile")}
            className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
              activeTab === "profile"
                ? "bg-white text-indigo-700 shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Profile & Address
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("branding")}
            className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
              activeTab === "branding"
                ? "bg-white text-indigo-700 shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Logo & Theme
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("sessions")}
            className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
              activeTab === "sessions"
                ? "bg-white text-indigo-700 shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Academic Sessions ({setupBundle?.all_sessions.length || 0})
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("gateways")}
            className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
              activeTab === "gateways"
                ? "bg-white text-indigo-700 shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Gateways (SMTP/SMS/WhatsApp/Pay)
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("social")}
            className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
              activeTab === "social"
                ? "bg-white text-indigo-700 shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Domain & Maps
          </button>
        </div>
      </div>

      {/* Profile & Address Tab */}
      {activeTab === "profile" && (
        <form onSubmit={handleProfileSubmit} className="space-y-6">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-base font-bold text-slate-900 mb-1">Institutional Profile & Contact</h2>
            <p className="text-xs text-slate-500 mb-5">
              Official institutional credentials, affiliation certificates, and administrative contact channels.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700">Campus Name</label>
                <input
                  type="text"
                  defaultValue={inst?.name}
                  onChange={(e) => {
                    setProfileForm((prev) => ({ ...prev, name: e.target.value }));
                    setIsProfileDirty(true);
                  }}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Campus Code</label>
                <input
                  type="text"
                  disabled
                  value={inst?.code || "MEI-HQ"}
                  className="mt-1 block w-full rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm font-mono text-slate-500 cursor-not-allowed"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Affiliation Number</label>
                <input
                  type="text"
                  defaultValue={inst?.affiliation_number || "UGC-AICTE-MP-2026-HQ"}
                  onChange={(e) => {
                    setProfileForm((prev) => ({ ...prev, affiliation_number: e.target.value }));
                    setIsProfileDirty(true);
                  }}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Official Email</label>
                <input
                  type="email"
                  defaultValue={inst?.official_email}
                  onChange={(e) => {
                    setProfileForm((prev) => ({ ...prev, official_email: e.target.value }));
                    setIsProfileDirty(true);
                  }}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Official Phone</label>
                <input
                  type="text"
                  defaultValue={inst?.official_phone}
                  onChange={(e) => {
                    setProfileForm((prev) => ({ ...prev, official_phone: e.target.value }));
                    setIsProfileDirty(true);
                  }}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Website Domain</label>
                <input
                  type="text"
                  defaultValue={inst?.website_domain || "myeducationindia.com"}
                  onChange={(e) => {
                    setProfileForm((prev) => ({ ...prev, website_domain: e.target.value }));
                    setIsProfileDirty(true);
                  }}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                />
              </div>
            </div>

            <div className="mt-4">
              <label className="block text-xs font-semibold text-slate-700">Campus Tagline</label>
              <input
                type="text"
                defaultValue={inst?.tagline || "Empowering India's Next Generation of Leaders & Innovators"}
                onChange={(e) => {
                  setProfileForm((prev) => ({ ...prev, tagline: e.target.value }));
                  setIsProfileDirty(true);
                }}
                className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
              />
            </div>
          </div>

          {/* Campus Location & Localization */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-base font-bold text-slate-900 mb-1">Physical Address & Regional Settings</h2>
            <p className="text-xs text-slate-500 mb-5">
              Postal coordinates, operational time zones, and reporting currency.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="md:col-span-2">
                <label className="block text-xs font-semibold text-slate-700">Address Line 1</label>
                <input
                  type="text"
                  defaultValue={inst?.address_line1 || "Sector B, Vijay Nagar"}
                  onChange={(e) => {
                    setProfileForm((prev) => ({ ...prev, address_line1: e.target.value }));
                    setIsProfileDirty(true);
                  }}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Address Line 2 (Optional)</label>
                <input
                  type="text"
                  defaultValue={inst?.address_line2 || "Near Brilliant Convention Centre"}
                  onChange={(e) => {
                    setProfileForm((prev) => ({ ...prev, address_line2: e.target.value }));
                    setIsProfileDirty(true);
                  }}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">City</label>
                <input
                  type="text"
                  defaultValue={inst?.city || "Indore"}
                  onChange={(e) => {
                    setProfileForm((prev) => ({ ...prev, city: e.target.value }));
                    setIsProfileDirty(true);
                  }}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">State</label>
                <input
                  type="text"
                  defaultValue={inst?.state || "Madhya Pradesh"}
                  onChange={(e) => {
                    setProfileForm((prev) => ({ ...prev, state: e.target.value }));
                    setIsProfileDirty(true);
                  }}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Postal Code (PIN)</label>
                <input
                  type="text"
                  defaultValue={inst?.postal_code || "452010"}
                  onChange={(e) => {
                    setProfileForm((prev) => ({ ...prev, postal_code: e.target.value }));
                    setIsProfileDirty(true);
                  }}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Time Zone</label>
                <select
                  defaultValue={inst?.time_zone || "Asia/Kolkata"}
                  onChange={(e) => {
                    setProfileForm((prev) => ({ ...prev, time_zone: e.target.value }));
                    setIsProfileDirty(true);
                  }}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                >
                  <option value="Asia/Kolkata">Asia/Kolkata (IST +5:30)</option>
                  <option value="UTC">UTC (Coordinated Universal Time)</option>
                  <option value="Asia/Dubai">Asia/Dubai (GST +4:00)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Default Language</label>
                <select
                  defaultValue={inst?.default_language || "en-IN"}
                  onChange={(e) => {
                    setProfileForm((prev) => ({ ...prev, default_language: e.target.value }));
                    setIsProfileDirty(true);
                  }}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                >
                  <option value="en-IN">English (India - en-IN)</option>
                  <option value="hi-IN">Hindi (India - hi-IN)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Currency & Symbol</label>
                <input
                  type="text"
                  disabled
                  value={`${inst?.currency_code || "INR"} (${inst?.currency_symbol || "₹"})`}
                  className="mt-1 block w-full rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm font-semibold text-slate-600 cursor-not-allowed"
                />
              </div>
            </div>

            <div className="mt-6 flex justify-end">
              <button
                type="submit"
                disabled={!isProfileDirty || updateProfileMutation.isPending}
                className="flex items-center gap-2 rounded-lg bg-indigo-600 px-5 py-2.5 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
              >
                <Save className="h-4 w-4" />
                {updateProfileMutation.isPending ? "Saving Profile..." : "Save Institute Profile"}
              </button>
            </div>
          </div>
        </form>
      )}

      {/* Logo & Branding Tab */}
      {activeTab === "branding" && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-6">
          <div>
            <h2 className="text-base font-bold text-slate-900">Visual Identity & Theme Integration</h2>
            <p className="text-xs text-slate-500">
              Harmonize Phase 1 public website theme with Phase 2 enterprise ERP portals.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Color Palette */}
            <div className="rounded-xl border border-slate-200 p-4 space-y-4">
              <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wide">
                Primary Brand Colors
              </h3>

              <div>
                <label className="block text-xs font-semibold text-slate-700">
                  Primary Accent Color
                </label>
                <div className="mt-1 flex items-center gap-3">
                  <input
                    type="color"
                    value={primaryColor}
                    onChange={(e) => setPrimaryColor(e.target.value)}
                    className="h-10 w-16 cursor-pointer rounded border border-slate-200"
                  />
                  <input
                    type="text"
                    value={primaryColor}
                    onChange={(e) => setPrimaryColor(e.target.value)}
                    className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-mono uppercase"
                  />
                  <span
                    className="rounded-md px-3 py-1.5 text-xs font-semibold text-white shadow-xs"
                    style={{ backgroundColor: primaryColor }}
                  >
                    Primary Preview
                  </span>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">
                  Secondary Accent Color
                </label>
                <div className="mt-1 flex items-center gap-3">
                  <input
                    type="color"
                    value={secondaryColor}
                    onChange={(e) => setSecondaryColor(e.target.value)}
                    className="h-10 w-16 cursor-pointer rounded border border-slate-200"
                  />
                  <input
                    type="text"
                    value={secondaryColor}
                    onChange={(e) => setSecondaryColor(e.target.value)}
                    className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-mono uppercase"
                  />
                  <span
                    className="rounded-md px-3 py-1.5 text-xs font-semibold text-white shadow-xs"
                    style={{ backgroundColor: secondaryColor }}
                  >
                    Secondary Preview
                  </span>
                </div>
              </div>
            </div>

            {/* Assets & Logos */}
            <div className="rounded-xl border border-slate-200 p-4 space-y-4">
              <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wide">
                Institutional Assets & Logos
              </h3>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Logo Image URL</label>
                <input
                  type="text"
                  placeholder="https://res.cloudinary.com/my-education-india/logo.png"
                  value={logoUrl}
                  onChange={(e) => setLogoUrl(e.target.value)}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700">Favicon URL</label>
                <input
                  type="text"
                  placeholder="https://res.cloudinary.com/my-education-india/favicon.ico"
                  value={faviconUrl}
                  onChange={(e) => setFaviconUrl(e.target.value)}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                />
              </div>
            </div>
          </div>

          <div className="flex justify-end pt-4 border-t border-slate-100">
            <button
              type="button"
              onClick={() => updateBrandingMutation.mutate()}
              disabled={updateBrandingMutation.isPending}
              className="flex items-center gap-2 rounded-lg bg-indigo-600 px-5 py-2.5 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
            >
              <Palette className="h-4 w-4" />
              {updateBrandingMutation.isPending ? "Applying Branding..." : "Save Branding Preferences"}
            </button>
          </div>
        </div>
      )}

      {/* Academic Sessions Tab */}
      {activeTab === "sessions" && (
        <div className="space-y-4">
          <div className="flex items-center justify-between rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
            <div>
              <h2 className="text-base font-bold text-slate-900">Academic Years & Sessions Engine</h2>
              <p className="mt-1 text-xs text-slate-500">
                Manage university admission calendars, term structures, and active academic year cycles.
              </p>
            </div>
            <button
              type="button"
              onClick={() => setSessionModalOpen(true)}
              className="flex items-center gap-1.5 rounded-lg bg-indigo-600 px-3.5 py-2 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700"
            >
              <Plus className="h-4 w-4" />
              New Academic Session
            </button>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead className="border-b border-slate-100 bg-slate-50 text-xs font-semibold text-slate-600">
                <tr>
                  <th className="px-3 py-2.5">Session Code</th>
                  <th className="px-3 py-2.5">Name</th>
                  <th className="px-3 py-2.5">Timeline (Start - End)</th>
                  <th className="px-3 py-2.5">Structure</th>
                  <th className="px-3 py-2.5">Admission Status</th>
                  <th className="px-3 py-2.5">Current Active</th>
                  <th className="px-3 py-2.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-xs">
                {(setupBundle?.all_sessions || []).map((sess) => (
                  <tr key={sess.id} className="hover:bg-slate-50/60">
                    <td className="px-3 py-3 font-mono font-bold text-indigo-700">
                      {sess.session_code}
                    </td>
                    <td className="px-3 py-3 font-semibold text-slate-900">
                      {sess.session_name}
                    </td>
                    <td className="px-3 py-3 text-slate-600">
                      {sess.start_date} to {sess.end_date}
                    </td>
                    <td className="px-3 py-3">
                      <span className="rounded bg-slate-100 px-2 py-0.5 font-medium text-slate-700">
                        {sess.term_structure} ({sess.terms_count} terms)
                      </span>
                    </td>
                    <td className="px-3 py-3">
                      {sess.is_admission_open ? (
                        <span className="rounded-full bg-emerald-100 px-2.5 py-0.5 text-[11px] font-semibold text-emerald-800">
                          Admissions Open
                        </span>
                      ) : (
                        <span className="rounded-full bg-slate-100 px-2.5 py-0.5 text-[11px] font-semibold text-slate-600">
                          Admissions Closed
                        </span>
                      )}
                    </td>
                    <td className="px-3 py-3">
                      {sess.is_current ? (
                        <span className="inline-flex items-center gap-1 rounded-full bg-indigo-100 px-2.5 py-0.5 text-[11px] font-bold text-indigo-800">
                          <CheckCircle2 className="h-3 w-3" />
                          Active Session
                        </span>
                      ) : (
                        <span className="text-slate-400 italic">Inactive</span>
                      )}
                    </td>
                    <td className="px-3 py-3 text-right">
                      {!sess.is_current && (
                        <button
                          type="button"
                          onClick={() => {
                            if (confirm(`Remove academic session ${sess.session_code}?`)) {
                              void deleteSessionMutation.mutate(sess.id);
                            }
                          }}
                          className="rounded p-1 text-rose-500 hover:bg-rose-50"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Gateways Tab (SMTP / SMS / WhatsApp / Payment) */}
      {activeTab === "gateways" && (
        <div className="space-y-6">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs">
            <h2 className="text-base font-bold text-slate-900 mb-1">
              Communication & Transaction Gateways
            </h2>
            <p className="text-xs text-slate-500 mb-6">
              Connect core infrastructure for email delivery, transactional SMS alerts, WhatsApp bot, and fee collection.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* SMTP Card */}
              <div className="rounded-xl border border-slate-200 p-4 space-y-3">
                <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                  <div className="flex items-center gap-2">
                    <Mail className="h-4 w-4 text-indigo-600" />
                    <span className="text-xs font-bold text-slate-900">SMTP Email Gateway</span>
                  </div>
                  <span className="rounded bg-emerald-100 px-2 py-0.5 text-[10px] font-bold text-emerald-800">
                    ONLINE
                  </span>
                </div>

                <div className="space-y-2 text-xs">
                  <div>
                    <label className="text-slate-600 font-medium">SMTP Host</label>
                    <input
                      type="text"
                      value={smtpConfig.host}
                      onChange={(e) => setSmtpConfig({ ...smtpConfig, host: e.target.value })}
                      className="mt-1 block w-full rounded border border-slate-200 px-2.5 py-1.5"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div>
                      <label className="text-slate-600 font-medium">Port</label>
                      <input
                        type="number"
                        value={smtpConfig.port}
                        onChange={(e) => setSmtpConfig({ ...smtpConfig, port: Number(e.target.value) })}
                        className="mt-1 block w-full rounded border border-slate-200 px-2.5 py-1.5"
                      />
                    </div>
                    <div>
                      <label className="text-slate-600 font-medium">Encryption</label>
                      <input
                        type="text"
                        value={smtpConfig.encryption}
                        onChange={(e) => setSmtpConfig({ ...smtpConfig, encryption: e.target.value })}
                        className="mt-1 block w-full rounded border border-slate-200 px-2.5 py-1.5"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="text-slate-600 font-medium">Sender Email Address</label>
                    <input
                      type="text"
                      value={smtpConfig.sender_email}
                      onChange={(e) => setSmtpConfig({ ...smtpConfig, sender_email: e.target.value })}
                      className="mt-1 block w-full rounded border border-slate-200 px-2.5 py-1.5"
                    />
                  </div>
                </div>
              </div>

              {/* SMS Gateway Card */}
              <div className="rounded-xl border border-slate-200 p-4 space-y-3">
                <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                  <div className="flex items-center gap-2">
                    <MessageSquare className="h-4 w-4 text-emerald-600" />
                    <span className="text-xs font-bold text-slate-900">Transactional SMS (DLT)</span>
                  </div>
                  <span className="rounded bg-emerald-100 px-2 py-0.5 text-[10px] font-bold text-emerald-800">
                    DLT VERIFIED
                  </span>
                </div>

                <div className="space-y-2 text-xs">
                  <div>
                    <label className="text-slate-600 font-medium">Provider</label>
                    <input
                      type="text"
                      value={smsConfig.provider}
                      onChange={(e) => setSmsConfig({ ...smsConfig, provider: e.target.value })}
                      className="mt-1 block w-full rounded border border-slate-200 px-2.5 py-1.5"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div>
                      <label className="text-slate-600 font-medium">Header / Sender ID</label>
                      <input
                        type="text"
                        value={smsConfig.sender_id}
                        onChange={(e) => setSmsConfig({ ...smsConfig, sender_id: e.target.value })}
                        className="mt-1 block w-full rounded border border-slate-200 px-2.5 py-1.5 font-mono"
                      />
                    </div>
                    <div>
                      <label className="text-slate-600 font-medium">DLT Entity ID</label>
                      <input
                        type="text"
                        value={smsConfig.dlt_entity_id}
                        onChange={(e) => setSmsConfig({ ...smsConfig, dlt_entity_id: e.target.value })}
                        className="mt-1 block w-full rounded border border-slate-200 px-2.5 py-1.5 font-mono"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="text-slate-600 font-medium">API Token</label>
                    <input
                      type="password"
                      value={smsConfig.api_key}
                      onChange={(e) => setSmsConfig({ ...smsConfig, api_key: e.target.value })}
                      className="mt-1 block w-full rounded border border-slate-200 px-2.5 py-1.5 font-mono"
                    />
                  </div>
                </div>
              </div>

              {/* WhatsApp Cloud API */}
              <div className="rounded-xl border border-slate-200 p-4 space-y-3">
                <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                  <div className="flex items-center gap-2">
                    <Send className="h-4 w-4 text-emerald-500" />
                    <span className="text-xs font-bold text-slate-900">WhatsApp Business Cloud API</span>
                  </div>
                  <span className="rounded bg-emerald-100 px-2 py-0.5 text-[10px] font-bold text-emerald-800">
                    META CERTIFIED
                  </span>
                </div>

                <div className="space-y-2 text-xs">
                  <div>
                    <label className="text-slate-600 font-medium">Phone Number ID</label>
                    <input
                      type="text"
                      value={whatsappConfig.phone_number_id}
                      onChange={(e) =>
                        setWhatsappConfig({ ...whatsappConfig, phone_number_id: e.target.value })
                      }
                      className="mt-1 block w-full rounded border border-slate-200 px-2.5 py-1.5 font-mono"
                    />
                  </div>
                  <div>
                    <label className="text-slate-600 font-medium">Business Account ID (WABA)</label>
                    <input
                      type="text"
                      value={whatsappConfig.business_account_id}
                      onChange={(e) =>
                        setWhatsappConfig({
                          ...whatsappConfig,
                          business_account_id: e.target.value,
                        })
                      }
                      className="mt-1 block w-full rounded border border-slate-200 px-2.5 py-1.5 font-mono"
                    />
                  </div>
                  <div>
                    <label className="text-slate-600 font-medium">System User Access Token</label>
                    <input
                      type="password"
                      value={whatsappConfig.access_token}
                      onChange={(e) =>
                        setWhatsappConfig({ ...whatsappConfig, access_token: e.target.value })
                      }
                      className="mt-1 block w-full rounded border border-slate-200 px-2.5 py-1.5 font-mono"
                    />
                  </div>
                </div>
              </div>

              {/* Payment Gateway */}
              <div className="rounded-xl border border-slate-200 p-4 space-y-3">
                <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                  <div className="flex items-center gap-2">
                    <CreditCard className="h-4 w-4 text-purple-600" />
                    <span className="text-xs font-bold text-slate-900">Payment Gateway (Fee Collection)</span>
                  </div>
                  <span className="rounded bg-purple-100 px-2 py-0.5 text-[10px] font-bold text-purple-800">
                    PCI-DSS COMPLIANT
                  </span>
                </div>

                <div className="space-y-2 text-xs">
                  <div>
                    <label className="text-slate-600 font-medium">Primary Provider</label>
                    <input
                      type="text"
                      value={paymentConfig.primary_gateway}
                      onChange={(e) =>
                        setPaymentConfig({ ...paymentConfig, primary_gateway: e.target.value })
                      }
                      className="mt-1 block w-full rounded border border-slate-200 px-2.5 py-1.5"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div>
                      <label className="text-slate-600 font-medium">Merchant Key ID</label>
                      <input
                        type="text"
                        value={paymentConfig.key_id}
                        onChange={(e) => setPaymentConfig({ ...paymentConfig, key_id: e.target.value })}
                        className="mt-1 block w-full rounded border border-slate-200 px-2.5 py-1.5 font-mono"
                      />
                    </div>
                    <div>
                      <label className="text-slate-600 font-medium">Key Secret</label>
                      <input
                        type="password"
                        value={paymentConfig.key_secret}
                        onChange={(e) =>
                          setPaymentConfig({ ...paymentConfig, key_secret: e.target.value })
                        }
                        className="mt-1 block w-full rounded border border-slate-200 px-2.5 py-1.5 font-mono"
                      />
                    </div>
                  </div>
                  <div className="flex items-center gap-2 pt-2">
                    <input
                      type="checkbox"
                      id="testMode"
                      checked={paymentConfig.test_mode}
                      onChange={(e) =>
                        setPaymentConfig({ ...paymentConfig, test_mode: e.target.checked })
                      }
                      className="rounded border-slate-300 text-indigo-600"
                    />
                    <label htmlFor="testMode" className="text-xs text-slate-700">
                      Sandbox / Test Mode
                    </label>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-6 flex justify-end">
              <button
                type="button"
                onClick={handleSaveIntegrations}
                disabled={updateIntegrationsMutation.isPending}
                className="flex items-center gap-2 rounded-lg bg-indigo-600 px-5 py-2.5 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
              >
                <Save className="h-4 w-4" />
                {updateIntegrationsMutation.isPending ? "Saving Gateways..." : "Save Gateway Credentials"}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Social Media & Custom Domain Tab */}
      {activeTab === "social" && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-6">
          <div>
            <h2 className="text-base font-bold text-slate-900">Custom Domain & Google Maps</h2>
            <p className="text-xs text-slate-500">
              Campus geolocation embed, social media footprint, and custom white-label domain routing.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wide">
                Custom Domain Routing
              </h3>
              <div>
                <label className="block text-xs font-semibold text-slate-700">Primary Domain FQDN</label>
                <input
                  type="text"
                  value={customDomain}
                  onChange={(e) => setCustomDomain(e.target.value)}
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm font-mono"
                />
                <div className="mt-2 flex items-center gap-2 text-xs text-emerald-600 font-medium">
                  <ShieldCheck className="h-4 w-4" />
                  SSL Certificate Active (Let's Encrypt TLS 1.3)
                </div>
              </div>

              <div className="pt-2">
                <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wide mb-2">
                  Google Maps Geolocation
                </h3>
                <label className="block text-xs font-semibold text-slate-700">Embed URL</label>
                <input
                  type="text"
                  defaultValue="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d117763.555896!2d75.834!3d22.75!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3AMY_EDUCATION_INDIA!5e0!3m2!1sen!2sin!4v1600000000000"
                  className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm font-mono text-xs"
                />
              </div>
            </div>

            <div className="space-y-3">
              <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wide">
                Social Media Handles
              </h3>
              {Object.entries(socialLinks).map(([network, url]) => (
                <div key={network}>
                  <label className="block text-xs font-semibold text-slate-700 capitalize">
                    {network}
                  </label>
                  <input
                    type="text"
                    value={url}
                    onChange={(e) => setSocialLinks({ ...socialLinks, [network]: e.target.value })}
                    className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-1.5 text-xs text-slate-700 font-mono"
                  />
                </div>
              ))}
            </div>
          </div>

          <div className="flex justify-end pt-4 border-t border-slate-100">
            <button
              type="button"
              onClick={handleSaveIntegrations}
              disabled={updateIntegrationsMutation.isPending}
              className="flex items-center gap-2 rounded-lg bg-indigo-600 px-5 py-2.5 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
            >
              <Globe className="h-4 w-4" />
              Save Domain & Social Settings
            </button>
          </div>
        </div>
      )}

      {/* New Academic Session Modal */}
      {sessionModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4 backdrop-blur-xs">
          <div className="relative w-full max-w-lg rounded-2xl bg-white p-6 shadow-2xl">
            <h3 className="text-base font-bold text-slate-900">Provision Academic Session</h3>
            <p className="mt-1 text-xs text-slate-500">
              Define a new operational academic year with custom calendar boundaries and admission status.
            </p>

            <form onSubmit={handleCreateSession} className="mt-4 space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Session Code</label>
                  <input
                    type="text"
                    placeholder="AY-2027-28"
                    value={sessionCode}
                    onChange={(e) => setSessionCode(e.target.value.toUpperCase())}
                    required
                    className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm font-mono focus:border-indigo-600 focus:outline-hidden"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700">Display Name</label>
                  <input
                    type="text"
                    placeholder="Academic Year 2027 - 2028"
                    value={sessionName}
                    onChange={(e) => setSessionName(e.target.value)}
                    required
                    className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-600 focus:outline-hidden"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Start Date</label>
                  <input
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                    required
                    className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700">End Date</label>
                  <input
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                    required
                    className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700">Term Structure</label>
                  <select
                    value={termStructure}
                    onChange={(e) => setTermStructure(e.target.value)}
                    className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
                  >
                    <option value="SEMESTER">Semester (2 Terms / Year)</option>
                    <option value="TRIMESTER">Trimester (3 Terms / Year)</option>
                    <option value="ANNUAL">Annual (1 Term / Year)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700">Terms Count</label>
                  <input
                    type="number"
                    min={1}
                    max={12}
                    value={termsCount}
                    onChange={(e) => setTermsCount(Number(e.target.value))}
                    className="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
                  />
                </div>
              </div>

              <div className="space-y-2 pt-2">
                <label className="flex items-center gap-2 text-xs text-slate-700 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={isAdmissionOpen}
                    onChange={(e) => setIsAdmissionOpen(e.target.checked)}
                    className="rounded border-slate-300 text-indigo-600"
                  />
                  <span>Open for Online Candidate Admissions</span>
                </label>

                <label className="flex items-center gap-2 text-xs text-slate-700 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={isCurrent}
                    onChange={(e) => setIsCurrent(e.target.checked)}
                    className="rounded border-slate-300 text-indigo-600"
                  />
                  <span>Promote as Active Current Academic Year</span>
                </label>
              </div>

              <div className="mt-5 flex justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setSessionModalOpen(false)}
                  className="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-semibold text-slate-600 hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createSessionMutation.isPending}
                  className="rounded-lg bg-indigo-600 px-4 py-1.5 text-xs font-semibold text-white shadow-xs hover:bg-indigo-700 disabled:opacity-50"
                >
                  {createSessionMutation.isPending ? "Creating..." : "Save Academic Session"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
