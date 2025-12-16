"""Test script to demonstrate the logging system with all log levels."""

import logging

from app_config import conf  # noqa: F401 - importing config triggers logging setup

# Get logger for this module
logger = logging.getLogger(__name__)


def demonstrate_logging() -> None:
    """Demonstrate all log levels and formatting."""
    logger.debug("This is a DEBUG message - detailed diagnostic information")
    logger.info("This is an INFO message - general informational message")
    logger.warning("This is a WARNING message - something unexpected happened")
    logger.error("This is an ERROR message - a serious problem occurred")
    logger.critical("This is a CRITICAL message - a very serious error")

    # Demonstrate logging with variables
    user_id = "12345"
    operation = "file_upload"
    logger.info("User %s performed operation: %s", user_id, operation)

    # Demonstrate exception logging
    try:
        result = 10 / 0  # noqa: F841
    except ZeroDivisionError as e:
        logger.error("Mathematical error occurred: %s", e, exc_info=True)

    # Demonstrate module context
    logger.info("Logger name: %s (shows module context)", logger.name)


if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("Starting Logging System Demonstration")
    logger.info("=" * 80)

    demonstrate_logging()

    logger.info("=" * 80)
    logger.info("Logging demonstration complete")
    logger.info("=" * 80)
