import time
from typing import Dict, Any, List
from graphai.core.models import WorkflowNode, NodeStatus, NodeExecutionResult

class WorkflowAgent:
    """
    WorkflowAgent: Orchestrates task flow dispatch, coordinates parallel node execution,
    and records execution artifacts.
    """
    def __init__(self):
        self.name = "WorkflowAgent"
        self.version = "1.0.0"

    def execute_node_task(self, node: WorkflowNode, payload: Dict[str, Any]) -> NodeExecutionResult:
        t0 = time.time()
        task = node.task_type
        
        # Simulate domain node tasks
        if task == "INTAKE":
            out = f"Payload validated for {payload.get('applicant_name', 'Customer')} (Amount: ${payload.get('loan_amount', 0):,})"
            status = NodeStatus.COMPLETED
        elif task == "PARALLEL_CREDIT":
            out = "Credit Score: 785 (Tier-A Prime). Debt-to-Income: 18.4%."
            status = NodeStatus.COMPLETED
        elif task == "PARALLEL_FRAUD":
            out = f"AML Screen Passed (Sanctions: Clear, Risk Index: {payload.get('risk_score', 0.1)})."
            status = NodeStatus.COMPLETED
        elif task == "SETTLEMENT":
            out = "Disbursement confirmed. Funds transferred to verified treasury account."
            status = NodeStatus.COMPLETED
        else:
            out = f"Executed generic node step: {node.name}"
            status = NodeStatus.COMPLETED

        duration = round((time.time() - t0) * 1000.0, 2)
        node.status = status
        node.result = out

        return NodeExecutionResult(
            node_id=node.node_id,
            status=status,
            attempts_taken=1,
            output=out,
            duration_ms=duration
        )
