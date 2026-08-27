import pytest
from graphai.orchestration.graph_engine import GraphEngine
from graphai.core.models import WorkflowExecutionRequest, ApprovalActionRequest, WorkflowStatus

def test_graph_engine_approval_pause_and_resume():
    engine = GraphEngine()
    req = WorkflowExecutionRequest(
        run_id="RUN-TEST-01",
        payload={"loan_amount": 500000.0, "risk_score": 0.45, "simulate_transient_error": True}
    )
    res = engine.execute_workflow(req)
    assert res.status == WorkflowStatus.PAUSED_FOR_APPROVAL
    assert res.waiting_approval_node == "NODE_3"
    assert "NODE_1" in res.completed_nodes
    assert "NODE_2A" in res.completed_nodes
    assert "NODE_2B" in res.completed_nodes

    # Approve checkpoint
    app_req = ApprovalActionRequest(
        run_id="RUN-TEST-01",
        node_id="NODE_3",
        action="APPROVE",
        approver_id="VP_CREDIT",
        signature_token="sig_valid_token"
    )
    res_app = engine.handle_approval(app_req)
    assert res_app.status == WorkflowStatus.COMPLETED
