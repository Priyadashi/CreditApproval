'use client';

import { format } from 'date-fns';

interface TimelineProps {
  events: any[];
}

const stepOrder = [
  'Credit Block Request',
  'AI Analysis & Recommendation',
  'Human Approval',
  'SAP Update',
  'Notification',
];

export default function Timeline({ events }: TimelineProps) {
  // Create array with all steps, marking which ones have events
  const timelineSteps = stepOrder.map((stepName) => {
    const event = events.find((e) => e.step === stepName);
    return {
      name: stepName,
      status: event ? event.status : 'Pending',
      timestamp: event ? event.timestamp : null,
      actor: event ? event.actor : null,
      payload: event ? event.payload : null,
    };
  });

  const getStepIcon = (stepName: string, status: string) => {
    if (status === 'Completed') {
      return '✅';
    } else if (status === 'In Progress') {
      return '⏳';
    } else if (status === 'Rejected') {
      return '❌';
    } else {
      return '⭕';
    }
  };

  const getActorBadge = (actor: string) => {
    const colors = {
      AI: 'bg-purple-100 text-purple-800',
      Human: 'bg-blue-100 text-blue-800',
      SAP: 'bg-green-100 text-green-800',
    };
    return colors[actor as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">
        📊 Workflow Timeline
      </h2>

      <div className="relative">
        {/* Vertical line */}
        <div className="absolute left-8 top-0 bottom-0 w-0.5 bg-gray-300"></div>

        {/* Timeline items */}
        <div className="space-y-6">
          {timelineSteps.map((step, index) => (
            <div key={index} className="relative flex items-start">
              {/* Icon */}
              <div
                className={`relative z-10 flex items-center justify-center w-16 h-16 rounded-full text-2xl ${
                  step.status === 'Completed'
                    ? 'bg-green-100'
                    : step.status === 'In Progress'
                    ? 'bg-blue-100'
                    : step.status === 'Rejected'
                    ? 'bg-red-100'
                    : 'bg-gray-100'
                }`}
              >
                {getStepIcon(step.name, step.status)}
              </div>

              {/* Content */}
              <div className="ml-6 flex-1">
                <div className="bg-gray-50 rounded-lg p-4 border-l-4 border-blue-500">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {step.name}
                    </h3>
                    {step.actor && (
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-semibold ${getActorBadge(
                          step.actor
                        )}`}
                      >
                        {step.actor}
                      </span>
                    )}
                  </div>

                  <div className="flex items-center mb-2">
                    <span
                      className={`px-2 py-1 rounded text-xs font-semibold ${
                        step.status === 'Completed'
                          ? 'bg-green-200 text-green-800'
                          : step.status === 'In Progress'
                          ? 'bg-blue-200 text-blue-800'
                          : step.status === 'Rejected'
                          ? 'bg-red-200 text-red-800'
                          : 'bg-gray-200 text-gray-600'
                      }`}
                    >
                      {step.status}
                    </span>
                    {step.timestamp && (
                      <span className="ml-3 text-sm text-gray-500">
                        {format(new Date(step.timestamp), 'MMM dd, yyyy HH:mm:ss')}
                      </span>
                    )}
                  </div>

                  {/* Step-specific details */}
                  {step.payload && (
                    <div className="mt-3 text-sm text-gray-700">
                      {step.name === 'Credit Block Request' && (
                        <div>
                          <p>
                            <strong>Type:</strong> {step.payload.request_type}
                          </p>
                          <p>
                            <strong>Requestor:</strong>{' '}
                            {step.payload.requestor?.name}
                          </p>
                        </div>
                      )}
                      {step.name === 'AI Analysis & Recommendation' && (
                        <div>
                          <p>
                            <strong>Recommendation:</strong>{' '}
                            {step.payload.recommendation}
                          </p>
                          <p>
                            <strong>Confidence:</strong>{' '}
                            {(step.payload.confidence * 100).toFixed(0)}%
                          </p>
                        </div>
                      )}
                      {step.name === 'Human Approval' && (
                        <div>
                          <p>
                            <strong>Decision:</strong> {step.payload.decision}
                          </p>
                        </div>
                      )}
                      {step.name === 'SAP Update' && (
                        <div>
                          <p>
                            <strong>Action:</strong>{' '}
                            {step.payload.action_taken || 'No action'}
                          </p>
                          <p>
                            <strong>SAP Ref:</strong>{' '}
                            {step.payload.sap_reference_id || 'N/A'}
                          </p>
                        </div>
                      )}
                      {step.name === 'Notification' && (
                        <div>
                          <p>
                            <strong>Sent to:</strong>{' '}
                            {step.payload.email_sent_to}
                          </p>
                          <p>
                            <strong>Subject:</strong> {step.payload.subject}
                          </p>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
