#!/bin/bash
# VertexOps Quick Deploy Script
# Run with: curl -fsSL https://raw.githubusercontent.com/vijaykalore/vertexops/main/deploy.sh | bash

set -e

echo "🚀 VertexOps Quick Deploy"
echo "========================="

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "🐳 Docker found - Using Docker deployment"
    
    # Clone repository
    echo "📥 Cloning repository..."
    git clone https://github.com/vijaykalore/vertexops.git
    cd vertexops
    
    # Build and run with Docker
    echo "🔨 Building Docker image..."
    docker build -t vertexops .
    
    echo "🚀 Starting VertexOps..."
    docker run -d -p 8000:8000 --name vertexops vertexops
    
    echo "✅ VertexOps deployed successfully!"
    echo "🌐 Access at: http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
    echo "📊 Dashboard: http://localhost:8000/dashboard"
    
elif command -v python3 &> /dev/null; then
    echo "🐍 Python found - Using local deployment"
    
    # Clone repository
    echo "📥 Cloning repository..."
    git clone https://github.com/vijaykalore/vertexops.git
    cd vertexops
    
    # Create virtual environment
    echo "🔧 Setting up virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    
    # Install dependencies
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    
    # Start server in background
    echo "🚀 Starting VertexOps..."
    nohup uvicorn vertexops.main:app --host 0.0.0.0 --port 8000 > vertexops.log 2>&1 &
    
    # Wait for server to start
    echo "⏳ Waiting for server to start..."
    sleep 3
    
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ VertexOps deployed successfully!"
        echo "🌐 Access at: http://localhost:8000"
        echo "📚 API Docs: http://localhost:8000/docs"
        echo "📊 Dashboard: http://localhost:8000/dashboard"
        echo "📋 Logs: tail -f vertexops.log"
    else
        echo "❌ Deployment failed - check vertexops.log for details"
        exit 1
    fi
    
else
    echo "❌ Neither Docker nor Python 3 found"
    echo "Please install Docker or Python 3.11+ and try again"
    exit 1
fi

echo ""
echo "🎉 VertexOps is ready to use!"
echo "📖 Full documentation: https://github.com/vijaykalore/vertexops"
