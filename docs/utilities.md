# Utilities Reference

## Overview

The `src/utils/` directory contains shared utility modules that support the loan underwriting demo. These utilities handle Box API authentication, file operations, message display, and logging configuration.

---

## Module Overview

```
src/utils/
├── box_api_auth.py       # Box CCG authentication
├── box_api_generic.py    # Custom Box file/folder operations
├── display_messages.py   # Agent message streaming and formatting
└── logging_config.py     # Centralized logging configuration
```

---

## box_api_auth.py

**Purpose:** Box API authentication using Client Credentials Grant (CCG)

**Location:** [src/utils/box_api_auth.py](../src/utils/box_api_auth.py)

### Functions

#### `get_box_client() -> BoxClient`

Authenticate and return a configured BoxClient instance.

**Returns:**
- `BoxClient` - Authenticated Box client ready for API calls

**Raises:**
- `ValueError` - If required configuration is missing or invalid
- `BoxAPIError` - If authentication fails

**Configuration Requirements:**
- `BOX_CLIENT_ID` - Box app client ID
- `BOX_CLIENT_SECRET` - Box app client secret
- `BOX_SUBJECT_TYPE` - Either "user" or "enterprise"
- `BOX_SUBJECT_ID` - User ID or Enterprise ID

**Example:**
```python
from utils.box_api_auth import get_box_client

# Get authenticated client
client = get_box_client()

# Use client for Box API operations
folder_info = client.folders.get_folder_by_id("123456")
```

**Implementation Details:**
- Uses **Client Credentials Grant (CCG)** authentication
- Stores tokens in `.auth.ccg` file for persistence
- Validates configuration before attempting authentication
- Tests authentication by retrieving current user info
- Logs all authentication steps for debugging

**Token Storage:**
```python
file_token_storage = FileTokenStorage(filename=".auth.ccg")
```

**Authentication Flow:**
1. Validate configuration (client ID, secret, subject)
2. Create CCG configuration with token storage
3. Initialize BoxCCGAuth
4. Create BoxClient with auth
5. Verify authentication with `get_user_me()` call
6. Return authenticated client

**Supported Authentication Types:**
- **User authentication** - `BOX_SUBJECT_TYPE="user"` with `BOX_SUBJECT_ID=user_id`
- **Enterprise authentication** - `BOX_SUBJECT_TYPE="enterprise"` with `BOX_SUBJECT_ID=enterprise_id`

---

## box_api_generic.py

**Purpose:** Custom Box file and folder operations beyond what's in the toolkit

**Location:** [src/utils/box_api_generic.py](../src/utils/box_api_generic.py)

### Functions

#### `box_file_pre_flight_check(client, local_file_name, parent_folder_id) -> tuple[bool, Optional[str], Optional[UploadUrl]]`

Check if a file can be uploaded to Box before attempting upload.

**Args:**
- `client` (`BoxClient`) - Authenticated Box client
- `local_file_name` (`Path`) - Path to local file
- `parent_folder_id` (`str`) - Target Box folder ID

**Returns:**
Tuple containing:
- `bool` - True if file can be uploaded, False if conflict exists
- `Optional[str]` - Existing file ID if conflict detected, None otherwise
- `Optional[UploadUrl]` - Upload URL if file can be uploaded, None if conflict

**Raises:**
- `BoxAPIError` - If check fails for reasons other than name conflict

**Use Case:**
Determine whether to upload a new file or update an existing one.

**Example:**
```python
from pathlib import Path

local_file = Path("report.pdf")
can_upload, conflict_id, upload_url = box_file_pre_flight_check(
    client, local_file, parent_folder_id="123456"
)

if can_upload:
    # Upload as new file
    file_id = box_file_upload(client, local_file, parent_folder_id)
elif conflict_id:
    # Update existing file
    file_id = box_file_update(client, conflict_id, local_file)
```

---

#### `box_file_upload(client, local_file_path, box_folder_parent_id) -> str`

Upload a new file to Box.

**Args:**
- `client` (`BoxClient`) - Authenticated Box client
- `local_file_path` (`Path`) - Path to local file to upload
- `box_folder_parent_id` (`str`) - Target Box folder ID

**Returns:**
- `str` - Box file ID of uploaded file

**Raises:**
- `BoxAPIError` - If upload fails
- `ValueError` - If no file entries returned from API

