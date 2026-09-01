import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any

from graphai.core.models import (
    WorkflowExecutionRequest, ApprovalActionRequest, WorkflowRunResult
)
from graphai.core.llm_client import OllamaClient, OLLAMA_MODEL
from graphai.orchestration.graph_engine import GraphEngine

app = FastAPI(
    title="GraphAI Workflow Orchestration Gateway",
    version="1.0.0",
    description="Enterprise DAG Workflow Orchestration with Branching, HITL Approvals & Exponential Retries"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = GraphEngine()

# Mount Static UI Files
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_dashboard():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"service": "GraphAI", "status": "active", "docs": "/docs"}

@app.get("/healthz")
def healthz():
    return {"status": "healthy", "service": "GraphAI", "version": "1.0.0"}

@app.get("/readyz")
def readyz():
    return {
        "status": "ready",
        "graph_agents_active": 3,
        "ollama_model": OLLAMA_MODEL,
        "ollama_reachable": OllamaClient.is_configured(),
    }

@app.post("/api/v1/workflow/execute", response_model=WorkflowRunResult)
def execute_workflow(req: WorkflowExecutionRequest):
    return engine.execute_workflow(req)

@app.post("/api/v1/workflow/{run_id}/approve", response_model=WorkflowRunResult)
def handle_approval(run_id: str, req: ApprovalActionRequest):
    req.run_id = run_id
    return engine.handle_approval(req)
