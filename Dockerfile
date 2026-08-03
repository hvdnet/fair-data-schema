# Multi-stage Dockerfile for FAIR Data JSON Schema API Server

FROM python:3.12-slim as builder

WORKDIR /app

# Install uv for fast dependency resolution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uv

# Copy project definition files
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
COPY schemas ./schemas
COPY cv ./cv

# Install package with API optional dependencies
RUN /uv pip install --system --no-cache .[api]

# --- Production Runtime ---
FROM python:3.12-slim as runtime

WORKDIR /app

# Copy installed site-packages and binaries from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    HOST=0.0.0.0

EXPOSE 8000

# Default command starts the API server via CLI
CMD ["fair-data-schema", "serve", "--host", "0.0.0.0", "--port", "8000"]
