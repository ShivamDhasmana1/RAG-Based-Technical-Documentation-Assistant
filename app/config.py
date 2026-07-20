import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
CHROMA_DB_DIR = DATA_DIR / "chroma"

# Chunking constants
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval constants
TOP_K_RESULTS = 5

# Workflow constants
MAX_RETRIES = 2


def validate_config() -> None:
    """Validate required configuration values.

    Raises:
        RuntimeError: if a required environment variable is missing, so the
        app fails fast at startup with a clear message instead of crashing
        deep inside a graph node the first time an LLM call is made (which
        previously surfaced as an opaque HTTP 500 from POST /api/query).
    """
    missing = []
    if not GROQ_API_KEY:
        missing.append("GROQ_API_KEY")

    if missing:
        raise RuntimeError(
            "Missing required environment variable(s): "
            f"{', '.join(missing)}. Set them in a .env file "
            "(see .env.example) before starting the app."
        )


# Validate as soon as config is imported (i.e. before any other module can
# construct a ChatGroq client with a None api_key). This is the first module
# imported by every other part of the app (nodes, retriever, ingest, etc.).
validate_config()