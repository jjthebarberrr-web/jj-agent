"""Configuration tests."""

import os
from pathlib import Path
from config import Config


def test_production_mode_detection():
    """Test production mode detection."""
    os.environ["JJ_ENV"] = "production"
    config = Config()
    assert config.is_production
    assert config.env == "production"
    
    os.environ.pop("JJ_ENV", None)
    config = Config()
    assert not config.is_production


def test_capabilities_loading():
    """Test capabilities loading."""
    config = Config()
    agent_dir = Path(__file__).parent.parent
    workspace = Path.home() / "code"
    
    # Should load if file exists
    try:
        caps = config.load_capabilities(agent_dir, workspace)
        assert "allowed_paths" in caps
    except ValueError:
        # Expected if production and no prod file
        pass


def test_secret_redaction():
    """Test secret redaction."""
    config = Config()
    
    text = "api_key=sk-1234567890abcdefghij"
    redacted = config.redact_secrets(text)
    
    assert "sk-" not in redacted or "[REDACTED]" in redacted

