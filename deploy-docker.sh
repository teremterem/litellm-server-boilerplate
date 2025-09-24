#!/bin/bash

# Deploy claude-code-gpt-5 Docker container
# This script pulls and runs the Docker image from GHCR

set -e

PROXY_DOCKER_IMAGE="${PROXY_DOCKER_IMAGE:-ghcr.io/teremterem/claude-code-gpt-5:latest}"
PROXY_CONTAINER_NAME="${PROXY_CONTAINER_NAME:-claude-code-gpt-5}"
PROXY_PORT="${PROXY_PORT:-4000}"

echo "🚀 Deploying Claude Code GPT-5 Proxy..."

# Stop and remove existing container if it exists
if docker ps -a --format 'table {{.Names}}' | grep -q "^${PROXY_CONTAINER_NAME}$"; then
    echo "📦 Stopping existing container..."
    docker stop ${PROXY_CONTAINER_NAME} || true
    docker rm ${PROXY_CONTAINER_NAME} || true
fi

# Pull the latest image
echo "⬇️  Pulling latest image from GHCR..."
docker pull ${PROXY_DOCKER_IMAGE}

# Run the container
echo "▶️  Starting container..."
docker run -d \
    --name ${PROXY_CONTAINER_NAME} \
    -p ${PROXY_PORT}:4000 \
    --env-file .env \
    --restart unless-stopped \
    ${PROXY_DOCKER_IMAGE}

echo "✅ Claude Code GPT-5 Proxy deployed successfully!"
echo "🔗 Proxy URL: http://localhost:${PROXY_PORT}"
echo "📊 Health check: curl http://localhost:${PROXY_PORT}/health"
echo ""
echo "📝 Usage with Claude Code:"
echo ""
echo "   ANTHROPIC_BASE_URL=http://localhost:${PROXY_PORT} claude"
echo ""
echo "      OR"
echo ""
echo "   ANTHROPIC_API_KEY=\"<LITELLM_MASTER_KEY>\" \\"
echo "   ANTHROPIC_BASE_URL=http://localhost:${PROXY_PORT} \\"
echo "   claude"
echo ""
echo "❌ To stop and remove container: ./stop-docker.sh"
echo "🛑 To stop container: docker stop ${PROXY_CONTAINER_NAME}"
echo "🗑️  To remove container: docker rm ${PROXY_CONTAINER_NAME}"
echo "🔍 To view logs: docker logs -f ${PROXY_CONTAINER_NAME}"
