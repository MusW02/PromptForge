import httpx
import re
from typing import Optional
from .models import PromptRequest, PromptResponse


async def generate_prompt(request: PromptRequest, api_key: str) -> PromptResponse:
    """
    Generate a structured system prompt using the Ollama Cloud API with deepseek-v3:671b model.
    
    Args:
        request: PromptRequest object containing raw_input, target, task_type, style, language
        api_key: Bearer token for Ollama Cloud API
    
    Returns:
        PromptResponse with generated prompt text and token count
    """
    
    # Build system prompt based on target and style
    system_prompt = _build_system_prompt(request.target, request.style)
    
    # Build user message with the raw input
    user_message = _build_user_message(request)
    
    try:
        # Combine system prompt and user message
        combined_prompt = f"{system_prompt}\n\n{user_message}"
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "https://ollama.com/api/generate",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "deepseek-v3.1:671b-cloud",
                    "prompt": combined_prompt,
                    "stream": False,
                },
            )
        
        response.raise_for_status()
        data = response.json()
        
        # Extract the generated prompt from the response
        generated_text = data.get("response", "")
        
        # Extract token usage (estimate based on response length if not provided)
        tokens_used = data.get("tokens", len(generated_text.split()))
        
        # Strip markdown code fences (``` or ```python, etc.)
        cleaned_prompt = _strip_markdown_fences(generated_text)
        
        return PromptResponse(
            prompt=cleaned_prompt,
            tokens_used=tokens_used,
            error="",
        )
    
    except httpx.HTTPStatusError as e:
        error_msg = f"Ollama API error: {e.response.status_code} - {e.response.text}"
        return PromptResponse(
            prompt="",
            tokens_used=0,
            error=error_msg,
        )
    except Exception as e:
        error_msg = f"Prompt generation failed: {str(e)}"
        return PromptResponse(
            prompt="",
            tokens_used=0,
            error=error_msg,
        )


def _strip_markdown_fences(text: str) -> str:
    """
    Remove markdown code fences (``` or ```language) from text.
    
    Args:
        text: Text potentially containing markdown code blocks
    
    Returns:
        Text with code fences removed, preserving the content inside
    """
    # Pattern to match triple backticks with optional language identifier
    pattern = r"```[\w]*\n?|\n?```"
    cleaned = re.sub(pattern, "", text)
    return cleaned.strip()


def _build_system_prompt(target: str, style: str) -> str:
    """
    Build the system prompt for the AI model based on target and style.
    
    Args:
        target: Target AI tool (Cursor, Claude, or Both)
        style: Prompt style (Minimal, Balanced, or Detailed)
    
    Returns:
        System prompt string
    """
    style_constraints = {
        "Minimal": "Produce the SHORTEST possible system prompt (under 200 tokens). Remove all fluff. Be ruthless with brevity.",
        "Balanced": "Produce a well-structured system prompt (300-500 tokens) that balances clarity with conciseness. Include key instructions, constraints, and examples.",
        "Detailed": "Produce a comprehensive system prompt (600-1000+ tokens) with rich context, detailed examples, edge cases, and nuanced instructions.",
    }
    
    target_guidance = {
        "Cursor": "This prompt is optimized for Cursor IDE. Focus on code completion, refactoring, and inline editing behaviors.",
        "Claude": "This prompt is optimized for Claude AI. Focus on conversational clarity, reasoning chains, and structured explanations.",
        "Both (Cursor + Claude)": "This prompt works with both Cursor and Claude. Balance both tool's strengths: Cursor's code focus and Claude's reasoning depth.",
    }
    
    style_text = style_constraints.get(style, style_constraints["Balanced"])
    target_text = target_guidance.get(target, target_guidance["Both (Cursor + Claude)"])
    
    return f"""You are a ruthless system prompt editor. Your job is to transform messy, unstructured thoughts into highly optimized, token-efficient system prompts for AI coding assistants.

{target_text}

{style_text}

OUTPUT REQUIREMENTS:
1. Output ONLY the system prompt itself. No explanations, no markdown, no preamble.
2. Start immediately with the system prompt content.
3. Remove any placeholder brackets [...] or example markers.
4. Ensure the prompt is executable (no ambiguous instructions).
5. Strip all markdown code fences from your output.
6. If markdown exists in the prompt content, preserve it inline without triple backticks.

Be ruthlessly efficient."""


def _build_user_message(request: PromptRequest) -> str:
    """
    Build the user message to send to the Ollama API.
    
    Args:
        request: PromptRequest containing all user inputs
    
    Returns:
        Formatted user message
    """
    message = f"""Transform this into a structured system prompt:

Raw Input:
{request.raw_input}

Metadata:
- Task Type: {request.task_type}
- Style Preference: {request.style}"""
    
    if request.language:
        message += f"\n- Language/Framework: {request.language}"
    
    message += "\n\nOutput only the final system prompt, nothing else."
    
    return message
