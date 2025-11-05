"""Additional CLI commands (doctor, config, etc.)."""

import sys
from pathlib import Path
import subprocess

from ..config import config


def cmd_doctor() -> int:
    """Run diagnostics and print system status."""
    print("JJ Agent Diagnostics")
    print("=" * 60)
    
    issues = []
    
    # Environment
    print(f"\nEnvironment: {config.env}")
    print(f"Production Mode: {config.is_production}")
    print(f"Strict Mode: {config.prod_strict}")
    
    # Python
    print(f"\nPython: {sys.version.split()[0]}")
    
    # Docker
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            timeout=2
        )
        if result.returncode == 0:
            print(f"Docker: {result.stdout.decode().strip()}")
        else:
            issues.append("Docker not found")
    except Exception:
        issues.append("Docker not available")
    
    # Workspace
    workspace = config.default_workspace
    if workspace.exists():
        print(f"\nDefault Workspace: {workspace} (exists)")
    else:
        print(f"\nDefault Workspace: {workspace} (does not exist)")
        issues.append(f"Default workspace {workspace} does not exist")
    
    # Capabilities
    agent_dir = Path(__file__).parent.parent
    if config.is_production:
        cap_file = agent_dir / "capabilities.prod.yaml"
        if cap_file.exists():
            print(f"\nCapabilities: {cap_file} (found)")
        else:
            print(f"\nCapabilities: {cap_file} (MISSING)")
            issues.append("Production capabilities file missing")
    else:
        cap_file = agent_dir / "capabilities.yaml"
        if cap_file.exists():
            print(f"\nCapabilities: {cap_file} (found)")
        else:
            print(f"\nCapabilities: {cap_file} (using defaults)")
    
    # API Key
    api_key = config.get_secret("OPENAI_API_KEY")
    if api_key:
        print(f"\nAPI Key: Set (length: {len(api_key)})")
    else:
        print("\nAPI Key: NOT SET")
        issues.append("OPENAI_API_KEY not set")
    
    # Permissions
    try:
        test_file = workspace / ".jj_test"
        test_file.write_text("test")
        test_file.unlink()
        print("\nPermissions: Workspace writable")
    except Exception as e:
        issues.append(f"Workspace not writable: {e}")
        print("\nPermissions: Workspace NOT writable")
    
    # Summary
    print("\n" + "=" * 60)
    if issues:
        print(f"⚠️  Found {len(issues)} issue(s):")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    else:
        print("✅ All checks passed")
        return 0


def cmd_config_show() -> int:
    """Show merged configuration."""
    print("JJ Agent Configuration")
    print("=" * 60)
    
    # Environment config
    print("\nEnvironment:")
    print(f"  JJ_ENV: {config.env}")
    print(f"  JJ_PROD_STRICT: {config.prod_strict}")
    print(f"  JJ_RUNTIME: {config.runtime}")
    print(f"  JJ_ALLOW_WEB: {config.allow_web}")
    
    # Timeouts
    print("\nTimeouts:")
    print(f"  Max Tool Seconds: {config.max_tool_seconds}")
    print(f"  Max Job Minutes: {config.max_job_minutes}")
    print(f"  Max Fetches Per Job: {config.max_fetches_per_job}")
    
    # Workspace
    print(f"\nDefault Workspace: {config.default_workspace}")
    
    # Load capabilities
    agent_dir = Path(__file__).parent.parent
    workspace = config.default_workspace
    try:
        capabilities = config.load_capabilities(agent_dir, workspace)
        
        print("\nCapabilities:")
        print(f"  Allowed Paths: {len(capabilities.get('allowed_paths', []))} patterns")
        print(f"  Denied Paths: {len(capabilities.get('denied_paths', []))} patterns")
        print(f"  Deny Globs: {len(capabilities.get('deny_globs', []))} patterns")
        print(f"  Allowed Commands: {len(capabilities.get('allowed_commands', []))} patterns")
        
        network = capabilities.get("network", {})
        print("\nNetwork:")
        print(f"  Allow Web: {network.get('allow_web', False)}")
        print(f"  Allowed Domains: {len(network.get('allowed_domains', []))}")
        
        budgets = capabilities.get("budgets", {})
        print("\nBudgets:")
        print(f"  Job Minutes: {budgets.get('job_minutes', 20)}")
        print(f"  Web Dollars: ${budgets.get('web_dollars', 2.00)}")
        
        # Redact secrets in output
        print("\nRedaction Patterns:")
        for pattern in config.redact_patterns:
            print(f"  {pattern}")
        
    except Exception as e:
        print(f"\nError loading capabilities: {e}")
        return 1
    
    return 0


def cmd_version() -> int:
    """Print version."""
    print(f"jj-agent version {config.version}")
    return 0

