from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import time

class NodeStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"

class WorkflowStatus(str, Enum):
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    PAUSED_FOR_APPROVAL = "PAUSED_FOR_APPROVAL"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class RetryPolicy(BaseModel):
    max_attempts: int = 3
    base_backoff_seconds: float = 0.5
    max_backoff_seconds: float = 5.0
    jitter: bool = True

class WorkflowNode(BaseModel):
    node_id: str
    name: str
    task_type: str # INTAKE | PARALLEL_EVAL | DECISION_BRANCH | APPROVAL_GATE | SETTLEMENT
    dependencies: List[str] = Field(default_factory=list)
    requires_approval: bool = False
    retry_policy: RetryPolicy = Field(default_factory=RetryPolicy)
    status: NodeStatus = NodeStatus.PENDING
    result: Optional[Any] = None
    error_message: Optional[str] = None
    execution_duration_ms: float = 0.0

class WorkflowEdge(BaseModel):
    source_node: str
    target_node: str
    condition_key: Optional[str] = None
    condition_value: Optional[Any] = None

class WorkflowGraph(BaseModel):
    graph_id: str
    name: str
    nodes: Dict[str, WorkflowNode]
    edges: List[WorkflowEdge] = Field(default_factory=list)

class WorkflowExecutionRequest(BaseModel):
    run_id: str = "RUN-7718"
    graph_id: str = "LOAN_ORIGINATION_DAG"
    payload: Dict[str, Any] = Field(default_factory=lambda: {
        "applicant_name": "Apex Holdings Ltd",
        "loan_amount": 250000.0,
        "risk_score": 0.42,
        "simulate_transient_error": True
    })

class ApprovalActionRequest(BaseModel):
    run_id: str
    node_id: str
    action: str # APPROVE | REJECT
    approver_id: str = "COMPLIANCE_OFFICER_01"
    signature_token: str = "sig_hmac_valid_9981"
    notes: Optional[str] = "Approved after secondary review of collateral."

class NodeExecutionResult(BaseModel):
    node_id: str
    status: NodeStatus
    attempts_taken: int
    output: Any
    duration_ms: float

class WorkflowRunResult(BaseModel):
    run_id: str
    graph_id: str
    status: WorkflowStatus
    completed_nodes: List[str]
    pending_nodes: List[str]
    waiting_approval_node: Optional[str] = None
    node_results: Dict[str, NodeExecutionResult]
    total_duration_ms: float
    audit_trail: List[str]
