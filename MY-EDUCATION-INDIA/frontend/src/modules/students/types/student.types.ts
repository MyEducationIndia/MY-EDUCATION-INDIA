export interface StudentSummary {
  id: string;
  registration_number: string;
  enrollment_number?: string | null;
  roll_number?: string | null;
  erp_id?: string | null;
  first_name: string;
  middle_name?: string | null;
  last_name: string;
  email: string;
  phone_number: string;
  date_of_birth: string;
  gender: string;
  course_name: string;
  batch_name: string;
  academic_year_code: string;
  status: string;
  photo_url?: string | null;
  admission_date: string;
  created_at: string;
}

export interface StudentProfileData {
  aadhaar_number?: string | null;
  pan_number?: string | null;
  apaar_id?: string | null;
  abc_account_id?: string | null;
  religion?: string | null;
  caste_category?: string | null;
  nationality: string;
  mother_tongue?: string | null;
  previous_school?: string | null;
  previous_qualification?: string | null;
  previous_marks_percentage?: number | null;
}

export interface StudentAddressData {
  address_type: string;
  address_line1: string;
  address_line2?: string | null;
  city: string;
  district: string;
  state: string;
  postal_code: string;
  country: string;
  is_primary: boolean;
}

export interface StudentGuardianData {
  relationship_type: string;
  full_name: string;
  mobile_number: string;
  email?: string | null;
  occupation?: string | null;
  annual_income?: number | null;
  is_emergency_contact: boolean;
}

export interface StudentMedicalData {
  blood_group?: string | null;
  height_cm?: number | null;
  weight_kg?: number | null;
  allergies?: string | null;
  medical_conditions?: string | null;
  emergency_doctor_name?: string | null;
  emergency_doctor_phone?: string | null;
}

export interface StudentDocumentItem {
  id: string;
  document_type: string;
  document_title: string;
  file_url: string;
  mime_type: string;
  file_size_bytes: number;
  is_verified: boolean;
  created_at: string;
}

export interface StudentTimelineItem {
  id: string;
  event_category: string;
  event_title: string;
  event_description: string;
  recorded_by: string;
  occurred_at: string;
  meta_payload: Record<string, any>;
}

export interface StudentDetailedProfile extends StudentSummary {
  profile?: StudentProfileData | null;
  addresses: StudentAddressData[];
  guardians: StudentGuardianData[];
  medical?: StudentMedicalData | null;
  documents: StudentDocumentItem[];
  timeline: StudentTimelineItem[];
  custom_values: Record<string, string>;
  qr_svg?: string | null;
}

export interface StudentCustomFieldItem {
  id: string;
  field_key: string;
  field_label: string;
  field_type: string;
  is_required: boolean;
  display_order: number;
  options_list: string[];
}
