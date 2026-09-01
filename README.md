# 📊 GraphAI — DAG Workflow Orchestration Engine

> **A Python/FastAPI reference implementation of graph-first agent orchestration: topological task dispatch, parallel fan-out/fan-in, conditional Human-in-the-Loop (HITL) approval gates, exponential-backoff retries, and an optional local-LLM (Ollama) node.**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-17%20Passing-brightgreen.svg)](tests)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-teal.svg)](https://fastapi.tiangolo.com/)
[![Author](https://img.shields.io/badge/Author-Asadullah%20Shafique-purple.svg)](https://asadullahshafique-devunity.vercel.app)

**🔗 Live Demo:** [graphai-pi.vercel.app](https://graphai-pi.vercel.app)
**📚 API Docs:** [graphai-pi.vercel.app/docs](https://graphai-pi.vercel.app/docs) (interactive Swagger/OpenAPI)

---

## What this is

GraphAI models a multi-step business workflow — here, commercial loan origination — as a **Directed Acyclic Graph (DAG)** and walks it with a small orchestration engine rather than a linear script. It exists to demonstrate the mechanics that make agentic/workflow systems reliable in practice, not to be an actual lending product:

- **Topological dispatch** — nodes only run once every upstream dependency has completed; independent branches (credit analysis, fraud/AML screening) run in parallel.
- **Human-in-the-Loop approval gates** — high-value or high-risk nodes pause execution and wait for an authenticated approve/reject action before resuming.
- **Exponential backoff retries with jitter** — transient failures are retried automatically using `min(max_backoff, base · 2^attempt + jitter)` instead of failing the whole run.
- **A real, optional LLM integration** — the credit-analysis node calls a local [Ollama](https://ollama.com) model to generate its narrative. Ollama is free, self-hosted, and needs no API key or billing account, which is why it's used here instead of a paid provider. If Ollama isn't running (e.g. on the hosted demo, or in CI), the node **automatically falls back** to a deterministic simulated narrative — the workflow never blocks on an external service. See `graphai/core/llm_client.py`.

Everything else in the domain layer (credit scores, AML screening, settlement) is intentionally simulated — the point of this project is the orchestration engine around it, which is exercised by the test suite in `tests/`.

---

## Architecture

```
                    ┌─────────────────────────┐
                    │     Workflow Trigger     │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │      GraphAI DAG Engine  │
                    └────────────┬────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│  WorkflowAgent    │   │  ApprovalAgent   │   │   RetryAgent     │
│ • DAG dispatch    │   │ • HITL gates     │   │ • Exp. backoff   │
│ • Parallel tasks  │   │ • Risk policy    │   │ • Jitter curves  │
│ • Ollama LLM node │   │ • Signature check│   │ • Dead-letter Q  │
└──────────────────┘   └──────────────────┘   └──────────────────┘
```

| Component | Responsibility |
| :--- | :--- |
| `graphai/core/dag_engine.py` | Resolves which nodes are ready to run from the dependency graph. |
| `graphai/core/retry_policy.py` | Computes exponential backoff intervals with jitter. |
| `graphai/core/llm_client.py` | Best-effort Ollama client — never raises, returns `None` on failure. |
| `graphai/agents/workflow_agent.py` | Executes a node's task, including the LLM-backed credit narrative. |
| `graphai/agents/approval_agent.py` | Evaluates approval policy and validates approval signatures. |
| `graphai/agents/retry_agent.py` | Wraps node execution with the retry policy. |
| `graphai/orchestration/graph_engine.py` | Ties the above together into a single workflow run. |
| `graphai/server.py` | FastAPI gateway + static dashboard. |

---

## Running it locally

```powershell
# 1. Clone and install
git clone https://github.com/asadullah48/graphai.git
cd graphai
pip install -r requirements.txt
pip install -e .

# 2. Run the test suite (17 tests, no external services required)
python -m pytest tests -v

# 3. Start the API + dashboard
uvicorn graphai.server:app --host 127.0.0.1 --port 8010 --reload
```

- **Dashboard:** http://127.0.0.1:8010/
- **Swagger docs:** http://127.0.0.1:8010/docs
- **Health/readiness:** `GET /healthz`, `GET /readyz` (the latter reports whether Ollama is reachable)

### Optional: enable the real LLM node

By default the credit-analysis node runs in simulated mode. To see it call a real model instead:

```powershell
ollama pull llama3.2
ollama serve
```

No further configuration is needed — `graphai/core/llm_client.py` talks to `http://localhost:11434` by default. Override `OLLAMA_BASE_URL` / `OLLAMA_MODEL` env vars to point at a different model or host.

### Docker

```powershell
docker compose up --build
```

---

## Deployment

The live demo above runs on [Vercel](https://vercel.com) as a Python serverless function (`api/index.py`, auto-detected as a FastAPI app; `.vercelignore` keeps the bundle lean). To redeploy your own copy:

```powershell
npm i -g vercel   # one-time
vercel --prod
```

Ollama has no hosted free-tier endpoint, so on Vercel the credit-analysis node runs in its simulated fallback mode automatically (confirmed live via `GET /readyz` → `"ollama_reachable": false`) — the same fallback path is exercised end-to-end by `tests/test_llm_client.py` and `tests/test_workflow_agent.py`. `Dockerfile` / `docker-compose.yml` / `helm/` are provided for a self-hosted deployment where a sidecar Ollama instance is reachable, giving the real LLM narrative in production too.

---

## Author & Portfolio

- **Portfolio:** [asadullahshafique-devunity.vercel.app](https://asadullahshafique-devunity.vercel.app)
- **GitHub:** [github.com/asadullah48](https://github.com/asadullah48)
