import { httpClient } from "@/api/httpClient";
import {
  Institute,
  InstituteBrandingUpdatePayload,
  SystemModuleConfig,
} from "@/types/institute.types";

export const instituteService = {
  async listInstitutes(): Promise<Institute[]> {
    const response = await httpClient.get<Institute[]>("/institutes");
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
