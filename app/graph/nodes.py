from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY, MODEL_NAME
from app.graph.state import GraphState
from app.prompts import (
    ANALYZE_QUERY_PROMPT,
    GENERATION_PROMPT,
    GRADE_PROMPT,
    REWRITE_QUERY_PROMPT,
)
from app.retriever.retriever import retrieve_documents

VALID_QUERY_TYPES = {"conceptual", "how_to", "troubleshooting", "api_reference"}

# Instantiated once at import time and reused by every node below, instead
# of being recreated (and re-authenticated) on every single graph step.
# app.config.validate_config() runs when app.config is first imported, so
# GROQ_API_KEY is guaranteed to be a non-empty string here.
llm = ChatGroq(api_key=GROQ_API_KEY, model=MODEL_NAME, temperature=0)


def analyze_query_node(state: GraphState) -> GraphState:
    """Classify the query and rewrite it for better retrieval before searching."""
    query = state["query"]

    prompt = ANALYZE_QUERY_PROMPT.format(query=query)
    response = llm.invoke(prompt).content.strip()

    query_type = "conceptual"
    rewritten_query = query
    for line in response.splitlines():
        if line.upper().startswith("TYPE:"):
            candidate = line.split(":", 1)[1].strip().lower()
            if candidate in VALID_QUERY_TYPES:
                query_type = candidate
        elif line.upper().startswith("QUERY:"):
            candidate = line.split(":", 1)[1].strip()
            if candidate:
                rewritten_query = candidate

    state["query_type"] = query_type
    state["current_query"] = rewritten_query
    return state


def retrieve_node(state: GraphState) -> GraphState:
    """Fetch documents relevant to the current query."""
    query = state["current_query"]
    state["retrieved_documents"] = retrieve_documents(query)
    return state


def grade_documents_node(state: GraphState) -> GraphState:
    """Filter retrieved documents down to ones relevant to the query."""
    query = state["current_query"]

    relevant_documents = []
    for document in state.get("retrieved_documents", []) or []:
        prompt = GRADE_PROMPT.format(query=query, document=document.page_content)
        response = llm.invoke(prompt)
        if response.content.strip().lower().startswith("yes"):
            relevant_documents.append(document)

    state["relevant_documents"] = relevant_documents
    return state


def generate_node(state: GraphState) -> GraphState:
    """Generate the final answer, citing sources from the relevant documents."""
    query = state["current_query"]
    documents = state.get("relevant_documents", []) or []

    sources = []
    context_blocks = []
    for document in documents:
        source = document.metadata.get("source", "unknown")
        if source not in sources:
            sources.append(source)
        context_blocks.append(f"[source: {source}]\n{document.page_content}")

    context = (
        "\n\n".join(context_blocks)
        if context_blocks
        else "No relevant documentation was found."
    )

    prompt = GENERATION_PROMPT.format(query=query, context=context)
    response = llm.invoke(prompt)

    state["answer"] = response.content
    state["sources"] = sources
    return state


def rewrite_query_node(state: GraphState) -> GraphState:
    """Rewrite the query to improve retrieval on the next attempt."""
    query = state["current_query"]

    prompt = REWRITE_QUERY_PROMPT.format(query=query)
    response = llm.invoke(prompt)

    state["current_query"] = response.content.strip()
    state["retry_count"] = state.get("retry_count", 0) + 1
    return state
