"""
AI Chatbot Frontend - Built with Streamlit
A user-friendly, production-ready interface for the FastAPI chatbot backend.
"""

import os
import requests
import streamlit as st
from datetime import datetime
from typing import Optional

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ============================================================================
# CUSTOM STYLING
# ============================================================================
st.markdown("""
    <style>
        /* Main container */
        .main {
            padding: 2rem;
        }
        
        /* Chat message styling */
        .user-message {
            background-color: #e3f2fd;
            padding: 12px 16px;
            border-radius: 12px;
            margin-bottom: 12px;
            border-left: 4px solid #1976d2;
        }
        
        .assistant-message {
            background-color: #f5f5f5;
            padding: 12px 16px;
            border-radius: 12px;
            margin-bottom: 12px;
            border-left: 4px solid #388e3c;
        }
        
        .error-message {
            background-color: #ffebee;
            padding: 12px 16px;
            border-radius: 12px;
            margin-bottom: 12px;
            border-left: 4px solid #d32f2f;
            color: #b71c1c;
        }
        
        /* Header styling */
        .header {
            text-align: center;
            padding: 20px 0;
            border-bottom: 2px solid #e0e0e0;
            margin-bottom: 30px;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 20px 0;
            border-top: 1px solid #e0e0e0;
            margin-top: 30px;
            color: #999;
            font-size: 0.85rem;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "api_endpoint" not in st.session_state:
    st.session_state.api_endpoint = os.getenv("API_ENDPOINT", "https://vercel-fastapi-for-ai-chatbot.vercel.app/")

if "message_count" not in st.session_state:
    st.session_state.message_count = 0

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if "waiting_for_response" not in st.session_state:
    st.session_state.waiting_for_response = False

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    # API Endpoint
    api_endpoint = st.text_input(
        "API Endpoint",
        value=st.session_state.api_endpoint,
        help="The URL of the FastAPI backend (e.g., http://localhost:8000)"
    )
    st.session_state.api_endpoint = api_endpoint
    
    # Rate limiting info
    st.markdown("---")
    st.markdown("### 📊 Rate Limiting")
    st.info("📌 **Limit:** 12 requests per minute")
    
    requests_remaining = 12 - (st.session_state.message_count % 12)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Requests This Minute", requests_remaining)
    
    # Clear chat history
    st.markdown("---")
    st.markdown("### 🗑️ Chat Management")
    if st.button("Clear Chat History", use_container_width=True, type="secondary"):
        st.session_state.chat_history = []
        st.session_state.message_count = 0
        st.rerun()
    
    # About
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
        **AI Chatbot Frontend v1.0**
        
        This is a user-friendly interface for the FastAPI chatbot backend.
        
        - Powered by **Groq LLM API**
        - Built with **Streamlit**
        - Designed for production use
        
        [GitHub Repository](https://github.com)
    """)

# ============================================================================
# MAIN HEADER
# ============================================================================
st.markdown("""
    <div class="header">
        <h1>🤖 AI Chatbot</h1>
        <p>Ask me anything! I'm powered by Groq's LLM.</p>
    </div>
""", unsafe_allow_html=True)

# ============================================================================
# CONNECTION STATUS
# ============================================================================
@st.cache_data(ttl=30)
def check_api_health(endpoint: str) -> bool:
    """Check if the API is reachable."""
    try:
        response = requests.get(f"{endpoint}/", timeout=2)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Display connection status
health_col1, health_col2, health_col3 = st.columns(3)
is_healthy = check_api_health(st.session_state.api_endpoint)

with health_col1:
    status_emoji = "🟢" if is_healthy else "🔴"
    status_text = "Connected" if is_healthy else "Disconnected"
    st.metric("API Status", status_text, delta=status_emoji)

# ============================================================================
# CHAT HISTORY DISPLAY
# ============================================================================
chat_container = st.container()
with chat_container:
    st.markdown("### 💬 Conversation")
    
    if not st.session_state.chat_history:
        st.info("👋 Start a conversation! Send a message below.")
    else:
        for idx, message in enumerate(st.session_state.chat_history):
            if message["role"] == "user":
                st.markdown(
                    f"""<div class="user-message"><strong>You:</strong><br>{message['content']}</div>""",
                    unsafe_allow_html=True
                )
            elif message["role"] == "assistant":
                st.markdown(
                    f"""<div class="assistant-message"><strong>🤖 Assistant:</strong><br>{message['content']}</div>""",
                    unsafe_allow_html=True
                )
            elif message["role"] == "error":
                st.markdown(
                    f"""<div class="error-message"><strong>⚠️ Error:</strong><br>{message['content']}</div>""",
                    unsafe_allow_html=True
                )

# ============================================================================
# INPUT FORM
# ============================================================================
st.markdown("---")
st.markdown("### ✉️ Send a Message")

col_input, col_button = st.columns([5, 1])

with col_input:
    user_input = st.text_area(
        "Your message",
        placeholder="Type your question here... (max 300 characters)",
        height=100,
        max_chars=300,
        label_visibility="collapsed",
        key="message_input",
        value=st.session_state.user_input,
        on_change=lambda: None  # Ensure state updates
    )

with col_button:
    st.write("")  # Spacing
    st.write("")  # Spacing
    send_clicked = st.button(
        "📤 Send",
        use_container_width=True,
        type="primary",
        key="send_button"
    )

# Handle send button click
if send_clicked and user_input.strip():
    st.session_state.user_input = user_input.strip()
    st.session_state.waiting_for_response = True
    
    # Add user message to history
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input.strip()
    })
    st.session_state.message_count += 1
    
    # Send to API
    with st.spinner("🤔 Thinking..."):
        try:
            response = requests.post(
                f"{st.session_state.api_endpoint}/chat",
                json={"prompt": user_input.strip()},
                timeout=35  # LLM timeout is 30s + buffer
            )
            
            if response.status_code == 200:
                ai_reply = response.json().get("reply", "No response received")
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": ai_reply
                })
            else:
                error_detail = response.json().get(
                    "detail",
                    f"HTTP {response.status_code}"
                )
                st.session_state.chat_history.append({
                    "role": "error",
                    "content": f"API Error: {error_detail}"
                })
                st.error(f"❌ {error_detail}", icon="⚠️")
        
        except requests.Timeout:
            error_msg = "Request timed out. Please try again."
            st.session_state.chat_history.append({
                "role": "error",
                "content": error_msg
            })
            st.error(f"❌ {error_msg}", icon="⏱️")
        
        except requests.ConnectionError:
            error_msg = f"Could not connect to API at {st.session_state.api_endpoint}. Is it running?"
            st.session_state.chat_history.append({
                "role": "error",
                "content": error_msg
            })
            st.error(f"❌ {error_msg}", icon="🔌")
        
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            st.session_state.chat_history.append({
                "role": "error",
                "content": error_msg
            })
            st.error(f"❌ {error_msg}", icon="💥")
    
    # Clear input and waiting state
    st.session_state.user_input = ""
    st.session_state.waiting_for_response = False
    st.rerun()

elif send_clicked and not user_input.strip():
    st.warning("⚠️ Please enter a message before sending.")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("""
    <div class="footer">
        <p>Built with ❤️ using Streamlit | Powered by Groq LLM</p>
        <p>Deployed on <code>""" + st.session_state.api_endpoint + """</code></p>
    </div>
""", unsafe_allow_html=True)
