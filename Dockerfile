# LiteLLM Server Boilerplate
FROM python:3.12-slim

ENV PATH="/root/.local/bin:${PATH}"
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

COPY pyproject.toml ./
COPY config.yaml ./
COPY server ./server

RUN uv sync --no-dev

ENV PORT=4000
EXPOSE 4000

CMD ["uv", "run", "litellm", "--config", "config.yaml"]
