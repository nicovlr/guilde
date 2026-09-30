"""LLM backends: deterministic mock + OpenAI-compatible HTTP client."""

from __future__ import annotations

from typing import Protocol

import httpx

from guilde_ai.rag.store import RetrievedChunk


class LlmClient(Protocol):
    async def complete(self, *, system: str, user: str) -> str: ...


class MockLlm:
    """Deterministic replies for CI / no-GPU demos."""

    async def complete(self, *, system: str, user: str) -> str:
        # Stable hash-like snippet from user message for tests
        digest = sum(ord(c) for c in user) % 997
        context_hint = ""
        if "Contexte:" in system:
            context_hint = " Je m'appuie sur les fiches de la société démo."
        return f"[mock] Bien reçu : « {user.strip()[:120]} ».{context_hint} (ref={digest})"


class OpenAICompatibleLlm:
    def __init__(self, *, base_url: str, model: str, api_key: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._api_key = api_key

    async def complete(self, *, system: str, user: str) -> str:
        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.2,
        }
        headers = {"Authorization": f"Bearer {self._api_key}"}
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{self._base_url}/chat/completions",
                json=payload,
                headers=headers,
            )
            resp.raise_for_status()
            data = resp.json()
        return data["choices"][0]["message"]["content"]


def build_system_prompt(npc_name: str, npc_role: str, chunks: list[RetrievedChunk]) -> str:
    context = "\n".join(f"- {c.text}" for c in chunks) or "- (aucun contexte)"
    return (
        f"Tu es {npc_name}, {npc_role}, PNJ du monde GUILDE. "
        "Réponds en français, de façon concise, en restant fidèle au contexte métier fictif.\n"
        f"Contexte:\n{context}"
    )
