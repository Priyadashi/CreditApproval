'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import axios from 'axios';
import Timeline from '@/components/Timeline';
import AnalysisPanel from '@/components/AnalysisPanel';
import ApprovalScreen from '@/components/ApprovalScreen';
import NotificationLog from '@/components/NotificationLog';

const API_BASE = 'http://localhost:8000';

export default function WorkflowPage() {
  const params = useParams();
  const router = useRouter();
  const requestId = params.id as string;

  const [workflowData, setWorkflowData] = useState<any>(null);
  const [events, setEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (requestId) {
      loadWorkflowData();
      const interval = setInterval(loadWorkflowData, 2000); // Poll every 2s
      return () => clearInterval(interval);
    }
  }, [requestId]);

  const loadWorkflowData = async () => {
    try {
      // Load workflow status
      const statusResponse = await axios.get(
        `${API_BASE}/api/workflow/status/${requestId}`
      );
      setWorkflowData(statusResponse.data);

      // Load events
      try {
        const eventsResponse = await axios.get(
          `${API_BASE}/api/workflow/events/${requestId}`
        );
        setEvents(eventsResponse.data);
      } catch (err) {
        // Events might not exist yet
        console.log('No events yet');
      }

      setLoading(false);
    } catch (err: any) {
      console.error('Error loading workflow:', err);
      setError(err.response?.data?.detail || 'Failed to load workflow');
      setLoading(false);
    }
  };

  if (loading && !workflowData) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mb-4"></div>
          <p className="text-gray-600">Loading workflow...</p>
        </div>
      </div>
    );
  }

  if (error && !workflowData) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="bg-red-50 border border-red-200 rounded-lg p-8 max-w-md">
          <h2 className="text-xl font-bold text-red-900 mb-2">Error</h2>
          <p className="text-red-700">{error}</p>
          <button
            onClick={() => router.push('/')}
            className="mt-4 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
          >
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  const isCompleted = workflowData?.status === 'completed';
  const summary = workflowData?.result;

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Credit Workflow
              </h1>
              <p className="text-gray-600">Request ID: {requestId}</p>
            </div>
            <button
              onClick={() => router.push('/')}
              className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-4 py-2 rounded-lg transition"
            >
              ← Back
            </button>
          </div>

          {/* Status Badge */}
          <div className="mt-4">
            <span
              className={`px-4 py-2 rounded-full text-sm font-semibold ${
                workflowData?.status === 'running'
                  ? 'bg-blue-100 text-blue-800'
                  : workflowData?.status === 'completed'
                  ? 'bg-green-100 text-green-800'
                  : 'bg-red-100 text-red-800'
              }`}
            >
              {workflowData?.status === 'running' && '⏳ Running'}
              {workflowData?.status === 'completed' && '✅ Completed'}
              {workflowData?.status === 'failed' && '❌ Failed'}
            </span>
          </div>
        </div>

        {/* Timeline */}
        <div className="mb-6">
          <Timeline events={events} />
        </div>

        {/* Analysis Panel */}
        {events.find((e) => e.step === 'AI Analysis & Recommendation') && (
          <div className="mb-6">
            <AnalysisPanel
              analysisData={
                events.find((e) => e.step === 'AI Analysis & Recommendation')
                  ?.payload
              }
            />
          </div>
        )}

        {/* Approval Screen */}
        {events.find((e) => e.step === 'Human Approval') && (
          <div className="mb-6">
            <ApprovalScreen
              requestId={requestId}
              approvalData={
                events.find((e) => e.step === 'Human Approval')?.payload
              }
            />
          </div>
        )}

        {/* Notification Log */}
        {events.find((e) => e.step === 'Notification') && (
          <div className="mb-6">
            <NotificationLog
              notificationData={
                events.find((e) => e.step === 'Notification')?.payload
              }
            />
          </div>
        )}

        {/* Final Summary (Demo Talk Track) */}
        {isCompleted && summary && (
          <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              🎯 Workflow Summary
            </h2>

            <div className="bg-white rounded-lg p-6 mb-6">
              <h3 className="font-semibold text-gray-900 mb-2">Overview</h3>
              <p className="text-gray-700">{summary.workflow_summary}</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-white rounded-lg p-4">
                <h4 className="text-sm font-semibold text-gray-500 mb-1">
                  Final Decision
                </h4>
                <p
                  className={`text-2xl font-bold ${
                    summary.final_decision === 'APPROVED'
                      ? 'text-green-600'
                      : 'text-red-600'
                  }`}
                >
                  {summary.final_decision}
                </p>
              </div>

              <div className="bg-white rounded-lg p-4">
                <h4 className="text-sm font-semibold text-gray-500 mb-1">
                  Credit Limit
                </h4>
                <p className="text-2xl font-bold text-gray-900">
                  ₹{(summary.final_credit_limit / 10000000).toFixed(1)}Cr
                </p>
              </div>

              <div className="bg-white rounded-lg p-4">
                <h4 className="text-sm font-semibold text-gray-500 mb-1">
                  Block Status
                </h4>
                <p className="text-2xl font-bold">
                  {summary.final_block_status ? '🔒 Blocked' : '✅ Active'}
                </p>
              </div>
            </div>

            {/* Demo Talk Track */}
            <div className="bg-white rounded-lg p-6">
              <h3 className="font-semibold text-gray-900 mb-3 flex items-center">
                <span className="mr-2">🎤</span>
                Demo Talk Track (For Presentation)
              </h3>
              <ul className="space-y-2">
                {summary.demo_talk_track.map((point: string, idx: number) => (
                  <li key={idx} className="flex items-start">
                    <span className="text-blue-600 mr-2 font-bold">
                      {idx + 1}.
                    </span>
                    <span className="text-gray-700">{point}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