**Example:**
```python
from pathlib import Path

local_file = Path("data/report.pdf")
file_id = box_file_upload(
    client=client,
    local_file_path=local_file,
    box_folder_parent_id="123456"
)
print(f"Uploaded file ID: {file_id}")
```

---

#### `box_file_update(client, file_id, local_file_path) -> str`

Update an existing file in Box with new content.

**Args:**
- `client` (`BoxClient`) - Authenticated Box client
- `file_id` (`str`) - ID of existing Box file to update
- `local_file_path` (`Path`) - Path to local file with new content

**Returns:**
- `str` - Box file ID of updated file

**Raises:**
- `BoxAPIError` - If update fails
- `ValueError` - If no file entries returned from API

**Example:**
```python
from pathlib import Path

local_file = Path("data/updated_report.pdf")
file_id = box_file_update(
    client=client,
    file_id="987654",
    local_file_path=local_file
)
```

---

#### `box_folder_create(client, folder_name, parent_folder_id) -> str`

Create a folder in Box (or return existing folder ID if conflict).

**Args:**
- `client` (`BoxClient`) - Authenticated Box client
- `folder_name` (`str`) - Name of folder to create
- `parent_folder_id` (`str`) - Parent Box folder ID

**Returns:**
- `str` - Box folder ID (newly created or existing)

**Raises:**
- `BoxAPIError` - If creation fails for reasons other than name conflict

**Example:**
```python
folder_id = box_folder_create(
    client=client,
    folder_name="Loan Applications",
    parent_folder_id="0"  # Root folder
)
```

**Conflict Handling:**
If a folder with the same name already exists, returns the existing folder ID instead of raising an error.

---

#### `save_upload_cache_to_json(folder_cache, output_file) -> None`

Save upload cache to a JSON file for tracking uploaded items.

**Args:**
- `folder_cache` (`Dict[str, Dict[str, str]]`) - Dictionary mapping local paths to Box metadata
- `output_file` (`Path`) - Path to output JSON file

**Example:**
```python
from pathlib import Path

cache = {
    "data/Applications/Sarah Chen/Sarah Documents/application.pdf": {
        "name": "application.pdf",
        "type": "file",
        "id": "123456789"
    }
}

save_upload_cache_to_json(
    folder_cache=cache,
    output_file=Path("agents_memories/box_upload_cache.json")
)
```

**Cache Structure:**
```json
{
  "local/path/to/file.pdf": {
    "name": "file.pdf",
    "type": "file",
    "id": "123456789"
  },
  "local/path/to/folder": {
    "name": "folder",
    "type": "folder",
    "id": "987654321"
  }
}
```

---

#### `local_folder_upload(client, local_dir, parent_folder_id, folder_cache) -> None`

Recursively upload a directory and its contents to Box.

**Args:**
- `client` (`BoxClient`) - Authenticated Box client
- `local_dir` (`Path`) - Path to local directory to upload
- `parent_folder_id` (`str`) - Target Box folder ID
- `folder_cache` (`Dict[str, Dict[str, str]]`) - Dictionary to track uploaded items

**Behavior:**
- Recursively processes all subdirectories
- Skips files starting with `.` (hidden files)
- Updates existing files if conflicts detected
- Creates folders if they don't exist
- Populates `folder_cache` with all uploaded items

**Example:**
```python
from pathlib import Path

cache = {}
local_folder_upload(
    client=client,
    local_dir=Path("data/Applications"),
    parent_folder_id="123456",
    folder_cache=cache
)

# Cache now contains all uploaded items
print(f"Uploaded {len(cache)} items")
```

**Used in:** [src/demo_upload_sample_data.py](../src/demo_upload_sample_data.py)

---

#### `local_file_upload(client, local_file_path, parent_folder_id) -> str`

Upload a single file to Box (wrapper combining pre-flight check + upload/update).

**Args:**
- `client` (`BoxClient`) - Authenticated Box client
- `local_file_path` (`Path`) - Path to local file
- `parent_folder_id` (`str`) - Target Box folder ID

**Returns:**
- `str` - Box file ID of uploaded/updated file

**Raises:**
- `BoxAPIError` - If upload/update fails
- `ValueError` - If unable to determine upload status

**Example:**
```python
from pathlib import Path

file_id = local_file_upload(
    client=client,
    local_file_path=Path("report.pdf"),
    parent_folder_id="123456"
)
```

**Logic:**
1. Run pre-flight check
2. If no conflict → upload new file
3. If conflict → update existing file
4. Return file ID

---

## display_messages.py

