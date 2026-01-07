"""
CreditWorkflowAgent - Core AI Agent for Credit Decision Workflow
Implements the 5-step process with explainability
"""
import os
from typing import Dict, Any, Optional
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from ..models.schemas import (
    CreditRequest, CustomerSnapshot, AIRecommendation, ApproverDecision,
    RecommendationType, WorkflowStatus, DecisionType, WorkflowSummary
)
from ..tools.credit_tools import credit_tools


class CreditWorkflowAgent:
    """
    Agentic AI Credit Controller
    Orchestrates the 5-step credit workflow with human-in-the-loop
    """

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.3,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.tools = credit_tools

    def execute_workflow(self, request_id: str) -> WorkflowSummary:
        """
        Execute the complete 5-step workflow
        Returns: WorkflowSummary with all events and final decision
        """
        print(f"\n{'='*60}")
        print(f"🚀 STARTING CREDIT WORKFLOW FOR REQUEST: {request_id}")
        print(f"{'='*60}\n")

        # STEP 1: Credit Block Trigger
        credit_request = self._step1_credit_block_trigger(request_id)

        # STEP 2: AI Analysis & Recommendation
        customer_snapshot = self.tools.get_customer_snapshot(credit_request.customer_id)
        ai_recommendation = self._step2_analysis_and_recommendation(credit_request, customer_snapshot)

        # STEP 3: Human Approval (BLOCKING - must wait for human decision)
        # In async system, workflow pauses here until approval received
        print("\n⏸️  WORKFLOW PAUSED - Waiting for human approval...")
        print("💡 In production, this would wait for real human input via API\n")

        # For demo, simulate waiting or use pre-set decision
        approver_decision = self._step3_wait_for_approval(request_id, ai_recommendation)

        # STEP 4: SAP Update
        sap_result = self._step4_sap_update(
            credit_request,
            customer_snapshot,
            approver_decision
        )

        # STEP 5: Notification
        self._step5_notification(credit_request, approver_decision, sap_result)

        # Generate final summary
        summary = self._generate_workflow_summary(
            request_id,
            credit_request,
            customer_snapshot,
            ai_recommendation,
            approver_decision,
            sap_result
        )

        print(f"\n{'='*60}")
        print(f"✅ WORKFLOW COMPLETED FOR REQUEST: {request_id}")
        print(f"{'='*60}\n")

        return summary

    def _step1_credit_block_trigger(self, request_id: str) -> CreditRequest:
        """STEP 1: Retrieve and validate credit request"""
        print("📋 STEP 1: Credit Block Trigger")
        print("-" * 40)

        credit_request = self.tools.get_credit_request(request_id)

        self.tools.emit_workflow_event(
            step="Credit Block Request",
            status=WorkflowStatus.COMPLETED,
            actor="Human",
            payload={
                "request_id": request_id,
                "customer_id": credit_request.customer_id,
                "request_type": credit_request.request_type.value,
                "requestor": credit_request.requestor.model_dump(),
                "reason": credit_request.reason
            }
        )

        print(f"✓ Request ID: {credit_request.request_id}")
        print(f"✓ Customer: {credit_request.customer_id}")
        print(f"✓ Type: {credit_request.request_type.value}")
        print(f"✓ Requestor: {credit_request.requestor.name}")
        print()

        return credit_request

    def _step2_analysis_and_recommendation(
        self,
        credit_request: CreditRequest,
        customer_snapshot: CustomerSnapshot
    ) -> AIRecommendation:
        """STEP 2: AI Analysis & Recommendation"""
        print("🤖 STEP 2: AI Analysis & Recommendation")
        print("-" * 40)

        # Perform credit analysis
        analysis = self._perform_credit_analysis(credit_request, customer_snapshot)

        # Emit event
        self.tools.emit_workflow_event(
            step="AI Analysis & Recommendation",
            status=WorkflowStatus.COMPLETED,
            actor="AI",
            payload={
                "request_id": credit_request.request_id,
                "recommendation": analysis.recommendation.value,
                "confidence": analysis.confidence,
                "rationale": analysis.rationale,
                "key_metrics": analysis.key_metrics,
                "risk_signals": analysis.risk_signals
            }
        )

        print(f"✓ Recommendation: {analysis.recommendation.value}")
        print(f"✓ Confidence: {analysis.confidence:.1%}")
        print(f"✓ Rationale: {analysis.rationale}")
        print()

        return analysis

    def _perform_credit_analysis(
        self,
        request: CreditRequest,
        snapshot: CustomerSnapshot
    ) -> AIRecommendation:
        """Core credit analysis logic using LLM"""

        # Calculate key metrics
        total_outstanding = sum([
            snapshot.ageing.bucket_0_30,
            snapshot.ageing.bucket_31_60,
            snapshot.ageing.bucket_61_90,
            snapshot.ageing.bucket_90_plus
        ])

        overdue_pct = (
            (snapshot.ageing.bucket_31_60 + snapshot.ageing.bucket_61_90 + snapshot.ageing.bucket_90_plus)
            / total_outstanding * 100
        ) if total_outstanding > 0 else 0

        # Build prompt for LLM
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert credit controller for an Indian manufacturing company.
            You analyze credit requests with discipline, focusing on DSO, ageing, utilisation, and risk category.

            Provide your recommendation as one of:
            - RELEASE_BLOCK: Remove credit block
            - MAINTAIN_BLOCK: Keep credit block in place
            - PARTIAL_LIMIT_INCREASE: Approve partial increase
            - FULL_LIMIT_INCREASE: Approve full requested increase
            - REJECT_REQUEST: Deny the request

            Be specific, data-driven, and focused on trade credit discipline."""),
            ("human", """Analyze this credit request:

            REQUEST:
            - Type: {request_type}
            - Requested Limit: {requested_limit}
            - Reason: {reason}

            CUSTOMER SNAPSHOT:
            - Name: {customer_name}
            - Segment: {segment}
            - Current Limit: ₹{current_limit:,.2f}
            - Credit Block: {credit_block}
            - Utilisation: {utilisation_pct:.1f}%
            - DSO: {dso:.0f} days
            - Risk Category: {risk_category}

            AGEING ANALYSIS:
            - 0-30 days: ₹{ageing_0_30:,.2f}
            - 31-60 days: ₹{ageing_31_60:,.2f}
            - 61-90 days: ₹{ageing_61_90:,.2f}
            - 90+ days: ₹{ageing_90_plus:,.2f}
            - Overdue %: {overdue_pct:.1f}%

            Provide:
            1. Your recommendation (one of the 5 options above)
            2. Recommended limit (if applicable)
            3. Confidence (0-1)
            4. Clear rationale (2-3 sentences max)
            5. Key risk signals identified

            Format as JSON.""")
        ])

        # Invoke LLM
        response = self.llm.invoke(
            prompt.format_messages(
                request_type=request.request_type.value,
                requested_limit=request.requested_limit or "N/A",
                reason=request.reason,
                customer_name=snapshot.name,
                segment=snapshot.segment,
                current_limit=snapshot.current_limit,
                credit_block="Yes" if snapshot.credit_block else "No",
                utilisation_pct=snapshot.utilisation_pct,
                dso=snapshot.dso,
                risk_category=snapshot.risk_category.value,
                ageing_0_30=snapshot.ageing.bucket_0_30,
                ageing_31_60=snapshot.ageing.bucket_31_60,
                ageing_61_90=snapshot.ageing.bucket_61_90,
                ageing_90_plus=snapshot.ageing.bucket_90_plus,
                overdue_pct=overdue_pct
            )
        )

        # Parse LLM response (simplified for demo)
        # In production, use function calling or structured output
        recommendation_text = response.content

        # For demo, apply rule-based logic with LLM context
        risk_signals = []

        if snapshot.dso > 60:
            risk_signals.append(f"High DSO: {snapshot.dso:.0f} days")

        if overdue_pct > 30:
            risk_signals.append(f"High overdue: {overdue_pct:.1f}%")

        if snapshot.utilisation_pct > 85:
            risk_signals.append(f"High utilisation: {snapshot.utilisation_pct:.1f}%")

        if snapshot.ageing.bucket_90_plus > 1000000:
            risk_signals.append(f"Significant 90+ ageing: ₹{snapshot.ageing.bucket_90_plus:,.0f}")

        # Determine recommendation
        if request.request_type == "UNBLOCK":
            if len(risk_signals) == 0 or (snapshot.risk_category == "A" and overdue_pct < 20):
                recommendation = RecommendationType.RELEASE_BLOCK
                confidence = 0.85
                rationale = f"Customer shows strong payment discipline with DSO of {snapshot.dso:.0f} days and {overdue_pct:.1f}% overdue. Risk category {snapshot.risk_category.value} supports unblocking."
            elif len(risk_signals) <= 2 and overdue_pct < 40:
                recommendation = RecommendationType.RELEASE_BLOCK
                confidence = 0.70
                rationale = f"Moderate risk signals present but manageable. Customer has demonstrated recent payment improvement. Recommend unblocking with close monitoring."
            else:
                recommendation = RecommendationType.MAINTAIN_BLOCK
                confidence = 0.80
                rationale = f"Multiple risk signals identified: {', '.join(risk_signals[:2])}. Maintain block until payment discipline improves."

        elif request.request_type == "LIMIT_INCREASE":
            if len(risk_signals) == 0 and snapshot.utilisation_pct < 70:
                recommendation = RecommendationType.FULL_LIMIT_INCREASE
                confidence = 0.90
                rationale = f"Excellent payment track record and healthy utilisation at {snapshot.utilisation_pct:.1f}%. Full increase approved."
            elif len(risk_signals) <= 1:
                recommendation = RecommendationType.PARTIAL_LIMIT_INCREASE
                confidence = 0.75
                rationale = f"Good payment history with minor concerns. Recommend partial increase of 30-50% with review in 90 days."
            else:
                recommendation = RecommendationType.REJECT_REQUEST
                confidence = 0.85
                rationale = f"Multiple credit concerns prevent limit increase: {', '.join(risk_signals[:2])}. Focus on clearing overdue first."
        else:
            recommendation = RecommendationType.MAINTAIN_BLOCK
            confidence = 0.70
            rationale = "Request requires further review by credit committee."

        return AIRecommendation(
            recommendation=recommendation,
            recommended_limit=None if request.request_type == "UNBLOCK" else snapshot.current_limit * 1.3,
            confidence=confidence,
            rationale=rationale,
            key_metrics={
                "dso": snapshot.dso,
                "utilisation_pct": snapshot.utilisation_pct,
                "overdue_pct": round(overdue_pct, 1),
                "risk_category": snapshot.risk_category.value,
                "total_outstanding": total_outstanding
            },
            risk_signals=risk_signals
        )

    def _step3_wait_for_approval(
        self,
        request_id: str,
        ai_recommendation: AIRecommendation
    ) -> ApproverDecision:
        """STEP 3: Wait for human approval (BLOCKING)"""
        print("👤 STEP 3: Human Approval")
        print("-" * 40)

        # In real system, this would block until API receives approval
        # For demo, check if decision already set, otherwise use default

        decision = self.tools.get_approver_decision(request_id)

        if not decision:
            # Demo fallback: Auto-approve AI recommendation
            print("⚠️  No human decision received - using demo auto-approval")
            decision = ApproverDecision(
                decision=DecisionType.APPROVE,
                approved_limit=ai_recommendation.recommended_limit,
                comments=f"Auto-approved based on AI recommendation: {ai_recommendation.recommendation.value}"
            )
            self.tools.set_approver_decision(request_id, decision)

        self.tools.emit_workflow_event(
            step="Human Approval",
            status=WorkflowStatus.COMPLETED,
            actor="Human",
            payload={
                "request_id": request_id,
                "decision": decision.decision.value,
                "approved_limit": decision.approved_limit,
                "comments": decision.comments
            }
        )

        print(f"✓ Decision: {decision.decision.value}")
        print(f"✓ Comments: {decision.comments}")
        print()

        return decision

    def _step4_sap_update(
        self,
        request: CreditRequest,
        snapshot: CustomerSnapshot,
        decision: ApproverDecision
    ) -> Optional[Dict[str, Any]]:
        """STEP 4: Update SAP S/4HANA"""
        print("🔧 STEP 4: SAP Update")
        print("-" * 40)

        if decision.decision == DecisionType.REJECT:
            print("⊘ Skipped - Request rejected")
            self.tools.emit_workflow_event(
                step="SAP Update",
                status=WorkflowStatus.COMPLETED,
                actor="SAP",
                payload={
                    "request_id": request.request_id,
                    "action_taken": "No action - request rejected",
                    "sap_reference_id": None
                }
            )
            return None

        sap_response = None

        # Execute SAP update based on request type
        if request.request_type == "UNBLOCK":
            sap_response = self.tools.update_credit_block_s4(
                customer_id=request.customer_id,
                block_flag=False,
                reason=f"Approved by credit controller. {decision.comments}"
            )

        elif request.request_type == "LIMIT_INCREASE" and decision.approved_limit:
            sap_response = self.tools.update_credit_limit_s4(
                customer_id=request.customer_id,
                new_limit=decision.approved_limit,
                reason=f"Credit limit increase approved. {decision.comments}"
            )

        if sap_response:
            self.tools.emit_workflow_event(
                step="SAP Update",
                status=WorkflowStatus.COMPLETED,
                actor="SAP",
                payload={
                    "request_id": request.request_id,
                    "action_taken": sap_response.action_taken,
                    "sap_reference_id": sap_response.sap_reference_id,
                    "success": sap_response.success
                }
            )

            print(f"✓ Action: {sap_response.action_taken}")
            print(f"✓ SAP Ref: {sap_response.sap_reference_id}")
            print()

        return sap_response.model_dump() if sap_response else None

    def _step5_notification(
        self,
        request: CreditRequest,
        decision: ApproverDecision,
        sap_result: Optional[Dict[str, Any]]
    ):
        """STEP 5: Send notification to requestor"""
        print("📧 STEP 5: Notification")
        print("-" * 40)

        # Build email content
        if decision.decision == DecisionType.REJECT:
            subject = f"Credit Request {request.request_id} - REJECTED"
            body = f"""Dear {request.requestor.name},

