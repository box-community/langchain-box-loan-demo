from utils.box_api_auth import get_box_client
from app_config import conf
from box_sdk_gen import BoxAPIError, BoxClient


def test_utils_box_auth_get_box_client():
    box_client = get_box_client()
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
    original_subject_type = conf.BOX_SUBJECT_TYPE
    original_subject_id = conf.BOX_SUBJECT_ID
    original_client_id = conf.BOX_CLIENT_ID
    original_client_secret = conf.BOX_CLIENT_SECRET

    try:
        conf.BOX_SUBJECT_TYPE = "invalid_type"
        try:
            get_box_client()
            assert False, "Expected ValueError for invalid BOX_SUBJECT_TYPE"
        except ValueError as e:
            assert str(e) == "BOX_SUBJECT_TYPE must be either 'user' or 'enterprise'."

        # reset config
        conf.BOX_SUBJECT_TYPE = original_subject_type
        conf.BOX_SUBJECT_TYPE = None  # type: ignore
        try:
            get_box_client()
            assert False, "Expected ValueError for missing BOX_SUBJECT_TYPE"
        except ValueError as e:
            assert str(e) == "BOX_SUBJECT_TYPE must be either 'user' or 'enterprise'."

        # reset config
        conf.BOX_SUBJECT_TYPE = original_subject_type
        conf.BOX_CLIENT_ID = None  # type: ignore
        try:
            get_box_client()
            assert False, "Expected ValueError for missing BOX_CLIENT_ID"
        except ValueError as e:
            assert str(e) == "BOX_CLIENT_ID and BOX_CLIENT_SECRET must be provided."

        # reset config
        conf.BOX_CLIENT_ID = original_client_id
        conf.BOX_CLIENT_SECRET = None  # type: ignore
        try:
            get_box_client()
            assert False, "Expected ValueError for missing BOX_CLIENT_SECRET"
        except ValueError as e:
            assert str(e) == "BOX_CLIENT_ID and BOX_CLIENT_SECRET must be provided."

        # reset config
        conf.BOX_CLIENT_SECRET = original_client_secret
        conf.BOX_SUBJECT_ID = None  # type: ignore
        try:
            get_box_client()
            assert False, "Expected ValueError for missing BOX_SUBJECT_ID"
        except ValueError as e:
            assert str(e) == "BOX_SUBJECT_ID must be provided."

        # reset config and test enterprise
        conf.BOX_SUBJECT_ID = original_subject_id
        conf.BOX_SUBJECT_TYPE = "enterprise"
        conf.BOX_SUBJECT_ID = "ABCD"

        get_box_client()
    finally:
        # Restore original config values
        conf.BOX_SUBJECT_TYPE = original_subject_type
        conf.BOX_SUBJECT_ID = original_subject_id
        conf.BOX_CLIENT_ID = original_client_id
        conf.BOX_CLIENT_SECRET = original_client_secret
