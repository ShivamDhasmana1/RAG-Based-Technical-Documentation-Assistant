import json
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, UploadFile

from app.config import RAW_DATA_DIR
from app.graph.state import GraphState
from app.graph.workflow import graph
from app.ingestion.ingest import ingest_documents
from app.schemas import (
    DocumentInfo,
    DocumentsResponse,
    FeedbackRequest,
    FeedbackResponse,
    IngestResponse,
    QueryRequest,
    QueryResponse,
)

router = APIRouter(prefix="/api", tags=["RAG"])

FEEDBACK_LOG_PATH = RAW_DATA_DIR.parent / "feedback.jsonl"


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    initial_state: GraphState = {
        "query": request.query,
        "current_query": request.query,
        "query_type": "",
        "retrieved_documents": [],
        "relevant_documents": [],
        "sources": [],
        "answer": "",
        "retry_count": 0,
    }

    result = graph.invoke(initial_state)

    return QueryResponse(
        query=request.query,
        answer=result["answer"],
        sources=result["sources"],
    )


@router.post("/ingest", response_model=IngestResponse)
def ingest(files: list[UploadFile] | None = None) -> IngestResponse:
    if files:
        for upload in files:
            destination = RAW_DATA_DIR / upload.filename
            destination.write_bytes(upload.file.read())

    try:
        _, chunk_count = ingest_documents()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return IngestResponse(
        message="Documents ingested successfully.",
        chunks_indexed=chunk_count,
    )


@router.get("/documents", response_model=DocumentsResponse)
def list_documents() -> DocumentsResponse:
    documents = [
        DocumentInfo(filename=path.name, size_bytes=path.stat().st_size)
        for path in sorted(RAW_DATA_DIR.iterdir())
        if path.is_file() and path.suffix in {".pdf", ".md"}
    ]
    return DocumentsResponse(documents=documents)


@router.post("/feedback", response_model=FeedbackResponse)
def submit_feedback(request: FeedbackRequest) -> FeedbackResponse:
    entry = {
        "query": request.query,
        "answer": request.answer,
        "rating": request.rating,
        "comment": request.comment,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    with FEEDBACK_LOG_PATH.open("a") as f:
        f.write(json.dumps(entry) + "\n")

    return FeedbackResponse(message="Feedback recorded.")
