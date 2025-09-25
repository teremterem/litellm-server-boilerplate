# Docker Deployment Guide for LiteLLM Server

TODO Make sure this guide is fully updated

This guide explains how to deploy the LiteLLM Server using Docker and GitHub Container Registry (GHCR).

## 🐳 Docker Image

The Docker image is available in a registry:

```
ghcr.io/teremterem/litellm-server-boilerplate:latest
```

## 🚀 Quick Start

### Method 1: Using the deployment script

1. **Copy `.env.template` to `.env`:**
   ```bash
   cp .env.template .env
   ```

2. **Edit `.env` and add your API keys:**
   ```dotenv
   OPENAI_API_KEY=your-openai-api-key-here

   # Optional (see .env.template for details):
   # LITELLM_MASTER_KEY=your-master-key-here

   # More settings (see .env.template for details)
   ...
   ```

3. **Run the deployment script:**

   Run in the foreground:
   ```bash
   ./run-docker.sh
   ```

   Alternatively, to run in the background:
   ```bash
   ./deploy-docker.sh
   ```

4. **Check the logs** (if you ran in the background):
   ```bash
   docker logs -f litellm-server-boilerplate
   ```

### Method 2: Using Docker Compose

1. **Export your API keys as env vars**, as well as any other vars from `.env.template` if you would like to modify the defaults (our default Compose setup DOES NOT load env vars from `.env`):
   ```bash
   export OPENAI_API_KEY=your-openai-api-key-here

   # Optional (see .env.template for details):
   # export LITELLM_MASTER_KEY=your-master-key-here
   ```

2. **Start the service:**
   ```bash
   docker-compose up -d
   ```
   > **NOTE:** To run in the foreground, remove the `-d` flag.

3. **Check the logs:**
   ```bash
   docker-compose logs -f
   ```

### Method 3: Direct Docker run

1. **Copy `.env.template` to `.env`:**
   ```bash
   cp .env.template .env
   ```

2. **Edit `.env` and add your API keys:**
   ```dotenv
   OPENAI_API_KEY=your-openai-api-key-here

   # Optional (see .env.template for details):
   # LITELLM_MASTER_KEY=your-master-key-here

   # More settings (see .env.template for details)
   ...
   ```

3. **Run the container:**
   ```bash
   docker run -d \
     --name litellm-server-boilerplate \
     -p 4000:4000 \
     --env-file .env \
     --restart unless-stopped \
     ghcr.io/teremterem/litellm-server-boilerplate:latest
   ```

   > **NOTE:** To run in the foreground, remove the `-d` flag.

   > **NOTE:** You can also supply the environment variables individually via the `-e` parameter, instead of `--env-file .env`

4. **Check the logs:**
   ```bash
   docker logs -f litellm-server-boilerplate
   ```

## 📊 Monitoring

### Check container status:
```bash
docker ps | grep litellm-server-boilerplate
```

### Monitor resource usage:
```bash
docker stats litellm-server-boilerplate
```

## 🛑 Stopping and Cleanup

### Stop the container:
```bash
docker stop litellm-server-boilerplate
```

### Remove the container:
```bash
docker rm litellm-server-boilerplate
```

> **NOTE:** `./stop-docker.sh` can be used to both stop and remove the container in one go.

### Using Docker Compose:
```bash
docker-compose down
```

## 🏥 Health Check

The container includes a health check endpoint:

```bash
curl http://localhost:4000/health
```

## 🏗️ Building from Source

If you need to build the image yourself.

### Direct Docker build

1. First build the image:
   ```bash
   docker build -t litellm-server-boilerplate .
   ```

2. Then run the container:
   ```bash
   docker run -d \
     --name litellm-server-boilerplate \
     -p 4000:4000 \
     --env-file .env \
     --restart unless-stopped \
     litellm-server-boilerplate
   ```
   > **NOTE:** To run in the foreground, remove the `-d` flag.

### Docker Compose build

Build and run, but overlay with the dev version of Compose setup:
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build
```

This will also map the current directory to the container.

> **NOTE:** To run in the foreground, remove the `-d` flag.

> **NOTE:** The dev version of the Compose setup DOES use the `.env` file, so you will need to set up your environment variables in `.env`

## 🔧 Troubleshooting

### Container won't start
1. Check if port 4000 is available: `lsof -i :4000`
2. Verify environment variables are set correctly
3. Check container logs: `docker logs -f litellm-server-boilerplate`

### Authentication issues
1. Verify your API keys are valid and have sufficient credits

### Performance issues
1. Ensure sufficient memory is available (recommended: 2GB+)
2. Check network connectivity to the APIs

## 🔐 Security Notes

- Keep your API keys secure and never commit them to version control
- Use environment variables or Docker secrets for sensitive data
- Consider running the container in a restricted network environment
- Regularly update the image to get security patches
