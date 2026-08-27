# 📊 GraphAI: Enterprise DAG Workflow Orchestration Layer

> **A graph-first agent orchestration framework supporting Directed Acyclic Graphs (DAGs), conditional branching, Human-in-the-Loop (HITL) approvals, parallel execution, and exponential retries.**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)
[![Tests Passing](https://img.shields.io/badge/Tests-155%2B%20Passing-brightgreen.svg)]()
[![FastAPI](https://img.shields.io/badge/API-FastAPI%20%3A8010-teal.svg)](http://127.0.0.1:8010/docs)
[![Author](https://img.shields.io/badge/Author-Asadullah%20Shafique-purple.svg)](https://asadullahshafique-devunity.vercel.app)

---

## 🚀 Key Value Propositions

1. **DAG-Based Agent Orchestration**: Executes complex multi-agent workflows with strict topological dependencies, parallel fan-out/fan-in, and conditional branching.
2. **Autonomous Multi-Agent Governance**:
   - **`WorkflowAgent`**: Manages DAG task flows, dependency trees, and parallel task dispatch.
   - **`ApprovalAgent`**: Halts workflows at compliance checkpoints, requires dual-custody authorization, and verifies HMAC signatures.
   - **`RetryAgent`**: Manages transient error self-healing via exponential backoff with jitter and idempotency keys.
3. **Deterministic Human-in-the-Loop (HITL)**: Seamlessly pauses workflows on high-risk thresholds ($>\$100	ext{k}$ or risk score $>0.40$) and resumes on authenticated approval.
4. **Resilient Exponential Retries**: Mitigates 504 Gateway Timeouts and downstream API flakiness with automated backoff retry curves.
5. **Interactive DAG Workflow Studio**: Glassmorphic bilingual (English/Arabic RTL) dashboard with real-time node state visualizers, parallel execution tracks, and interactive approval modals.

---

## 🏛️ GraphAI Architecture

```
                    ┌─────────────────────────┐
                    │     Workflow Trigger    │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │    GraphAI DAG Engine   │
                    └────────────┬────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│  WorkflowAgent   │   │  ApprovalAgent   │   │    RetryAgent    │
│ • DAG Topology   │   │ • HITL Gates     │   │ • Exp Backoff    │
│ • Parallel Tasks │   │ • Risk Policies  │   │ • Jitter Curves  │
│ • Fan-out/Fan-in │   │ • HMAC Signatures│   │ • Dead-Letter Q  │
└──────────────────┘   └──────────────────┘   └──────────────────┘
```

---

## 🛠️ Quick Start

```powershell
# 1. Clone repository
git clone https://github.com/asadullah48/graphai.git
cd graphai

# 2. Install dependencies
pip install -e .

# 3. Run automated test suite
python -m pytest tests -v

# 4. Start local gateway & frontend DAG studio
uvicorn graphai.server:app --host 127.0.0.1 --port 8010 --reload
```

- **Interactive DAG Studio**: [http://127.0.0.1:8010/](http://127.0.0.1:8010/)
- **Swagger OpenAPI Docs**: [http://127.0.0.1:8010/docs](http://127.0.0.1:8010/docs)

---

## 🌐 Connected Ecosystem & Portfolio

- **DevUnity Portfolio**: [https://asadullahshafique-devunity.vercel.app](https://asadullahshafique-devunity.vercel.app)
- **LoopAI**: [https://github.com/asadullah48/loopai](https://github.com/asadullah48/loopai)
- **HarnessAI**: [https://github.com/asadullah48/harnessai](https://github.com/asadullah48/harnessai)
- **SecureBridge**: [https://github.com/asadullah48/securebridge](https://github.com/asadullah48/securebridge)
- **WorkforceAI Academy**: [https://github.com/asadullah48/workforceai-academy](https://github.com/asadullah48/workforceai-academy)
- **ConciergeAgent**: [https://github.com/asadullah48/conciergeagent](https://github.com/asadullah48/conciergeagent)
- **ContextX**: [https://github.com/asadullah48/contextx](https://github.com/asadullah48/contextx)
- **GuardrailAI**: [https://github.com/asadullah48/guardrailai](https://github.com/asadullah48/guardrailai)
- **MarketAgentHub**: [https://github.com/asadullah48/marketagenthub](https://github.com/asadullah48/marketagenthub)
- **WorkforceAI**: [https://github.com/asadullah48/workforceai](https://github.com/asadullah48/workforceai)
- **DomainX**: [https://github.com/asadullah48/domainx](https://github.com/asadullah48/domainx)
