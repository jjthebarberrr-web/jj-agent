"""Test execution tool."""

from pathlib import Path
from typing import Dict, Any, Optional
from .shell import ShellTool


class TestTool:
    """Tool for running tests."""

    def __init__(self, workspace: Path, capabilities: Dict[str, Any]):
        self.workspace = Path(workspace).resolve()
        self.capabilities = capabilities
        self.shell = ShellTool(workspace, capabilities)

    def _detect_test_framework(self, path: Optional[str] = None) -> str:
        """Detect test framework from project files."""
        work_dir = Path(path) if path else self.workspace

        # Check for pytest
        if (work_dir / "pytest.ini").exists() or (work_dir / "pyproject.toml").exists():
            result = self.shell.run("pytest --version", cwd=str(work_dir))
            if result["success"]:
                return "pytest"

        # Check for jest
        if (work_dir / "package.json").exists():
            try:
                import json

                pkg = json.loads((work_dir / "package.json").read_text())
                if "jest" in pkg.get("devDependencies", {}) or "jest" in pkg.get(
                    "dependencies", {}
                ):
                    return "jest"
            except Exception:
                pass

        # Default to pytest for Python, jest for Node
        if (work_dir / "requirements.txt").exists() or (
            work_dir / "pyproject.toml"
        ).exists():
            return "pytest"
        elif (work_dir / "package.json").exists():
            return "jest"

        return "pytest"

    def pytest(
        self,
        path: Optional[str] = None,
        args: Optional[str] = None,
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """Run pytest tests."""
        work_dir = Path(path) if path else self.workspace
        cmd = f"pytest {args or ''}".strip()
        return self.shell.run(cmd, cwd=str(work_dir), dry_run=dry_run)

    def jest(
        self,
        path: Optional[str] = None,
        args: Optional[str] = None,
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """Run jest tests."""
        work_dir = Path(path) if path else self.workspace
        cmd = f"npm test {args or ''}".strip()
        return self.shell.run(cmd, cwd=str(work_dir), dry_run=dry_run)

    def run(
        self,
        framework: Optional[str] = None,
        path: Optional[str] = None,
        args: Optional[str] = None,
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """Run tests with auto-detected or specified framework."""
        work_dir = Path(path) if path else self.workspace
        framework = framework or self._detect_test_framework(str(work_dir))

        if framework == "pytest":
            return self.pytest(path=str(work_dir), args=args, dry_run=dry_run)
        elif framework == "jest":
            return self.jest(path=str(work_dir), args=args, dry_run=dry_run)
        else:
            return {"success": False, "error": f"Unknown test framework: {framework}"}
