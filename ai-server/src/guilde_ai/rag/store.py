"""RAG interface + in-memory implementation over fictional company data."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from guilde_data.generator import generate_company
from guilde_data.models import FictionalCompany


@dataclass(frozen=True)
class RetrievedChunk:
    text: str
    score: float
    source: str


class RagStore(Protocol):
    def retrieve(
        self, query: str, *, npc_id: str | None = None, k: int = 5
    ) -> list[RetrievedChunk]:
        """Return top-k chunks relevant to the query."""


class InMemoryRag:
    """Simple token-overlap retriever (no GPU). Swap later for pgvector."""

    def __init__(self, company: FictionalCompany) -> None:
        self._company = company
        self._docs: list[tuple[str, str]] = []
        self._index(company)

    @classmethod
    def from_seed(cls, seed: int) -> InMemoryRag:
        return cls(generate_company(seed))

    def _index(self, company: FictionalCompany) -> None:
        docs: list[tuple[str, str]] = []
        docs.append(
            (
                "company",
                f"Entreprise {company.company_name}. Trésorerie: {company.treasury_eur:.2f} EUR.",
            )
        )
        for npc in company.npcs:
            docs.append(
                (
                    npc.id,
                    f"PNJ {npc.name} ({npc.id}), rôle {npc.role}, quartier {npc.district}.",
                )
            )
        for party in company.parties:
            docs.append(
                (
                    party.id,
                    f"{party.kind} {party.name} ({party.id}). Contact {party.contact}. {party.notes}",
                )
            )
        for inv in company.invoices:
            docs.append(
                (
                    inv.id,
                    (
                        f"Facture {inv.id} {inv.direction} {inv.amount_eur} EUR "
                        f"statut {inv.status} date {inv.issued_on} sujet {inv.topic} "
                        f"partie {inv.party_id}."
                    ),
                )
            )
        for ex in company.exchanges:
            docs.append(
                (
                    ex.id,
                    (
                        f"Échange {ex.id} PNJ {ex.npc_id} avec {ex.counterpart_id} "
                        f"via {ex.channel} le {ex.occurred_on}: {ex.summary}"
                    ),
                )
            )
        self._docs = docs

    def retrieve(
        self, query: str, *, npc_id: str | None = None, k: int = 5
    ) -> list[RetrievedChunk]:
        tokens = {t.lower() for t in query.split() if len(t) > 2}
        scored: list[RetrievedChunk] = []
        for source, text in self._docs:
            if npc_id and source.startswith("npc-") and source != npc_id:
                # Soft bias: do not hard-filter; boost later
                pass
            text_tokens = {t.lower().strip(".,;:") for t in text.split()}
            overlap = len(tokens & text_tokens)
            bonus = 1 if npc_id and npc_id in text else 0
            score = float(overlap + bonus)
            if score > 0:
                scored.append(RetrievedChunk(text=text, score=score, source=source))
        scored.sort(key=lambda c: c.score, reverse=True)
        if not scored:
            # Fallback: company + npc profile
            fallback = [d for d in self._docs if d[0] in ("company", npc_id or "")]
            return [
                RetrievedChunk(text=t, score=0.1, source=s)
                for s, t in fallback[:k] or self._docs[:k]
            ]
        return scored[:k]

    @property
    def company(self) -> FictionalCompany:
        return self._company
