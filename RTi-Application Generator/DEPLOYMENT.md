# 🚀 Deployment Guide: RTI & Complaint Generator

This guide covers deploying the backend to **Render** and the frontend to **Vercel**.

## ⚡ Key Optimizations

This project includes production-ready optimizations:

- **CPU-only PyTorch:** Reduces build size from ~3.5GB to ~150MB by using CPU wheels instead of CUDA
- **Environment variable parsing:** Supports both JSON arrays and comma-separated values for list configs
- **Auto-deployment:** Push to `main` triggers automatic redeploy on both platforms

---

## 📋 Prerequisites

1. GitHub repository with your code
2. Render account (https://render.com)
3. Vercel account (https://vercel.com)
4. (Optional) OpenAI API key for LLM features

---

## 🔧 Backend Deployment (Render)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Add deployment configuration"
git push origin main
```

### Step 2: Create Render Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Configure the service:

| Setting | Value |
|---------|-------|
| **Name** | `rti-complaint-generator-api` |
| **Region** | Oregon (or Singapore for India) |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | Python 3 |
| **Build Command** | `./build.sh` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Plan** | Free (or Starter for production) |

### Step 3: Set Environment Variables

In Render Dashboard → Your Service → **Environment**:

| Key | Value |
|-----|-------|
| `ENVIRONMENT` | `production` |
| `DEBUG` | `false` |
| `LOG_LEVEL` | `INFO` |
| `CORS_ORIGINS` | `["https://your-app.vercel.app","http://localhost:3000"]` |
| `SPACY_MODEL` | `en_core_web_sm` |
| `ENABLE_DISTILBERT` | `false` (use `true` on Starter plan with 1GB RAM) |
| `RATE_LIMIT_ENABLED` | `true` |
| `OPENAI_API_KEY` | `sk-your-key` (Optional) |

**Memory optimization:**
- DistilBERT disabled by default to fit in 512MB free tier
- App uses rule-based engine + spaCy (works great without DistilBERT!)
- To enable DistilBERT: Set `ENABLE_DISTILBERT=true` and upgrade to Starter plan

**Note:** `CORS_ORIGINS` accepts:
- JSON array: `["https://app.vercel.app","http://localhost:3000"]`
- Comma-separated: `https://app.vercel.app,http://localhost:3000`

### Step 4: Deploy

Click **Create Web Service**. Render will:
1. Clone your repository
2. Run `build.sh` (installs dependencies + spaCy model)
3. Start the uvicorn server

**Note:** First deployment takes ~3-5 minutes:
- CPU-only PyTorch: ~150MB download (vs 3.5GB for CUDA version)
- spaCy model: ~13MB
- Total build time: 3-5 minutes on free tier

### Step 5: Get Your Backend URL

After deployment, your API will be available at:
```
https://your-service-name.onrender.com
```

**Live Example:**
```
https://ai-powered-public-complaint-and-rti-bbv6.onrender.com
```

Test it:
```bash
curl https://your-service-name.onrender.com/health
```

---

## 🎨 Frontend Deployment (Vercel)

### Step 1: Install Vercel CLI (Optional)
```bash
npm install -g vercel
```

### Step 2: Deploy via Vercel Dashboard

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **Add New** → **Project**
3. Import your GitHub repository
4. Configure the project:

| Setting | Value |
|---------|-------|
| **Framework Preset** | Create React App |
| **Root Directory** | `frontend` |
| **Build Command** | `npm run build` |
| **Output Directory** | `build` |

### Step 3: Set Environment Variables

In Vercel Dashboard → Your Project → **Settings** → **Environment Variables**:

| Key | Value |
|-----|-------|
| `REACT_APP_API_URL` | `https://your-service-name.onrender.com/api` |
| `REACT_APP_NAME` | `RTI & Complaint Generator` |
| `REACT_APP_VERSION` | `1.0.0` |

**Important:** Replace `your-service-name.onrender.com` with your actual Render backend URL!

**Live Example:**
```
REACT_APP_API_URL=https://ai-powered-public-complaint-and-rti-bbv6.onrender.com/api
```

### Step 4: Deploy

Click **Deploy**. Vercel will:
1. Install dependencies
2. Build the React app
3. Deploy to their CDN

### Step 5: Get Your Frontend URL

After deployment, your app will be available at:
```
https://your-project-name.vercel.app
```

**Live Example:**
```
https://rti-complaint-generator.vercel.app
```

**Note:** Vercel automatically assigns a production URL and creates deployment-specific preview URLs.

---

## 🔗 Connect Frontend to Backend

### Update Backend CORS

After getting your Vercel URL, update the backend's CORS settings in Render:

```
CORS_ORIGINS=["https://your-project-name.vercel.app","http://localhost:3000"]
```

### Verify Connection

1. Open your Vercel app
2. Try the inference feature
3. Check browser console for any CORS errors

---

## 🔄 Automatic Deployments

Both Render and Vercel support automatic deployments:

- **Push to `main` branch** → Both platforms auto-deploy
- **Pull Requests** → Vercel creates preview deployments

---

## 📊 Monitoring

### Render
- **Logs:** Dashboard → Your Service → Logs
- **Metrics:** Dashboard → Your Service → Metrics

### Vercel
- **Analytics:** Dashboard → Your Project → Analytics
- **Logs:** Dashboard → Your Project → Deployments → Functions

---

## 🚨 Troubleshooting

### Backend Issues

**"error parsing value for field CORS_ORIGINS"**
- Use JSON array format: `["https://app.vercel.app","http://localhost:3000"]`
- Or comma-separated: `https://app.vercel.app,http://localhost:3000`
- Don't use mixed quotes or invalid JSON syntax

**"spaCy model not found"**
- Ensure `build.sh` has execute permissions
- Check that `python -m spacy download en_core_web_sm` runs in build

**"CORS error"**
- Update `CORS_ORIGINS` in Render with your Vercel URL
- Include both `https://` and any preview URLs
- Wildcards like `https://*.vercel.app` are supported

**"Memory exceeded"**
- Should not happen with CPU-only PyTorch (~150MB)
- If it does, upgrade to Starter plan (512MB → 1GB RAM)

### Frontend Issues

**"Network Error"**
- Check `REACT_APP_API_URL` is set correctly
- Ensure backend is running and healthy
- Check for HTTPS/HTTP mismatch

**"Build failed"**
- Check Node version (should be 18+)
- Clear cache: Vercel Dashboard → Settings → Build Cache → Clear

---

## 💰 Cost Estimates

### Render (Backend)
| Plan | RAM | Price | Notes |
|------|-----|-------|-------|
| Free | 512MB | $0/mo | **Sufficient** with CPU-only PyTorch, spins down after 15min |
| Starter | 1GB | $7/mo | Always on, faster cold starts |

### Vercel (Frontend)
| Plan | Price | Notes |
|------|-------|-------|
| Hobby | $0/mo | 100GB bandwidth, great for demos |
| Pro | $20/mo | Unlimited bandwidth, analytics |

---

## 🔐 Security Checklist

- [ ] `DEBUG=false` in production
- [ ] `API_KEY_ENABLED=true` if needed
- [ ] `CORS_ORIGINS` only includes your domains
- [ ] `OPENAI_API_KEY` set via dashboard (not in code)
- [ ] HTTPS enforced (both platforms do this automatically)

---

## 🎉 You're Done!

Your AI-Powered RTI & Complaint Generator is now live!

- **Frontend:** `https://your-app.vercel.app`
- **Backend API:** `https://your-api.onrender.com`
- **API Docs:** `https://your-api.onrender.com/docs`
