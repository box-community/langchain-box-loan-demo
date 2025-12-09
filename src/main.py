from config import Config
from utils.logging_config import get_logger, setup_logging

logger = get_logger(__name__)


def main() -> None:
    """Main application entry point."""
    # Load configuration
    config = Config()  # pyright: ignore[reportCallIssue]

    # Initialize logging
    setup_logging(level=config.LOG_LEVEL, log_file=config.LOG_FILE)

    logger.info("Starting langchain-box-loan-demo application")
    logger.debug("Configuration loaded successfully")

    # Application logic will go here
    logger.info("Application initialized successfully")


if __name__ == "__main__":
    main()
