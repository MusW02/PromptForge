import json
import os
from datetime import datetime
from typing import List, Dict, Any


HISTORY_FILE = "prompt_history.json"
HISTORY_MAX_ITEMS = 50


def load_history() -> List[Dict[str, Any]]:
    """
    Load prompt history from the JSON file.
    
    Returns:
        List of history dictionaries, capped at HISTORY_MAX_ITEMS
    """
    if not os.path.exists(HISTORY_FILE):
        return []
    
    try:
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
            # Ensure it's a list and cap at max items
            if not isinstance(history, list):
                history = []
            return history[-HISTORY_MAX_ITEMS:]  # Return only last 50 items
    except (json.JSONDecodeError, IOError):
        return []


def save_to_history(entry: Dict[str, Any]) -> None:
    """
    Save a new prompt entry to the history file, maintaining FIFO 50-item cap.
    
    Args:
        entry: Dictionary containing:
            - raw_input (str)
            - target (str)
            - task_type (str)
            - style (str)
            - language (str, optional)
            - prompt (str) - the generated prompt
            - tokens_used (int)
            - timestamp (str) - ISO format
    """
    # Ensure the entry has a timestamp
    if "timestamp" not in entry:
        entry["timestamp"] = datetime.now().isoformat()
    
    # Load existing history
    history = load_history()
    
    # Add new entry
    history.append(entry)
    
    # Keep only the last 50 items (FIFO)
    history = history[-HISTORY_MAX_ITEMS:]
    
    # Write back to file
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
    except IOError as e:
        print(f"Warning: Could not save to history file: {e}")


def clear_history() -> None:
    """
    Clear all prompt history by deleting or truncating the history file.
    """
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
    except IOError as e:
        print(f"Warning: Could not clear history file: {e}")


def get_history_stats() -> Dict[str, Any]:
    """
    Get statistics about the current history.
    
    Returns:
        Dictionary with 'total_items' and 'max_items'
    """
    history = load_history()
    return {
        "total_items": len(history),
        "max_items": HISTORY_MAX_ITEMS,
    }
