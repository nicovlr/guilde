"""Deterministic generator of a fictional SMB for demos and RAG."""

from __future__ import annotations

import hashlib
import random

from guilde_data.models import Company, Exchange, FictionalCompany, Invoice, Person

DISTRICTS = ("Comptabilité", "Commercial", "Opérations")
FIRST = ("Camille", "Alex", "Samira", "Julien", "Inès", "Marc")
LAST = ("Bernard", "Morel", "Diallo", "Petit", "Nguyen", "Rossi")
CLIENT_NAMES = (
    "Atelier Nord SAS",
    "Boulangerie des Quais",
    "TechParc Limité",
    "Maison Verte",
)
SUPPLIER_NAMES = (
    "Fournitures Express",
    "CloudLocal SARL",
    "Print & Co",
)


def _rng(seed: int) -> random.Random:
    digest = hashlib.sha256(f"guilde-fictional-{seed}".encode()).hexdigest()
    return random.Random(int(digest[:16], 16))


def generate_company(seed: int = 42) -> FictionalCompany:
    rng = _rng(seed)
    npcs = [
        Person(
            id=f"npc-{i}",
            name=f"{rng.choice(FIRST)} {rng.choice(LAST)}",
            role=role,
            district=district,
        )
        for i, (role, district) in enumerate(
            (
                ("Responsable comptable", DISTRICTS[0]),
                ("Chargé commercial", DISTRICTS[1]),
                ("Chef d'opérations", DISTRICTS[2]),
            ),
            start=1,
        )
    ]

    parties: list[Company] = []
    for i, name in enumerate(CLIENT_NAMES, start=1):
        parties.append(
            Company(
                id=f"client-{i}",
                name=name,
                kind="client",
                contact=f"{rng.choice(FIRST)}@{name.split()[0].lower()}.example",
                notes=rng.choice(
                    (
                        "Contrat annuel, paiement 30 jours.",
                        "Prospect converti Q1, volume en hausse.",
                        "Litige mineur sur facture F-2025-03 résolu.",
                    )
                ),
            )
        )
    for i, name in enumerate(SUPPLIER_NAMES, start=1):
        parties.append(
            Company(
                id=f"supplier-{i}",
                name=name,
                kind="supplier",
                contact=f"contact@{name.split()[0].lower()}.example",
                notes=rng.choice(
                    (
                        "Délai livraison 5 jours ouvrés.",
                        "Remise volume à partir de 10k€.",
                        "SLA support 24h.",
                    )
                ),
            )
        )

    invoices: list[Invoice] = []
    for i in range(1, 9):
        party = parties[i % len(parties)]
        direction = "in" if party.kind == "client" else "out"
        invoices.append(
            Invoice(
                id=f"inv-{seed}-{i:03d}",
                party_id=party.id,
                direction=direction,
                amount_eur=round(rng.uniform(450, 12500), 2),
                status=rng.choice(("paid", "open", "overdue")),
                issued_on=f"2025-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}",
                topic=rng.choice(
                    (
                        "Prestation conseil",
                        "Abonnement logiciel",
                        "Fournitures bureau",
                        "Maintenance",
                    )
                ),
            )
        )

    exchanges: list[Exchange] = []
    for i in range(1, 13):
        npc = npcs[i % len(npcs)]
        party = parties[i % len(parties)]
        exchanges.append(
            Exchange(
                id=f"ex-{seed}-{i:03d}",
                npc_id=npc.id,
                counterpart_id=party.id,
                channel=rng.choice(("email", "appel", "réunion")),
                summary=rng.choice(
                    (
                        f"Relance paiement {party.name}.",
                        f"Négociation tarif avec {party.name}.",
                        f"Point livraison / SLA — {party.name}.",
                        f"Brief commercial trimestriel — {party.name}.",
                    )
                ),
                occurred_on=f"2025-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}",
            )
        )

    treasury = round(85000 + rng.uniform(-12000, 40000), 2)
    return FictionalCompany(
        seed=seed,
        company_name="Société Démo Guilde SARL",
        treasury_eur=treasury,
        npcs=npcs,
        parties=parties,
        invoices=invoices,
        exchanges=exchanges,
    )
