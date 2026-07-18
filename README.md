# RAG Technical Documentation Assistant

A Retrieval-Augmented Generation system that answers technical documentation
questions using a LangGraph-based agentic workflow.

## Stack

- Python
- FastAPI
- LangGraph
- ChromaDB
- Sentence Transformers
- UV (package manager)

## Workflow

1. Query Analysis
2. Retrieval
3. Document Grading
4. Conditional Routing
5. Query Rewrite (Retry)
6. Answer Generation

## Project Structure

```
rag-assistant/
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── graph/
│   │   ├── workflow.py
│   │   ├── nodes.py
│   │   └── state.py
│   ├── ingestion/
│   │   ├── loader.py
│   │   ├── chunker.py
│   │   └── ingest.py
│   ├── retriever/
│   │   └── retriever.py
│   ├── config.py
│   ├── prompts.py
│   ├── schemas.py
│   └── main.py
├── data/
│   └── raw/
├── tests/
├── README.md
└── pyproject.toml
```

## Setup

```bash
uv sync
cp .env.example .env
```

## Run

```bash
uv run uvicorn app.main:app --reload
```

## Ingest Documents

```bash
uv run python -m app.ingestion.ingest
```
