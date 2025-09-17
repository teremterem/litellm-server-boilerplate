# LiteLLM Server Boilerplate

A production-ready boilerplate for hosting custom AI solutions with an OpenAI-compatible API interface using LiteLLM Proxy. This project demonstrates how to create a custom LLM implementation that modifies requests before forwarding them to any LiteLLM-supported provider.

## Features

- **Custom LLM Implementation**: Subclass of `CustomLLM` that intercepts and modifies requests
- **Yoda-speak Demo**: Example implementation that adds a Yoda-speak system prompt to all requests
- **Multi-provider Stream Conversion**: Robust stream converter supporting multiple LLM providers (OpenAI, Anthropic, Cohere, Google, etc.)
- **Production Ready**: Includes Docker support, pre-commit hooks, and proper Python packaging with `uv`
- **OpenAI API Compatible**: Works with any OpenAI-compatible client or web interface
- **Type Safety**: Full type hints and linting with Black and Pylint

## Project Structure

```
litellm-server-boilerplate/
├── server/                  # Main application code
│   ├── __init__.py
│   ├── main.py             # Server entry point
│   ├── yoda_model.py       # Custom LLM implementation
│   └── stream_converter.py # Multi-provider stream conversion
├── config.yaml             # LiteLLM proxy configuration
├── pyproject.toml          # Python project configuration
├── .python-version         # Python version specification
├── .pylintrc              # Pylint configuration
├── .pre-commit-config.yaml # Pre-commit hooks
├── Dockerfile             # Docker configuration
├── .dockerignore
├── .env.template          # Environment variables template
└── README.md
```

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) for dependency management
- Docker (optional, for containerized deployment)
- OpenAI API key (or API key for your chosen provider)

## Quick Start

### Local Development

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd litellm-server-boilerplate
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.template .env
   # Edit .env and add your OpenAI API key
   ```

3. **Install dependencies with uv**:
   ```bash
   uv sync
   ```

4. **Install pre-commit hooks**:
   ```bash
   uv run pre-commit install
   ```

5. **Run the server**:
   ```bash
   uv run python -m server.main
   ```

   The server will start on `http://localhost:8000`

### Using Docker

1. **Build the Docker image**:
   ```bash
   docker build -t litellm-server-boilerplate:latest .
   ```

2. **Run the container**:
   ```bash
   docker run -d \
     --name litellm-server \
     -p 8000:8000 \
     -e OPENAI_API_KEY=your-api-key-here \
     -e LITELLM_MASTER_KEY=your-master-key \
     litellm-server-boilerplate:latest
   ```

## Publishing to GitHub Container Registry

1. **Login to GitHub Container Registry**:
   ```bash
   echo $GITHUB_TOKEN | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
   ```

2. **Tag the image**:
   ```bash
   docker tag litellm-server-boilerplate:latest ghcr.io/YOUR_GITHUB_USERNAME/litellm-server-boilerplate:latest
   ```

3. **Push the image**:
   ```bash
   docker push ghcr.io/YOUR_GITHUB_USERNAME/litellm-server-boilerplate:latest
   ```

## API Usage

The server provides an OpenAI-compatible API. You can use it with any OpenAI client:

### Using curl

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-master-key" \
  -d '{
    "model": "yoda-gpt",
    "messages": [
      {"role": "user", "content": "What is the meaning of life?"}
    ]
  }'
```

### Using OpenAI Python SDK

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-master-key",
    base_url="http://localhost:8000/v1"
)

response = client.chat.completions.create(
    model="yoda-gpt",
    messages=[
        {"role": "user", "content": "What is the meaning of life?"}
    ]
)

print(response.choices[0].message.content)
```

### Streaming Example

```python
stream = client.chat.completions.create(
    model="yoda-gpt",
    messages=[
        {"role": "user", "content": "Tell me a story"}
    ],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

## Customization Guide

### Creating Your Own Custom Model

1. **Create a new model class** in `server/` that inherits from `CustomLLM`:

```python
from litellm.llms.custom_llm import CustomLLM