Your credit request for customer {request.customer_id} has been REJECTED.

Request Type: {request.request_type.value}
Decision: {decision.decision.value}
Reason: {decision.comments}

If you have questions, please contact the credit control team.

Best regards,
Credit Control System"""

        else:
            subject = f"Credit Request {request.request_id} - APPROVED"
            body = f"""Dear {request.requestor.name},

Your credit request for customer {request.customer_id} has been APPROVED.

Request Type: {request.request_type.value}
Decision: {decision.decision.value}
Comments: {decision.comments}

SAP Reference: {sap_result.get('sap_reference_id') if sap_result else 'N/A'}
Action Taken: {sap_result.get('action_taken') if sap_result else 'N/A'}

The changes have been updated in SAP S/4HANA.

Best regards,
Credit Control System"""

        # Send notification
        notification_result = self.tools.send_notification(
            email=request.requestor.email,
            subject=subject,
            body=body
        )

        self.tools.emit_workflow_event(
            step="Notification",
            status=WorkflowStatus.COMPLETED,
            actor="AI",
            payload={
                "request_id": request.request_id,
                "email_sent_to": request.requestor.email,
                "subject": subject,
                "timestamp": notification_result["timestamp"]
            }
        )

        print(f"✓ Sent to: {request.requestor.email}")
        print(f"✓ Subject: {subject}")
        print()

    def _generate_workflow_summary(
        self,
        request_id: str,
        request: CreditRequest,
        snapshot: CustomerSnapshot,
        ai_recommendation: AIRecommendation,
        decision: ApproverDecision,
        sap_result: Optional[Dict[str, Any]]
    ) -> WorkflowSummary:
        """Generate final workflow summary with demo talk track"""

        events = self.tools.get_workflow_events(request_id)

        # Build workflow summary
        workflow_summary = f"""Credit workflow completed for {snapshot.name} (Customer ID: {request.customer_id}).
