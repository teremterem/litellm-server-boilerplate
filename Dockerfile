FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS base
WORKDIR /app

COPY pyproject.toml ./
COPY .python-version ./

RUN uv sync --no-dev

COPY . .

EXPOSE 4000
ENV PYTHONUNBUFFERED=1
ENV UV_PROJECT_ENV=.venv

CMD ["uv", "run", "litellm", "--config", "config.yaml", "--host", "0.0.0.0", "--port", "4000"]
