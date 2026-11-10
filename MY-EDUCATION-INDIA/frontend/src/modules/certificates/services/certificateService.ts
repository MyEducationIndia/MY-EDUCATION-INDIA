import { apiClient } from "@/lib/api/apiClient";
import {
  CertificateDashboardSummary,
  CertificateTemplate,
  DocumentType,
  IDCard,
  IssuedCertificate,
  PublicVerificationResult,
} from "../types/certificate.types";

export const certificateService = {
  // Dashboard & Analytics
  getDashboardSummary: async (instituteId: string): Promise<CertificateDashboardSummary> => {
    const res = await apiClient.get<CertificateDashboardSummary>("/certificates/dashboard", {
      params: { institute_id: instituteId },
    });
    return res.data;
  },

  // Document Types & Templates
  getDocumentTypes: async (instituteId: string): Promise<DocumentType[]> => {
    const res = await apiClient.get<DocumentType[]>("/certificates/types", {
      params: { institute_id: instituteId },
    });
    return res.data;
  },

  createDocumentType: async (payload: {
    institute_id: string;
    code: string;
    name: string;
    category?: string;
  }): Promise<DocumentType> => {
    const res = await apiClient.post<DocumentType>("/certificates/types", payload);
    return res.data;
  },

  getTemplates: async (instituteId: string): Promise<CertificateTemplate[]> => {
    const res = await apiClient.get<CertificateTemplate[]>("/certificates/templates", {
      params: { institute_id: instituteId },
    });
    return res.data;
  },

  createTemplate: async (payload: any): Promise<CertificateTemplate> => {
    const res = await apiClient.post<CertificateTemplate>("/certificates/templates", payload);
    return res.data;
  },

  // Issuing & Revocation
  issueSingle: async (payload: {
    template_id: string;
    recipient_type: string;
    recipient_user_id: string;
    payload_data: Record<string, any>;
    issue_date?: string;
    expiry_date?: string;
  }): Promise<IssuedCertificate> => {
    const res = await apiClient.post<IssuedCertificate>("/certificates/issue", payload);
    return res.data;
  },

  revokeCertificate: async (certificateId: string, reason: string): Promise<IssuedCertificate> => {
    const res = await apiClient.post<IssuedCertificate>("/certificates/revoke", {
      certificate_id: certificateId,
      reason,
    });
    return res.data;
  },

  // ID Cards
  issueIDCard: async (payload: {
    institute_id: string;
    holder_type: string;
    holder_user_id: string;
    blood_group?: string;
    emergency_contact?: string;
    valid_until: string;
  }): Promise<IDCard> => {
    const res = await apiClient.post<IDCard>("/certificates/id-cards", payload);
    return res.data;
  },

  // Public Verification Portal (Unauthenticated)
  verifyPublicCredential: async (identifier: string): Promise<PublicVerificationResult> => {
    const res = await apiClient.get<PublicVerificationResult>(`/public/verify/${encodeURIComponent(identifier)}`);
    return res.data;
  },
};
