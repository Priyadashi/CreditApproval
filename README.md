# 🤖 CreditWorkflowAgent

**AI-Powered Credit Controller with Human-in-the-Loop Workflow**

A full-stack demo system showcasing an agentic AI credit controller for an executive presentation. This system demonstrates end-to-end credit workflow automation with explainable AI, human oversight, and SAP S/4HANA integration.

---

## 🎯 System Overview

**CreditWorkflowAgent** is a production-ready demo that implements a complete 5-step credit workflow:

1. **Credit Block Trigger** - Receive and validate credit request
2. **AI Analysis & Recommendation** - Analyze customer data using GPT-4
3. **Human Approval** - Human-in-the-loop decision point
4. **SAP Update** - Execute changes in SAP S/4HANA (mock/real)
5. **Notification** - Inform requestor of decision

### Key Features

- ✅ **Explainable AI** - Every recommendation includes rationale, confidence, and risk signals
- ✅ **Human-in-the-Loop** - Mandatory approval step ensures humans stay in control
- ✅ **SAP Integration** - Mock and real SAP S/4HANA adapters
- ✅ **Real-time Timeline** - Visual workflow tracking with 5-step timeline
- ✅ **Demo-First Design** - Built for executive presentations with talk tracks
- ✅ **Production Ready** - FastAPI backend, Next.js frontend, Docker deployment

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                       │
│  • Timeline UI    • Analysis Panel    • Approval Screen    │
└───────────────────────┬─────────────────────────────────────┘
                        │ REST API
┌───────────────────────▼─────────────────────────────────────┐
│                  Backend (FastAPI)                          │
│  ┌─────────────────────────────────────────────────┐       │
│  │         CreditWorkflowAgent (LangGraph)         │       │
│  │   • GPT-4 Analysis    • Workflow Orchestration  │       │
│  └─────────────────────────────────────────────────┘       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Credit Tools │  │  SAP Adapter │  │  Event Store │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└───────────────────────┬─────────────────────────────────────┘
                        │
                   ┌────▼─────┐
                   │ SAP S/4  │
                   │ HANA     │
                   └──────────┘
