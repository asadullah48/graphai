import os
from typing import Optional

import httpx

# Ollama is a free, locally-hosted LLM runtime (https://ollama.com) - no API key,
# no billing, no rate limits. It's the "free-tier API" this project integrates
# with for the credit-analysis narrative node.
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")
OLLAMA_TIMEOUT_SECONDS = float(os.environ.get("OLLAMA_TIMEOUT_SECONDS", "3.0"))


class OllamaClient:
    """
    Thin, best-effort wrapper around Ollama's local /api/generate endpoint.

    GraphAI's DAG engine must keep running whether or not a local LLM is
    available (e.g. on a serverless deployment with no Ollama daemon), so
    every call here is defensive: any failure - connection refused, DNS
    error, timeout, missing model - is swallowed and reported as `None`
    rather than raised. Callers are expected to fall back to deterministic
    output when that happens; see WorkflowAgent.execute_node_task.
    """

    @staticmethod
    def generate(prompt: str, timeout: float = OLLAMA_TIMEOUT_SECONDS) -> Optional[str]:
        try:
            response = httpx.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
                timeout=timeout,
            )
            response.raise_for_status()
            text = response.json().get("response", "").strip()
            return text or None
        except (httpx.HTTPError, ValueError, KeyError):
            return None

    @staticmethod
    def is_configured() -> bool:
        """Cheap reachability probe, used only to report status - never blocks execution."""
        try:
            response = httpx.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=1.0)
            return response.status_code == 200
        except httpx.HTTPError:
            return False
