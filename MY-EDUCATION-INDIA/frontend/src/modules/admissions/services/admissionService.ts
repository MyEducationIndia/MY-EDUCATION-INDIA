import { httpClient } from "@/api/httpClient";
import { AdmissionMetrics, ApplicationRecord, LeadRecord } from "../types/admission.types";

export const admissionService = {
  async getDashboardMetrics(): Promise<AdmissionMetrics> {
    const res = await httpClient.get<AdmissionMetrics>("/admissions/dashboard");
    return res.data;
  },

  async listLeads(params?: { priority?: string; status?: string; search?: string; page?: number }): Promise<{ items: LeadRecord[]; total: number }> {
    const res = await httpClient.get<{ items: LeadRecord[]; total: number }>("/admissions/leads", { params });
    return res.data;
  },

  async createLead(payload: any): Promise<LeadRecord> {
    const res = await httpClient.post<LeadRecord>("/admissions/leads", payload);
    return res.data;
  },

  async addFollowup(leadId: string, payload: any): Promise<{ success: boolean; followup_id: string }> {
    const res = await httpClient.post<{ success: boolean; followup_id: string }>(`/admissions/leads/${leadId}/followups`, payload);
    return res.data;
  },

  async listApplications(params?: { status?: string; course_name?: string; search?: string; page?: number }): Promise<{ items: ApplicationRecord[]; total: number }> {
    const res = await httpClient.get<{ items: ApplicationRecord[]; total: number }>("/admissions/applications", { params });
    return res.data;
  },

  async submitApplication(payload: any): Promise<ApplicationRecord> {
    const res = await httpClient.post<ApplicationRecord>("/admissions/applications", payload);
    return res.data;
  },

  async approveAdmission(applicationId: string, allocatedBatch: string): Promise<{ success: boolean; student_id: string; registration_number: string }> {
    const res = await httpClient.post<{ success: boolean; student_id: string; registration_number: string }>("/admissions/applications/approve", {
      application_id: applicationId,
      allocated_batch: allocatedBatch,
    });
    return res.data;
  },

  async rejectAdmission(applicationId: string, reason: string): Promise<{ success: boolean; message: string }> {
    const res = await httpClient.post<{ success: boolean; message: string }>("/admissions/applications/reject", {
      application_id: applicationId,
      rejection_reason: reason,
    });
    return res.data;
  },

  async collectFee(payload: { application_id: string; amount_paid: number; fee_type?: string; payment_mode?: string }): Promise<any> {
    const res = await httpClient.post("/admissions/fees/collect", payload);
    return res.data;
  },
};
