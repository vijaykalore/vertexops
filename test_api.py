import requests
import json

# Test the VertexOps API
API_KEY = "supersecret123"
BASE_URL = "http://127.0.0.1:8080"

headers = {"x-api-key": API_KEY}

# Test 1: Add a document to vector store
print("Testing vector add...")
response = requests.post(f"{BASE_URL}/vector/add?id=doc1&text=This is about VertexOps testing", 
                        headers=headers)
print(f"Vector add response: {response.status_code} - {response.json()}")

# Test 2: Query RAG
print("\nTesting RAG query...")
rag_data = {"query": "Tell me about VertexOps", "top_k": 3}
response = requests.post(f"{BASE_URL}/rag/query", 
                        headers={**headers, "Content-Type": "application/json"}, 
                        json=rag_data)
print(f"RAG query response: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"Response text: {result['response_text']}")
    print(f"Confidence: {result['confidence_score']}")

# Test 3: Deploy a model
print("\nTesting model deployment...")
deploy_data = {"model_type": "custom", "config": {"param": "value"}}
response = requests.post(f"{BASE_URL}/models/deploy", 
                        headers={**headers, "Content-Type": "application/json"}, 
                        json=deploy_data)
print(f"Model deploy response: {response.status_code} - {response.json()}")

print("\nAll tests completed!")
