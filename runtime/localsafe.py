"""LocalSafe runtime with command and path allowlists."""

import subprocess
import re
from pathlib import Path
from typing import Dict, Any, Optional
import fnmatch


class LocalSafeRuntime:
    """Safe local execution with strict allowlists."""
    
    def __init__(self, workspace: Path, capabilities: Dict[str, Any]):
        self.workspace = Path(workspace).resolve()
        self.capabilities = capabilities
        self.allowed_paths = capabilities.get("allowed_paths", [])
        self.denied_paths = capabilities.get("denied_paths", [])
        self.deny_globs = capabilities.get("deny_globs", [])
        self.allowed_commands = capabilities.get("allowed_commands", [])
        self.denied_commands = capabilities.get("denied_commands", [])
    
    def _check_path(self, path: Path) -> tuple[bool, Optional[str]]:
        """Check if a path is allowed."""
        path = Path(path).resolve()
        
        # Check denied paths (exact or prefix)
        for denied in self.denied_paths:
            denied_path = Path(denied).resolve()
            try:
                path.relative_to(denied_path)
                return False, f"Path denied: {path} matches denied path {denied}"
            except ValueError:
                pass
        
        # Check deny globs
        path_str = str(path)
        for glob_pattern in self.deny_globs:
            if fnmatch.fnmatch(path_str, glob_pattern) or fnmatch.fnmatch(path_str, f"**/{glob_pattern}"):
                return False, f"Path denied: {path} matches glob {glob_pattern}"
        
        # Check allowed paths (at least one must match)
        allowed = False
        for allowed_pattern in self.allowed_paths:
            allowed_path = Path(allowed_pattern.rstrip("/**")).resolve()
            try:
                path.relative_to(allowed_path)
                allowed = True
                break
            except ValueError:
                # Check glob pattern
                if fnmatch.fnmatch(str(path), allowed_pattern):
                    allowed = True
                    break
        
        if not allowed:
            return False, f"Path not in allowed paths: {path}"
        
        return True, None
    
    def _check_command(self, command: str) -> tuple[bool, Optional[str]]:
        """Check if a command is allowed."""
        # Check denied command patterns
        for denied_pattern in self.denied_commands:
            if denied_pattern.lower() in command.lower():
                return False, f"Command matches denied pattern: {denied_pattern}"
        
        # Check for dangerous patterns
        dangerous_patterns = [
            r"rm\s+-rf\s+/",
            r"rm\s+-rf\s+\*",
            r"format\s+",
            r"del\s+/f\s+/s\s+/q",
            r":\s*\(\s*\)\s*\{\s*:\s*\|:\s*&?\s*\}\s*;?\s*:",
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return False, f"Dangerous command pattern detected: {pattern}"
        
        # Check for unsafe pipe patterns
        if "|" in command:
            parts = command.split("|")
            if len(parts) > 1:
                for part in parts[1:]:
                    if any(cmd in part.lower() for cmd in ["bash", "sh", "python", "node"]):
                        return False, "Unsafe pipe to interpreter detected"
        
        # Check allowed commands (regex patterns)
        if self.allowed_commands:
            matched = False
            for pattern in self.allowed_commands:
                if re.match(pattern, command, re.IGNORECASE):
                    matched = True
                    break
            if not matched:
                return False, f"Command not in allowed list: {command}"
        
        return True, None
    
    def run(
        self,
        command: str,
        cwd: Optional[str] = None,
        timeout: int = 180,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """Run a command with safety checks."""
        # Check command safety
        is_allowed, error = self._check_command(command)
        if not is_allowed:
            return {"success": False, "error": error, "denied": True}
        
        if dry_run:
            return {
                "success": True,
                "dry_run": True,
                "command": command,
                "cwd": cwd or str(self.workspace)
            }
        
        try:
            work_dir = Path(cwd).resolve() if cwd else self.workspace
            
            # Verify working directory is allowed
            is_path_ok, path_error = self._check_path(work_dir)
            if not is_path_ok:
                return {"success": False, "error": path_error, "denied": True}
            
            process = subprocess.run(
                command,
                shell=True,
                cwd=str(work_dir),
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding="utf-8",
                errors="replace"
            )
            
            return {
                "success": process.returncode == 0,
                "command": command,
                "returncode": process.returncode,
                "stdout": process.stdout,
                "stderr": process.stderr,
                "cwd": str(work_dir)
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"Command timed out after {timeout}s"}
        except Exception as e:
            return {"success": False, "error": str(e)}

