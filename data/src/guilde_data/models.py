"""Fictional company dataset for GUILDE — seed-reproducible, never real employer data."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Person:
    id: str
    name: str
    role: str
    district: str


@dataclass(frozen=True)
class Company:
    id: str
    name: str
    kind: str  # client | supplier
    contact: str
    notes: str


@dataclass(frozen=True)
class Invoice:
    id: str
    party_id: str
    direction: str  # in | out
    amount_eur: float
    status: str
    issued_on: str
    topic: str


@dataclass(frozen=True)
class Exchange:
    id: str
    npc_id: str
    counterpart_id: str
    channel: str
    summary: str
    occurred_on: str


@dataclass
class FictionalCompany:
    seed: int
    company_name: str
    treasury_eur: float
    npcs: list[Person]
    parties: list[Company]
    invoices: list[Invoice]
    exchanges: list[Exchange]

    def to_dict(self) -> dict[str, Any]:
        return {
            "seed": self.seed,
            "company_name": self.company_name,
            "treasury_eur": self.treasury_eur,
            "npcs": [asdict(x) for x in self.npcs],
            "parties": [asdict(x) for x in self.parties],
            "invoices": [asdict(x) for x in self.invoices],
            "exchanges": [asdict(x) for x in self.exchanges],
        }
