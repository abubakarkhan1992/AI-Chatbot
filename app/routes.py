from fastapi import APIRouter, HTTPException

from app.schemas import ChatRequest, ChatResponse
from app.llm_service import get_llm_reply

router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Send a prompt to the AI chatbot",
    responses={
        200: {"description": "Successful AI response"},
        400: {"description": "Empty or invalid prompt"},
        422: {"description": "Validation error (e.g. prompt too long)"},
        429: {"description": "Gemini API rate limit reached — slow down and retry"},
        500: {"description": "LLM API failure"},
        502: {"description": "Gemini API server-side error"},
    },
)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Receive a user prompt, forward it to the LLM, and return the AI-generated reply.

    - **prompt**: The user's message (required, max 300 characters)
    """
    # Extra guard for empty prompt after stripping (Pydantic already handles this,
    # but we return a 400 instead of 422 per the spec)
    if not request.prompt:
        raise HTTPException(status_code=400, detail="prompt must not be empty")

    reply = await get_llm_reply(request.prompt)
    return ChatResponse(reply=reply)