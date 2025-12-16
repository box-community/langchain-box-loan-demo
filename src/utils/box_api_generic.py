import json
import logging
from pathlib import Path
from typing import Dict, Optional

from box_sdk_gen import (
    BoxAPIError,
    BoxClient,
    CreateFolderParent,
    PreflightFileUploadCheckParent,
    UploadFileAttributes,
    UploadFileAttributesParentField,
    UploadFileVersionAttributes,
    UploadUrl,
)

logger = logging.getLogger(__name__)


def box_file_pre_flight_check(
    client: BoxClient, local_file_name: Path, parent_folder_id: str
) -> tuple[bool, Optional[str], Optional[UploadUrl]]:
    """
    Checks if a file can be uploaded to Box.
    Possible errors include conflicts with existing files, lack of storage space, or insufficient permissions.
    If there is a conflict, the existing file ID is returned.
    Args:
        client (BoxClient): The Box client instance.
        local_file_name (str): The name of the local file to be uploaded.
        local_file_size (int): The size of the local file in bytes.
        parent_folder_id (str): The ID of the parent folder in Box.

    Returns:
        tuple[bool, Optional[str], Optional[UploadUrl]]: A tuple containing a boolean indicating if the file can be uploaded,
        the existing file ID if there is a conflict, and the upload URL if the file can be uploaded.

    """
    parent = PreflightFileUploadCheckParent(id=parent_folder_id)
    local_file_size = local_file_name.stat().st_size
    try:
        upload_url = client.uploads.preflight_file_upload_check(
            name=local_file_name.name, size=local_file_size, parent=parent
        )
        return True, None, upload_url
    except BoxAPIError as e:
        # Check if file already exists (conflict error)
        if (
            e.response_info.status_code == 409
            and e.response_info.code == "item_name_in_use"
        ):
            logger.debug(
                "File '%s' already exists, uploading new version", local_file_name
            )

            # Get the existing file ID from the error details
            if (
                e.response_info.context_info
                and "conflicts" in e.response_info.context_info
            ):
                file_id = e.response_info.context_info["conflicts"]["id"]
                return False, file_id, None
            else:
                raise ValueError("Conflict error without conflict details")
        else:
            # Reraise the exception if it's not a conflict error
            raise e


def box_file_upload(
    client: BoxClient, local_file_path: Path, box_folder_parent_id: str
) -> str:
    """
    Upload a file to Box.

    Args:
        client: Authenticated Box client
        local_file_path: Path to the local file to upload
        box_folder_parent_id: ID of the parent folder in Box

    Returns:
        str: ID of the uploaded file
    """
    attributes = UploadFileAttributes(
        name=local_file_path.name,
        parent=UploadFileAttributesParentField(id=box_folder_parent_id),
    )

    try:
        with open(local_file_path, "rb") as file_stream:
            files = client.uploads.upload_file(attributes=attributes, file=file_stream)
            if files.entries:
                return files.entries[0].id
            else:
                raise ValueError("No file entries returned from Box API")
    except BoxAPIError as e:
        logger.error("Failed to upload file '%s': %s", local_file_path, e)
        raise e


def box_file_update(client: BoxClient, file_id: str, local_file_path: Path) -> str:
    """
    Update a file in Box.

    Args:
        client: Authenticated Box client
        file_id: ID of the file to update
        local_file_path: Path to the local file to upload

    Returns:
        str: ID of the updated file
    """
    attributes = UploadFileVersionAttributes(name=local_file_path.name)
    try:
        with open(local_file_path, "rb") as file_stream:
            files = client.uploads.upload_file_version(
                file_id=file_id, attributes=attributes, file=file_stream
            )
            if files.entries:
                return files.entries[0].id
            else:
                raise ValueError("No file entries returned from Box API")
    except BoxAPIError as e:
        logger.error("Failed to update file '%s': %s", local_file_path, e)
        raise e


