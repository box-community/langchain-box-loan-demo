# Box AI Agents Toolkit

## Overview

The **`box-ai-agents-toolkit`** is a comprehensive Python library that provides high-level abstractions for interacting with Box's API, with a particular focus on Box AI capabilities. It simplifies common Box operations by wrapping the Box SDK with intuitive, agent-friendly functions.

**Package:** `box-ai-agents-toolkit` (≥0.1.5)

**GitHub Repository:** [https://github.com/box-community/box-ai-agents-toolkit](https://github.com/box-community/box-ai-agents-toolkit)

**Purpose:** Enable AI agents and applications to seamlessly interact with Box content, AI features, and enterprise collaboration tools.

---

## What This Project Uses

This loan underwriting demo primarily uses:

### 1. Box AI Functions
- `box_ai_ask_file_multi()` - Query Box AI about multiple documents
- `box_ai_extract_structured_enhanced_using_fields()` - Extract structured data with field definitions

### 2. Box Search Functions
- `box_locate_folder_by_name()` - Find folders by name
- `box_folder_items_list()` - List folder contents

### 3. Box File/Folder Operations
- `box_folder_create()` - Create folders (from toolkit)
- `box_file_upload()` - Upload files (custom wrapper in [src/utils/box_api_generic.py](../src/utils/box_api_generic.py))
- `box_file_update()` - Update existing files (custom wrapper)
- `local_file_upload()` - Upload single file (custom wrapper)
- `local_folder_upload()` - Recursively upload directories (custom implementation)

### 4. Authentication
- `get_ccg_client()` - Client Credentials Grant authentication

---

## Library Organization

The toolkit is organized into functional modules:

```
box_ai_agents_toolkit/
├── __init__.py                      # Main exports
├── box_api_ai.py                    # Box AI capabilities
├── box_api_file.py                  # File operations
├── box_api_folder.py                # Folder operations
├── box_api_search.py                # Search functionality
├── box_api_file_transfer.py         # Upload/download
├── box_api_file_representation.py   # File representations (text extraction)
├── box_api_collaborations.py        # Sharing and collaboration
├── box_api_shared_links.py          # Shared link management
├── box_api_metadata_template.py     # Metadata operations
├── box_api_tasks.py                 # Task management
├── box_api_users.py                 # User management
├── box_api_groups.py                # Group management
├── box_api_weblink.py               # Web link operations
├── box_api_docgen.py                # Document generation
├── box_api_docgen_template.py       # DocGen templates
├── box_authentication.py            # Authentication helpers
├── box_api_util_classes.py          # Utility classes
├── box_api_util_generic.py          # Generic utilities
└── box_api_util_http.py             # HTTP utilities
```

---

## Complete Function Reference

### Box AI Functions

#### AI Agent Management
```python
box_ai_agents_list(client, limit=1000) -> Dict[str, Any]
```
List all available AI agents in Box AI Studio.

```python
box_ai_agents_search_by_name(client, name, limit=1000) -> Dict[str, Any]
```
Search for AI agents by name (case-insensitive).

```python
box_ai_agent_info_by_id(client, ai_agent_id) -> Dict[str, Any]
```
Get detailed information about a specific AI agent by ID.

#### AI Ask (Question Answering)

```python
box_ai_ask_file_single(
    client: BoxClient,
    file_id: str,
    prompt: str,
    ai_agent_id: Optional[str] = None
) -> Dict[str, Any]
```
Ask a question about a single file using Box AI.

**Used in this project:** ✅ (via `box_ai_ask_file_multi`)

```python
box_ai_ask_file_multi(
    client: BoxClient,
    file_ids: List[str],
    prompt: str,
    ai_agent_id: Optional[str] = None
) -> Dict[str, Any]
```
Ask a question about multiple files simultaneously. Box AI analyzes all files together.

**Used in this project:** ✅
- Querying loan application documents
- Asking policy questions across multiple policy files

**Example:**
```python
response = box_ai_ask_file_multi(
    client=box_client,
    file_ids=["123", "456", "789"],
    prompt="What is the applicant's gross monthly income?",
)
```

```python
box_ai_ask_hub(
    client: BoxClient,
    prompt: str,
    ai_agent_id: Optional[str] = None
) -> Dict[str, Any]
```
Ask Box AI Hub a general question (not file-specific).

#### AI Extract (Structured Data Extraction)

```python
box_ai_extract_freeform(
    client: BoxClient,
    file_id: str,
    prompt: str,
    ai_agent_id: Optional[str] = None
) -> Dict[str, Any]
```
Extract unstructured information from a file using natural language prompt.

```python
box_ai_extract_structured_using_fields(
    client: BoxClient,
    file_id: str,
    fields: List[Dict],
    ai_agent_id: Optional[str] = None
) -> Dict[str, Any]
```
Extract structured data from a file using field definitions.

```python
box_ai_extract_structured_enhanced_using_fields(
    client: BoxClient,
    file_ids: List[str],
    fields: List[Dict],
    ai_agent_id: Optional[str] = None
) -> Dict[str, Any]
```
Extract structured data from multiple files with enhanced field definitions.

**Used in this project:** ✅
- Extracting applicant information, income, credit, vehicle, loan details

**Example:**
```python
fields = [
    {
        "key": "applicant_name",
        "type": "string",
        "prompt": "Full name of the applicant",
    },
    {
        "key": "monthly_income",
        "type": "float",
        "prompt": "Gross monthly income",
    },
]

response = box_ai_extract_structured_enhanced_using_fields(
    client=box_client,
    file_ids=["123", "456"],
    fields=fields,
)
```

```python
box_ai_extract_structured_using_template(
    client: BoxClient,
    file_id: str,
    template_key: str,
    scope: str,
    ai_agent_id: Optional[str] = None
) -> Dict[str, Any]
```
Extract data using a pre-defined Box metadata template.

```python
box_ai_extract_structured_enhanced_using_template(
    client: BoxClient,
    file_ids: List[str],
    template_key: str,
    scope: str,
    ai_agent_id: Optional[str] = None
) -> Dict[str, Any]
```
Extract data from multiple files using a metadata template.

---

### File Operations

```python
box_file_info(client, file_id) -> dict[str, Any]
```
Get detailed information about a file.

```python
box_file_copy(client, file_id, destination_parent_folder_id, name=None) -> dict[str, Any]
```
Copy a file to a new location.

```python
box_file_move(client, file_id, destination_parent_folder_id) -> dict[str, Any]
```
Move a file to a different folder.

```python
box_file_delete(client, file_id) -> dict[str, Any]
```
Delete a file from Box.

```python
box_file_rename(client, file_id, new_name) -> dict[str, Any]
```
Rename a file.

```python
box_file_set_description(client, file_id, description) -> dict[str, Any]
```
Set or update file description.

```python
box_file_lock(client, file_id, is_download_prevented=False) -> dict[str, Any]
```
Lock a file to prevent edits.

```python
box_file_unlock(client, file_id) -> dict[str, Any]
```
Unlock a previously locked file.

```python
box_file_retention_date_set(client, file_id, retention_date) -> dict[str, Any]
```
Set retention date for a file.

```python
box_file_retention_date_clear(client, file_id) -> dict[str, Any]
```
Clear retention date from a file.

#### File Download Settings

```python
box_file_set_download_open(client, file_id) -> dict[str, Any]
```
Allow anyone with link to download file.

```python
box_file_set_download_company(client, file_id) -> dict[str, Any]
```
Restrict downloads to company users only.

```python
box_file_set_download_reset(client, file_id) -> dict[str, Any]
```
Reset download permissions to default.

#### File Tags

```python
box_file_tag_list(client, file_id) -> dict[str, Any]
```
List all tags on a file.

```python
box_file_tag_add(client, file_id, tags) -> dict[str, Any]
```
Add tags to a file.

```python
box_file_tag_remove(client, file_id, tags) -> dict[str, Any]
```
Remove specific tags from a file.

#### File Thumbnails

```python
box_file_thumbnail_url(client, file_id, min_width=256, min_height=256) -> dict[str, Any]
```
Get URL for file thumbnail.

```python
box_file_thumbnail_download(client, file_id, output_path, min_width=256, min_height=256) -> dict[str, Any]
```
Download file thumbnail to local path.

---

### File Transfer

```python
box_file_download(client, file_id, output_path) -> dict[str, Any]
```
Download a file from Box to local filesystem.

```python
box_file_upload(client, local_file_path, parent_folder_id) -> dict[str, Any]
```
Upload a file to Box.

**Used in this project:** ✅ (custom wrapper in utils)

---

### File Representations

```python
box_file_text_extract(client, file_id) -> dict[str, Any]
```
Extract text content from a file (PDF, Word, etc.).

---

### Folder Operations

```python
box_folder_info(client, folder_id) -> dict[str, Any]
```
Get detailed information about a folder.

```python
box_folder_items_list(client, folder_id, is_recursive=False, limit=1000) -> dict[str, Any]
```
List items in a folder with optional recursive traversal.

**Used in this project:** ✅
- Listing loan application documents

**Example:**
```python
response = box_folder_items_list(
    client=box_client,
    folder_id="123456",
    is_recursive=True,  # Include subfolders
)
```

```python
box_folder_create(client, name, parent_folder_id) -> dict[str, Any]
```
Create a new folder.

**Used in this project:** ✅
- Creating folder structure when uploading sample data

```python
box_folder_delete(client, folder_id, recursive=False) -> dict[str, Any]
```
Delete a folder (optionally with all contents).

```python
box_folder_copy(client, folder_id, destination_parent_folder_id, name=None) -> dict[str, Any]
```
Copy a folder to a new location.

```python
box_folder_move(client, folder_id, destination_parent_folder_id) -> dict[str, Any]
```
Move a folder to a different parent.

```python
box_folder_rename(client, folder_id, new_name) -> dict[str, Any]
```
Rename a folder.

```python
box_folder_set_description(client, folder_id, description) -> dict[str, Any]
```
Set or update folder description.

```python
box_folder_set_collaboration(client, folder_id, collaboration_role) -> dict[str, Any]
```
Set collaboration access level for a folder.

```python
box_folder_favorites_add(client, folder_id) -> dict[str, Any]
```
Add folder to favorites.

```python
box_folder_favorites_remove(client, folder_id) -> dict[str, Any]
```
Remove folder from favorites.

```python
box_folder_set_sync(client, folder_id, sync_state) -> dict[str, Any]
```
Enable/disable folder sync.

```python
box_folder_set_upload_email(client, folder_id, access_level) -> dict[str, Any]
```
Configure email-to-folder upload settings.

#### Folder Tags

```python
box_folder_tag_list(client, folder_id) -> dict[str, Any]
```
List all tags on a folder.

```python
box_folder_tag_add(client, folder_id, tags) -> dict[str, Any]
```
Add tags to a folder.

```python
box_folder_tag_remove(client, folder_id, tags) -> dict[str, Any]
```
Remove tags from a folder.

---

### Search Functions

```python
box_search(client, query, limit=100) -> dict[str, Any]
```
General Box content search.

```python
box_locate_folder_by_name(client, folder_name, limit=100) -> dict[str, Any]
```
Search for folders by name.

**Used in this project:** ✅
- Finding loan application folders by applicant name

**Example:**
```python
response = box_locate_folder_by_name(
    client=box_client,
    folder_name="Sarah Chen",
)
# Returns folder ID if found
```

---

### Collaboration Functions

```python
box_collaborations_list_by_file(client, file_id) -> dict[str, Any]
```
List all collaborations on a file.

```python
box_collaborations_list_by_folder(client, folder_id) -> dict[str, Any]
```
List all collaborations on a folder.

#### Add Collaborations

```python
box_collaboration_file_user_by_user_id(client, file_id, user_id, role) -> dict[str, Any]
```
Share a file with a user by user ID.

```python
box_collaboration_file_user_by_user_login(client, file_id, user_login, role) -> dict[str, Any]
```
Share a file with a user by email.

```python
box_collaboration_folder_user_by_user_id(client, folder_id, user_id, role) -> dict[str, Any]
```
Share a folder with a user by user ID.

```python
box_collaboration_folder_user_by_user_login(client, folder_id, user_login, role) -> dict[str, Any]
```
Share a folder with a user by email.

```python
box_collaboration_file_group_by_group_id(client, file_id, group_id, role) -> dict[str, Any]
```
Share a file with a group.

```python
box_collaboration_folder_group_by_group_id(client, folder_id, group_id, role) -> dict[str, Any]
```
Share a folder with a group.

#### Manage Collaborations

```python
box_collaboration_update(client, collaboration_id, role) -> dict[str, Any]
```
Update collaboration role.

```python
box_collaboration_delete(client, collaboration_id) -> dict[str, Any]
```
Remove a collaboration.

---

### Shared Links

#### File Shared Links

```python
box_shared_link_file_get(client, file_id) -> dict[str, Any]
```
Get existing shared link for a file.

```python
box_shared_link_file_create_or_update(client, file_id, access_level, password=None, unshared_at=None) -> dict[str, Any]
```
Create or update shared link for a file.

```python
box_shared_link_file_remove(client, file_id) -> dict[str, Any]
```
Remove shared link from a file.

```python
box_shared_link_file_find_by_shared_link_url(client, shared_link_url, password=None) -> dict[str, Any]
```
Get file information from shared link URL.

#### Folder Shared Links

```python
box_shared_link_folder_get(client, folder_id) -> dict[str, Any]
```
Get existing shared link for a folder.

```python
box_shared_link_folder_create_or_update(client, folder_id, access_level, password=None, unshared_at=None) -> dict[str, Any]
```
Create or update shared link for a folder.

```python
box_shared_link_folder_remove(client, folder_id) -> dict[str, Any]
```
Remove shared link from a folder.

```python
box_shared_link_folder_find_by_shared_link_url(client, shared_link_url, password=None) -> dict[str, Any]
```
Get folder information from shared link URL.

#### Web Link Shared Links

```python
box_shared_link_web_link_get(client, web_link_id) -> dict[str, Any]
```
Get shared link for a web link.

```python
box_shared_link_web_link_create_or_update(client, web_link_id, access_level, password=None) -> dict[str, Any]
```
Create or update shared link for a web link.

```python
box_shared_link_web_link_remove(client, web_link_id) -> dict[str, Any]
```
Remove shared link from a web link.

```python
box_shared_link_web_link_find_by_shared_link_url(client, shared_link_url, password=None) -> dict[str, Any]
```
Find web link by shared link URL.

---

### Metadata Functions

```python
box_metadata_template_list(client, scope="enterprise") -> dict[str, Any]
```
List all metadata templates.

```python
box_metadata_template_get_by_id(client, template_id) -> dict[str, Any]
```
Get metadata template by ID.

```python
box_metadata_template_get_by_key(client, scope, template_key) -> dict[str, Any]
```
Get metadata template by scope and key.

```python
box_metadata_template_get_by_name(client, template_name, scope="enterprise") -> dict[str, Any]
```
Get metadata template by name.

```python
box_metadata_template_create(client, display_name, fields, scope="enterprise") -> dict[str, Any]
```
Create a new metadata template.

#### Instance Operations

```python
box_metadata_get_instance_on_file(client, file_id, scope, template_key) -> dict[str, Any]
```
Get metadata instance from a file.

```python
box_metadata_set_instance_on_file(client, file_id, scope, template_key, metadata) -> dict[str, Any]
```
Apply metadata to a file.

```python
box_metadata_update_instance_on_file(client, file_id, scope, template_key, updates) -> dict[str, Any]
```
Update metadata on a file.

```python
box_metadata_delete_instance_on_file(client, file_id, scope, template_key) -> dict[str, Any]
```
Remove metadata from a file.

---

### User Management

```python
box_users_list(client, limit=1000) -> dict[str, Any]
```
List all users in the enterprise.

```python
box_users_locate_by_email(client, email) -> dict[str, Any]
```
Find user by email address.

```python
box_users_locate_by_name(client, name) -> dict[str, Any]
```
Find user by name.

```python
box_users_search_by_name_or_email(client, query) -> dict[str, Any]
```
Search users by name or email.

---

### Group Management

```python
box_groups_search(client, name) -> dict[str, Any]
```
Search for groups by name.

```python
box_groups_list_by_user(client, user_id) -> dict[str, Any]
```
List all groups a user belongs to.

```python
box_groups_list_members(client, group_id) -> dict[str, Any]
```
List all members of a group.

---

### Task Management

```python
box_task_file_list(client, file_id) -> dict[str, Any]
```
List all tasks on a file.

```python
box_task_details(client, task_id) -> dict[str, Any]
```
Get details about a specific task.

```python
box_task_review_create(client, file_id, message, due_at=None) -> dict[str, Any]
```
Create a review task on a file.

```python
box_task_complete_create(client, file_id, message, due_at=None) -> dict[str, Any]
```
Create a complete task on a file.

```python
box_task_update(client, task_id, message=None, due_at=None) -> dict[str, Any]
```
Update task details.

```python
box_task_remove(client, task_id) -> dict[str, Any]
```
Delete a task.

#### Task Assignments

```python
box_task_assignments_list(client, task_id) -> dict[str, Any]
```
List all assignments for a task.

```python
box_task_assignment_details(client, assignment_id) -> dict[str, Any]
```
Get details about a task assignment.

```python
box_task_assign_by_user_id(client, task_id, user_id) -> dict[str, Any]
```
Assign task to a user by ID.

```python
box_task_assign_by_email(client, task_id, email) -> dict[str, Any]
```
Assign task to a user by email.

```python
box_task_assignment_update(client, assignment_id, resolution_state, message=None) -> dict[str, Any]
```
Update task assignment status.

```python
box_task_assignment_remove(client, assignment_id) -> dict[str, Any]
```
Remove a task assignment.

---

### Document Generation (DocGen)

```python
box_docgen_create_single_file_from_user_input(client, template_file_id, output_name, output_folder_id, user_input) -> dict[str, Any]
```
Generate a document from template with user input.

```python
box_docgen_create_batch(client, template_file_id, output_folder_id, batch_inputs) -> dict[str, Any]
```
Generate multiple documents in batch.

```python
box_docgen_get_job_by_id(client, job_id) -> dict[str, Any]
```
Get status of a DocGen job.

```python
box_docgen_list_jobs(client, limit=100) -> dict[str, Any]
```
List all DocGen jobs.

```python
box_docgen_list_jobs_by_batch(client, batch_id) -> dict[str, Any]
```
List jobs for a specific batch.

#### DocGen Templates

```python
box_docgen_template_list(client) -> dict[str, Any]
```
List all DocGen templates.

```python
box_docgen_template_get_by_id(client, template_id) -> dict[str, Any]
```
Get DocGen template by ID.

```python
box_docgen_template_get_by_name(client, template_name) -> dict[str, Any]
```
Get DocGen template by name.

```python
box_docgen_template_create(client, name, file_id) -> dict[str, Any]
```
Create a new DocGen template.

```python
box_docgen_template_delete(client, template_id) -> dict[str, Any]
```
Delete a DocGen template.

```python
box_docgen_template_list_jobs(client, template_id) -> dict[str, Any]
```
List jobs for a specific template.

```python
box_docgen_template_list_tags(client, template_id) -> dict[str, Any]
```
List available tags in a template.

---

### Web Links

```python
box_web_link_create(client, url, parent_folder_id, name=None, description=None) -> dict[str, Any]
```
Create a web link in Box.

```python
box_web_link_get_by_id(client, web_link_id) -> dict[str, Any]
```
Get web link information.

```python
box_web_link_update_by_id(client, web_link_id, url=None, name=None, description=None) -> dict[str, Any]
```
Update web link properties.

```python
box_web_link_delete_by_id(client, web_link_id) -> dict[str, Any]
```
Delete a web link.

---

### Authentication

```python
get_ccg_client(client_id, client_secret, user_id=None, enterprise_id=None) -> BoxClient
```
Create authenticated Box client using Client Credentials Grant (CCG).

**Used in this project:** ✅ (via custom wrapper in [src/utils/box_api_auth.py](../src/utils/box_api_auth.py))

```python
get_oauth_client() -> BoxClient
```
Create authenticated Box client using OAuth 2.0.

```python
authorize_app(client_id, client_secret, redirect_uri) -> str
```
Start OAuth authorization flow.

```python
get_auth_config(config_file_path) -> dict
```
Load authentication config from file.

```python
get_ccg_config(config_file_path) -> CCGConfig
```
Load CCG configuration from file.

---

### Utility Classes

```python
class BoxFileExtended
```
Extended file object with additional metadata.

```python
class DocumentFiles
```
Container for document file collections.

```python
class ImageFiles
```
Container for image file collections.

---

## Integration with LangChain Tools

The toolkit functions are wrapped as LangChain tools in [src/agents/loan_underwriting/loan_tools.py](../src/agents/loan_underwriting/loan_tools.py):

```python
from langchain_core.tools import tool
from box_ai_agents_toolkit import box_ai_ask_file_multi, box_locate_folder_by_name

@tool(parse_docstring=True)
def search_loan_folder(applicant_name: str) -> str:
    """Locate loan application folder by applicant name.

    Args:
        applicant_name: Full name of the loan applicant

    Returns:
        Box folder ID containing applicant's documents
    """
    response = box_locate_folder_by_name(
        client=conf.box_client,
        folder_name=applicant_name,
    )
    # Process response and return folder ID
    return folder_id

@tool(parse_docstring=True)
def ask_box_ai_about_loan(folder_id: str, question: str) -> str:
    """Ask Box AI a question about loan application documents.

    Args:
        folder_id: Box folder ID containing loan documents
        question: Question to ask about the documents

    Returns:
        Box AI's response with information from documents
    """
    # Get file IDs from folder
    file_ids = get_file_ids_from_folder(folder_id)

    # Query Box AI
    response = box_ai_ask_file_multi(
        client=conf.box_client,
        file_ids=file_ids,
        prompt=question,
    )
    return format_response(response)
```

---

## Error Handling

All toolkit functions return dictionaries with either:

**Success:**
```python
{
    "folder": {...},  # Or "file", "AI_response", etc.
}
```

**Error:**
```python
{
    "error": "Error message description"
}
```

**Empty Result:**
```python
{
    "message": "No items found in folder."
}
```

---

## Dependencies

The toolkit requires:
- `box-sdk-gen` - Official Box Python SDK
- Standard library modules (typing, logging, etc.)

---

## Further Reading

- **Box AI Agents Toolkit GitHub** - [https://github.com/box-community/box-ai-agents-toolkit](https://github.com/box-community/box-ai-agents-toolkit)
- **Box AI Documentation** - https://developer.box.com/guides/box-ai/
- **Box Python SDK** - https://github.com/box/box-python-sdk-gen
- **This Project's Tool Wrappers** - [src/agents/loan_underwriting/loan_tools.py](../src/agents/loan_underwriting/loan_tools.py)
- **Custom Box Utilities** - [src/utils/box_api_generic.py](../src/utils/box_api_generic.py)

---

## Summary

The `box-ai-agents-toolkit` provides:

- **150+ functions** covering all major Box API operations
- **Box AI integration** - Ask, Extract, and AI agent management
- **Enterprise features** - Collaboration, metadata, tasks, DocGen
- **Simple interfaces** - Consistent return types, error handling
- **Agent-friendly** - Easy to wrap as LangChain tools

This project leverages the toolkit primarily for Box AI capabilities (Ask and Extract) combined with folder/file operations to build an intelligent loan underwriting system.
