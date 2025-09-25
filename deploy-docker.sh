#!/bin/bash

# Deploy LiteLLM Server Docker container
# This script pulls the Docker image from a registry and runs it in the background

set -e

# TODO Mention in the docs that the defaults below need to be changed
LITELLM_SERVER_DOCKER_IMAGE="${LITELLM_SERVER_DOCKER_IMAGE:-ghcr.io/teremterem/litellm-server-boilerplate:latest}"
LITELLM_SERVER_CONTAINER_NAME="${LITELLM_SERVER_CONTAINER_NAME:-litellm-server-boilerplate}"
LITELLM_SERVER_PORT="${LITELLM_SERVER_PORT:-4000}"

echo "🚀 Deploying LiteLLM Server..."

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
echo "▶️  Starting container..."
docker run -d \
    --name ${LITELLM_SERVER_CONTAINER_NAME} \
    -p ${LITELLM_SERVER_PORT}:4000 \
    --env-file .env \
    --restart unless-stopped \
    ${LITELLM_SERVER_DOCKER_IMAGE}

echo "✅ LiteLLM Server deployed successfully!"
echo "🔗 Server URL: http://localhost:${LITELLM_SERVER_PORT}"
echo "📊 Health check: curl http://localhost:${LITELLM_SERVER_PORT}/health"
echo ""
echo "❌ To stop and remove container: ./stop-docker.sh"
echo "🛑 To stop container: docker stop ${LITELLM_SERVER_CONTAINER_NAME}"
echo "🗑️  To remove container: docker rm ${LITELLM_SERVER_CONTAINER_NAME}"
echo "🔍 To view logs: docker logs -f ${LITELLM_SERVER_CONTAINER_NAME}"
