![Claude Code with GPT-5](claude-code-gpt-5.jpeg)

This repository lets you use **Anthropic's Claude Code CLI** with **OpenAI's GPT-5** via a local LiteLLM proxy.

## Quick Start ⚡

### Prerequisites

- [OpenAI API key 🔑](https://platform.openai.com/settings/organization/api-keys)
- [Anthropic API key 🔑](https://console.anthropic.com/settings/keys) - optional (if you decide not to remap to OpenAI in certain scenarios)
- Either [uv](https://docs.astral.sh/uv/getting-started/installation/) or [Docker Desktop](https://docs.docker.com/desktop/), depending on your preferred setup method

### First time using GPT-5 via API?

If you are going to use GPT-5 via API for the first time, **OpenAI may require you to verify your identity via Persona.** You may encounter an OpenAI error asking you to “verify your organization.” To resolve this, you can go through the verification process here:
- [OpenAI developer platform - Organization settings](https://platform.openai.com/settings/organization/general)

### Setup 🛠️

1. **Clone this repository:**
   ```bash
   git clone https://github.com/teremterem/claude-code-gpt-5.git
   cd claude-code-gpt-5
   ```

2. **Configure Environment Variables:**

   Copy the template file to create your `.env`:
   ```bash
   cp .env.template .env
   ```
   Edit `.env` and add your OpenAI API key:
   ```dotenv
   OPENAI_API_KEY=your-openai-api-key-here
   # Optional: only needed if you plan to use Anthropic models
   # ANTHROPIC_API_KEY=your-anthropic-api-key-here

   # Optional (see .env.template for details):
   # LITELLM_MASTER_KEY=your-master-key-here

   # Recommended: remap Claude models to GPT‑5 variants to ensure all
   # built-in agents in Claude Code also use GPT‑5
   REMAP_CLAUDE_HAIKU_TO=gpt-5-nano-reason-minimal
   REMAP_CLAUDE_SONNET_TO=gpt-5-reason-medium
   REMAP_CLAUDE_OPUS_TO=gpt-5-reason-high

   # Some more optional settings (see .env.template for details)
   ...
   ```

3. **Run the proxy:**

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
      docker run -d \
         --name claude-code-gpt-5 \
         -p 4000:4000 \
         --env-file .env \
         --restart unless-stopped \
         ghcr.io/teremterem/claude-code-gpt-5:latest
      ```
      > **NOTE:** To run with this command in the foreground instead of the background, remove the `-d` flag.

      To see the logs, run:
      ```bash
      docker logs -f claude-code-gpt-5
      ```

      To stop and remove the container, run:
      ```bash
      ./stop-docker.sh
      ```

      > **NOTE:** The `Docker` options above will pull the latest image from `GHCR` and will ignore all your local files except `.env`. For more detailed `Docker` deployment instructions and more options (like building `Docker` image from source yourself, using `Docker Compose`, etc.), see [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)

### Using with Claude Code 🎮

1. **Install Claude Code** (if you haven't already):
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

2. **Connect to GPT-5 instead of Claude:**

   Recommended:
   ```bash
   ANTHROPIC_BASE_URL=http://localhost:4000 claude
   ```

   Optionally, you can override the default model on the CLI side with:
   ```bash
   ANTHROPIC_BASE_URL=http://localhost:4000 claude --model gpt-5-reason-medium
   ```

   > **NOTE:** The former is more desirable than the latter - relying solely on the remap env vars and not explicitly setting the model in the CLI eliminates confusion when it comes to CLI's built-in agents, which are hardwired to always use a specific Claude model and will ignore the CLI's global model choice anyway.


   If you set `LITELLM_MASTER_KEY` for the proxy (see `.env.template` for details), pass it as the Anthropic API key for the CLI:
   ```bash
   ANTHROPIC_API_KEY="<LITELLM_MASTER_KEY>" \
   ANTHROPIC_BASE_URL=http://localhost:4000 \
   claude
   ```
   > **NOTE:** In this case, if you've previously authenticated, run `claude /logout` first.

4. **That's it!** Your Claude Code client will now use the selected **GPT-5 variant(s)** with your chosen reasoning effort level(s). 🎯

### Available GPT-5 model aliases

- **GPT-5**:
   - `gpt-5-reason-minimal`
   - `gpt-5-reason-low`
   - `gpt-5-reason-medium`
   - `gpt-5-reason-high`
- **GPT-5-mini**:
   - `gpt-5-mini-reason-minimal`
   - `gpt-5-mini-reason-low`
   - `gpt-5-mini-reason-medium`
   - `gpt-5-mini-reason-high`
- **GPT-5-nano**:
   - `gpt-5-nano-reason-minimal`
   - `gpt-5-nano-reason-low`
   - `gpt-5-nano-reason-medium`
   - `gpt-5-nano-reason-high`

> **NOTE:** Generally, you can use arbitrary models from [arbitrary providers](https://docs.litellm.ai/docs/providers), but for providers other than OpenAI or Anthropic, you will need to specify the provider in the model name, e.g. `gemini/gemini-pro`, `gemini/gemini-pro-reason-disable` etc. (as well as set the respective API keys along with any other environment variables that the provider might require in your `.env` file).

## KNOWN PROBLEM

The `Web Search` tool currently does not work with this setup. You may see an error like:

```text
API Error (500 {"error":{"message":"Error calling litellm.acompletion for non-Anthropic model: litellm.BadRequestError: OpenAIException - Invalid schema for function 'web_search': 'web_search_20250305' is not valid under any of the given schemas.","type":"None","param":"None","code":"500"}}) · Retrying in 1 seconds… (attempt 1/10)
```

This is planned to be fixed soon.

> **NOTE:** The `Fetch` tool (getting web content from specific URLs) is not affected and works normally.

## P. S. You are welcome to join our [MiniAgents Discord Server 👥](https://discord.gg/ptSvVnbwKt)

## And if you like the project, please give it a Star 💫
