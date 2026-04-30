from pydantic import BaseModel, field_validator


class ChatRequest(BaseModel):
    prompt: str

    @field_validator("prompt")
    @classmethod
    def prompt_must_not_be_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("prompt must not be empty")
        if len(v) > 300:
            raise ValueError("prompt must not exceed 300 characters")
        return v


class ChatResponse(BaseModel):
    reply: str
