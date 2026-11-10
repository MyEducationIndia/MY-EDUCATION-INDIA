import { httpClient } from "@/api/httpClient";
import { CrmLead, CrmEnquiry, CrmCampaign, FranchiseCenter, CrmDashboardMetrics } from "../types/crm.types";

export const crmService = {
  getDashboardMetrics: async (): Promise<CrmDashboardMetrics> => {
    const res = await httpClient.get<CrmDashboardMetrics>("/crm/dashboard");
    return res.data;
  },

  listLeads: async (stage?: string): Promise<CrmLead[]> => {
    const res = await httpClient.get<CrmLead[]>("/crm/leads", { params: { stage } });
    return res.data;
  },

  listEnquiries: async (): Promise<CrmEnquiry[]> => {
    const res = await httpClient.get<CrmEnquiry[]>("/crm/enquiries");
    return res.data;
  },

  listCampaigns: async (): Promise<CrmCampaign[]> => {
    const res = await httpClient.get<CrmCampaign[]>("/crm/campaigns");
    return res.data;
  },

  listFranchiseCenters: async (): Promise<FranchiseCenter[]> => {
    const res = await httpClient.get<FranchiseCenter[]>("/crm/franchise/centers");
    return res.data;
  }
};
