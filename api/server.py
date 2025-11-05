"""FastAPI server for daemon mode and health endpoints."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Dict, Any
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from metrics import metrics
from config import config

app = FastAPI(title="JJ Agent API", version=config.version)


@app.get("/healthz")
async def healthz() -> Dict[str, Any]:
    """Liveness probe."""
    return {"status": "healthy", "version": config.version}


@app.get("/readyz")
async def readyz() -> Dict[str, Any]:
    """Readiness probe."""
    # Check if we can load capabilities
    try:
        agent_dir = Path(__file__).parent.parent
        workspace = config.default_workspace
        config.load_capabilities(agent_dir, workspace)
        return {"status": "ready", "version": config.version}
    except Exception as e:
        return JSONResponse(
            status_code=503, content={"status": "not ready", "error": str(e)}
        )


@app.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Get metrics."""
    return metrics.get_stats()


@app.get("/version")
async def version() -> Dict[str, str]:
    """Get version."""
    return {"version": config.version}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5858)
