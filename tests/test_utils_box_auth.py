from utils.box_auth import get_box_client
from config import Config
from box_sdk_gen import BoxAPIError, BoxClient


def test_utils_box_auth_get_box_client():
    config = Config()  # pyright: ignore[reportCallIssue]
    box_client = get_box_client(config)
    assert isinstance(box_client, BoxClient)

    # Test currently logged in user
    try:
        user_info = box_client.users.get_user_me()
    except BoxAPIError as e:
        assert False, f"BoxAPIError occurred: {e}"
    assert "id" in user_info.to_dict()
    assert "login" in user_info.to_dict()


def test_utils_box_auth_client_invalid_configurations():
    # Test invalid subject type
    config = Config()  # pyright: ignore[reportCallIssue]

    config.BOX_SUBJECT_TYPE = "invalid_type"
    try:
        get_box_client(config)
        assert False, "Expected ValueError for invalid BOX_SUBJECT_TYPE"
    except ValueError as e:
        assert str(e) == "BOX_SUBJECT_TYPE must be either 'user' or 'enterprise'."

    # reset config
    config = Config()  # pyright: ignore[reportCallIssue]
    config.BOX_SUBJECT_TYPE = None
    try:
        get_box_client(config)
        assert False, "Expected ValueError for missing BOX_SUBJECT_TYPE"
    except ValueError as e:
        assert str(e) == "BOX_SUBJECT_TYPE must be either 'user' or 'enterprise'."

    # reset config
    config = Config()  # pyright: ignore[reportCallIssue]
    config.BOX_CLIENT_ID = None
    try:
        get_box_client(config)
        assert False, "Expected ValueError for missing BOX_CLIENT_ID"
    except ValueError as e:
        assert str(e) == "BOX_CLIENT_ID and BOX_CLIENT_SECRET must be provided."

    # reset config
    config = Config()  # pyright: ignore[reportCallIssue]
    config.BOX_CLIENT_SECRET = None
    try:
        get_box_client(config)
        assert False, "Expected ValueError for missing BOX_CLIENT_SECRET"
    except ValueError as e:
        assert str(e) == "BOX_CLIENT_ID and BOX_CLIENT_SECRET must be provided."

    # reset config
    config = Config()  # pyright: ignore[reportCallIssue]
    config.BOX_SUBJECT_ID = None
    try:
        get_box_client(config)
        assert False, "Expected ValueError for missing BOX_SUBJECT_ID"
    except ValueError as e:
        assert str(e) == "BOX_SUBJECT_ID must be provided."

    # reset config
    config = Config()  # pyright: ignore[reportCallIssue]
    config.BOX_SUBJECT_TYPE = "enterprise"
    config.BOX_SUBJECT_ID = "ABCD"

    get_box_client(config)
