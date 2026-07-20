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