**Purpose:** Format and display agent messages with rich terminal output

**Location:** [src/utils/display_messages.py](../src/utils/display_messages.py)

### Functions

#### `format_message_content(message) -> str`

Convert message content to displayable string.

**Args:**
- `message` - LangChain message object

**Returns:**
- `str` - Formatted message content

**Handles:**
- String content
- List content (Anthropic format with tool calls)
- Tool calls in message (OpenAI format)
- Complex nested structures

**Example:**
```python
from langchain_core.messages import HumanMessage

message = HumanMessage(content="Process loan for Sarah Chen")
formatted = format_message_content(message)
```

---

#### `format_messages(messages) -> None`

Format and display a list of messages with Rich formatting.

**Args:**
- `messages` - List of LangChain message objects

**Display Styles:**
- **Human messages** - Blue panel with 🧑 icon
- **AI messages** - Green panel with 🤖 icon
- **Tool messages** - Yellow panel with 🔧 icon
- **Other messages** - White panel with 📝 icon

**Example:**
```python
from langchain_core.messages import HumanMessage, AIMessage

messages = [
    HumanMessage(content="What is the DTI ratio?"),
    AIMessage(content="The DTI ratio is 42.1%")
]

format_messages(messages)
```

**Output:**
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🧑 Human                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛
What is the DTI ratio?

┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🤖 Assistant             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛
The DTI ratio is 42.1%
```

---

#### `format_message(messages) -> None`

Alias for `format_messages()` for backward compatibility.

---

#### `show_prompt(prompt_text, title="Prompt", border_style="blue") -> None`

Display a prompt with rich formatting and syntax highlighting.

**Args:**
- `prompt_text` (`str`) - Prompt string to display
- `title` (`str`) - Panel title (default: "Prompt")
- `border_style` (`str`) - Border color (default: "blue")

**Highlighting:**
- **XML tags** - Bold blue (`<tag>`)
- **Headers** - Bold magenta (`##Header`)
- **Sub-headers** - Bold cyan (`###Subheader`)

**Example:**
```python
prompt = """
## Loan Underwriting Instructions

Extract the following from <documents>:
- Applicant name
- Monthly income
"""

show_prompt(prompt, title="System Prompt")
```

---

#### `stream_agent(agent, query, config=None) -> dict`

Stream agent execution with real-time message display.

**Args:**
- `agent` - LangGraph agent (CompiledStateGraph)
- `query` (`dict`) - Input query with messages
- `config` (`dict`, optional) - Agent configuration

**Returns:**
- `dict` - Final agent state after execution

**Behavior:**
- Streams agent execution in real-time
- Displays messages as they're generated
- Shows both orchestrator and sub-agent messages
- Returns final state when complete

**Example:**
```python
from agents.loan_orchestrator import loan_orchestrator_create

async def run_agent():
    agent = loan_orchestrator_create("Sarah Chen")

    final_state = await stream_agent(
        agent,
        {"messages": [{"role": "user", "content": "Process loan application"}]}
    )

    print(f"Final state: {final_state}")
```

**Used in:**
- [src/demo_loan.py](../src/demo_loan.py)
- [src/demo_research.py](../src/demo_research.py)

**Stream Modes:**
- **updates** - Individual node updates (messages, tool calls)
- **values** - Complete state snapshots

---

## logging_config.py

**Purpose:** Centralized logging configuration with colored console output

**Location:** [src/utils/logging_config.py](../src/utils/logging_config.py)

### Configuration

**Auto-initialization:** Logging is automatically configured when this module is imported.

**Configuration Source:** Reads settings from [src/app_config.py](../src/app_config.py):
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `LOG_FILE` - Optional log file path (None = console only)

### Log Format

**Console Output (with colors):**
```
2024-12-17 14:30:45 | INFO     | module_name:123 | Message text
```

**File Output (no colors):**
```
2024-12-17 14:30:45 | INFO     | module_name:123 | Message text
```

### Color Scheme

| Level | Color |
|-------|-------|
| DEBUG | Cyan |
| INFO | Green |
| WARNING | Yellow |
| ERROR | Red |
| CRITICAL | Red on white background |

### Functions

#### `_configure_logging(level="INFO", log_file=None) -> None`

Internal function to configure application-wide logging.

**Args:**
- `level` (`str`) - Logging level (default: "INFO")
- `log_file` (`str`, optional) - Path to log file (default: None)

