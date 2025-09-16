# LiteLLM Server Boilerplate

A production-ready boilerplate for creating custom LiteLLM proxy servers with OpenAI API compatibility. This project demonstrates how to build AI solutions that can integrate with any OpenAI-compatible chat interface while implementing custom logic through LiteLLM's CustomLLM interface.

## Features

- **Custom LLM Implementation**: Extends LiteLLM's CustomLLM class to add custom processing logic
- **Streaming Support**: Full support for both synchronous and asynchronous streaming with proper token conversion
- **Provider Agnostic**: Token converter supports all LiteLLM-compatible providers (OpenAI, Anthropic, Google, Azure, etc.)
- **Production Ready**: Includes Docker configuration, pre-commit hooks, and proper Python packaging
- **Developer Friendly**: Configured with Black formatter, Pylint, and pre-commit hooks for code quality

## Example Implementation

This boilerplate includes a fun example implementation that adds "Yoda-speak" to all responses by appending a system prompt. The implementation showcases:
- Message modification before forwarding to the underlying model
- Proper handling of streaming and non-streaming requests
- Token conversion from provider-specific formats to generic streaming chunks

## Project Structure

```
litellm-server-boilerplate/
├── server/                      # Main application code
│   ├── __init__.py
│   ├── yoda_llm.py             # Custom LLM implementation
│   └── streaming_converter.py  # Universal streaming token converter
├── config.yaml                  # LiteLLM proxy configuration
├── Dockerfile                   # Container configuration
├── docker-compose.yaml         # Docker Compose setup
├── pyproject.toml              # Project dependencies and settings
├── .pre-commit-config.yaml     # Pre-commit hooks configuration
├── .python-version             # Python version specification
├── .pylintrc                   # Pylint configuration
├── .env.template               # Environment variables template
└── README.md                   # This file
```

## Quick Start

### Prerequisites

- Python 3.13.3 or higher
- uv (Python package manager)
- Docker and Docker Compose (for containerized deployment)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd litellm-server-boilerplate
   ```

2. **Install uv (if not already installed)**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Set up the Python environment**
   ```bash
   uv sync
   ```

4. **Install pre-commit hooks**
   ```bash
   uv run pre-commit install
   ```

5. **Configure environment variables**
   ```bash
   cp .env.template .env
   # Edit .env and add your OpenAI API key and other settings
   ```

6. **Run the server**
   ```bash
   uv run litellm --config config.yaml --port 4000
   ```

The server will be available at `http://localhost:4000`.

### Test the Server

You can test the server using curl:

```bash
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-master-key" \
  -d '{
    "model": "yoda-gpt",
    "messages": [{"role": "user", "content": "Hello, how are you?"}]
  }'
```

## Docker Deployment

### Build and Run with Docker Compose

1. **Build and start the container**
   ```bash
   docker-compose up --build
   ```

2. **Run in detached mode**
   ```bash
   docker-compose up -d
   ```

3. **Stop the container**
   ```bash
   docker-compose down
   ```

### Build Docker Image Manually

```bash
# Build the image
docker build -t litellm-server-boilerplate:latest .

# Run the container
docker run -p 4000:4000 \
  -e OPENAI_API_KEY=your-api-key \
  -e LITELLM_MASTER_KEY=your-master-key \
  litellm-server-boilerplate:latest
```

## Publishing to GitHub Container Registry

1. **Authenticate with GitHub Container Registry**
   ```bash
   echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
   ```

2. **Tag the image**
   ```bash
   docker tag litellm-server-boilerplate:latest ghcr.io/USERNAME/litellm-server-boilerplate:latest
   ```

3. **Push the image**
   ```bash
   docker push ghcr.io/USERNAME/litellm-server-boilerplate:latest
   ```

## Development

### Code Quality

This project uses several tools to maintain code quality:

- **Black**: Automatic code formatting (line length: 119)
- **Pylint**: Static code analysis
- **Pre-commit**: Runs checks before each commit

Run formatting manually:
```bash
uv run black server/
```

Run linting manually:
```bash
uv run pylint server/
```

### Customizing the Implementation

To create your own custom LLM implementation:

1. **Modify `server/yoda_llm.py`**:
   - Change the class name and implementation
   - Update the four required methods: `completion`, `acompletion`, `streaming`, `astreaming`
   - Implement your custom logic for message processing

2. **Update `config.yaml`**:
   - Change the model name and custom_llm_provider path
   - Adjust router settings as needed

3. **Modify streaming converter if needed**:
   - The `streaming_converter.py` handles token conversion for all providers
   - Extend it if you need support for additional provider formats

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for forwarding requests | Required |
| `LITELLM_MASTER_KEY` | Master key for authenticating with the proxy | Required |
| `LITELLM_BASE_URL` | Base URL for the LiteLLM server | `http://localhost:4000` |
| `DATABASE_URL` | Optional database URL for persistence | None |
| `LITELLM_VERBOSE` | Enable verbose logging | `false` |
| `LOG_RAW_REQUESTS` | Log raw request/response data | `false` |
| `PORT` | Server port | `4000` |

## API Endpoints

The server provides OpenAI-compatible endpoints:

- `POST /v1/chat/completions` - Chat completions (streaming and non-streaming)
- `GET /health` - Health check endpoint
- `GET /` - LiteLLM UI dashboard

## Use Cases

This boilerplate is ideal for:

- Creating custom AI gateways with specialized processing logic
- Building middleware that modifies or enhances LLM responses
- Implementing custom routing, filtering, or transformation logic
- Developing AI solutions that need OpenAI API compatibility
- Testing and development of LLM applications

## Contributing

Feel free to submit issues and enhancement requests!

## License

[Add your license here]
