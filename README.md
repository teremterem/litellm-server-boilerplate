## LiteLLM Server Boilerplate

Opinionated starter for hosting a LiteLLM Proxy with a custom provider that forces responses in "Yoda-speak". It uses uv to manage Python, dependencies, and virtualenvs, comes with pre-commit hooks (Black, Pylint, and basic hygiene), and ships with Docker.

### Features
- **uv-managed project**: reproducible, fast installs with `uv` and `pyproject.toml`.
- **Pre-commit hooks**: run Black, Pylint, Ruff, and standard checks using local installs via `uv`.
- **Custom provider**: `server/custom_yoda_llm.py` implements a `CustomLLM` that appends a Yoda system prompt and forwards to `openai/gpt-5`.
- **Streaming conversion**: `server/streaming_utils.py` converts provider stream tokens to `GenericStreamingChunk`, best-effort across providers.
- **Config-driven**: `config.yaml` maps a single public model `yoda-gpt5` to the custom provider.
- **Dockerized**: build, run, and publish with a minimal image.

### Prerequisites
- Python `3.11` (managed via `.python-version` for pyenv users)
- `uv` installed locally. Install: `pip install uv` or follow uv docs.
- Set `OPENAI_API_KEY` in your environment or copy `.env.template` to `.env` and fill it in.

### Setup
```bash
# Install dependencies (runtime + dev)
uv sync --all-extras --dev

# (Optional) enable pre-commit
uv run pre-commit install
```

### Run the LiteLLM Proxy (without Docker)
```bash
# Starts LiteLLM Proxy with config.yaml
uv run python -m server.main
```
The proxy will listen on `http://0.0.0.0:8000`. The public model name is `yoda-gpt5`.

Example curl:
```bash
curl -s http://localhost:8000/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{
        "model": "yoda-gpt5",
        "messages": [
          {"role": "user", "content": "Explain binary trees."}
        ],
        "stream": false
      }' | jq
```

For streaming:
```bash
curl -N http://localhost:8000/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{
        "model": "yoda-gpt5",
        "messages": [
          {"role": "user", "content": "Explain binary trees."}
        ],
        "stream": true
      }'
```

### Docker
#### Build
```bash
# From repo root
docker build -t ghcr.io/<your-gh-username>/litellm-server-boilerplate:latest .
```

#### Run
```bash
# Provide your keys
docker run --rm -p 8000:8000 \
  -e OPENAI_API_KEY=sk-... \
  --name litellm-yoda \
  ghcr.io/<your-gh-username>/litellm-server-boilerplate:latest
```

#### Publish to GitHub Container Registry
```bash
# Login (one-time)
echo $GH_TOKEN | docker login ghcr.io -u <your-gh-username> --password-stdin

# Tag and push
IMAGE=ghcr.io/<your-gh-username>/litellm-server-boilerplate:latest

docker push $IMAGE
```

### Configuration
- `config.yaml` defines the `yoda-gpt5` model which uses `server/custom_yoda_llm.py:YodaLLM`.
- The custom provider appends a system message asking the model to always answer in Yoda-speak, then forwards the call to `openai/gpt-5`.
- To change the underlying target model/provider, pass `forward_model` in the request or extend the code to read from env.

### Development
- All Python code lives in `server/`.
- Formatting: Black, line length 119 (see `pyproject.toml`).
- Linting: Pylint, Ruff (lightweight checks). Configure Pylint in `.pylintrc`.

Run hooks manually:
```bash
uv run black .
uv run ruff check .
uv run pylint server
```
