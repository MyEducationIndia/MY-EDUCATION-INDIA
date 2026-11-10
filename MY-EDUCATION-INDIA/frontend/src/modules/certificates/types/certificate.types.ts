export interface DocumentType {
  id: string;
  institute_id: string;
  code: string;
  name: string;
  description?: string;
  category: "ACADEMIC" | "ADMINISTRATIVE" | "IDENTIFICATION";
  requires_approval: boolean;
  has_expiry: boolean;
  validity_months: number;
  is_active: boolean;
  created_at: string;
}

export interface CertificateTemplate {
  id: string;
  institute_id: string;
  branch_id?: string;
  document_type_id: string;
  template_code: string;
  title: string;
  page_orientation: "LANDSCAPE" | "PORTRAIT";
  page_size: "A4" | "LETTER" | "LEGAL" | "ID_CARD_CR80";
  background_image_url?: string;
  html_markup: string;
  css_styles: string;
  version: number;
  is_active: boolean;
  created_at: string;
}

export interface IssuedCertificate {
  id: string;
  certificate_number: string;
  verification_id: string;
  template_id: string;
  institute_id: string;
  recipient_type: "STUDENT" | "FACULTY" | "STAFF" | "EXTERNAL";
  recipient_user_id: string;
  issue_date: string;
  expiry_date?: string;
  payload_data_json: Record<string, any>;
  pdf_document_url?: string;
  qr_code_payload: string;
  barcode_data: string;
  status: "DRAFT" | "PENDING_REVIEW" | "APPROVED" | "ISSUED" | "REVOKED" | "ARCHIVED";
  revocation_reason?: string;
  created_at: string;
}

export interface IDCard {
  id: string;
  card_number: string;
  holder_type: "STUDENT" | "FACULTY" | "STAFF" | "VISITOR";
  holder_user_id: string;
  blood_group?: string;
  emergency_contact?: string;
  valid_until: string;
  status: "ACTIVE" | "EXPIRED" | "BLOCKED";
  qr_code_payload: string;
  created_at: string;
}

export interface PublicVerificationResult {
  is_valid: boolean;
  status: "VALID" | "REVOKED" | "EXPIRED" | "NOT_FOUND";
  certificate_number?: string;
  document_type_name?: string;
  recipient_name_masked?: string;
  institute_name?: string;
  issue_date?: string;
  expiry_date?: string;
  digital_signature_verified: boolean;
  message: string;
}

export interface CertificateDashboardSummary {
  total_issued_certificates: number;
  pending_approvals_count: number;
  revoked_certificates_count: number;
  public_verifications_count: number;
  active_templates_count: number;
  id_cards_active_count: number;
  document_distribution: Record<string, number>;
  monthly_trend: Array<{ month: string; issued: number; verified: number }>;
}
