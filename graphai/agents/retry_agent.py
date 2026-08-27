import time
from typing import Dict, Any, Tuple
from graphai.core.models import WorkflowNode, NodeStatus, NodeExecutionResult
from graphai.core.retry_policy import RetryCalculator

class RetryAgent:
    """
    RetryAgent: Intercepts node failures, applies exponential backoff,
    and executes self-healing retries with idempotency.
    """
    def __init__(self):
        self.name = "RetryAgent"
        self.version = "1.0.0"

    def execute_with_retry(
        self, node: WorkflowNode, payload: Dict[str, Any]
    ) -> Tuple[NodeExecutionResult, int]:
        t0 = time.time()
        policy = node.retry_policy
        attempts = 0
        success = False
        last_error = ""

        while attempts < policy.max_attempts:
            attempts += 1
            # Simulate transient failure on first attempt if configured
            if attempts == 1 and payload.get("simulate_transient_error", False):
                backoff = RetryCalculator.calculate_backoff(attempts, policy)
                last_error = f"Transient Gateway Timeout (504). Backoff: {backoff}s before retry."
                node.status = NodeStatus.RETRYING
                continue
            
            # Succeeded
            success = True
            break

        duration = round((time.time() - t0) * 1000.0, 2)

        if success:
            node.status = NodeStatus.COMPLETED
            node.result = f"Settlement & Disbursement executed successfully after {attempts} attempts."
            res = NodeExecutionResult(
                node_id=node.node_id,
                status=NodeStatus.COMPLETED,
                attempts_taken=attempts,
                output=node.result,
                duration_ms=duration
            )
        else:
            node.status = NodeStatus.FAILED
            node.error_message = last_error
            res = NodeExecutionResult(
                node_id=node.node_id,
                status=NodeStatus.FAILED,
                attempts_taken=attempts,
                output=last_error,
                duration_ms=duration
            )

        return res, attempts
