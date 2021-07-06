# directsql

API Server.


/whitelist
    /v1/get_settings.txt
        Return the config for the user
        ---
        SELECT *
        FROM user_settings
        WHERE user_id = :user_id
    /v1/get_notes.sql
        Return the user's notes (between 0 and 100 at a time)
        ---
        SELECT *
        FROM notes
        WHERE user_id = :user_id
        LIMIT :limit
        OFFSET :offset


# Queries with validation rules
queries = {
    "*": {
        "user_id": auth,
    }
    "v1/get_settings.txt": {
        "user_id": auth,
        "limit": validate_int(min=0, max=100)
    }
}


def auth(key: str, value: str, headers: dict, params: dict):
    if "user_id" not in params:
        return

    token = headers["Authorization"]
    user_id = get_user_id(token)
    if user_id == params["user_id"]:
        return validate_int()(key, value, headers, params)

    raise Unauthenticated("Invalid User ID.")


def validate_int(key, value, headers, params):
    if value is not int:
        raise InvalidParameter()


STARTUP:
    - Read each query
    - Process SQL -> Save as Stored Procedure
    - Ensure parameter names match validation rules


Rate limiting:
    - Rate limit at Nginx layer
