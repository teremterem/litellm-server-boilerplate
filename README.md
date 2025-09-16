# LiteLLM Server Boilerplate (Yoda-speak Proxy)

This repository is a minimal, production-friendly boilerplate for running a [LiteLLM](https://github.com/BerriAI/litellm) Proxy with a custom provider. All inbound requests are routed through a custom `CustomLLM` that appends a Yoda-speak system prompt and then forwards to an underlying model (`openai/gpt-5` by default).

It uses:
- `uv` for dependency management and virtualenvs
- `pre-commit` for Black + Pylint and standard sanity checks
- A Dockerfile to containerize the proxy

## Features
- Custom LiteLLM provider (`server/custom_provider.py`) that:
  - Appends a Yoda-speak system prompt
  - Supports `completion`, `acompletion`, `streaming`, `astreaming`
  - Converts provider streaming tokens to a generic format (`server/streaming_utils.py`)
- All Python code under `server/`
- Configurable via `config.yaml`
- `.python-version` (3.11), `.pylintrc`, and Black line length set to 119

## Prerequisites
- Python 3.11 (see `.python-version`)
- `uv` installed (https://docs.astral.sh/uv/)
- An API key for your provider (e.g., `OPENAI_API_KEY`)

## Setup
1. Create a `.env` file from the template and set your keys:
   ```bash
   cp .env.template .env
   # edit .env and set OPENAI_API_KEY=...
   ```

2. Install dependencies (creates a local virtualenv managed by uv):
   ```bash
   uv sync --dev
   ```

3. (Optional) Enable pre-commit hooks:
   ```bash
   uv run pre-commit install
   uv run pre-commit run -a
   ```

## Running the LiteLLM Proxy (without Docker)
You can run the proxy directly via the CLI entrypoint provided by LiteLLM. This project’s `config.yaml` routes all requests through the custom provider:

```bash
# Environment (from .env)
export $(grep -v '^#' .env | xargs -I{} echo {})

# Start the proxy
uv run litellm --config config.yaml --host 0.0.0.0 --port 4000
```

- Default logical model name: `yoda-proxy` (see `config.yaml`).
- Underlying provider/model: `openai/gpt-5` by default but you can change it in `config.yaml`.

Example curl (OpenAI-compatible chat completions):
```bash
curl -s -X POST "http://localhost:4000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "yoda-proxy",
    "messages": [
      {"role": "user", "content": "Explain recursion in one sentence."}
    ]
  }'
```

## Docker
### Build the image
```bash
# Build (tag as you wish)
docker build -t ghcr.io/<your-username>/litellm-yoda-proxy:0.1.0 .
```

### Publish to GitHub Container Registry
1. Login:
   ```bash
   echo "$GITHUB_TOKEN" | docker login ghcr.io -u <your-username> --password-stdin
   ```
2. Push:
   ```bash
   docker push ghcr.io/<your-username>/litellm-yoda-proxy:0.1.0
   ```

### Run the container
```bash
# Provide your provider key as env vars
# OPENAI_API_KEY is needed for the default underlying model

docker run --rm -p 4000:4000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  ghcr.io/<your-username>/litellm-yoda-proxy:0.1.0
```

Then hit `http://localhost:4000/v1/chat/completions` as shown above.

## How it Works
- `server/custom_provider.py`: Implements `YodaSpeakLLM`, a subclass of LiteLLM’s `CustomLLM` with four methods:
  - `completion` and `acompletion` forward to the underlying model after appending a Yoda system prompt.
  - `streaming` and `astreaming` forward streaming responses and convert provider-specific tokens into a generic shape using `server/streaming_utils.py`.
- `server/streaming_utils.py`: Best-effort conversion to a GenericStreamingChunk-like dict. It handles common patterns from OpenAI-like and Anthropic-like streams and falls back to generic fields when needed. This allows the Proxy to forward streaming data in a provider-agnostic way.
- `config.yaml`: Declares a logical model `yoda-proxy` that uses our custom provider class `server.custom_provider:YodaSpeakLLM`. All inbound model names are routed to this logical model via the simple router definition.

## Notes and Customization
- To change the underlying model/provider, edit `config.yaml` under `model_list[0].litellm_params.model`.
- The Yoda prompt can be tweaked in `server/custom_provider.py` (`YODA_SYSTEM_PROMPT`).
- This boilerplate is intentionally minimal and meant to be adapted to your provider(s) of choice.

## Linting & Formatting
- Black (line length 119) and Pylint are configured via `pyproject.toml` and `.pylintrc`.
- Pre-commit hooks are configured to use the local environment’s `black` and `pylint` (installed via `uv`).

## Troubleshooting
- If streaming conversion misses a provider format, extend the heuristics in `server/streaming_utils.py`.
- If LiteLLM cannot locate the custom provider, confirm the import path `server.custom_provider:YodaSpeakLLM` in `config.yaml` and ensure the `server` package is present in the working directory.
- Ensure environment variables (e.g., `OPENAI_API_KEY`) are present both locally and in Docker via `-e` flags or env files.

