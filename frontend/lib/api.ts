/**
 * API Client for CreditWorkflowAgent
 */

import axios from 'axios';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface CreditRequest {
  request_id: string;
  customer_id: string;
  request_type: 'BLOCK' | 'UNBLOCK' | 'LIMIT_INCREASE';
  requested_limit?: number;
  reason: string;
  requestor: {
    name: string;
    email: string;
  };
}

export interface ApproverDecision {
  decision: 'APPROVE' | 'APPROVE_WITH_CHANGES' | 'REJECT';
  approved_limit?: number;
  comments: string;
}

export const api = {
  // Health check
  health: () => apiClient.get('/health'),

  // Credit requests
  createRequest: (request: CreditRequest) =>
    apiClient.post('/api/requests', request),

  getRequest: (requestId: string) =>
    apiClient.get(`/api/requests/${requestId}`),

  // Customer data
  getCustomer: (customerId: string) =>
    apiClient.get(`/api/customers/${customerId}`),

  // Workflow
  startWorkflow: (requestId: string) =>
    apiClient.post(`/api/workflow/start/${requestId}`),

  getWorkflowStatus: (requestId: string) =>
    apiClient.get(`/api/workflow/status/${requestId}`),

  getWorkflowEvents: (requestId: string) =>
    apiClient.get(`/api/workflow/events/${requestId}`),

  getWorkflowSummary: (requestId: string) =>
    apiClient.get(`/api/workflow/summary/${requestId}`),

  submitApproval: (requestId: string, decision: ApproverDecision) =>
    apiClient.post(`/api/workflow/approve/${requestId}`, decision),

  // Demo
  runDemoScenario: (scenario: string) =>
    apiClient.post(`/api/demo/quick-run/${scenario}`),

  listDemoCustomers: () => apiClient.get('/api/demo/customers'),
};

export default apiClient;
