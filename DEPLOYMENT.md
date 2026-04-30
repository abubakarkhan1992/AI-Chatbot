# 🚀 Deployment Guide - AI Chatbot

Complete step-by-step deployment guides for various platforms and environments.

---

## 📋 Quick Reference

| Platform | Difficulty | Cost | Setup Time |
|---|---|---|---|
| **Local Development** | ⭐ Easy | Free | 5 min |
| **Docker Compose** | ⭐⭐ Easy | Free | 10 min |
| **Streamlit Cloud** | ⭐⭐ Easy | Free | 15 min |
| **Heroku/Railway** | ⭐⭐ Easy | $5-10/mo | 20 min |
| **AWS/DigitalOcean** | ⭐⭐⭐ Medium | $5-20/mo | 45 min |
| **Kubernetes** | ⭐⭐⭐⭐ Hard | $10-50/mo | 1-2 hours |

---

## 🏠 1. Local Development

### Prerequisites
- Python 3.9+
- Git
- Groq API key (free from https://console.groq.com)

### Setup (5 minutes)

```bash
# 1. Clone/extract project
cd Task6

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure .env
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### Run Both Services

**Option A: Using Scripts**
```bash
./run.sh        # Linux/Mac
run.bat         # Windows
```

**Option B: Manual (Two Terminals)**

Terminal 1 - Backend:
```bash
uvicorn app.main:app --reload --port 8000
```

Terminal 2 - Frontend:
```bash
streamlit run streamlit_app.py
```

### Access
- Frontend: http://localhost:8501
- Backend: http://localhost:8000
- Docs: http://localhost:8000/docs

---

## 🐳 2. Docker Compose (Recommended for Teams)

### Prerequisites
- Docker & Docker Compose installed
- Groq API key

### Setup (10 minutes)

```bash
# 1. Clone/extract project
cd Task6

# 2. Configure environment
cp .env.example .env
# Edit .env and add GROQ_API_KEY

# 3. Start services
docker-compose up

# To run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Troubleshooting

**Ports already in use?**
```bash
# Change ports in docker-compose.yml
# Or kill existing services
docker ps
docker kill <container_id>
```

**Container won't start?**
```bash
docker-compose logs frontend  # Check frontend logs
docker-compose logs backend   # Check backend logs
```

---

## ☁️ 3. Streamlit Cloud (Easiest for Frontend)

Best for: Rapid prototyping, hobby projects

### Prerequisites
- GitHub account
- Groq API key

### Step-by-Step (15 minutes)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/username/chatbot.git
   git push origin main
   ```

2. **Deploy Frontend:**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Select your repo & `streamlit_app.py`
   - Click "Deploy"

3. **Set Environment Variable:**
   - In Streamlit Cloud settings → Secrets
   - Add: `API_ENDPOINT=https://your-backend-url.com`

4. **Deploy Backend Separately:**
   - See Railway/Render/Heroku sections below
   - Get the backend URL
   - Update Streamlit Cloud secrets

---

## 🚂 4. Railway (Recommended for Beginners)

Best for: Simple deployments with free tier

### Pricing
- Free tier: 500 hours/month (covers 1 small app 24/7)
- After free tier: $5/month

### Step-by-Step (20 minutes)

1. **Create Railway Account:**
   - Go to https://railway.app
   - Sign up with GitHub
   - Authorize Railway

2. **Deploy Backend:**
   ```bash
   npm install -g @railway/cli
   railway login
   railway init  # In project root
   ```
   
   When prompted:
   - Project name: `chatbot-backend`
   - Select Python environment
   
   In Railway dashboard:
   - Add environment variable: `GROQ_API_KEY=your_key`
   - Note the deployed URL

3. **Deploy Frontend:**
   - In Railway dashboard, create new service
   - Select "GitHub" → your chatbot repo
   - Set `streamlit_app.py` as start file
   - Add environment: `API_ENDPOINT=https://your-backend-url.railway.app`
   - Deploy

### Access
- Frontend: `https://your-project.railway.app`

---

## 🎯 5. Render (Good Alternative)

### Pricing
- Free tier: 750 hours/month
- Paid: $7/month

### Deploy Backend

1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Configuration:
   - Runtime: Python 3.11
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - Add environment: `GROQ_API_KEY`
5. Deploy

### Deploy Frontend

1. New → Web Service
2. Same repo
3. Configuration:
   - Start command: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
   - Add environment: `API_ENDPOINT=https://your-backend.onrender.com`
4. Deploy

---

## 🌐 6. AWS (Production Recommended)

### Architecture
- **Frontend:** CloudFront + S3 or EC2
- **Backend:** EC2 or App Runner
- **Database:** Optional (for future features)

### Using EC2 (Simplest)

**1. Launch EC2 Instance**
- AMI: Ubuntu 22.04 LTS
- Instance: t3.micro (free tier eligible)
- Security: Allow ports 80, 443, 8000, 8501

**2. SSH into instance:**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

**3. Install dependencies:**
```bash
sudo apt update && sudo apt install -y python3.11 python3-pip docker.io

# Add user to docker group
sudo usermod -aG docker ubuntu
```

**4. Clone and setup:**
```bash
git clone https://github.com/username/chatbot.git
cd chatbot
cp .env.example .env
# Edit .env with your API key
```

**5. Start with Docker Compose:**
```bash
docker-compose up -d
```

**6. Setup Reverse Proxy (Nginx):**
```bash
sudo apt install nginx

# Create /etc/nginx/sites-available/chatbot
sudo tee /etc/nginx/sites-available/chatbot << EOF
upstream backend {
    server localhost:8000;
}

upstream frontend {
    server localhost:8501;
}

server {
    listen 80;
    server_name your-domain.com;

    location /api/ {
        proxy_pass http://backend/;
    }

    location / {
        proxy_pass http://frontend/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/chatbot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl start nginx
```

**7. Setup HTTPS (Let's Encrypt):**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## ☸️ 7. Kubernetes (Enterprise)

For high-availability, auto-scaling deployments.

### Prerequisites
- kubectl installed
- Access to K8s cluster (Docker Desktop, EKS, GKE, etc.)

### Create Kubernetes Manifests

**k8s/namespace.yaml:**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: chatbot
```

**k8s/backend-deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: chatbot
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: chatbot-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: GROQ_API_KEY
          valueFrom:
            secretKeyRef:
              name: groq-secret
              key: api-key
```

**k8s/frontend-deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: chatbot
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: chatbot-frontend:latest
        ports:
        - containerPort: 8501
        env:
        - name: API_ENDPOINT
          value: "http://backend:8000"
```

**k8s/service.yaml:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: chatbot
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8501
  selector:
    app: frontend
```

### Deploy

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create secret
kubectl create secret generic groq-secret \
  --from-literal=api-key=YOUR_GROQ_API_KEY \
  -n chatbot

# Deploy
kubectl apply -f k8s/

# Check status
kubectl get pods -n chatbot
kubectl get svc -n chatbot

# Get external IP
kubectl get svc frontend-service -n chatbot
```

---

## 🔒 SSL/HTTPS Setup

### Using Let's Encrypt (Free)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --standalone -d your-domain.com

# Certificate location
/etc/letsencrypt/live/your-domain.com/fullchain.pem
/etc/letsencrypt/live/your-domain.com/privkey.pem

# Auto-renew (runs automatically)
sudo systemctl start certbot.timer
```

### Using Cloudflare (Easy)
1. Add domain to Cloudflare
2. Enable "Flexible SSL" or "Full SSL"
3. Point DNS to your server IP
4. Auto-renewed by Cloudflare

---

## 📊 Monitoring & Logging

### Backend Logs
```bash
# Docker
docker-compose logs -f backend

# Kubernetes
kubectl logs -f deployment/backend -n chatbot
```

### Frontend Logs
```bash
# Docker
docker-compose logs -f frontend

# Streamlit
tail -f .streamlit/streamlit.log
```

### Monitoring Tools
- **Free:** DataDog (500M events/month), New Relic
- **Paid:** CloudWatch (AWS), Stackdriver (GCP)

---

## 🆘 Common Issues & Solutions

| Issue | Solution |
|---|---|
| **Port already in use** | `lsof -i :8000` or change port in config |
| **API key error** | Verify GROQ_API_KEY in .env, check Groq console |
| **CORS errors** | Backend already allows all origins |
| **Timeout errors** | Increase LLM_TIMEOUT, check network |
| **Memory issues** | Reduce Streamlit cache, use smaller model |
| **Container won't start** | Check logs, verify image exists |

---

## 📈 Scaling Considerations

### For 100+ concurrent users
- Use load balancer (NGINX, HAProxy)
- Multiple backend instances
- Caching layer (Redis)
- CDN for frontend assets

### For 1000+ concurrent users
- Kubernetes auto-scaling
- Database connection pooling
- Message queue (Redis, RabbitMQ)
- Distributed tracing

### For 10000+ concurrent users
- Multi-region deployment
- Advanced caching
- Rate limiting per user
- Consider alternative LLM APIs

---

## 💰 Cost Estimation (Monthly)

| Service | Cost |
|---|---|
| **Streamlit Cloud (Frontend)** | Free - $15 |
| **Railway (Backend)** | Free - $15 |
| **AWS EC2 t3.micro** | Free - $10 |
| **Groq API** | Free (30 RPM) |
| **Domain** | $10-15 |
| **SSL Certificate** | Free (Let's Encrypt) |
| **CDN (optional)** | $0-20 |
| **Total** | Free - $75 |

---

## 🎓 Next Steps

1. **Choose a platform** based on your needs
2. **Deploy** following the guide above
3. **Test thoroughly** before going live
4. **Monitor** for issues
5. **Scale** as needed

For questions, check [FRONTEND.md](FRONTEND.md) or [README.md](README.md).

---

**Version:** 1.0.0 | Last Updated: April 2026
