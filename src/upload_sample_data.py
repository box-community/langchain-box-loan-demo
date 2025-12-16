import logging
from pathlib import Path
from typing import Dict

from app_config import conf
from utils.box_api_auth import get_box_client
from utils.box_api_generic import (
    box_folder_create,
    local_folder_upload,
    save_upload_cache_to_json,
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
        base_folder_name = conf.BOX_DEMO_FOLDER_NAME
        logger.info("Using base folder name: %s", base_folder_name)

        # Create or get the base folder in Box
        base_folder_id = box_folder_create(
            client, base_folder_name, conf.BOX_DEMO_PARENT_FOLDER
        )

        # Get the data directory path
        data_dir = Path(__file__).parent.parent / "data"
        if not data_dir.exists():
            logger.error("Data directory not found: %s", data_dir)
            raise FileNotFoundError(f"Data directory not found: {data_dir}")

        logger.info("Uploading data from: %s", data_dir)

        # Cache for tracking uploaded files and folders
        folder_cache: Dict[str, Dict[str, str]] = {}
        local_folder_upload(client, data_dir, base_folder_id, folder_cache)

        # Memories folder is on the project folder
        memories_folder = Path(__file__).parent.parent.parent / "agents_memories"
        memories_folder.mkdir(parents=True, exist_ok=True)
        # Save the upload cache to a JSON file
        cache_file = memories_folder / "box_upload_cache.json"
        save_upload_cache_to_json(folder_cache, cache_file)

        logger.info("Sample data upload completed successfully")
        logger.info("Uploaded %d items (files and folders)", len(folder_cache))

    except Exception as e:
        logger.error("Failed to upload sample data: %s", e, exc_info=True)
        raise


if __name__ == "__main__":
    main()
