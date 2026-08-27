from fastapi.testclient import TestClient
from graphai.server import app

client = TestClient(app)

def test_server_dashboard_root():
    res = client.get("/")
    assert res.status_code == 200
    assert "GraphAI" in res.text

def test_server_healthz():
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_server_readyz():
    res = client.get("/readyz")
    assert res.status_code == 200
    assert res.json()["graph_agents_active"] == 3

def test_server_execute_and_approve():
    payload = {
        "run_id": "RUN-API-01",
        "graph_id": "LOAN_ORIGINATION_DAG",
        "payload": {"applicant_name": "Acme Corp", "loan_amount": 150000.0, "risk_score": 0.35, "simulate_transient_error": False}
    }
    res1 = client.post("/api/v1/workflow/execute", json=payload)
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["status"] in ["PAUSED_FOR_APPROVAL", "COMPLETED"]

    # Approve
    app_payload = {
        "run_id": "RUN-API-01",
        "node_id": "NODE_3",
        "action": "APPROVE",
        "approver_id": "OFFICER_01",
        "signature_token": "sig_valid_99",
        "notes": "Approved"
    }
    res2 = client.post("/api/v1/workflow/RUN-API-01/approve", json=app_payload)
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["status"] == "COMPLETED"
