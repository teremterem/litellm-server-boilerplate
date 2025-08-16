# Claude Code with GPT-5


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
   Copy the template file to create your `.env`:
   ```bash
   cp .env.template .env
   ```
   Edit `.env` and add your API keys:
   ```dotenv
   OPENAI_API_KEY=your-openai-api-key-here
   ANTHROPIC_API_KEY=your-anthropic-api-key-here
   # Reasoning effort setting for GPT-5. Possible values: minimal, low, medium, high
   REASONING_EFFORT=low
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
   ANTHROPIC_BASE_URL=http://localhost:4000 claude --model gpt-5
   ```

3. **That's it!** Your Claude Code client will now use GPT-5. 🎯
