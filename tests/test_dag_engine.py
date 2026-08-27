import pytest
from graphai.core.dag_engine import DAGEngine
from graphai.core.models import WorkflowGraph, WorkflowNode, NodeStatus

def test_dag_ready_nodes_resolution():
    nodes = {
        "N1": WorkflowNode(node_id="N1", name="Step 1", task_type="INTAKE", status=NodeStatus.COMPLETED),
        "N2A": WorkflowNode(node_id="N2A", name="Step 2A", task_type="PARALLEL_CREDIT", dependencies=["N1"], status=NodeStatus.PENDING),
        "N2B": WorkflowNode(node_id="N2B", name="Step 2B", task_type="PARALLEL_FRAUD", dependencies=["N1"], status=NodeStatus.PENDING),
        "N3": WorkflowNode(node_id="N3", name="Step 3", task_type="APPROVAL_GATE", dependencies=["N2A", "N2B"], status=NodeStatus.PENDING)
    }
    graph = WorkflowGraph(graph_id="TEST_DAG", name="Test Graph", nodes=nodes)
    ready = DAGEngine.get_ready_nodes(graph)
    ready_ids = [n.node_id for n in ready]
    assert "N2A" in ready_ids
    assert "N2B" in ready_ids
    assert "N3" not in ready_ids

def test_dag_completion_check():
    nodes = {
        "N1": WorkflowNode(node_id="N1", name="Step 1", task_type="INTAKE", status=NodeStatus.COMPLETED),
        "N2": WorkflowNode(node_id="N2", name="Step 2", task_type="SETTLEMENT", status=NodeStatus.COMPLETED)
    }
    graph = WorkflowGraph(graph_id="TEST_DAG", name="Test Graph", nodes=nodes)
    assert DAGEngine.is_graph_complete(graph) is True
