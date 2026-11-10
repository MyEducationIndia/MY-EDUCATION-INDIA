import { httpClient } from "@/api/httpClient";
import {
  CreateAutomationRulePayload,
  CreateWorkflowInstancePayload,
  ExecuteWorkflowActionPayload,
  WorkflowAutomationRuleItem,
  WorkflowDefinitionItem,
  WorkflowEngineSummary,
  WorkflowInstanceItem,
} from "@/types/workflowEngine.types";

export const workflowEngineService = {
  async getSummary(): Promise<WorkflowEngineSummary> {
    const response = await httpClient.get<WorkflowEngineSummary>(
      "/workflows/summary"
    );
    return response.data;
  },

  async listDefinitions(): Promise<WorkflowDefinitionItem[]> {
    const response = await httpClient.get<WorkflowDefinitionItem[]>(
      "/workflows/definitions"
    );
    return response.data;
  },

  async listInstances(params?: {
    status?: string;
    entity_type?: string;
  }): Promise<WorkflowInstanceItem[]> {
    const response = await httpClient.get<WorkflowInstanceItem[]>(
      "/workflows/instances",
      { params }
    );
    return response.data;
  },

  async createInstance(
    payload: CreateWorkflowInstancePayload
  ): Promise<WorkflowInstanceItem> {
    const response = await httpClient.post<WorkflowInstanceItem>(
      "/workflows/instances",
      payload
    );
    return response.data;
  },

  async executeAction(
    instanceId: string,
    payload: ExecuteWorkflowActionPayload
  ): Promise<WorkflowInstanceItem> {
    const response = await httpClient.post<WorkflowInstanceItem>(
      `/workflows/instances/${instanceId}/action`,
      payload
    );
    return response.data;
  },

  async listAutomationRules(): Promise<WorkflowAutomationRuleItem[]> {
    const response = await httpClient.get<WorkflowAutomationRuleItem[]>(
      "/workflows/automation-rules"
    );
    return response.data;
  },

  async createAutomationRule(
    payload: CreateAutomationRulePayload
  ): Promise<WorkflowAutomationRuleItem> {
    const response = await httpClient.post<WorkflowAutomationRuleItem>(
      "/workflows/automation-rules",
      payload
    );
    return response.data;
  },
};
