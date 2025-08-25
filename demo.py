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
        try:
            result = response.json()
            print(f"📊 Response: {json.dumps(result, indent=2)}")
        except:
            print(f"📊 Response: {response.text}")
    else:
        print(f"❌ {operation} - Status: {response.status_code}")
        print(f"Error: {response.text}")

def test_connection():
    """Test if server is accessible"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def demo_basic_endpoints():
    """Test basic endpoints"""
    print_section("Basic Endpoints")
    
    try:
        # Test root endpoint
        response = requests.get(f"{BASE_URL}/api", timeout=10)
        print_response(response, "API Info Endpoint")
        
        # Test health check
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        print_response(response, "Health Check")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")

def demo_vector_operations():
    """Demonstrate vector store operations"""
    print_section("Vector Store Operations")
    
    # Add sample documents
    sample_docs = [
        {"id": "doc1", "text": "VertexOps is a powerful LLMOps platform for managing AI models"},
        {"id": "doc2", "text": "FastAPI provides high-performance web APIs with automatic documentation"}
    ]
    
    for doc in sample_docs:
        try:
            response = requests.post(
                f"{BASE_URL}/vector/add",
                params={"id": doc["id"], "text": doc["text"]},
                headers={"x-api-key": API_KEY},
                timeout=10
            )
            print_response(response, f"Adding document {doc['id']}")
            time.sleep(1)  # Small delay
        except requests.exceptions.RequestException as e:
            print(f"❌ Error adding document {doc['id']}: {e}")

def demo_rag_queries():
    """Demonstrate RAG functionality"""
    print_section("RAG Query Processing")
    
    try:
        query = "What is VertexOps?"
        response = requests.post(
            f"{BASE_URL}/rag/query",
            headers=HEADERS,
            json={"query": query, "top_k": 2},
            timeout=15
        )
        print(f"\n🤖 RAG Query: '{query}'")
        print_response(response, "RAG Response")
    except requests.exceptions.RequestException as e:
        print(f"❌ RAG query error: {e}")

def demo_model_operations():
    """Demonstrate model deployment"""
    print_section("Model Operations")
    
    try:
        # Deploy a model
        deploy_data = {
            "model_type": "custom",
            "config": {"name": "demo-model-v1"}
        }
        
        response = requests.post(
            f"{BASE_URL}/models/deploy",
            headers=HEADERS,
            json=deploy_data,
            timeout=15
        )
        print_response(response, "Model Deployment")
        
        if response.status_code == 200:
            print("⏳ Waiting for deployment to complete...")
            time.sleep(3)
            
            # List models
            response = requests.get(f"{BASE_URL}/models", 
                                 headers={"x-api-key": API_KEY},
                                 timeout=10)
            print_response(response, "List Models")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Model operation error: {e}")

def main():
    """Run the complete demo"""
    print("""
    🚀 VertexOps Platform Demo
    ==========================
    
    This demo will test all key features of VertexOps locally.
    Make sure the server is running on http://127.0.0.1:8080
    """)
    
    # Test connection first
    print("🔍 Testing server connection...")
    if not test_connection():
        print("""
        ❌ Cannot connect to VertexOps server!
        
        Please make sure the server is running:
        uvicorn vertexops.main:app --reload --host 127.0.0.1 --port 8080
        
        Then try running the demo again.
        """)
        return
    
    print("✅ Server connection successful!")
    input("\nPress Enter to start the demo...")
    
    try:
        demo_basic_endpoints()
        demo_vector_operations()
        demo_rag_queries()
        demo_model_operations()
        
        print_section("Demo Complete! 🎉")
        print("""
        ✅ All VertexOps features tested successfully!
        
        🌐 Access the web interface: http://127.0.0.1:8080
        � Interactive API docs: http://127.0.0.1:8080/docs
        📊 Dashboard: http://127.0.0.1:8080/dashboard
        📈 Metrics: http://127.0.0.1:8080/metrics
        """)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo failed with error: {e}")

if __name__ == "__main__":
    main()
