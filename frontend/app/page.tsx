'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

export default function Home() {
  const router = useRouter();
  const [customers, setCustomers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [runningDemo, setRunningDemo] = useState(false);

  useEffect(() => {
    loadCustomers();
  }, []);

  const loadCustomers = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/demo/customers`);
      setCustomers(response.data.customers);
    } catch (error) {
      console.error('Error loading customers:', error);
    } finally {
      setLoading(false);
    }
  };

  const runDemoScenario = async (scenario: string) => {
    setRunningDemo(true);
    try {
      const response = await axios.post(`${API_BASE}/api/demo/quick-run/${scenario}`);
      const requestId = response.data.request_id;

      // Navigate to workflow page
      router.push(`/workflow/${requestId}`);
    } catch (error) {
      console.error('Error running demo:', error);
      alert('Failed to run demo. Check console for details.');
    } finally {
      setRunningDemo(false);
    }
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🤖 CreditWorkflowAgent
          </h1>
          <p className="text-xl text-gray-600 mb-2">
            AI-Powered Credit Controller with Human-in-the-Loop
          </p>
          <p className="text-gray-500">
            Demo system showcasing end-to-end credit workflow with AI analysis,
            human approval, and SAP S/4HANA integration
          </p>
        </div>

        {/* Demo Scenarios */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            🎬 Quick Demo Scenarios
          </h2>
          <p className="text-gray-600 mb-6">
            Run a complete 5-step workflow with one click:
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button
              onClick={() => runDemoScenario('unblock-good')}
              disabled={runningDemo}
              className="bg-green-600 hover:bg-green-700 text-white font-semibold py-4 px-6 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              <div className="text-lg mb-2">✅ Unblock - Good Customer</div>
              <div className="text-sm opacity-90">
                Low risk, cleared overdue
              </div>
            </button>

            <button
              onClick={() => runDemoScenario('unblock-risky')}
              disabled={runningDemo}
              className="bg-yellow-600 hover:bg-yellow-700 text-white font-semibold py-4 px-6 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              <div className="text-lg mb-2">⚠️ Unblock - Risky Customer</div>
              <div className="text-sm opacity-90">
                High DSO, overdue amounts
              </div>
            </button>

            <button
              onClick={() => runDemoScenario('limit-increase')}
              disabled={runningDemo}
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 px-6 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              <div className="text-lg mb-2">📈 Credit Limit Increase</div>
              <div className="text-sm opacity-90">
                Excellent payment history
              </div>
            </button>
          </div>

          {runningDemo && (
            <div className="mt-4 text-center text-gray-600">
              <div className="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-gray-900 mr-2"></div>
              Running demo workflow...
            </div>
          )}
        </div>

        {/* Customer List */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            👥 Demo Customers
          </h2>

          {loading ? (
            <div className="text-center py-8 text-gray-600">Loading...</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Customer
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Segment
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Credit Limit
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Risk
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {customers.map((customer) => (
                    <tr key={customer.customer_id}>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">
                          {customer.name}
                        </div>
                        <div className="text-sm text-gray-500">
                          {customer.customer_id}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {customer.segment}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        ₹{(customer.current_limit / 10000000).toFixed(1)}Cr
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span
                          className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                            customer.risk_category === 'A'
                              ? 'bg-green-100 text-green-800'
                              : customer.risk_category === 'B'
                              ? 'bg-yellow-100 text-yellow-800'
                              : customer.risk_category === 'C'
                              ? 'bg-orange-100 text-orange-800'
                              : 'bg-red-100 text-red-800'
                          }`}
                        >
                          {customer.risk_category}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {customer.credit_block ? (
                          <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                            🔒 Blocked
                          </span>
                        ) : (
                          <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                            ✅ Active
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-gray-500 text-sm">
          <p>
            CreditWorkflowAgent v1.0.0 | Demo System | FastAPI + LangGraph + Next.js
          </p>
        </div>
      </div>
    </main>
  );
}
