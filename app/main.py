from fastapi import FastAPI

from app.config import validate_config

# Fail fast if required configuration (e.g. GROQ_API_KEY) is missing, before
# the router (and the ChatGroq client it depends on) is even imported.
validate_config()

from app.api.routes import router  # noqa: E402

app = FastAPI(title="RAG Chatbot API", version="1.0.0")

app.include_router(router)


@app.get("/")
def health() -> dict:
    return {"status": "healthy", "service": "RAG Chatbot API"}