from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class QueryRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    query: str = Field(..., min_length=1)


class QueryResponse(BaseModel):
    query: str
    answer: str
    sources: list[str]


class IngestResponse(BaseModel):
    message: str
    chunks_indexed: int


class DocumentInfo(BaseModel):
    filename: str
    size_bytes: int


class DocumentsResponse(BaseModel):
    documents: list[DocumentInfo]


class FeedbackRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    query: str = Field(..., min_length=1)
    answer: str = Field(..., min_length=1)
    rating: Literal["up", "down"]
    comment: str | None = None


class FeedbackResponse(BaseModel):
    message: str
