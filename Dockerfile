# Use Python 3.13.3 slim image
FROM python:3.13.3-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.20 /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml .python-version ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Copy application code
COPY server/ ./server/
COPY config.yaml ./

# Create non-root user
RUN useradd -m -u 1000 litellm && chown -R litellm:litellm /app
USER litellm

# Expose port
EXPOSE 4000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

# Run LiteLLM proxy
CMD ["litellm", "--config", "config.yaml", "--port", "4000", "--host", "0.0.0.0"]
