# VertexOps Screenshot Guide

This guide helps you take professional screenshots of all VertexOps interfaces for documentation.

## 🚀 Prerequisites

1. **Start the server**:
   ```bash
   # Make sure you're in the project directory
   .\.venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   
   uvicorn vertexops.main:app --reload --host 127.0.0.1 --port 8083
   ```

2. **Verify server is running**:
   - Check terminal shows: `INFO: Uvicorn running on http://127.0.0.1:8083`

## 📸 Screenshot Checklist

This file documents how to create optional screenshots for the project. Screenshots are not required for CI.

If you want to include screenshots in the repository, follow these steps and add the PNG files under `screenshots/`.

### 1. 🏠 Main Interface
- **URL**: http://127.0.0.1:8083
- **Filename**: `main-interface.png`
- **What to capture**:
  - Full browser window showing the landing page
  - Modern gradient background
  - VertexOps branding and welcome message
  - Feature highlights and navigation elements
  - Professional design elements

### 2. 📚 API Documentation
- **URL**: http://127.0.0.1:8083/docs
- **Filename**: `api-docs.png`
- **What to capture**:
  - Swagger UI interface
  - List of all API endpoints (models, vector, rag, etc.)
  - Authentication section at the top
  - Clean, professional API documentation
  - Interactive "Try it out" buttons visible

### 3. 📊 Dashboard
- **URL**: http://127.0.0.1:8083/dashboard
- **Filename**: `dashboard.png`
- **What to capture**:
  - Real-time dashboard interface
  - System status cards showing "active" services
  - Performance metrics and statistics
  - Interactive elements and buttons
  - Modern card-based layout

### 4. 🏥 Health Check
- **URL**: http://127.0.0.1:8083/health
- **Filename**: `health-check.png`
- **What to capture**:
  - JSON response in browser
  - Health status showing "healthy"
  - All services showing "active" status
  - Timestamp information
  - Clean JSON formatting

### 5. 📈 Metrics
- **URL**: http://127.0.0.1:8083/metrics
- **Filename**: `metrics.png`
- **What to capture**:
  - Prometheus metrics format
  - HTTP request counters and histograms
  - Various metric types
  - Professional monitoring data
  - Plain text metrics output

## 📏 Screenshot Guidelines

### **Technical Requirements**:
- **Resolution**: 1920x1080 or higher
- **Format**: PNG (for quality)
- **Browser**: Use Chrome or Edge for consistency
- **Zoom**: 100% browser zoom level

### **Composition Tips**:
- Capture full browser window (include address bar)
- Ensure good lighting/contrast
- No personal bookmarks or browser extensions visible
- Clean, professional appearance
- Center the content in the browser window

### **Quality Checklist**:
- [ ] High resolution and crisp text
- [ ] No browser notifications or popups
- [ ] Professional color scheme visible
- [ ] All UI elements clearly readable
- [ ] No sensitive information visible
- [ ] Consistent browser theme

## 📁 File Organization

Save screenshots in the `screenshots/` directory with these exact filenames:
```
screenshots/
├── main-interface.png
├── api-docs.png  
├── dashboard.png
├── health-check.png
└── metrics.png
```

## 🎯 Final Steps

After taking all screenshots:

1. **Verify all files are saved correctly**
2. **Check image quality and readability**
3. **Commit to git**:
   ```bash
   git add screenshots/
   git commit -m "Add professional screenshots of VertexOps interfaces"
   git push origin main
   ```

This will update the documentation with visual examples of your professional LLMOps platform! 🎉
