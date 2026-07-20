from typing import Any, TypedDict


class GraphState(TypedDict):
    query: str
    # Original user query.

    current_query: str
    # Current query being processed (rewritten by analysis/retry steps).

    query_type: str
    # Query classification: conceptual, how_to, troubleshooting, or api_reference.

    retrieved_documents: list[Any]
    # Documents returned by the retriever.

    relevant_documents: list[Any]
    # Documents selected after relevance grading.

    sources: list[str]
    # Source identifiers of the documents used to generate the answer.

    answer: str
    # Final generated answer.

    retry_count: int
    # Number of query rewrite attempts.