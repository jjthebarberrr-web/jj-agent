# Multi-stage Docker build for JJ Agent
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy source
COPY . .

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 jj && \
    mkdir -p /app /srv/jj/workspaces /var/log/jj && \
    chown -R jj:jj /app /srv/jj /var/log/jj

# Copy installed packages from builder
COPY --from=builder /root/.local /home/jj/.local
COPY --chown=jj:jj . /app

# Set PATH to include user local bin
ENV PATH=/home/jj/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5858/healthz', timeout=5)" || exit 1

USER jj

EXPOSE 5858

ENTRYPOINT ["python", "-m", "cli.main"]
CMD ["--daemon", "--listen", "0.0.0.0:5858"]

