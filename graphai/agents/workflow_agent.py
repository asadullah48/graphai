import time
from typing import Dict, Any, List
from graphai.core.models import WorkflowNode, NodeStatus, NodeExecutionResult
from graphai.core.llm_client import OllamaClient, OLLAMA_MODEL

# Deterministic fallback used whenever no local LLM is reachable (e.g. CI, or a
# serverless deployment with no Ollama daemon running alongside it).
_SIMULATED_CREDIT_NARRATIVE = "Credit Score: 785 (Tier-A Prime). Debt-to-Income: 18.4%."

class WorkflowAgent:
    """
    WorkflowAgent: Orchestrates task flow dispatch, coordinates parallel node execution,
    and records execution artifacts.
    """
    def __init__(self):
        self.name = "WorkflowAgent"
        self.version = "1.0.0"

    def _generate_credit_narrative(self, payload: Dict[str, Any]) -> str:
        """
        Calls a local Ollama model (free, self-hosted, no API key) to write the
        credit-analysis narrative. Falls back to a fixed simulated narrative if
        Ollama isn't running or reachable, so the workflow never blocks on it.
        """
        prompt = (
            "You are a credit analyst. In one concise sentence (under 40 words), "
            f"summarize a plausible credit decision for '{payload.get('applicant_name', 'the applicant')}' "
            f"requesting ${payload.get('loan_amount', 0):,.0f}, given a risk score of "
            f"{payload.get('risk_score', 0.1)}. Invent a realistic credit score and "
            "debt-to-income ratio; do not ask follow-up questions."
        )
        narrative = OllamaClient.generate(prompt)
        if narrative:
            return f"[AI — Ollama/{OLLAMA_MODEL}] {narrative}"
        return f"{_SIMULATED_CREDIT_NARRATIVE} (simulated — Ollama unavailable)"

    def execute_node_task(self, node: WorkflowNode, payload: Dict[str, Any]) -> NodeExecutionResult:
        t0 = time.time()
        task = node.task_type

        # Simulate domain node tasks
        if task == "INTAKE":
            out = f"Payload validated for {payload.get('applicant_name', 'Customer')} (Amount: ${payload.get('loan_amount', 0):,})"
            status = NodeStatus.COMPLETED
        elif task == "PARALLEL_CREDIT":
            out = self._generate_credit_narrative(payload)
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
