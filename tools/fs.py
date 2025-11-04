"""File system operations tool."""

import os
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
import difflib


class FileSystemTool:
    """Tool for file system operations."""
    
    def __init__(self, workspace: Path, capabilities: Dict[str, Any]):
        self.workspace = Path(workspace).resolve()
        self.capabilities = capabilities
        self.allowed_paths = capabilities.get("allowed_paths", [])
        self.denied_paths = capabilities.get("denied_paths", [])
    
    def _check_path(self, path: Path) -> bool:
        """Check if a path is allowed."""
        path = Path(path).resolve()
        
        # Check if path is within workspace
        try:
            path.relative_to(self.workspace)
        except ValueError:
            return False
        
        # Check denied paths
        path_str = str(path)
        for denied in self.denied_paths:
            denied_expanded = denied.replace("${workspace}", str(self.workspace))
            if path_str.startswith(denied_expanded) or path_str == denied_expanded:
                return False
        
        # Check allowed paths
        for allowed in self.allowed_paths:
            allowed_expanded = allowed.replace("${workspace}", str(self.workspace))
            if path_str.startswith(allowed_expanded) or path_str == denied_expanded:
                return True
        
        return True
    
    def write(self, path: str, content: str, dry_run: bool = False) -> Dict[str, Any]:
        """Write content to a file."""
        file_path = self.workspace / path
        
        if not self._check_path(file_path):
            return {"success": False, "error": f"Path not allowed: {path}"}
        
        if dry_run:
            existing = None
            if file_path.exists():
                existing = file_path.read_text(encoding="utf-8")
            
            diff = ""
            if existing is not None:
                diff = "\n".join(difflib.unified_diff(
                    existing.splitlines(keepends=True),
                    content.splitlines(keepends=True),
                    fromfile=f"a/{path}",
                    tofile=f"b/{path}",
                    lineterm=""
                ))
            else:
                diff = f"+++ New file: {path}\n{content}"
            
            return {
                "success": True,
                "dry_run": True,
                "path": str(file_path),
                "diff": diff,
                "action": "create" if existing is None else "modify"
            }
        
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            return {"success": True, "path": str(file_path), "action": "write"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def patch(self, path: str, old_string: str, new_string: str, dry_run: bool = False) -> Dict[str, Any]:
        """Patch a file by replacing old_string with new_string."""
        file_path = self.workspace / path
        
        if not self._check_path(file_path):
            return {"success": False, "error": f"Path not allowed: {path}"}
        
        if not file_path.exists():
            return {"success": False, "error": f"File does not exist: {path}"}
        
        try:
            content = file_path.read_text(encoding="utf-8")
            
            if old_string not in content:
                return {"success": False, "error": "old_string not found in file"}
            
            new_content = content.replace(old_string, new_string)
            
            if dry_run:
                diff = "\n".join(difflib.unified_diff(
                    content.splitlines(keepends=True),
                    new_content.splitlines(keepends=True),
                    fromfile=f"a/{path}",
                    tofile=f"b/{path}",
                    lineterm=""
                ))
                return {
                    "success": True,
                    "dry_run": True,
                    "path": str(file_path),
                    "diff": diff,
                    "action": "patch"
                }
            
            file_path.write_text(new_content, encoding="utf-8")
            return {"success": True, "path": str(file_path), "action": "patch"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def mkdir(self, path: str, dry_run: bool = False) -> Dict[str, Any]:
        """Create a directory."""
        dir_path = self.workspace / path
        
        if not self._check_path(dir_path):
            return {"success": False, "error": f"Path not allowed: {path}"}
        
        if dry_run:
            exists = dir_path.exists()
            return {
                "success": True,
                "dry_run": True,
                "path": str(dir_path),
                "action": "mkdir",
                "exists": exists
            }
        
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            return {"success": True, "path": str(dir_path), "action": "mkdir"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def read(self, path: str) -> Dict[str, Any]:
        """Read a file."""
        file_path = self.workspace / path
        
        if not self._check_path(file_path):
            return {"success": False, "error": f"Path not allowed: {path}"}
        
        if not file_path.exists():
            return {"success": False, "error": f"File does not exist: {path}"}
        
        try:
            content = file_path.read_text(encoding="utf-8")
            return {"success": True, "content": content, "path": str(file_path)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_files(self, path: str = ".") -> Dict[str, Any]:
        """List files in a directory."""
        dir_path = self.workspace / path
        
        if not self._check_path(dir_path):
            return {"success": False, "error": f"Path not allowed: {path}"}
        
        if not dir_path.exists():
            return {"success": False, "error": f"Directory does not exist: {path}"}
        
        try:
            files = []
            for item in dir_path.iterdir():
                files.append({
                    "name": item.name,
                    "path": str(item.relative_to(self.workspace)),
                    "type": "directory" if item.is_dir() else "file"
                })
            return {"success": True, "files": files, "path": str(dir_path)}
        except Exception as e:
            return {"success": False, "error": str(e)}

