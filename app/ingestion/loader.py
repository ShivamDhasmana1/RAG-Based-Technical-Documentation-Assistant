from typing import Any

from langchain_community.document_loaders import PyPDFLoader, TextLoader

from app.config import RAW_DATA_DIR

SUPPORTED_EXTENSIONS = {".pdf", ".md"}


def load_documents() -> list[Any]:
    documents = []

    for file_path in RAW_DATA_DIR.iterdir():
        suffix = file_path.suffix.lower()

        if suffix not in SUPPORTED_EXTENSIONS:
            continue

        if suffix == ".pdf":
            loader = PyPDFLoader(str(file_path))
        else:
            loader = TextLoader(str(file_path))

        documents.extend(loader.load())

    if not documents:
        raise ValueError(f"No supported documents found in {RAW_DATA_DIR}")

    return documents