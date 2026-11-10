import { httpClient } from "@/api/httpClient";
import {
  AcademicYearItem,
  BranchItem,
  FinancialYearItem,
  InstituteItem,
  NumberGeneratorItem,
  OrganizationSettings,
  SystemSettingRecord,
} from "../types/system.types";

export const systemApi = {
  // Institutes
  async listInstitutes(): Promise<InstituteItem[]> {
    const res = await httpClient.get<InstituteItem[]>("/system/institutes");
    return res.data;
  },

  // Branches
  async listBranches(instituteId?: string): Promise<BranchItem[]> {
    const res = await httpClient.get<BranchItem[]>("/system/branches", {
      params: instituteId ? { institute_id: instituteId } : undefined,
    });
    return res.data;
  },

  async createBranch(payload: Partial<BranchItem>): Promise<BranchItem> {
    const res = await httpClient.post<BranchItem>("/system/branches", payload);
    return res.data;
  },

  async updateBranch(branchId: string, payload: Partial<BranchItem>): Promise<BranchItem> {
    const res = await httpClient.patch<BranchItem>(`/system/branches/${branchId}`, payload);
    return res.data;
  },

  // Academic Years
  async listAcademicYears(instituteId?: string): Promise<AcademicYearItem[]> {
    const res = await httpClient.get<AcademicYearItem[]>("/system/academic-years", {
      params: instituteId ? { institute_id: instituteId } : undefined,
    });
    return res.data;
  },

  async createAcademicYear(payload: Partial<AcademicYearItem>): Promise<AcademicYearItem> {
    const res = await httpClient.post<AcademicYearItem>("/system/academic-years", payload);
    return res.data;
  },

  async setCurrentAcademicYear(ayId: string): Promise<AcademicYearItem> {
    const res = await httpClient.post<AcademicYearItem>(`/system/academic-years/${ayId}/set-current`, {});
    return res.data;
  },

  // Financial Years
  async listFinancialYears(instituteId?: string): Promise<FinancialYearItem[]> {
    const res = await httpClient.get<FinancialYearItem[]>("/system/financial-years", {
      params: instituteId ? { institute_id: instituteId } : undefined,
    });
    return res.data;
  },

  async createFinancialYear(payload: Partial<FinancialYearItem>): Promise<FinancialYearItem> {
    const res = await httpClient.post<FinancialYearItem>("/system/financial-years", payload);
    return res.data;
  },

  async setCurrentFinancialYear(fyId: string): Promise<FinancialYearItem> {
    const res = await httpClient.post<FinancialYearItem>(`/system/financial-years/${fyId}/set-current`, {});
    return res.data;
  },

  // Number Generator
  async listNumberGenerators(instituteId?: string): Promise<NumberGeneratorItem[]> {
    const res = await httpClient.get<NumberGeneratorItem[]>("/system/number-generator", {
      params: instituteId ? { institute_id: instituteId } : undefined,
    });
    return res.data;
  },

  async createNumberGenerator(payload: Partial<NumberGeneratorItem>): Promise<NumberGeneratorItem> {
    const res = await httpClient.post<NumberGeneratorItem>("/system/number-generator", payload);
    return res.data;
  },

  async updateNumberGenerator(genId: string, payload: Partial<NumberGeneratorItem>): Promise<NumberGeneratorItem> {
    const res = await httpClient.patch<NumberGeneratorItem>(`/system/number-generator/${genId}`, payload);
    return res.data;
  },

  async previewNumber(payload: {
    prefix?: string;
    suffix?: string;
    format_template: string;
    separator: string;
    padding_length: number;
    sample_number: number;
    branch_code?: string;
    year?: number;
  }): Promise<{ preview: string }> {
    const res = await httpClient.post<{ preview: string }>("/system/number-generator/preview", payload);
    return res.data;
  },

  // Settings & Organization
  async getOrganizationSettings(instituteId?: string): Promise<OrganizationSettings> {
    const res = await httpClient.get<OrganizationSettings>("/system/organization", {
      params: instituteId ? { institute_id: instituteId } : undefined,
    });
    return res.data;
  },

  async updateOrganizationSettings(payload: Partial<OrganizationSettings>, instituteId?: string): Promise<OrganizationSettings> {
    const res = await httpClient.patch<OrganizationSettings>("/system/organization", payload, {
      params: instituteId ? { institute_id: instituteId } : undefined,
    });
    return res.data;
  },

  async getSettingsByCategory(category: string, instituteId?: string): Promise<SystemSettingRecord[]> {
    const res = await httpClient.get<SystemSettingRecord[]>("/system/settings", {
      params: { category, institute_id: instituteId },
    });
    return res.data;
  },

  async saveSetting(payload: { category: string; key: string; value: Record<string, unknown>; institute_id?: string }): Promise<SystemSettingRecord> {
    const res = await httpClient.post<SystemSettingRecord>("/system/settings", payload);
    return res.data;
  },
};
