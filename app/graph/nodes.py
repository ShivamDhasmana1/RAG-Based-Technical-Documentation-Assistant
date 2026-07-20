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


def analyze_query_node(state: GraphState) -> GraphState:
    """Classify the query and rewrite it for better retrieval before searching."""
    query = state["query"]
    llm = ChatGroq(api_key=GROQ_API_KEY, model=MODEL_NAME, temperature=0)

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
    llm = ChatGroq(api_key=GROQ_API_KEY, model=MODEL_NAME, temperature=0)

    relevant_documents = []
    for document in state["retrieved_documents"]:
        prompt = GRADE_PROMPT.format(query=query, document=document.page_content)
        response = llm.invoke(prompt)
        if response.content.strip().lower().startswith("yes"):
            relevant_documents.append(document)

    state["relevant_documents"] = relevant_documents
    return state


def generate_node(state: GraphState) -> GraphState:
    """Generate the final answer, citing sources from the relevant documents."""
    query = state["current_query"]
    documents = state["relevant_documents"]

    sources = []
    context_blocks = []
    for document in documents:
        source = document.metadata.get("source", "unknown")
        if source not in sources:
            sources.append(source)
        context_blocks.append(f"[source: {source}]\n{document.page_content}")

    context = "\n\n".join(context_blocks)

    llm = ChatGroq(api_key=GROQ_API_KEY, model=MODEL_NAME, temperature=0)
    prompt = GENERATION_PROMPT.format(query=query, context=context)
    response = llm.invoke(prompt)

    state["answer"] = response.content
    state["sources"] = sources
    return state


def rewrite_query_node(state: GraphState) -> GraphState:
    """Rewrite the query to improve retrieval on the next attempt."""
    query = state["current_query"]

    llm = ChatGroq(api_key=GROQ_API_KEY, model=MODEL_NAME, temperature=0)
    prompt = REWRITE_QUERY_PROMPT.format(query=query)
    response = llm.invoke(prompt)

    state["current_query"] = response.content.strip()
    state["retry_count"] += 1
    return state
