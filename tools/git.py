"""Git operations tool."""

from pathlib import Path
from typing import Dict, Any, Optional
from .shell import ShellTool


class GitTool:
    """Tool for Git operations."""
    
    def __init__(self, workspace: Path, capabilities: Dict[str, Any]):
        self.workspace = Path(workspace).resolve()
        self.capabilities = capabilities
        self.shell = ShellTool(workspace, capabilities)
    
    def init(self, dry_run: bool = False) -> Dict[str, Any]:
        """Initialize a Git repository."""
        return self.shell.run("git init", cwd=str(self.workspace), dry_run=dry_run)
    
    def add(self, files: str = ".", dry_run: bool = False) -> Dict[str, Any]:
        """Add files to Git staging."""
        return self.shell.run(f"git add {files}", cwd=str(self.workspace), dry_run=dry_run)
    
    def commit(self, message: str, dry_run: bool = False) -> Dict[str, Any]:
        """Commit changes."""
        # Escape the message for shell
        escaped_message = message.replace('"', '\\"')
        return self.shell.run(
            f'git commit -m "{escaped_message}"',
            cwd=str(self.workspace),
            dry_run=dry_run
        )
    
    def branch(self, name: str, create: bool = True, dry_run: bool = False) -> Dict[str, Any]:
        """Create or switch to a branch."""
        if create:
            return self.shell.run(
                f"git checkout -b {name}",
                cwd=str(self.workspace),
                dry_run=dry_run
            )
        else:
            return self.shell.run(
                f"git checkout {name}",
                cwd=str(self.workspace),
                dry_run=dry_run
            )
    
    def push(
        self, 
        remote: str = "origin", 
        branch: Optional[str] = None, 
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """Push to remote repository."""
        if branch:
            return self.shell.run(
                f"git push {remote} {branch}",
                cwd=str(self.workspace),
                dry_run=dry_run
            )
        else:
            return self.shell.run(
                f"git push {remote}",
                cwd=str(self.workspace),
                dry_run=dry_run
            )
    
    def status(self, dry_run: bool = False) -> Dict[str, Any]:
        """Get Git status."""
        return self.shell.run("git status", cwd=str(self.workspace), dry_run=dry_run)
    
    def remote_add(self, name: str, url: str, dry_run: bool = False) -> Dict[str, Any]:
        """Add a remote repository."""
        return self.shell.run(
            f"git remote add {name} {url}",
            cwd=str(self.workspace),
            dry_run=dry_run
        )

