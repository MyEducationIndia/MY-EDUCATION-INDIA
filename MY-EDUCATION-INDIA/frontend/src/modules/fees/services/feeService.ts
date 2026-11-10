import { apiClient } from "@/lib/api/apiClient";
import {
  FeeAnalyticsSummary,
  FeeCategory,
  FeeHead,
  FeeStructure,
  Payment,
  Receipt,
  Refund,
  Scholarship,
  StudentFeeAssignment,
} from "../types/fee.types";

export const feeService = {
  // Analytics
  getAnalytics: async (instituteId: string): Promise<FeeAnalyticsSummary> => {
    const res = await apiClient.get<FeeAnalyticsSummary>("/fees/analytics", {
      params: { institute_id: instituteId },
    });
    return res.data;
  },

  // Categories & Heads
  getCategories: async (instituteId: string): Promise<FeeCategory[]> => {
    const res = await apiClient.get<FeeCategory[]>("/fees/categories", {
      params: { institute_id: instituteId },
    });
    return res.data;
  },

  createCategory: async (payload: { code: string; name: string; description?: string; institute_id: string; branch_id?: string }): Promise<FeeCategory> => {
    const res = await apiClient.post<FeeCategory>("/fees/categories", payload);
    return res.data;
  },

  getFeeHeads: async (instituteId: string, categoryId?: string): Promise<FeeHead[]> => {
    const res = await apiClient.get<FeeHead[]>("/fees/heads", {
      params: { institute_id: instituteId, category_id: categoryId },
    });
    return res.data;
  },

  createFeeHead: async (payload: { category_id: string; code: string; name: string; default_amount: number; is_refundable: boolean; institute_id: string }): Promise<FeeHead> => {
    const res = await apiClient.post<FeeHead>("/fees/heads", payload);
    return res.data;
  },

  // Structures
  getStructures: async (instituteId: string): Promise<FeeStructure[]> => {
    const res = await apiClient.get<FeeStructure[]>("/fees/structures", {
      params: { institute_id: instituteId },
    });
    return res.data;
  },

  createStructure: async (payload: any): Promise<FeeStructure> => {
    const res = await apiClient.post<FeeStructure>("/fees/structures", payload);
    return res.data;
  },

  // Fee Assignment
  assignFee: async (payload: { student_id: string; fee_structure_id: string; institute_id: string; academic_year_id: string; assignment_type?: string }): Promise<StudentFeeAssignment> => {
    const res = await apiClient.post<StudentFeeAssignment>("/fees/assignments", payload);
    return res.data;
  },

  // Collections & Payments
  collectPayment: async (payload: {
    student_fee_assignment_id: string;
    student_id: string;
    installment_id?: string;
    amount_paid: number;
    payment_mode: string;
    transaction_reference?: string;
    remarks?: string;
  }): Promise<Payment> => {
    const res = await apiClient.post<Payment>("/fees/collections", payload);
    return res.data;
  },

  // Receipts
  getReceipt: async (paymentId: string): Promise<Receipt> => {
    const res = await apiClient.get<Receipt>(`/fees/receipts/${paymentId}`);
    return res.data;
  },

  // Scholarships
  getScholarships: async (instituteId: string): Promise<Scholarship[]> => {
    const res = await apiClient.get<Scholarship[]>("/fees/scholarships", {
      params: { institute_id: instituteId },
    });
    return res.data;
  },

  createScholarship: async (payload: { institute_id: string; code: string; name: string; calculation_type: string; value: number }): Promise<Scholarship> => {
    const res = await apiClient.post<Scholarship>("/fees/scholarships", payload);
    return res.data;
  },

  // Refunds
  processRefund: async (payload: { payment_id: string; student_id: string; institute_id: string; amount: number; refund_type: string; reason: string }): Promise<Refund> => {
    const res = await apiClient.post<Refund>("/fees/refunds", payload);
    return res.data;
  },

  // Reports
  getDailyReport: async (instituteId: string, date: string): Promise<any> => {
    const res = await apiClient.get("/fees/reports/daily-collection", {
      params: { institute_id: instituteId, report_date: date },
    });
    return res.data;
  },

  getOutstandingReport: async (instituteId: string): Promise<any> => {
    const res = await apiClient.get("/fees/reports/outstanding", {
      params: { institute_id: instituteId },
    });
    return res.data;
  },
};
