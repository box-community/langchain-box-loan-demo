from pathlib import Path
from typing import Dict

from box_sdk_gen import BoxAPIError, BoxClient
from box_sdk_gen.managers.folders import CreateFolderParent
from box_sdk_gen.managers.uploads import (
    UploadFileAttributes,
    UploadFileAttributesParentField,
    UploadFileVersionAttributes,
)

from config import Config
from utils.box_auth import get_box_client
from utils.logging_config import get_logger, setup_logging

logger = get_logger(__name__)


def get_or_create_folder(
    client: BoxClient, folder_name: str, parent_folder_id: str
) -> str:
    """Get or create a folder in Box.

    Args:
        client: Authenticated Box client
        folder_name: Name of the folder to create
        parent_folder_id: ID of the parent folder

    Returns:
        Folder ID of the existing or newly created folder

    Raises:
        BoxAPIError: If folder creation fails for reasons other than already existing
    """
    try:
        logger.debug(
            "Creating folder '%s' in parent folder %s", folder_name, parent_folder_id
        )
        folder = client.folders.create_folder(
            name=folder_name,
            parent=CreateFolderParent(id=parent_folder_id),
        )
        logger.info("Created folder '%s' with ID: %s", folder_name, folder.id)
        return folder.id
    except BoxAPIError as e:
        # Check if folder already exists (conflict error)
        if (
            e.response_info.status_code == 409
            and e.response_info.code == "item_name_in_use"
        ):
            logger.debug(
                "Folder '%s' already exists, retrieving folder ID", folder_name
            )

            # get the conflicting folder ID from the error details
            existing_folder_id = e.response_info.body["context_info"]["conflicts"][0][
                "id"
            ]

            return existing_folder_id
        else:
            logger.error("Failed to create folder '%s': %s", folder_name, e)
            raise


def upload_file(client: BoxClient, file_path: Path, folder_id: str) -> None:
    """Upload a file to Box, replacing if it already exists.

    Args:
        client: Authenticated Box client
        file_path: Path to the file to upload
        folder_id: ID of the folder to upload to

    Raises:
        BoxAPIError: If file upload fails
    """
    file_name = file_path.name

    # Skip .DS_Store files
    if file_name == ".DS_Store":
        logger.debug("Skipping .DS_Store file: %s", file_path)
        return

    try:
        logger.debug("Uploading file '%s' to folder %s", file_name, folder_id)

        with open(file_path, "rb") as file_stream:
            attributes = UploadFileAttributes(
                name=file_name,
                parent=UploadFileAttributesParentField(id=folder_id),
            )
            files = client.uploads.upload_file(
                attributes=attributes,
                file=file_stream,
            )
            uploaded_file = files.entries[0]
            logger.info("Uploaded file '%s' with ID: %s", file_name, uploaded_file.id)

    except BoxAPIError as e:
        # Check if file already exists (conflict error)
        if (
            e.response_info.status_code == 409
            and e.response_info.code == "item_name_in_use"
        ):
            logger.debug("File '%s' already exists, uploading new version", file_name)

            # Get the existing file ID from the error details
            file_id = e.response_info.context_info["conflicts"]["id"]

            with open(file_path, "rb") as file_stream:
                # upload a new file version
                attributes = UploadFileVersionAttributes(
                    name=file_name,
                )
                files = client.uploads.upload_file_version(
                    file_id=file_id,
                    attributes=attributes,
                    file=file_stream,
                )
                uploaded_file = files.entries[0]
                logger.info(
                    "Uploaded file '%s' with ID: %s", file_name, uploaded_file.id
                )
            return

        else:
            logger.error("Failed to upload file '%s': %s", file_name, e)
            raise


def upload_directory(
    client: BoxClient,
    local_dir: Path,
    parent_folder_id: str,
    folder_cache: Dict[str, str],
) -> None:
    """Recursively upload a directory and its contents to Box.

    Args:
        client: Authenticated Box client
        local_dir: Path to the local directory to upload
        parent_folder_id: ID of the parent folder in Box
        folder_cache: Cache of folder paths to Box folder IDs
    """
    logger.info("Processing directory: %s", local_dir)

    # Create or get the current folder in Box
    folder_name = local_dir.name
    cache_key = str(local_dir)

    if cache_key in folder_cache:
        current_folder_id = folder_cache[cache_key]
    else:
        current_folder_id = get_or_create_folder(client, folder_name, parent_folder_id)
        folder_cache[cache_key] = current_folder_id

    # Process all items in the directory
    for item in local_dir.iterdir():
        if item.is_file():
            upload_file(client, item, current_folder_id)
        elif item.is_dir():
            upload_directory(client, item, current_folder_id, folder_cache)


def main() -> None:
    """Upload sample data to Box."""
    # Load configuration
    config = Config()  # pyright: ignore[reportCallIssue]

    # Initialize logging
    setup_logging(level=config.LOG_LEVEL, log_file=config.LOG_FILE)

    logger.info("Starting sample data upload process")

    try:
        # Get authenticated Box client
        client = get_box_client(config=config)
        logger.debug("Box client ready for upload operations")

        # Get the base folder ID from config
        base_folder_name = config.BOX_DEMO_FOLDER_NAME
        logger.info("Using base folder name: %s", base_folder_name)

        # Create or get the base folder in Box
        base_folder_id = get_or_create_folder(
            client, base_folder_name, config.BOX_DEMO_PARENT_FOLDER
        )

        # Get the data directory path
        data_dir = Path(__file__).parent.parent / "data"
        if not data_dir.exists():
            logger.error("Data directory not found: %s", data_dir)
            raise FileNotFoundError(f"Data directory not found: {data_dir}")

        logger.info("Uploading data from: %s", data_dir)

        # Cache for folder IDs to avoid redundant lookups
        folder_cache: Dict[str, str] = {}

        # Upload all subdirectories in the data folder
        for item in data_dir.iterdir():
            if item.is_dir():
                upload_directory(client, item, base_folder_id, folder_cache)
            elif item.is_file():
                # Upload files in the root data directory
                upload_file(client, item, base_folder_id)

        logger.info("Sample data upload completed successfully")

    except Exception as e:
        logger.error("Failed to upload sample data: %s", e, exc_info=True)
        raise


if __name__ == "__main__":
    main()
