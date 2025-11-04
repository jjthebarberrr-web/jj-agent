# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-11-03

### Added

- Production mode with `JJ_ENV=production`
- Strict security enforcement with `JJ_PROD_STRICT=1`
- LocalSafe runtime with command and path allowlists
- Sandboxed runtime using Docker/Podman
- Production capabilities file (`capabilities.prod.yaml`)
- Structured JSON logging with secret redaction
- Audit trail logging (`state/<job-id>/audit.jsonl`)
- Metrics collection (jobs, tool calls, denials)
- Error monitoring integration (Sentry/OpenTelemetry)
- Docker image with non-root user
- Systemd service file
- Health endpoints (`/healthz`, `/readyz`, `/metrics`)
- CLI commands: `doctor`, `config`, `version`
- `run --plan` flag to preview execution plan
- Log rotation configuration
- CI/CD workflow for automated releases
- Comprehensive test suite
- Security documentation (`SECURITY.md`)
- Operations guide (`OPERATIONS.md`)

### Changed

- Default workspace changed to `~/code`
- Dry-run mode required in production unless explicitly requested
- Web access disabled by default in production
- Command validation now uses regex patterns
- Logging output is structured JSON

### Security

- Implemented kill-switch for dangerous commands
- Path validation with allow/deny lists
- Command whitelisting with regex patterns
- Network domain allowlisting
- Secret redaction in logs
- Audit trail for all actions
- Sandboxed execution option

[0.1.0]: https://github.com/ORG/jj-agent/releases/tag/v0.1.0

