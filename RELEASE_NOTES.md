# Release v0.1.0 - Production Ready

## 🎉 First Production Release

This is the first stable, production-ready release of JJ Agent. The agent is now hardened with comprehensive security, monitoring, and operational features.

## What's New

### Production Hardening
- **Production Mode**: `JJ_ENV=production` with strict enforcement
- **Security Sandboxing**: LocalSafe and Docker-based sandboxed runtimes
- **Capabilities System**: Production capabilities file with allowlists and budgets
- **Kill-Switch**: Automatic blocking of dangerous commands and paths

### Observability
- **Structured Logging**: JSON logs with secret redaction
- **Audit Trail**: Complete audit logs for all actions (`state/<job-id>/audit.jsonl`)
- **Metrics**: Job and tool call metrics with Prometheus-compatible format
- **Error Monitoring**: Sentry and OpenTelemetry integration

### Operations
- **Health Endpoints**: `/healthz`, `/readyz`, `/metrics`
- **Systemd Service**: Production-ready systemd unit file
- **Docker Image**: Multi-stage build, non-root user, health checks
- **Log Rotation**: Automated log rotation configuration

### Developer Experience
- **CLI Commands**: `jj doctor`, `jj config`, `jj version`
- **Plan Preview**: `jj run --plan` to preview execution
- **Dry-Run Mode**: Safe plan preview without execution
- **Better Errors**: Clear error messages and diagnostics

## Installation

### Quick Install (pipx)
```bash
pipx install jj-agent
```

### Docker
```bash
docker pull ghcr.io/ORG/jj-agent:v0.1.0
```

### Production Setup
```bash
export JJ_ENV=production
export JJ_PROD_STRICT=1
export OPENAI_API_KEY=sk-your-key

jj run "Create a FastAPI app with JWT auth and PostgreSQL" --workspace ~/code/demo
```

## Breaking Changes

None - this is the first release.

## Security

- Path allowlist enforcement
- Command regex allowlist
- Dangerous command detection
- Network domain allowlisting
- Secret redaction in logs
- Audit trail for compliance

## Documentation

- `README.md` - Full documentation
- `SECURITY.md` - Security guide
- `OPERATIONS.md` - Operations guide
- `QUICKSTART.md` - Quick start
- `CHANGELOG.md` - Version history

## Requirements

- Python 3.8+
- OpenAI API key
- (Optional) Docker for sandboxed runtime

## Known Limitations

- Web search is stubbed (fetch works, search returns error)
- Sentry/OTel require additional dependencies (optional)

## Next Steps

See `ROADMAP.md` for v0.2.0 plans:
- Web search integration
- RAG improvements
- Skills library expansion
- Faster planning & caching

## Support

Report issues on GitHub or check documentation in `docs/`.