```

### Tech Stack

**Backend:**
- FastAPI (Python)
- LangChain + LangGraph
- OpenAI GPT-4
- Pydantic for data validation

**Frontend:**
- Next.js 14 (React)
- TypeScript
- Tailwind CSS
- Axios for API calls

**Infrastructure:**
- Docker & Docker Compose
- Mock SAP adapter (extensible to real SAP OData)

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- OpenAI API key
- (Optional) SAP S/4HANA credentials for real integration

### 1. Clone Repository

```bash
git clone <repository-url>
cd CreditApproval
```

### 2. Configure Environment

```bash
cd backend
cp .env.example .env
```

Edit `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
ENVIRONMENT=demo
SAP_MODE=mock
```

### 3. Start Services

```bash
# From project root
docker-compose up --build
```

This starts:
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

### 4. Access Demo

Open browser to **http://localhost:3000**

---

## 🎬 Running Demo Scenarios

The system includes 3 pre-configured demo scenarios:

### Scenario 1: Unblock - Good Customer
**Customer:** Tata Steel Limited
**Situation:** Customer cleared 80% of overdue invoices
**Expected AI Recommendation:** RELEASE_BLOCK
**Risk Level:** Low

### Scenario 2: Unblock - Risky Customer
**Customer:** Mahindra & Mahindra
**Situation:** High DSO, significant overdue amounts
**Expected AI Recommendation:** MAINTAIN_BLOCK
**Risk Level:** High

### Scenario 3: Credit Limit Increase
**Customer:** Reliance Industries Ltd
**Situation:** Excellent payment history, expanding relationship
**Expected AI Recommendation:** FULL_LIMIT_INCREASE
**Risk Level:** Very Low

### Running a Demo

**Option A: Via UI (Recommended)**
1. Go to http://localhost:3000
2. Click any scenario button
3. Workflow runs automatically
4. View real-time timeline and results

**Option B: Via API**
```bash
curl -X POST http://localhost:8000/api/demo/quick-run/unblock-good
```

---

## 📊 Understanding the Workflow

### Step 1: Credit Block Request
- **Actor:** Human (Credit Controller)
- **Action:** Submit request for unblock/limit increase
- **Data Captured:** Customer ID, request type, reason, requestor

### Step 2: AI Analysis & Recommendation
- **Actor:** AI (GPT-4)
- **Analysis:**
  - DSO (Days Sales Outstanding)
  - Utilisation percentage
  - Ageing buckets (0-30, 31-60, 61-90, 90+ days)
  - Risk category (A/B/C/D)
- **Output:**
  - Recommendation (5 types)
  - Confidence score
  - Rationale
  - Risk signals

### Step 3: Human Approval
- **Actor:** Human (Credit Manager)
- **Decision Options:**
  - ✅ APPROVE - Accept AI recommendation
  - ✅ APPROVE_WITH_CHANGES - Modify AI recommendation
  - ❌ REJECT - Deny request
- **Critical:** Workflow BLOCKS here until decision received

### Step 4: SAP Update
- **Actor:** SAP System
- **Actions:**
  - Update credit limit in SAP
  - Release/maintain credit block
- **Output:** SAP reference ID

### Step 5: Notification
- **Actor:** AI (System)
- **Action:** Send email to requestor with decision and details

---

## 🔧 API Endpoints

### Health & Info
```bash
GET  /health                    # Health check
GET  /                         # API info
```

### Credit Requests
```bash
POST /api/requests             # Create credit request
GET  /api/requests/{id}        # Get request details
```

### Customer Data
```bash
GET  /api/customers/{id}       # Get customer snapshot
```

### Workflow
```bash
POST /api/workflow/start/{id}        # Start workflow
GET  /api/workflow/status/{id}       # Get status
GET  /api/workflow/events/{id}       # Get timeline events
GET  /api/workflow/summary/{id}      # Get final summary
POST /api/workflow/approve/{id}      # Submit approval
```

### Demo
```bash
POST /api/demo/quick-run/{scenario}  # Run demo scenario
GET  /api/demo/customers             # List demo customers
```

---

## 🎤 Demo Talk Track (For Presentation)

Use these talking points when presenting:

### Opening
> "Today we're showcasing CreditWorkflowAgent - an AI system that doesn't just make recommendations, but drives an entire credit workflow from analysis to execution."

### Step 1
> "A credit controller raises a request to unblock a customer. The system captures all context - who's requesting, why, and for which customer."

### Step 2
> "Our AI agent analyzes the customer's financial position in real-time. It examines DSO, ageing, utilisation - all the metrics a senior credit controller would review. But it does this in seconds, not hours."

> "Notice the AI provides a recommendation WITH a confidence score and clear rationale. This isn't a black box - every decision is explainable."

### Step 3
> "Here's where humans stay in control. The workflow STOPS and waits for human approval. The AI recommends, but humans decide. This is true human-in-the-loop design."

### Step 4
> "Once approved, the system automatically updates SAP S/4HANA. No manual data entry, no errors. The change happens instantly with full audit trail."

### Step 5
> "Finally, all stakeholders are notified automatically. The requestor gets immediate feedback on their request."

### Closing
> "This is enterprise AI done right: fast, explainable, and always with humans in control. We've reduced credit decision time from days to minutes while maintaining governance."

---

## 🛠️ Development

### Project Structure

```
CreditApproval/
├── backend/
│   ├── app/
│   │   ├── workflow/
│   │   │   ├── agent.py           # Core AI agent
│   │   │   └── graph.py           # LangGraph workflow
│   │   ├── tools/
│   │   │   ├── credit_tools.py    # 7 tool contracts
│   │   │   └── sap_adapter.py     # SAP integration
│   │   ├── models/
│   │   │   └── schemas.py         # Pydantic models
│   │   ├── api/
│   │   │   └── routes.py          # FastAPI routes
│   │   └── main.py                # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app/
│   │   ├── page.tsx              # Home page
│   │   └── workflow/[id]/
│   │       └── page.tsx          # Workflow detail
│   ├── components/
│   │   ├── Timeline.tsx          # 5-step timeline
│   │   ├── AnalysisPanel.tsx    # AI analysis UI
│   │   ├── ApprovalScreen.tsx   # Approval interface
│   │   └── NotificationLog.tsx  # Notification display
│   ├── lib/
│   │   └── api.ts               # API client
│   └── package.json
├── docker-compose.yml
└── README.md
```

### Running Locally (Without Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Adding Real SAP Integration

1. Edit `backend/app/tools/sap_adapter.py`
2. Implement `_real_update_credit_limit()` and `_real_update_credit_block()`
3. Update `.env`:
   ```env
   SAP_MODE=real
   SAP_API_URL=https://your-sap-system.com/sap/opu/odata/sap/
   SAP_API_KEY=your_api_key
   ```

Example SAP OData call:
```python
import httpx