def box_folder_create(
    client: BoxClient, folder_name: str, parent_folder_id: str
) -> str:
    """
    Create a folder in Box.

    Args:
        client: Authenticated Box client
        folder_name: Name of the folder to create
        parent_folder_id: ID of the parent folder in Box

    Returns:
        str: ID of the created or existing folder
    """
    try:
        folder = client.folders.create_folder(
            name=folder_name,
            parent=CreateFolderParent(id=parent_folder_id),
        )
        return folder.id
    except BoxAPIError as e:
        # Check if folder already exists (conflict error)
        if (
            e.response_info.status_code == 409
            and e.response_info.code == "item_name_in_use"
        ):
            # get the conflicting folder ID from the error details
            existing_folder_id = e.response_info.body["context_info"]["conflicts"][0][
                "id"
            ]
            return existing_folder_id
        else:
            logger.error("Failed to create folder '%s': %s", folder_name, e)
            raise e


def save_upload_cache_to_json(
    folder_cache: Dict[str, Dict[str, str]], output_file: Path
) -> None:
    """Save the upload cache to a JSON file.

    Args:
        folder_cache: Dictionary mapping local paths to Box item metadata
        output_file: Path to the JSON file to write
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(folder_cache, f, indent=2, ensure_ascii=False)
    logger.info("Upload cache saved to: %s", output_file)


def local_folder_upload(
    client: BoxClient,
    local_dir: Path,
    parent_folder_id: str,
    folder_cache: Dict[str, Dict[str, str]],
) -> None:
    """Recursively upload a directory and its contents to Box.

    Args:
        client: Authenticated Box client
        local_dir: Path to the local directory to upload
        parent_folder_id: ID of the parent folder in Box
        folder_cache: Dictionary to track uploaded items with their Box IDs
                     Structure: {path: {"name": str, "type": "file"|"folder", "id": str}}
    """
    # clip local_dir str to start at data/
    local_dir_str = str(local_dir)
    if "data/" in local_dir_str:
        local_dir_str = local_dir_str.split("langchain-box-loan-demo/")[-1]
    logger.info("Processing folder: %s", local_dir_str)

    # Process all items in the directory
    for item in local_dir.iterdir():
        if item.is_file():
            # skip files starting with .
            if item.name.startswith("."):
                continue
            (can_upload, conflict_file_id, _) = box_file_pre_flight_check(
                client, item, parent_folder_id
            )
            if can_upload:
                file_id = box_file_upload(client, item, parent_folder_id)
                logger.info("Uploaded file: %s", item.name)
                # Track the uploaded file
                folder_cache[str(item)] = {
                    "name": item.name,
                    "type": "file",
                    "id": file_id,
                }
            elif conflict_file_id:
                file_id = box_file_update(client, conflict_file_id, item)
                logger.info("Updated file: %s", item.name)
                # Track the updated file
                folder_cache[str(item)] = {
                    "name": item.name,
                    "type": "file",
                    "id": file_id,
                }
        elif item.is_dir():
            new_folder_id = box_folder_create(client, item.name, parent_folder_id)
            logger.info("Created folder: %s", item.name)
            # Track the created folder
            folder_cache[str(item)] = {
                "name": item.name,
                "type": "folder",
                "id": new_folder_id,
            }
            # Recursively process subdirectory
            local_folder_upload(client, item, new_folder_id, folder_cache)


def local_file_upload(
    client: BoxClient,
    local_file_path: Path,
    parent_folder_id: str,
) -> str:
    """Upload a single file to Box.

    Args:
        client: Authenticated Box client
        local_file_path: Path to the local file to upload
        parent_folder_id: ID of the parent folder in Box
        folder_cache: Dictionary to track uploaded items with their Box IDs
                     Structure: {path: {"name": str, "type": "file"|"folder", "id": str}}
    """
    try:
        (can_upload, conflict_file_id, _) = box_file_pre_flight_check(
            client, local_file_path, parent_folder_id
        )

        if can_upload:
            file_id = box_file_upload(client, local_file_path, parent_folder_id)
            logger.info("Uploaded file: %s", local_file_path.name)

        elif conflict_file_id:
            file_id = box_file_update(client, conflict_file_id, local_file_path)
            logger.info("Updated file: %s", local_file_path.name)
        else:
            raise ValueError("Unable to determine upload status for file.")

        return file_id
    except BoxAPIError as e:
        logger.error("Failed to upload/update file '%s': %s", local_file_path, e)
        raise e
