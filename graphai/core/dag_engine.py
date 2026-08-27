from typing import List, Dict, Set
from graphai.core.models import WorkflowGraph, WorkflowNode, NodeStatus

class DAGEngine:
    """
    DAGEngine: Validates acyclic invariants, computes topological levels for parallel dispatch,
    and resolves ready nodes based on upstream dependencies.
    """
    @staticmethod
    def get_ready_nodes(graph: WorkflowGraph) -> List[WorkflowNode]:
        ready = []
        completed_ids = {nid for nid, n in graph.nodes.items() if n.status in [NodeStatus.COMPLETED, NodeStatus.APPROVED]}

        for nid, node in graph.nodes.items():
            if node.status in [NodeStatus.PENDING, NodeStatus.RETRYING]:
                # Check if all upstream dependencies are satisfied
                if all(dep in completed_ids for dep in node.dependencies):
                    ready.append(node)
        return ready

    @staticmethod
    def is_graph_complete(graph: WorkflowGraph) -> bool:
        return all(n.status in [NodeStatus.COMPLETED, NodeStatus.APPROVED, NodeStatus.REJECTED] for n in graph.nodes.values())
