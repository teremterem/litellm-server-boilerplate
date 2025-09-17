# LiteLLM Server Boilerplate

A minimal, production-ready LiteLLM Proxy boilerplate. All Python code lives in `server/`. A single custom provider (`CustomYodaLLM`) appends a Yoda-speak system message and forwards requests to `openai/gpt-5`. Streaming tokens are converted to a generic shape for broad provider compatibility.

## Features
- uv-managed Python project (deps + venv)
- Pre-commit hooks using local (uv) installs of black and pylint
- .python-version, .pylintrc (generated), black line length 119 in pyproject
- LiteLLM Proxy config routing all models to one custom provider
- Dockerized for easy deploy; instructions for GHCR publishing

## Requirements
- Python (local) managed by [uv](https://github.com/astral-sh/uv)
- An OpenAI-compatible API key in your environment

## Setup (local)
1) Install uv (if needed):
   curl -LsSf https://astral.sh/uv/install.sh | sh
2) Sync deps:
   uv sync
3) Create env file:
   cp .env.template .env
   # Fill OPENAI_API_KEY, optionally LITELLM_MASTER_KEY and PORT
4) Install pre-commit hooks (local tools via uv):
   uv run pre-commit install
   uv run pre-commit run -a

## Run LiteLLM Proxy (without Docker)
- Start server (uses `config.yaml`):
  uv run litellm --config config.yaml
- Default port is 4000 (override with `PORT` env var)

## Usage
- Non-streaming example:
  curl -s -X POST http://localhost:4000/v1/chat/completions \
    -H "Authorization: Bearer ${LITELLM_MASTER_KEY:-dummy}" \
    -H "Content-Type: application/json" \
    -d '{
      "model": "yoda",
      "messages": [
        {"role": "user", "content": "Explain recursion."}
      ]
    }'
- Streaming example (SSE-style, `stream: true`):
  curl -N -s -X POST http://localhost:4000/v1/chat/completions \
    -H "Authorization: Bearer ${LITELLM_MASTER_KEY:-dummy}" \
    -H "Content-Type: application/json" \
    -d '{
      "model": "yoda",
      "stream": true,
      "messages": [
        {"role": "user", "content": "Tell a short joke."}
      ]
    }'

Notes:
- The `yoda` alias sends to `openai/gpt-5` and appends a Yoda-speak system prompt at the end of the message list.
- The streaming converter makes best-effort to normalize chunks across providers.

## Docker
- Build image:
  docker build -t ghcr.io/OWNER/litellm-server-boilerplate:latest .
- Run container:
  docker run --rm -p 4000:4000 \
    -e OPENAI_API_KEY="$OPENAI_API_KEY" \
    -e LITELLM_MASTER_KEY="local-key" \
    -e PORT=4000 \
    ghcr.io/OWNER/litellm-server-boilerplate:latest

### Publish to GitHub Container Registry (GHCR)
- Login:
  echo "$GH_PAT" | docker login ghcr.io -u OWNER --password-stdin
- Push:
  docker push ghcr.io/OWNER/litellm-server-boilerplate:latest

Replace `OWNER` with your GitHub username or org. Your token needs `write:packages`.

## Project Layout
- pyproject.toml — uv project, black line length 119
- .python-version — Python version hint
- .pre-commit-config.yaml — runs `uv run black` and `uv run pylint` + standard hooks
- .pylintrc — generated via `pylint --generate-rcfile`
- config.yaml — LiteLLM Proxy config loading the custom provider
- server/
  - custom_yoda.py — `CustomYodaLLM` implementing `completion`, `acompletion`, `streaming`, `astreaming`
  - stream_converter.py — converts provider stream tokens to a generic chunk shape

## Development
- Lint:
  uv run pylint server
- Format:
  uv run black --line-length 119 server
- Run hooks on all files:
  uv run pre-commit run -a

## Environment
- .env.template provided. Copy to `.env` or export values before running:
  - OPENAI_API_KEY
  - LITELLM_MASTER_KEY (any non-empty value to auth to proxy)
  - PORT (default 4000)
