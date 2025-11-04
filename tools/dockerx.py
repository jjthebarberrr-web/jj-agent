"""Docker operations tool."""

from pathlib import Path
from typing import Dict, Any, Optional
from .shell import ShellTool


class DockerTool:
    """Tool for Docker operations."""
    
    def __init__(self, workspace: Path, capabilities: Dict[str, Any]):
        self.workspace = Path(workspace).resolve()
        self.capabilities = capabilities
        self.shell = ShellTool(workspace, capabilities)
    
    def compose_up(
        self, 
        file: Optional[str] = None,
        detach: bool = True,
        build: bool = False,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """Start docker-compose services."""
        file_arg = f"-f {file}" if file else ""
        build_arg = "--build" if build else ""
        detach_arg = "-d" if detach else ""
        
        cmd = f"docker-compose {file_arg} up {build_arg} {detach_arg}".strip()
        return self.shell.run(cmd, cwd=str(self.workspace), dry_run=dry_run)
    
    def compose_down(
        self,
        file: Optional[str] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """Stop docker-compose services."""
        file_arg = f"-f {file}" if file else ""
        cmd = f"docker-compose {file_arg} down".strip()
        return self.shell.run(cmd, cwd=str(self.workspace), dry_run=dry_run)
    
    def compose_ps(
        self,
        file: Optional[str] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """List docker-compose services."""
        file_arg = f"-f {file}" if file else ""
        cmd = f"docker-compose {file_arg} ps".strip()
        return self.shell.run(cmd, cwd=str(self.workspace), dry_run=dry_run)
    
    def compose_logs(
        self,
        service: Optional[str] = None,
        file: Optional[str] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """Get docker-compose logs."""
        file_arg = f"-f {file}" if file else ""
        service_arg = service or ""
        cmd = f"docker-compose {file_arg} logs {service_arg}".strip()
        return self.shell.run(cmd, cwd=str(self.workspace), dry_run=dry_run)

