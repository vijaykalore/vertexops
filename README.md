# 🚀 VertexOps - LLMOps Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](Dockerfile)
[![Deploy](https://img.shields.io/badge/Deploy-Ready-success.svg)](DEPLOYMENT_GUIDE.md)

> A complete, production-ready LLMOps platform built with FastAPI. Features model deployment, RAG queries, vector search, professional web UI, and comprehensive monitoring.

## ✨ Key Features

### 🎯 Core LLMOps Capabilities

### 🌐 Professional Web Interface  

### 🔒 Enterprise Security & DevOps

## 🚀 Quick Deploy

### Prerequisites

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

> 📖 **Full deployment guide**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions


## Screenshots

Note: the repository does not include binary screenshot image files. The `screenshots/` directory previously referenced image assets that are not present in this repository. If you want to add screenshots for documentation or GitHub Pages, follow the steps in `SCREENSHOTS.md` to generate and add them, then commit the image files under `screenshots/`.

If you prefer not to include screenshots in the repo, you can host images externally and reference them from the README instead.

## �🔧 Configuration

### 🔐 Authentication
All endpoints require the `x-api-key` header:
```bash
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

### 💾 Production Storage

### 🔒 Security & Scale

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



**⭐ If this project helped you, please give it a star!**
