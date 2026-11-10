export interface FeeCategory {
  id: string;
  code: string;
  name: string;
  description?: string;
  institute_id: string;
  branch_id?: string;
  is_active: boolean;
  created_at: string;
}

export interface FeeHead {
  id: string;
  category_id: string;
  code: string;
  name: string;
  description?: string;
  is_refundable: boolean;
  default_amount: number;
  institute_id: string;
  is_active: boolean;
  created_at: string;
}

export interface FeeStructureItem {
  id: string;
  fee_structure_id: string;
  fee_head_id: string;
  amount: number;
  is_optional: boolean;
  frequency: string;
  due_period?: string;
  created_at: string;
}

export interface Installment {
  id: string;
  fee_structure_id: string;
  installment_number: number;
  title: string;
  due_date: string;
  percentage: number;
  amount: number;
  grace_days: number;
  status: string;
  created_at: string;
}

export interface FeeStructure {
  id: string;
  code: string;
  name: string;
  version: number;
  institute_id: string;
  branch_id?: string;
  academic_year_id: string;
  effective_date: string;
  validity_date: string;
  total_amount: number;
  status: string;
  items: FeeStructureItem[];
  installments: Installment[];
  created_at: string;
}

export interface StudentFeeAssignment {
  id: string;
  student_id: string;
  fee_structure_id: string;
  institute_id: string;
  total_fee_amount: number;
  total_discount_amount: number;
  total_scholarship_amount: number;
  total_payable_amount: number;
  total_paid_amount: number;
  total_due_amount: number;
  assignment_type: string;
  status: "PENDING" | "PARTIAL" | "PAID" | "OVERDUE";
  assigned_at: string;
  created_at: string;
}

export interface Payment {
  id: string;
  student_fee_assignment_id: string;
  student_id: string;
  installment_id?: string;
  payment_number: string;
  amount_paid: number;
  payment_mode: "CASH" | "UPI" | "CREDIT_CARD" | "DEBIT_CARD" | "NET_BANKING" | "CHEQUE" | "DEMAND_DRAFT" | "BANK_TRANSFER";
  transaction_reference?: string;
  payment_date: string;
  status: "COMPLETED" | "PENDING" | "FAILED" | "REFUNDED";
  remarks?: string;
  created_at: string;
}

export interface Receipt {
  id: string;
  receipt_number: string;
  payment_id: string;
  student_id: string;
  institute_id: string;
  academic_year_id: string;
  total_amount: number;
  amount_in_words: string;
  qr_code_data: string;
  barcode_data: string;
  digital_signature_hash: string;
  receipt_date: string;
  status: string;
  created_at: string;
}

export interface Scholarship {
  id: string;
  code: string;
  name: string;
  scholarship_type: string;
  calculation_type: "PERCENTAGE" | "FIXED_AMOUNT";
  value: number;
  eligibility_criteria?: string;
  approval_workflow_status: string;
  max_beneficiaries: number;
  is_active: boolean;
  created_at: string;
}

export interface Discount {
  id: string;
  code: string;
  name: string;
  discount_type: string;
  calculation_type: "PERCENTAGE" | "FIXED_AMOUNT";
  value: number;
  max_discount_amount: number;
  is_active: boolean;
  created_at: string;
}

export interface Refund {
  id: string;
  refund_number: string;
  payment_id: string;
  student_id: string;
  amount: number;
  refund_type: "FULL" | "PARTIAL";
  reason: string;
  approval_status: "PENDING" | "APPROVED" | "REJECTED" | "PROCESSED";
  payment_mode: string;
  reference_number?: string;
  created_at: string;
}

export interface FeeAnalyticsSummary {
  total_projected_revenue: number;
  total_collected_revenue: number;
  total_outstanding_dues: number;
  collection_percentage: number;
  total_scholarships_granted: number;
  total_discounts_granted: number;
  total_refunds_processed: number;
  today_collection: number;
  month_collection: number;
  payment_mode_distribution: Record<string, number>;
  monthly_trend: Array<{ month: string; projected: number; collected: number }>;
}
