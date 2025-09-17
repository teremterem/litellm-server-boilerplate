# LiteLLM Server Boilerplate (Yoda-speak proxy)

A minimal LiteLLM Proxy boilerplate wired to a single custom provider that forwards requests to `openai/gpt-5` and appends a system message enforcing Yoda-speak. Uses `uv` for dependency and environment management, with Black + Pylint enforced via pre-commit.

## Features
- `uv`-managed Python project
- Pre-commit hooks: Black (119 cols), Pylint, and standard pre-commit-hooks
- All Python code in `server/`
- Custom provider: `server.yoda_llm:YodaLLM` (completion, acompletion, streaming, astreaming)
- Streaming adapter to normalize provider tokens to a generic chunk shape
- Dockerized, ready for GHCR publishing

## Project layout
- `server/yoda_llm.py` – Custom LiteLLM provider that appends Yoda system prompt and forwards to `openai/gpt-5`
- `server/stream_convert.py` – Converts streaming responses into generic chunks
- `config.yaml` – LiteLLM Proxy config mapping all models to the custom provider
- `.pre-commit-config.yaml` – Runs Black/Pylint via local `uv` env + basic checks
- `.pylintrc` – Baseline Pylint config (max line length 119)
- `.python-version` – Python version hint
- `pyproject.toml` – Dependencies + tool configuration
- `.env.template` – Environment variable template
- `Dockerfile` – Container setup running the LiteLLM Proxy

## Prerequisites
- Python 3.12 (see `.python-version`)
- `uv` installed
- An OpenAI API key with access to an appropriate model, exported as `OPENAI_API_KEY`

## Setup (local, no Docker)
1. Copy env template and set your key:
   - macOS/Linux: `cp .env.template .env && export $(cat .env | xargs)`
   - Or export directly: `export OPENAI_API_KEY=YOUR_KEY`
2. Install deps:
   - `uv sync --group dev`
3. (Optional) Install pre-commit hooks:
   - `uv run pre-commit install`
4. Run the LiteLLM Proxy:
   - `uv run litellm --config config.yaml --host 0.0.0.0 --port 8000`

The proxy will listen on http://localhost:8000.

## Quick test
Example OpenAI-compatible Chat Completions request:

```bash
curl -s http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "anything",
    "messages": [
      {"role": "user", "content": "Explain gravity in one sentence"}
    ]
  }'
```

Any `model` value is routed to `server.yoda_llm:YodaLLM` by `config.yaml` and forwarded to `openai/gpt-5` with a Yoda-speak system message appended.

## Docker
### Build
```bash
docker build -t litellm-yoda:latest .
```

### Run
```bash
docker run --rm -p 8000:8000 \
  -e OPENAI_API_KEY=YOUR_KEY \
  --name litellm-yoda \
  litellm-yoda:latest
```

### Publish to GitHub Container Registry (GHCR)
1. Tag the image:
```bash
docker tag litellm-yoda:latest ghcr.io/OWNER/REPO/litellm-yoda:latest
```
2. Login to GHCR (requires a PAT with `write:packages`):
```bash
docker login ghcr.io -u YOUR_GITHUB_USERNAME -p YOUR_GHCR_PAT
```
3. Push:
```bash
docker push ghcr.io/OWNER/REPO/litellm-yoda:latest
```

Replace `OWNER/REPO` and credentials as appropriate.

## Notes
- Black line length is set to 119 in both Black and Pylint configurations.
- Hooks run Black and Pylint from the local `uv` environment:
  - Black: `uv run black --line-length 119`
  - Pylint: `uv run pylint --rcfile=.pylintrc`
- `config.yaml` maps all model names (`"*"`) to the custom provider `server.yoda_llm:YodaLLM`.
