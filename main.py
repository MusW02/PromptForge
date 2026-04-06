import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Dict, Any

from src.models import PromptRequest, PromptResponse
from src.generator import generate_prompt
from src.history import load_history, save_to_history, clear_history, get_history_stats

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="PromptForge",
    description="Transform messy thoughts into structured system prompts for AI coding assistants",
    version="1.0.0",
)

# Get API key from environment
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

if not OLLAMA_API_KEY:
    print("WARNING: OLLAMA_API_KEY not found in .env file. The /api/generate endpoint will fail.")


@app.post("/api/generate")
async def generate(request: PromptRequest) -> PromptResponse:
    """
    Generate a structured system prompt from raw input.
    
    Args:
        request: PromptRequest with raw_input, target, task_type, style, language
    
    Returns:
        PromptResponse with generated prompt and token count
    """
    if not OLLAMA_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OLLAMA_API_KEY not configured. Please set it in your .env file.",
        )
    
    # Generate the prompt
    response = await generate_prompt(request, OLLAMA_API_KEY)
    
    # If generation was successful, save to history
    if not response.error and response.prompt:
        history_entry = {
            "raw_input": request.raw_input,
            "target": request.target,
            "task_type": request.task_type,
            "style": request.style,
            "language": request.language or "",
            "prompt": response.prompt,
            "tokens_used": response.tokens_used,
        }
        save_to_history(history_entry)
    
    return response


@app.get("/api/history")
def get_history() -> Dict[str, Any]:
    """
    Retrieve the prompt history.
    
    Returns:
        Dictionary with 'items' list and 'stats'
    """
    items = load_history()
    stats = get_history_stats()
    
    return {
        "items": items,
        "stats": stats,
    }


@app.post("/api/history/clear")
def clear_prompt_history() -> Dict[str, str]:
    """
    Clear all history entries.
    
    Returns:
        Confirmation message
    """
    clear_history()
    return {"message": "History cleared successfully"}


# Mount static files folder (serves index.html and other static assets)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def serve_index() -> FileResponse:
    """
    Serve the main index.html file at the root URL.
    """
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        raise HTTPException(status_code=404, detail="index.html not found")


@app.get("/health")
def health_check() -> Dict[str, str]:
    """
    Simple health check endpoint.
    """
    return {"status": "ok"}


@app.get("/api/info")
def app_info() -> Dict[str, Any]:
    """
    Get application information.
    """
    return {
        "name": "PromptForge",
        "version": "1.0.0",
        "description": "Transform messy thoughts into structured system prompts",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
