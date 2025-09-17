# LiteLLM Server Boilerplate

A ready-to-run LiteLLM proxy that wraps any upstream model with a custom provider forcing every
response to come back in classic Yoda-speak. The project is intentionally lightweight so it can be
forked as a starting point for self-hosted AI backends that need OpenAI-compatible chat endpoints.

## What You Get

- **uv-managed project** – dependencies, virtual environment, and tooling are orchestrated with
  [uv](https://docs.astral.sh/uv/).
- **Custom LiteLLM provider** – `server.YodaSpeakLLM` forwards calls to `openai/gpt-5` (or any
  configured target model) after appending a Yoda system prompt.
- **Streaming adapter** – generic conversion helpers turn provider-specific streaming payloads into
  `GenericStreamingChunk` instances.
- **Batteries included tooling** – pre-commit hooks for `black`, `pylint`, and common housekeeping.
- **Containerisation** – Dockerfile targeting the `ghcr.io/astral-sh/uv` base images.

## Project Layout

```
.
├── config.yaml                # LiteLLM proxy configuration
├── server/                    # All Python source code
│   ├── __init__.py
│   ├── streaming.py           # Streaming conversion utilities
│   └── yoda_llm.py            # CustomLLM subclass
├── tests/                     # Pytest-based smoke tests
├── Dockerfile
├── .env.template              # Copy to .env and fill in secrets
├── .pre-commit-config.yaml
├── .pylintrc
├── .python-version
└── pyproject.toml
```

## Prerequisites

- Python `3.11.x` (uv will respect `.python-version`)
- [uv](https://docs.astral.sh/uv/getting-started/) installed locally
- An OpenAI-compatible API key exposed as `OPENAI_API_KEY`

## Getting Started (uv)

```bash
# create the virtual environment and install deps
oùv sync  # or: UV_CACHE_DIR=.uv-cache uv sync

# activate the shell if you want (optional)
uv shell

# copy environment template and fill secrets
cp .env.template .env
```

> ℹ️ If the sandbox you are running in restricts uv from downloading Python, set
> `UV_NO_MANAGED_PYTHON=1` and ensure Python 3.11.x is available on your PATH.

### Running the Proxy (without Docker)

```bash
uv run litellm --config config.yaml --host 0.0.0.0 --port 4000
```

The proxy exposes the standard OpenAI-compatible `/v1/chat/completions` endpoint. All models resolve
to the logical alias `gpt-5-yoda` defined in `config.yaml`.

### Running Tests

```bash
uv run pytest
```

### Pre-commit Hooks

Install the hooks once and they will rely on the uv-managed tools (`uv run black`/`pylint`).

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

## Docker Workflow

### Build the Image

```bash
docker build -t ghcr.io/<owner>/litellm-server-boilerplate:latest .
```

### Publish to GitHub Container Registry

```bash
echo "<GHCR_PAT>" | docker login ghcr.io -u <owner> --password-stdin
docker push ghcr.io/<owner>/litellm-server-boilerplate:latest
```

### Run the Container

```bash
docker run --rm -p 4000:4000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e LITELLM_MASTER_KEY=${LITELLM_MASTER_KEY:-change-me} \
  ghcr.io/<owner>/litellm-server-boilerplate:latest
```

### Override Settings

Pass `LITELLM_HOST`, `LITELLM_PORT`, or swap the `target_model` in `config.yaml` to redirect traffic
at any other provider LiteLLM supports.

## Extending the Boilerplate

1. Duplicate `server/yoda_llm.py`, swap the system prompt (or alter the pre-processing logic).
2. Add new routed models to `config.yaml` by creating additional entries under `model_list`.
3. Update pre-commit or testing requirements in `pyproject.toml` and rerun `uv sync`.

## Additional Notes

- `.pylintrc` was generated with `pylint --generate-rcfile` for easy tweaking.
- The included streaming helpers attempt to normalise chunks from any provider supported by
  LiteLLM; extend `_build_generic_choices` if you encounter a bespoke payload.
- Remember to guard your `.env` file—it is intentionally ignored by git.
