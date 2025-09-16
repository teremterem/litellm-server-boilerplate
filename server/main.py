from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env if present
PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

# Entrypoint to run LiteLLM Proxy using config.yaml
# Usage: uv run python -m server.main

if __name__ == "__main__":
    import sys
    import subprocess

    config_path = str(PROJECT_ROOT / "config.yaml")

    # Allow overriding host/port via env
    host = os.getenv("LITELLM_HOST", "0.0.0.0")
    port = os.getenv("LITELLM_PORT", "8000")

    cmd = [
        sys.executable,
        "-m",
        "litellm",
        "--config",
        config_path,
        "--host",
        host,
        "--port",
        port,
    ]
    subprocess.run(cmd, check=True)
