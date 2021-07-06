from directsql import (
    create_application,
    Query,
    sqlite3_executor,
    InvalidParameters,
    validate_int,
    validate_one,
)
from pathlib import Path
import logging
import warnings

logging.basicConfig(level=logging.DEBUG)
warnings.simplefilter("always")


def auth(key, values, headers) -> int:
    result = validate_int()(key, values)
    if headers.get("HTTP_TOKEN") != str(result):
        raise InvalidParameters("token does not match user_id")

    return result


queries = [
    Query(
        file=Path("v1/users/post.md"),
        schema={},
    ),
    Query(
        file=Path("get_settings.md"),
        schema={
            "user_id": auth,
        },
    ),
    Query(
        file=Path("post_settings.md"),
        schema={
            "user_id": auth,
            "enable_dark_mode": validate_one,
        },
    ),
    Query(
        file=Path("v1/get_lists.md"),
        schema={
            "user_id": auth,
        },
    ),
    Query(
        file=Path("misc/get_foreign_keys.md"),
        schema={},
    ),
]


BASE_PATH = Path(__file__).parent

application = create_application(
    base=(BASE_PATH / "sql").absolute(),
    queries=queries,
    executor=sqlite3_executor(
        file=BASE_PATH / "db.sqlite3",
        num_statements=len(queries),
    ),
)
