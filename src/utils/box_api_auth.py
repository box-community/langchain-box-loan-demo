import logging

from box_sdk_gen import BoxAPIError, BoxClient, CCGConfig, BoxCCGAuth, FileTokenStorage
from app_config import conf

logger = logging.getLogger(__name__)


def get_box_client() -> BoxClient:
    """Authenticate and return a BoxClient instance.

    Returns:
        Authenticated BoxClient instance

    Raises:
        ValueError: If required configuration is missing or invalid
    """
    logger.debug("Initializing Box client authentication")

    # Validate configuration
    if conf.BOX_SUBJECT_TYPE not in {"user", "enterprise"}:
        logger.error("Invalid BOX_SUBJECT_TYPE: %s", conf.BOX_SUBJECT_TYPE)
        raise ValueError("BOX_SUBJECT_TYPE must be either 'user' or 'enterprise'.")

    if not conf.BOX_SUBJECT_ID:
        logger.error("BOX_SUBJECT_ID is missing")
        raise ValueError("BOX_SUBJECT_ID must be provided.")

    if not conf.BOX_CLIENT_ID or not conf.BOX_CLIENT_SECRET:
        logger.error("Box API credentials are missing")
        raise ValueError("BOX_CLIENT_ID and BOX_CLIENT_SECRET must be provided.")

    # Determine authentication type
    if conf.BOX_SUBJECT_TYPE == "user":
        user_id = conf.BOX_SUBJECT_ID
        enterprise_id = None
        logger.info("Authenticating as Box user: %s", user_id)
    else:
        user_id = None
        enterprise_id = conf.BOX_SUBJECT_ID
        logger.info("Authenticating as Box enterprise: %s", enterprise_id)

    # Configure token storage
    file_token_storage = FileTokenStorage(filename=".auth.ccg")
    logger.debug("Using file token storage: .auth.ccg")

    # Create CCG configuration
    ccg_config = CCGConfig(
        client_id=conf.BOX_CLIENT_ID,
        client_secret=conf.BOX_CLIENT_SECRET,
        user_id=user_id,
        enterprise_id=enterprise_id,
        token_storage=file_token_storage,
    )

    # Authenticate and create client
    auth = BoxCCGAuth(ccg_config)
    box_client = BoxClient(auth)

    # Try to get the information about the authenticated user or enterprise
    try:
        box_client.users.get_user_me()
    except BoxAPIError as e:
        logger.error("Failed to authenticate Box client: %s", e)
        raise e

    logger.info("Box client authenticated successfully")
    return box_client
