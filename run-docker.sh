#!/bin/bash

# Run LiteLLM Server Docker container in the foreground
# This script pulls the Docker image from a registry and runs it in the foreground

set -e

# TODO Mention in the docs that the defaults below need to be changed
LITELLM_SERVER_DOCKER_IMAGE="${LITELLM_SERVER_DOCKER_IMAGE:-ghcr.io/teremterem/litellm-server-boilerplate:latest}"
LITELLM_SERVER_CONTAINER_NAME="${LITELLM_SERVER_CONTAINER_NAME:-litellm-server-boilerplate}"
LITELLM_SERVER_PORT="${LITELLM_SERVER_PORT:-4000}"

echo "🚀 Running LiteLLM Server..."

# Stop and remove existing container if it exists
if docker ps -a --format 'table {{.Names}}' | grep -q "^${LITELLM_SERVER_CONTAINER_NAME}$"; then
    echo "📦 Stopping existing container..."
    docker stop ${LITELLM_SERVER_CONTAINER_NAME} || true
    docker rm ${LITELLM_SERVER_CONTAINER_NAME} || true
fi

# Pull the latest image
echo "⬇️  Pulling latest image from the registry..."
docker pull ${LITELLM_SERVER_DOCKER_IMAGE}

# Run the container
echo ""
echo "▶️  Starting container..."
echo ""
docker run \
    --name ${LITELLM_SERVER_CONTAINER_NAME} \
    -p ${LITELLM_SERVER_PORT}:4000 \
    --env-file .env \
    --restart unless-stopped \
    ${LITELLM_SERVER_DOCKER_IMAGE}
