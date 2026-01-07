'use client';

import { format } from 'date-fns';

interface NotificationLogProps {
  notificationData: any;
}

export default function NotificationLog({
  notificationData,
}: NotificationLogProps) {
  if (!notificationData) return null;

  const { email_sent_to, subject, timestamp } = notificationData;

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">
        📧 Notification Log
      </h2>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <div className="flex items-center mb-4">
          <span className="text-4xl mr-4">✉️</span>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              Email Notification Sent
            </h3>
            <p className="text-sm text-gray-600">
              {format(new Date(timestamp), 'MMM dd, yyyy HH:mm:ss')}
            </p>
          </div>
        </div>

        <div className="bg-white rounded-lg p-4 space-y-3">
          <div>
            <p className="text-sm font-semibold text-gray-600">To:</p>
            <p className="text-gray-900">{email_sent_to}</p>
          </div>
          <div>
            <p className="text-sm font-semibold text-gray-600">Subject:</p>
            <p className="text-gray-900">{subject}</p>
          </div>
        </div>

        <div className="mt-4 text-sm text-gray-600 bg-white rounded-lg p-3">
          <p className="flex items-center">
            <span className="mr-2">ℹ️</span>
            In production, this integrates with email service (SendGrid, AWS SES,
            etc.)
          </p>
        </div>
      </div>
    </div>
  );
}
