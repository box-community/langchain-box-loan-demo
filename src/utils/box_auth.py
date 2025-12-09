from box_sdk_gen import BoxClient, CCGConfig, BoxCCGAuth, FileTokenStorage
from config import Config
from utils.logging_config import get_logger

logger = get_logger(__name__)


def get_box_client(config: Config) -> BoxClient:
    """Authenticate and return a BoxClient instance.

    Args:
        config: Configuration object with Box API credentials

    Returns:
        Authenticated BoxClient instance

    Raises:
        ValueError: If required configuration is missing or invalid
    """
    logger.debug("Initializing Box client authentication")

    # Validate configuration
    if config.BOX_SUBJECT_TYPE not in {"user", "enterprise"}:
        logger.error("Invalid BOX_SUBJECT_TYPE: %s", config.BOX_SUBJECT_TYPE)
        raise ValueError("BOX_SUBJECT_TYPE must be either 'user' or 'enterprise'.")

    if not config.BOX_SUBJECT_ID:
        logger.error("BOX_SUBJECT_ID is missing")
        raise ValueError("BOX_SUBJECT_ID must be provided.")

    if not config.BOX_CLIENT_ID or not config.BOX_CLIENT_SECRET:
        logger.error("Box API credentials are missing")
        raise ValueError("BOX_CLIENT_ID and BOX_CLIENT_SECRET must be provided.")

    # Determine authentication type
    if config.BOX_SUBJECT_TYPE == "user":
        user_id = config.BOX_SUBJECT_ID
        enterprise_id = None
        logger.info("Authenticating as Box user: %s", user_id)
    else:
        user_id = None
        enterprise_id = config.BOX_SUBJECT_ID
        logger.info("Authenticating as Box enterprise: %s", enterprise_id)

    # Configure token storage
    file_token_storage = FileTokenStorage(filename=".auth.ccg")
    logger.debug("Using file token storage: .auth.ccg")

    # Create CCG configuration
    ccg_config = CCGConfig(
        client_id=config.BOX_CLIENT_ID,
        client_secret=config.BOX_CLIENT_SECRET,
        user_id=user_id,
        enterprise_id=enterprise_id,
        token_storage=file_token_storage,
    )

    # Authenticate and create client
    auth = BoxCCGAuth(ccg_config)
    box_client = BoxClient(auth)

    logger.info("Box client authenticated successfully")
    return box_client
