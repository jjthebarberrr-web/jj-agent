"""Audit logging for compliance and security."""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class AuditLogger:
    """Audit trail logger for all tool calls and actions."""
    
    def __init__(self, job_id: str, state_dir: Path):
        self.job_id = job_id
        self.audit_file = state_dir / job_id / "audit.jsonl"
        self.audit_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log_action(
        self,
        tool: str,
        args: Dict[str, Any],
        result: Dict[str, Any],
        duration_ms: float,
        exit_code: Optional[int] = None
    ):
        """Log an action to audit trail."""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "job_id": self.job_id,
            "tool": tool,
            "args": args,
            "result": {
                "success": result.get("success", False),
                "error": result.get("error"),
                "denied": result.get("denied", False)
            },
            "duration_ms": duration_ms,
            "exit_code": exit_code
        }
        
        try:
            with open(self.audit_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(audit_entry) + "\n")
        except Exception:
            pass  # Don't fail on audit write errors
    
    def log_denial(
        self,
        tool: str,
        args: Dict[str, Any],
        reason: str
    ):
        """Log a denied action."""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "job_id": self.job_id,
            "tool": tool,
            "args": args,
            "result": {
                "success": False,
                "error": reason,
                "denied": True
            },
            "duration_ms": 0,
            "exit_code": None
        }
        
        try:
            with open(self.audit_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(audit_entry) + "\n")
        except Exception:
            pass

