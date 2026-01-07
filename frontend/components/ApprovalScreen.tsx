'use client';

interface ApprovalScreenProps {
  requestId: string;
  approvalData: any;
}

export default function ApprovalScreen({
  requestId,
  approvalData,
}: ApprovalScreenProps) {
  if (!approvalData) return null;

  const { decision, approved_limit, comments } = approvalData;

  const getDecisionColor = (dec: string) => {
    if (dec === 'APPROVE' || dec === 'APPROVE_WITH_CHANGES')
      return 'bg-green-100 text-green-800 border-green-300';
    return 'bg-red-100 text-red-800 border-red-300';
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">
        👤 Human Approval Decision
      </h2>

      <div
        className={`rounded-lg p-6 border-2 ${getDecisionColor(decision)}`}
      >
        <div className="flex justify-between items-start mb-4">
          <div>
            <h3 className="text-lg font-semibold mb-2">Decision</h3>
            <p className="text-3xl font-bold">
              {decision.replace(/_/g, ' ')}
            </p>
          </div>
          {approved_limit && (
            <div className="text-right">
              <p className="text-sm font-semibold mb-1">Approved Limit</p>
              <p className="text-2xl font-bold">
                ₹{(approved_limit / 10000000).toFixed(1)}Cr
              </p>
            </div>
          )}
        </div>

        {comments && (
          <div className="bg-white rounded-lg p-4 mt-4">
            <h4 className="font-semibold mb-2">Approver Comments</h4>
            <p className="text-gray-700">{comments}</p>
          </div>
        )}
      </div>

      <div className="mt-4 text-sm text-gray-500 text-center">
        ℹ️ This step represents human-in-the-loop control. In production, the
        workflow pauses here until a credit controller makes a decision.
      </div>
    </div>
  );
}
