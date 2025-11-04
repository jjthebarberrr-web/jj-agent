"""End-to-end smoke tests."""

import pytest
import tempfile
import shutil
from pathlib import Path
import sys

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import config
from api.llm_client import LLMClient
from agent import Planner, Executor


@pytest.mark.asyncio
async def test_dry_run_planning():
    """Test dry-run mode generates plan without executing."""
    # Skip if no API key
    if not config.get_secret("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = Path(tmpdir)
        capabilities = {
            "allowed_paths": [str(workspace / "**")],
            "denied_paths": [],
            "deny_globs": [],
            "allowed_commands": ["^echo ", "^mkdir "],
            "denied_commands": []
        }
        
        llm_client = LLMClient()
        planner = Planner(llm_client)
        executor = Executor(workspace, capabilities, llm_client, dry_run=True)
        
        plan = await planner.plan("Create a FastAPI skeleton with main.py")
        
        assert len(plan) > 0, "Plan should have steps"
        assert any(step.get("tool") == "fs_write" for step in plan), "Plan should include file writes"
        
        # Execute in dry-run mode
        result = await executor.execute_plan(plan)
        
        # Should not create any files
        assert not any((workspace / "main.py").exists() for _ in [1]), "No files should be created in dry-run"


@pytest.mark.asyncio
async def test_simple_file_creation():
    """Test creating a simple file."""
    # Skip if no API key
    if not config.get_secret("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = Path(tmpdir) / "app"
        workspace.mkdir()
        
        capabilities = {
            "allowed_paths": [str(workspace / "**")],
            "denied_paths": [],
            "deny_globs": [],
            "allowed_commands": ["^echo ", "^python "],
            "denied_commands": []
        }
        
        llm_client = LLMClient()
        planner = Planner(llm_client)
        executor = Executor(workspace, capabilities, llm_client, dry_run=False)
        
        plan = await planner.plan("Create a hello world Python script")
        
        # Execute
        result = await executor.execute_plan(plan)
        
        # Should have executed steps
        assert len(result["results"]) > 0, "Should have execution results"
        
        # Cleanup
        shutil.rmtree(workspace, ignore_errors=True)

