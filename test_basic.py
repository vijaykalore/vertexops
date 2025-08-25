"""Basic tests for VertexOps platform"""
import pytest
from fastapi.testclient import TestClient
from vertexops.main import app
import json

def test_health_endpoint():
    """Test the health endpoint"""
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "services" in data

def test_root_endpoint():
    """Test the root endpoint"""
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        # Should return HTML
        assert "text/html" in response.headers.get("content-type", "")

def test_api_info_endpoint():
    """Test the API info endpoint"""
    with TestClient(app) as client:
        response = client.get("/api")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == "1.0.0"

def test_metrics_endpoint():
    """Test the metrics endpoint"""
    with TestClient(app) as client:
        response = client.get("/metrics")
        assert response.status_code == 200
        # Prometheus metrics should be plain text
        assert "text/plain" in response.headers.get("content-type", "")

def test_vector_add_requires_auth():
    """Test that vector endpoints require authentication"""
    with TestClient(app) as client:
        response = client.post("/vector/add", json={
            "text": "test document",
            "metadata": {}
        })
        assert response.status_code == 401  # Unauthorized

def test_vector_add_with_auth():
    """Test adding a vector with authentication"""
    with TestClient(app) as client:
        headers = {"x-api-key": "supersecret123"}
        response = client.post("/vector/add", 
            headers=headers,
            json={
                "text": "test document",
                "metadata": {}
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "record" in data

def test_rag_query_with_auth():
    """Test RAG query with authentication"""
    with TestClient(app) as client:
        # First add a document
        headers = {"x-api-key": "supersecret123"}
        client.post("/vector/add", 
            headers=headers,
            json={
                "text": "VertexOps is a powerful LLMOps platform",
                "metadata": {}
            }
        )
        
        # Now query
        response = client.post("/rag/query",
            headers=headers,
            json={
                "query": "What is VertexOps?",
                "max_results": 3
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "response_text" in data
        assert "source_docs" in data

if __name__ == "__main__":
    pytest.main([__file__])
