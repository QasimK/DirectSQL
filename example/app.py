from directsql import (
    create_application,
    Query,
    sqlite3_executor,
    InvalidParameters,
    validate_int,
    validate_one,
)
from typing import Tuple
from pathlib import Path
import base64
import logging
import warnings

logging.basicConfig(level=logging.DEBUG)
warnings.simplefilter("always")


def user_auth_by_authorization_header(query_params, headers) -> int:
    # raise InvalidParameters("token does not match user_id")
    auth_header = headers.get("AUTHORIZATION", b"")
    scheme, _, value = auth_header.partition(" ")
    assert scheme == "Basic"
    auth_bytes = base64.standard_b64decode(value)
    auth_string = auth_bytes.decode("utf-8")
    raw_user_id, _, auth_password = auth_string.partition(":")
    auth_user_id = validate_int(ge=1)("AUTHORIZATION", [raw_user_id], headers)
    return {
        "auth_user_id": auth_user_id,
        "auth_password": auth_password,
    }

    return result


def session_auth_by_authorization_header(query_params, headers) -> int:
    # raise InvalidParameters("token does not match user_id")
    auth_header = headers.get("AUTHORIZATION", b"")
    scheme, _, value = auth_header.partition(" ")
    assert scheme == "Basic"
    auth_bytes = base64.standard_b64decode(value)
    auth_string = auth_bytes.decode("utf-8")
    raw_user_id, _, auth_token = auth_string.partition(":")
    auth_user_id = validate_int(ge=1)("AUTHORIZATION", [raw_user_id], headers)
    return {
        "auth_user_id": auth_user_id,
        "auth_token": auth_token,
    }

    return result


BASE_PATH = Path(__file__).parent

queries = [
    Query(
        file=Path("v1/users/post.md"),
        schema={
            "password": validate_one,
        },
        param_mappings=[],
    ),
    #
    # --------
    # Sessions
    # --------
    Query(
        file=Path("v1/sessions/post.md"),
        schema={
            "token": validate_one,
        },
        param_mappings=[user_auth_by_authorization_header],
    ),
    Query(
        file=Path("v1/sessions/get.md"),
        schema={},
        param_mappings=[session_auth_by_authorization_header],
    ),
    Query(
        file=Path("v1/sessions/delete.md"),
        schema={
            "session_id": validate_int(ge=1),
        },
        param_mappings=[user_auth_by_authorization_header],
    ),
    #
    # -----
    # Lists
    # -----
    Query(
        file=Path("v1/lists/post.md"),
        schema={
            "title": validate_one,
        },
        param_mappings=[session_auth_by_authorization_header],
    ),
    #
    # -----
    # MISC
    # -----
    Query(
        file=Path("misc/get_foreign_keys.md"),
        schema={},
        param_mappings=[],
    ),
]

application = create_application(
    base=(BASE_PATH / "sql").absolute(),
    queries=queries,
    executor=sqlite3_executor(
        file=BASE_PATH / "db.sqlite3",
        num_statements=len(queries),
    ),
)
