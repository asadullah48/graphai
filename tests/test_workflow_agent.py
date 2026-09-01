import pytest
from graphai.agents.workflow_agent import WorkflowAgent
from graphai.core.models import WorkflowNode, NodeStatus

def test_workflow_agent_execution():
    agent = WorkflowAgent()
    node = WorkflowNode(node_id="N1", name="Intake", task_type="INTAKE")
    res = agent.execute_node_task(node, {"applicant_name": "Test Co", "loan_amount": 50000})
    assert res.status == NodeStatus.COMPLETED
    assert "Test Co" in res.output

def test_workflow_agent_credit_node_falls_back_when_ollama_unreachable(monkeypatch):
    # Force the Ollama call to fail regardless of the test machine's environment,
    # so this test is deterministic whether or not Ollama happens to be running.
    from graphai.agents import workflow_agent as wa_module
    monkeypatch.setattr(wa_module.OllamaClient, "generate", staticmethod(lambda prompt, timeout=None: None))

    agent = WorkflowAgent()
    node = WorkflowNode(node_id="N2A", name="Parallel Credit Analysis", task_type="PARALLEL_CREDIT")
    res = agent.execute_node_task(node, {"applicant_name": "Test Co", "loan_amount": 50000, "risk_score": 0.1})
    assert res.status == NodeStatus.COMPLETED
    assert "simulated" in res.output
