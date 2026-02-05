"""Environment and configuration management for last30days skill.

With x402 payments, API keys are no longer needed - payments are handled
via FluxA Agent Wallet and X-Payment headers passed to the script.
"""

import os
from pathlib import Path
from typing import Dict, Any

CONFIG_DIR = Path.home() / ".config" / "last30days"
CONFIG_FILE = CONFIG_DIR / ".env"


def load_env_file(path: Path) -> Dict[str, str]:
    """Load environment variables from a file."""
    env = {}
    if not path.exists():
        return env

    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, _, value = line.partition('=')
                key = key.strip()
                value = value.strip()
                # Remove quotes if present
                if value and value[0] in ('"', "'") and value[-1] == value[0]:
                    value = value[1:-1]
                if key and value:
                    env[key] = value
    return env


def get_config() -> Dict[str, Any]:
    """Load configuration from ~/.config/last30days/.env and environment.

    Note: API keys are no longer required with x402 payments.
    Config is now primarily for model preferences.
    """
    # Load from config file first
    file_env = load_env_file(CONFIG_FILE)

    # Environment variables override file
    config = {
        # Model preferences (optional)
        'OPENAI_MODEL': os.environ.get('OPENAI_MODEL') or file_env.get('OPENAI_MODEL', 'gpt-4o'),
        'XAI_MODEL': os.environ.get('XAI_MODEL') or file_env.get('XAI_MODEL', 'grok-4-1-fast-reasoning'),
    }

    return config


def config_exists() -> bool:
    """Check if configuration file exists."""
    return CONFIG_FILE.exists()
