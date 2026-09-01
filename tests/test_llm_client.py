import httpx
import pytest

from graphai.core.llm_client import OllamaClient


class _FakeResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError("error", request=None, response=self)

    def json(self):
        return self._json_data


def test_generate_returns_text_on_success(monkeypatch):
    monkeypatch.setattr(
        httpx, "post", lambda *a, **k: _FakeResponse({"response": "  Looks good.  "})
    )
    assert OllamaClient.generate("prompt") == "Looks good."


def test_generate_returns_none_when_ollama_unreachable(monkeypatch):
    def _raise(*args, **kwargs):
        raise httpx.ConnectError("connection refused")

    monkeypatch.setattr(httpx, "post", _raise)
    assert OllamaClient.generate("prompt") is None


def test_generate_returns_none_on_empty_response(monkeypatch):
    monkeypatch.setattr(httpx, "post", lambda *a, **k: _FakeResponse({"response": "   "}))
    assert OllamaClient.generate("prompt") is None


def test_is_configured_false_when_unreachable(monkeypatch):
    def _raise(*args, **kwargs):
        raise httpx.ConnectError("connection refused")

    monkeypatch.setattr(httpx, "get", _raise)
    assert OllamaClient.is_configured() is False
