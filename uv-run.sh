#!/bin/bash

# Run LiteLLM Server via uv

set -e
LITELLM_CONFIG="${LITELLM_CONFIG:-config.yaml}"
LITELLM_SERVER_PORT="${LITELLM_SERVER_PORT:-4000}"
echo ""
echo "🚀 Running LiteLLM Server (via uv)..."
echo "📦 Config: ${LITELLM_CONFIG}"
echo ""
uv run litellm --config "${LITELLM_CONFIG}" --port "${LITELLM_SERVER_PORT}" --host "0.0.0.0"
