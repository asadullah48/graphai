import pytest
from graphai.agents.workflow_agent import WorkflowAgent
from graphai.core.models import WorkflowNode, NodeStatus

def test_workflow_agent_execution():
    agent = WorkflowAgent()
    node = WorkflowNode(node_id="N1", name="Intake", task_type="INTAKE")
    res = agent.execute_node_task(node, {"applicant_name": "Test Co", "loan_amount": 50000})
    assert res.status == NodeStatus.COMPLETED
    assert "Test Co" in res.output
