# LiteLLM Server Boilerplate

A comprehensive boilerplate project for creating custom LiteLLM proxy servers. This project demonstrates how to build a custom LLM proxy that forwards requests to any LiteLLM-supported provider while applying custom processing, transformations, or prompting techniques.

## Features

- 🔧 **Custom LLM Implementation**: Subclass of `CustomLLM` with all four required methods (`completion`, `acompletion`, `streaming`, `astreaming`)
- 🎭 **Yoda-style Responses**: Example implementation that adds Yoda-speak system prompts to all requests
- 🌊 **Stream Processing**: Universal stream converter that works with any LiteLLM-supported provider
- 🐍 **Modern Python**: Uses `uv` for dependency management and virtual environments
- 🔍 **Code Quality**: Pre-commit hooks with Black, Pylint, and standard checks
- 🐳 **Docker Ready**: Complete Docker and Docker Compose setup
- 📊 **Health Checks**: Built-in health monitoring for production deployments
- 🔑 **Secure**: Environment-based configuration with API key management

## Project Structure

```
litellm-server-boilerplate/
├── server/
│   ├── __init__.py
│   ├── main.py              # Server entry point
│   ├── yoda_llm.py          # Custom LLM implementation
│   └── stream_converter.py  # Universal stream conversion utility
├── config.yaml              # LiteLLM configuration
├── pyproject.toml           # Project dependencies and configuration
├── .python-version          # Python version specification
├── .pylintrc               # Pylint configuration
├── .pre-commit-config.yaml # Pre-commit hooks configuration
├── .env.template           # Environment variables template
├── Dockerfile              # Docker container configuration
├── docker-compose.yml      # Docker Compose setup
└── README.md              # This file
```

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- OpenAI API key
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd litellm-server-boilerplate
   ```

2. **Install dependencies**:
   ```bash
   uv sync --dev
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.template .env
   # Edit .env with your actual API keys
   ```

4. **Install pre-commit hooks**:
   ```bash
   uv run pre-commit install
   ```

### Configuration

Edit `.env` with your configuration:

```env
# OpenAI API Key for the proxy server
OPENAI_API_KEY=your_openai_api_key_here

# LiteLLM Configuration
LITELLM_MASTER_KEY=your_master_key_here
LITELLM_LOG_LEVEL=INFO

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

## Usage

### Running Without Docker

```bash
# Start the server
uv run python server/main.py
```

The server will start on `http://localhost:8000`.

### Running with Docker

1. **Build the Docker image**:
   ```bash
   docker build -t litellm-yoda-server .
   ```

2. **Run with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

3. **Or run the container directly**:
   ```bash
   docker run -d \
     --name litellm-yoda-server \
     -p 8000:8000 \
     -e OPENAI_API_KEY=your_api_key \
     -e LITELLM_MASTER_KEY=your_master_key \
     litellm-yoda-server
   ```

### Publishing to GitHub Container Registry

1. **Build and tag the image**:
   ```bash
   docker build -t ghcr.io/yourusername/litellm-yoda-server:latest .
   ```

2. **Login to GitHub Container Registry**:
   ```bash
   echo $GITHUB_TOKEN | docker login ghcr.io -u yourusername --password-stdin
   ```

3. **Push the image**:
   ```bash
   docker push ghcr.io/yourusername/litellm-yoda-server:latest
   ```

### Testing the Server

1. **Health Check**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Chat Completion**:
   ```bash
   curl -X POST http://localhost:8000/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your_master_key" \
     -d '{
       "model": "yoda-gpt-5",
       "messages": [{"role": "user", "content": "Hello, how are you?"}],
       "stream": false
     }'
   ```

3. **Streaming Chat**:
   ```bash
   curl -X POST http://localhost:8000/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your_master_key" \
     -d '{
       "model": "yoda-gpt-5",
       "messages": [{"role": "user", "content": "Tell me a story"}],
       "stream": true
     }'
   ```

## Development

### Code Quality

The project uses several tools to maintain code quality:

- **Black**: Code formatting (119 character line length)
- **Pylint**: Code linting and static analysis
- **Pre-commit**: Automated code quality checks on commit

### Running Linters Manually

```bash
# Format code with Black
uv run black server/

# Run Pylint
uv run pylint server/

# Run all pre-commit hooks
uv run pre-commit run --all-files
```

### Project Architecture

#### Custom LLM Implementation

The `YodaLLM` class in `server/yoda_llm.py` demonstrates how to:

1. **Intercept requests**: Modify messages before forwarding
2. **Forward to providers**: Send requests to any LiteLLM-supported provider
3. **Process responses**: Transform responses before returning
4. **Handle streaming**: Convert provider streams to standard formats

#### Stream Conversion

The `stream_converter.py` module provides universal stream conversion utilities that:

- Convert `ModelResponseStream` to `GenericStreamingChunk`
- Handle responses from any LiteLLM-supported provider
- Provide both sync and async conversion functions
- Include error handling and fallback mechanisms

### Customization

To create your own custom LLM proxy:

1. **Modify the LLM class**: Edit `server/yoda_llm.py` to implement your custom logic
2. **Update configuration**: Modify `config.yaml` to point to your custom class
3. **Adjust prompts**: Change the system prompts or message processing logic
4. **Add new providers**: Configure different target models in the config

### Example Custom Implementation

```python
class MyCustomLLM(CustomLLM):
    def __init__(self):
        super().__init__()
        self.model_name = "my-custom-model"
        self.target_model = "anthropic/claude-3-sonnet"  # Any LiteLLM provider

    def completion(self, model, messages, **kwargs):
        # Add your custom logic here
        modified_messages = self._add_custom_processing(messages)
        return litellm.completion(
            model=self.target_model,
            messages=modified_messages,
            **kwargs
        )
```

## Deployment

### Production Considerations

- Use environment variables for all sensitive configuration
- Set up proper logging and monitoring
- Configure rate limiting and authentication
- Use a reverse proxy (nginx) for SSL termination
- Set up health checks and auto-restart policies

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `LITELLM_MASTER_KEY` | Master key for proxy access | Required |
| `LITELLM_LOG_LEVEL` | Logging level | INFO |
| `HOST` | Server bind address | 0.0.0.0 |
| `PORT` | Server port | 8000 |

## Troubleshooting

### Common Issues

1. **ImportError with LiteLLM**: Ensure all dependencies are installed with `uv sync`
2. **Stream conversion errors**: Check the stream converter logs for provider-specific issues
3. **Authentication errors**: Verify your API keys are correctly set in the environment

### Debugging

Enable verbose logging by setting:
```env
LITELLM_LOG_LEVEL=DEBUG
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the linters: `uv run pre-commit run --all-files`
5. Submit a pull request

## License

This project is provided as a boilerplate for building custom LiteLLM proxy servers. Modify and use according to your needs.

## Support

For issues with:
- **LiteLLM**: Check the [LiteLLM documentation](https://docs.litellm.ai/)
- **This boilerplate**: Open an issue in this repository
- **Provider-specific problems**: Consult the respective provider's documentation
