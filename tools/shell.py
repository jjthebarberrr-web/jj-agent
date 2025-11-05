"""Shell command execution tool."""

from pathlib import Path
from typing import Dict, Any, Optional

try:
    from ..config import config
    from ..runtime import LocalSafeRuntime, SandboxedRuntime
except ImportError:
    # Fallback for direct execution
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from config import config
    from runtime import LocalSafeRuntime, SandboxedRuntime


class ShellTool:
    """Tool for executing shell commands."""

    def __init__(self, workspace: Path, capabilities: Dict[str, Any]):
        self.workspace = Path(workspace).resolve()
        self.capabilities = capabilities

        # Initialize runtime based on config
        runtime_type = config.runtime
        if runtime_type == "sandboxed":
            self.runtime = SandboxedRuntime(workspace, capabilities)
        else:
            self.runtime = LocalSafeRuntime(workspace, capabilities)

    def run(
        self,
        command: str,
        cwd: Optional[str] = None,
        dry_run: bool = False,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Run a shell command."""
        if timeout is None:
            timeout = config.max_tool_seconds

        return self.runtime.run(
            command=command, cwd=cwd, timeout=timeout, dry_run=dry_run
        )
