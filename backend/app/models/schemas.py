from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any
from datetime import datetime
from enum import Enum


class RequestType(str, Enum):
    BLOCK = "BLOCK"
    UNBLOCK = "UNBLOCK"
    LIMIT_INCREASE = "LIMIT_INCREASE"


class RiskCategory(str, Enum):
    A = "A"  # Low risk
    B = "B"  # Medium risk
    C = "C"  # High risk
    D = "D"  # Critical risk


class DecisionType(str, Enum):
    APPROVE = "APPROVE"
    APPROVE_WITH_CHANGES = "APPROVE_WITH_CHANGES"
    REJECT = "REJECT"


class RecommendationType(str, Enum):
    RELEASE_BLOCK = "RELEASE_BLOCK"
    MAINTAIN_BLOCK = "MAINTAIN_BLOCK"
    PARTIAL_LIMIT_INCREASE = "PARTIAL_LIMIT_INCREASE"
    FULL_LIMIT_INCREASE = "FULL_LIMIT_INCREASE"
    REJECT_REQUEST = "REJECT_REQUEST"


class WorkflowStatus(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    REJECTED = "Rejected"


class Requestor(BaseModel):
    name: str
    email: str


class CreditRequest(BaseModel):
    request_id: str
    customer_id: str
    request_type: RequestType
    requested_limit: Optional[float] = None
    reason: str
    requestor: Requestor
    created_at: datetime = Field(default_factory=datetime.now)


class AgeingBuckets(BaseModel):
    bucket_0_30: float = Field(alias="0_30")
    bucket_31_60: float = Field(alias="31_60")
    bucket_61_90: float = Field(alias="61_90")
    bucket_90_plus: float = Field(alias="90_plus")

    class Config:
        populate_by_name = True


class CustomerSnapshot(BaseModel):
    customer_id: str
    name: str
    segment: str
    current_limit: float
    currency: str = "INR"
    credit_block: bool
    utilisation_pct: float
    dso: float
    ageing: AgeingBuckets
    risk_category: RiskCategory


class AIRecommendation(BaseModel):
    recommendation: RecommendationType
    recommended_limit: Optional[float] = None
    confidence: float = Field(ge=0, le=1)
    rationale: str
    key_metrics: Dict[str, Any]
    risk_signals: list[str]


class ApproverDecision(BaseModel):
    decision: DecisionType
    approved_limit: Optional[float] = None
    comments: str


class WorkflowEvent(BaseModel):
    step: str
    status: WorkflowStatus
    timestamp: datetime = Field(default_factory=datetime.now)
    actor: Literal["AI", "Human", "SAP"]
    payload: Dict[str, Any]


class SAPUpdateResponse(BaseModel):
    success: bool
    sap_reference_id: str
    action_taken: str
    timestamp: datetime = Field(default_factory=datetime.now)


class NotificationRequest(BaseModel):
    email: str
    subject: str
    body: str


class WorkflowSummary(BaseModel):
    request_id: str
    workflow_summary: str
    final_decision: str
    final_credit_limit: Optional[float]
    final_block_status: bool
    demo_talk_track: list[str]
    events: list[WorkflowEvent]
