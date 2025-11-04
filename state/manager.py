"""State management for agent runs."""

from pathlib import Path
from typing import Dict, Any, Optional, List
import json
from datetime import datetime
import uuid


class StateManager:
    """Manages state and logging for agent runs."""
    
    def __init__(self, state_dir: Path):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.current_run_id: Optional[str] = None
    
    def start_run(self, prompt: str, workspace: Path, dry_run: bool = False) -> str:
        """Start a new run and return run ID."""
        run_id = str(uuid.uuid4())[:8]
        self.current_run_id = run_id
        
        run_data = {
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "workspace": str(workspace),
            "dry_run": dry_run,
            "status": "running",
            "steps": []
        }
        
        run_file = self.state_dir / f"run_{run_id}.json"
        run_file.write_text(json.dumps(run_data, indent=2), encoding="utf-8")
        
        return run_id
    
    def log_step(self, step: Dict[str, Any]):
        """Log a step to the current run."""
        if not self.current_run_id:
            return
        
        run_file = self.state_dir / f"run_{self.current_run_id}.json"
        if not run_file.exists():
            return
        
        run_data = json.loads(run_file.read_text(encoding="utf-8"))
        run_data["steps"].append(step)
        run_file.write_text(json.dumps(run_data, indent=2), encoding="utf-8")
    
    def complete_run(self, success: bool, results: Optional[Dict[str, Any]] = None):
        """Mark run as complete."""
        if not self.current_run_id:
            return
        
        run_file = self.state_dir / f"run_{self.current_run_id}.json"
        if not run_file.exists():
            return
        
        run_data = json.loads(run_file.read_text(encoding="utf-8"))
        run_data["status"] = "completed" if success else "failed"
        run_data["completed_at"] = datetime.now().isoformat()
        if results:
            run_data["results"] = results
        
        run_file.write_text(json.dumps(run_data, indent=2), encoding="utf-8")
        self.current_run_id = None
    
    def get_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Get run data by ID."""
        run_file = self.state_dir / f"run_{run_id}.json"
        if not run_file.exists():
            return None
        
        return json.loads(run_file.read_text(encoding="utf-8"))
    
    def list_runs(self, limit: int = 10) -> List[Dict[str, Any]]:
        """List recent runs."""
        runs = []
        for run_file in sorted(self.state_dir.glob("run_*.json"), reverse=True):
            if len(runs) >= limit:
                break
            try:
                run_data = json.loads(run_file.read_text(encoding="utf-8"))
                runs.append(run_data)
            except:
                continue
        
        return runs

