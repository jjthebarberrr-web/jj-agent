"""Sandboxed runtime using Docker/Podman."""

import subprocess
from pathlib import Path
from typing import Dict, Any, Optional


class SandboxedRuntime:
    """Sandboxed execution using Docker with strict security."""
    
    def __init__(self, workspace: Path, capabilities: Dict[str, Any]):
        self.workspace = Path(workspace).resolve()
        self.capabilities = capabilities
        self.sandbox_config = capabilities.get("sandbox", {})
        
        # Detect Docker/Podman
        self.container_runtime = "docker"
        try:
            result = subprocess.run(
                ["podman", "--version"],
                capture_output=True,
                timeout=2
            )
            if result.returncode == 0:
                self.container_runtime = "podman"
        except Exception:
            pass
    
    def _build_run_command(
        self,
        command: str,
        cwd: Optional[str] = None,
        timeout: int = 180
    ) -> list:
        """Build Docker/Podman run command with security constraints."""
        work_dir = Path(cwd).resolve() if cwd else self.workspace
        
        cmd = [self.container_runtime, "run", "--rm"]
        
        # Resource limits
        if self.sandbox_config.get("pids_limit"):
            cmd.extend(["--pids-limit", str(self.sandbox_config["pids_limit"])])
        if self.sandbox_config.get("cpus"):
            cmd.extend(["--cpus", str(self.sandbox_config["cpus"])])
        if self.sandbox_config.get("memory"):
            cmd.extend(["--memory", str(self.sandbox_config["memory"])])
        
        # Security options
        if self.sandbox_config.get("read_only_root", True):
            cmd.append("--read-only")
        if self.sandbox_config.get("no_new_privileges", True):
            cmd.append("--security-opt=no-new-privileges:true")
        
        # Seccomp profile (if available)
        # cmd.extend(["--security-opt", "seccomp=seccomp-profile.json"])
        
        # Bind mount only workspace
        cmd.extend(["--mount", f"type=bind,source={work_dir},target=/workspace,readonly=false"])
        cmd.extend(["--workdir", "/workspace"])
        
        # Use a minimal image
        image = "python:3.11-slim"  # Can be configurable
        cmd.append(image)
        
        # Add command with timeout
        cmd.extend(["sh", "-c", f"timeout {timeout} {command}"])
        
        return cmd
    
    def run(
        self,
        command: str,
        cwd: Optional[str] = None,
        timeout: int = 180,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """Run a command in sandboxed container."""
        if dry_run:
            run_cmd = self._build_run_command(command, cwd, timeout)
            return {
                "success": True,
                "dry_run": True,
                "command": command,
                "container_command": " ".join(run_cmd),
                "cwd": cwd or str(self.workspace)
            }
        
        try:
            run_cmd = self._build_run_command(command, cwd, timeout)
            
            process = subprocess.run(
                run_cmd,
                capture_output=True,
                text=True,
                timeout=timeout + 10,  # Add buffer for container overhead
                encoding="utf-8",
                errors="replace"
            )
            
            return {
                "success": process.returncode == 0,
                "command": command,
                "returncode": process.returncode,
                "stdout": process.stdout,
                "stderr": process.stderr,
                "cwd": cwd or str(self.workspace),
                "sandboxed": True
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"Command timed out after {timeout}s"}
        except FileNotFoundError:
            return {
                "success": False,
                "error": f"{self.container_runtime} not found. Install Docker or Podman."
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

