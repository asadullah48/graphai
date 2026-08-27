import pytest
from graphai.agents.retry_agent import RetryAgent
from graphai.core.models import WorkflowNode, NodeStatus

def test_retry_agent_transient_recovery():
    agent = RetryAgent()
    node = WorkflowNode(node_id="N4", name="Settlement", task_type="SETTLEMENT")
    payload = {"simulate_transient_error": True}
    res, attempts = agent.execute_with_retry(node, payload)
    assert res.status == NodeStatus.COMPLETED
    assert attempts == 2
    assert "executed successfully" in res.output
