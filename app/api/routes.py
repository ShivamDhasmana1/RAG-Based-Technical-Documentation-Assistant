from fastapi import APIRouter

from app.graph.state import GraphState
from app.graph.workflow import graph
from app.schemas import QueryRequest, QueryResponse

router = APIRouter(prefix="/api", tags=["RAG"])


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    initial_state: GraphState = {
        "query": request.query,
        "current_query": request.query,
        "retrieved_documents": [],
        "relevant_documents": [],
        "answer": "",
        "retry_count": 0,
    }

    result = graph.invoke(initial_state)

    return QueryResponse(
        query=request.query,
        answer=result["answer"],
    )