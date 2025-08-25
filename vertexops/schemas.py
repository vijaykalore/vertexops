from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class DeployRequest(BaseModel):
    model_type: str  # "openai"|"vertex"|"custom"
    config: Optional[Dict[str, Any]] = {}

class DeployResponse(BaseModel):
    model_id: str
    status: str
    message: Optional[str] = None

class FineTuneRequest(BaseModel):
    dataset_uri: str  # e.g. gs://bucket/dataset.csv or local path

class FineTuneResponse(BaseModel):
    job_id: str
    status: str

class RAGQueryRequest(BaseModel):
    query: str
    context_sources: Optional[List[str]] = []
    top_k: Optional[int] = 5

class RAGQueryResponse(BaseModel):
    response_text: str
    source_docs: List[Dict[str, Any]]
    confidence_score: float

class VectorSearchRequest(BaseModel):
    embedding: Optional[List[float]] = None
    text: Optional[str] = None
    top_k: int = 5

class VectorSearchResponse(BaseModel):
    results: List[Dict[str, Any]]
