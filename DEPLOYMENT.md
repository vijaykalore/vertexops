# 🚀 Live Deployment Instructions

## Deploy to Railway (Recommended)

1. **Install Railway CLI:**
```bash
npm install -g @railway/cli
# or
curl -fsSL https://railway.app/install.sh | sh
```

2. **Deploy:**
```bash
railway login
railway init
railway up
```

3. **Your live URL will be:** `https://your-project-name.railway.app`

## Deploy to Render

1. **Connect GitHub:**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub
   - Connect your `vertexops` repository

2. **Configure Service:**
   - Service Type: Web Service
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn vertexops.main:app --host 0.0.0.0 --port $PORT`
   - Environment Variables:
     - `API_KEY` = `supersecret123`

## Deploy to Heroku

1. **Install Heroku CLI and login:**
```bash
heroku login
```

2. **Create and deploy:**
```bash
heroku create your-vertexops-app
git push heroku main
```

3. **Set environment variables:**
```bash
heroku config:set API_KEY=supersecret123
```

## For Resume: After Deployment

1. **Update README.md** with your live URL
2. **Test all endpoints** to ensure they work
3. **Take screenshots** of the professional UI
4. **Add to your resume** as a live project

## Example Resume URLs:
- **Live Demo:** https://vertexops-vijay.railway.app
- **API Documentation:** https://vertexops-vijay.railway.app/docs
- **Admin Dashboard:** https://vertexops-vijay.railway.app/dashboard
- **GitHub Repository:** https://github.com/vijaykalore/vertexops
