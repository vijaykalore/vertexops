# 🚀 VertexOps - LLMOps Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](Dockerfile)
[![Deploy](https://img.shields.io/badge/Deploy-Ready-success.svg)](DEPLOYMENT_GUIDE.md)

> A complete, production-ready LLMOps platform built with FastAPI. Features model deployment, RAG queries, vector search, professional web UI, and comprehensive monitoring.

## ✨ Key Features

### 🎯 Core LLMOps Capabilities
- **🤖 Model Deployment**: Async model deployment simulation with status tracking
- **🔍 RAG System**: Intelligent Retrieval-Augmented Generation with context awareness
- **📊 Vector Search**: High-performance cosine similarity search with embedding support
- **⚡ Real-time Processing**: Async request handling with background task support

### 🌐 Professional Web Interface  
- **🎨 Modern UI**: Gradient-based design with responsive layout
- **📚 Interactive Docs**: Auto-generated Swagger/OpenAPI documentation
- **📊 Live Dashboard**: Real-time system monitoring and management
- **🔍 Health Checks**: Comprehensive service status monitoring

### 🔒 Enterprise Security & DevOps
- **🔐 API Authentication**: Multi-key authentication system
- **� Prometheus Metrics**: Production-grade monitoring and alerting
- **🐳 Docker Ready**: Optimized containerization for any cloud platform
- **� CI/CD Pipeline**: Automated testing, security scans, and deployment

## 🚀 Quick Deploy

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
### 🐳 Docker (Recommended)
```bash
# Clone and deploy with Docker
git clone https://github.com/vijaykalore/vertexops.git
cd vertexops
docker-compose up --build
```
Access at: http://localhost:8000

### 🚀 Cloud Platform (One-Click)
Deploy directly to your favorite platform:

[![Deploy on Railway](https://img.shields.io/badge/Deploy-Railway-blueviolet.svg)](https://railway.app)
[![Deploy on Render](https://img.shields.io/badge/Deploy-Render-46E3B7.svg)](https://render.com)

### 💻 Local Development
```bash
# Clone the repository
git clone https://github.com/vijaykalore/vertexops.git
cd vertexops

# Setup virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .\.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn vertexops.main:app --reload --host 127.0.0.1 --port 8083
```

## 🌐 Access Points
- **🏠 Main Interface**: http://localhost:8000 (or 8083 for local dev)
- **📊 Dashboard**: `/dashboard` - Real-time monitoring
- **📚 API Docs**: `/docs` - Interactive Swagger UI  
- **🏥 Health Check**: `/health` - System diagnostics
- **📈 Metrics**: `/metrics` - Prometheus metrics

> 📖 **Full deployment guide**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions

## � Screenshots

### 🏠 Main Interface
![VertexOps Main Interface](screenshots/main-interface.png)
*Professional landing page with modern gradient design and intuitive navigation*

### 📚 Interactive API Documentation  
![API Documentation](screenshots/api-docs.png)
*Comprehensive Swagger UI with all endpoints, authentication, and try-it-out functionality*

### 📊 Real-time Dashboard
![System Dashboard](screenshots/dashboard.png)
*Live monitoring dashboard with service health, metrics, and system status*

### 🏥 Health Check Endpoint
![Health Check](screenshots/health-check.png)
*JSON health status showing all services active and system diagnostics*

### 📈 Prometheus Metrics
![Metrics Endpoint](screenshots/metrics.png)
*Production-grade metrics in Prometheus format for monitoring and alerting*

## �🔧 Configuration

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

### Build and Run
```bash
docker build -t vertexops .
docker run -p 8080:8000 -e API_KEY=supersecret123 vertexops
```

### Docker Compose
```bash
docker-compose up -d
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
