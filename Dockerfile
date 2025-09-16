# syntax=docker/dockerfile:1.7-labs

FROM python:3.11-slim AS base

# Install uv
RUN pip install --no-cache-dir uv

WORKDIR /app

# System deps for building some wheels (optional minimal set)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential curl git && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml README.md LICENSE .python-version config.yaml .pre-commit-config.yaml .env.template /app/
COPY server /app/server

# Install runtime + dev deps
RUN uv sync --all-extras --dev

ENV LITELLM_HOST=0.0.0.0 \
    LITELLM_PORT=8000 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uv", "run", "python", "-m", "server.main"]
