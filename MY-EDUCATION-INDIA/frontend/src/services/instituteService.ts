import { httpClient } from "@/api/httpClient";
import {
  AcademicSessionCreatePayload,
  AcademicSessionItem,
  AcademicSessionUpdatePayload,
  Institute,
  InstituteBrandingUpdatePayload,
  InstituteIntegrationsUpdatePayload,
  InstituteProfileUpdatePayload,
  InstituteSetupBundle,
  SystemModuleConfig,
} from "@/types/institute.types";

export const instituteService = {
  async listInstitutes(): Promise<Institute[]> {
    const response = await httpClient.get<Institute[]>("/institutes");
    return response.data;
  },

  async getInstitute(instituteId: string): Promise<Institute> {
    const response = await httpClient.get<Institute>(`/institutes/${instituteId}`);
    return response.data;
  },

  async getSetupBundle(instituteId: string): Promise<InstituteSetupBundle> {
    const response = await httpClient.get<InstituteSetupBundle>(
      `/institutes/${instituteId}/setup-bundle`
    );
    return response.data;
  },

  async updateProfile(
    instituteId: string,
    payload: InstituteProfileUpdatePayload
  ): Promise<Institute> {
    const response = await httpClient.patch<Institute>(
      `/institutes/${instituteId}/profile`,
      payload
    );
    return response.data;
  },

  async updateBranding(
    instituteId: string,
    payload: InstituteBrandingUpdatePayload
  ): Promise<Institute> {
    const response = await httpClient.patch<Institute>(
      `/institutes/${instituteId}/branding`,
      payload
    );
    return response.data;
  },

  async updateIntegrations(
    instituteId: string,
    payload: InstituteIntegrationsUpdatePayload
  ): Promise<Institute> {
    const response = await httpClient.patch<Institute>(
      `/institutes/${instituteId}/integrations`,
      payload
    );
    return response.data;
  },

  async listAcademicSessions(instituteId: string): Promise<AcademicSessionItem[]> {
    const response = await httpClient.get<AcademicSessionItem[]>(
      `/institutes/${instituteId}/academic-sessions`
    );
    return response.data;
  },

  async createAcademicSession(
    instituteId: string,
    payload: AcademicSessionCreatePayload
  ): Promise<AcademicSessionItem> {
    const response = await httpClient.post<AcademicSessionItem>(
      `/institutes/${instituteId}/academic-sessions`,
      payload
    );
    return response.data;
  },

  async updateAcademicSession(
    instituteId: string,
    sessionId: string,
    payload: AcademicSessionUpdatePayload
  ): Promise<AcademicSessionItem> {
    const response = await httpClient.patch<AcademicSessionItem>(
      `/institutes/${instituteId}/academic-sessions/${sessionId}`,
      payload
    );
    return response.data;
  },

  async deleteAcademicSession(
    instituteId: string,
    sessionId: string
  ): Promise<{ status: string; message: string }> {
    const response = await httpClient.delete<{ status: string; message: string }>(
      `/institutes/${instituteId}/academic-sessions/${sessionId}`
    );
    return response.data;
  },

  async toggleModule(
    instituteId: string,
    moduleKey: string,
    isEnabled: boolean
  ): Promise<SystemModuleConfig> {
    const response = await httpClient.patch<SystemModuleConfig>(
      `/institutes/${instituteId}/modules/${moduleKey}`,
      { is_enabled: isEnabled }
    );
    return response.data;
  },
};
