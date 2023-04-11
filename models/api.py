from models.models import (
    Document,
    DocumentMetadataFilter,
    Query,
    QueryResult
)
from pydantic import BaseModel
from typing import List, Optional

class WebSearchRequest(BaseModel):
    query: str

class WebSearchResult(BaseModel):
    title: Optional[str]=None
    link: Optional[str]=None
    description: Optional[str]=None

class WebSearchResponse(BaseModel):
    results: List[WebSearchResult]

class UpsertRequest(BaseModel):
    documents: List[Document]


class UpsertResponse(BaseModel):
    ids: List[str]


class QueryRequest(BaseModel):
    queries: List[Query]


class QueryResponse(BaseModel):
    results: List[QueryResult]


class DeleteRequest(BaseModel):
    ids: Optional[List[str]] = None
    filter: Optional[DocumentMetadataFilter] = None
    delete_all: Optional[bool] = False


class DeleteResponse(BaseModel):
    success: bool
