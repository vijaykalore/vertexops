import time
import uuid
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pathlib import Path
import os
from .schemas import (
    DeployRequest, DeployResponse, FineTuneRequest, FineTuneResponse,
    RAGQueryRequest, RAGQueryResponse, VectorSearchRequest, VectorSearchResponse
)
from .auth import get_api_key
from .vector_store import InMemoryVectorStore
from .model_service import ModelService
from .rag_service import RAGService
from .monitoring import record_request, metrics_response
from time import perf_counter

app = FastAPI(title="VertexOps - LLMOps Platform (Local MVP)")

# CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
vector_store = InMemoryVectorStore()
model_service = ModelService()
rag_service = RAGService(vector_store)

# Ensure models.json exists
Path("vertexops").mkdir(exist_ok=True)

# Middleware-like helper to record metrics (simple)
@app.middleware("http")
async def add_metrics(request, call_next):
    start = perf_counter()
    try:
        response = await call_next(request)
        latency = perf_counter() - start
        record_request(request.method, request.url.path, str(response.status_code), latency)
        return response
    except Exception as e:
        latency = perf_counter() - start
        record_request(request.method, request.url.path, "500", latency)
        raise

@app.get("/metrics")
def prometheus_metrics():
    return metrics_response()

@app.post("/models/deploy", response_model=DeployResponse)
async def deploy_model(req: DeployRequest, api_key: str = Depends(get_api_key)):
    entry = model_service.deploy_model(req.model_type, req.config)
    return DeployResponse(model_id=entry["model_id"], status=entry["status"], message=entry.get("message"))

@app.post("/models/{model_id}/finetune", response_model=FineTuneResponse)
async def finetune_model(model_id: str, req: FineTuneRequest, api_key: str = Depends(get_api_key)):
    status = model_service.get_status(model_id)
    if not status:
        raise HTTPException(status_code=404, detail="Model not found")
    job = model_service.fine_tune(model_id, req.dataset_uri)
    return FineTuneResponse(job_id=job["job_id"], status=job["status"])

@app.post("/rag/query", response_model=RAGQueryResponse)
async def rag_query(req: RAGQueryRequest, api_key: str = Depends(get_api_key)):
    res = await rag_service.generate_response(req.query, top_k=req.top_k or 5)
    return RAGQueryResponse(response_text=res["response_text"], source_docs=res["source_docs"], confidence_score=res["confidence_score"])

@app.post("/vector/search", response_model=VectorSearchResponse)
async def vector_search(req: VectorSearchRequest, api_key: str = Depends(get_api_key)):
    if req.embedding is None:
        if req.text:
            from .utils import text_to_embedding
            emb = text_to_embedding(req.text)
        else:
            raise HTTPException(status_code=400, detail="Provide embedding or text")
    else:
        emb = req.embedding
    results = vector_store.search(emb, top_k=req.top_k)
    return VectorSearchResponse(results=results)

# Utility endpoints for data ingestion and listing models / vectors (for testing)
@app.post("/vector/add")
async def add_vector(id: str, text: str, api_key: str = Depends(get_api_key)):
    rec = vector_store.add_text(id=id, text=text)
    return {"status": "ok", "record": rec}

@app.get("/models")
async def list_models(api_key: str = Depends(get_api_key)):
    # Return models.json content
    import json
    p = Path("vertexops/models.json")
    if p.exists():
        return json.loads(p.read_text())
    return {}

@app.get("/")
def root():
    return {
        "message": "🚀 Welcome to VertexOps - LLMOps Platform (Local MVP)",
        "version": "1.0.0",
        "docs": "http://127.0.0.1:8080/docs",
        "metrics": "http://127.0.0.1:8080/metrics",
        "features": [
            "Model Deployment & Fine-tuning",
            "RAG Query Processing", 
            "Vector Search",
            "API Key Authentication",
            "Prometheus Metrics"
        ],
        "auth_note": "Include 'x-api-key: supersecret123' header for authenticated endpoints",
        "status": "running"
    }

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "services": {
            "vector_store": "active",
            "model_service": "active", 
            "rag_service": "active"
        }
    }