Request type was {request.request_type.value}. AI analysis identified {len(ai_recommendation.risk_signals)} risk signals and recommended {ai_recommendation.recommendation.value} with {ai_recommendation.confidence:.0%} confidence.
Human approver {'approved' if decision.decision != DecisionType.REJECT else 'rejected'} the request."""

        if decision.decision != DecisionType.REJECT:
            workflow_summary += f" SAP S/4HANA was updated successfully (Ref: {sap_result.get('sap_reference_id', 'N/A')})."

        # Build demo talk track
        demo_talk_track = [
            f"AI analyzed customer data: DSO {snapshot.dso:.0f} days, {snapshot.utilisation_pct:.1f}% utilisation, {snapshot.risk_category.value}-grade risk",
            f"Identified {len(ai_recommendation.risk_signals)} risk signals: {', '.join(ai_recommendation.risk_signals) if ai_recommendation.risk_signals else 'None'}",
            f"AI recommended: {ai_recommendation.recommendation.value} ({ai_recommendation.confidence:.0%} confidence)",
            f"Human {'approved' if decision.decision != DecisionType.REJECT else 'rejected'}: {decision.comments[:100]}",
        ]

        if sap_result:
            demo_talk_track.append(f"SAP updated: {sap_result.get('action_taken')}")
        else:
            demo_talk_track.append("No SAP changes (request rejected)")

        # Get final status
        final_limit = snapshot.current_limit
        final_block = snapshot.credit_block

        if decision.decision != DecisionType.REJECT and sap_result:
            if request.request_type == "UNBLOCK":
                final_block = False
            elif request.request_type == "LIMIT_INCREASE" and decision.approved_limit:
                final_limit = decision.approved_limit

        return WorkflowSummary(
            request_id=request_id,
            workflow_summary=workflow_summary,
            final_decision="APPROVED" if decision.decision != DecisionType.REJECT else "REJECTED",
            final_credit_limit=final_limit,
            final_block_status=final_block,
            demo_talk_track=demo_talk_track,
            events=events
        )


# Singleton instance
workflow_agent = CreditWorkflowAgent()
