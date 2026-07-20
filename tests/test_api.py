from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "RAG Chatbot API",
    }


def test_query_endpoint() -> None:
    with patch("app.api.routes.graph.invoke") as mock_invoke:
        mock_invoke.return_value = {"answer": "Mock answer"}

        response = client.post(
            "/api/query",
            json={"query": "What is LangGraph?"},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["query"] == "What is LangGraph?"
    assert body["answer"] == "Mock answer"