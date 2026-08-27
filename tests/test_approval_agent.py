import pytest
from graphai.agents.approval_agent import ApprovalAgent
from graphai.core.models import WorkflowNode, NodeStatus, ApprovalActionRequest

def test_approval_requirement_detection():
    agent = ApprovalAgent()
    node = WorkflowNode(node_id="N3", name="Gate", task_type="APPROVAL_GATE", requires_approval=True)
    needed = agent.check_approval_requirement(node, {"loan_amount": 250000.0, "risk_score": 0.5})
    assert needed is True
    assert node.status == NodeStatus.WAITING_APPROVAL

def test_approval_processing():
    agent = ApprovalAgent()
    node = WorkflowNode(node_id="N3", name="Gate", task_type="APPROVAL_GATE", status=NodeStatus.WAITING_APPROVAL)
    req = ApprovalActionRequest(
        run_id="RUN-1",
        node_id="N3",
        action="APPROVE",
        approver_id="OFFICER_99",
        signature_token="sig_hmac_valid",
        notes="Risk within tolerance"
    )
    ok, msg = agent.process_approval(req, node)
    assert ok is True
    assert node.status == NodeStatus.APPROVED
