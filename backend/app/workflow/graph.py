"""
LangGraph Workflow Graph (Optional Enhancement)
For future: Visual workflow representation and state management
"""
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from ..models.schemas import WorkflowStatus


class WorkflowState(TypedDict):
    """State schema for workflow graph"""
    request_id: str
    current_step: str
    status: WorkflowStatus
    data: dict


def create_workflow_graph():
    """
    Create LangGraph state machine for credit workflow
    Future enhancement for visual workflow management
    """

    # Define workflow graph
    workflow = StateGraph(WorkflowState)

    # Add nodes for each step
    workflow.add_node("trigger", lambda state: {**state, "current_step": "trigger"})
    workflow.add_node("analysis", lambda state: {**state, "current_step": "analysis"})
    workflow.add_node("approval", lambda state: {**state, "current_step": "approval"})
    workflow.add_node("sap_update", lambda state: {**state, "current_step": "sap_update"})
    workflow.add_node("notification", lambda state: {**state, "current_step": "notification"})

    # Define edges
    workflow.set_entry_point("trigger")
    workflow.add_edge("trigger", "analysis")
    workflow.add_edge("analysis", "approval")
    workflow.add_edge("approval", "sap_update")
    workflow.add_edge("sap_update", "notification")
    workflow.add_edge("notification", END)

    return workflow.compile()


# For future use
# graph = create_workflow_graph()
