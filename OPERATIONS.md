# Operations Guide

## Installation

### pipx (Recommended)

```bash
pipx install jj-agent
```

### Docker

```bash
docker pull ghcr.io/ORG/jj-agent:latest
```

### System Package

```bash
pip install jj-agent
```

## Configuration

### Environment Variables

Create `/etc/jj-agent/jj.env`:

```bash
JJ_ENV=production
JJ_PROD_STRICT=1
OPENAI_API_KEY=sk-your-key
JJ_RUNTIME=localsafe
JJ_ALLOW_WEB=0
```

### Capabilities File

Production requires `capabilities.prod.yaml` in the agent directory.

## Systemd Service

### Installation

```bash
# Copy service file
sudo cp jj-agent.service /etc/systemd/system/

# Copy environment file
sudo mkdir -p /etc/jj-agent
sudo cp jj.env /etc/jj-agent/

# Create user
sudo useradd -r -s /bin/false jj

# Reload systemd
sudo systemctl daemon-reload

# Enable and start
sudo systemctl enable jj-agent
sudo systemctl start jj-agent
```

### Management

```bash
# Status
sudo systemctl status jj-agent

# Restart
sudo systemctl restart jj-agent

# Logs
sudo journalctl -u jj-agent -f
```

## Log Rotation

Install logrotate config:

```bash
sudo cp logrotate.conf /etc/logrotate.d/jj-agent
```

Logs are rotated daily, kept for 14 days.

## Health Checks

### Liveness

```bash
curl http://localhost:5858/healthz
```

### Readiness

```bash
curl http://localhost:5858/readyz
```

### Metrics

```bash
curl http://localhost:5858/metrics
```

## Backups

### State Directory

Backup `state/` directory regularly:

```bash
# Daily backup
tar -czf jj-state-$(date +%Y%m%d).tar.gz state/
```

### Configuration

Backup configuration files:
- `/etc/jj-agent/jj.env`
- `capabilities.prod.yaml`

## Monitoring

### Metrics Endpoint

Query metrics at `/metrics`:
- `jobs_started`
- `jobs_succeeded`
- `jobs_failed`
- `avg_job_time_seconds`
- `denied_actions_count`

### Audit Logs

Review audit logs:
```bash
tail -f state/*/audit.jsonl | jq
```

### Error Monitoring

Configure Sentry or OpenTelemetry:
```bash
JJ_SENTRY_DSN=https://...@sentry.io/...
# or
JJ_OTEL_ENDPOINT=http://otel-collector:4317
```

## Updating

### pipx

```bash
pipx upgrade jj-agent
```

### Docker

```bash
docker pull ghcr.io/ORG/jj-agent:latest
docker stop jj-agent
docker rm jj-agent
# Start new container
```

### System Package

```bash
pip install --upgrade jj-agent
sudo systemctl restart jj-agent
```

## Rollback

1. Stop service: `sudo systemctl stop jj-agent`
2. Install previous version
3. Restart service: `sudo systemctl start jj-agent`

## Troubleshooting

### Service Won't Start

1. Check logs: `sudo journalctl -u jj-agent`
2. Verify capabilities file exists
3. Check permissions
4. Verify API key is set

### High Memory Usage

1. Enable sandboxed runtime
2. Reduce `JJ_MAX_JOB_MINUTES`
3. Review job history

### Denied Actions

1. Check audit logs
2. Review capabilities configuration
3. Add required commands/paths to allowlist

