from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from app.config import CHROMA_DB_DIR, EMBEDDING_MODEL
from app.ingestion.chunker import chunk_documents
from app.ingestion.loader import load_documents


def ingest_documents() -> tuple[Chroma, int]:
    documents = load_documents()
    chunks = chunk_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    vector_store = Chroma(
        persist_directory=str(CHROMA_DB_DIR),
        embedding_function=embeddings,
    )

    vector_store.add_documents(chunks)

    return vector_store, len(chunks)