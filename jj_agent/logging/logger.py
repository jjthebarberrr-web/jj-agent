"""Structured JSON logging."""

import json
import sys
from pathlib import Path
from typing import Any, Optional
from datetime import datetime
import re

from ..config import config


class Logger:
    """Structured JSON logger."""

    def __init__(self, job_id: Optional[str] = None, log_file: Optional[Path] = None):
        self.job_id = job_id
        self.log_file = log_file
        self.redact_patterns = config.redact_patterns

    def _redact(self, data: Any) -> Any:
        """Recursively redact secrets from data."""
        if isinstance(data, str):
            redacted = data
            for pattern in self.redact_patterns:
                redacted = re.sub(pattern, "[REDACTED]", redacted, flags=re.IGNORECASE)
            return redacted
        elif isinstance(data, dict):
            return {k: self._redact(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._redact(item) for item in data]
        else:
            return data

    def _log(self, level: str, message: str, **kwargs):
        """Write structured log entry."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level,
            "message": message,
            "job_id": self.job_id,
            **kwargs,
        }

        # Redact secrets
        log_entry = self._redact(log_entry)

        # Write to stdout as JSON
        json_str = json.dumps(log_entry)
        print(json_str, file=sys.stderr)

        # Write to file if specified
        if self.log_file:
            try:
                self.log_file.parent.mkdir(parents=True, exist_ok=True)
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(json_str + "\n")
            except Exception:
                pass  # Don't fail on log write errors

    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self._log("DEBUG", message, **kwargs)

    def info(self, message: str, **kwargs):
        """Log info message."""
        self._log("INFO", message, **kwargs)

    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self._log("WARNING", message, **kwargs)

    def error(self, message: str, **kwargs):
        """Log error message."""
        self._log("ERROR", message, **kwargs)

    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self._log("CRITICAL", message, **kwargs)


def get_logger(job_id: Optional[str] = None, log_file: Optional[Path] = None) -> Logger:
    """Get a logger instance."""
    return Logger(job_id=job_id, log_file=log_file)
