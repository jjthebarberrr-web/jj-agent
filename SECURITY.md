# Security Documentation

## Overview

JJ Agent implements multiple layers of security to ensure safe execution of code generation tasks.

## Sandboxing

### LocalSafe Runtime

The default runtime uses strict allowlists:

- **Path Allowlist**: Only paths within allowed directories can be accessed
- **Command Allowlist**: Only regex-matched commands can be executed
- **Deny Glob Patterns**: Glob patterns that deny access (e.g., `**/.env`, `**/.ssh/**`)
- **Dangerous Pattern Detection**: Blocks commands like `rm -rf /`, `curl | bash`, fork bombs

### Sandboxed Runtime (Docker)

For maximum isolation, use the sandboxed runtime:

```bash
JJ_RUNTIME=sandboxed jj run "your prompt"
```

Features:
- `--pids-limit`: Limit process count
- `--cpus`: CPU limit
- `--memory`: Memory limit
- `--read-only`: Read-only root filesystem
- `--no-new-privileges`: Prevent privilege escalation
- Bind mount only workspace directory

## Capabilities Configuration

### Production Mode

In production mode (`JJ_ENV=production`), the agent requires `capabilities.prod.yaml`:

- Strict allowlists for paths and commands
- Network restrictions
- Budget limits
- Timeout constraints

### Adding Allowed Commands

Edit `capabilities.prod.yaml`:

```yaml
allowed_commands:
  - "^your-command "  # Regex pattern
```

### Adding Allowed Domains

```yaml
network:
  allow_web: true
  allowed_domains:
    - "example.com"
    - "docs.example.com"
```

## Kill-Switch

The agent automatically blocks:

1. **Dangerous Commands**:
   - `rm -rf /`
   - `format`
   - `curl | bash`
   - Fork bombs

2. **Path Violations**:
   - Writing outside allowed paths
   - Accessing system directories
   - Accessing `.ssh` or `.env` files

3. **Network Violations**:
   - Web access without `JJ_ALLOW_WEB=1`
   - Accessing non-allowlisted domains

## Audit Logging

All actions are logged to `state/<job-id>/audit.jsonl`:

- Tool calls
- Arguments
- Results
- Duration
- Denials

## Secrets Management

- Secrets are redacted from logs using pattern matching
- API keys are never logged
- Use environment variables or `.env` files
- Never commit secrets to version control

## Best Practices

1. **Use Production Mode**: Always use `JJ_ENV=production` in production
2. **Restrict Paths**: Limit allowed paths to specific directories
3. **Whitelist Commands**: Only allow necessary commands
4. **Monitor Audit Logs**: Regularly review `state/*/audit.jsonl`
5. **Use Sandboxed Runtime**: For untrusted code, use Docker sandboxing
6. **Rotate Secrets**: Regularly rotate API keys and tokens

## Reporting Security Issues

If you discover a security vulnerability, please report it privately.

