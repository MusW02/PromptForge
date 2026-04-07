"""
Pytest configuration and fixtures.
This file is automatically loaded by pytest and ensures proper Python path handling.
"""

import sys
from pathlib import Path

# Add the project root to sys.path so imports work correctly
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
