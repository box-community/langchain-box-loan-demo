from pathlib import Path
from typing import Optional

from box_sdk_gen import BoxClient
from pydantic_settings import BaseSettings


class _APP_Config(BaseSettings):
    """Configuration for Box API integration and application settings."""

    # Box API Configuration
    BOX_CLIENT_ID: str
    BOX_CLIENT_SECRET: str
    BOX_SUBJECT_TYPE: str
    BOX_SUBJECT_ID: str
    BOX_DEMO_PARENT_FOLDER: str
    BOX_DEMO_FOLDER_NAME: str

    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = None  # Optional log file path

    # External API Keys
    TAVILY_API_KEY: str
    ANTHROPIC_API_KEY: str
    AGENTS_MEMORY_FOLDER: str = "agents_memories"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore",  # Ignore extra fields from .env file
        "validate_assignment": True,  # Validate on assignment
    }

    box_client: Optional[BoxClient] = None
    local_agents_memory: Optional[Path] = None


# Global config instance - import this from other modules
# Usage: from src.config import config
conf = _APP_Config()  # type: ignore

# Initialize box_client after conf is created (breaks circular import)
from utils.box_api_auth import get_box_client  # noqa: E402

conf.box_client = get_box_client()

# Memories folder is on the project folder
memories_folder = Path(__file__).parent.parent / conf.AGENTS_MEMORY_FOLDER
memories_folder.mkdir(parents=True, exist_ok=True)

conf.local_agents_memory = memories_folder


# Import logging_config to auto-configure logging based on config settings
# This ensures logging is set up whenever config is imported
import utils.logging_config  # noqa: E402, F401

# For backwards compatibility and explicit exports
__all__ = ["conf"]
