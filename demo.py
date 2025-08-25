#!/usr/bin/env python3
"""
🚀 VertexOps Demo Script
========================

This script demonstrates the core functionality of the VertexOps platform.
Run this after starting the server to see all features in action.

Usage: python demo.py
"""

import requests
import json
import time
from typing import Dict, Any

# Configuration
API_KEY = "supersecret123"
BASE_URL = "http://127.0.0.1:8080"
HEADERS = {"x-api-key": API_KEY, "Content-Type": "application/json"}

def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"🔥 {title}")
    print(f"{'='*60}")

def print_response(response: requests.Response, operation: str):
    """Print formatted response"""
    if response.status_code == 200:
        print(f"✅ {operation} - Status: {response.status_code}")
        print(f"📊 Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"❌ {operation} - Status: {response.status_code}")
        print(f"Error: {response.text}")

def demo_basic_endpoints():
    """Test basic endpoints"""
    print_section("Basic Endpoints")
    
    # Test root endpoint
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "Root Endpoint")
    
    # Test health check
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Health Check")

def demo_vector_operations():
    """Demonstrate vector store operations"""
    print_section("Vector Store Operations")
    
    # Add sample documents
    sample_docs = [
        {"id": "doc1", "text": "VertexOps is a powerful LLMOps platform for managing AI models"},
        {"id": "doc2", "text": "FastAPI provides high-performance web APIs with automatic documentation"},
        {"id": "doc3", "text": "Vector databases enable semantic search and similarity matching"},
        {"id": "doc4", "text": "RAG (Retrieval Augmented Generation) combines search with language models"}
    ]
    
    for doc in sample_docs:
        response = requests.post(
            f"{BASE_URL}/vector/add",
            params={"id": doc["id"], "text": doc["text"]},
            headers={"x-api-key": API_KEY}
        )
        print_response(response, f"Adding document {doc['id']}")
        time.sleep(0.5)  # Small delay for demo effect

def demo_vector_search():
    """Demonstrate vector search"""
    print_section("Vector Search")
    
    search_queries = [
        "What is VertexOps?",
        "Tell me about FastAPI",
        "How does semantic search work?"
    ]
    
    for query in search_queries:
        response = requests.post(
            f"{BASE_URL}/vector/search",
            headers=HEADERS,
            json={"text": query, "top_k": 3}
        )
        print(f"\n🔍 Query: '{query}'")
        print_response(response, "Vector Search")

def demo_rag_queries():
    """Demonstrate RAG functionality"""
    print_section("RAG Query Processing")
    
    rag_queries = [
        "Explain what VertexOps does",
        "How can I use FastAPI for building APIs?",
        "What are the benefits of vector databases?"
    ]
    
    for query in rag_queries:
        response = requests.post(
            f"{BASE_URL}/rag/query",
            headers=HEADERS,
            json={"query": query, "top_k": 2}
        )
        print(f"\n🤖 RAG Query: '{query}'")
        print_response(response, "RAG Response")

def demo_model_operations():
    """Demonstrate model deployment and fine-tuning"""
    print_section("Model Operations")
    
    # Deploy a model
    deploy_data = {
        "model_type": "custom",
        "config": {
            "name": "demo-model-v1",
            "parameters": {"temperature": 0.7, "max_tokens": 256}
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/models/deploy",
        headers=HEADERS,
        json=deploy_data
    )
    print_response(response, "Model Deployment")
    
    if response.status_code == 200:
        model_id = response.json()["model_id"]
        print(f"📝 Model ID: {model_id}")
        
        # Wait a bit for deployment to "complete"
        print("⏳ Waiting for deployment to complete...")
        time.sleep(3)
        
        # Check model status
        response = requests.get(f"{BASE_URL}/models", headers={"x-api-key": API_KEY})
        print_response(response, "List Models")
        
        # Fine-tune the model
        finetune_data = {
            "dataset_uri": "gs://demo-bucket/training-data.csv"
        }
        response = requests.post(
            f"{BASE_URL}/models/{model_id}/finetune",
            headers=HEADERS,
            json=finetune_data
        )
        print_response(response, "Model Fine-tuning")

def demo_metrics():
    """Show Prometheus metrics"""
    print_section("Monitoring & Metrics")
    
    response = requests.get(f"{BASE_URL}/metrics")
    if response.status_code == 200:
        print("✅ Prometheus Metrics Available")
        # Show first few lines of metrics
        metrics_lines = response.text.split('\n')[:10]
        print("📈 Sample Metrics:")
        for line in metrics_lines:
            if line.strip() and not line.startswith('#'):
                print(f"   {line}")
    else:
        print(f"❌ Failed to retrieve metrics: {response.status_code}")

def main():
    """Run the complete demo"""
    print("""
    🚀 VertexOps Platform Demo
    ==========================
    
    This demo will showcase all the key features of VertexOps:
    • Basic API endpoints
    • Vector store operations  
    • Semantic search
    • RAG query processing
    • Model deployment & fine-tuning
    • Monitoring metrics
    
    Make sure the server is running on http://127.0.0.1:8080
    """)
    
    input("Press Enter to start the demo...")
    
    try:
        demo_basic_endpoints()
        demo_vector_operations()
        demo_vector_search()
        demo_rag_queries()
        demo_model_operations()
        demo_metrics()
        
        print_section("Demo Complete! 🎉")
        print("""
        ✅ All VertexOps features demonstrated successfully!
        
        🌐 Try the interactive docs: http://127.0.0.1:8080/docs
        📊 View metrics: http://127.0.0.1:8080/metrics
        
        Ready for production integration with:
        • Real AI models (OpenAI, Vertex AI)
        • Production vector databases
        • Advanced monitoring & logging
        """)
        
    except requests.ConnectionError:
        print("❌ Error: Could not connect to VertexOps server")
        print("Make sure the server is running: uvicorn vertexops.main:app --reload --host 127.0.0.1 --port 8080")
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")

if __name__ == "__main__":
    main()
