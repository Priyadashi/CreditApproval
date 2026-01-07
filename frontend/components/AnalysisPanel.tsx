'use client';

interface AnalysisPanelProps {
  analysisData: any;
}

export default function AnalysisPanel({ analysisData }: AnalysisPanelProps) {
  if (!analysisData) return null;

  const {
    recommendation,
    confidence,
    rationale,
    key_metrics,
    risk_signals,
  } = analysisData;

  const getRecommendationColor = (rec: string) => {
    if (rec.includes('RELEASE') || rec.includes('FULL')) return 'text-green-600';
    if (rec.includes('MAINTAIN') || rec.includes('REJECT')) return 'text-red-600';
    return 'text-yellow-600';
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">
        🤖 AI Analysis & Recommendation
      </h2>

      {/* Recommendation Card */}
      <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-lg p-6 mb-6 border-2 border-purple-200">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-700 mb-2">
              AI Recommendation
            </h3>
            <p className={`text-3xl font-bold ${getRecommendationColor(recommendation)}`}>
              {recommendation.replace(/_/g, ' ')}
            </p>
          </div>
          <div className="text-right">
            <p className="text-sm text-gray-600 mb-1">Confidence</p>
            <p className="text-3xl font-bold text-purple-600">
              {(confidence * 100).toFixed(0)}%
            </p>
          </div>
        </div>

        <div className="bg-white rounded-lg p-4">
          <h4 className="font-semibold text-gray-700 mb-2">Rationale</h4>
          <p className="text-gray-700">{rationale}</p>
        </div>
      </div>

      {/* Key Metrics Grid */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Key Metrics Analyzed
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {key_metrics && (
            <>
              <div className="bg-blue-50 rounded-lg p-4 text-center">
                <p className="text-sm text-gray-600 mb-1">DSO</p>
                <p className="text-2xl font-bold text-blue-600">
                  {key_metrics.dso?.toFixed(0)}
                </p>
                <p className="text-xs text-gray-500">days</p>
              </div>

              <div className="bg-green-50 rounded-lg p-4 text-center">
                <p className="text-sm text-gray-600 mb-1">Utilisation</p>
                <p className="text-2xl font-bold text-green-600">
                  {key_metrics.utilisation_pct?.toFixed(1)}%
                </p>
              </div>

              <div className="bg-yellow-50 rounded-lg p-4 text-center">
                <p className="text-sm text-gray-600 mb-1">Overdue</p>
                <p className="text-2xl font-bold text-yellow-600">
                  {key_metrics.overdue_pct?.toFixed(1)}%
                </p>
              </div>

              <div className="bg-purple-50 rounded-lg p-4 text-center">
                <p className="text-sm text-gray-600 mb-1">Risk</p>
                <p className="text-2xl font-bold text-purple-600">
                  {key_metrics.risk_category}
                </p>
              </div>

              <div className="bg-gray-50 rounded-lg p-4 text-center">
                <p className="text-sm text-gray-600 mb-1">Outstanding</p>
                <p className="text-2xl font-bold text-gray-600">
                  ₹{(key_metrics.total_outstanding / 10000000).toFixed(1)}Cr
                </p>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Risk Signals */}
      {risk_signals && risk_signals.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            ⚠️ Risk Signals Identified
          </h3>
          <div className="space-y-2">
            {risk_signals.map((signal: string, idx: number) => (
              <div
                key={idx}
                className="bg-red-50 border border-red-200 rounded-lg p-3 flex items-center"
              >
                <span className="text-red-600 mr-3">⚠️</span>
                <span className="text-red-800">{signal}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {(!risk_signals || risk_signals.length === 0) && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-center">
            <span className="text-green-600 mr-3 text-2xl">✅</span>
            <span className="text-green-800 font-semibold">
              No significant risk signals detected
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
