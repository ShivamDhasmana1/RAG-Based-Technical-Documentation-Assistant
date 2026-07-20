from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from app.config import CHROMA_DB_DIR, EMBEDDING_MODEL, TOP_K_RESULTS

# The embedding model, Chroma connection, and retriever are expensive to
# create (the embedding model in particular loads weights from disk/HF hub),
# so they are built once at import time and reused across every request
# instead of being reconstructed on every call to retrieve_documents().
_embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

_vector_store = Chroma(
    persist_directory=str(CHROMA_DB_DIR),
    embedding_function=_embeddings,
)

_retriever = _vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": TOP_K_RESULTS},
)


def retrieve_documents(query: str) -> list[Document]:
    """Return documents relevant to `query`.

    Never raises: an empty/unseeded Chroma collection or a blank query
    simply yields no documents, letting the graph route to rewrite/end
    instead of crashing the request.
    """
    if not query or not query.strip():
        return []

    try:
        results = _retriever.invoke(query)
    except Exception:
        # Some Chroma versions raise instead of returning [] when the
        # collection has never been populated. Treat that as "no results".
        return []

    return results or []