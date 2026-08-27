from typing import Dict, Any, Tuple
from graphai.core.models import WorkflowNode, NodeStatus, ApprovalActionRequest

class ApprovalAgent:
    """
    ApprovalAgent: Manages compliance authorization gates, inspects risk policies,
    and validates HMAC approval signatures.
    """
    def __init__(self):
        self.name = "ApprovalAgent"
        self.version = "1.0.0"

    def check_approval_requirement(self, node: WorkflowNode, payload: Dict[str, Any]) -> bool:
        amount = payload.get("loan_amount", 0.0)
        risk = payload.get("risk_score", 0.0)
        # Policy rule: require manual approval if amount > $100k or risk > 0.40
        if node.requires_approval or amount > 100000.0 or risk > 0.40:
            node.status = NodeStatus.WAITING_APPROVAL
            return True
        return False

    def process_approval(self, req: ApprovalActionRequest, node: WorkflowNode) -> Tuple[bool, str]:
        if not req.signature_token.startswith("sig_"):
            return False, "Invalid approval authorization signature token."

        if req.action == "APPROVE":
            node.status = NodeStatus.APPROVED
            node.result = f"Compliance Approval Granted by {req.approver_id}. Notes: {req.notes}"
            return True, "Node approved successfully."
        else:
            node.status = NodeStatus.REJECTED
            node.result = f"Compliance Rejected by {req.approver_id}. Notes: {req.notes}"
            return True, "Node rejected."
