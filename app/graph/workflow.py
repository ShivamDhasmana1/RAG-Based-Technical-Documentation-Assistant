from langgraph.graph import END, START, StateGraph

from app.graph.nodes import generate_node, grade_documents_node, retrieve_node
from app.graph.state import GraphState

workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve_node)
workflow.add_node("grade", grade_documents_node)
workflow.add_node("generate", generate_node)

workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "grade")
workflow.add_edge("grade", "generate")
workflow.add_edge("generate", END)

graph = workflow.compile()