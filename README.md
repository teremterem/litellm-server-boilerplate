# Claude Code with GPT-5

**NOTE:** Claude Code currently compains about the following problem when using certain tools: "Error: Streaming fallback triggered". We are waiting for the following LiteLLM bugfix to be merged and released to resolve this problem:
- https://github.com/BerriAI/litellm/pull/13521
- https://github.com/BerriAI/litellm/issues/13373

## Quick Start ⚡

### Prerequisites

- [OpenAI API](https://platform.openai.com/docs/api-reference) key 🔑
- [Anthropic API](https://console.anthropic.com/) key 🔑

**Why the Anthropic API key is still required**

Claude Code uses two models: a fast model (for quick actions) and a slow “smart” model. This setup only replaces the slow model with GPT‑5 via the proxy; the fast model still runs on Anthropic, hence the need for the Anthropic API key.

### Setup 🛠️

1. **Clone this repository**:
   ```bash
   git clone https://github.com/teremterem/claude-code-gpt-5.git
   cd claude-code-gpt-5
   ```

2. **Install [uv](https://docs.astral.sh/uv/)** (if you haven't already):

   **macOS/Linux:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   **macOS (using [Homebrew](https://brew.sh/)):**
   ```bash
   brew install uv
   ```

   **Windows (using PowerShell):**
   ```powershell
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

   **Windows (using Scoop):**
   ```bash
   scoop install uv
   ```

   **Alternative: pip install**
   ```bash
   pip install uv
   ```

3. **Configure Environment Variables**:
   Create a `.env` file:
   ```bash
   touch .env
   ```
   Edit `.env` and add your API keys:
   ```dotenv
   OPENAI_API_KEY=your-openai-api-key-here
   ANTHROPIC_API_KEY=your-anthropic-api-key-here
   ```

4. **Run the server**:
   ```bash
   uv run litellm --config config.yaml
   ```

### Using with Claude Code 🎮

1. **Install Claude Code** (if you haven't already):
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

2. **Connect to your proxy**:
   ```bash
   ANTHROPIC_BASE_URL=http://localhost:4000 claude
   ```

3. **That's it!** Your Claude Code client will now use GPT-5. 🎯
