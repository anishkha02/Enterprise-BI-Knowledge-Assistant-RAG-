from fastapi.testclient import TestClient
import src.api as api


class FakeAssistant:
    def ask(self, question):
        return {"answer": "demo answer", "sources": ["customer_churn_rate.md"], "latency_s": 0.1}


def test_health():
    client = TestClient(api.app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_ask_returns_answer_and_sources(monkeypatch):
    monkeypatch.setattr(api, "get_assistant", lambda: FakeAssistant())
    client = TestClient(api.app)
    r = client.post("/ask", json={"question": "What is churn?"})
    assert r.status_code == 200
    body = r.json()
    assert "answer" in body and "sources" in body


def test_empty_question_rejected(monkeypatch):
    monkeypatch.setattr(api, "get_assistant", lambda: FakeAssistant())
    client = TestClient(api.app)
    assert client.post("/ask", json={"question": "  "}).status_code == 400