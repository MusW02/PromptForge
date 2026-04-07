"""
Tests for PromptForge generator and history logic.
Run with: pytest tests/ -v

Install test dependencies: pip install pytest pytest-asyncio
"""

import pytest
import json
import os
from unittest.mock import patch, AsyncMock, MagicMock
from src.models import PromptRequest, PromptResponse
from src.generator import _strip_markdown_fences, _build_system_prompt, _build_user_message
from src.history import save_to_history, load_history, clear_history, HISTORY_MAX_ITEMS


class TestMarkdownFenceStripping:
    """Test markdown code fence removal"""
    
    def test_strips_triple_backticks(self):
        text = "```\nHello world\n```"
        result = _strip_markdown_fences(text)
        assert result == "Hello world"
    
    def test_strips_language_specified_backticks(self):
        text = "```python\nprint('hello')\n```"
        result = _strip_markdown_fences(text)
        assert result == "print('hello')"
    
    def test_strips_multiple_blocks(self):
        text = "```\nFirst\n```\nMiddle\n```\nLast\n```"
        result = _strip_markdown_fences(text)
        assert "```" not in result
        assert "Middle" in result
    
    def test_preserves_content_without_fences(self):
        text = "Just plain text without fences"
        result = _strip_markdown_fences(text)
        assert result == text
    
    def test_handles_empty_string(self):
        result = _strip_markdown_fences("")
        assert result == ""


class TestSystemPromptBuilder:
    """Test system prompt generation based on target and style"""
    
    def test_minimal_style_is_brief(self):
        prompt = _build_system_prompt("Cursor", "Minimal")
        assert "ruthless" in prompt.lower()
        assert "200 tokens" in prompt.lower()
    
    def test_balanced_style_moderate_length(self):
        prompt = _build_system_prompt("Claude", "Balanced")
        assert "ruthless" in prompt.lower()
        assert "300-500 tokens" in prompt.lower()
    
    def test_detailed_style_comprehensive(self):
        prompt = _build_system_prompt("Both (Cursor + Claude)", "Detailed")
        assert "ruthless" in prompt.lower()
        assert "600-1000" in prompt.lower()
    
    def test_cursor_target_mentioned(self):
        prompt = _build_system_prompt("Cursor", "Minimal")
        assert "cursor" in prompt.lower()
    
    def test_claude_target_mentioned(self):
        prompt = _build_system_prompt("Claude", "Balanced")
        assert "claude" in prompt.lower()
    
    def test_both_targets_balanced(self):
        prompt = _build_system_prompt("Both (Cursor + Claude)", "Detailed")
        assert "both" in prompt.lower() or "cursor" in prompt.lower() and "claude" in prompt.lower()


class TestUserMessageBuilder:
    """Test user message formatting"""
    
    def test_includes_raw_input(self):
        request = PromptRequest(
            raw_input="Test input",
            target="Cursor",
            task_type="Code Generation",
            style="Balanced"
        )
        msg = _build_user_message(request)
        assert "Test input" in msg
    
    def test_includes_task_type(self):
        request = PromptRequest(
            raw_input="test",
            target="Claude",
            task_type="Debugging",
            style="Minimal"
        )
        msg = _build_user_message(request)
        assert "Debugging" in msg
    
    def test_includes_style(self):
        request = PromptRequest(
            raw_input="test",
            target="Both (Cursor + Claude)",
            task_type="Refactoring",
            style="Detailed"
        )
        msg = _build_user_message(request)
        assert "Detailed" in msg
    
    def test_includes_language_when_provided(self):
        request = PromptRequest(
            raw_input="test",
            target="Cursor",
            task_type="Code Generation",
            style="Balanced",
            language="Python"
        )
        msg = _build_user_message(request)
        assert "Python" in msg
    
    def test_excludes_language_when_empty(self):
        request = PromptRequest(
            raw_input="test",
            target="Cursor",
            task_type="Code Generation",
            style="Balanced",
            language=""
        )
        msg = _build_user_message(request)
        assert "Language/Framework:" not in msg


