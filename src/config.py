from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Configuration for Box API integration."""

    BOX_CLIENT_ID: str
    BOX_CLIENT_SECRET: str
    BOX_SUBJECT_TYPE: str
    BOX_SUBJECT_ID: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields from .env file


# Global config instance
config = Config()  # type: ignore[call-arg]
