# LiteLLM Server Boilerplate

A boilerplate LiteLLM proxy server that demonstrates how to create custom model routing with modified prompts. This project serves as a starting point for building your own AI solutions that can connect to OpenAI API-compatible chat interfaces.

## Features

- **Custom LLM Implementation**: Extends LiteLLM's `CustomLLM` class to add custom behavior
- **Yoda-speak Enhancement**: Automatically appends a system prompt to make responses speak like Yoda
- **Full Streaming Support**: Implements both synchronous and asynchronous streaming methods
- **Universal Stream Converter**: Handles streaming responses from any LiteLLM-supported provider
- **Docker Support**: Fully containerized with Docker and Docker Compose configurations
- **Development Tools**: Pre-commit hooks with Black and Pylint for code quality
- **uv Integration**: Modern Python package and virtual environment management

## Project Structure

```
litellm-server-boilerplate/
├── server/
│   ├── __init__.py
│   ├── yoda_llm.py              # Custom LLM implementation
│   ├── stream_converter.py       # Universal streaming converter
│   └── main.py                   # Server entry point
├── config.yaml                   # LiteLLM configuration
├── pyproject.toml                # Project dependencies and settings
├── Dockerfile                    # Docker container configuration
├── docker-compose.yml            # Docker Compose setup
├── .env.template                 # Environment variables template
├── .pre-commit-config.yaml       # Pre-commit hooks configuration
├── .pylintrc                     # Pylint configuration
├── .python-version               # Python version specification
└── README.md                     # This file
```

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (for dependency management)
- Docker (optional, for containerized deployment)
- OpenAI API key

## Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd litellm-server-boilerplate

# Install dependencies
uv sync

# Copy environment template
cp .env.template .env
```

### 2. Configure Environment

Edit `.env` file with your API keys:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (defaults provided)
LITELLM_MASTER_KEY=sk-1234
HOST=0.0.0.0
PORT=4000
```

### 3. Run the Server

#### Option A: Using uv (Recommended for development)

```bash
# Run directly with LiteLLM CLI
uv run litellm --config config.yaml --host 0.0.0.0 --port 4000

# Or use the main.py entry point
uv run python server/main.py
```

#### Option B: Using Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t litellm-yoda-server .
docker run -p 4000:4000 --env-file .env litellm-yoda-server
```

### 4. Test the Server

The server will be available at:
- API: `http://localhost:4000`
- Documentation: `http://localhost:4000/docs`
- Health check: `http://localhost:4000/health`

Test with curl:

```bash
curl -X POST "http://localhost:4000/chat/completions" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-1234" \
     -d '{
       "model": "yoda-gpt-5",
       "messages": [
         {"role": "user", "content": "Hello, how are you?"}
       ]
     }'
```

## Usage

### API Endpoints

The server provides OpenAI-compatible endpoints:

- `POST /chat/completions` - Chat completions (streaming and non-streaming)
- `GET /models` - List available models
- `GET /health` - Health check
- `GET /docs` - API documentation

### Model Configuration

The `yoda-gpt-5` model is configured in `config.yaml` to:

1. Route all requests to OpenAI's GPT-5
2. Automatically append a Yoda-speak system prompt
3. Support both streaming and non-streaming responses

### Customizing the Implementation

#### Modify the System Prompt

Edit `server/yoda_llm.py`:

```python
YODA_SYSTEM_PROMPT = (
    "Your custom system prompt here..."
)
```

#### Change the Target Model

Edit the `model_name` in `YodaLLM.__init__()`:

```python
self.model_name = "openai/gpt-4"  # or any LiteLLM-supported model
```

#### Add New Custom Models

1. Create a new class extending `CustomLLM`
2. Register it in `config.yaml`:

```yaml
model_list:
  - model_name: my-custom-model
    litellm_params:
      model: custom/my-model
      custom_llm_provider: my-provider

litellm_settings:
  custom_llm_provider:
    my-provider:
      class_name: server.my_custom_llm.MyCustomLLM
```

## Development

### Setup Development Environment

```bash
# Install with dev dependencies
uv sync

# Install pre-commit hooks
uv run pre-commit install

# Run pre-commit on all files
uv run pre-commit run --all-files
```

### Code Quality

The project uses:
- **Black**: Code formatting (119 character line length)
- **Pylint**: Code linting and quality checks
- **Pre-commit**: Automated checks before commits

Run quality checks:

```bash
# Format code
uv run black server/

# Run linting
uv run pylint server/

# Run pre-commit checks
uv run pre-commit run --all-files
```

### Testing

```bash
# Run tests (when implemented)
uv run pytest

# Run with coverage
uv run pytest --cov=server
```

## Docker Deployment

### Building the Image

```bash
# Build locally
docker build -t litellm-yoda-server .

# Build for multiple platforms
docker buildx build --platform linux/amd64,linux/arm64 -t litellm-yoda-server .
```

### Publishing to GitHub Container Registry

```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USERNAME --password-stdin

# Tag for GHCR
docker tag litellm-yoda-server ghcr.io/$GITHUB_USERNAME/litellm-server-boilerplate:latest

# Push to GHCR
docker push ghcr.io/$GITHUB_USERNAME/litellm-server-boilerplate:latest
```

### Running from GHCR

```bash
docker run -p 4000:4000 --env-file .env ghcr.io/$GITHUB_USERNAME/litellm-server-boilerplate:latest
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `LITELLM_MASTER_KEY` | LiteLLM master key for authentication | `sk-1234` |
| `HOST` | Server bind address | `0.0.0.0` |
| `PORT` | Server port | `4000` |
| `DEBUG` | Enable debug mode | `false` |
| `LOG_LEVEL` | Logging level | `INFO` |

### LiteLLM Configuration

The `config.yaml` file contains:
- Model routing definitions
- Custom provider configurations
- Budget and rate limiting settings
- CORS and security settings

## Extending the Boilerplate

This boilerplate is designed to be extended for various use cases:

1. **Custom Model Routing**: Route different models to different providers
2. **Prompt Engineering**: Modify or enhance prompts for specific use cases
3. **Authentication**: Add custom authentication logic
4. **Logging**: Implement custom logging and analytics
5. **Caching**: Add response caching for improved performance

## Troubleshooting

### Common Issues

1. **Module Import Errors**: Ensure the `server` package is properly installed with `uv sync`
2. **API Key Issues**: Verify your OpenAI API key is valid and has sufficient credits
3. **Port Conflicts**: Change the port in `.env` if 4000 is already in use
4. **Docker Build Issues**: Ensure Docker has sufficient resources allocated

### Debug Mode

Enable debug logging:

```bash
DEBUG=true LOG_LEVEL=DEBUG uv run python server/main.py
```

### Health Checks

Monitor server health:

```bash
curl http://localhost:4000/health
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run quality checks: `uv run pre-commit run --all-files`
5. Submit a pull request

## License

This project is provided as a boilerplate for educational and development purposes. Please ensure compliance with OpenAI's usage policies and terms of service when deploying to production.

## Support

For issues and questions:
1. Check the [LiteLLM documentation](https://docs.litellm.ai/)
2. Review the configuration files
3. Enable debug logging for detailed error information
