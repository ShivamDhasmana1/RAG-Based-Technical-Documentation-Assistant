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
        mock_invoke.return_value = {
            "answer": "Mock answer",
            "sources": ["fastapi_basics.md"],
        }

        response = client.post(
            "/api/query",
            json={"query": "What is LangGraph?"},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["query"] == "What is LangGraph?"
    assert body["answer"] == "Mock answer"
    assert body["sources"] == ["fastapi_basics.md"]


def test_documents_endpoint() -> None:
    response = client.get("/api/documents")

    assert response.status_code == 200
    filenames = {doc["filename"] for doc in response.json()["documents"]}
    assert "fastapi_basics.md" in filenames


def test_ingest_endpoint() -> None:
    with patch("app.api.routes.ingest_documents") as mock_ingest:
        mock_ingest.return_value = (None, 42)

        response = client.post("/api/ingest")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Documents ingested successfully.",
        "chunks_indexed": 42,
    }


def test_feedback_endpoint() -> None:
    response = client.post(
        "/api/feedback",
        json={
            "query": "What is LangGraph?",
            "answer": "Mock answer",
            "rating": "up",
            "comment": "Helpful",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Feedback recorded."}
