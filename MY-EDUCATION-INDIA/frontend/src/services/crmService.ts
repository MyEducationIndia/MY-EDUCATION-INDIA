import { httpClient } from "@/services/httpClient";
import {
  CrmLead,
  CrmFollowup,
  CrmCampaign,
  FranchiseCenter,
  CrmPipelineStage,
  CrmDashboardMetrics,
} from "@/types/crm.types";

export const crmService = {
  // Dashboard & Pipeline Stages
  async getDashboard(): Promise<CrmDashboardMetrics> {
    const res = await httpClient.get<CrmDashboardMetrics>("/crm/dashboard");
    return res.data;
  },

  async getPipelineStages(): Promise<CrmPipelineStage[]> {
    const res = await httpClient.get<CrmPipelineStage[]>("/crm/pipeline/stages");
    return res.data;
  },

  // Leads
  async listLeads(stage?: string, q?: string): Promise<CrmLead[]> {
    const res = await httpClient.get<CrmLead[]>("/crm/leads", {
      params: { stage: stage && stage !== "ALL" ? stage : undefined, q },
    });
    return res.data;
  },

  async createLead(payload: Partial<CrmLead>): Promise<CrmLead> {
    const res = await httpClient.post<CrmLead>("/crm/leads", payload);
    return res.data;
  },

  async updateLead(id: string, payload: Partial<CrmLead>): Promise<CrmLead> {
    const res = await httpClient.patch<CrmLead>(`/crm/leads/${id}`, payload);
    return res.data;
  },

  async deleteLead(id: string): Promise<void> {
    await httpClient.delete(`/crm/leads/${id}`);
  },

  // Follow-ups
  async listFollowups(lead_id?: string): Promise<CrmFollowup[]> {
    const res = await httpClient.get<CrmFollowup[]>("/crm/followups", {
      params: { lead_id },
    });
    return res.data;
  },

  async createFollowup(payload: Partial<CrmFollowup>): Promise<CrmFollowup> {
    const res = await httpClient.post<CrmFollowup>("/crm/followups", payload);
    return res.data;
  },

  // Campaigns
  async listCampaigns(): Promise<CrmCampaign[]> {
    const res = await httpClient.get<CrmCampaign[]>("/crm/campaigns");
    return res.data;
  },

  async createCampaign(payload: Partial<CrmCampaign>): Promise<CrmCampaign> {
    const res = await httpClient.post<CrmCampaign>("/crm/campaigns", payload);
    return res.data;
  },

  async deleteCampaign(id: string): Promise<void> {
    await httpClient.delete(`/crm/campaigns/${id}`);
  },

  // Franchise Centers
  async listFranchiseCenters(): Promise<FranchiseCenter[]> {
    const res = await httpClient.get<FranchiseCenter[]>("/crm/franchise/centers");
    return res.data;
  },

  async createFranchiseCenter(payload: Partial<FranchiseCenter>): Promise<FranchiseCenter> {
    const res = await httpClient.post<FranchiseCenter>("/crm/franchise/centers", payload);
    return res.data;
  },

  async deleteFranchiseCenter(id: string): Promise<void> {
    await httpClient.delete(`/crm/franchise/centers/${id}`);
  },
};
