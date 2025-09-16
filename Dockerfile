# syntax=docker/dockerfile:1.6

# Use the official uv Python base image
FROM ghcr.io/astral-sh/uv:python3.11-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1

WORKDIR /app

# Copy project metadata and config first for efficient caching
COPY pyproject.toml .
COPY .python-version .
COPY .pylintrc .
COPY .pre-commit-config.yaml .
COPY config.yaml .

# Copy source
COPY server ./server

# Install runtime deps only (dev tools not needed in container)
RUN uv sync --frozen --no-dev

# Expose LiteLLM default port
EXPOSE 4000

# Run LiteLLM Proxy using our config
CMD ["uv", "run", "litellm", "--config", "config.yaml", "--host", "0.0.0.0", "--port", "4000"]

