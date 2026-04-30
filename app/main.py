from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.routes import router

app = FastAPI(
    title="AI Chatbot Backend",
    description="A FastAPI backend that forwards user prompts to an LLM and returns AI-generated replies.",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# Custom validation error handler – returns 422 with a clean message
# ---------------------------------------------------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    # Detect empty-prompt specifically and promote to 400
    for error in errors:
        if "prompt" in error.get("loc", ()) and "empty" in error.get("msg", "").lower():
            return JSONResponse(
                status_code=400,
                content={"detail": "prompt must not be empty"},
            )
    return JSONResponse(
        status_code=422,
        content={"detail": errors},
    )


app.include_router(router)


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "AI Chatbot Backend is running"}
