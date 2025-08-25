# 🚀 VertexOps - LLMOps Platform (Local MVP)

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](Dockerfile)

> A minimal but extensible LLMOps platform built with FastAPI, featuring model deployment, RAG queries, vector search, and monitoring capabilities.

![VertexOps Demo](https://via.placeholder.com/800x400/1e1e1e/ffffff?text=VertexOps+Local+MVP)

## ✨ Features

- 🤖 **Model Deployment & Fine-tuning** (Simulated with realistic async processing)
- 🔍 **RAG Query System** with intelligent context retrieval
- 📊 **Vector Search** using cosine similarity
- 🔐 **API Key Authentication** for secure access
- 📈 **Prometheus Metrics** for monitoring and observability
- 🐳 **Docker Support** for easy deployment
- 📚 **Interactive API Documentation** with Swagger UI
- 🔄 **Hot Reload** for development
- 🌐 **CORS Support** for web applications

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        VertexOps Platform                      │
├─────────────────────────────────────────────────────────────────┤
│  FastAPI Server (Port 8080)                                    │
│  ├── 🔐 Authentication Layer                                   │
│  ├── 📊 Prometheus Metrics                                     │
│  └── 🌐 CORS Middleware                                        │
├─────────────────────────────────────────────────────────────────┤
│  Core Services                                                 │
│  ├── 🤖 Model Service (Deploy/Fine-tune)                      │
│  ├── 🗂️  Vector Store (In-memory)                             │
│  ├── 🔍 RAG Service (Query Processing)                        │
│  └── 📈 Monitoring Service                                     │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Git

### 1. Clone & Setup
```bash
git clone https://github.com/vijaykalore/vertexops.git
cd vertexops
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux
```

### 3. Start the Server
```bash
uvicorn vertexops.main:app --reload --host 127.0.0.1 --port 8080
```

### 4. Access the Platform
- **🏠 Main Interface**: http://127.0.0.1:8080
- **📊 Admin Dashboard**: http://127.0.0.1:8080/dashboard  
- **📚 Interactive API Docs**: http://127.0.0.1:8080/docs
- **🏥 Health Check**: http://127.0.0.1:8080/health
- **📈 Metrics**: http://127.0.0.1:8080/metrics

## 📖 API Usage Examples

### 🔐 Authentication
All endpoints require the `x-api-key` header:
```bash
-H "x-api-key: supersecret123"
```

### 📝 Add Document to Vector Store
```bash
curl -X POST "http://127.0.0.1:8080/vector/add?id=doc1&text=VertexOps%20is%20awesome" \
  -H "x-api-key: supersecret123"
```

### 🤖 Deploy a Model
```bash
curl -X POST "http://127.0.0.1:8080/models/deploy" \
  -H "Content-Type: application/json" \
  -H "x-api-key: supersecret123" \
  -d '{"model_type": "custom", "config": {"version": "1.0"}}'
```

### 🔍 RAG Query
```bash
curl -X POST "http://127.0.0.1:8080/rag/query" \
  -H "Content-Type: application/json" \
  -H "x-api-key: supersecret123" \
  -d '{"query": "What is VertexOps?", "top_k": 3}'
```

### 📊 Check Metrics
```bash
curl http://127.0.0.1:8080/metrics
```

## 🐳 Docker Deployment

### Option 1: Docker Compose (Recommended)
```bash
# Quick start with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 2: Manual Docker Build
```bash
# Build image
docker build -t vertexops .

# Run container
docker run -d -p 8080:8000 \
  -e API_KEY=supersecret123 \
  --name vertexops-app \
  vertexops

# Check status
docker ps
docker logs vertexops-app
```

## ☁️ Cloud Deployment

### Deploy to Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Deploy to Heroku
```bash
# Install Heroku CLI and login
heroku login

# Create app and deploy
heroku create your-vertexops-app
git push heroku main
```

## 🔧 Extension Points

This MVP provides clear extension points for production use:

### 🧠 Real AI Integration
- **Embeddings**: Replace `text_to_embedding()` with OpenAI/Sentence Transformers
- **LLM**: Update `RAGService` with real OpenAI/Vertex AI calls
- **Models**: Implement actual Vertex AI deployment in `ModelService`

### 💾 Production Storage
- **Vector DB**: Integrate Pinecone, Weaviate, or Chroma
- **Model Metadata**: Use PostgreSQL or Firestore
- **Caching**: Add Redis for performance

### 🔒 Security & Scale
- **JWT Authentication**: Replace simple API key
- **Rate Limiting**: Add request throttling
- **Load Balancing**: Deploy multiple instances

## 📁 Project Structure

```
vertexops/
├── 🚀 main.py              # FastAPI application & routes
├── 📋 schemas.py           # Pydantic models
├── 🔐 auth.py              # Authentication logic
├── 🤖 model_service.py     # Model deployment & fine-tuning
├── 🗂️ vector_store.py      # In-memory vector storage
├── 🔍 rag_service.py       # RAG query processing
├── 📊 monitoring.py        # Prometheus metrics
└── 🛠️ utils.py             # Utility functions
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) for high-performance APIs
- Inspired by modern LLMOps practices
- Ready for integration with Google Vertex AI, OpenAI, and other cloud providers

---

**⭐ If this project helped you, please give it a star!**
