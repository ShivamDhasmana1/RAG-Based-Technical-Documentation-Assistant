from typing import Any, TypedDict


class GraphState(TypedDict):
    
    query: str
    # Original user query.

    current_query: str
    # Current query being processed.

    retrieved_documents: list[Any]
    # Documents returned by the retriever.

    relevant_documents: list[Any]
    # Documents selected after relevance grading.

    answer: str
    # Final generated answer.

    retry_count: int
    # Number of query rewrite attempts.