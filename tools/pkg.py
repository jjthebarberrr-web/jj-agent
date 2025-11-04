"""Package management tool."""

from pathlib import Path
from typing import Dict, Any, Optional, List
from .shell import ShellTool


class PackageTool:
    """Tool for package management operations."""
    
    def __init__(self, workspace: Path, capabilities: Dict[str, Any]):
        self.workspace = Path(workspace).resolve()
        self.capabilities = capabilities
        self.shell = ShellTool(workspace, capabilities)
    
    def _detect_manager(self, path: Optional[str] = None) -> str:
        """Detect package manager from project files."""
        work_dir = Path(path) if path else self.workspace
        
        if (work_dir / "pyproject.toml").exists() or (work_dir / "requirements.txt").exists():
            # Try uv first, then pip
            result = self.shell.run("uv --version", cwd=str(work_dir))
            if result["success"]:
                return "uv"
            return "pip"
        
        if (work_dir / "package.json").exists():
            if (work_dir / "pnpm-lock.yaml").exists():
                return "pnpm"
            if (work_dir / "yarn.lock").exists():
                return "yarn"
            return "npm"
        
        return "pip"  # Default
    
    def install(
        self, 
        packages: Optional[List[str]] = None,
        manager: Optional[str] = None,
        path: Optional[str] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """Install packages."""
        work_dir = Path(path) if path else self.workspace
        manager = manager or self._detect_manager(str(work_dir))
        
        if packages:
            # Install specific packages
            if manager == "uv":
                cmd = f"uv pip install {' '.join(packages)}"
            elif manager == "pip" or manager == "pip3":
                cmd = f"{manager} install {' '.join(packages)}"
            elif manager in ["npm", "pnpm", "yarn"]:
                cmd = f"{manager} install {' '.join(packages)}"
            else:
                return {"success": False, "error": f"Unknown package manager: {manager}"}
        else:
            # Install from lock file
            if manager == "uv":
                cmd = "uv pip install -r requirements.txt"
            elif manager == "pip" or manager == "pip3":
                cmd = f"{manager} install -r requirements.txt"
            elif manager == "npm":
                cmd = "npm install"
            elif manager == "pnpm":
                cmd = "pnpm install"
            elif manager == "yarn":
                cmd = "yarn install"
            else:
                return {"success": False, "error": f"Unknown package manager: {manager}"}
        
        return self.shell.run(cmd, cwd=str(work_dir), dry_run=dry_run)
    
    def add(self, package: str, dev: bool = False, manager: Optional[str] = None, path: Optional[str] = None, dry_run: bool = False) -> Dict[str, Any]:
        """Add a package (and save to dependencies)."""
        work_dir = Path(path) if path else self.workspace
        manager = manager or self._detect_manager(str(work_dir))
        
        if manager in ["pip", "pip3", "uv"]:
            # For Python, just install
            return self.install([package], manager=manager, path=str(work_dir), dry_run=dry_run)
        elif manager == "npm":
            cmd = f"npm install {'--save-dev' if dev else '--save'} {package}"
        elif manager == "pnpm":
            cmd = f"pnpm add {'--save-dev' if dev else ''} {package}"
        elif manager == "yarn":
            cmd = f"yarn add {'--dev' if dev else ''} {package}"
        else:
            return {"success": False, "error": f"Unknown package manager: {manager}"}
        
        return self.shell.run(cmd, cwd=str(work_dir), dry_run=dry_run)

