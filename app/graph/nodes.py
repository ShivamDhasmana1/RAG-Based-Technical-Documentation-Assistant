from langchain_groq import ChatGroq
from prompts import GRADE_PROMPT, GENERATION_PROMPT
from app.config import GROQ_API_KEY, MODEL_NAME
from app.graph.state import GraphState
from app.retriever.retriever import retrieve_documents

def retrieve_node(state: GraphState) -> GraphState:
    query = state["current_query"]
    state["retrieved_documents"] = retrieve_documents(query)
    return state


def grade_documents_node(state: GraphState) -> GraphState:
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
    query = state["current_query"]
    context = "\n\n".join(doc.page_content for doc in state["relevant_documents"])

    llm = ChatGroq(api_key=GROQ_API_KEY, model=MODEL_NAME, temperature=0)
    prompt = GENERATION_PROMPT.format(query=query, context=context)
    response = llm.invoke(prompt)

    state["answer"] = response.content
    return state