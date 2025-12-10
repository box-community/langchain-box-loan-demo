from typing import Optional

from pydantic_settings import BaseSettings


class _Config(BaseSettings):
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

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore",  # Ignore extra fields from .env file
        "validate_assignment": True,  # Validate on assignment
    }


# Global config instance - import this from other modules
# Usage: from src.config import config
config = _Config()  # type: ignore

# Import logging_config to auto-configure logging based on config settings
# This ensures logging is set up whenever config is imported
import utils.logging_config  # noqa: E402, F401

# For backwards compatibility and explicit exports
__all__ = ["config"]
