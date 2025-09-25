#!/bin/bash

# Stop and remove the LiteLLM Server Docker container

set -e

# TODO Mention in the docs that the name below needs to be changed
LITELLM_SERVER_CONTAINER_NAME="${LITELLM_SERVER_CONTAINER_NAME:-litellm-server-boilerplate}"

echo "❌ Stopping LiteLLM Server..."

if docker ps -a --format 'table {{.Names}}' | grep -q "^${LITELLM_SERVER_CONTAINER_NAME}$"; then
    echo "📦 Stopping container..."
    docker stop ${LITELLM_SERVER_CONTAINER_NAME} || true
    echo "🗑️  Removing container..."
    docker rm ${LITELLM_SERVER_CONTAINER_NAME} || true
    echo "✅ ${LITELLM_SERVER_CONTAINER_NAME} stopped and removed."
else
    echo "ℹ️  No container named ${LITELLM_SERVER_CONTAINER_NAME} found."
fi
