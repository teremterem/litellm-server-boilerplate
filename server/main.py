"""
Main entry point for the LiteLLM Server with YodaLLM.
"""

import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv


def main():
    """
    Start the LiteLLM server with YodaLLM configuration.
    """
    # Load environment variables
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)

    # Start litellm server
    try:
        # This will use the config.yaml file to start the server

        config_path = Path(__file__).parent.parent / "config.yaml"
        host = os.getenv("HOST", "0.0.0.0")
        port = os.getenv("PORT", "4000")

        cmd = [
            sys.executable,
            "-m",
            "litellm",
            "--config",
            str(config_path),
            "--host",
            host,
            "--port",
            port,
        ]

        print(f"Starting LiteLLM server with YodaLLM on {host}:{port}")
        print(f"Using config: {config_path}")
        print("Server will be available at: http://localhost:4000")
        print("API docs will be available at: http://localhost:4000/docs")

        subprocess.run(cmd, check=True)

    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
