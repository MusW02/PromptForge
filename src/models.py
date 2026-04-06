from pydantic import BaseModel
from typing import Optional

class PromptRequest(BaseModel):
    raw_input: str
    target: str = "Both (Cursor + Claude)"
    task_type: str = "Auto-detect"
    style: str = "Balanced"
    language: Optional[str] = ""

class PromptResponse(BaseModel):
    prompt: str
    tokens_used: int
    error: str