from langgraph.graph import END, START, StateGraph

from app.config import MAX_RETRIES
from app.graph.nodes import (
    analyze_query_node,
    generate_node,
    grade_documents_node,
    retrieve_node,
    rewrite_query_node,
)
from app.graph.state import GraphState


def route_after_grading(state: GraphState) -> str:
    """Decide the next node after grading: generate, retry, or end."""
    if len(state.get("relevant_documents") or []) > 0:
        return "generate"
    if state.get("retry_count", 0) < MAX_RETRIES:
        return "rewrite_query"
    return "end"


workflow = StateGraph(GraphState)

workflow.add_node("analyze_query", analyze_query_node)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("grade", grade_documents_node)
workflow.add_node("generate", generate_node)
workflow.add_node("rewrite_query", rewrite_query_node)

workflow.add_edge(START, "analyze_query")
workflow.add_edge("analyze_query", "retrieve")
workflow.add_edge("retrieve", "grade")
workflow.add_conditional_edges(
    "grade",
    route_after_grading,
    {"generate": "generate", "rewrite_query": "rewrite_query", "end": END},
)
workflow.add_edge("rewrite_query", "retrieve")
workflow.add_edge("generate", END)

graph = workflow.compile()
