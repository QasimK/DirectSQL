from directsql import (
    create_application,
    required,
    Query,
    sqlite3_executor,
    InvalidParameters,
    max_last_modified_str,
    integer,
    integers,
    one,
    from_querystring,
    from_header,
    compose,
    str_list,
)
from typing import Tuple, List
from pathlib import Path
import base64
import logging
import warnings

logging.basicConfig(level=logging.DEBUG)
warnings.simplefilter("always")


def user_auth_by_authorization_header(query_params, headers) -> int:
    # raise InvalidParameters("password does not match user_id")
    auth_header = headers.get("AUTHORIZATION", b"")
    scheme, _, value = auth_header.partition(" ")
    assert scheme == "Basic"
    auth_bytes = base64.standard_b64decode(value)
    auth_string = auth_bytes.decode("utf-8")
    raw_user_id, _, auth_password = auth_string.partition(":")
    _, auth_user_id = integer(ge=1)(("Authorization", raw_user_id))
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
    _, auth_user_id = integer(ge=1)(("Authorization", raw_user_id))
    return {
        "auth_user_id": auth_user_id,
        "auth_token": auth_token,
    }

    return result


BASE_PATH = Path(__file__).parent

queries = [
    #
    # -----
    # Users
    # -----
    Query(
        file=Path("v1/users/post.md"),
        schema={
            "password": compose(one, required, from_querystring("password")),
            "name": compose(one, required, from_querystring("name")),
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
            "token": compose(one, required, from_header("Token")),
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
            "session_id": compose(
                integer(ge=1), one, required, from_querystring("session_id")
            ),
        },
        param_mappings=[user_auth_by_authorization_header],
    ),
    #
    # -----
    # Lists
    # -----
    Query(
        file=Path("v1/lists/post.md"),
        schema={"title": compose(one, required, from_querystring("title"))},
        param_mappings=[session_auth_by_authorization_header],
    ),
    Query(
        file=Path("v1/lists/get.md"),
        schema={
            "str_list_ids": compose(
                str_list, integers(ge=1), from_querystring("list_id")
            ),
        },
        param_mappings=[session_auth_by_authorization_header],
        last_modified=max_last_modified_str("last_modified"),
    ),
    Query(
        file=Path("v1/lists/put.md"),
        schema={
            "list_id": compose(
                integer(ge=1), one, required, from_querystring("list_id")
            ),
            "title": compose(one, from_querystring("title")),
            "last_modified": compose(one, required, from_querystring("last_modified")),
        },
        param_mappings=[session_auth_by_authorization_header],
    ),
    Query(
        file=Path("v1/lists/delete.md"),
        schema={
            "str_list_ids": compose(
                str_list, integers(ge=1), required, from_querystring("list_id")
            ),
        },
        param_mappings=[session_auth_by_authorization_header],
    ),
    #
    # -----
    # Items
    # -----
    # ...
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

# from werkzeug.middleware.profiler import ProfilerMiddleware
# application = ProfilerMiddleware(application, profile_dir=str(BASE_PATH))
