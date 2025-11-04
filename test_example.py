"""Simple test script to verify the agent structure."""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from api.llm_client import LLMClient
    from agent import Planner, Executor
    from state.manager import StateManager
    from tools import FileSystemTool, ShellTool
    
    print("[OK] All imports successful!")
    print("[OK] Agent structure is correct")
    print("\nAvailable components:")
    print("  - LLMClient")
    print("  - Planner")
    print("  - Executor")
    print("  - StateManager")
    print("  - FileSystemTool")
    print("  - ShellTool")
    print("\nReady to use!")
except ImportError as e:
    print(f"[ERROR] Import error: {e}")
    print("\nNote: You may need to install dependencies:")
    print("  pip install -r requirements.txt")
    sys.exit(1)

