"""
Main entry point for the LiteLLM server with custom Yoda-speak model.
"""

import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv
import litellm
from server.yoda_model import YodaSpeakModel

# Load environment variables
load_dotenv()


def initialize_custom_model():
    """Register the custom Yoda-speak model with LiteLLM."""
    # Create an instance of the custom model
    yoda_model = YodaSpeakModel()

    # Register the custom model with LiteLLM
    litellm.custom_provider_map = [{"provider": "custom", "custom_handler": yoda_model, "model": "custom/yoda-speak"}]


def run_server():
    """Run the LiteLLM proxy server."""
    # Initialize the custom model
    initialize_custom_model()

    # Get the config file path
    config_path = Path(__file__).parent.parent / "config.yaml"

    # Run LiteLLM proxy as a subprocess
    cmd = [
        sys.executable,
        "-m",
        "litellm",
        "--config",
        str(config_path),
        "--host",
        os.getenv("LITELLM_HOST", "0.0.0.0"),
        "--port",
        os.getenv("LITELLM_PORT", "8000"),
        "--num_workers",
        "1",
    ]

    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    run_server()