class TestHistoryFunctions:
    """Test history persistence layer"""
    
    def test_save_and_load_single_entry(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        
        entry = {
            "raw_input": "test input",
            "target": "Claude",
            "task_type": "Code Gen",
            "style": "Balanced",
            "language": "Python",
            "prompt": "Generated prompt",
            "tokens_used": 100,
        }
        
        save_to_history(entry)
        history = load_history()
        
        assert len(history) == 1
        assert history[0]["raw_input"] == "test input"
        assert history[0]["target"] == "Claude"
        assert history[0]["tokens_used"] == 100
    
    def test_load_empty_history_returns_list(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        history = load_history()
        assert isinstance(history, list)
        assert len(history) == 0
    
    def test_clear_history_deletes_file(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        
        entry = {"raw_input": "test", "target": "Claude", "task_type": "Test", "style": "Balanced", "language": "", "prompt": "test", "tokens_used": 10}
        save_to_history(entry)
        assert len(load_history()) == 1
        
        clear_history()
        assert len(load_history()) == 0
    
    def test_history_fifo_cap(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        
        # Add more than max items
        for i in range(HISTORY_MAX_ITEMS + 10):
            entry = {
                "raw_input": f"input {i}",
                "target": "Cursor",
                "task_type": "Test",
                "style": "Balanced",
                "language": "",
                "prompt": f"output {i}",
                "tokens_used": 10,
            }
            save_to_history(entry)
        
        history = load_history()
        assert len(history) == HISTORY_MAX_ITEMS
        
        # Verify oldest items were dropped
        assert history[0]["raw_input"] == f"input 10"  # First 10 should be gone
        assert history[-1]["raw_input"] == f"input {HISTORY_MAX_ITEMS + 9}"  # Last one should be newest
    
    def test_history_includes_timestamp(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        
        entry = {"raw_input": "test", "target": "Claude", "task_type": "Test", "style": "Balanced", "language": "", "prompt": "test", "tokens_used": 10}
        save_to_history(entry)
        
        history = load_history()
        assert "timestamp" in history[0]
        assert "T" in history[0]["timestamp"]  # ISO format inclusion


class TestPromptResponse:
    """Test PromptResponse model"""
    
    def test_successful_response(self):
        response = PromptResponse(
            prompt="Test prompt",
            tokens_used=100,
            error=""
        )
        assert response.prompt == "Test prompt"
        assert response.tokens_used == 100
        assert response.error == ""
    
    def test_error_response(self):
        response = PromptResponse(
            prompt="",
            tokens_used=0,
            error="API Error"
        )
        assert response.error == "API Error"
        assert response.prompt == ""


class TestIntegration:
    """Integration tests for full workflow"""
    
    def test_history_workflow(self, tmp_path, monkeypatch):
        """Test complete save, load, clear workflow"""
        monkeypatch.chdir(tmp_path)
        
        # Save 3 entries
        for i in range(3):
            entry = {
                "raw_input": f"input {i}",
                "target": "Claude",
                "task_type": "Code Gen",
                "style": "Balanced",
                "language": "Python",
                "prompt": f"prompt {i}",
                "tokens_used": 100 + i,
            }
            save_to_history(entry)
        
        # Load and verify
        history = load_history()
        assert len(history) == 3
        assert history[0]["raw_input"] == "input 0"
        assert history[-1]["raw_input"] == "input 2"
        
        # Clear
        clear_history()
        assert len(load_history()) == 0
    
    def test_markdown_stripping_in_workflow(self):
        """Ensure markdown is properly handled"""
        texts = [
            "```\nPrompt text\n```",
            "```python\nCode prompt\n```",
            "Normal prompt with no fences",
        ]
        
        for text in texts:
            cleaned = _strip_markdown_fences(text)
            assert "```" not in cleaned
            assert len(cleaned) > 0
