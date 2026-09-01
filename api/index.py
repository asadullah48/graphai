"""
Vercel serverless entrypoint.

Vercel's Python runtime looks for a top-level `app` variable in files under
`api/`; this just re-exports the real FastAPI app defined in graphai/server.py
so the whole project runs unmodified in both `uvicorn` (local/Docker) and
Vercel (serverless) contexts.

Note: Ollama has no public free-tier hosted endpoint, so on Vercel the
credit-analysis node automatically falls back to its simulated narrative
(see graphai/core/llm_client.py) - the AI code path is real and tested, it
just prefers a locally running Ollama daemon over a network dependency.
"""
from graphai.server import app  # noqa: F401
