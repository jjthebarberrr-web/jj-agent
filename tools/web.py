"""Web search and fetch tool (production posture)."""

from pathlib import Path
from typing import Dict, Any, Optional
from urllib.parse import urlparse

from ..config import config
from jj_agent import __version__


class WebTool:
    """Tool for web search and fetch with production safety."""

    def __init__(self, workspace: Path, capabilities: Dict[str, Any]):
        self.workspace = Path(workspace).resolve()
        self.capabilities = capabilities
        self.network_config = capabilities.get("network", {})
        self.allow_web = (
            self.network_config.get("allow_web", False) and config.allow_web
        )
        self.allowed_domains = self.network_config.get("allowed_domains", [])
        self.fetch_count = 0
        self.max_fetches = config.max_fetches_per_job

    def _check_domain(self, url: str) -> tuple[bool, Optional[str]]:
        """Check if domain is allowed."""
        if not self.allow_web:
            return (
                False,
                "Web access is disabled. Set JJ_ALLOW_WEB=1 and configure allowed_domains.",
            )

        try:
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path.split("/")[0]

            # Remove port
            domain = domain.split(":")[0]

            # Check against allowlist
            if not self.allowed_domains:
                return (
                    False,
                    "No allowed domains configured. Web access requires domain allowlist.",
                )

            allowed = any(
                domain == allowed or domain.endswith(f".{allowed}")
                for allowed in self.allowed_domains
            )

            if not allowed:
                return False, f"Domain {domain} not in allowed_domains list"

            return True, None
        except Exception as e:
            return False, f"Invalid URL: {e}"

    def _check_url_scheme(self, url: str) -> tuple[bool, Optional[str]]:
        """Check URL scheme is safe."""
        blocked_schemes = ["file:", "data:", "mailto:", "javascript:"]
        for scheme in blocked_schemes:
            if url.lower().startswith(scheme):
                return False, f"Blocked URL scheme: {scheme}"

        # Only allow http/https
        if not url.lower().startswith(("http://", "https://")):
            return False, "Only http:// and https:// URLs are allowed"

        return True, None

    def fetch(self, url: str, dry_run: bool = False) -> Dict[str, Any]:
        """Fetch content from URL."""
        # Check fetch limit
        if self.fetch_count >= self.max_fetches:
            return {
                "success": False,
                "error": f"Maximum fetch limit reached ({self.max_fetches})",
            }

        # Check URL scheme
        is_safe, error = self._check_url_scheme(url)
        if not is_safe:
            return {"success": False, "error": error, "denied": True}

        # Check domain
        is_allowed, error = self._check_domain(url)
        if not is_allowed:
            return {"success": False, "error": error, "denied": True}

        if dry_run:
            return {
                "success": True,
                "dry_run": True,
                "url": url,
                "domain": urlparse(url).netloc,
            }

        try:
            import httpx

            # Set User-Agent
            headers = {"User-Agent": f"JJ-Agent/{__version__}"}

            # Fetch with timeout
            timeout = self.capabilities.get("timeouts", {}).get("fetch_seconds", 12)
            with httpx.Client(timeout=timeout) as client:
                response = client.get(url, headers=headers, follow_redirects=True)
                response.raise_for_status()

            self.fetch_count += 1

            # Redact secrets from content
            content = response.text
            content = config.redact_secrets(content)

            return {
                "success": True,
                "url": url,
                "status_code": response.status_code,
                "content": content[:10000],  # Limit content size
                "content_length": len(content),
                "fetch_count": self.fetch_count,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def search(self, query: str, dry_run: bool = False) -> Dict[str, Any]:
        """Search the web (stub - requires web search API integration)."""
        # Web search is not implemented in v0.1.0
        # This is a placeholder for future implementation
        return {
            "success": False,
            "error": "Web search not implemented. Use fetch() with specific URLs.",
        }
