export type LeadPriority = "LOW" | "MEDIUM" | "HIGH" | "URGENT";
export type LeadStage = 
  | "NEW_LEAD" | "CONTACTED" | "COUNSELLING" | "DEMO_GIVEN"
  | "INTERESTED" | "DOCUMENTS_PENDING" | "FEE_DISCUSSION"
  | "ADMISSION_CONFIRMED" | "LOST";

export interface CrmLead {
  id: string;
  instituteId: string;
  leadCode: string;
  fullName: string;
  mobile: string;
  email?: string;
  guardianName?: string;
  courseInterestedId?: string;
  priority: LeadPriority;
  assignedCounsellorId?: string;
  stage: LeadStage;
  status: "ACTIVE" | "CONVERTED" | "DROPPED";
  score: number;
  expectedAdmissionDate?: string;
  remarks?: string;
  createdAt: string;
  updatedAt: string;
}

export interface CrmEnquiry {
  id: string;
  instituteId: string;
  enquiryCode: string;
  enquirerName: string;
  mobile: string;
  email?: string;
  sourceType: string;
  courseId?: string;
  message?: string;
  isConvertedToLead: bool;
  createdAt: string;
}

export interface CrmFollowup {
  id: string;
  leadId: string;
  counsellorId: string;
  channel: "CALL" | "WHATSAPP" | "SMS" | "EMAIL" | "MEETING" | "VISIT" | "VIDEO_CALL";
  scheduledAt: string;
  notes?: string;
  outcome?: string;
  nextFollowupDate?: string;
}

export interface CrmCampaign {
  id: string;
  campaignName: string;
  channel: string;
  startDate: string;
  endDate?: string;
  allocatedBudget: number;
  actualSpent: number;
  status: "DRAFT" | "ACTIVE" | "PAUSED" | "COMPLETED";
  utmSource?: string;
  utmCampaign?: string;
}

export interface FranchiseCenter {
  id: string;
  centerCode: string;
  centerName: string;
  city: string;
  state: string;
  contactEmail: string;
  contactPhone: string;
  royaltyPercentage: number;
  status: "ACTIVE" | "SUSPENDED" | "PENDING";
}

export interface CrmDashboardMetrics {
  totalNewLeads: number;
  todaysFollowupsCount: number;
  admissionsThisMonth: number;
  conversionRatePercentage: number;
  revenueForecast: number;
  topCounsellor: string;
  activeCampaignsCount: number;
  pendingTasksCount: number;
}
