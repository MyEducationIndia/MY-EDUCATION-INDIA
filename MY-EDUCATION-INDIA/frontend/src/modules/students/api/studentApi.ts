import { httpClient } from "@/api/httpClient";
import {
  StudentCustomFieldItem,
  StudentDetailedProfile,
  StudentSummary,
} from "../types/student.types";

export const studentApi = {
  async searchStudents(params?: {
    query?: string;
    course_name?: string;
    batch_name?: string;
    status?: string;
    page?: number;
    page_size?: number;
  }): Promise<{ items: StudentSummary[]; total: number; page: number; page_size: number }> {
    const res = await httpClient.get<{ items: StudentSummary[]; total: number; page: number; page_size: number }>("/students", {
      params: { ...params, page: params?.page || 1, page_size: params?.page_size || 20 },
    });
    return res.data;
  },

  async getStudentProfile(id: string): Promise<StudentDetailedProfile> {
    const res = await httpClient.get<StudentDetailedProfile>(`/students/${id}`);
    return res.data;
  },

  async registerStudent(payload: any): Promise<StudentDetailedProfile> {
    const res = await httpClient.post<StudentDetailedProfile>("/students", payload);
    return res.data;
  },

  async updateStudentStatus(id: string, newStatus: string, reason?: string): Promise<StudentSummary> {
    const res = await httpClient.patch<StudentSummary>(`/students/${id}/status`, {
      new_status: newStatus,
      reason,
    });
    return res.data;
  },

  async promoteStudents(payload: {
    student_ids: string[];
    target_course_name?: string;
    target_batch_name?: string;
    target_semester_or_year: number;
    target_academic_year_code: string;
  }): Promise<{ success: boolean; promoted_count: number }> {
    const res = await httpClient.post<{ success: boolean; promoted_count: number }>("/students/promote", payload);
    return res.data;
  },

  async bulkDeleteStudents(studentIds: string[]): Promise<{ success: boolean; deleted_count: number }> {
    const res = await httpClient.post<{ success: boolean; deleted_count: number }>("/students/bulk-delete", {
      student_ids: studentIds,
    });
    return res.data;
  },

  async listCustomFields(): Promise<StudentCustomFieldItem[]> {
    const res = await httpClient.get<StudentCustomFieldItem[]>("/students/custom-fields");
    return res.data;
  },
};
