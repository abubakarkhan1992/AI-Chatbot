import asyncio
import httpx
from fastapi import HTTPException

from app.config import settings

# Groq — free tier, 30 RPM / 14 400 RPD, OpenAI-compatible API
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"   # fast, free, no quota headaches

MAX_RETRIES = 3
RETRY_BACKOFF = [2, 5, 10]   # seconds between retries (timeout / 5xx)


async def get_llm_reply(prompt: str) -> str:
    """Send prompt to Groq and return the generated text."""
    if not settings.GROQ_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="LLM API key is not configured. Please set GROQ_API_KEY in .env",
        )

    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
        "temperature": 0.7,
    }
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=settings.LLM_TIMEOUT) as client:
        for attempt in range(MAX_RETRIES):
            try:
                response = await client.post(
                    GROQ_API_URL, json=payload, headers=headers
                )
                response.raise_for_status()
                break  # success

            except httpx.TimeoutException:
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(RETRY_BACKOFF[attempt])
                    continue
                raise HTTPException(
                    status_code=500,
                    detail="LLM API request timed out. Please try again.",
                )

            except httpx.HTTPStatusError as exc:
                status = exc.response.status_code

                if status in (401, 403):
                    raise HTTPException(
                        status_code=500,
                        detail="Invalid or unauthorised Groq API key. Check GROQ_API_KEY in .env.",
                    )

                if status == 429:
                    retry_after = exc.response.headers.get("retry-after")
                    wait = float(retry_after) if retry_after else RETRY_BACKOFF[attempt]
                    if attempt < MAX_RETRIES - 1:
                        await asyncio.sleep(wait)
                        continue
                    raise HTTPException(
                        status_code=429,
                        detail="LLM API rate limit reached. Please wait a moment and try again.",
                    )

                if status >= 500:
                    if attempt < MAX_RETRIES - 1:
                        await asyncio.sleep(RETRY_BACKOFF[attempt])
                        continue
                    raise HTTPException(
                        status_code=502,
                        detail=f"LLM API server error ({status}). Please try again later.",
                    )

                raise HTTPException(
                    status_code=500,
                    detail=f"LLM API returned an unexpected error: {status}",
                )

            except httpx.RequestError as exc:
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(RETRY_BACKOFF[attempt])
                    continue
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to reach LLM API: {exc}",
                )

    # Parse OpenAI-compatible response
    try:
        reply = response.json()["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise HTTPException(
            status_code=500,
            detail="Received an unexpected or empty response from the LLM API.",
        )

    if not reply or not reply.strip():
        raise HTTPException(status_code=500, detail="LLM returned an empty response.")

    return reply.strip()