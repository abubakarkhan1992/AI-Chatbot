#!/bin/bash

# =========================================================================
# AI Chatbot - Unix/Linux/Mac Startup Script
# This script starts both the backend and frontend servers
# =========================================================================

set -e

echo ""
echo "========================================"
echo "  AI Chatbot - Startup Script"
echo "========================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    echo "Please copy .env.example to .env and configure it with your GROQ_API_KEY"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Please install Python 3.9+"
    exit 1
fi

echo "Checking dependencies..."
if ! python3 -c "import uvicorn" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

echo ""
echo "Starting services..."
echo ""

# Create virtual terminal sessions or use tmux if available
if command -v tmux &> /dev/null; then
    echo "Using tmux for session management..."
    
    # Create new session
    tmux new-session -d -s chatbot
    
    # Backend window
    tmux new-window -t chatbot -n backend -c "$(pwd)"
    tmux send-keys -t chatbot:backend "python -m uvicorn app.main:app --reload --port 8000" Enter
    
    # Frontend window
    tmux new-window -t chatbot -n frontend -c "$(pwd)"
    tmux send-keys -t chatbot:frontend "streamlit run streamlit_app.py" Enter
    
    echo "========================================"
    echo "   Services Started with tmux!"
    echo "========================================"
    echo ""
    echo "Backend:  http://localhost:8000"
    echo "Frontend: http://localhost:8501"
    echo ""
    echo "Tmux commands:"
    echo "  tmux attach -t chatbot       # Attach to session"
    echo "  tmux list-windows -t chatbot # List windows"
    echo "  tmux kill-session -t chatbot # Kill session"
    echo ""
    
else
    echo "Starting Backend (FastAPI on port 8000)..."
    python -m uvicorn app.main:app --reload --port 8000 &
    BACKEND_PID=$!
    
    echo "Waiting for backend to start..."
    sleep 3
    
    echo "Starting Frontend (Streamlit on port 8501)..."
    streamlit run streamlit_app.py &
    FRONTEND_PID=$!
    
    echo ""
    echo "========================================"
    echo "   Services Started!"
    echo "========================================"
    echo ""
    echo "Backend:  http://localhost:8000 (PID: $BACKEND_PID)"
    echo "Frontend: http://localhost:8501 (PID: $FRONTEND_PID)"
    echo ""
    echo "Press Ctrl+C to stop the services."
    echo ""
    
    # Keep script running and handle cleanup
    trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Services stopped.'; exit 0" SIGINT
    
    wait
fi
