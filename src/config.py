from typing import Optional

from pydantic_settings import BaseSettings


class Config(BaseSettings):
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

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields from .env file