async def _real_update_credit_limit(self, customer_id: str, new_limit: float, reason: str):
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{self.api_url}API_BUSINESS_PARTNER/A_Customer('{customer_id}')",
            headers={
                "Authorization": f"Basic {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "CreditLimitAmount": new_limit,
                "CreditLimitNotes": reason
            }
        )
        return SAPUpdateResponse(...)
```

---

## 📈 Extending the System

### Add New Recommendation Type

1. Edit `backend/app/models/schemas.py`:
```python
class RecommendationType(str, Enum):
    # ... existing types
    TEMPORARY_UNBLOCK = "TEMPORARY_UNBLOCK"
```

2. Update agent logic in `backend/app/workflow/agent.py`

### Add New Workflow Step

1. Define new step in workflow
2. Update timeline component
3. Add event emission in agent

### Integrate with Email Service

Edit `backend/app/tools/credit_tools.py`:
```python
import sendgrid
from sendgrid.helpers.mail import Mail

def send_notification(self, email: str, subject: str, body: str):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    message = Mail(
        from_email='noreply@company.com',
        to_emails=email,
        subject=subject,
        html_content=body
    )
    response = sg.send(message)
    return {"success": True, "notification": {...}}
```

---

## 🔒 Security Considerations

For production deployment:

1. **Authentication:** Add JWT auth to all API endpoints
2. **Authorization:** Implement role-based access control
3. **API Keys:** Use secret management (AWS Secrets Manager, Azure Key Vault)
4. **Rate Limiting:** Add rate limiting to prevent abuse
5. **Input Validation:** Already implemented with Pydantic
6. **HTTPS:** Enforce TLS in production
7. **Audit Logging:** Log all workflow decisions and changes

---

## 📝 Demo Data

The system includes 3 demo customers:

### Customer 1: Tata Steel Limited (CUST001)
- Segment: Large Enterprise
- Credit Limit: ₹50Cr
- Risk: B
- Status: Blocked
- Characteristics: High DSO but clearing overdue

### Customer 2: Reliance Industries Ltd (CUST002)
- Segment: Large Enterprise
- Credit Limit: ₹100Cr
- Risk: A
- Status: Active
- Characteristics: Excellent payment history

### Customer 3: Mahindra & Mahindra (CUST003)
- Segment: Mid Enterprise
- Credit Limit: ₹25Cr
- Risk: C
- Status: Blocked
- Characteristics: High overdue, poor DSO

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version (requires 3.9+)
python --version

# Check OpenAI API key
echo $OPENAI_API_KEY

# View logs
docker-compose logs backend
```

### Frontend shows connection error
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check CORS settings in backend/app/main.py
```

### Workflow stuck at approval step
This is expected behavior! The workflow BLOCKS at Step 3 until human approval is submitted. In the demo, we auto-approve, but in production this would wait for real human input.

---

## 🎓 Learning Resources

- **LangChain Docs:** https://python.langchain.com/
- **LangGraph:** https://langchain-ai.github.io/langgraph/
- **FastAPI:** https://fastapi.tiangolo.com/
- **Next.js:** https://nextjs.org/docs
- **SAP OData:** https://www.odata.org/

---

## 📄 License

This is a demo system for educational and presentation purposes.

---

## 🤝 Contributing

This is a demo project. For production use, consider:
- Real database (PostgreSQL, MongoDB)
- Async task queue (Celery, Redis)
- Production WSGI server (Gunicorn)
- Monitoring (Prometheus, Grafana)
- CI/CD pipeline

---

## 📧 Support

For questions or issues:
1. Check troubleshooting section
2. Review API documentation at `/docs`
3. Check Docker logs
4. Open an issue on GitHub

---

## 🎉 Acknowledgments

Built with:
- OpenAI GPT-4 for AI analysis
- LangChain & LangGraph for workflow orchestration
- FastAPI for high-performance backend
- Next.js for modern frontend

---

**Ready to demo?** Start Docker, click a scenario, and present! 🚀
