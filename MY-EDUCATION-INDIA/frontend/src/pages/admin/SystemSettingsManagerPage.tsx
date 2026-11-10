import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Settings,
  Database,
  Calendar,
  Clock,
  Hash,
  FileCode,
  Plus,
  Trash2,
  Edit2,
  CheckCircle2,
  XCircle,
  RefreshCw,
  Eye,
  Sliders,
  Sparkles,
  ChevronRight,
  Printer,
  Copy,
  BookOpen,
  CalendarDays,
  Award,
  IdCard,
} from "lucide-react";
import { systemSettingsService } from "@/services/systemSettingsService";
import {
  CampusHoliday,
  DocumentTemplate,
  MasterDataCategorySummary,
  MasterDataEntry,
  NumberingRule,
  WorkingDaysConfig,
} from "@/types/systemSettings.types";

type ActiveTab = "OVERVIEW" | "MASTER_DATA" | "HOLIDAYS_WORKING_DAYS" | "NUMBERING_RULES" | "TEMPLATES";

export const SystemSettingsManagerPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<ActiveTab>("OVERVIEW");

  // Master Data state
  const [selectedCategory, setSelectedCategory] = useState<string>("GENDER");
  const [showItemModal, setShowItemModal] = useState(false);
  const [editingItem, setEditingItem] = useState<MasterDataEntry | null>(null);
  const [itemForm, setItemForm] = useState({ item_code: "", item_label: "", item_value: "", display_order: 1, is_active: true });

  // Holiday state
  const [showHolidayModal, setShowHolidayModal] = useState(false);
  const [holidayForm, setHolidayForm] = useState({ name: "", holiday_date: "", holiday_type: "GAZETTED", description: "", is_optional: false });

  // Working day edit state
  const [editingDay, setEditingDay] = useState<WorkingDaysConfig | null>(null);

  // Numbering rules state
  const [editingRule, setEditingRule] = useState<NumberingRule | null>(null);
  const [ruleForm, setRuleForm] = useState({ prefix: "", suffix: "", digits_padding: 4, format_pattern: "", reset_frequency: "ANNUAL" });
  const [generatedSample, setGeneratedSample] = useState<{ entityType: string; number: string } | null>(null);

  // Document templates state
  const [selectedTemplateCode, setSelectedTemplateCode] = useState<string>("TRANSFER_CERTIFICATE");
  const [renderedPreview, setRenderedPreview] = useState<string | null>(null);
  const [templateHtml, setTemplateHtml] = useState<string>("");
  const [isEditingTemplate, setIsEditingTemplate] = useState(false);

  // Queries
  const { data: summary, isLoading: summaryLoading } = useQuery({
    queryKey: ["systemSettingsSummary"],
    queryFn: () => systemSettingsService.getSummary(),
  });

  const { data: categories = [] } = useQuery({
    queryKey: ["masterDataCategories"],
    queryFn: () => systemSettingsService.listCategories(),
  });

  const { data: items = [], refetch: refetchItems } = useQuery({
    queryKey: ["masterDataItems", selectedCategory],
    queryFn: () => systemSettingsService.listItems(selectedCategory),
    enabled: !!selectedCategory,
  });

  const { data: holidays = [], refetch: refetchHolidays } = useQuery({
    queryKey: ["campusHolidays"],
    queryFn: () => systemSettingsService.listHolidays(),
  });

  const { data: workingDays = [], refetch: refetchWorkingDays } = useQuery({
    queryKey: ["workingDaysConfig"],
    queryFn: () => systemSettingsService.getWorkingDays(),
  });

  const { data: numberingRules = [], refetch: refetchRules } = useQuery({
    queryKey: ["numberingRules"],
    queryFn: () => systemSettingsService.listNumberingRules(),
  });

  const { data: templates = [], refetch: refetchTemplates } = useQuery({
    queryKey: ["documentTemplates"],
    queryFn: () => systemSettingsService.listDocumentTemplates(),
  });

  // Mutations
  const createItemMutation = useMutation({
    mutationFn: (payload: any) => systemSettingsService.createItem(payload),
    onSuccess: () => {
      refetchItems();
      queryClient.invalidateQueries({ queryKey: ["masterDataCategories"] });
      queryClient.invalidateQueries({ queryKey: ["systemSettingsSummary"] });
      setShowItemModal(false);
      setItemForm({ item_code: "", item_label: "", item_value: "", display_order: 1, is_active: true });
    },
  });

  const updateItemMutation = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: any }) => systemSettingsService.updateItem(id, payload),
    onSuccess: () => {
      refetchItems();
      setShowItemModal(false);
      setEditingItem(null);
    },
  });

  const deleteItemMutation = useMutation({
    mutationFn: (id: string) => systemSettingsService.deleteItem(id),
    onSuccess: () => {
      refetchItems();
      queryClient.invalidateQueries({ queryKey: ["masterDataCategories"] });
      queryClient.invalidateQueries({ queryKey: ["systemSettingsSummary"] });
    },
  });

  const createHolidayMutation = useMutation({
    mutationFn: (payload: any) => systemSettingsService.createHoliday(payload),
    onSuccess: () => {
      refetchHolidays();
      queryClient.invalidateQueries({ queryKey: ["systemSettingsSummary"] });
      setShowHolidayModal(false);
      setHolidayForm({ name: "", holiday_date: "", holiday_type: "GAZETTED", description: "", is_optional: false });
    },
  });

  const deleteHolidayMutation = useMutation({
    mutationFn: (id: string) => systemSettingsService.deleteHoliday(id),
    onSuccess: () => {
      refetchHolidays();
      queryClient.invalidateQueries({ queryKey: ["systemSettingsSummary"] });
    },
  });

  const updateWorkingDayMutation = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: any }) => systemSettingsService.updateWorkingDay(id, payload),
    onSuccess: () => {
      refetchWorkingDays();
      setEditingDay(null);
    },
  });

  const updateRuleMutation = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: any }) => systemSettingsService.updateNumberingRule(id, payload),
    onSuccess: () => {
      refetchRules();
      setEditingRule(null);
    },
  });

  const testSequenceMutation = useMutation({
    mutationFn: (entityType: string) => systemSettingsService.generateSequence(entityType, true),
    onSuccess: (data) => {
      setGeneratedSample({ entityType: data.entity_type, number: data.generated_number });
      refetchRules();
    },
  });

  const renderTemplateMutation = useMutation({
    mutationFn: ({ code, context }: { code: string; context: Record<string, any> }) =>
      systemSettingsService.renderTemplate(code, context),
    onSuccess: (data) => {
      setRenderedPreview(data.rendered_html);
    },
  });

  const updateTemplateMutation = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: any }) => systemSettingsService.updateDocumentTemplate(id, payload),
    onSuccess: () => {
      refetchTemplates();
      setIsEditingTemplate(false);
      alert("Document template saved successfully!");
    },
  });

  // Current active template
  const currentTemplate = templates.find((t) => t.template_code === selectedTemplateCode);

  const handleTestRender = () => {
    if (!currentTemplate) return;
    const sampleContext: Record<string, string> = {
      CERTIFICATE_NO: "MEI-TC-2026-0042",
      ISSUE_DATE: new Date().toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" }),
      STUDENT_NAME: "Aarav Sharma",
      FATHER_NAME: "Rajesh Sharma",
      MOTHER_NAME: "Sunita Sharma",
      ROLL_NO: "MEI-2026-CSE-0042",
      ADMISSION_DATE: "01-Jul-2023",
      LEAVING_DATE: "30-Apr-2026",
      PROGRAM_NAME: "B.Tech Computer Science & Engineering",
      DEPARTMENT_NAME: "School of Engineering & Technology",
      CONDUCT: "Exemplary",
      REASON_FOR_LEAVING: "Graduated with First Class Honors",
      SEMESTER: "VIII Semester",
      ACADEMIC_SESSION: "2026-2027",
      DATE_OF_BIRTH: "15-Aug-2004",
      PURPOSE: "Higher Studies & Visa Verification",
      BLOOD_GROUP: "O+",
      EMERGENCY_PHONE: "+91 98260 12345",
      VALID_TILL: "30-Jun-2027",
    };
    renderTemplateMutation.mutate({ code: currentTemplate.template_code, context: sampleContext });
  };

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white p-6 rounded-2xl shadow-xl">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-500/30 text-blue-200 border border-blue-400/30">
              Module 12 Enterprise Foundation
            </span>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/30 text-emerald-200 border border-emerald-400/30">
              MEI-HQ Autonomous Campus, Indore
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight">System Settings & Master Controls</h1>
          <p className="text-sm text-blue-200/80">
            Configure institutional taxonomies, gazetted holidays calendar, weekly working schedule, auto-numbering series rules, and official document generation templates.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => {
              refetchItems();
              refetchHolidays();
              refetchWorkingDays();
              refetchRules();
              refetchTemplates();
            }}
            className="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 text-white text-sm font-medium rounded-xl transition border border-white/10"
          >
            <RefreshCw className="w-4 h-4" /> Refresh All
          </button>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-gray-200 dark:border-gray-800 space-x-2 overflow-x-auto">
        {[
          { key: "OVERVIEW", label: "Overview & Telemetry", icon: Sliders },
          { key: "MASTER_DATA", label: "Master Data Dictionary", icon: Database },
          { key: "HOLIDAYS_WORKING_DAYS", label: "Holidays & Working Days", icon: CalendarDays },
          { key: "NUMBERING_RULES", label: "Auto-Numbering Series", icon: Hash },
          { key: "TEMPLATES", label: "Document Templates", icon: FileCode },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.key;
          return (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key as ActiveTab)}
              className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition whitespace-nowrap ${
                isActive
                  ? "border-blue-600 text-blue-600 dark:border-blue-400 dark:text-blue-400"
                  : "border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* TAB 1: OVERVIEW & TELEMETRY */}
      {activeTab === "OVERVIEW" && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-white dark:bg-gray-800 p-5 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm">
              <div className="flex items-center justify-between text-gray-500 dark:text-gray-400 text-xs font-semibold uppercase tracking-wider">
                <span>Master Taxonomies</span>
                <Database className="w-4 h-4 text-blue-500" />
              </div>
              <div className="mt-2 flex items-baseline gap-2">
                <span className="text-3xl font-extrabold text-gray-900 dark:text-white">
                  {summary?.master_data_items_count || 32}
                </span>
                <span className="text-xs text-gray-500">entries in {summary?.master_data_categories_count || 6} categories</span>
              </div>
              <p className="mt-2 text-xs text-gray-500">Genders, Blood Groups, Quotas, Salutations, Doc Types, Fee Heads</p>
            </div>

            <div className="bg-white dark:bg-gray-800 p-5 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm">
              <div className="flex items-center justify-between text-gray-500 dark:text-gray-400 text-xs font-semibold uppercase tracking-wider">
                <span>MP Gazetted Holidays</span>
                <Calendar className="w-4 h-4 text-emerald-500" />
              </div>
              <div className="mt-2 flex items-baseline gap-2">
                <span className="text-3xl font-extrabold text-gray-900 dark:text-white">
                  {summary?.holidays_count || 16}
                </span>
                <span className="text-xs text-gray-500">declared holidays (2026-27)</span>
              </div>
              <p className="mt-2 text-xs text-gray-500">Includes Rangpanchmi, Ambedkar Jayanti, Dussehra, Diwali</p>
            </div>

            <div className="bg-white dark:bg-gray-800 p-5 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm">
              <div className="flex items-center justify-between text-gray-500 dark:text-gray-400 text-xs font-semibold uppercase tracking-wider">
                <span>Numbering Rules</span>
                <Hash className="w-4 h-4 text-purple-500" />
              </div>
              <div className="mt-2 flex items-baseline gap-2">
                <span className="text-3xl font-extrabold text-gray-900 dark:text-white">
                  {summary?.numbering_rules_count || 5}
                </span>
                <span className="text-xs text-gray-500">auto-sequences</span>
              </div>
              <p className="mt-2 text-xs text-gray-500">Roll Numbers, Employee IDs, Invoices, Applications, Certs</p>
            </div>

            <div className="bg-white dark:bg-gray-800 p-5 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm">
              <div className="flex items-center justify-between text-gray-500 dark:text-gray-400 text-xs font-semibold uppercase tracking-wider">
                <span>Document Templates</span>
                <FileCode className="w-4 h-4 text-amber-500" />
              </div>
              <div className="mt-2 flex items-baseline gap-2">
                <span className="text-3xl font-extrabold text-gray-900 dark:text-white">
                  {summary?.document_templates_count || 3}
                </span>
                <span className="text-xs text-gray-500">ready-to-print formats</span>
              </div>
              <p className="mt-2 text-xs text-gray-500">Transfer Certificate, Bonafide, Smart ID Cards</p>
            </div>
          </div>

          {/* Regional & System Environment Telemetry */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm space-y-4">
            <h3 className="text-base font-bold text-gray-900 dark:text-white flex items-center gap-2">
              <Sliders className="w-5 h-5 text-blue-600" /> Regional & Autonomous Governance Settings
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="p-4 rounded-xl bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-800">
                <span className="text-xs font-semibold text-gray-500 uppercase">Campus Location & Jurisdiction</span>
                <p className="text-sm font-semibold text-gray-900 dark:text-white mt-1">Indore, Madhya Pradesh, India</p>
                <p className="text-xs text-gray-500 mt-1">Timezone: Asia/Kolkata (IST +05:30) | Locale: en-IN</p>
              </div>

              <div className="p-4 rounded-xl bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-800">
                <span className="text-xs font-semibold text-gray-500 uppercase">Active Academic Session</span>
                <p className="text-sm font-semibold text-blue-600 dark:text-blue-400 mt-1">2026-2027 (Undergraduate & Postgrad)</p>
                <p className="text-xs text-gray-500 mt-1">Term: Odd / Autumn Semester (Jul-Dec 2026)</p>
              </div>

              <div className="p-4 rounded-xl bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-800">
                <span className="text-xs font-semibold text-gray-500 uppercase">Institutional Code & Affiliation</span>
                <p className="text-sm font-semibold text-gray-900 dark:text-white mt-1">MEI-HQ (Flagship Autonomous Campus)</p>
                <p className="text-xs text-gray-500 mt-1">Affiliation: MP-IND-2026-88 | UGC Autonomous Tier-1</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: MASTER DATA DICTIONARY */}
      {activeTab === "MASTER_DATA" && (
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Categories Sidebar */}
          <div className="lg:col-span-1 space-y-2">
            <h3 className="text-xs font-bold uppercase tracking-wider text-gray-500 px-2">Taxonomy Categories</h3>
            <div className="space-y-1">
              {categories.map((cat) => (
                <button
                  key={cat.category_key}
                  onClick={() => setSelectedCategory(cat.category_key)}
                  className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-sm font-medium transition ${
                    selectedCategory === cat.category_key
                      ? "bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300 font-semibold"
                      : "text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800"
                  }`}
                >
                  <span>{cat.category_label}</span>
                  <span className="text-xs px-2 py-0.5 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
                    {cat.item_count}
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Items Table */}
          <div className="lg:col-span-3 bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 p-6 shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                  {categories.find((c) => c.category_key === selectedCategory)?.category_label || selectedCategory}
                </h3>
                <p className="text-xs text-gray-500">Key: {selectedCategory} | Total active items: {items.filter((i) => i.is_active).length}</p>
              </div>
              <button
                onClick={() => {
                  setEditingItem(null);
                  setItemForm({ item_code: "", item_label: "", item_value: "", display_order: items.length + 1, is_active: true });
                  setShowItemModal(true);
                }}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-xl shadow-sm transition"
              >
                <Plus className="w-3.5 h-3.5" /> Add Taxonomy Item
              </button>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-gray-50 dark:bg-gray-900/50 text-xs uppercase font-semibold text-gray-500 border-b border-gray-100 dark:border-gray-800">
                  <tr>
                    <th className="px-4 py-3">Order</th>
                    <th className="px-4 py-3">Item Code</th>
                    <th className="px-4 py-3">Item Label</th>
                    <th className="px-4 py-3">Value / Mapping</th>
                    <th className="px-4 py-3">Status</th>
                    <th className="px-4 py-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100 dark:divide-gray-800">
                  {items.map((item) => (
                    <tr key={item.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition">
                      <td className="px-4 py-3 font-mono text-xs text-gray-500">{item.display_order}</td>
                      <td className="px-4 py-3 font-mono text-xs font-semibold text-blue-600 dark:text-blue-400">{item.item_code}</td>
                      <td className="px-4 py-3 font-medium text-gray-900 dark:text-white">{item.item_label}</td>
                      <td className="px-4 py-3 text-xs text-gray-500">{item.item_value || "—"}</td>
                      <td className="px-4 py-3">
                        <span
                          className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                            item.is_active
                              ? "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400"
                              : "bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400"
                          }`}
                        >
                          {item.is_active ? "Active" : "Disabled"}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-right space-x-2">
                        <button
                          onClick={() => {
                            setEditingItem(item);
                            setItemForm({
                              item_code: item.item_code,
                              item_label: item.item_label,
                              item_value: item.item_value || "",
                              display_order: item.display_order,
                              is_active: item.is_active,
                            });
                            setShowItemModal(true);
                          }}
                          className="p-1 hover:text-blue-600 text-gray-400"
                        >
                          <Edit2 className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => {
                            if (confirm(`Delete "${item.item_label}"?`)) {
                              deleteItemMutation.mutate(item.id);
                            }
                          }}
                          className="p-1 hover:text-red-600 text-gray-400"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: HOLIDAYS & WORKING DAYS */}
      {activeTab === "HOLIDAYS_WORKING_DAYS" && (
        <div className="space-y-6">
          {/* Working Days Schedule */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-base font-bold text-gray-900 dark:text-white flex items-center gap-2">
                  <Clock className="w-5 h-5 text-indigo-600" /> Weekly Working Days & Lecture Timetable Schedule
                </h3>
                <p className="text-xs text-gray-500">Configure standard campus hours, teaching periods, and lunch breaks</p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {workingDays.map((wd) => (
                <div
                  key={wd.id}
                  className={`p-4 rounded-xl border transition ${
                    wd.is_working_day
                      ? "bg-blue-50/40 dark:bg-blue-900/10 border-blue-200 dark:border-blue-800"
                      : "bg-gray-50 dark:bg-gray-900/50 border-gray-200 dark:border-gray-800 opacity-75"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-sm text-gray-900 dark:text-white">{wd.day_name}</span>
                    <button
                      onClick={() =>
                        updateWorkingDayMutation.mutate({
                          id: wd.id,
                          payload: { is_working_day: !wd.is_working_day },
                        })
                      }
                      className={`text-xs px-2 py-0.5 rounded-full font-semibold ${
                        wd.is_working_day
                          ? "bg-blue-100 text-blue-700 dark:bg-blue-800 dark:text-blue-200"
                          : "bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-300"
                      }`}
                    >
                      {wd.is_working_day ? "Working" : "Closed"}
                    </button>
                  </div>
                  {wd.is_working_day ? (
                    <div className="mt-2 text-xs space-y-1 text-gray-600 dark:text-gray-300">
                      <div>Hours: <strong>{wd.start_time} - {wd.end_time}</strong></div>
                      <div>Periods: <strong>{wd.periods_count} Slots</strong></div>
                      {wd.lunch_break_start && (
                        <div>Lunch: <strong>{wd.lunch_break_start} - {wd.lunch_break_end}</strong></div>
                      )}
                    </div>
                  ) : (
                    <p className="mt-2 text-xs text-gray-400 italic">Campus closed (Weekly Off)</p>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Holidays Calendar */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-base font-bold text-gray-900 dark:text-white flex items-center gap-2">
                  <Calendar className="w-5 h-5 text-emerald-600" /> Madhya Pradesh & Indore Gazetted Holidays (2026-2027)
                </h3>
                <p className="text-xs text-gray-500">Official institutional holidays observed at MEI Flagship Campus</p>
              </div>
              <button
                onClick={() => setShowHolidayModal(true)}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-xl shadow-sm transition"
              >
                <Plus className="w-3.5 h-3.5" /> Declare Campus Holiday
              </button>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-gray-50 dark:bg-gray-900/50 text-xs uppercase font-semibold text-gray-500 border-b border-gray-100 dark:border-gray-800">
                  <tr>
                    <th className="px-4 py-3">Holiday Date</th>
                    <th className="px-4 py-3">Holiday Name</th>
                    <th className="px-4 py-3">Type</th>
                    <th className="px-4 py-3">Description</th>
                    <th className="px-4 py-3">Staff Optional</th>
                    <th className="px-4 py-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100 dark:divide-gray-800">
                  {holidays.map((hol) => (
                    <tr key={hol.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition">
                      <td className="px-4 py-3 font-semibold text-gray-900 dark:text-white">
                        {new Date(hol.holiday_date).toLocaleDateString("en-IN", {
                          day: "numeric",
                          month: "short",
                          year: "numeric",
                          weekday: "short",
                        })}
                      </td>
                      <td className="px-4 py-3 font-medium text-gray-900 dark:text-white">{hol.name}</td>
                      <td className="px-4 py-3">
                        <span
                          className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold ${
                            hol.holiday_type === "GAZETTED"
                              ? "bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300"
                              : hol.holiday_type === "RESTRICTED"
                              ? "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300"
                              : "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300"
                          }`}
                        >
                          {hol.holiday_type}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-xs text-gray-500">{hol.description || "—"}</td>
                      <td className="px-4 py-3">
                        {hol.is_optional ? (
                          <span className="text-amber-600 text-xs font-medium">Yes (Restricted)</span>
                        ) : (
                          <span className="text-emerald-600 text-xs font-medium">Mandatory</span>
                        )}
                      </td>
                      <td className="px-4 py-3 text-right">
                        <button
                          onClick={() => {
                            if (confirm(`Remove holiday "${hol.name}"?`)) {
                              deleteHolidayMutation.mutate(hol.id);
                            }
                          }}
                          className="p-1 hover:text-red-600 text-gray-400"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* TAB 4: AUTO-NUMBERING RULES */}
      {activeTab === "NUMBERING_RULES" && (
        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-base font-bold text-gray-900 dark:text-white flex items-center gap-2">
                  <Hash className="w-5 h-5 text-purple-600" /> Enterprise Auto-Numbering Series Rules
                </h3>
                <p className="text-xs text-gray-500">
                  Configurable prefix, suffix, zero-padding, and reset cadence for Roll Numbers, Employee IDs, and Invoices
                </p>
              </div>
            </div>

            {/* Test Generation Banner */}
            {generatedSample && (
              <div className="p-4 rounded-xl bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 flex items-center justify-between">
                <div>
                  <span className="text-xs font-semibold text-purple-600 uppercase">Live Generated Sequence</span>
                  <div className="text-lg font-mono font-bold text-purple-900 dark:text-purple-100">
                    {generatedSample.number}
                  </div>
                  <span className="text-xs text-purple-600">Entity: {generatedSample.entityType}</span>
                </div>
                <button
                  onClick={() => setGeneratedSample(null)}
                  className="text-xs text-purple-600 hover:text-purple-800 underline"
                >
                  Dismiss
                </button>
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {numberingRules.map((rule) => (
                <div
                  key={rule.id}
                  className="p-5 rounded-2xl bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-800 space-y-4"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <span className="text-xs font-mono font-semibold text-blue-600 dark:text-blue-400">
                        {rule.entity_type}
                      </span>
                      <h4 className="font-bold text-sm text-gray-900 dark:text-white">{rule.entity_title}</h4>
                    </div>
                    <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300">
                      Active
                    </span>
                  </div>

                  <div className="p-3 bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700">
                    <span className="text-xs text-gray-500">Live Preview Format</span>
                    <div className="text-base font-mono font-bold text-indigo-600 dark:text-indigo-400 mt-0.5">
                      {rule.sample_preview || "—"}
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-2 text-xs text-gray-600 dark:text-gray-300">
                    <div>Prefix: <strong>{rule.prefix || "None"}</strong></div>
                    <div>Suffix: <strong>{rule.suffix || "None"}</strong></div>
                    <div>Digits: <strong>{rule.digits_padding} digits</strong></div>
                    <div>Next Seq: <strong>#{rule.current_sequence}</strong></div>
                    <div>Reset: <strong>{rule.reset_frequency}</strong></div>
                    <div>Pattern: <code className="text-2xs bg-gray-200 dark:bg-gray-700 px-1 rounded">{rule.format_pattern}</code></div>
                  </div>

                  <div className="flex items-center gap-2 pt-2 border-t border-gray-200 dark:border-gray-800">
                    <button
                      onClick={() => testSequenceMutation.mutate(rule.entity_type)}
                      disabled={testSequenceMutation.isPending}
                      className="flex-1 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold rounded-xl transition shadow-sm text-center"
                    >
                      Test Sequence
                    </button>
                    <button
                      onClick={() => {
                        setEditingRule(rule);
                        setRuleForm({
                          prefix: rule.prefix,
                          suffix: rule.suffix,
                          digits_padding: rule.digits_padding,
                          format_pattern: rule.format_pattern,
                          reset_frequency: rule.reset_frequency,
                        });
                      }}
                      className="px-3 py-1.5 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 text-xs font-semibold rounded-xl transition"
                    >
                      Edit Rule
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* TAB 5: DOCUMENT TEMPLATES */}
      {activeTab === "TEMPLATES" && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Template Selector & Info */}
          <div className="lg:col-span-1 space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-gray-500">Available Templates</h3>
            <div className="space-y-2">
              {templates.map((tpl) => (
                <button
                  key={tpl.id}
                  onClick={() => {
                    setSelectedTemplateCode(tpl.template_code);
                    setTemplateHtml(tpl.content_html);
                    setRenderedPreview(null);
                  }}
                  className={`w-full text-left p-4 rounded-xl border transition ${
                    selectedTemplateCode === tpl.template_code
                      ? "bg-blue-50/60 border-blue-300 dark:bg-blue-900/20 dark:border-blue-700"
                      : "bg-white dark:bg-gray-800 border-gray-100 dark:border-gray-700 hover:bg-gray-50"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-sm text-gray-900 dark:text-white">{tpl.title}</span>
                    <span className="text-2xs font-mono uppercase bg-gray-200 dark:bg-gray-700 px-1.5 py-0.5 rounded text-gray-700 dark:text-gray-300">
                      {tpl.paper_size}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 mt-1 font-mono">{tpl.template_code}</p>
                </button>
              ))}
            </div>

            {/* Placeholder Variables Cheat Sheet */}
            {currentTemplate && currentTemplate.available_placeholders && (
              <div className="p-4 bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 space-y-2">
                <span className="text-xs font-bold uppercase text-gray-500">Available Placeholders</span>
                <div className="space-y-1.5 max-h-60 overflow-y-auto text-xs font-mono">
                  {Object.entries(currentTemplate.available_placeholders).map(([tag, desc]) => (
                    <div key={tag} className="p-1.5 bg-gray-50 dark:bg-gray-900 rounded border border-gray-200 dark:border-gray-800">
                      <code className="text-blue-600 dark:text-blue-400 font-bold">{`{{${tag}}}`}</code>
                      <p className="text-2xs text-gray-500 font-sans mt-0.5">{desc}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Template Preview & Actions */}
          <div className="lg:col-span-2 bg-white dark:bg-gray-800 p-6 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-base font-bold text-gray-900 dark:text-white">{currentTemplate?.title}</h3>
                <p className="text-xs text-gray-500">
                  Paper: {currentTemplate?.paper_size} | Orientation: {currentTemplate?.orientation}
                </p>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={handleTestRender}
                  disabled={renderTemplateMutation.isPending}
                  className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-xl shadow-sm transition"
                >
                  <Eye className="w-3.5 h-3.5" /> Test Render Sample
                </button>
                <button
                  onClick={() => setIsEditingTemplate(!isEditingTemplate)}
                  className="flex items-center gap-1.5 px-3 py-1.5 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 text-gray-800 dark:text-gray-200 text-xs font-semibold rounded-xl transition"
                >
                  <Edit2 className="w-3.5 h-3.5" /> {isEditingTemplate ? "Preview Mode" : "Edit HTML"}
                </button>
              </div>
            </div>

            {/* Template Content */}
            {isEditingTemplate ? (
              <div className="space-y-3">
                <textarea
                  value={templateHtml}
                  onChange={(e) => setTemplateHtml(e.target.value)}
                  rows={16}
                  className="w-full font-mono text-xs p-3 rounded-xl border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                  onClick={() => {
                    if (currentTemplate) {
                      updateTemplateMutation.mutate({
                        id: currentTemplate.id,
                        payload: { content_html: templateHtml },
                      });
                    }
                  }}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-xl shadow-sm transition"
                >
                  Save Template HTML
                </button>
              </div>
            ) : renderedPreview ? (
              <div className="border border-gray-200 dark:border-gray-700 rounded-xl p-4 bg-gray-100 dark:bg-gray-900 overflow-x-auto">
                <div className="flex items-center justify-between pb-3 mb-3 border-b border-gray-200 dark:border-gray-700 text-xs text-gray-500">
                  <span className="font-semibold text-emerald-600">Sample Generated Certificate Preview</span>
                  <button
                    onClick={() => window.print()}
                    className="flex items-center gap-1 text-blue-600 hover:underline"
                  >
                    <Printer className="w-3.5 h-3.5" /> Print Preview
                  </button>
                </div>
                <div
                  className="bg-white text-black p-4 rounded shadow-sm mx-auto"
                  dangerouslySetInnerHTML={{ __html: renderedPreview }}
                />
              </div>
            ) : (
              <div className="border border-dashed border-gray-300 dark:border-gray-700 rounded-xl p-8 text-center space-y-2">
                <FileCode className="w-8 h-8 text-gray-400 mx-auto" />
                <p className="text-sm font-semibold text-gray-600 dark:text-gray-300">
                  Click "Test Render Sample" to compile and preview this certificate format
                </p>
                <p className="text-xs text-gray-400">
                  Substitutes student profile tags like Roll No, Program, Conduct, and Issue Dates automatically
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* MODAL: Add/Edit Master Data Item */}
      {showItemModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 max-w-md w-full shadow-2xl border border-gray-100 dark:border-gray-700 space-y-4">
            <h3 className="text-base font-bold text-gray-900 dark:text-white">
              {editingItem ? "Edit Taxonomy Item" : `Add Item to ${selectedCategory}`}
            </h3>

            <div className="space-y-3">
              <div>
                <label className="text-xs font-semibold text-gray-500">Item Code (Machine Unique)</label>
                <input
                  type="text"
                  disabled={!!editingItem}
                  value={itemForm.item_code}
                  onChange={(e) => setItemForm({ ...itemForm, item_code: e.target.value.toUpperCase() })}
                  placeholder="e.g. MALE, O_POS, GEN"
                  className="w-full mt-1 px-3 py-2 text-sm rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                />
              </div>

              <div>
                <label className="text-xs font-semibold text-gray-500">Item Label (Human Readable)</label>
                <input
                  type="text"
                  value={itemForm.item_label}
                  onChange={(e) => setItemForm({ ...itemForm, item_label: e.target.value })}
                  placeholder="e.g. Male, O Positive (O+)"
                  className="w-full mt-1 px-3 py-2 text-sm rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                />
              </div>

              <div>
                <label className="text-xs font-semibold text-gray-500">Item Value / Code (Optional)</label>
                <input
                  type="text"
                  value={itemForm.item_value}
                  onChange={(e) => setItemForm({ ...itemForm, item_value: e.target.value })}
                  placeholder="e.g. M, O+, GEN"
                  className="w-full mt-1 px-3 py-2 text-sm rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                />
              </div>

              <div>
                <label className="text-xs font-semibold text-gray-500">Display Order</label>
                <input
                  type="number"
                  value={itemForm.display_order}
                  onChange={(e) => setItemForm({ ...itemForm, display_order: parseInt(e.target.value) || 1 })}
                  className="w-full mt-1 px-3 py-2 text-sm rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                />
              </div>
            </div>

            <div className="flex items-center justify-end gap-2 pt-3 border-t border-gray-100 dark:border-gray-700">
              <button
                onClick={() => setShowItemModal(false)}
                className="px-4 py-2 text-xs font-semibold text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-xl"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  if (editingItem) {
                    updateItemMutation.mutate({
                      id: editingItem.id,
                      payload: itemForm,
                    });
                  } else {
                    createItemMutation.mutate({
                      institute_id: "00000000-0000-0000-0000-000000000001",
                      category_key: selectedCategory,
                      ...itemForm,
                    });
                  }
                }}
                className="px-4 py-2 text-xs font-semibold bg-blue-600 hover:bg-blue-700 text-white rounded-xl shadow-sm"
              >
                {editingItem ? "Update Item" : "Create Item"}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* MODAL: Declare Campus Holiday */}
      {showHolidayModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 max-w-md w-full shadow-2xl border border-gray-100 dark:border-gray-700 space-y-4">
            <h3 className="text-base font-bold text-gray-900 dark:text-white">Declare Official Campus Holiday</h3>

            <div className="space-y-3">
              <div>
                <label className="text-xs font-semibold text-gray-500">Holiday Title</label>
                <input
                  type="text"
                  value={holidayForm.name}
                  onChange={(e) => setHolidayForm({ ...holidayForm, name: e.target.value })}
                  placeholder="e.g. Rangpanchmi Festival Break"
                  className="w-full mt-1 px-3 py-2 text-sm rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                />
              </div>

              <div>
                <label className="text-xs font-semibold text-gray-500">Holiday Date</label>
                <input
                  type="date"
                  value={holidayForm.holiday_date}
                  onChange={(e) => setHolidayForm({ ...holidayForm, holiday_date: e.target.value })}
                  className="w-full mt-1 px-3 py-2 text-sm rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                />
              </div>

              <div>
                <label className="text-xs font-semibold text-gray-500">Holiday Classification</label>
                <select
                  value={holidayForm.holiday_type}
                  onChange={(e) => setHolidayForm({ ...holidayForm, holiday_type: e.target.value })}
                  className="w-full mt-1 px-3 py-2 text-sm rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                >
                  <option value="GAZETTED">GAZETTED (Mandatory State/National)</option>
                  <option value="RESTRICTED">RESTRICTED (Optional for Staff)</option>
                  <option value="ACADEMIC_BREAK">ACADEMIC_BREAK (Student Recess)</option>
                  <option value="INSTITUTIONAL">INSTITUTIONAL (Founders Day/Campus event)</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-semibold text-gray-500">Description / Circular Memo</label>
                <textarea
                  value={holidayForm.description}
                  onChange={(e) => setHolidayForm({ ...holidayForm, description: e.target.value })}
                  rows={2}
                  placeholder="Official notification details"
                  className="w-full mt-1 px-3 py-2 text-sm rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                />
              </div>
            </div>

            <div className="flex items-center justify-end gap-2 pt-3 border-t border-gray-100 dark:border-gray-700">
              <button
                onClick={() => setShowHolidayModal(false)}
                className="px-4 py-2 text-xs font-semibold text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-xl"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  createHolidayMutation.mutate({
                    institute_id: "00000000-0000-0000-0000-000000000001",
                    ...holidayForm,
                  });
                }}
                className="px-4 py-2 text-xs font-semibold bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl shadow-sm"
              >
                Declare Holiday
              </button>
            </div>
          </div>
        </div>
      )}

      {/* MODAL: Edit Numbering Rule */}
      {editingRule && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 max-w-md w-full shadow-2xl border border-gray-100 dark:border-gray-700 space-y-4">
            <h3 className="text-base font-bold text-gray-900 dark:text-white">
              Edit Numbering Rule: {editingRule.entity_title}
            </h3>

            <div className="space-y-3">
              <div>
                <label className="text-xs font-semibold text-gray-500">Prefix</label>
                <input
                  type="text"
                  value={ruleForm.prefix}
                  onChange={(e) => setRuleForm({ ...ruleForm, prefix: e.target.value })}
                  placeholder="e.g. MEI-, RCP-"
                  className="w-full mt-1 px-3 py-2 text-sm rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                />
              </div>

              <div>
                <label className="text-xs font-semibold text-gray-500">Suffix</label>
                <input
                  type="text"
                  value={ruleForm.suffix}
                  onChange={(e) => setRuleForm({ ...ruleForm, suffix: e.target.value })}
                  placeholder="e.g. -IND"
                  className="w-full mt-1 px-3 py-2 text-sm rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                />
              </div>

              <div>
                <label className="text-xs font-semibold text-gray-500">Zero-Padding Digits Count</label>
                <input
                  type="number"
                  min={1}
                  max={8}
                  value={ruleForm.digits_padding}
                  onChange={(e) => setRuleForm({ ...ruleForm, digits_padding: parseInt(e.target.value) || 4 })}
                  className="w-full mt-1 px-3 py-2 text-sm rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                />
              </div>

              <div>
                <label className="text-xs font-semibold text-gray-500">Format Pattern</label>
                <input
                  type="text"
                  value={ruleForm.format_pattern}
                  onChange={(e) => setRuleForm({ ...ruleForm, format_pattern: e.target.value })}
                  placeholder="{PREFIX}{YEAR}-{SEQ}{SUFFIX}"
                  className="w-full mt-1 px-3 py-2 text-sm rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white font-mono"
                />
              </div>

              <div>
                <label className="text-xs font-semibold text-gray-500">Reset Frequency</label>
                <select
                  value={ruleForm.reset_frequency}
                  onChange={(e) => setRuleForm({ ...ruleForm, reset_frequency: e.target.value })}
                  className="w-full mt-1 px-3 py-2 text-sm rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                >
                  <option value="ANNUAL">Annual (Resets every calendar year)</option>
                  <option value="ACADEMIC_SESSION">Academic Session (Resets each academic year)</option>
                  <option value="NEVER">Never (Continuous incrementing serial)</option>
                </select>
              </div>
            </div>

            <div className="flex items-center justify-end gap-2 pt-3 border-t border-gray-100 dark:border-gray-700">
              <button
                onClick={() => setEditingRule(null)}
                className="px-4 py-2 text-xs font-semibold text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-xl"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  updateRuleMutation.mutate({
                    id: editingRule.id,
                    payload: ruleForm,
                  });
                }}
                className="px-4 py-2 text-xs font-semibold bg-purple-600 hover:bg-purple-700 text-white rounded-xl shadow-sm"
              >
                Save Numbering Rule
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
export default SystemSettingsManagerPage;
