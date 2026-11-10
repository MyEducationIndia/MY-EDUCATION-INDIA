export type ReportCategory = "ACADEMIC" | "FINANCIAL" | "ADMISSION" | "ATTENDANCE" | "EXAM" | "LXP" | "CRM" | "SYSTEM";
export type ExportFormat = "PDF" | "EXCEL" | "CSV" | "DOCX" | "JSON";
export type ChartType = "BAR" | "LINE" | "AREA" | "PIE" | "DONUT" | "STACKED" | "RADAR" | "SCATTER" | "HEATMAP" | "GAUGE" | "FUNNEL" | "TREEMAP";

export interface ReportDefinition {
  id: string;
  instituteId: string;
  reportCode: string;
  reportName: string;
  category: ReportCategory;
  description?: string;
  sourceTables: string[];
  selectedFields: any[];
  isSystemReport: boolean;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface KpiDefinition {
  id: string;
  kpiKey: string;
  kpiName: string;
  category: string;
  calculationFormula: string;
  targetValue: number;
  currentValue: number;
  unit: string;
  trendDirection: "UP" | "DOWN" | "STABLE";
}

export interface ExecutiveDashboardMetrics {
  admissionsCount: number;
  totalRevenueInr: number;
  pendingFeesInr: number;
  feeCollectionRatePercentage: number;
  averageAttendancePercentage: number;
  examPassPercentage: number;
  activeCourseEnrollments: number;
  leadConversionRatePercentage: number;
  instituteHealthScore: number;
}

export interface SystemHealthOverview {
  overallStatus: "HEALTHY" | "DEGRADED" | "DOWN";
  components: {
    name: string;
    status: string;
    latencyMs: number;
    errorRate: number;
  }[];
}
