export interface WorkflowStepItem {
  id: string;
  step_number: number;
  step_name: string;
  approver_role: string;
  approver_department?: string | null;
  timeout_hours: number;
  is_mandatory: boolean;
  auto_action_on_timeout: string;
}

export interface WorkflowDefinitionItem {
  id: string;
  institute_id: string;
  workflow_code: string;
  name: string;
  category: string;
  description: string | null;
  is_multi_level: boolean;
  total_steps: number;
  is_active: boolean;
  steps: WorkflowStepItem[];
  created_at: string;
}

export interface WorkflowApprovalActionItem {
  id: string;
  instance_id: string;
  step_number: number;
  actor_user_id: string | null;
  actor_name: string | null;
  actor_role: string;
  action: "APPROVED" | "REJECTED" | "SENT_BACK" | "ESCALATED";
  remarks: string | null;
  performed_at: string;
}

export interface WorkflowInstanceItem {
  id: string;
  institute_id: string;
  workflow_id: string;
  workflow_code: string;
  workflow_name: string;
  tracking_number: string;
  title: string;
  entity_type: string;
  entity_id: string;
  requester_user_id: string | null;
  requester_name: string | null;
  current_step_number: number;
  total_steps: number;
  status: "PENDING" | "IN_REVIEW" | "APPROVED" | "REJECTED" | "CANCELLED";
  priority: "LOW" | "NORMAL" | "HIGH" | "URGENT";
  payload_data: Record<string, unknown>;
  actions: WorkflowApprovalActionItem[];
  created_at: string;
}

export interface CreateWorkflowInstancePayload {
  workflow_code: string;
  title: string;
  entity_type: string;
  entity_id: string;
  priority?: "LOW" | "NORMAL" | "HIGH" | "URGENT";
  payload_data?: Record<string, unknown>;
}

export interface ExecuteWorkflowActionPayload {
  action: "APPROVED" | "REJECTED" | "SENT_BACK" | "ESCALATED";
  remarks?: string;
}

export interface WorkflowAutomationRuleItem {
  id: string;
  workflow_id?: string | null;
  rule_name: string;
  trigger_event: string;
  condition_expression: Record<string, unknown>;
  action_type: string;
  action_payload: Record<string, unknown>;
  is_active: boolean;
  created_at: string;
}

export interface CreateAutomationRulePayload {
  workflow_id?: string | null;
  rule_name: string;
  trigger_event: string;
  condition_expression?: Record<string, unknown>;
  action_type: string;
  action_payload?: Record<string, unknown>;
}

export interface WorkflowEngineSummary {
  total_active_instances: number;
  pending_my_approval: number;
  completed_this_month: number;
  avg_cycle_time_hours: number;
  pipeline_breakdown: Record<string, number>;
}
