"""Centralized logging configuration for the application.

This module provides a colored, formatted logging system with:
- Timestamp for each log entry
- Module name and line number
- Colored output based on log level
- Consistent formatting across the application
"""

import logging
import sys
from typing import Optional

import colorlog


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
) -> None:
    """Configure application-wide logging with color support.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to also log to a file
    """
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    # Create color formatter for console
    console_formatter = colorlog.ColoredFormatter(
        fmt=(
            "%(log_color)s%(asctime)s%(reset)s | "
            "%(log_color)s%(levelname)-8s%(reset)s | "
            "%(cyan)s%(name)s:%(lineno)d%(reset)s | "
            "%(message_log_color)s%(message)s%(reset)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={
            "message": {
                "DEBUG": "white",
                "INFO": "white",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red",
            }
        },
        style="%",
    )

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()

    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # Optional file handler (no colors)
    if log_file:
        file_formatter = logging.Formatter(
            fmt=(
                "%(asctime)s | %(levelname)-8s | "
                "%(name)s:%(lineno)d | %(message)s"
            ),
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

    # Suppress overly verbose third-party loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("box").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module.

    Args:
        name: Usually __name__ from the calling module

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)
