import { apiClient } from "@/lib/api/apiClient";
import {
  AttendanceDashboardSummary,
  AttendanceRule,
  AttendanceSession,
  FacultyAttendanceRecord,
  LeaveRequest,
  LeaveType,
  StudentAttendanceRecord,
} from "../types/attendance.types";

export const attendanceService = {
  // Analytics & KPIs
  getDashboardAnalytics: async (instituteId: string): Promise<AttendanceDashboardSummary> => {
    const res = await apiClient.get<AttendanceDashboardSummary>("/attendance/analytics", {
      params: { institute_id: instituteId },
    });
    return res.data;
  },

  // Sessions & Student Attendance
  createSession: async (payload: {
    institute_id: string;
    branch_id?: string;
    course_id?: string;
    batch_id?: string;
    section_id?: string;
    subject_id?: string;
    session_date: string;
    session_type: string;
    period_number?: number;
    attendance_records: Array<{ student_id: string; status: string; remarks?: string }>;
  }): Promise<AttendanceSession> => {
    const res = await apiClient.post<AttendanceSession>("/attendance/sessions", payload);
    return res.data;
  },

  // QR Code Instant Log
  scanQRAttendance: async (sessionId: string, studentId: string, qrToken: string): Promise<StudentAttendanceRecord> => {
    const res = await apiClient.post<StudentAttendanceRecord>(
      "/attendance/qr-scan",
      { student_qr_token: qrToken, session_id: sessionId },
      { params: { student_id: studentId } }
    );
    return res.data;
  },

  // Faculty Attendance
  facultyClock: async (payload: {
    faculty_user_id: string;
    institute_id: string;
    action_type: "CLOCK_IN" | "CLOCK_OUT";
    method?: string;
  }): Promise<FacultyAttendanceRecord> => {
    const res = await apiClient.post<FacultyAttendanceRecord>("/attendance/faculty/clock", payload);
    return res.data;
  },

  // Leaves
  getLeaveTypes: async (instituteId: string): Promise<LeaveType[]> => {
    const res = await apiClient.get<LeaveType[]>("/attendance/leave-types", {
      params: { institute_id: instituteId },
    });
    return res.data;
  },

  applyLeave: async (payload: {
    institute_id: string;
    user_id: string;
    user_type: string;
    leave_type_id: string;
    start_date: string;
    end_date: string;
    reason: string;
  }): Promise<LeaveRequest> => {
    const res = await apiClient.post<LeaveRequest>("/attendance/leaves/apply", payload);
    return res.data;
  },

  takeLeaveAction: async (leaveRequestId: string, action: "APPROVED" | "REJECTED", comments?: string): Promise<LeaveRequest> => {
    const res = await apiClient.post<LeaveRequest>("/attendance/leaves/action", {
      leave_request_id: leaveRequestId,
      action,
      comments,
    });
    return res.data;
  },

  // Reports
  getDailyReport: async (instituteId: string, date: string): Promise<any> => {
    const res = await apiClient.get("/attendance/reports/daily", {
      params: { institute_id: instituteId, report_date: date },
    });
    return res.data;
  },

  // Rules
  configureRules: async (payload: Partial<AttendanceRule>): Promise<AttendanceRule> => {
    const res = await apiClient.post<AttendanceRule>("/attendance/rules", payload);
    return res.data;
  },
};
