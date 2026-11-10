import { httpClient } from "@/api/httpClient";
import {
  CampusHoliday,
  DocumentRenderResponse,
  DocumentTemplate,
  MasterDataCategorySummary,
  MasterDataEntry,
  NumberingRule,
  NumberingSequenceGenerateResponse,
  SystemSettingsSummary,
  WorkingDaysConfig,
} from "@/types/systemSettings.types";

export const systemSettingsService = {
  async getSummary(instituteId?: string): Promise<SystemSettingsSummary> {
    const params = instituteId ? { institute_id: instituteId } : {};
    const res = await httpClient.get<SystemSettingsSummary>("/system-settings/summary", { params });
    return res.data;
  },

  // 1. Master Data
  async listCategories(instituteId?: string): Promise<MasterDataCategorySummary[]> {
    const params = instituteId ? { institute_id: instituteId } : {};
    const res = await httpClient.get<MasterDataCategorySummary[]>("/system-settings/master-data/categories", { params });
    return res.data;
  },

  async listItems(categoryKey: string, activeOnly = false, instituteId?: string): Promise<MasterDataEntry[]> {
    const params: Record<string, any> = { category_key: categoryKey, active_only: activeOnly };
    if (instituteId) params.institute_id = instituteId;
    const res = await httpClient.get<MasterDataEntry[]>("/system-settings/master-data/items", { params });
    return res.data;
  },

  async createItem(payload: Partial<MasterDataEntry> & { category_key: string; item_code: string; item_label: string; institute_id: string }): Promise<MasterDataEntry> {
    const res = await httpClient.post<MasterDataEntry>("/system-settings/master-data/items", payload);
    return res.data;
  },

  async updateItem(itemId: string, payload: Partial<MasterDataEntry>): Promise<MasterDataEntry> {
    const res = await httpClient.put<MasterDataEntry>(`/system-settings/master-data/items/${itemId}`, payload);
    return res.data;
  },

  async deleteItem(itemId: string): Promise<void> {
    await httpClient.delete(`/system-settings/master-data/items/${itemId}`);
  },

  // 2. Campus Holidays
  async listHolidays(year?: number, instituteId?: string): Promise<CampusHoliday[]> {
    const params: Record<string, any> = {};
    if (year) params.year = year;
    if (instituteId) params.institute_id = instituteId;
    const res = await httpClient.get<CampusHoliday[]>("/system-settings/holidays", { params });
    return res.data;
  },

  async createHoliday(payload: Partial<CampusHoliday> & { name: string; holiday_date: string; institute_id: string }): Promise<CampusHoliday> {
    const res = await httpClient.post<CampusHoliday>("/system-settings/holidays", payload);
    return res.data;
  },

  async updateHoliday(holidayId: string, payload: Partial<CampusHoliday>): Promise<CampusHoliday> {
    const res = await httpClient.put<CampusHoliday>(`/system-settings/holidays/${holidayId}`, payload);
    return res.data;
  },

  async deleteHoliday(holidayId: string): Promise<void> {
    await httpClient.delete(`/system-settings/holidays/${holidayId}`);
  },

  // 3. Working Days & Timings
  async getWorkingDays(instituteId?: string): Promise<WorkingDaysConfig[]> {
    const params = instituteId ? { institute_id: instituteId } : {};
    const res = await httpClient.get<WorkingDaysConfig[]>("/system-settings/working-days", { params });
    return res.data;
  },

  async updateWorkingDay(dayId: string, payload: Partial<WorkingDaysConfig>): Promise<WorkingDaysConfig> {
    const res = await httpClient.put<WorkingDaysConfig>(`/system-settings/working-days/${dayId}`, payload);
    return res.data;
  },

  // 4. Auto-Numbering Rules
  async listNumberingRules(instituteId?: string): Promise<NumberingRule[]> {
    const params = instituteId ? { institute_id: instituteId } : {};
    const res = await httpClient.get<NumberingRule[]>("/system-settings/numbering-rules", { params });
    return res.data;
  },

  async updateNumberingRule(ruleId: string, payload: Partial<NumberingRule>): Promise<NumberingRule> {
    const res = await httpClient.put<NumberingRule>(`/system-settings/numbering-rules/${ruleId}`, payload);
    return res.data;
  },

  async generateSequence(entityType: string, increment = true, instituteId?: string): Promise<NumberingSequenceGenerateResponse> {
    const params = instituteId ? { institute_id: instituteId } : {};
    const res = await httpClient.post<NumberingSequenceGenerateResponse>(
      "/system-settings/numbering-rules/generate",
      { entity_type: entityType, increment_counter: increment },
      { params }
    );
    return res.data;
  },

  // 5. Document Templates
  async listDocumentTemplates(instituteId?: string): Promise<DocumentTemplate[]> {
    const params = instituteId ? { institute_id: instituteId } : {};
    const res = await httpClient.get<DocumentTemplate[]>("/system-settings/document-templates", { params });
    return res.data;
  },

  async getDocumentTemplate(templateCode: string, instituteId?: string): Promise<DocumentTemplate> {
    const params = instituteId ? { institute_id: instituteId } : {};
    const res = await httpClient.get<DocumentTemplate>(`/system-settings/document-templates/${templateCode}`, { params });
    return res.data;
  },

  async updateDocumentTemplate(templateId: string, payload: Partial<DocumentTemplate>): Promise<DocumentTemplate> {
    const res = await httpClient.put<DocumentTemplate>(`/system-settings/document-templates/${templateId}`, payload);
    return res.data;
  },

  async renderDocumentTemplate(templateCode: string, contextData: Record<string, any>, instituteId?: string): Promise<DocumentRenderResponse> {
    const params = instituteId ? { institute_id: instituteId } : {};
    const res = await httpClient.post<DocumentRenderResponse>(
      "/system-settings/document-templates/render",
      { template_code: templateCode, context_data: contextData },
      { params }
    );
    return res.data;
  },
};
