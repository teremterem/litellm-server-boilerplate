# Publishing LiteLLM Server to GHCR (Maintainer's Guide)

This guide is intended for the maintainers of this LiteLLM Server repository to build and publish the Docker image to GitHub Container Registry (GHCR). **If you are simply looking to use the Docker image, see [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) instead.**

## Prerequisites

- A GitHub [Personal Access Token (PAT)](https://github.com/settings/tokens) with the `write:packages` scope
- Docker installed on your machine
- Multi-arch `buildx` enabled in Docker (see [Docker documentation](https://docs.docker.com/build/install-buildx/))

## Steps

1. **Login to GHCR:**

```bash
echo <YOUR_GITHUB_PAT> | docker login ghcr.io -u <YOUR_GITHUB_USERNAME> --password-stdin
```

2. **Build the Docker image and push it to GHCR:**

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t ghcr.io/teremterem/litellm-server-boilerplate:<VERSION> \
  -t ghcr.io/teremterem/litellm-server-boilerplate:latest \
  --push .
```
