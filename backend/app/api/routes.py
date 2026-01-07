"""
API Routes for Credit Workflow System
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, List
from datetime import datetime
from ..models.schemas import (
    CreditRequest, CustomerSnapshot, ApproverDecision,
    WorkflowEvent, WorkflowSummary, RequestType, Requestor
)
from ..workflow.agent import workflow_agent
from ..tools.credit_tools import credit_tools

router = APIRouter(prefix="/api", tags=["credit-workflow"])


# Store active workflows
active_workflows: Dict[str, Any] = {}


@router.get("/")
async def root():
    """Health check"""
    return {
        "service": "CreditWorkflowAgent",
        "status": "running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@router.post("/requests", response_model=CreditRequest)
async def create_credit_request(request: CreditRequest):
    """Create a new credit request"""
    created_request = credit_tools.create_credit_request(request)
    return created_request


@router.get("/requests/{request_id}", response_model=CreditRequest)
async def get_credit_request(request_id: str):
    """Get credit request details"""
    try:
        return credit_tools.get_credit_request(request_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/customers/{customer_id}", response_model=CustomerSnapshot)
async def get_customer_snapshot(customer_id: str):
    """Get customer financial snapshot"""
    try:
        return credit_tools.get_customer_snapshot(customer_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/workflow/start/{request_id}")
async def start_workflow(request_id: str, background_tasks: BackgroundTasks):
    """
    Start credit workflow for a request
    Workflow runs in background and can be monitored via events endpoint
    """
    try:
        # Validate request exists
        credit_tools.get_credit_request(request_id)

        # Check if already running
        if request_id in active_workflows and active_workflows[request_id]["status"] == "running":
            raise HTTPException(status_code=400, detail="Workflow already running for this request")

        # Mark as running
        active_workflows[request_id] = {
            "status": "running",
            "started_at": datetime.now().isoformat()
        }

        # Run workflow in background (in production, use Celery or similar)
        # For demo, run synchronously but return immediately with status
        def run_workflow():
            try:
                result = workflow_agent.execute_workflow(request_id)
                active_workflows[request_id] = {
                    "status": "completed",
                    "started_at": active_workflows[request_id]["started_at"],
                    "completed_at": datetime.now().isoformat(),
                    "result": result.model_dump()
                }
            except Exception as e:
                active_workflows[request_id] = {
                    "status": "failed",
                    "started_at": active_workflows[request_id]["started_at"],
                    "error": str(e)
                }

        background_tasks.add_task(run_workflow)

        return {
            "message": "Workflow started",
            "request_id": request_id,
            "status": "running",
            "monitor_url": f"/api/workflow/status/{request_id}"
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/workflow/status/{request_id}")
async def get_workflow_status(request_id: str):
    """Get current workflow status"""
    if request_id not in active_workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return active_workflows[request_id]


@router.get("/workflow/events/{request_id}", response_model=List[WorkflowEvent])
async def get_workflow_events(request_id: str):
    """Get all workflow events for a request (for timeline UI)"""
    events = credit_tools.get_workflow_events(request_id)
    if not events:
        raise HTTPException(status_code=404, detail="No events found for this request")
    return events


@router.post("/workflow/approve/{request_id}")
async def submit_approval(request_id: str, decision: ApproverDecision):
    """
    Submit human approval decision
    This unblocks STEP 3 of the workflow
    """
    try:
        # Validate request exists
        credit_tools.get_credit_request(request_id)

        # Store decision
        credit_tools.set_approver_decision(request_id, decision)

        return {
            "message": "Approval decision recorded",
            "request_id": request_id,
            "decision": decision.decision.value
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/workflow/summary/{request_id}", response_model=WorkflowSummary)
async def get_workflow_summary(request_id: str):
    """Get complete workflow summary (for demo presentation)"""
    if request_id not in active_workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")

    workflow_data = active_workflows[request_id]

    if workflow_data["status"] != "completed":
        raise HTTPException(status_code=400, detail=f"Workflow not completed yet. Status: {workflow_data['status']}")

    return WorkflowSummary(**workflow_data["result"])


@router.post("/demo/quick-run/{scenario}")
async def demo_quick_run(scenario: str):
    """
    Quick demo runner - creates request and runs workflow in one call
    Scenarios: 'unblock-good', 'unblock-risky', 'limit-increase'
    """
    # Create demo request based on scenario
    if scenario == "unblock-good":
        request = CreditRequest(
            request_id=f"REQ-DEMO-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            customer_id="CUST001",
            request_type=RequestType.UNBLOCK,
            requested_limit=None,
            reason="Customer cleared 80% overdue. Major payment received from government contract.",
            requestor=Requestor(name="Demo User", email="demo@company.com")
        )

    elif scenario == "unblock-risky":
        request = CreditRequest(
            request_id=f"REQ-DEMO-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            customer_id="CUST003",
            request_type=RequestType.UNBLOCK,
            requested_limit=None,
            reason="Customer requesting unblock for urgent order.",
            requestor=Requestor(name="Demo User", email="demo@company.com")
        )

    elif scenario == "limit-increase":
        request = CreditRequest(
            request_id=f"REQ-DEMO-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            customer_id="CUST002",
            request_type=RequestType.LIMIT_INCREASE,
            requested_limit=150000000.0,
            reason="Expanding business relationship. Customer has excellent payment history.",
            requestor=Requestor(name="Demo User", email="demo@company.com")
        )

    else:
        raise HTTPException(status_code=400, detail="Invalid scenario. Use: unblock-good, unblock-risky, limit-increase")

    # Create request
    credit_tools.create_credit_request(request)

    # Set auto-approval (for demo)
    auto_decision = ApproverDecision(
        decision="APPROVE",
        approved_limit=request.requested_limit,
        comments="Demo auto-approval"
    )
    credit_tools.set_approver_decision(request.request_id, auto_decision)

    # Run workflow synchronously for demo
    try:
        result = workflow_agent.execute_workflow(request.request_id)

        active_workflows[request.request_id] = {
            "status": "completed",
            "started_at": datetime.now().isoformat(),
            "completed_at": datetime.now().isoformat(),
            "result": result.model_dump()
        }

        return {
            "message": "Demo workflow completed",
            "request_id": request.request_id,
            "scenario": scenario,
            "summary": result.model_dump()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow failed: {str(e)}")


@router.get("/demo/customers")
async def list_demo_customers():
    """List all demo customers"""
    return {
        "customers": [
            {
                "customer_id": "CUST001",
                "name": "Tata Steel Limited",
                "segment": "Large Enterprise",
                "risk_category": "B",
                "current_limit": 50000000.0,
                "credit_block": True
            },
            {
                "customer_id": "CUST002",
                "name": "Reliance Industries Ltd",
                "segment": "Large Enterprise",
                "risk_category": "A",
                "current_limit": 100000000.0,
                "credit_block": False
            },
            {
                "customer_id": "CUST003",
                "name": "Mahindra & Mahindra",
                "segment": "Mid Enterprise",
                "risk_category": "C",
                "current_limit": 25000000.0,
                "credit_block": True
            }
        ]
    }
