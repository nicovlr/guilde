from guilde_ai.rag.store import InMemoryRag


def test_rag_retrieve_finds_treasury():
    rag = InMemoryRag.from_seed(42)
    chunks = rag.retrieve("trésorerie entreprise", k=3)
    assert chunks
    assert any("Trésorerie" in c.text or "trésorerie" in c.text.lower() for c in chunks)


def test_rag_npc_bias():
    rag = InMemoryRag.from_seed(42)
    chunks = rag.retrieve("rôle quartier", npc_id="npc-2", k=5)
    assert any("npc-2" in c.text or c.source == "npc-2" for c in chunks)
