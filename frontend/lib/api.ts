/**
 * API Client for CreditWorkflowAgent
 */

import axios from 'axios';

const getApiBase = () => {
  if (process.env.NEXT_PUBLIC_API_BASE) {
    return process.env.NEXT_PUBLIC_API_BASE;
  }

  // Auto-detect Codespaces environment
  if (typeof window !== 'undefined' && window.location.hostname.endsWith('.app.github.dev')) {
    // Codespaces usually forwards ports to <host>-<port>.app.github.dev
    // Frontend is on 3000, Backend is on 8000. Replace -3000 with -8000 in hostname
    const newHost = window.location.hostname.replace('-3000', '-8000');
    return `${window.location.protocol}//${newHost}`;
  }

  return 'http://localhost:8000';
};

const API_BASE = getApiBase();

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
