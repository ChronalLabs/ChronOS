# 🚀 Deployment Guide for RTI Generator

You have two main options to deploy this application: **Docker** (Recommended) or **Manual Cloud Deployment**.

---

## Option 1: Docker (Easiest for You)

Since you already have `docker-compose.yml`, this is the fastest way to run the full stack (Frontend + Backend + Database) on any server (AWS EC2, DigitalOcean Droplet, or your local machine).

### Prerequisites
- Install **Docker Desktop** (or Docker Engine on Linux).

### Steps
1.  **Configure Environment**:
    - Create a `.env` file in the root directory.
    - Add your OpenAI Key:
      ```env
      OPENAI_API_KEY=sk-your-real-key-here
      ```

2.  **Build & Run**:
    Open a terminal in the project root and run:
    ```bash
    docker-compose up --build -d
    ```

3.  **Access App**:
    - Frontend: `http://localhost:5173` (or server IP)
    - Backend: `http://localhost:8081`

---

## Option 2: Free Cloud Hosting (No Credit Card)

If you don't want to manage a server, use these free tiers:

### 1. Backend (Render.com)
1.  Sign up at [Render.com](https://render.com).
2.  Click **New +** -> **Web Service**.
3.  Connect your GitHub repository.
4.  **Settings**:
    - **Root Directory**: `backend`
    - **Build Command**: `mvn clean package -DskipTests`
    - **Start Command**: `java -jar target/*.jar`
    - **Environment Variables**:
        - `OPENAI_API_KEY`: *Your Key*
        - `PORT`: `8080`
5.  Click **Deploy**. Copy the URL (e.g., `https://rti-backend.onrender.com`).

### 2. Frontend (Vercel)
1.  Sign up at [Vercel.com](https://vercel.com).
2.  Click **Add New** -> **Project**.
3.  Import your GitHub repository.
4.  **Settings**:
    - **Root Directory**: `frontend`
    - **Framework Preset**: Vite
    - **Environment Variables**:
        - `VITE_API_BASE_URL`: Paste your Render Backend URL (e.g., `https://rti-backend.onrender.com`)
5.  Click **Deploy**.

---

## ⚠️ Important Configuration Change

Before deploying to Vercel/Render, you **MUST** update your frontend code to use the dynamic API URL instead of `localhost`.

**File**: `frontend/src/services/api.js`
**Change**:
```javascript
// Current
const API_BASE_URL = "http://localhost:8090/api/v1";

// Change to
const API_BASE_URL = import.meta.env.VITE_API_KEY || "http://localhost:8090/api/v1";
```
*Note: I can make this code change for you if you'd like.*
