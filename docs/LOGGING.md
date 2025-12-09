# Logging System Documentation

## Overview

The application uses a centralized, colored logging system with:
- **Timestamps**: Every log entry includes a timestamp (YYYY-MM-DD HH:MM:SS format)
- **Module context**: Shows the module name and line number where the log was generated
- **Color-coded levels**: Different colors for each log level for easy visual scanning
- **Consistent formatting**: All modules use the same logging format

## Log Levels and Colors

- **DEBUG** (Cyan): Detailed diagnostic information
- **INFO** (Green): General informational messages
- **WARNING** (Yellow): Something unexpected happened but the application continues
- **ERROR** (Red): A serious problem occurred
- **CRITICAL** (Red on white background): A very serious error

## Usage in Code

### 1. Import the logger utilities

```python
from utils.logging_config import get_logger, setup_logging
```

### 2. Initialize logging (in main entry point only)

```python
from config import Config

# Load configuration
config = Config()

# Initialize logging (call this once at application startup)
setup_logging(level=config.LOG_LEVEL, log_file=config.LOG_FILE)
```

### 3. Get a logger for your module

```python
# At the top of your module, after imports
logger = get_logger(__name__)
```

### 4. Use the logger

```python
# Simple messages
logger.debug("Detailed diagnostic information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical error")

# With variables (recommended - use %s formatting)
user_id = "12345"
logger.info("Processing user: %s", user_id)

# With exception information
try:
    # some operation
    result = risky_operation()
except Exception as e:
    logger.error("Operation failed: %s", e, exc_info=True)
```

## Configuration

Logging is configured through environment variables or the `.env` file:

```bash
# Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# Optional: Write logs to a file in addition to console
LOG_FILE=logs/application.log
```

## Features

### Automatic Module Context
The logger automatically shows which module and line number generated each log entry:
```
2025-12-09 16:51:40 | INFO     | utils.box_auth:62 | Box client authenticated successfully
```

### Exception Logging with Traceback
When logging exceptions with `exc_info=True`, the full traceback is displayed with syntax highlighting:
```python
logger.error("Failed to process: %s", e, exc_info=True)
```

### Third-Party Library Suppression
The logging system automatically suppresses verbose logging from common third-party libraries:
- urllib3
- box SDK
- httpx
- httpcore

These libraries are set to WARNING level to reduce noise in the logs.

## Example Output

```
2025-12-09 16:52:13 | INFO     | __main__:38 | Starting application
2025-12-09 16:52:13 | DEBUG    | __main__:16 | Detailed diagnostic information
2025-12-09 16:52:13 | INFO     | __main__:17 | General informational message
2025-12-09 16:52:13 | WARNING  | __main__:18 | Something unexpected happened
2025-12-09 16:52:13 | ERROR    | __main__:19 | A serious problem occurred
2025-12-09 16:52:13 | INFO     | __main__:25 | User 12345 performed operation: file_upload
```

## Testing

To test the logging system, run the demonstration script:

```bash
uv run python test_logging.py
```

This will display all log levels and demonstrate various logging features including:
- All log level colors
- Variable interpolation
- Exception logging with tracebacks
- Module context display

## Best Practices

1. **Use appropriate log levels**:
   - DEBUG: Detailed diagnostic information for development
   - INFO: Confirmation that things are working as expected
   - WARNING: Something unexpected but the app continues
   - ERROR: Serious problem, some functionality is affected
   - CRITICAL: Application may be unable to continue

2. **Use lazy formatting**: Use `%s` placeholders instead of f-strings
   ```python
   # Good
   logger.info("User %s logged in", username)

   # Avoid (formats even if not logged)
   logger.info(f"User {username} logged in")
   ```

3. **Include context**: Log relevant information to help with debugging
   ```python
   logger.error("Failed to process order %s for customer %s", order_id, customer_id)
   ```

4. **Log exceptions with traceback**: Always use `exc_info=True` when logging exceptions
   ```python
   except Exception as e:
       logger.error("Operation failed: %s", e, exc_info=True)
   ```

5. **Don't log sensitive information**: Avoid logging passwords, API keys, or PII

## File Logging

To enable file logging, set the `LOG_FILE` environment variable:

```bash
LOG_FILE=logs/app.log
```

File logs use the same format but without colors (plain text for better compatibility with log analysis tools).
