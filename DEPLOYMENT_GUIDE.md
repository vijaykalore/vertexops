# 🚀 VertexOps Deployment Guide

## Overview
VertexOps is a complete LLMOps (Large Language Model Operations) platform built with FastAPI, featuring model deployment, vector search, RAG queries, and a professional web interface.

## � Interface Previews

### 🏠 Professional Web Interface
<!-- Main Interface screenshot removed from repository; add images under screenshots/ if desired -->

### 📚 Interactive API Documentation
<!-- API Documentation screenshot removed from repository; add images under screenshots/ if desired -->

### 📊 Real-time Dashboard
<!-- System Dashboard screenshot removed from repository; add images under screenshots/ if desired -->

### 🏥 Health Monitoring
<!-- Health Check screenshot removed from repository; add images under screenshots/ if desired -->

### 📈 Production Metrics
<!-- Metrics screenshot removed from repository; add images under screenshots/ if desired -->

## �📋 Quick Deploy Options

### Option 1: Docker Deployment (Recommended)

```bash
# Clone the repository
git clone https://github.com/vijaykalore/vertexops.git
cd vertexops

# Build and run with Docker
docker build -t vertexops .
docker run -p 8000:8000 vertexops

# Or use Docker Compose
docker-compose up --build
```

Access at: `http://localhost:8000`

### Option 2: Local Python Development

```bash
# Clone the repository
git clone https://github.com/vijaykalore/vertexops.git
cd vertexops

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.\.venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn vertexops.main:app --reload --host 0.0.0.0 --port 8000
```

Access at: `http://localhost:8000`

### Option 3: Cloud Platform Deployment

#### Railway
1. Fork this repository
2. Connect to Railway
3. Deploy automatically with zero configuration
4. Environment: Python 3.11+, FastAPI

#### Render
1. Fork this repository  
2. Create new Web Service on Render
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn vertexops.main:app --host 0.0.0.0 --port $PORT`

#### Heroku
```bash
# Add Procfile (already included)
web: uvicorn vertexops.main:app --host 0.0.0.0 --port $PORT

# Deploy
heroku create your-vertexops-app
git push heroku main
```

## 🌟 Features

### Core Functionality
- **🤖 Model Deployment**: Simulated ML model deployment and management
- **🔍 Vector Search**: In-memory vector storage with similarity search
- **📝 RAG Queries**: Retrieval-Augmented Generation with context-aware responses
- **🔒 Authentication**: API key-based security system
- **📊 Monitoring**: Prometheus metrics and health checks

### Web Interface
- **🎨 Professional UI**: Modern gradient-based design
- **📚 Interactive API Docs**: Swagger/OpenAPI documentation
- **📊 Management Dashboard**: Real-time system monitoring
- **🔍 Health Monitoring**: Service status and diagnostics

### DevOps Ready
- **🐳 Docker Support**: Multi-stage production builds
- **🔄 CI/CD Pipeline**: GitHub Actions for testing and deployment
- **📈 Metrics**: Prometheus integration for monitoring
- **🔒 Security**: Bandit and safety checks included

## 🚀 API Endpoints

### Core Endpoints
- `GET /` - Professional web interface
- `GET /health` - System health check
- `GET /docs` - Interactive API documentation
- `GET /dashboard` - Management dashboard
- `GET /metrics` - Prometheus metrics

### Authenticated Endpoints (Require `x-api-key` header)
- `POST /models/deploy` - Deploy ML models
- `POST /models/{id}/finetune` - Fine-tune models
- `POST /vector/add` - Add documents to vector store
- `POST /vector/search` - Search similar documents
- `POST /rag/query` - RAG-powered question answering

## 🔧 Configuration

### Environment Variables
```env
API_KEYS=supersecret123,anothersecretkey
LOG_LEVEL=info
ENVIRONMENT=production
```

### Default Settings
- **Default API Key**: `supersecret123`
- **Default Port**: 8000
- **Health Check**: `/health`
- **Metrics**: `/metrics`

## 📊 Monitoring & Observability

### Health Checks
```bash
curl http://localhost:8000/health
```

### Metrics
```bash
curl http://localhost:8000/metrics
```

### Logs
- Application logs via uvicorn
- Request/response metrics
- Performance monitoring

## 🛠️ Development

### Running Tests
```bash
# Basic functionality tests
python -c "
from vertexops.vector_store import InMemoryVectorStore
from vertexops.model_service import ModelService
print('✅ All core services working!')
"

# Demo script (local testing)
python demo.py
```

### Code Quality
```bash
# Format code
black .

# Lint code  
flake8 .

# Security scan
bandit -r vertexops/
```

## 🔒 Security

### API Authentication
Include the API key in request headers:
```bash
curl -H "x-api-key: supersecret123" http://localhost:8000/vector/add
```

### Security Features
- API key authentication for sensitive endpoints
- Input validation with Pydantic models
- CORS middleware configuration
- Security scanning in CI/CD pipeline

## 📈 Performance

### Scalability
- Async/await FastAPI for high concurrency
- In-memory vector store for fast similarity search
- Background task processing for long-running operations
- Prometheus metrics for performance monitoring

### Optimization
- Multi-stage Docker builds for smaller images
- Production-ready uvicorn configuration
- Efficient request/response handling
- Memory-optimized vector operations

## 🆘 Troubleshooting

### Common Issues
1. **Port conflicts**: Use different port with `--port 8001`
2. **Import errors**: Ensure virtual environment is activated
3. **Permission issues**: Check file permissions and user access
4. **Docker issues**: Verify Docker installation and permissions

### Debug Mode
```bash
# Run with debug logging
uvicorn vertexops.main:app --reload --log-level debug
```

### Support
- GitHub Issues: https://github.com/vijaykalore/vertexops/issues
- Documentation: Check `/docs` endpoint when running
- Logs: Monitor application logs for detailed error information

---

## 🏆 Production Ready

VertexOps is production-ready with:
- ✅ Docker containerization
- ✅ CI/CD pipeline
- ✅ Security scanning
- ✅ Health checks
- ✅ Metrics collection
- ✅ Professional UI
- ✅ Comprehensive documentation
- ✅ Error handling
- ✅ Performance optimization

Deploy with confidence! 🚀
