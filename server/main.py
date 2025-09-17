"""Main server entry point for the LiteLLM Yoda proxy server."""

import os
from pathlib import Path

import uvicorn
from dotenv import load_dotenv


def main():
    """Start the LiteLLM proxy server."""
    # Load environment variables
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    # Set default environment variables if not set
    os.environ.setdefault("LITELLM_LOG_LEVEL", "INFO")
    os.environ.setdefault("HOST", "0.0.0.0")
    os.environ.setdefault("PORT", "8000")

    # Import and start LiteLLM proxy
    try:
        from litellm import proxy

        config_path = Path(__file__).parent.parent / "config.yaml"

        # Start the proxy server
        proxy.run_server(
            host=os.environ.get("HOST", "0.0.0.0"),
            port=int(os.environ.get("PORT", 8000)),
            config_file_path=str(config_path),
        )

    except ImportError as e:
        print(f"Error importing LiteLLM proxy: {e}")
        print("Make sure all dependencies are installed with: uv sync")
        return 1

    except Exception as e:
        print(f"Error starting server: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
