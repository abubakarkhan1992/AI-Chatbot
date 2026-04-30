# 🎨 AI Chatbot Frontend - Streamlit Guide

A production-ready, user-friendly Streamlit frontend for the FastAPI AI Chatbot backend.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- FastAPI backend running (see main README.md)

### Installation & Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure the backend is running:**
   ```bash
   uvicorn app.main:app --reload
   ```
   (in a separate terminal)

3. **Run the Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Open in browser:**
   - Streamlit will automatically open at `http://localhost:8501`
   - Or navigate manually if it doesn't auto-open

---

## 📋 Features

✅ **User-Friendly Interface**
- Clean, modern design with intuitive controls
- Real-time chat conversation display
- Message history management

✅ **Production-Ready**
- Configurable API endpoint
- Connection status indicator
- Rate limiting awareness (12/minute)
- Comprehensive error handling
- Timeout management

✅ **Error Handling**
- Connection errors
- API errors with descriptive messages
- Timeout notifications
- Validation feedback

✅ **Session Management**
- Persistent chat history within session
- Message counter for rate limit tracking
- One-click chat history clearing

---

## ⚙️ Configuration

### Environment Variables

Set these in `.env` or directly in the sidebar:

```env
# Optional - defaults to http://localhost:8000
API_ENDPOINT=http://localhost:8000
```

### Runtime Configuration

Access the sidebar ⚙️ to:
- Change API endpoint URL
- View rate limit status
- Clear chat history
- Check API connection status

---

## 🌐 Deployment

### Streamlit Cloud Deployment

1. **Push to GitHub:**
   ```bash
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Select this repository
   - Configure environment variables in "Advanced settings"
   - Deploy!

3. **Set environment variable:**
   ```
   API_ENDPOINT=https://your-api-backend.com
   ```

### Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Build & Run:**
```bash
docker build -t chatbot-frontend .
docker run -p 8501:8501 -e API_ENDPOINT=http://backend:8000 chatbot-frontend
```

### Traditional VPS Deployment

**Using Gunicorn (recommended for production):**

Install `gunicorn`:
```bash
pip install gunicorn
```

Run with Gunicorn:
```bash
gunicorn --workers 1 --worker-class sync --bind 0.0.0.0:8501 streamlit run streamlit_app.py
```

**Using systemd service:**

Create `/etc/systemd/system/chatbot-frontend.service`:
```ini
[Unit]
Description=AI Chatbot Frontend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/chatbot
Environment="PATH=/opt/chatbot/venv/bin"
Environment="API_ENDPOINT=http://api-backend:8000"
ExecStart=/opt/chatbot/venv/bin/streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable & start:
```bash
sudo systemctl enable chatbot-frontend
sudo systemctl start chatbot-frontend
```

---

## 📊 Frontend Architecture

```
Streamlit Frontend (streamlit_app.py)
├── Session State Management
│   ├── Chat history
│   ├── Message counter
│   └── API endpoint config
├── Sidebar (Configuration)
│   ├── API endpoint settings
│   ├── Rate limit status
│   └── Chat management
├── Main Content Area
│   ├── Connection status indicator
│   ├── Chat history display
│   └── Message input form
└── Styling & UI
    ├── Custom CSS
    ├── Message formatting
    └── Error display
```

---

## 🔌 API Integration

The frontend communicates with the backend via:

**Endpoint:** `POST /chat`
**Request:**
```json
{
  "prompt": "Your question here (max 300 chars)"
}
```

**Response (Success):**
```json
{
  "reply": "AI-generated answer"
}
```

**Response (Error):**
```json
{
  "detail": "Error description"
}
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Frontend won't connect to API** | Check `API_ENDPOINT` in sidebar; ensure backend is running |
| **Messages timeout** | Backend LLM call taking too long; check API key & network |
| **"Too many requests" error** | Wait a moment; rate limit is 12 requests/minute |
| **Blank page** | Clear browser cache; try incognito mode |
| **Slow responses** | Check backend logs; may be LLM API latency |

---

## 📱 Mobile Support

The frontend is fully responsive and works on:
- ✅ Desktop browsers
- ✅ Tablets
- ✅ Mobile phones

---

## 🔐 Security Considerations

1. **API Endpoint:** Use HTTPS for production (`https://...`)
2. **CORS:** Backend allows frontend requests
3. **Rate Limiting:** Enforced at backend (12/min)
4. **Input Validation:** Max 300 characters per prompt
5. **Error Messages:** Sensitive info is not exposed to client

---

## 📈 Performance Tips

- Keep chat history clean (use "Clear Chat History" if needed)
- For deployments, use Streamlit Cloud or Docker
- Monitor backend API logs for performance issues
- Consider CDN for static files if self-hosted

---

## 📞 Support

For issues or improvements:
1. Check the troubleshooting section above
2. Review backend logs: `app/llm_service.py`
3. Check Streamlit logs in terminal
4. Verify `.env` file configuration

---

**Version:** 1.0.0  
**Built with:** Streamlit, FastAPI, Groq LLM  
**License:** MIT
