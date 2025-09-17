FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Copy dependency files first for better Docker layer caching
COPY pyproject.toml ./
COPY uv.lock ./
COPY .python-version ./

# Install Python dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY server/ server/
COPY config.yaml ./
COPY .env.template ./

# Expose the port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=8000
ENV PYTHONPATH=/app

# Run the application
CMD ["uv", "run", "python", "server/main.py"]
