# LiteLLM Server Boilerplate

TODO Short description

## Quick Start ⚡

### Prerequisites

- Either [uv](https://docs.astral.sh/uv/getting-started/installation/) or [Docker Desktop](https://docs.docker.com/desktop/), depending on your preferred setup method

### Setup 🛠️

TODO Adapt this section to the fact that this is a repo template and not just a ready-to-use server

1. **Clone this repository:**
   ```bash
   git clone https://github.com/teremterem/litellm-server-boilerplate.git
   cd litellm-server-boilerplate
   ```

2. **Configure Environment Variables:**

   Copy the template file to create your `.env`:
   ```bash
   cp .env.template .env
   ```
   Edit `.env` and add your OpenAI API key:
   ```dotenv
   # OPTIONAL BUT RECOMMENDED: Authentication for the server. Set a strong random
   # key to require clients to authenticate to the LiteLLM proxy. When set,
   # clients must present this key as their API key when calling the server.
   #LITELLM_MASTER_KEY=

   # For internal use by your agents.
   #OPENAI_API_KEY=
   #ANTHROPIC_API_KEY=
   # ... (any other providers)

   # More optional settings (see .env.template for details)
   ...
   ```

3. **Run the server:**

   1) **EITHER via `uv`** (make sure to install [uv](https://docs.astral.sh/uv/getting-started/installation/) first):

      **OPTION 1:** Use a script for `uv`:
      ```bash
      ./uv-run.sh
      ```

      **OPTION 2:** Run via a direct `uv` command:
      ```bash
      uv run litellm --config config.yaml
      ```

   2) **OR via `Docker`** (make sure to install [Docker Desktop](https://docs.docker.com/desktop/install/mac-install/) first):

      **OPTION 3:** Run `Docker` in the foreground:
      ```bash
      ./run-docker.sh
      ```

      **OPTION 4:** Run `Docker` in the background:
      ```bash
      ./deploy-docker.sh
      ```

      **OPTION 5:** Run `Docker` via a direct command:
      ```bash
      # TODO Mention that the name and the image below need to be changed
      docker run -d \
         --name litellm-server-boilerplate \
         -p 4000:4000 \
         --env-file .env \
         --restart unless-stopped \
         ghcr.io/teremterem/litellm-server-boilerplate:latest
      ```
      > **NOTE:** To run with this command in the foreground instead of the background, remove the `-d` flag.

      To see the logs, run:
      ```bash
      docker logs -f litellm-server-boilerplate
      ```

      To stop and remove the container, run:
      ```bash
      ./stop-docker.sh
      ```

      > **NOTE:** The `Docker` options above will pull the latest image from a registry and will ignore all your local files except `.env`. For more detailed `Docker` deployment instructions and more options (like building `Docker` image from source yourself, using `Docker Compose`, etc.), see [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)

## 📝 Architecture

```
OpenAI/Anthropic API compatible clients (LibreChat etc.)
 ↓
LiteLLM Server (Port 4000)
 ↓
 Your custom agents
```

## P. S. You are welcome to join our [MiniAgents Discord Server 👥](https://discord.gg/ptSvVnbwKt)

## And if you like the project, please give it a Star 💫
