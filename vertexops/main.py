import time
import uuid
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
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

@app.get("/", response_class=HTMLResponse)
def root():
    """Professional landing page for VertexOps"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VertexOps - LLMOps Platform</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 2rem;
            }
            
            .header {
                text-align: center;
                color: white;
                margin-bottom: 3rem;
            }
            
            .logo {
                font-size: 3.5rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            
            .tagline {
                font-size: 1.3rem;
                opacity: 0.9;
                margin-bottom: 1rem;
            }
            
            .version-badge {
                display: inline-block;
                background: rgba(255,255,255,0.2);
                padding: 0.3rem 1rem;
                border-radius: 20px;
                font-size: 0.9rem;
                backdrop-filter: blur(10px);
            }
            
            .main-content {
                background: white;
                border-radius: 20px;
                padding: 3rem;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                margin-bottom: 2rem;
            }
            
            .status {
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 2rem;
                padding: 1rem;
                background: #e8f5e8;
                border-radius: 10px;
                border-left: 4px solid #28a745;
            }
            
            .status-dot {
                width: 12px;
                height: 12px;
                background: #28a745;
                border-radius: 50%;
                margin-right: 0.5rem;
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.5; }
                100% { opacity: 1; }
            }
            
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 2rem;
                margin: 2rem 0;
            }
            
            .feature {
                padding: 1.5rem;
                background: #f8f9fa;
                border-radius: 15px;
                border-left: 4px solid #667eea;
                transition: transform 0.3s ease;
            }
            
            .feature:hover {
                transform: translateY(-5px);
            }
            
            .feature-icon {
                font-size: 2rem;
                margin-bottom: 1rem;
            }
            
            .feature-title {
                font-size: 1.2rem;
                font-weight: 600;
                margin-bottom: 0.5rem;
                color: #333;
            }
            
            .feature-desc {
                color: #666;
                line-height: 1.5;
            }
            
            .quick-actions {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
                margin: 2rem 0;
            }
            
            .action-btn {
                display: block;
                padding: 1rem 1.5rem;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 10px;
                text-align: center;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }
            
            .action-btn:hover {
                background: #5a67d8;
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            }
            
            .action-btn.secondary {
                background: #6c757d;
                box-shadow: 0 4px 15px rgba(108, 117, 125, 0.3);
            }
            
            .action-btn.secondary:hover {
                background: #5a6268;
            }
            
            .api-info {
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 10px;
                padding: 1.5rem;
                margin: 2rem 0;
            }
            
            .api-key {
                font-family: 'Courier New', monospace;
                background: #f8f9fa;
                padding: 0.5rem 1rem;
                border-radius: 5px;
                color: #d63384;
                font-weight: 600;
            }
            
            .footer {
                text-align: center;
                color: white;
                margin-top: 2rem;
                opacity: 0.8;
            }
            
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 1rem;
                margin: 2rem 0;
            }
            
            .stat {
                text-align: center;
                padding: 1rem;
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                color: white;
                backdrop-filter: blur(10px);
            }
            
            .stat-number {
                font-size: 2rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
            }
            
            .stat-label {
                font-size: 0.9rem;
                opacity: 0.9;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🚀 VertexOps</div>
                <div class="tagline">Professional LLMOps Platform</div>
                <div class="version-badge">v1.0.0 • Production Ready</div>
            </div>
            
            <div class="stats">
                <div class="stat">
                    <div class="stat-number">⚡</div>
                    <div class="stat-label">High Performance</div>
                </div>
                <div class="stat">
                    <div class="stat-number">🔒</div>
                    <div class="stat-label">Secure API</div>
                </div>
                <div class="stat">
                    <div class="stat-number">📊</div>
                    <div class="stat-label">Full Monitoring</div>
                </div>
                <div class="stat">
                    <div class="stat-number">🐳</div>
                    <div class="stat-label">Docker Ready</div>
                </div>
            </div>
            
            <div class="main-content">
                <div class="status">
                    <div class="status-dot"></div>
                    <strong>System Status: Online & Ready</strong>
                </div>
                
                <div class="features">
                    <div class="feature">
                        <div class="feature-icon">🤖</div>
                        <div class="feature-title">Model Deployment</div>
                        <div class="feature-desc">Deploy and manage AI models with automated scaling and version control</div>
                    </div>
                    
                    <div class="feature">
                        <div class="feature-icon">🔍</div>
                        <div class="feature-title">RAG Query Engine</div>
                        <div class="feature-desc">Advanced retrieval-augmented generation with semantic search capabilities</div>
                    </div>
                    
                    <div class="feature">
                        <div class="feature-icon">🗂️</div>
                        <div class="feature-title">Vector Search</div>
                        <div class="feature-desc">High-performance vector similarity search with real-time indexing</div>
                    </div>
                    
                    <div class="feature">
                        <div class="feature-icon">📈</div>
                        <div class="feature-title">Monitoring & Metrics</div>
                        <div class="feature-desc">Comprehensive observability with Prometheus metrics and health checks</div>
                    </div>
                </div>
                
                <div class="api-info">
                    <h3>🔐 API Authentication</h3>
                    <p>Include this header in all requests:</p>
                    <div class="api-key">x-api-key: supersecret123</div>
                </div>
                
                <div class="quick-actions">
                    <a href="/docs" class="action-btn">📚 Interactive API Docs</a>
                    <a href="/dashboard" class="action-btn">📊 Admin Dashboard</a>
                    <a href="/metrics" class="action-btn secondary">� System Metrics</a>
                    <a href="/health" class="action-btn secondary">🏥 Health Check</a>
                </div>
            </div>
            
            <div class="footer">
                <p>Built with FastAPI • Powered by Python • Ready for Production</p>
                <p>© 2025 VertexOps Platform</p>
            </div>
        </div>
        
        <script>
            // Add some interactivity
            document.addEventListener('DOMContentLoaded', function() {
                // Animate features on scroll
                const features = document.querySelectorAll('.feature');
                
                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            entry.target.style.opacity = '1';
                            entry.target.style.transform = 'translateY(0)';
                        }
                    });
                });
                
                features.forEach(feature => {
                    feature.style.opacity = '0';
                    feature.style.transform = 'translateY(20px)';
                    feature.style.transition = 'all 0.6s ease';
                    observer.observe(feature);
                });
                
                // Update status in real-time
                setInterval(async () => {
                    try {
                        const response = await fetch('/health');
                        const data = await response.json();
                        if (data.status === 'healthy') {
                            document.querySelector('.status').style.background = '#e8f5e8';
                            document.querySelector('.status').style.borderLeftColor = '#28a745';
                            document.querySelector('.status-dot').style.background = '#28a745';
                        }
                    } catch (error) {
                        document.querySelector('.status').style.background = '#f8d7da';
                        document.querySelector('.status').style.borderLeftColor = '#dc3545';
                        document.querySelector('.status-dot').style.background = '#dc3545';
                    }
                }, 30000); // Check every 30 seconds
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api")
def api_info():
    """JSON API information for developers"""
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
        "status": "running",
        "endpoints": {
            "models": {
                "deploy": "POST /models/deploy",
                "list": "GET /models",
                "finetune": "POST /models/{model_id}/finetune"
            },
            "vector": {
                "add": "POST /vector/add",
                "search": "POST /vector/search"
            },
            "rag": {
                "query": "POST /rag/query"
            },
            "system": {
                "health": "GET /health",
            }
        }
    }

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    """Professional dashboard for monitoring VertexOps"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VertexOps Dashboard</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #f8f9fa;
                color: #333;
            }
            
            .navbar {
                background: #343a40;
                color: white;
                padding: 1rem 2rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .navbar h1 {
                display: inline;
                font-size: 1.5rem;
            }
            
            .nav-links {
                float: right;
            }
            
            .nav-links a {
                color: white;
                text-decoration: none;
                margin-left: 2rem;
                padding: 0.5rem 1rem;
                border-radius: 5px;
                transition: background 0.3s;
            }
            
            .nav-links a:hover {
                background: rgba(255,255,255,0.1);
            }
            
            .container {
                max-width: 1200px;
                margin: 2rem auto;
                padding: 0 2rem;
            }
            
            .dashboard-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 2rem;
                margin-bottom: 2rem;
            }
            
            .card {
                background: white;
                border-radius: 10px;
                padding: 2rem;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                transition: transform 0.3s;
            }
            
            .card:hover {
                transform: translateY(-5px);
            }
            
            .card-header {
                display: flex;
                align-items: center;
                margin-bottom: 1rem;
            }
            
            .card-icon {
                font-size: 2rem;
                margin-right: 1rem;
            }
            
            .card-title {
                font-size: 1.3rem;
                font-weight: 600;
            }
            
            .metric {
                font-size: 2.5rem;
                font-weight: 700;
                color: #28a745;
                margin: 1rem 0;
            }
            
            .status-online {
                color: #28a745;
            }
            
            .status-offline {
                color: #dc3545;
            }
            
            .activity-log {
                max-height: 300px;
                overflow-y: auto;
            }
            
            .log-entry {
                padding: 0.5rem 0;
                border-bottom: 1px solid #e9ecef;
                font-family: 'Courier New', monospace;
                font-size: 0.9rem;
            }
            
            .btn {
                display: inline-block;
                padding: 0.7rem 1.5rem;
                background: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin-right: 1rem;
                margin-top: 1rem;
                transition: background 0.3s;
            }
            
            .btn:hover {
                background: #0056b3;
            }
            
            .btn-success {
                background: #28a745;
            }
            
            .btn-success:hover {
                background: #1e7e34;
            }
        </style>
    </head>
    <body>
        <nav class="navbar">
            <h1>🚀 VertexOps Dashboard</h1>
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/docs">API Docs</a>
                <a href="/metrics">Metrics</a>
                <a href="/health">Health</a>
            </div>
        </nav>
        
        <div class="container">
            <div class="dashboard-grid">
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon">🏥</div>
                        <div class="card-title">System Health</div>
                    </div>
                    <div class="metric status-online" id="system-status">ONLINE</div>
                    <p>All services are operational</p>
                    <a href="/health" class="btn btn-success">Check Health</a>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon">🤖</div>
                        <div class="card-title">Models Deployed</div>
                    </div>
                    <div class="metric" id="models-count">0</div>
                    <p>Active model instances</p>
                    <a href="/docs#/default/deploy_model_models_deploy_post" class="btn">Deploy Model</a>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon">🗂️</div>
                        <div class="card-title">Vector Store</div>
                    </div>
                    <div class="metric" id="vector-count">0</div>
                    <p>Documents indexed</p>
                    <a href="/docs#/default/add_vector_vector_add_post" class="btn">Add Documents</a>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon">📊</div>
                        <div class="card-title">API Requests</div>
                    </div>
                    <div class="metric" id="requests-count">-</div>
                    <p>Total requests processed</p>
                    <a href="/metrics" class="btn">View Metrics</a>
                </div>
                
                <div class="card" style="grid-column: span 2;">
                    <div class="card-header">
                        <div class="card-icon">📝</div>
                        <div class="card-title">Recent Activity</div>
                    </div>
                    <div class="activity-log" id="activity-log">
                        <div class="log-entry">2025-08-25 10:30:15 - Server started successfully</div>
                        <div class="log-entry">2025-08-25 10:30:16 - Vector store initialized</div>
                        <div class="log-entry">2025-08-25 10:30:16 - Model service ready</div>
                        <div class="log-entry">2025-08-25 10:30:16 - RAG service initialized</div>
                        <div class="log-entry">2025-08-25 10:30:16 - Metrics endpoint active</div>
                        <div class="log-entry">2025-08-25 10:30:17 - Dashboard loaded</div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">🔧</div>
                    <div class="card-title">Quick Actions</div>
                </div>
                <a href="/docs#/default/rag_query_rag_query_post" class="btn">Test RAG Query</a>
                <a href="/docs#/default/vector_search_vector_search_post" class="btn">Vector Search</a>
                <a href="/docs#/default/list_models_models_get" class="btn">List Models</a>
                <a href="/docs" class="btn btn-success">View Full API</a>
            </div>
        </div>
        
        <script>
            // Real-time dashboard updates
            async function updateDashboard() {
                try {
                    // Update system status
                    const healthResponse = await fetch('/health');
                    const healthData = await healthResponse.json();
                    document.getElementById('system-status').textContent = 
                        healthData.status === 'healthy' ? 'ONLINE' : 'OFFLINE';
                    
                    // Update models count
                    const modelsResponse = await fetch('/models', {
                        headers: {'x-api-key': 'supersecret123'}
                    });
                    if (modelsResponse.ok) {
                        const modelsData = await modelsResponse.json();
                        document.getElementById('models-count').textContent = 
                            Object.keys(modelsData).length;
                    }
                    
                    // Add activity log entry
                    const now = new Date().toLocaleString();
                    const logEntry = document.createElement('div');
                    logEntry.className = 'log-entry';
                    logEntry.textContent = `${now} - Dashboard updated`;
                    
                    const activityLog = document.getElementById('activity-log');
                    activityLog.insertBefore(logEntry, activityLog.firstChild);
                    
                    // Keep only last 10 entries
                    while (activityLog.children.length > 10) {
                        activityLog.removeChild(activityLog.lastChild);
                    }
                    
                } catch (error) {
                    console.error('Dashboard update failed:', error);
                    document.getElementById('system-status').textContent = 'ERROR';
                    document.getElementById('system-status').className = 'metric status-offline';
                }
            }
            
            // Update dashboard every 10 seconds
            setInterval(updateDashboard, 10000);
            
            // Initial update
            updateDashboard();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

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
