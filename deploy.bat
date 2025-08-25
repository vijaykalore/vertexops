@echo off
REM VertexOps Quick Deploy Script for Windows
REM Run with: powershell -c "iwr -useb https://raw.githubusercontent.com/vijaykalore/vertexops/main/deploy.bat | iex"

echo 🚀 VertexOps Quick Deploy (Windows)
echo ===================================

REM Check if Docker is available
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo 🐳 Docker found - Using Docker deployment
    
    REM Clone repository
    echo 📥 Cloning repository...
    git clone https://github.com/vijaykalore/vertexops.git
    cd vertexops
    
    REM Build and run with Docker
    echo 🔨 Building Docker image...
    docker build -t vertexops .
    
    echo 🚀 Starting VertexOps...
    docker run -d -p 8000:8000 --name vertexops vertexops
    
    echo ✅ VertexOps deployed successfully!
    echo 🌐 Access at: http://localhost:8000
    echo 📚 API Docs: http://localhost:8000/docs
    echo 📊 Dashboard: http://localhost:8000/dashboard
    goto :end
)

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo 🐍 Python found - Using local deployment
    
    REM Clone repository
    echo 📥 Cloning repository...
    git clone https://github.com/vijaykalore/vertexops.git
    cd vertexops
    
    REM Create virtual environment
    echo 🔧 Setting up virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    
    REM Install dependencies
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
    
    REM Start server
    echo 🚀 Starting VertexOps...
    echo Use Ctrl+C to stop the server
    uvicorn vertexops.main:app --host 127.0.0.1 --port 8000
    goto :end
)

echo ❌ Neither Docker nor Python found
echo Please install Docker or Python 3.11+ and try again
exit /b 1

:end
echo.
echo 🎉 VertexOps is ready to use!
echo 📖 Full documentation: https://github.com/vijaykalore/vertexops