**Behavior:**
- Configures root logger with colored console handler
- Optionally adds file handler (without colors)
- Suppresses verbose third-party loggers (urllib3, box, httpx, httpcore)
- Only configures once (subsequent calls are no-ops)

**Third-Party Logger Suppression:**
```python
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("box").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
```

### Usage

**Automatic Configuration:**
```python
# Simply import the config module to initialize logging
from utils import logging_config
import logging

logger = logging.getLogger(__name__)
logger.info("Logging is configured automatically")
```

**Manual Configuration:**
```python
import logging
from utils.logging_config import _configure_logging

# Reconfigure with custom settings
_configure_logging(level="DEBUG", log_file="app.log")

logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

### Example Output

```python
import logging
from utils import logging_config

logger = logging.getLogger(__name__)

logger.debug("Debugging information")
logger.info("Processing loan application")
logger.warning("High DTI ratio detected")
logger.error("Failed to connect to Box API")
```

**Console Output:**
```
2024-12-17 14:30:45 | DEBUG    | __main__:5 | Debugging information
2024-12-17 14:30:45 | INFO     | __main__:6 | Processing loan application
2024-12-17 14:30:45 | WARNING  | __main__:7 | High DTI ratio detected
2024-12-17 14:30:45 | ERROR    | __main__:8 | Failed to connect to Box API
```

---

## Integration with Main Application

### Configuration Pattern

All utilities read configuration from [src/app_config.py](../src/app_config.py):

```python
from app_config import conf

# Access Box client (configured with CCG auth)
client = conf.box_client

# Access memories folder
memories = conf.local_agents_memory

# Log level and file are read automatically
```

### Typical Usage Pattern

```python
import logging
from app_config import conf
from utils.display_messages import stream_agent

logger = logging.getLogger(__name__)

async def process_application(applicant_name: str):
    # Logging is already configured
    logger.info(f"Processing application for {applicant_name}")

    # Box client is ready to use
    client = conf.box_client

    # Stream agent execution
    agent = create_agent(applicant_name)
    await stream_agent(agent, {"messages": [...]})
```

---

## Dependencies

**box_api_auth.py:**
- `box_sdk_gen` - BoxClient, BoxCCGAuth, CCGConfig, FileTokenStorage
- `app_config` - Configuration settings

**box_api_generic.py:**
- `box_sdk_gen` - Box API types and client
- `pathlib` - Path operations
- `json` - Cache file serialization

**display_messages.py:**
- `rich` - Terminal formatting (Console, Markdown, Panel, Text)
- `json` - Message content formatting

**logging_config.py:**
- `colorlog` - Colored logging output
- `app_config` - Configuration settings

---

## Common Patterns

### Pattern 1: Authenticate and Upload

```python
from utils.box_api_auth import get_box_client
from utils.box_api_generic import local_file_upload
from pathlib import Path

# Get authenticated client
client = get_box_client()

# Upload file
file_id = local_file_upload(
    client=client,
    local_file_path=Path("report.pdf"),
    parent_folder_id="123456"
)
```

### Pattern 2: Recursive Folder Upload with Cache

```python
from utils.box_api_generic import local_folder_upload, save_upload_cache_to_json
from pathlib import Path

cache = {}
local_folder_upload(
    client=client,
    local_dir=Path("data/Applications"),
    parent_folder_id="123456",
    folder_cache=cache
)

# Save cache for later reference
save_upload_cache_to_json(
    folder_cache=cache,
    output_file=Path("agents_memories/box_upload_cache.json")
)
```

### Pattern 3: Stream Agent with Logging

```python
import logging
from utils.display_messages import stream_agent
from utils import logging_config  # Auto-configures logging

logger = logging.getLogger(__name__)

async def run_workflow():
    logger.info("Starting workflow")

    final_state = await stream_agent(
        agent,
        {"messages": [{"role": "user", "content": "Process loan"}]}
    )

    logger.info("Workflow complete")
```

---

## Summary

The utilities module provides:

- **box_api_auth.py** - Simple CCG authentication with token persistence
- **box_api_generic.py** - File/folder operations with conflict handling and recursive uploads
- **display_messages.py** - Rich terminal formatting for agent messages and prompts
- **logging_config.py** - Colored, structured logging with automatic configuration

These utilities are used throughout the project to:
- Authenticate with Box API
- Upload sample data to Box
- Display agent execution in real-time
- Log application events with proper formatting

All utilities integrate seamlessly with [src/app_config.py](../src/app_config.py) for centralized configuration management.
