import logging

from config import config  # noqa: F401 - importing config triggers logging setup

logger = logging.getLogger(__name__)


def main() -> None:
    """Main application entry point."""
    logger.info("Starting langchain-box-loan-demo application")
    logger.debug("Configuration loaded successfully")

    # Application logic will go here
    logger.info("Application initialized successfully")


if __name__ == "__main__":
    main()