class MyCustomModel(CustomLLM):
    def completion(self, model, messages, **kwargs):
        # Your custom logic here
        modified_messages = self.process_messages(messages)
        return litellm.completion(
            model="your-target-model",
            messages=modified_messages,
            **kwargs
        )

    # Implement acompletion, streaming, and astreaming similarly
```

2. **Update `server/main.py`** to register your model:

```python
from server.my_custom_model import MyCustomModel

def initialize_custom_model():
    custom_model = MyCustomModel()
    litellm.custom_provider_map = [
        {"provider": "custom", "custom_handler": custom_model, "model": "custom/my-model"}
    ]
```

3. **Update `config.yaml`** with your model configuration:

```yaml
model_list:
  - model_name: my-custom-model
    litellm_params:
      model: custom/my-model
      custom_llm_provider: custom
```

### Supporting Different Providers

The `stream_converter.py` module handles conversion between different provider formats. It supports:

- OpenAI / Azure OpenAI
- Anthropic (Claude)
- Google (Gemini) / Vertex AI
- Cohere
- Hugging Face
- And more through LiteLLM

To add support for a new provider, extend the `_convert_chunk_to_generic()` function in `stream_converter.py`.

## Development

### Running Tests

```bash
uv run pytest
```

### Code Formatting

```bash
uv run black server/
```

### Linting

```bash
uv run pylint server/
```

### Pre-commit Hooks

Pre-commit hooks automatically run Black and Pylint on commit:

```bash
uv run pre-commit run --all-files
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LITELLM_HOST` | Server host address | `0.0.0.0` |
| `LITELLM_PORT` | Server port | `8000` |
| `LITELLM_MASTER_KEY` | API authentication key | Required |
| `OPENAI_API_KEY` | OpenAI API key for forwarding | Required |
| `LITELLM_DEBUG` | Enable debug logging | `false` |
| `DATABASE_URL` | PostgreSQL URL for persistence | Optional |
| `REDIS_URL` | Redis URL for caching | Optional |

## Health Check

The server provides a health endpoint at `/health`:

```bash
curl http://localhost:8000/health
```

## Monitoring and Observability

- **Logs**: The server outputs structured logs to stdout
- **Metrics**: Available at `/metrics` endpoint when telemetry is enabled
- **Health checks**: Docker includes automatic health checking

## Production Deployment

For production deployments:

1. Use a strong `LITELLM_MASTER_KEY`
2. Enable HTTPS with a reverse proxy (nginx, Caddy, etc.)
3. Set up monitoring and alerting
4. Configure rate limiting
5. Use environment-specific configuration
6. Set up database persistence if needed

## Use Cases

This boilerplate is ideal for:

- **Content Filtering**: Add safety filters or content moderation
- **Prompt Engineering**: Inject context or instructions into requests
- **Multi-tenancy**: Route requests based on API keys or headers
- **Cost Optimization**: Route to different models based on request complexity
- **Compliance**: Add audit logging or data residency controls
- **Custom Features**: Add your own AI capabilities on top of existing models

## Troubleshooting

### Common Issues

1. **Module not found errors**: Ensure you're running with `uv run` or activate the virtual environment
2. **Connection refused**: Check that the server is running and ports are correct
3. **Authentication errors**: Verify your API keys in the `.env` file
4. **Stream conversion issues**: Check the logs for provider-specific error messages

### Debug Mode

Enable debug logging for more detailed output:

```bash
LITELLM_DEBUG=true uv run python -m server.main
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is provided as a boilerplate for creating custom LiteLLM implementations. You are free to use, modify, and distribute it according to your needs.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Acknowledgments

Built with [LiteLLM](https://github.com/BerriAI/litellm) - a powerful library for working with multiple LLM providers through a unified interface.
