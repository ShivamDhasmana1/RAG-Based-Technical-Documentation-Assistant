from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="RAG Chatbot API", version="1.0.0")

app.include_router(router)


@app.get("/")
def health() -> dict:
    return {"status": "healthy", "service": "RAG Chatbot API"}