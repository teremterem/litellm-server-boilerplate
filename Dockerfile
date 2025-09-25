FROM python:3.13-slim

# TODO Mention in the docs that the values below need to be changed
LABEL org.opencontainers.image.source=https://github.com/teremterem/litellm-server-boilerplate \
      org.opencontainers.image.description="LiteLLM Server Boilerplate" \
      org.opencontainers.image.licenses=MIT

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

COPY .python-version ./
COPY uv.lock ./
COPY pyproject.toml ./

# Install Python dependencies using uv (before copying other project files,
# so this layer is rebuilt less often during development)
RUN uv sync --frozen

# Set up the environment variable defaults.
# NOTE: This works because python_dotenv does NOT override variables that
# already exist in the environment; it only loads missing ones from the .env
# file.
COPY .env.template .env
# TODO This would break if LITELLM_MODE env var is set to a value other than
#  DEV (although, when it is not set, it is DEV by default). What would be the
#  best way to adapt to the approach taken by litellm ?

# Copy all the project files
COPY . .

# Expose port 4000 (default LiteLLM proxy port)
EXPOSE 4000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f -H "Authorization: Bearer ${LITELLM_MASTER_KEY}" http://localhost:4000/health || exit 1

# Default command to run the LiteLLM proxy
CMD ["uv", "run", "litellm", "--config", "config.yaml", "--port", "4000", "--host", "0.0.0.0"]
