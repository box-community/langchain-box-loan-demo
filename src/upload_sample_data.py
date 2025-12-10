import logging
from pathlib import Path
from typing import Dict

from box_sdk_gen import BoxAPIError, BoxClient
from box_sdk_gen.managers.folders import CreateFolderParent
from box_sdk_gen.managers.uploads import (
    UploadFileAttributes,
    UploadFileAttributesParentField,
    UploadFileVersionAttributes,
)

from config import config
from utils.box_api_auth import get_box_client
from utils.box_api_generic import (
    box_file_pre_flight_check,
    box_file_upload,
    box_file_update,
    box_folder_create,
    local_folder_upload,
)

logger = logging.getLogger(__name__)


def main() -> None:
    """Upload sample data to Box."""

    logger.info("Starting sample data upload process")

    try:
        # Get authenticated Box client
        client = get_box_client()
        logger.debug("Box client ready for upload operations")

        # Get the base folder ID from config
        base_folder_name = config.BOX_DEMO_FOLDER_NAME
        logger.info("Using base folder name: %s", base_folder_name)

        # Create or get the base folder in Box
        base_folder_id = box_folder_create(
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
        local_folder_upload(client, data_dir, base_folder_id, folder_cache)

        logger.info("Sample data upload completed successfully")

    except Exception as e:
        logger.error("Failed to upload sample data: %s", e, exc_info=True)
        raise


if __name__ == "__main__":
    main()
