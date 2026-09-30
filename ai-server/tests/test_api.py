from fastapi.testclient import TestClient

from guilde_ai.config import Settings
from guilde_ai.main import create_app


def _client() -> TestClient:
    settings = Settings(llm_mode="mock", company_seed=42)
    return TestClient(create_app(settings))


def test_health_ok():
    with _client() as client:
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"
        assert r.json()["mode"] == "mock"


def test_talk_unknown_npc():
    with _client() as client:
        r = client.post("/npc/npc-999/talk", json={"message": "Bonjour"})
        assert r.status_code == 404


def test_talk_mock_deterministic():
    with _client() as client:
        r1 = client.post("/npc/npc-1/talk", json={"message": "Quelle est la trésorerie ?"})
        r2 = client.post("/npc/npc-1/talk", json={"message": "Quelle est la trésorerie ?"})
        assert r1.status_code == 200
        body = r1.json()
        assert body["mode"] == "mock"
        assert body["reply"].startswith("[mock]")
        assert body["npc_id"] == "npc-1"
        assert body["sources"]
        assert r1.json() == r2.json()
