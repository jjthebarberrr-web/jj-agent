"""Configuration management for JJ Agent."""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from dotenv import load_dotenv


class Config:
    """Global configuration manager."""

    def __init__(self):
        # Load .env file if present
        env_file = Path(".env")
        if env_file.exists():
            load_dotenv(env_file)

        # Environment detection
        self.env = os.getenv("JJ_ENV", "development").lower()
        self.is_production = self.env == "production"
        self.prod_strict = os.getenv("JJ_PROD_STRICT", "0") == "1"

        # Version
        self.version = os.getenv("JJ_VERSION", "0.1.0")

        # Default workspace
        self.default_workspace = Path.home() / "code"

        # Budgets and timeouts
        self.max_tool_seconds = int(os.getenv("JJ_MAX_TOOL_SECONDS", "180"))
        self.max_job_minutes = int(os.getenv("JJ_MAX_JOB_MINUTES", "20"))
        self.max_fetches_per_job = int(os.getenv("JJ_MAX_FETCHES_PER_JOB", "50"))

        # Web access
        self.allow_web = (
            os.getenv("JJ_ALLOW_WEB", "0") == "1" if self.is_production else True
        )

        # Runtime mode
        self.runtime = os.getenv(
            "JJ_RUNTIME", "localsafe"
        ).lower()  # localsafe or sandboxed

        # Secrets redaction
        self.redact_patterns = [
            r"sk-[A-Za-z0-9]{20,}",
            r"ghp_[A-Za-z0-9]{36}",
            r"xoxb-[A-Za-z0-9-]+",
        ]

    def load_capabilities(self, agent_dir: Path, workspace: Path) -> Dict[str, Any]:
        """Load capabilities configuration."""
        if self.is_production:
            # Production mode: require capabilities.prod.yaml
            prod_file = agent_dir / "capabilities.prod.yaml"
            if not prod_file.exists():
                raise ValueError(
                    f"Production mode requires capabilities.prod.yaml at {prod_file}. "
                    "Refusing to start without production capabilities."
                )
            capabilities_file = prod_file
        else:
            # Development mode: use capabilities.yaml or default
            capabilities_file = agent_dir / "capabilities.yaml"

        if not capabilities_file.exists():
            # Return safe defaults
            return {
                "allowed_paths": [str(workspace / "**")],
                "denied_paths": [],
                "deny_globs": [],
                "allowed_commands": [],
                "denied_commands": [],
                "network": {"allow_web": False, "allowed_domains": []},
                "budgets": {"job_minutes": self.max_job_minutes, "web_dollars": 2.00},
                "timeouts": {
                    "tool_seconds": self.max_tool_seconds,
                    "fetch_seconds": 12,
                },
                "logging": {"redact_patterns": self.redact_patterns},
            }

        with open(capabilities_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        # Expand placeholders
        workspace_str = str(workspace.resolve())
        home_str = str(Path.home())

        # Expand allowed_paths
        if "allowed_paths" in data:
            data["allowed_paths"] = [
                p.replace("${workspace}", workspace_str)
                .replace("~/", f"{home_str}/")
                .replace("~", home_str)
                for p in data["allowed_paths"]
            ]

        # Expand denied_paths
        if "denied_paths" in data:
            data["denied_paths"] = [
                p.replace("${workspace}", workspace_str)
                .replace("~/", f"{home_str}/")
                .replace("~", home_str)
                for p in data["denied_paths"]
            ]

        # Merge with defaults
        defaults = {
            "budgets": {"job_minutes": self.max_job_minutes, "web_dollars": 2.00},
            "timeouts": {"tool_seconds": self.max_tool_seconds, "fetch_seconds": 12},
            "logging": {"redact_patterns": self.redact_patterns},
        }

        for key, value in defaults.items():
            if key not in data:
                data[key] = value
            elif isinstance(value, dict):
                data[key] = {**value, **data.get(key, {})}

        return data

    def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get secret from environment (with dotenv support)."""
        return os.getenv(key, default)

    def redact_secrets(self, text: str) -> str:
        """Redact secrets from text using patterns."""
        import re

        redacted = text
        for pattern in self.redact_patterns:
            redacted = re.sub(pattern, "[REDACTED]", redacted)
        return redacted


# Global config instance
config = Config()
