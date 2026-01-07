"""
Credit Workflow Tools - Implements the 7 tool contracts
"""
from datetime import datetime
from typing import Optional
from ..models.schemas import (
    CreditRequest, CustomerSnapshot, ApproverDecision,
    WorkflowEvent, SAPUpdateResponse, NotificationRequest,
    RequestType, RiskCategory, AgeingBuckets, Requestor
)
from .sap_adapter import sap_adapter


class CreditWorkflowTools:
    """Implements all 7 tool contracts for the credit workflow"""

    def __init__(self):
        # Mock data stores (in production, use real database)
        self.requests_db = {}
        self.customers_db = {}
        self.approvals_db = {}
        self.events_db = {}
        self._init_demo_data()

    def _init_demo_data(self):
        """Initialize demo data"""
        # Demo customer 1: Good standing
        self.customers_db["CUST001"] = CustomerSnapshot(
            customer_id="CUST001",
            name="Tata Steel Limited",
            segment="Large Enterprise",
            current_limit=50000000.0,
            currency="INR",
            credit_block=True,
            utilisation_pct=72.5,
            dso=42.0,
            ageing=AgeingBuckets(**{
                "0_30": 25000000.0,
                "31_60": 8000000.0,
                "61_90": 3000000.0,
                "90_plus": 500000.0
            }),
            risk_category=RiskCategory.B
        )

        # Demo customer 2: High risk
        self.customers_db["CUST002"] = CustomerSnapshot(
            customer_id="CUST002",
            name="Reliance Industries Ltd",
            segment="Large Enterprise",
            current_limit=100000000.0,
            currency="INR",
            credit_block=False,
            utilisation_pct=45.0,
            dso=35.0,
            ageing=AgeingBuckets(**{
                "0_30": 40000000.0,
                "31_60": 5000000.0,
                "61_90": 0.0,
                "90_plus": 0.0
            }),
            risk_category=RiskCategory.A
        )

        # Demo customer 3: Moderate risk
        self.customers_db["CUST003"] = CustomerSnapshot(
            customer_id="CUST003",
            name="Mahindra & Mahindra",
            segment="Mid Enterprise",
            current_limit=25000000.0,
            currency="INR",
            credit_block=True,
            utilisation_pct=88.0,
            dso=65.0,
            ageing=AgeingBuckets(**{
                "0_30": 8000000.0,
                "31_60": 7000000.0,
                "61_90": 5000000.0,
                "90_plus": 2000000.0
            }),
            risk_category=RiskCategory.C
        )

        # Demo request 1
        self.requests_db["REQ001"] = CreditRequest(
            request_id="REQ001",
            customer_id="CUST001",
            request_type=RequestType.UNBLOCK,
            requested_limit=None,
            reason="Customer has cleared 80% of overdue invoices. Major payment received from government project.",
            requestor=Requestor(
                name="Rajesh Kumar",
                email="rajesh.kumar@company.com"
            ),
            created_at=datetime.now()
        )

    def get_credit_request(self, request_id: str) -> CreditRequest:
        """Tool 1: Retrieve credit request details"""
        if request_id not in self.requests_db:
            raise ValueError(f"Request {request_id} not found")
        return self.requests_db[request_id]

    def get_customer_snapshot(self, customer_id: str) -> CustomerSnapshot:
        """Tool 2: Get customer financial snapshot from SAP"""
        if customer_id not in self.customers_db:
            raise ValueError(f"Customer {customer_id} not found")
        return self.customers_db[customer_id]

    def emit_workflow_event(self, step: str, status: str, payload: dict, actor: str = "AI") -> WorkflowEvent:
        """Tool 3: Emit workflow event for frontend timeline"""
        event = WorkflowEvent(
            step=step,
            status=status,
            timestamp=datetime.now(),
            actor=actor,
            payload=payload
        )

        # Store event
        request_id = payload.get("request_id")
        if request_id:
            if request_id not in self.events_db:
                self.events_db[request_id] = []
            self.events_db[request_id].append(event)

        return event

    def get_approver_decision(self, request_id: str) -> Optional[ApproverDecision]:
        """Tool 4: Get human approver decision (BLOCKING CALL in real system)"""
        # In real system, this would wait for human input
        # For demo, return mock or stored decision
        return self.approvals_db.get(request_id)

    def set_approver_decision(self, request_id: str, decision: ApproverDecision):
        """Helper: Set approver decision (called by API endpoint)"""
        self.approvals_db[request_id] = decision

    def update_credit_limit_s4(self, customer_id: str, new_limit: float, reason: str) -> SAPUpdateResponse:
        """Tool 5: Update credit limit in SAP"""
        response = sap_adapter.update_credit_limit(customer_id, new_limit, reason)

        # Update local cache
        if customer_id in self.customers_db:
            self.customers_db[customer_id].current_limit = new_limit

        return response

    def update_credit_block_s4(self, customer_id: str, block_flag: bool, reason: str) -> SAPUpdateResponse:
        """Tool 6: Update credit block status in SAP"""
        response = sap_adapter.update_credit_block(customer_id, block_flag, reason)

        # Update local cache
        if customer_id in self.customers_db:
            self.customers_db[customer_id].credit_block = block_flag

        return response

    def send_notification(self, email: str, subject: str, body: str) -> dict:
        """Tool 7: Send email notification"""
        # In production, integrate with email service (SendGrid, SES, etc.)
        notification = NotificationRequest(
            email=email,
            subject=subject,
            body=body
        )

        # For demo, just log
        print(f"EMAIL SENT TO: {email}")
        print(f"SUBJECT: {subject}")
        print(f"BODY:\n{body}")

        return {
            "success": True,
            "notification": notification.model_dump(),
            "timestamp": datetime.now().isoformat()
        }

    def get_workflow_events(self, request_id: str) -> list[WorkflowEvent]:
        """Get all events for a request"""
        return self.events_db.get(request_id, [])

    def create_credit_request(self, request: CreditRequest) -> CreditRequest:
        """Helper: Create new credit request"""
        self.requests_db[request.request_id] = request
        return request


# Singleton instance
credit_tools = CreditWorkflowTools()
